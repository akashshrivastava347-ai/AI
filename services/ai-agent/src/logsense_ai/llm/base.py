"""The provider port.

Everything downstream depends on this interface, never on a vendor SDK. Swapping
OpenAI for Anthropic, or for a self-hosted model, is a new adapter and a config
change — no call site moves.

The port deliberately exposes one operation: "given a system prompt, a user prompt
and a Pydantic schema, return a validated instance plus what it cost". Schema
validation and the single retry live here rather than in each adapter, so every
provider behaves identically under malformed output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LlmError(RuntimeError):
    """Provider failure that survived the adapter's retries.

    Callers treat this as a degradation signal, not a crash: ingestion pauses and
    stays resumable, and the assistant falls back to deterministic output.
    """

    def __init__(self, message: str, *, retryable: bool = True) -> None:
        super().__init__(message)
        self.retryable = retryable


@dataclass(slots=True)
class LlmUsage:
    """Cost and latency attribution for a single call.

    Recorded per operation so cost per plant per month is measured rather than
    estimated (docs/03-INDUSTRY-READINESS.md section 6).
    """

    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0
    cost_inr: float = 0.0
    attempts: int = 1

    def __add__(self, other: LlmUsage) -> LlmUsage:
        return LlmUsage(
            model=self.model or other.model,
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            latency_ms=self.latency_ms + other.latency_ms,
            cost_inr=self.cost_inr + other.cost_inr,
            attempts=self.attempts + other.attempts,
        )


@dataclass(slots=True)
class LlmResponse(Generic[T]):
    parsed: T
    usage: LlmUsage
    raw_text: str = field(default="", repr=False)


class LlmClient(Protocol):
    """Structured-output completion. The only capability the domain may assume."""

    def complete_json(
        self,
        *,
        system: str,
        user: str,
        schema: type[T],
        model: str | None = None,
        temperature: float = 0.0,
    ) -> LlmResponse[T]:
        """Return a schema-valid instance, or raise LlmError.

        Implementations must retry at least once on schema-validation failure before
        giving up — malformed JSON is the single most common provider failure mode.
        """
        ...
