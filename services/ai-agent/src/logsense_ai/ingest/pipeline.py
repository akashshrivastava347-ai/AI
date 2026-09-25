"""The ingestion pipeline.

One message in, one routed outcome out:

    persist raw (immutable)  ->  extract  ->  resolve  ->  score  ->  route

Ordering is deliberate. The raw record is committed *before* the LLM is called, so a
provider outage can never lose a technician's message — the worst case is a FAILED
staged row that is retried later against text we still hold.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from logsense_ai.config import Settings, get_settings
from logsense_ai.domain.enums import RecordSource, RecordStatus, StagedStatus
from logsense_ai.domain.models import (
    Machine,
    MaintenanceRecord,
    Plant,
    RawRecord,
    StagedRecord,
)
from logsense_ai.extraction.service import ExtractionService
from logsense_ai.ingest.scoring import score_and_route
from logsense_ai.llm.base import LlmClient, LlmError
from logsense_ai.resolution.resolver import MachineResolver

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class IngestResult:
    raw_record_id: str
    staged_record_id: str | None
    maintenance_record_id: str | None
    status: StagedStatus
    overall_confidence: float
    machine_id: str | None
    machine_name: str | None
    review_reasons: list[str]
    duplicate: bool = False
    error: str | None = None

    @property
    def auto_approved(self) -> bool:
        return self.status is StagedStatus.AUTO_APPROVED


class IngestPipeline:
    def __init__(
        self,
        session: Session,
        llm: LlmClient,
        *,
        settings: Settings | None = None,
    ) -> None:
        self._session = session
        self._settings = settings or get_settings()
        self._extraction = ExtractionService(llm, model=self._settings.llm_model_extract)
        self._resolver = MachineResolver(session, fuzzy_floor=self._settings.fuzzy_match_floor)

    def ingest_message(
        self,
        *,
        plant_id: str,
        raw_text: str,
        source: RecordSource = RecordSource.WHATSAPP,
        external_id: str | None = None,
        reporter: str | None = None,
        source_metadata: dict | None = None,
    ) -> IngestResult:
        plant = self._session.get(Plant, plant_id)
        if plant is None:
            raise ValueError(f"Unknown plant {plant_id!r}")

        # --- idempotency ------------------------------------------------------------
        # A WhatsApp provider retries deliveries. Without this, one technician message
        # becomes two breakdown records and the plant's downtime total is wrong.
        if external_id:
            existing = self._session.scalars(
                select(RawRecord).where(
                    RawRecord.source == source, RawRecord.external_id == external_id
                )
            ).first()
            if existing is not None:
                logger.info("duplicate delivery ignored: %s/%s", source, external_id)
                return self._result_for_existing(existing)

        # --- 1. persist raw, immutably, before anything can fail ---------------------
        raw = RawRecord(
            tenant_id=plant.tenant_id,
            plant_id=plant.id,
            source=source,
            external_id=external_id,
            raw_text=raw_text,
            reporter=reporter,
            source_metadata=source_metadata or {},
        )
        self._session.add(raw)
        self._session.flush()

        staged = StagedRecord(
            tenant_id=plant.tenant_id,
            plant_id=plant.id,
            raw_record_id=raw.id,
            status=StagedStatus.EXTRACTED,
        )
        self._session.add(staged)

        # --- 2. extract -------------------------------------------------------------
        known = [
            m.name
            for m in self._session.scalars(
                select(Machine).where(Machine.plant_id == plant.id, Machine.is_active.is_(True))
            )
        ]
        try:
            outcome = self._extraction.extract(raw_text, known_machines=known)
        except LlmError as exc:
            # The message is safe on disk; this row is retryable once the provider
            # recovers. Nothing is lost and nothing is guessed.
            staged.status = StagedStatus.FAILED
            staged.error = str(exc)
            self._session.flush()
            logger.warning("extraction failed for raw %s: %s", raw.id, exc)
            return IngestResult(
                raw_record_id=raw.id,
                staged_record_id=staged.id,
                maintenance_record_id=None,
                status=StagedStatus.FAILED,
                overall_confidence=0.0,
                machine_id=None,
                machine_name=None,
                review_reasons=["extraction_failed"],
                error=str(exc),
            )

        fields = outcome.fields
        usage = outcome.usage

        # --- 3. resolve -------------------------------------------------------------
        resolution = self._resolver.resolve(fields.machine_text, plant_id=plant.id)

        # --- 4. score and route -----------------------------------------------------
        decision = score_and_route(fields, resolution, threshold=plant.auto_approve_threshold)

        staged.occurred_on = fields.occurred_on
        staged.machine_text = fields.machine_text
        staged.machine_id = resolution.machine_id
        staged.failure_mode = fields.failure_mode
        staged.action = fields.action
        staged.parts = fields.parts
        staged.downtime_hours = fields.downtime_hours
        staged.technician = fields.technician or reporter
        staged.kind = fields.kind
        staged.field_confidence = fields.field_confidence
        staged.resolution_confidence = resolution.confidence
        staged.resolution_method = resolution.method
        staged.overall_confidence = decision.overall_confidence
        staged.review_reasons = decision.reasons
        staged.llm_model = usage.model
        staged.llm_input_tokens = usage.input_tokens
        staged.llm_output_tokens = usage.output_tokens
        staged.llm_latency_ms = usage.latency_ms
        staged.llm_cost_inr = usage.cost_inr

        machine = (
            self._session.get(Machine, resolution.machine_id) if resolution.machine_id else None
        )

        if not decision.auto_approve:
            staged.status = StagedStatus.PENDING_REVIEW
            self._session.flush()
            logger.info(
                "raw %s queued for review (confidence %.2f): %s",
                raw.id,
                decision.overall_confidence,
                ", ".join(decision.reasons[:3]),
            )
            return IngestResult(
                raw_record_id=raw.id,
                staged_record_id=staged.id,
                maintenance_record_id=None,
                status=StagedStatus.PENDING_REVIEW,
                overall_confidence=decision.overall_confidence,
                machine_id=resolution.machine_id,
                machine_name=machine.name if machine else None,
                review_reasons=decision.reasons,
            )

        # --- 5. auto-approve --------------------------------------------------------
        staged.status = StagedStatus.AUTO_APPROVED
        record = MaintenanceRecord(
            tenant_id=plant.tenant_id,
            plant_id=plant.id,
            raw_record_id=raw.id,  # the provenance chain, never null
            staged_record_id=staged.id,
            machine_id=resolution.machine_id,
            occurred_on=fields.occurred_on,
            machine_text=fields.machine_text,
            failure_mode=fields.failure_mode,
            action=fields.action,
            parts=fields.parts,
            downtime_hours=fields.downtime_hours,
            technician=fields.technician or reporter,
            kind=fields.kind,
            status=RecordStatus.ACTIVE,
            confidence=decision.overall_confidence,
        )
        self._session.add(record)
        self._session.flush()

        logger.info(
            "raw %s auto-approved as record %s (confidence %.2f)",
            raw.id,
            record.id,
            decision.overall_confidence,
        )
        return IngestResult(
            raw_record_id=raw.id,
            staged_record_id=staged.id,
            maintenance_record_id=record.id,
            status=StagedStatus.AUTO_APPROVED,
            overall_confidence=decision.overall_confidence,
            machine_id=resolution.machine_id,
            machine_name=machine.name if machine else None,
            review_reasons=decision.reasons,
        )

    def _result_for_existing(self, raw: RawRecord) -> IngestResult:
        staged = self._session.scalars(
            select(StagedRecord).where(StagedRecord.raw_record_id == raw.id)
        ).first()
        record = self._session.scalars(
            select(MaintenanceRecord).where(MaintenanceRecord.raw_record_id == raw.id)
        ).first()
        machine = (
            self._session.get(Machine, staged.machine_id) if staged and staged.machine_id else None
        )
        return IngestResult(
            raw_record_id=raw.id,
            staged_record_id=staged.id if staged else None,
            maintenance_record_id=record.id if record else None,
            status=staged.status if staged else StagedStatus.EXTRACTED,
            overall_confidence=staged.overall_confidence if staged else 0.0,
            machine_id=staged.machine_id if staged else None,
            machine_name=machine.name if machine else None,
            review_reasons=list(staged.review_reasons) if staged else [],
            duplicate=True,
        )
