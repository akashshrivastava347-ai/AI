"""Confidence calibration and routing.

Overall confidence is the product of three independent signals, as specified in
docs/01-AGENTIC-ARCHITECTURE.md:

    model self-assessment  x  resolver certainty  x  field completeness

Multiplicative rather than additive on purpose. A record can be beautifully
extracted and still useless if nobody knows which machine it belongs to, and an
average would hide that. A near-zero in any one factor must sink the whole score.
"""

from __future__ import annotations

from dataclasses import dataclass

from logsense_ai.extraction.schema import CORE_FIELDS, ExtractedFields
from logsense_ai.resolution.resolver import ResolutionOutcome

# Relative importance when averaging the model's own per-field confidence.
_FIELD_WEIGHTS: dict[str, float] = {
    "machine_text": 0.40,
    "failure_mode": 0.30,
    "action": 0.20,
    "downtime_hours": 0.05,
    "parts": 0.05,
}


@dataclass(slots=True)
class RoutingDecision:
    overall_confidence: float
    model_confidence: float
    resolution_confidence: float
    completeness: float
    auto_approve: bool
    reasons: list[str]


def _model_confidence(fields: ExtractedFields) -> float:
    total_weight = 0.0
    accumulated = 0.0
    for name, weight in _FIELD_WEIGHTS.items():
        # Only score fields the model actually produced. Penalising absent optional
        # fields would push every terse-but-correct message into the review queue.
        value = getattr(fields, name, None)
        if value in (None, [], ""):
            continue
        accumulated += fields.confidence_for(name) * weight
        total_weight += weight
    if total_weight == 0.0:
        return 0.0
    return round(accumulated / total_weight, 4)


def _completeness(fields: ExtractedFields) -> float:
    present = sum(1 for name in CORE_FIELDS if getattr(fields, name, None))
    return round(present / len(CORE_FIELDS), 4)


def score_and_route(
    fields: ExtractedFields,
    resolution: ResolutionOutcome,
    *,
    threshold: float,
) -> RoutingDecision:
    model_conf = _model_confidence(fields)
    completeness = _completeness(fields)
    overall = round(model_conf * resolution.confidence * completeness, 4)

    reasons: list[str] = []
    if not resolution.resolved:
        reasons.append(
            f"machine_unresolved: no asset matched {fields.machine_text!r} "
            f"(best score {resolution.confidence:.2f})"
        )
    elif resolution.is_ambiguous:
        top = resolution.candidates[0]
        runner = resolution.candidates[1]
        reasons.append(
            f"machine_ambiguous: {top.machine_name} ({top.score:.2f}) vs "
            f"{runner.machine_name} ({runner.score:.2f})"
        )

    for name in fields.missing_core_fields():
        reasons.append(f"missing_{name}")

    for name in ("machine_text", "failure_mode", "action"):
        if getattr(fields, name, None) and fields.confidence_for(name) < 0.70:
            reasons.append(f"low_confidence_{name}: {fields.confidence_for(name):.2f}")

    if fields.downtime_hours is None:
        # Not a blocker on its own: plenty of valid records state no duration. It is
        # recorded so coverage reporting stays honest about what totals are built on.
        reasons.append("downtime_absent")

    # Ambiguity blocks auto-approval regardless of arithmetic: two plausible machines
    # is exactly the case a human resolves in one click and a machine resolves wrongly.
    auto_approve = overall >= threshold and resolution.resolved and not resolution.is_ambiguous
    if not auto_approve and overall < threshold:
        reasons.insert(0, f"below_threshold: {overall:.2f} < {threshold:.2f}")

    return RoutingDecision(
        overall_confidence=overall,
        model_confidence=model_conf,
        resolution_confidence=resolution.confidence,
        completeness=completeness,
        auto_approve=auto_approve,
        reasons=reasons,
    )
