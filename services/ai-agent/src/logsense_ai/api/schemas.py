"""Request and response models for the HTTP API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from logsense_ai.domain.enums import RecordSource, StagedStatus


class IngestMessageRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    plant_id: str
    text: str = Field(min_length=1, max_length=8000)
    source: RecordSource = RecordSource.WHATSAPP
    external_id: str | None = Field(
        default=None,
        max_length=200,
        description="Provider message id. Supplying it makes ingestion idempotent.",
    )
    reporter: str | None = Field(default=None, max_length=200)


class IngestMessageResponse(BaseModel):
    raw_record_id: str
    staged_record_id: str | None
    maintenance_record_id: str | None
    status: StagedStatus
    auto_approved: bool
    overall_confidence: float
    machine_id: str | None
    machine_name: str | None
    review_reasons: list[str]
    duplicate: bool
    error: str | None = None


class MachineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    asset_code: str
    line: str | None
    machine_type: str | None


class RecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    machine_id: str | None
    machine_text: str | None
    failure_mode: str | None
    action: str | None
    parts: list[str]
    downtime_hours: float | None
    technician: str | None
    confidence: float
    raw_record_id: str


class ReviewItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    raw_record_id: str
    machine_text: str | None
    machine_id: str | None
    failure_mode: str | None
    action: str | None
    downtime_hours: float | None
    overall_confidence: float
    review_reasons: list[str]
