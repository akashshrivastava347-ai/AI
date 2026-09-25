# LogSense AI Agent Service

Story 1 of the delivery backlog: **a technician's message becomes a structured,
traceable maintenance record.**

```
message ──▶ raw record ──▶ extraction ──▶ machine ──▶ confidence ──▶ record
            (immutable)     (LLM)          resolution   routing       or review queue
```

Covers backlog stories `LS-060`, `LS-061`, `LS-063`, `LS-064`, `LS-070`, `LS-040`,
`LS-041`. WhatsApp delivery (`LS-170`–`LS-174`) is Story 2 — the pipeline is already
shaped for it, which is why ingestion is idempotent on a provider message id.

## Run it in 30 seconds — no API key needed

The deterministic offline adapter means you can review the whole pipeline before any
provider credentials or Meta onboarding exist.

```bash
cd services/ai-agent
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"

.venv/bin/python -m logsense_ai.cli --provider fake demo
```

```
  [Ramesh] Line 3 ka conveyor motor band tha, bearing change kiya, 2 ghante
      AUTO-APPROVED  confidence=0.88
      machine: Line 3 Conveyor Motor

  [Suresh] MTR brng noise L3 conv, replcd 6205ZZ, algnmnt chk, OK
      -> PENDING_REVIEW  confidence=0.88
      flags:   machine_ambiguous: Line 3 Conveyor Motor (1.00) vs Line 3 Conveyor Gearbox (1.00)

  [Priya] लाइन 2 कैपिंग मोटर गरम हो रहा था, बेयरिंग बदला, डेढ़ घंटा बंद
      AUTO-APPROVED  confidence=0.88
      machine: Line 2 Capping Motor
  ...
  auto-approved 4/6 (67%)  |  2 queued for review
```

Both queued messages are queued for *correct* reasons. `"L3 conv"` genuinely could be
the Line 3 conveyor **motor** or its **gearbox** — a human decides once, an alias is
written, and the question is never asked again. `"machine kharab hai"` genuinely says
nothing. **Refusing to guess is the feature.**

## Run it against a real model

```bash
cp .env.example .env
# put your key in .env — it is git-ignored
.venv/bin/python -m logsense_ai.cli demo
```

## Run the API

```bash
.venv/bin/alembic upgrade head
.venv/bin/python -m logsense_ai.cli seed
.venv/bin/uvicorn logsense_ai.api.main:app --reload     # docs at /docs
```

| Endpoint | Purpose |
|---|---|
| `POST /api/v1/messages` | Ingest one technician message |
| `GET /api/v1/plants/{id}/records` | Records that were accepted |
| `GET /api/v1/plants/{id}/review-queue` | Extractions needing a human, worst first |
| `GET /api/v1/raw-records/{id}` | **View Source** — the original message, verbatim |
| `GET /health` | Liveness + configured provider |

## What is enforced, not just intended

| Principle | How it is enforced |
|---|---|
| Raw data is immutable | `raw_records` is written once; `RESTRICT` FK blocks deletion while referenced — proven by a test that fails without it |
| Every record has provenance | `maintenance_records.raw_record_id` is `NOT NULL`. A record without a source is unrepresentable |
| Low confidence goes to a human | Multiplicative scoring against a per-plant threshold; ambiguity blocks approval regardless of score |
| Never guess a number | Downtime is parsed deterministically or left `null`. Null is counted in coverage; zero would corrupt every total |
| Retries never duplicate | Ingestion is idempotent on `(source, external_id)` — a WhatsApp redelivery cannot double a plant's downtime |
| Provider outage loses nothing | The raw record commits *before* the LLM is called; failures become retryable rows |
| Tenancy from day one | `tenant_id` on every table from the first migration; resolution is plant-scoped |

## Layout

```
src/logsense_ai/
  config.py            settings; every secret from the environment
  db.py                engine, session scope, declarative base
  domain/              enums + ORM models (the invariants live here)
  llm/                 provider port, OpenAI adapter, deterministic fake
  extraction/          Hinglish dictionary, schema, prompts, service
  resolution/          exact → alias → fuzzy machine resolver
  ingest/              pipeline + confidence scoring
  api/                 FastAPI surface
  cli.py               demo / ingest / show
```

## Development

```bash
.venv/bin/python -m pytest -q --cov=logsense_ai   # 80 tests, 87% coverage
.venv/bin/ruff check src tests
.venv/bin/ruff format src tests
```

Tests never call a live provider: CI that depends on someone else's uptime is CI that
fails during their incident.

## Notes for the next story

- **The dictionary is the moat, not the model.** `extraction/dictionary.py` is shared by
  extraction and (from Story 3) search, so the two can never disagree about what
  `brng` means. Devanagari entries need the Devanagari block in the tokeniser — a plain
  `\w` splits `मोटर` into `म` + `टर` and silently kills every Hindi/Marathi entry.
- **Fuzzy scoring is fragile.** `partial_token_set_ratio` and `WRatio` both saturate at
  ~100 for every candidate on these strings; only `token_set_ratio` discriminates. Name
  and asset code are scored separately — concatenating them dilutes an exact match.
- **The semantic (embedding) resolution stage is deliberately absent.** It needs an
  embedding provider and a backfill job; the first three stages carry most plants and
  alias learning closes the gap faster.
- **Alias learning is not wired up yet.** The `machine_aliases` table and the resolver
  stage exist; the validation action that *writes* an alias from a human correction is
  `LS-072`, in Story 3.
