"""The extraction contract and the confidence/routing calculation."""

from __future__ import annotations

import pytest

from logsense_ai.domain.enums import ResolutionMethod
from logsense_ai.extraction.schema import ExtractedFields
from logsense_ai.ingest.scoring import score_and_route
from logsense_ai.resolution.resolver import MachineCandidate, ResolutionOutcome


def _resolved(score: float = 0.95) -> ResolutionOutcome:
    return ResolutionOutcome(
        "machine-1",
        score,
        ResolutionMethod.FUZZY,
        [
            MachineCandidate(
                "machine-1", "Line 3 Conveyor Motor", "C1", score, ResolutionMethod.FUZZY
            )
        ],
    )


def _ambiguous() -> ResolutionOutcome:
    return ResolutionOutcome(
        "machine-1",
        0.95,
        ResolutionMethod.FUZZY,
        [
            MachineCandidate("machine-1", "Conveyor Motor", "C1", 0.95, ResolutionMethod.FUZZY),
            MachineCandidate("machine-2", "Conveyor Gearbox", "C2", 0.95, ResolutionMethod.FUZZY),
        ],
    )


def _good_fields() -> ExtractedFields:
    return ExtractedFields(
        machine_text="Line 3 conveyor motor",
        failure_mode="Bearing Failure",
        action="Bearing replaced",
        downtime_hours=2.0,
        field_confidence={
            "machine_text": 0.95,
            "failure_mode": 0.95,
            "action": 0.9,
            "downtime_hours": 0.9,
        },
    )


# --- schema -------------------------------------------------------------------------


def test_parts_are_normalised_and_deduplicated() -> None:
    fields = ExtractedFields.model_validate({"parts": ["6205 zz", "6205ZZ", " skf-6205 "]})
    assert fields.parts == ["6205ZZ", "SKF-6205"]


def test_confidence_scores_are_clamped() -> None:
    """A model reporting 1.4 confidence is not more certain, it is wrong."""
    fields = ExtractedFields.model_validate(
        {"field_confidence": {"machine_text": 1.4, "action": -0.5, "parts": "nonsense"}}
    )
    assert fields.field_confidence == {"machine_text": 1.0, "action": 0.0}


def test_downtime_phrase_is_coerced_not_discarded() -> None:
    fields = ExtractedFields.model_validate({"downtime_hours": "2 ghante"})
    assert fields.downtime_hours == pytest.approx(2.0)


def test_unparseable_downtime_becomes_null_not_a_guess() -> None:
    assert ExtractedFields.model_validate({"downtime_hours": "kuch der"}).downtime_hours is None


def test_negative_downtime_is_rejected() -> None:
    with pytest.raises(ValueError):
        ExtractedFields(downtime_hours=-1)


def test_missing_core_fields_are_reported() -> None:
    assert ExtractedFields().missing_core_fields() == ["machine_text", "failure_mode", "action"]


# --- scoring ------------------------------------------------------------------------


def test_complete_confident_extraction_auto_approves() -> None:
    decision = score_and_route(_good_fields(), _resolved(), threshold=0.80)
    assert decision.auto_approve
    assert decision.overall_confidence >= 0.80


def test_unresolved_machine_never_auto_approves() -> None:
    """Perfect extraction is useless if nobody knows which machine it belongs to."""
    outcome = ResolutionOutcome(None, 0.4, ResolutionMethod.UNRESOLVED, [])
    decision = score_and_route(_good_fields(), outcome, threshold=0.80)

    assert not decision.auto_approve
    assert any(r.startswith("machine_unresolved") for r in decision.reasons)


def test_ambiguity_blocks_approval_despite_high_score() -> None:
    """Two confident candidates are individually certain and jointly useless."""
    decision = score_and_route(_good_fields(), _ambiguous(), threshold=0.50)
    assert decision.overall_confidence >= 0.50
    assert not decision.auto_approve
    assert any("machine_ambiguous" in r for r in decision.reasons)


def test_scoring_is_multiplicative_so_one_weak_signal_sinks_the_row() -> None:
    """An average would hide a near-zero factor; a product cannot."""
    strong = score_and_route(_good_fields(), _resolved(0.95), threshold=0.80)
    weak_resolution = score_and_route(_good_fields(), _resolved(0.62), threshold=0.80)
    assert weak_resolution.overall_confidence < strong.overall_confidence
    assert not weak_resolution.auto_approve


def test_absent_downtime_is_flagged_but_not_blocking() -> None:
    """Plenty of valid records state no duration; coverage must stay honest about it."""
    fields = _good_fields().model_copy(update={"downtime_hours": None})
    decision = score_and_route(fields, _resolved(), threshold=0.80)
    assert "downtime_absent" in decision.reasons
    assert decision.auto_approve


def test_low_field_confidence_is_named_specifically() -> None:
    """A reviewer needs to know WHICH field is uncertain, not just that the row is."""
    fields = _good_fields().model_copy(
        update={"field_confidence": {**_good_fields().field_confidence, "failure_mode": 0.4}}
    )
    decision = score_and_route(fields, _resolved(), threshold=0.80)
    assert any(r.startswith("low_confidence_failure_mode") for r in decision.reasons)
