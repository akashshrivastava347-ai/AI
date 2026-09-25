"""The extraction contract.

This schema is the boundary between generative output and the rest of the system.
Anything the model returns that does not validate here never reaches the database.

Note what is *not* here: no free-form fields the model can use to smuggle prose into
a numeric column, and no confidence the model can omit. Missing values are explicit
nulls, because a guessed date is worse than a null one.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from logsense_ai.domain.enums import RecordKind

# Fields a reviewer actually cares about when judging whether an extraction is safe
# to auto-approve. Weighted in confidence scoring (see scoring.py).
CORE_FIELDS: tuple[str, ...] = ("machine_text", "failure_mode", "action")


class ExtractedFields(BaseModel):
    """Structured fields pulled from one raw message or row."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    occurred_on: date | None = Field(
        default=None, description="Event date if stated. Null if absent — never inferred."
    )
    machine_text: str | None = Field(
        default=None, max_length=300, description="Machine as written, verbatim."
    )
    failure_mode: str | None = Field(default=None, max_length=200)
    action: str | None = Field(default=None, max_length=2000)
    parts: list[str] = Field(default_factory=list)
    downtime_hours: float | None = Field(default=None, ge=0, le=720)
    technician: str | None = Field(default=None, max_length=200)
    kind: RecordKind = RecordKind.BREAKDOWN

    field_confidence: dict[str, float] = Field(
        default_factory=dict,
        description="Per-field self-assessed confidence in [0,1]. A field the model "
        "could not find scores 0.",
    )

    @field_validator("parts", mode="before")
    @classmethod
    def _clean_parts(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            return []
        seen: list[str] = []
        for item in value:
            code = str(item).strip().upper().replace(" ", "")
            if code and code not in seen:
                seen.append(code)
        return seen[:20]

    @field_validator("field_confidence", mode="before")
    @classmethod
    def _clamp_confidence(cls, value: object) -> dict[str, float]:
        if not isinstance(value, dict):
            return {}
        cleaned: dict[str, float] = {}
        for key, raw in value.items():
            try:
                score = float(raw)
            except (TypeError, ValueError):
                continue
            # A model that reports 1.4 confidence is not more certain, it is wrong.
            cleaned[str(key)] = min(max(score, 0.0), 1.0)
        return cleaned

    @field_validator("downtime_hours", mode="before")
    @classmethod
    def _coerce_downtime(cls, value: object) -> float | None:
        """Accept a number, or a phrase the model failed to convert.

        Models occasionally return "2 hours" where a float was asked for. Parsing it
        deterministically is better than discarding a real datum — but a phrase we
        cannot parse becomes null, never a guess.
        """
        if value is None or isinstance(value, int | float):
            return value
        if isinstance(value, str):
            from logsense_ai.extraction.dictionary import parse_downtime_hours

            return parse_downtime_hours(value)
        return None

    def confidence_for(self, field: str) -> float:
        return self.field_confidence.get(field, 0.0)

    def missing_core_fields(self) -> list[str]:
        return [f for f in CORE_FIELDS if not getattr(self, f, None)]
