"""Extraction service: raw text in, validated structured fields out."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from logsense_ai.extraction.dictionary import parse_downtime_hours
from logsense_ai.extraction.prompts import SYSTEM_PROMPT, build_user_prompt
from logsense_ai.extraction.schema import ExtractedFields
from logsense_ai.llm.base import LlmClient, LlmUsage

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ExtractionOutcome:
    fields: ExtractedFields
    usage: LlmUsage
    raw_response: str


class ExtractionService:
    """Turns one technician message into validated fields with per-field confidence."""

    def __init__(self, llm: LlmClient, *, model: str | None = None) -> None:
        self._llm = llm
        self._model = model

    def extract(
        self, raw_text: str, *, known_machines: list[str] | None = None
    ) -> ExtractionOutcome:
        """Extract from one message.

        Raises ``LlmError`` when the provider is unavailable or output stays invalid
        after retries. Callers translate that into a retryable FAILED row rather than
        losing the message — the raw record is already durably stored by then.
        """
        user_prompt = build_user_prompt(raw_text, known_machines=known_machines)
        response = self._llm.complete_json(
            system=SYSTEM_PROMPT,
            user=user_prompt,
            schema=ExtractedFields,
            model=self._model,
        )

        fields = self._apply_deterministic_fallbacks(response.parsed, raw_text)
        return ExtractionOutcome(
            fields=fields, usage=response.usage, raw_response=response.raw_text
        )

    @staticmethod
    def _apply_deterministic_fallbacks(fields: ExtractedFields, raw_text: str) -> ExtractedFields:
        """Recover values the model missed, using deterministic rules only.

        Downtime is the one field worth a second pass: it drives every cost figure in
        the product, and a phrase like "2 ghante" is far more reliably parsed by the
        dictionary than by a model on a bad day. The fallback only ever *fills a
        null* — it never overrides something the model actually extracted.
        """
        if fields.downtime_hours is None:
            recovered = parse_downtime_hours(raw_text)
            if recovered is not None:
                fields = fields.model_copy(
                    update={
                        "downtime_hours": recovered,
                        # Deterministic, but from a fallback rather than the model's
                        # own reading, so it is scored slightly below a direct hit.
                        "field_confidence": {
                            **fields.field_confidence,
                            "downtime_hours": 0.85,
                        },
                    }
                )
                logger.debug("recovered downtime %.2fh via dictionary fallback", recovered)
        return fields
