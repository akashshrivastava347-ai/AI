"""Database engine, session management and the declarative base."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from logsense_ai.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for every ORM model."""


def _engine_kwargs(url: str) -> dict:
    # SQLite needs check_same_thread off for the FastAPI threadpool; Postgres wants
    # pre-ping so a recycled connection does not surface as a request error.
    if url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {"pool_pre_ping": True}


_settings = get_settings()
engine = create_engine(
    _settings.database_url,
    echo=_settings.sql_echo,
    future=True,
    **_engine_kwargs(_settings.database_url),
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Transactional scope. Commits on success, rolls back on any exception."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Iterator[Session]:
    """FastAPI dependency yielding a request-scoped session."""
    with session_scope() as session:
        yield session
