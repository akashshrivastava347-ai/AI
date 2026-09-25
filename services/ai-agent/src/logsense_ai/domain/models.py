"""ORM models.

Two invariants from docs/00-PRODUCT-VISION.md are enforced structurally here rather
than by convention:

1. **Raw data is immutable.** ``RawRecord.raw_text`` is written once and never
   updated by normalisation. Deleting one is blocked by a RESTRICT foreign key.
2. **Every maintenance record has a raw ancestor.** ``raw_record_id`` is NOT NULL,
   so a record with no provenance cannot be represented, let alone persisted.

``tenant_id`` is present from the first migration. Retrofitting tenancy later is
the documented mistake (docs/03-INDUSTRY-READINESS.md section 1).
"""

from __future__ import annotations

import uuid
from datetime import UTC, date, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from logsense_ai.db import Base
from logsense_ai.domain.enums import (
    AliasSource,
    RecordKind,
    RecordSource,
    RecordStatus,
    ResolutionMethod,
    StagedStatus,
)


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(UTC)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )


class Plant(Base, TimestampMixin):
    __tablename__ = "plants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    tenant_id: Mapped[str] = mapped_column(String(36), index=True)
    name: Mapped[str] = mapped_column(String(200))
    code: Mapped[str] = mapped_column(String(50))
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Kolkata")

    # Per-plant tuning. A plant with cleaner data earns a higher bar; a plant with
    # messy scanned registers gets a lower one until alias learning catches up.
    auto_approve_threshold: Mapped[float] = mapped_column(Float, default=0.80)
    downtime_cost_per_hour_inr: Mapped[float] = mapped_column(Float, default=125000.0)

    machines: Mapped[list[Machine]] = relationship(back_populates="plant")

    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_plant_tenant_code"),
        CheckConstraint(
            "auto_approve_threshold >= 0 AND auto_approve_threshold <= 1",
            name="ck_plant_threshold_range",
        ),
    )


class Machine(Base, TimestampMixin):
    __tablename__ = "machines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    tenant_id: Mapped[str] = mapped_column(String(36), index=True)
    plant_id: Mapped[str] = mapped_column(ForeignKey("plants.id"), index=True)

    name: Mapped[str] = mapped_column(String(200))
    asset_code: Mapped[str] = mapped_column(String(64))
    line: Mapped[str | None] = mapped_column(String(100), default=None)
    machine_type: Mapped[str | None] = mapped_column(String(100), default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    plant: Mapped[Plant] = relationship(back_populates="machines")
    aliases: Mapped[list[MachineAlias]] = relationship(back_populates="machine")

    __table_args__ = (
        UniqueConstraint("plant_id", "asset_code", name="uq_machine_plant_code"),
        Index("ix_machine_plant_active", "plant_id", "is_active"),
    )


class MachineAlias(Base, TimestampMixin):
    """A learned mapping from messy text to a real asset.

    This table is the product's compounding asset: every correction a plant makes
    deepens their own switching cost, and none of it requires model training.
    """

    __tablename__ = "machine_aliases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    tenant_id: Mapped[str] = mapped_column(String(36), index=True)
    plant_id: Mapped[str] = mapped_column(ForeignKey("plants.id"), index=True)
    machine_id: Mapped[str] = mapped_column(ForeignKey("machines.id"), index=True)

    # Lower-cased, whitespace-collapsed form used for lookup.
    alias_text: Mapped[str] = mapped_column(String(300))
    normalized_text: Mapped[str] = mapped_column(String(300), index=True)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    source: Mapped[AliasSource] = mapped_column(String(20), default=AliasSource.VALIDATION)
    created_by: Mapped[str | None] = mapped_column(String(200), default=None)

    machine: Mapped[Machine] = relationship(back_populates="aliases")

    __table_args__ = (UniqueConstraint("plant_id", "normalized_text", name="uq_alias_plant_text"),)


class RawRecord(Base):
    """Immutable source of truth for one inbound message, row or page.

    Never updated after insert. Normalisation reads it and writes elsewhere.
    """

    __tablename__ = "raw_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    tenant_id: Mapped[str] = mapped_column(String(36), index=True)
    plant_id: Mapped[str] = mapped_column(ForeignKey("plants.id"), index=True)

    source: Mapped[RecordSource] = mapped_column(String(20))
    # Provider message id / file+sheet+row. Unique per source so a webhook retry
    # cannot create the record twice.
    external_id: Mapped[str | None] = mapped_column(String(200), default=None)
    raw_text: Mapped[str] = mapped_column(Text)
    reporter: Mapped[str | None] = mapped_column(String(200), default=None)
    source_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_raw_source_external"),
        Index("ix_raw_plant_received", "plant_id", "received_at"),
    )


class StagedRecord(Base, TimestampMixin):
    """An extraction awaiting routing: auto-approved, or queued for human review."""

    __tablename__ = "staged_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    tenant_id: Mapped[str] = mapped_column(String(36), index=True)
    plant_id: Mapped[str] = mapped_column(ForeignKey("plants.id"), index=True)
    raw_record_id: Mapped[str] = mapped_column(
        ForeignKey("raw_records.id", ondelete="RESTRICT"), index=True
    )

    status: Mapped[StagedStatus] = mapped_column(String(20), default=StagedStatus.EXTRACTED)

    occurred_on: Mapped[date | None] = mapped_column(Date, default=None)
    machine_text: Mapped[str | None] = mapped_column(String(300), default=None)
    machine_id: Mapped[str | None] = mapped_column(
        ForeignKey("machines.id"), default=None, index=True
    )
    failure_mode: Mapped[str | None] = mapped_column(String(200), default=None)
    action: Mapped[str | None] = mapped_column(Text, default=None)
    parts: Mapped[list] = mapped_column(JSON, default=list)
    downtime_hours: Mapped[float | None] = mapped_column(Float, default=None)
    technician: Mapped[str | None] = mapped_column(String(200), default=None)
    kind: Mapped[RecordKind] = mapped_column(String(20), default=RecordKind.BREAKDOWN)

    # Confidence breakdown, kept so a reviewer can see *which* field is uncertain
    # rather than only that the row as a whole scored low.
    field_confidence: Mapped[dict] = mapped_column(JSON, default=dict)
    resolution_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    resolution_method: Mapped[ResolutionMethod] = mapped_column(
        String(20), default=ResolutionMethod.UNRESOLVED
    )
    overall_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    review_reasons: Mapped[list] = mapped_column(JSON, default=list)

    # Cost and latency attribution, per docs/03 section 6.
    llm_model: Mapped[str | None] = mapped_column(String(100), default=None)
    llm_input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    llm_output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    llm_latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    llm_cost_inr: Mapped[float] = mapped_column(Float, default=0.0)
    error: Mapped[str | None] = mapped_column(Text, default=None)

    raw_record: Mapped[RawRecord] = relationship()

    __table_args__ = (Index("ix_staged_plant_status", "plant_id", "status"),)


class MaintenanceRecord(Base, TimestampMixin):
    """The system of record. Always traceable to the raw text it came from."""

    __tablename__ = "maintenance_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    tenant_id: Mapped[str] = mapped_column(String(36), index=True)
    plant_id: Mapped[str] = mapped_column(ForeignKey("plants.id"), index=True)

    # NOT NULL by design: a record with no raw ancestor is unrepresentable.
    raw_record_id: Mapped[str] = mapped_column(
        ForeignKey("raw_records.id", ondelete="RESTRICT"), index=True
    )
    staged_record_id: Mapped[str | None] = mapped_column(
        ForeignKey("staged_records.id"), default=None
    )
    machine_id: Mapped[str | None] = mapped_column(
        ForeignKey("machines.id"), default=None, index=True
    )

    occurred_on: Mapped[date | None] = mapped_column(Date, default=None, index=True)
    machine_text: Mapped[str | None] = mapped_column(String(300), default=None)
    failure_mode: Mapped[str | None] = mapped_column(String(200), default=None, index=True)
    action: Mapped[str | None] = mapped_column(Text, default=None)
    parts: Mapped[list] = mapped_column(JSON, default=list)
    downtime_hours: Mapped[float | None] = mapped_column(Float, default=None)
    technician: Mapped[str | None] = mapped_column(String(200), default=None)
    kind: Mapped[RecordKind] = mapped_column(String(20), default=RecordKind.BREAKDOWN)

    status: Mapped[RecordStatus] = mapped_column(String(20), default=RecordStatus.ACTIVE)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

    raw_record: Mapped[RawRecord] = relationship()
    machine: Mapped[Machine | None] = relationship()

    __table_args__ = (
        Index("ix_record_plant_machine_date", "plant_id", "machine_id", "occurred_on"),
        CheckConstraint(
            "downtime_hours IS NULL OR downtime_hours >= 0", name="ck_record_downtime_non_negative"
        ),
    )
