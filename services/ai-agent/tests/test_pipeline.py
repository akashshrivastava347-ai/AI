"""End-to-end ingestion: extraction, routing, provenance and failure handling."""

from __future__ import annotations

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from logsense_ai.config import Settings
from logsense_ai.domain.enums import RecordSource, StagedStatus
from logsense_ai.domain.models import MaintenanceRecord, Plant, RawRecord, StagedRecord
from logsense_ai.ingest.pipeline import IngestPipeline
from logsense_ai.llm.fake import FakeLlmClient

CLEAR_MESSAGE = "Line 3 ka conveyor motor band tha, bearing change kiya, 2 ghante"
VAGUE_MESSAGE = "machine kharab hai"


def test_clear_message_is_auto_approved(
    pipeline: IngestPipeline, plant: Plant, session: Session
) -> None:
    result = pipeline.ingest_message(plant_id=plant.id, raw_text=CLEAR_MESSAGE)

    assert result.auto_approved
    assert result.status is StagedStatus.AUTO_APPROVED
    assert result.maintenance_record_id is not None
    assert result.machine_name == "Line 3 Conveyor Motor"

    record = session.get(MaintenanceRecord, result.maintenance_record_id)
    assert record is not None
    assert record.failure_mode == "Bearing Failure"
    assert record.downtime_hours == pytest.approx(2.0)


def test_vague_message_goes_to_review_not_to_records(
    pipeline: IngestPipeline, plant: Plant, session: Session
) -> None:
    """A message that says nothing must never become a maintenance record."""
    result = pipeline.ingest_message(plant_id=plant.id, raw_text=VAGUE_MESSAGE)

    assert not result.auto_approved
    assert result.status is StagedStatus.PENDING_REVIEW
    assert result.maintenance_record_id is None
    assert any(r.startswith("missing_machine_text") for r in result.review_reasons)
    assert session.scalar(select(func.count()).select_from(MaintenanceRecord)) == 0


def test_ambiguous_machine_blocks_auto_approval(pipeline: IngestPipeline, plant: Plant) -> None:
    """Two equally plausible machines is exactly the case a human should decide."""
    result = pipeline.ingest_message(
        plant_id=plant.id, raw_text="MTR brng noise L3 conv, replcd 6205ZZ"
    )
    assert not result.auto_approved
    assert any("machine_ambiguous" in r for r in result.review_reasons)


def test_every_record_keeps_its_raw_provenance(
    pipeline: IngestPipeline, plant: Plant, session: Session
) -> None:
    result = pipeline.ingest_message(plant_id=plant.id, raw_text=CLEAR_MESSAGE)
    record = session.get(MaintenanceRecord, result.maintenance_record_id)

    raw = session.get(RawRecord, record.raw_record_id)
    assert raw is not None
    # Raw text is preserved verbatim — normalisation never overwrites the evidence.
    assert raw.raw_text == CLEAR_MESSAGE


def test_raw_record_cannot_be_deleted_while_referenced(
    pipeline: IngestPipeline, plant: Plant, session: Session
) -> None:
    """The provenance chain is enforced by the schema, not by convention."""
    result = pipeline.ingest_message(plant_id=plant.id, raw_text=CLEAR_MESSAGE)
    session.commit()

    raw = session.get(RawRecord, result.raw_record_id)
    session.delete(raw)
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_duplicate_delivery_is_idempotent(
    pipeline: IngestPipeline, plant: Plant, session: Session
) -> None:
    """A WhatsApp provider retry must not double a plant's downtime total."""
    first = pipeline.ingest_message(
        plant_id=plant.id, raw_text=CLEAR_MESSAGE, external_id="wamid.ABC123"
    )
    second = pipeline.ingest_message(
        plant_id=plant.id, raw_text=CLEAR_MESSAGE, external_id="wamid.ABC123"
    )

    assert second.duplicate
    assert second.raw_record_id == first.raw_record_id
    assert session.scalar(select(func.count()).select_from(MaintenanceRecord)) == 1
    assert session.scalar(select(func.count()).select_from(RawRecord)) == 1


def test_provider_outage_preserves_the_message(
    session: Session, plant: Plant, settings: Settings
) -> None:
    """The raw record is committed before the LLM is called, so nothing is lost."""
    failing = FakeLlmClient(fail_times=99)
    pipeline = IngestPipeline(session, failing, settings=settings)

    result = pipeline.ingest_message(plant_id=plant.id, raw_text=CLEAR_MESSAGE)

    assert result.status is StagedStatus.FAILED
    assert result.error is not None
    raw = session.get(RawRecord, result.raw_record_id)
    assert raw.raw_text == CLEAR_MESSAGE  # recoverable: retry needs no re-delivery
    assert session.scalar(select(func.count()).select_from(MaintenanceRecord)) == 0


def test_unknown_plant_is_rejected(pipeline: IngestPipeline) -> None:
    with pytest.raises(ValueError, match="Unknown plant"):
        pipeline.ingest_message(plant_id="does-not-exist", raw_text=CLEAR_MESSAGE)


def test_cost_and_latency_are_recorded(
    pipeline: IngestPipeline, plant: Plant, session: Session
) -> None:
    """Cost per plant per month is measured, not estimated."""
    result = pipeline.ingest_message(plant_id=plant.id, raw_text=CLEAR_MESSAGE)
    staged = session.get(StagedRecord, result.staged_record_id)

    assert staged.llm_model
    assert staged.llm_input_tokens > 0
    assert staged.llm_cost_inr >= 0.0


def test_devanagari_message_is_understood(pipeline: IngestPipeline, plant: Plant) -> None:
    result = pipeline.ingest_message(
        plant_id=plant.id,
        raw_text="लाइन 2 कैपिंग मोटर गरम हो रहा था, बेयरिंग बदला, डेढ़ घंटा बंद",
    )
    assert result.machine_name == "Line 2 Capping Motor"
    assert result.auto_approved


def test_reporter_is_used_when_technician_absent(
    pipeline: IngestPipeline, plant: Plant, session: Session
) -> None:
    result = pipeline.ingest_message(
        plant_id=plant.id,
        raw_text=CLEAR_MESSAGE,
        source=RecordSource.WHATSAPP,
        reporter="Ramesh",
    )
    record = session.get(MaintenanceRecord, result.maintenance_record_id)
    assert record.technician == "Ramesh"
