"""Command-line entry point.

Exists so the pipeline is reviewable today: no WhatsApp credentials, no API key,
no server. ``logsense demo`` runs a scripted technician conversation against the
deterministic adapter and prints exactly what would be stored.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

from sqlalchemy import select

from logsense_ai.config import get_settings
from logsense_ai.db import Base, engine, session_scope
from logsense_ai.domain.enums import RecordSource
from logsense_ai.domain.models import MaintenanceRecord, StagedRecord
from logsense_ai.ingest.pipeline import IngestPipeline
from logsense_ai.llm import build_llm_client
from logsense_ai.llm.fake import FakeLlmClient
from logsense_ai.seed import seed_demo_plant

# Messages of the kind this product actually receives: Hinglish, Devanagari,
# shorthand, and one deliberately vague message that must NOT be auto-approved.
DEMO_MESSAGES: list[tuple[str, str]] = [
    ("Ramesh", "Line 3 ka conveyor motor band tha, bearing change kiya, 2 ghante"),
    ("Suresh", "MTR brng noise L3 conv, replcd 6205ZZ, algnmnt chk, OK"),
    ("Priya", "लाइन 2 कैपिंग मोटर गरम हो रहा था, बेयरिंग बदला, डेढ़ घंटा बंद"),
    ("Amit", "L1 filling pump seal leakage, replaced seal, 45 min downtime"),
    ("Vikram", "machine kharab hai"),
    ("Ramesh", "Utilities air compressor ka belt tuta, naya belt lagaya, ek shift"),
]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="logsense", description="LogSense AI agent service")
    parser.add_argument(
        "--provider",
        choices=["openai", "fake"],
        help="Override the configured LLM provider. 'fake' needs no API key.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db", help="Create tables directly (dev only; prefer alembic upgrade head)")
    sub.add_parser("seed", help="Create or update the demo plant")
    sub.add_parser("demo", help="Run the scripted technician conversation end to end")

    ingest = sub.add_parser("ingest", help="Ingest one message")
    ingest.add_argument("text", help="The technician's message")
    ingest.add_argument("--reporter", default=None)
    ingest.add_argument("--external-id", default=None)

    sub.add_parser("show", help="Show stored records and the review queue")
    return parser


def _client(provider: str | None):
    settings = get_settings()
    if provider == "fake" or (provider is None and settings.llm_provider == "fake"):
        return FakeLlmClient()
    if provider:
        return build_llm_client(settings.model_copy(update={"llm_provider": provider}))
    return build_llm_client(settings)


def _print_result(label: str, text: str, result) -> None:
    mark = "AUTO-APPROVED" if result.auto_approved else f"-> {result.status.value}"
    print(f"\n  [{label}] {text}")
    print(f"      {mark}  confidence={result.overall_confidence:.2f}")
    if result.machine_name:
        print(f"      machine: {result.machine_name}")
    if result.review_reasons:
        print(f"      flags:   {', '.join(result.review_reasons[:4])}")


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    logging.basicConfig(
        level=get_settings().log_level, format="%(levelname)s %(name)s: %(message)s"
    )

    if args.command == "init-db":
        Base.metadata.create_all(engine)
        print(f"schema created at {get_settings().database_url}")
        return 0

    if args.command == "seed":
        with session_scope() as session:
            plant = seed_demo_plant(session)
            print(f"demo plant ready: {plant.name}  id={plant.id}")
        return 0

    if args.command == "demo":
        Base.metadata.create_all(engine)
        with session_scope() as session:
            plant = seed_demo_plant(session)
            pipeline = IngestPipeline(session, _client(args.provider))
            print(f"\nPlant: {plant.name}  (auto-approve at {plant.auto_approve_threshold:.2f})")
            print("=" * 72)
            approved = 0
            for reporter, text in DEMO_MESSAGES:
                result = pipeline.ingest_message(
                    plant_id=plant.id, raw_text=text, reporter=reporter
                )
                _print_result(reporter, text, result)
                approved += int(result.auto_approved)
            total = len(DEMO_MESSAGES)
            print("\n" + "=" * 72)
            print(
                f"  auto-approved {approved}/{total} "
                f"({approved / total:.0%})  |  {total - approved} queued for review"
            )
            print("  This rate is THE number the business rests on (docs/00 section 10).")
        return 0

    if args.command == "ingest":
        with session_scope() as session:
            plant = seed_demo_plant(session)
            pipeline = IngestPipeline(session, _client(args.provider))
            result = pipeline.ingest_message(
                plant_id=plant.id,
                raw_text=args.text,
                source=RecordSource.API,
                external_id=args.external_id,
                reporter=args.reporter,
            )
            print(json.dumps(result.__dict__, indent=2, default=str))
        return 0

    if args.command == "show":
        with session_scope() as session:
            records = list(session.scalars(select(MaintenanceRecord)))
            queued = list(
                session.scalars(select(StagedRecord).where(StagedRecord.status == "PENDING_REVIEW"))
            )
            print(f"\nMaintenance records ({len(records)}):")
            for r in records:
                print(
                    f"  - {r.failure_mode or '?':22} {r.action or '?':24} "
                    f"downtime={r.downtime_hours}  conf={r.confidence:.2f}"
                )
            print(f"\nReview queue ({len(queued)}):")
            for s in queued:
                print(
                    f"  - {s.machine_text or '?':28} conf={s.overall_confidence:.2f}  "
                    f"{', '.join(s.review_reasons[:2])}"
                )
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
