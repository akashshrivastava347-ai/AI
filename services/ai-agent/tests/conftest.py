"""Shared fixtures.

Every test runs against an in-memory SQLite database and the deterministic fake
provider. No network, no API key, no cost — CI must never depend on a live LLM.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from logsense_ai.config import Settings
from logsense_ai.db import Base
from logsense_ai.domain.models import Plant
from logsense_ai.ingest.pipeline import IngestPipeline
from logsense_ai.llm.fake import FakeLlmClient
from logsense_ai.seed import seed_demo_plant


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # one shared connection, so :memory: survives
        future=True,
    )

    # SQLite disables foreign keys by default, which would let a RESTRICT
    # constraint pass silently in tests and fail only in production on Postgres.
    @event.listens_for(engine, "connect")
    def _enforce_foreign_keys(dbapi_connection, _record):  # type: ignore[no-untyped-def]
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
    db = factory()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()


@pytest.fixture
def settings() -> Settings:
    return Settings(llm_provider="fake", default_auto_approve_threshold=0.80)


@pytest.fixture
def plant(session: Session) -> Plant:
    created = seed_demo_plant(session)
    session.commit()
    return created


@pytest.fixture
def fake_llm() -> FakeLlmClient:
    return FakeLlmClient()


@pytest.fixture
def pipeline(session: Session, fake_llm: FakeLlmClient, settings: Settings) -> IngestPipeline:
    return IngestPipeline(session, fake_llm, settings=settings)
