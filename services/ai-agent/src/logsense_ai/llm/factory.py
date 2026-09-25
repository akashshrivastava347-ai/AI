"""Build the configured LLM adapter."""

from __future__ import annotations

from logsense_ai.config import Settings, get_settings
from logsense_ai.llm.base import LlmClient, LlmError


def build_llm_client(settings: Settings | None = None) -> LlmClient:
    settings = settings or get_settings()
    provider = settings.llm_provider.lower()

    if provider == "fake":
        from logsense_ai.llm.fake import FakeLlmClient

        return FakeLlmClient()

    if provider == "openai":
        from logsense_ai.llm.openai_client import OpenAiLlmClient

        return OpenAiLlmClient(settings)

    raise LlmError(f"Unknown LLM provider {provider!r}. Supported: openai, fake.", retryable=False)
