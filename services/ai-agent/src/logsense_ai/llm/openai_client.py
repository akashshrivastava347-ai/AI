"""OpenAI adapter for the LLM port.

Uses JSON-object mode with the schema described in the prompt, rather than
provider-specific strict structured outputs. That choice is deliberate: it keeps
the adapter portable, so an Anthropic or self-hosted adapter is a near copy, and it
keeps validation-and-retry in one place (this module) for every provider.
"""

from __future__ import annotations

import json
import logging
import time

from pydantic import ValidationError

from logsense_ai.config import Settings
from logsense_ai.llm.base import LlmError, LlmResponse, LlmUsage, T

logger = logging.getLogger(__name__)

_RETRY_NOTE = (
    "Your previous reply was not valid against the schema: {error}\n"
    "Reply again with ONLY a JSON object matching the schema exactly. No prose, no "
    "code fences."
)


class OpenAiLlmClient:
    """Thin, typed wrapper over the OpenAI SDK."""

    def __init__(self, settings: Settings) -> None:
        if not settings.llm_api_key:
            raise LlmError(
                "No LLM API key configured. Export LOGSENSE_LLM_API_KEY, or run with "
                "--provider fake to use the deterministic offline adapter.",
                retryable=False,
            )
        # Imported lazily so the package still imports (and tests still run) in an
        # environment with no provider SDK configured.
        from openai import OpenAI

        self._client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            timeout=settings.llm_timeout_seconds,
            max_retries=0,  # retries are handled here so they are observable
        )
        self._settings = settings

    def _cost_inr(self, input_tokens: int, output_tokens: int) -> float:
        s = self._settings
        usd = (
            input_tokens / 1_000_000 * s.llm_cost_input_per_mtok_usd
            + output_tokens / 1_000_000 * s.llm_cost_output_per_mtok_usd
        )
        return round(usd * s.usd_to_inr, 6)

    def complete_json(
        self,
        *,
        system: str,
        user: str,
        schema: type[T],
        model: str | None = None,
        temperature: float = 0.0,
    ) -> LlmResponse[T]:
        model_name = model or self._settings.llm_model_extract
        messages: list[dict[str, str]] = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        total = LlmUsage(model=model_name, attempts=0)
        last_error: Exception | None = None

        # One attempt per allowed retry, plus the initial call. Schema failures get a
        # corrective turn; transport failures get a plain retry with backoff.
        for attempt in range(self._settings.llm_max_retries + 1):
            started = time.perf_counter()
            try:
                completion = self._client.chat.completions.create(
                    model=model_name,
                    messages=messages,  # type: ignore[arg-type]
                    temperature=temperature,
                    response_format={"type": "json_object"},
                )
            except Exception as exc:  # provider/transport failure
                last_error = exc
                total.attempts += 1
                logger.warning("LLM call failed (attempt %s): %s", attempt + 1, exc)
                if attempt < self._settings.llm_max_retries:
                    time.sleep(2**attempt)
                    continue
                raise LlmError(f"LLM provider unavailable: {exc}") from exc

            latency_ms = int((time.perf_counter() - started) * 1000)
            usage = completion.usage
            in_tok = usage.prompt_tokens if usage else 0
            out_tok = usage.completion_tokens if usage else 0
            total = total + LlmUsage(
                model=model_name,
                input_tokens=in_tok,
                output_tokens=out_tok,
                latency_ms=latency_ms,
                cost_inr=self._cost_inr(in_tok, out_tok),
                attempts=0,
            )
            total.attempts = attempt + 1

            content = (completion.choices[0].message.content or "").strip()
            try:
                parsed = schema.model_validate(json.loads(content))
            except (json.JSONDecodeError, ValidationError) as exc:
                last_error = exc
                logger.warning("LLM returned schema-invalid output (attempt %s)", attempt + 1)
                if attempt < self._settings.llm_max_retries:
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "user", "content": _RETRY_NOTE.format(error=exc)})
                    continue
                raise LlmError(
                    f"LLM output failed schema validation after "
                    f"{self._settings.llm_max_retries + 1} attempts: {exc}",
                    retryable=False,
                ) from exc

            return LlmResponse(parsed=parsed, usage=total, raw_text=content)

        raise LlmError(f"LLM call exhausted retries: {last_error}")
