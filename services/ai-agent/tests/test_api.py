"""HTTP surface."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from logsense_ai.api.main import app, get_pipeline
from logsense_ai.config import Settings
from logsense_ai.db import get_session
from logsense_ai.domain.models import Plant
from logsense_ai.ingest.pipeline import IngestPipeline
from logsense_ai.llm.fake import FakeLlmClient


@pytest.fixture
def client(session: Session, plant: Plant, settings: Settings) -> Iterator[TestClient]:
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_pipeline] = lambda: IngestPipeline(
        session, FakeLlmClient(), settings=settings
    )
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_health(client: TestClient) -> None:
    body = client.get("/health").json()
    assert body["status"] == "ok"


def test_ingest_returns_the_routing_decision(client: TestClient, plant: Plant) -> None:
    response = client.post(
        "/api/v1/messages",
        json={
            "plant_id": plant.id,
            "text": "Line 3 ka conveyor motor band tha, bearing change kiya, 2 ghante",
            "reporter": "Ramesh",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["auto_approved"] is True
    assert body["machine_name"] == "Line 3 Conveyor Motor"
    assert body["maintenance_record_id"]


def test_unknown_plant_returns_404(client: TestClient) -> None:
    response = client.post(
        "/api/v1/messages", json={"plant_id": "nope", "text": "bearing replaced"}
    )
    assert response.status_code == 404


def test_empty_text_is_rejected(client: TestClient, plant: Plant) -> None:
    response = client.post("/api/v1/messages", json={"plant_id": plant.id, "text": ""})
    assert response.status_code == 422


def test_review_queue_lists_only_uncertain_rows(client: TestClient, plant: Plant) -> None:
    client.post(
        "/api/v1/messages",
        json={
            "plant_id": plant.id,
            "text": "Line 3 ka conveyor motor band tha, bearing change kiya, 2 ghante",
        },
    )
    client.post("/api/v1/messages", json={"plant_id": plant.id, "text": "machine kharab hai"})

    queue = client.get(f"/api/v1/plants/{plant.id}/review-queue").json()
    records = client.get(f"/api/v1/plants/{plant.id}/records").json()

    assert len(queue) == 1
    assert len(records) == 1
    assert queue[0]["review_reasons"]


def test_view_source_returns_the_original_message(client: TestClient, plant: Plant) -> None:
    """Every record must be traceable to exactly what the technician wrote."""
    text = "L1 filling pump seal leakage, replaced seal, 45 min downtime"
    ingest = client.post("/api/v1/messages", json={"plant_id": plant.id, "text": text}).json()

    source = client.get(f"/api/v1/raw-records/{ingest['raw_record_id']}").json()
    assert source["raw_text"] == text


def test_view_source_404_for_unknown_id(client: TestClient) -> None:
    assert client.get("/api/v1/raw-records/nope").status_code == 404


def test_machines_endpoint_is_plant_scoped(client: TestClient, plant: Plant) -> None:
    machines = client.get(f"/api/v1/plants/{plant.id}/machines").json()
    assert len(machines) == 7
    assert all(m["asset_code"] for m in machines)


def test_llm_unavailable_returns_actionable_503(session: Session, plant: Plant) -> None:
    """A missing API key must not surface as an opaque 500."""
    from logsense_ai.llm.base import LlmError

    def _broken_pipeline() -> IngestPipeline:
        raise LlmError("No LLM API key configured.", retryable=False)

    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_pipeline] = _broken_pipeline
    try:
        client = TestClient(app, raise_server_exceptions=False)
        response = client.post(
            "/api/v1/messages", json={"plant_id": plant.id, "text": "bearing replaced"}
        )
        assert response.status_code == 503
        body = response.json()["error"]
        assert body["code"] == "LLM_UNAVAILABLE"
        assert "fake" in body["hint"]
    finally:
        app.dependency_overrides.clear()
