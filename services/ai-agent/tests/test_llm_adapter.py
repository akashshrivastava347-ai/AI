"""The OpenAI adapter's retry, validation and cost behaviour.

Exercised against a stub that mimics the SDK's response shape. The adapter is the
one module that would otherwise only be covered by calling a paid live service.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from pydantic import BaseModel

from logsense_ai.config import Settings
from logsense_ai.llm.base import LlmError
from logsense_ai.llm.factory import build_llm_client
from logsense_ai.llm.fake import FakeLlmClient
from logsense_ai.llm.openai_client import OpenAiLlmClient


class Answer(BaseModel):
    value: int


def _completion(content: str, *, prompt_tokens: int = 100, completion_tokens: int = 20):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage=SimpleNamespace(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens),
    )


class StubSdk:
    """Mimics ``openai.OpenAI`` closely enough for the adapter under test."""

    def __init__(self, responses: list, **_: object) -> None:
        self._responses = list(responses)
        self.call_count = 0
        self.last_messages: list[dict] = []
        outer = self

        class _Completions:
            def create(self, *, model, messages, temperature, response_format):
                outer.call_count += 1
                outer.last_messages = list(messages)
                item = outer._responses.pop(0)
                if isinstance(item, Exception):
                    raise item
                return item

        self.chat = SimpleNamespace(completions=_Completions())


@pytest.fixture
def settings() -> Settings:
    return Settings(llm_provider="openai", llm_api_key="test-key", llm_max_retries=2)


def _client(monkeypatch, settings: Settings, responses: list) -> OpenAiLlmClient:
    stub_holder = {}

    def _factory(**kwargs):
        stub = StubSdk(responses, **kwargs)
        stub_holder["stub"] = stub
        return stub

    monkeypatch.setattr("openai.OpenAI", _factory)
    client = OpenAiLlmClient(settings)
    client.stub = stub_holder["stub"]  # type: ignore[attr-defined]
    return client


def test_valid_response_is_parsed_with_usage(monkeypatch, settings: Settings) -> None:
    client = _client(monkeypatch, settings, [_completion(json.dumps({"value": 7}))])

    result = client.complete_json(system="s", user="u", schema=Answer)

    assert result.parsed.value == 7
    assert result.usage.input_tokens == 100
    assert result.usage.output_tokens == 20
    assert result.usage.cost_inr > 0  # cost is attributed, not estimated later


def test_schema_invalid_output_triggers_a_corrective_retry(monkeypatch, settings: Settings) -> None:
    """Malformed JSON is the most common provider failure; one corrective turn fixes it."""
    client = _client(
        monkeypatch,
        settings,
        [_completion("not json at all"), _completion(json.dumps({"value": 3}))],
    )

    result = client.complete_json(system="s", user="u", schema=Answer)

    assert result.parsed.value == 3
    assert client.stub.call_count == 2
    # The retry must tell the model what was wrong, not silently repeat the request.
    assert any("not valid against the schema" in m["content"] for m in client.stub.last_messages)


def test_persistently_invalid_output_raises(monkeypatch, settings: Settings) -> None:
    client = _client(monkeypatch, settings, [_completion("garbage")] * 3)

    with pytest.raises(LlmError, match="schema validation"):
        client.complete_json(system="s", user="u", schema=Answer)


def test_transport_failure_is_retried_then_raises(monkeypatch, settings: Settings) -> None:
    monkeypatch.setattr("time.sleep", lambda _: None)  # no real backoff in tests
    client = _client(monkeypatch, settings, [RuntimeError("connection reset")] * 3)

    with pytest.raises(LlmError, match="provider unavailable"):
        client.complete_json(system="s", user="u", schema=Answer)
    assert client.stub.call_count == 3


def test_transport_failure_then_success(monkeypatch, settings: Settings) -> None:
    monkeypatch.setattr("time.sleep", lambda _: None)
    client = _client(
        monkeypatch,
        settings,
        [RuntimeError("timeout"), _completion(json.dumps({"value": 11}))],
    )

    assert client.complete_json(system="s", user="u", schema=Answer).parsed.value == 11


def test_missing_api_key_fails_fast_with_guidance(monkeypatch) -> None:
    """The message must point at the offline adapter, not just complain."""
    with pytest.raises(LlmError, match="fake"):
        OpenAiLlmClient(Settings(llm_provider="openai", llm_api_key=None))


# --- factory ------------------------------------------------------------------------


def test_factory_returns_fake_adapter() -> None:
    assert isinstance(build_llm_client(Settings(llm_provider="fake")), FakeLlmClient)


def test_factory_rejects_unknown_provider() -> None:
    with pytest.raises(LlmError, match="Unknown LLM provider"):
        build_llm_client(Settings(llm_provider="bogus"))


def test_fake_adapter_is_deterministic() -> None:
    """Same input, same extraction — otherwise routing assertions mean nothing."""
    from logsense_ai.extraction.schema import ExtractedFields

    client = FakeLlmClient()
    text = "<<<MESSAGE\nLine 3 conveyor motor bearing replaced, 2 ghante\n>>>"
    first = client.complete_json(system="s", user=text, schema=ExtractedFields)
    second = client.complete_json(system="s", user=text, schema=ExtractedFields)
    assert first.parsed.model_dump() == second.parsed.model_dump()
