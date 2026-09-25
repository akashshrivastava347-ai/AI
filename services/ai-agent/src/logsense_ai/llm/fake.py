"""Deterministic in-memory adapter.

Used by the entire test suite and by ``--provider fake`` so the pipeline is
reviewable without an API key, without network, and without cost. CI never calls a
live provider: tests that do are slow, flaky, and fail during someone else's incident.

The fake is rule-based, not random. Same input always yields the same extraction,
which is what makes assertions about routing and confidence meaningful.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable

from pydantic import ValidationError

from logsense_ai.llm.base import LlmError, LlmResponse, LlmUsage, T

# Minimal knowledge the fake needs to imitate a competent extractor on the kinds of
# messages this product actually receives.
_FAILURE_PATTERNS: list[tuple[str, str]] = [
    (r"\b(brng|bearing|beyring|बेयरिंग|बेअरिंग)\b", "Bearing Failure"),
    (r"\b(belt|बेल्ट)\b", "Belt Failure"),
    (r"\b(vfd|drive|ड्राइव)\b", "VFD Trip"),
    (r"\b(motor|mtr|मोटर)\s*(burn|jam|hot|fail)", "Motor Failure"),
    (r"\b(seal|leak|leakage|रिसाव)\b", "Seal Leak"),
    (r"\b(sensor|प्रॉक्सी|proximity|prox)\b", "Sensor Fault"),
    (r"\b(overheat|heating|garam|गरम)\b", "Overheating"),
    (r"\b(oil|lubric|grease)\b", "Lubrication Issue"),
]

_ACTION_PATTERNS: list[tuple[str, str]] = [
    (r"\b(replac|change|badl|बदल|चेंज)\w*", "Component replaced"),
    (r"\b(clean|saaf|साफ)\w*", "Cleaned"),
    (r"\b(tight|kas|कस)\w*", "Tightened"),
    (r"\b(align|algn|अलाइन)\w*", "Alignment checked"),
    (r"\b(reset|restart)\w*", "Reset"),
    (r"\b(repair|marammat|मरम्मत)\w*", "Repaired"),
    (r"\b(lagaya|lagayi|laga|install|fit)\w*", "Component installed"),
    (r"\b(nikala|remov)\w*", "Component removed"),
]

# Part codes as technicians actually write them: 6205ZZ, 6205 ZZ, SKF-6205.
_PART_RE = re.compile(r"\b([A-Z]{0,3}-?\d{4,5}\s?[A-Z]{0,3})\b", re.IGNORECASE)

# A bare "l" only qualifies as a line marker when a digit follows, so the "l" in
# "seal leakage" is not mistaken for "Line".
_LINE_QUAL = r"(?:lines?|l(?=\s*-?\s*\d)|लाइन|utilities|utility|util)\s*-?\s*\d*"
_MACHINE_NOUN = (
    r"(?:motor|mtr|conveyor|conv|pump|compressor|fan|blower|gearbox|gbx|vfd"
    r"|capping|filling|packing|labeller"
    r"|मोटर|पंप|कन्वेयर|कैपिंग|फिलिंग|पैकिंग|कंप्रेसर)"
)
# The trailing-noun group lets "line 2 capping motor" capture in full rather than
# stopping at the first noun. The reverse form's gap is kept tight so a phrase like
# "MTR brng noise L3" cannot be swallowed whole as one machine name.
_MACHINE_RE = re.compile(
    rf"({_LINE_QUAL}[^,.;]{{0,20}}?{_MACHINE_NOUN}(?:\s+{_MACHINE_NOUN})?"
    rf"|{_MACHINE_NOUN}(?:\s+{_MACHINE_NOUN})?[^,.;]{{0,8}}?{_LINE_QUAL})",
    re.IGNORECASE,
)


def _first_match(text: str, patterns: list[tuple[str, str]]) -> str | None:
    for pattern, value in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return value
    return None


def default_extractor(user_prompt: str) -> dict:
    """Imitate an extraction good enough to exercise every downstream branch."""
    from logsense_ai.extraction.dictionary import expand_shorthand, parse_downtime_hours

    # The prompt carries the raw message inside a fenced block; pull it back out.
    fenced = re.search(r"<<<MESSAGE\n(.*?)\n>>>", user_prompt, re.DOTALL)
    text = fenced.group(1) if fenced else user_prompt
    expanded = expand_shorthand(text)

    machine_match = _MACHINE_RE.search(text)
    machine_text = machine_match.group(1).strip() if machine_match else None

    failure_mode = _first_match(expanded, _FAILURE_PATTERNS)
    action = _first_match(expanded, _ACTION_PATTERNS)
    downtime = parse_downtime_hours(text)
    parts = [p.strip().upper().replace(" ", "") for p in _PART_RE.findall(text)]

    confidence = {
        "machine_text": 0.94 if machine_text else 0.0,
        "failure_mode": 0.93 if failure_mode else 0.0,
        "action": 0.88 if action else 0.0,
        "parts": 0.91 if parts else 0.0,
        "downtime_hours": 0.90 if downtime is not None else 0.0,
        "occurred_on": 0.0,
    }

    return {
        "occurred_on": None,
        "machine_text": machine_text,
        "failure_mode": failure_mode,
        "action": action,
        "parts": parts,
        "downtime_hours": downtime,
        "technician": None,
        "kind": "BREAKDOWN",
        "field_confidence": confidence,
    }


class FakeLlmClient:
    """Rule-based stand-in for a real provider."""

    def __init__(
        self,
        extractor: Callable[[str], dict] | None = None,
        *,
        model: str = "fake-extract-v1",
        fail_times: int = 0,
    ) -> None:
        self._extractor = extractor or default_extractor
        self._model = model
        # Lets tests exercise the retry and degradation paths deterministically.
        self._fail_times = fail_times
        self.calls: list[tuple[str, str]] = []

    def complete_json(
        self,
        *,
        system: str,
        user: str,
        schema: type[T],
        model: str | None = None,
        temperature: float = 0.0,
    ) -> LlmResponse[T]:
        self.calls.append((system, user))

        if self._fail_times > 0:
            self._fail_times -= 1
            raise LlmError("fake provider outage", retryable=True)

        payload = self._extractor(user)
        raw_text = json.dumps(payload, default=str)
        try:
            parsed = schema.model_validate(payload)
        except ValidationError as exc:  # pragma: no cover - guards fake misconfiguration
            raise LlmError(f"fake produced schema-invalid output: {exc}", retryable=False) from exc

        return LlmResponse(
            parsed=parsed,
            usage=LlmUsage(
                model=model or self._model,
                input_tokens=len(user) // 4,
                output_tokens=len(raw_text) // 4,
                latency_ms=1,
                cost_inr=0.0,
            ),
            raw_text=raw_text,
        )
