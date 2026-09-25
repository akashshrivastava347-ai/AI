"""FastAPI application.

Story 1 exposes the minimum needed to review the pipeline: ingest a message, list
what was stored, and see what landed in the review queue. Auth, tenancy middleware
and the WhatsApp webhook arrive in their own stories.
"""

from __future__ import annotations

import logging

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from logsense_ai import __version__
from logsense_ai.api.schemas import (
    IngestMessageRequest,
    IngestMessageResponse,
    MachineOut,
    RecordOut,
    ReviewItemOut,
)
from logsense_ai.config import get_settings
from logsense_ai.db import get_session
from logsense_ai.domain.enums import StagedStatus
from logsense_ai.domain.models import Machine, MaintenanceRecord, RawRecord, StagedRecord
from logsense_ai.ingest.pipeline import IngestPipeline
from logsense_ai.llm import build_llm_client
from logsense_ai.llm.base import LlmError

logger = logging.getLogger(__name__)

app = FastAPI(
    title="LogSense AI Agent Service",
    version=__version__,
    description="Technician message in, structured maintenance record out.",
)


def get_pipeline(session: Session = Depends(get_session)) -> IngestPipeline:
    return IngestPipeline(session, build_llm_client())


@app.exception_handler(LlmError)
def handle_llm_error(_request: Request, exc: LlmError) -> JSONResponse:
    """Degrade honestly when the model provider is missing or down.

    An opaque 500 sends whoever is on call hunting through logs. A 503 that names
    the cause and the offline fallback is actionable in seconds.
    """
    logger.warning("LLM unavailable: %s", exc)
    return JSONResponse(
        status_code=503,
        content={
            "error": {
                "code": "LLM_UNAVAILABLE",
                "message": str(exc),
                "retryable": exc.retryable,
                "hint": (
                    "Set LOGSENSE_LLM_API_KEY, or set LOGSENSE_LLM_PROVIDER=fake to run "
                    "the deterministic offline adapter."
                ),
            }
        },
    )


@app.get("/health", tags=["ops"])
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "llm_provider": settings.llm_provider,
        "env": settings.app_env,
    }


@app.post("/api/v1/messages", response_model=IngestMessageResponse, tags=["ingest"])
def ingest_message(
    payload: IngestMessageRequest,
    pipeline: IngestPipeline = Depends(get_pipeline),
) -> IngestMessageResponse:
    """Ingest one technician message and route it."""
    try:
        result = pipeline.ingest_message(
            plant_id=payload.plant_id,
            raw_text=payload.text,
            source=payload.source,
            external_id=payload.external_id,
            reporter=payload.reporter,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return IngestMessageResponse(
        raw_record_id=result.raw_record_id,
        staged_record_id=result.staged_record_id,
        maintenance_record_id=result.maintenance_record_id,
        status=result.status,
        auto_approved=result.auto_approved,
        overall_confidence=result.overall_confidence,
        machine_id=result.machine_id,
        machine_name=result.machine_name,
        review_reasons=result.review_reasons,
        duplicate=result.duplicate,
        error=result.error,
    )


@app.get("/api/v1/plants/{plant_id}/machines", response_model=list[MachineOut], tags=["master"])
def list_machines(plant_id: str, session: Session = Depends(get_session)) -> list[Machine]:
    return list(
        session.scalars(select(Machine).where(Machine.plant_id == plant_id).order_by(Machine.name))
    )


@app.get("/api/v1/plants/{plant_id}/records", response_model=list[RecordOut], tags=["records"])
def list_records(
    plant_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    session: Session = Depends(get_session),
) -> list[MaintenanceRecord]:
    return list(
        session.scalars(
            select(MaintenanceRecord)
            .where(MaintenanceRecord.plant_id == plant_id)
            .order_by(MaintenanceRecord.created_at.desc())
            .limit(limit)
        )
    )


@app.get(
    "/api/v1/plants/{plant_id}/review-queue",
    response_model=list[ReviewItemOut],
    tags=["validation"],
)
def review_queue(
    plant_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    session: Session = Depends(get_session),
) -> list[StagedRecord]:
    """Extractions the system was not confident enough to accept on its own."""
    return list(
        session.scalars(
            select(StagedRecord)
            .where(
                StagedRecord.plant_id == plant_id,
                StagedRecord.status == StagedStatus.PENDING_REVIEW,
            )
            .order_by(StagedRecord.overall_confidence.asc())
            .limit(limit)
        )
    )


@app.get("/api/v1/raw-records/{raw_record_id}", tags=["records"])
def view_source(raw_record_id: str, session: Session = Depends(get_session)) -> dict:
    """View Source: the original message, exactly as it was received."""
    raw = session.get(RawRecord, raw_record_id)
    if raw is None:
        raise HTTPException(status_code=404, detail="raw record not found")
    return {
        "id": raw.id,
        "source": raw.source,
        "external_id": raw.external_id,
        "raw_text": raw.raw_text,
        "reporter": raw.reporter,
        "received_at": raw.received_at.isoformat(),
        "metadata": raw.source_metadata,
    }
