"""Domain enumerations.

String-valued so that database rows stay readable and stable across releases.
"""

from __future__ import annotations

from enum import StrEnum


class RecordSource(StrEnum):
    """Where a raw record was born. Every maintenance record traces back to one."""

    WHATSAPP = "WHATSAPP"
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    API = "API"


class RecordKind(StrEnum):
    BREAKDOWN = "BREAKDOWN"
    PREVENTIVE = "PREVENTIVE"
    INSPECTION = "INSPECTION"
    OTHER = "OTHER"


class StagedStatus(StrEnum):
    """Lifecycle of an extraction before it becomes a maintenance record."""

    EXTRACTED = "EXTRACTED"
    AUTO_APPROVED = "AUTO_APPROVED"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class RecordStatus(StrEnum):
    ACTIVE = "ACTIVE"
    CORRECTED = "CORRECTED"
    DELETED = "DELETED"


class ResolutionMethod(StrEnum):
    """Which stage of the resolver cascade produced a match.

    Recorded per record so that a bad mapping can be traced to the stage that caused
    it rather than guessed at.
    """

    EXACT_CODE = "EXACT_CODE"
    EXACT_NAME = "EXACT_NAME"
    ALIAS = "ALIAS"
    FUZZY = "FUZZY"
    UNRESOLVED = "UNRESOLVED"


class AliasSource(StrEnum):
    IMPORT = "IMPORT"
    VALIDATION = "VALIDATION"
    MANUAL = "MANUAL"
