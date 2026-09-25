#!/usr/bin/env python3
"""
LogSense v2 — backlog as code.

Single source of truth for the delivery plan. Running this regenerates:

    docs/02-BACKLOG.md                  human-readable, sprint-ordered backlog
    backlog/logsense-jira-import.csv    Jira / Linear / Azure Boards CSV import

Keeping both outputs generated from one dataset means the board and the document
can never disagree about scope, points or dependencies.

    python3 tools/backlog.py            # regenerate both outputs
    python3 tools/backlog.py --check    # validate only (used in CI)
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------------------
# Releases and sprints
# --------------------------------------------------------------------------------------

RELEASES = [
    dict(
        key="R0",
        name="Validation & Foundation",
        sprints=["S0", "S1"],
        goal="Prove somebody will pay before writing the expensive parts; stand up the "
             "platform, tenancy and CI that everything else assumes.",
        exit_criteria=[
            "At least one paid design partner signed with a written pilot SOW.",
            "Three real (anonymised) maintenance files in hand and manually audited.",
            "App boots from one compose command; CI green with coverage and ArchUnit gates.",
            "Multi-tenant isolation proven by an automated cross-tenant test suite.",
        ],
    ),
    dict(
        key="R1",
        name="The Pilot Slice",
        sprints=["S2", "S3", "S4", "S5"],
        goal="Take one real customer file from upload to searchable, validated records — "
             "and measure the auto-approval rate the whole business model rests on.",
        exit_criteria=[
            "A design partner's real file imports end-to-end without engineering intervention.",
            "Auto-approval rate measured on real data and reported to the customer.",
            "Alias bulk-mapping demonstrably maps a 30+ record group in one action.",
            "Every record traceable to its original file, sheet and row.",
        ],
    ),
    dict(
        key="R2",
        name="Intelligence",
        sprints=["S6", "S7", "S8", "S9"],
        goal="Make the plant's history answerable. Search, deterministic analytics, the "
             "agent runtime, the Reliability Copilot, and the guardrails and evals that "
             "make its output trustworthy.",
        exit_criteria=[
            "Copilot answers the six benchmark questions with correct numbers and citations.",
            "Answer numeric accuracy is 100% on the golden set; CI blocks regressions.",
            "Agent runs are fully traced, budgeted and replayable.",
            "Degraded mode verified by killing the LLM provider in staging.",
        ],
    ),
    dict(
        key="R3",
        name="Proactive & Field",
        sprints=["S10", "S11", "S12"],
        goal="Stop waiting to be asked. Watchtower briefings, generative work artifacts, "
             "the WhatsApp field agent and the approval inbox that governs every agent write.",
        exit_criteria=[
            "Daily briefing delivered to a real plant for 14 consecutive days.",
            "An engineer approves an agent-drafted RCA and exports it with citations intact.",
            "Technicians create records via WhatsApp without training beyond one demo.",
            "No agent write reaches the database without a recorded human approval.",
        ],
    ),
    dict(
        key="R4",
        name="Industry Hardening",
        sprints=["S13", "S14", "S15"],
        goal="Make it sellable to a second and third plant without heroics: compliant, "
             "observable, metered, recoverable and penetration-tested.",
        exit_criteria=[
            "Third-party penetration test passed with all high findings remediated.",
            "DPDP obligations implemented; sub-processor register and DPA ready for signature.",
            "SLOs defined with alerting; a restore drill executed end-to-end.",
            "Cost per plant per month measured and inside the pricing model.",
        ],
    ),
]

SPRINT_ORDER = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15"]

# --------------------------------------------------------------------------------------
# Epics
# --------------------------------------------------------------------------------------

EPICS = [
    dict(key="EPIC-00", name="Discovery & Design-Partner Validation", release="R0",
         component="GTM",
         goal="Find out whether anyone will pay, before the expensive engineering starts."),
    dict(key="EPIC-01", name="Platform Foundation & Developer Experience", release="R0",
         component="Platform",
         goal="A boring, fast, well-instrumented base every other epic builds on."),
    dict(key="EPIC-02", name="Identity, Tenancy & Access Control", release="R0",
         component="Security",
         goal="Multi-tenant isolation and per-plant RBAC that is proven, not assumed."),
    dict(key="EPIC-03", name="Plant, Asset & Taxonomy Master Data", release="R1",
         component="Domain",
         goal="The asset hierarchy and vocabulary every record resolves against."),
    dict(key="EPIC-04", name="Maintenance Record Core & Provenance", release="R1",
         component="Domain",
         goal="The system of record, with an immutable chain back to the original raw row."),
    dict(key="EPIC-05", name="Ingestion Pipeline", release="R1",
         component="Ingestion",
         goal="Files in any shape become verbatim raw records, safely and resumably."),
    dict(key="EPIC-06", name="Generative Extraction & Normalisation", release="R1",
         component="AI",
         goal="Turn Hinglish shorthand into structured fields with calibrated confidence."),
    dict(key="EPIC-07", name="Entity Resolution & Alias Learning", release="R1",
         component="AI",
         goal='"Conv Motor-3" resolves to a real asset, and the system never asks twice.'),
    dict(key="EPIC-08", name="Human-in-the-Loop Validation Workbench", release="R1",
         component="Product",
         goal="Make reviewing 200 uncertain rows a 20-minute job, not a 2-day job."),
    dict(key="EPIC-09", name="Hybrid Search & Retrieval", release="R2",
         component="AI",
         goal="Find the right records from shorthand, Hindi, Marathi or English."),
    dict(key="EPIC-10", name="Deterministic Analytics & KPI Engine", release="R2",
         component="Domain",
         goal="Every number in the product, computed in SQL and reproducible forever."),
    dict(key="EPIC-11", name="Agent Runtime & Tool Platform", release="R2",
         component="AI-Platform",
         goal="The planner, tool registry, budgets, memory and traces all agents share."),
    dict(key="EPIC-12", name="Reliability Copilot", release="R2",
         component="AI",
         goal="Multi-step investigation that answers 'why does this keep happening?'."),
    dict(key="EPIC-13", name="Trust, Guardrails & Verification", release="R2",
         component="AI-Safety",
         goal="Structurally prevent the product from ever stating an ungrounded number."),
    dict(key="EPIC-14", name="AI Evaluation & Quality Harness", release="R2",
         component="AI-Quality",
         goal="Know whether a prompt change made the product better or worse, before shipping."),
    dict(key="EPIC-15", name="Pattern Detection & Watchtower Agent", release="R3",
         component="AI",
         goal="The product stops waiting to be asked and starts bringing findings to people."),
    dict(key="EPIC-16", name="Generative Work Artifacts", release="R3",
         component="Product",
         goal="Draft the documents engineers hate writing, with citations intact."),
    dict(key="EPIC-17", name="WhatsApp Field Agent", release="R3",
         component="Integrations",
         goal="Capture new records where technicians already are, in the language they use."),
    dict(key="EPIC-18", name="Plant Knowledge Base", release="R3",
         component="AI",
         goal="Ground answers in manuals, SOPs and past RCAs, not only in log rows."),
    dict(key="EPIC-19", name="Proposal & Approval Inbox", release="R3",
         component="Product",
         goal="The governed write path: agents propose, named humans dispose, everything reverts."),
    dict(key="EPIC-20", name="AI Observability, Cost & FinOps", release="R4",
         component="Platform",
         goal="Know the quality, latency and rupee cost of every agent run and every tenant."),
    dict(key="EPIC-21", name="Security, Privacy & Compliance", release="R4",
         component="Security",
         goal="Survive a plant IT head's security review and India's DPDP Act."),
    dict(key="EPIC-22", name="Reliability, SRE & Deployment", release="R4",
         component="Platform",
         goal="Ship safely, stay up, and be able to prove you can restore from backup."),
    dict(key="EPIC-23", name="Commercialization & Onboarding", release="R4",
         component="GTM",
         goal="Meter it, bill it, and onboard plant number three without a founder present."),
    dict(key="EPIC-24", name="Frontend Product Application", release="R1",
         component="Frontend",
         goal="Turn the demo prototype into the real multilingual product UI."),
]

STORIES: list[dict] = []

# --------------------------------------------------------------------------------------
# EPIC-00 — Discovery & Design-Partner Validation
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-001", epic="EPIC-00", type="Spike", points=5, priority="P0", sprint="S0",
         component="GTM", labels=["discovery", "founder-led"], depends=[],
         summary="Run 15 structured discovery interviews with maintenance leaders",
         narrative="As a founder, I want evidence of who owns the pain and who signs the "
                   "cheque, so that I do not build a product for a buyer who does not exist.",
         ac=["Interview guide asks about the last three breakdowns and how each was diagnosed — listen first, never pitch.",
             "At least 15 interviews completed across at least 8 distinct plants.",
             "Notes captured in one shared repository, tagged by pain, role and plant size.",
             "Written synthesis names the top three pains and, per plant, who signs a purchase order.",
             "Explicit kill/continue call recorded: if nobody will share a file or discuss a paid pilot, the wedge changes before any backend code is written."]),
    dict(key="LS-002", epic="EPIC-00", type="Spike", points=5, priority="P0", sprint="S0",
         component="GTM", labels=["discovery", "data-risk"], depends=["LS-001"],
         summary="Collect and manually audit three real historical maintenance files",
         narrative="As a founder, I want to know what real plant data actually looks like, "
                   "so that the messy-data promise is tested before it is sold.",
         ac=["At least three real (anonymised) files obtained under NDA from different plants.",
             "100 random rows per file extracted by hand into the target schema.",
             "Achievable per-field accuracy recorded per file (date, machine, failure mode, action, parts, downtime).",
             "Worst-case formats catalogued: merged cells, multi-sheet layouts, scanned registers, free-text-only columns.",
             "Findings feed the extraction golden set (LS-140) and the realistic auto-approval target."]),
    dict(key="LS-003", epic="EPIC-00", type="Task", points=3, priority="P0", sprint="S0",
         component="GTM", labels=["pricing", "legal"], depends=["LS-001"],
         summary="Define and price the four-week paid pilot offer",
         narrative="As a founder, I want a repeatable written pilot offer, so that every "
                   "sales conversation converges instead of being renegotiated from scratch.",
         ac=["One-page SOW covering success criteria, data scope, timeline, named champion, pilot fee and the annual price if it succeeds.",
             "Success criteria are objectively measurable (for example: ten real historical questions answered correctly with citations).",
             "Internal floor price agreed and documented; free pilots are explicitly excluded.",
             "Reviewed by a CA or lawyer for Indian contracting norms."]),
    dict(key="LS-004", epic="EPIC-00", type="Story", points=8, priority="P0", sprint="S1",
         component="GTM", labels=["design-partner"], depends=["LS-002", "LS-003", "LS-006"],
         summary="Sign the first paid design partner",
         narrative="As a founder, I want one plant paying for a pilot, so that the pain is "
                   "proven with money rather than politeness.",
         ac=["Signed SOW and NDA with a named champion and an executive sponsor.",
             "Pilot fee invoiced and received — a free pilot does not satisfy this story.",
             "Historical data scope agreed, with a date for the first file handover.",
             "Pricing protection and case-study permission negotiated in exchange for design-partner status."]),
    dict(key="LS-005", epic="EPIC-00", type="Task", points=2, priority="P1", sprint="S0",
         component="GTM", labels=["legal", "brand"], depends=[],
         summary="Clear the product name: trademark and domain search",
         narrative="As a founder, I want naming risk resolved before the name is on a "
                   "contract, so that a rename after ten pilots never happens.",
         ac=["Indian trademark search completed in classes 9 and 42; conflicting marks listed.",
             "Primary domain and the obvious variants checked and secured.",
             "Go/no-go decision on the name recorded with reasoning; fallback name shortlisted.",
             "Company and IP assignment position documented for review with a lawyer."]),
    dict(key="LS-006", epic="EPIC-00", type="Task", points=3, priority="P0", sprint="S0",
         component="GTM", labels=["legal", "security", "trust"], depends=[],
         summary="Draft NDA, data-processing terms and a one-page security FAQ",
         narrative="As a plant IT head, I want clear answers about where my maintenance data "
                   "goes, so that I can approve a pilot without a three-month review.",
         ac=["NDA and DPA drafted covering ownership, deletion or return on exit, and a no-training-on-customer-data commitment.",
             "LLM sub-processor disclosure written in plain language, including the zero-retention option.",
             "One-page security FAQ covers encryption, per-plant isolation, audit logs, backups and access control.",
             "DPDP Act 2023 consent and purpose language drafted for technician personal data.",
             "Reviewed by a lawyer before being sent to any prospect."]),
    dict(key="LS-007", epic="EPIC-00", type="Spike", points=3, priority="P1", sprint="S1",
         component="GTM", labels=["positioning"], depends=["LS-001"],
         summary="Competitive teardown against CMMS incumbents and general-purpose chatbots",
         narrative="As a founder, I want a sharp answer to 'why not UpKeep, or just "
                   "ChatGPT?', so that the wedge holds up in a real sales meeting.",
         ac=["Teardown of at least five relevant players covering positioning, pricing and India presence.",
             "One-paragraph differentiated answer written for each of: an incumbent CMMS, a generic chatbot, and doing nothing.",
             "The 'do nothing / Excel and memory' competitor is treated as the primary one.",
             "Findings folded into the pitch and into docs/00-PRODUCT-VISION.md."]),
    dict(key="LS-008", epic="EPIC-00", type="Task", points=3, priority="P0", sprint="S1",
         component="GTM", labels=["metrics"], depends=["LS-003"],
         summary="Define the north-star metric tree and the per-pilot scorecard",
         narrative="As a founder, I want agreed leading indicators, so that a failing pilot "
                   "is visible in week two rather than at renewal.",
         ac=["North-star metric selected and justified; supporting input metrics mapped beneath it.",
             "Pilot scorecard defines auto-approval %, corrections per 100 records, queue burn-down time, weekly active engineers, WhatsApp records per week and time-to-first-answer.",
             "Internal red lines set (for example: auto-approval below 85% after alias mapping is a product problem, not a sales problem).",
             "Scorecard template ready to be populated manually before LS-147 automates it."]),
]

# --------------------------------------------------------------------------------------
# EPIC-01 — Platform Foundation & Developer Experience
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-010", epic="EPIC-01", type="Story", points=3, priority="P0", sprint="S0",
         component="Platform", labels=["foundation"], depends=[],
         summary="Bootstrap the Spring Boot 3 / Java 21 modular-monolith skeleton",
         narrative="As an engineer, I want a running application with enforced module "
                   "boundaries, so that the monolith stays extractable later.",
         ac=["Spring Boot 3.x on Java 21 builds and boots with an actuator health endpoint.",
             "Package structure com.logsense.<module> created for every module in reference doc 02.",
             "Constructor injection, DTO-at-the-boundary and no-entity-serialization conventions documented.",
             "Application starts with no database present in a 'lite' profile for fast unit tests."]),
    dict(key="LS-011", epic="EPIC-01", type="Story", points=3, priority="P0", sprint="S0",
         component="Platform", labels=["devex"], depends=["LS-010"],
         summary="One-command local dev stack via Docker Compose",
         narrative="As an engineer, I want the whole stack up with one command, so that "
                   "onboarding is minutes rather than a day.",
         ac=["docker compose up starts PostgreSQL 16 with pgvector and pg_trgm, plus MinIO.",
             "Application connects to all services with zero manual configuration.",
             "Named volumes persist data across restarts; a documented reset command wipes them.",
             "README documents prerequisites and the full first-run sequence."]),
    dict(key="LS-012", epic="EPIC-01", type="Story", points=2, priority="P0", sprint="S0",
         component="Platform", labels=["database"], depends=["LS-011"],
         summary="Flyway migrations with a forward-only policy",
         narrative="As an engineer, I want schema changes versioned and forward-only, so "
                   "that production schema drift is impossible.",
         ac=["Flyway wired with a documented V<n>__<description>.sql naming convention.",
             "ddl-auto is validate in every profile except the throwaway test profile.",
             "A CI lint rejects edits to already-applied migration files.",
             "Rollback policy documented: forward fixes only, never destructive down-migrations."]),
    dict(key="LS-013", epic="EPIC-01", type="Story", points=3, priority="P0", sprint="S0",
         component="Platform", labels=["api-contract"], depends=["LS-010"],
         summary="Standard error envelope, stable error codes and a traceId filter",
         narrative="As an API consumer, I want every failure to look the same, so that "
                   "clients handle errors generically and support can trace any incident.",
         ac=["A single @RestControllerAdvice renders the error envelope from reference doc 17.",
             "Every response carries a traceId, propagated into logs and OpenTelemetry spans.",
             "Error codes are stable string constants, enumerated and documented.",
             "Contract tests assert the envelope shape for 400, 401, 403, 404, 409, 422, 424, 429 and 500."]),
    dict(key="LS-014", epic="EPIC-01", type="Story", points=2, priority="P0", sprint="S0",
         component="Platform", labels=["api-contract"], depends=["LS-013"],
         summary="Uniform pagination, filtering and sorting kernel",
         narrative="As an API consumer, I want identical paging semantics everywhere, so "
                   "that I write list-handling code once.",
         ac=["Shared page/size/sort request binding with server-side clamping of size.",
             "Consistent page response envelope with content, page, size, totalElements, totalPages.",
             "Sort fields are whitelisted per resource; an unknown field returns 400, never a 500.",
             "Deep-paging guard prevents unbounded offsets on million-row tables."]),
    dict(key="LS-015", epic="EPIC-01", type="Story", points=5, priority="P0", sprint="S1",
         component="Platform", labels=["async"], depends=["LS-012", "LS-013"],
         summary="Database-backed async job framework with pollable status",
         narrative="As a user starting a long import, I want to poll progress, so that the "
                   "UI shows real movement instead of a spinner.",
         ac=["jobs table with type, status, progress percentage, result reference and error detail.",
             "GET /api/v1/jobs/{id} returns live status; terminal states are immutable.",
             "Jobs survive an application restart and resume or fail cleanly, never hang in RUNNING.",
             "Worker concurrency is bounded and configurable; no Kafka or external broker is introduced."]),
    dict(key="LS-016", epic="EPIC-01", type="Story", points=3, priority="P0", sprint="S1",
         component="Platform", labels=["audit", "compliance"], depends=["LS-012"],
         summary="Append-only audit log service",
         narrative="As a compliance reviewer, I want every consequential action recorded "
                   "immutably, so that an audit can reconstruct who did what.",
         ac=["audit_logs table is append-only; UPDATE and DELETE are revoked at the database role level.",
             "Records actor, tenant, plant, action, entity type, entity id, before/after summary and timestamp.",
             "A single AuditService is the only write path; an ArchUnit rule forbids direct repository access.",
             "Audit writes participate in the caller's transaction so an action and its audit row commit together."]),
    dict(key="LS-017", epic="EPIC-01", type="Story", points=3, priority="P1", sprint="S1",
         component="Platform", labels=["api-contract", "ci"], depends=["LS-014"],
         summary="OpenAPI generation, Swagger UI and a spec-diff CI gate",
         narrative="As an API consumer, I want an accurate spec and advance warning of "
                   "breaking changes, so that integrations do not break silently.",
         ac=["springdoc generates the spec; Swagger UI is enabled in dev and disabled in prod.",
             "The committed spec is regenerated in CI and a drift check fails the build.",
             "A breaking-change diff against the previous release fails the build unless an override label is applied.",
             "Every endpoint documents auth requirements, roles and error codes."]),
    dict(key="LS-018", epic="EPIC-01", type="Story", points=5, priority="P0", sprint="S0",
         component="Platform", labels=["ci", "quality"], depends=["LS-010"],
         summary="CI pipeline with coverage and architecture gates",
         narrative="As an engineer, I want the build to enforce our standards, so that "
                   "quality does not depend on reviewer memory.",
         ac=["CI runs build, unit tests, integration tests on Testcontainers, and static analysis on every PR.",
             "Coverage gate fails the build below the agreed line and branch thresholds.",
             "ArchUnit rules enforce module boundaries, no cross-module repository access, and no JPA entity on a controller signature.",
             "Full pipeline completes in under 20 minutes; failures annotate the PR."]),
    dict(key="LS-019", epic="EPIC-01", type="Chore", points=2, priority="P2", sprint="S1",
         component="Platform", labels=["docs"], depends=[],
         summary="Architecture Decision Record process and repository documentation layout",
         narrative="As a future engineer, I want decisions and their reasoning recorded, so "
                   "that settled questions are not relitigated every quarter.",
         ac=["ADR template and numbered docs/adr/ directory established.",
             "Backfilled ADRs for: modular monolith, PostgreSQL with pgvector, agents-propose-humans-dispose, no fine-tuning on customer data.",
             "Contribution guide explains when an ADR is required.",
             "Documentation layout described in the repository README."]),
]

# --------------------------------------------------------------------------------------
# EPIC-02 — Identity, Tenancy & Access Control
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-020", epic="EPIC-02", type="Story", points=5, priority="P0", sprint="S1",
         component="Security", labels=["multi-tenancy"], depends=["LS-012"],
         summary="Organisation/tenant model with tenant_id on every table",
         narrative="As a company selling to multiple plants, I want tenancy in the schema "
                   "from the first migration, so that retrofitting it later never happens.",
         ac=["organisations table sits above plants; every business table carries a non-null tenant_id.",
             "A migration lint fails CI if a new table omits tenant_id without an explicit allowlist entry.",
             "Tenant context is resolved from the JWT and held in a request-scoped holder.",
             "Composite indexes lead with tenant_id on every hot query path."]),
    dict(key="LS-021", epic="EPIC-02", type="Story", points=8, priority="P0", sprint="S1",
         component="Security", labels=["multi-tenancy", "security"], depends=["LS-020"],
         summary="Enforce tenant isolation with row-level security and an automated cross-tenant suite",
         narrative="As a plant IT head, I want proof that another customer cannot see my "
                   "data, so that a security review does not stall the deal.",
         ac=["PostgreSQL row-level security policies applied to every tenant-scoped table.",
             "A Hibernate interceptor sets the tenant GUC on every connection checkout.",
             "An automated suite attempts cross-tenant reads and writes on every endpoint and expects 404, never 403 or an empty 200.",
             "A deliberately unscoped repository method fails the build via an ArchUnit rule.",
             "Test evidence is exportable as an artifact for customer security questionnaires."]),
    dict(key="LS-022", epic="EPIC-02", type="Story", points=5, priority="P0", sprint="S1",
         component="Security", labels=["auth"], depends=["LS-020"],
         summary="JWT access and refresh token lifecycle with rotation and revocation",
         narrative="As a user, I want long sessions without long-lived credentials, so that "
                   "a stolen token has a short blast radius.",
         ac=["Short-lived access token and long-lived refresh token with rotation on each use.",
             "Refresh-token reuse detection revokes the whole family and raises a security event.",
             "Logout, password change and deactivation all revoke outstanding tokens.",
             "JWT secret is required from the environment in prod; the app refuses to start without it."]),
    dict(key="LS-023", epic="EPIC-02", type="Story", points=5, priority="P0", sprint="S1",
         component="Security", labels=["auth"], depends=["LS-022"],
         summary="User CRUD, invite flow and first-login password set",
         narrative="As a plant admin, I want to invite my team by email, so that onboarding "
                   "does not require me to share passwords.",
         ac=["Invite issues a single-use, time-limited token; the invitee sets their own password on first login.",
             "Password policy enforced with BCrypt hashing; passwords never appear in logs or audit payloads.",
             "Deactivation is soft: login is blocked, history and authorship are retained.",
             "Every user lifecycle action writes an audit row."]),
    dict(key="LS-024", epic="EPIC-02", type="Story", points=5, priority="P0", sprint="S1",
         component="Security", labels=["rbac"], depends=["LS-023"],
         summary="Per-plant role assignment and a central PlantAccessService",
         narrative="As a plant admin, I want roles granted per plant, so that a group "
                   "engineer can see one plant without seeing all of them.",
         ac=["Five roles supported: SUPER_ADMIN (global), PLANT_ADMIN, ENGINEER, TECHNICIAN, VIEWER (per plant).",
             "A single PlantAccessService answers 'can user X act on plant Y as role Z' and is the only authority.",
             "Method-level authorization applied on every controller; a missing annotation fails an ArchUnit rule.",
             "Access to an out-of-scope plant returns 404 so plant existence cannot be probed."]),
    dict(key="LS-025", epic="EPIC-02", type="Story", points=5, priority="P0", sprint="S1",
         component="Security", labels=["rbac", "testing"], depends=["LS-024"],
         summary="Automated role-matrix authorization test suite",
         narrative="As a security reviewer, I want every endpoint tested against every role, "
                   "so that an IDOR is caught by CI rather than by a customer.",
         ac=["A generated matrix exercises every endpoint against all five roles plus anonymous.",
             "Expected outcomes are declared per endpoint; an undeclared endpoint fails the suite.",
             "Ownership-scoped resources are probed with another user's identifier and expect 404.",
             "The suite runs on every PR and its report is attached to the build."]),
    dict(key="LS-026", epic="EPIC-02", type="Story", points=3, priority="P0", sprint="S1",
         component="Security", labels=["auth", "hardening"], depends=["LS-022"],
         summary="Login rate limiting and brute-force lockout",
         narrative="As a security reviewer, I want credential stuffing to fail fast, so "
                   "that exposed passwords elsewhere do not compromise this system.",
         ac=["Per-identity and per-IP rate limits on login, refresh and password-reset endpoints.",
             "Progressive backoff and temporary lockout after a configured failure count.",
             "Rate-limit responses use 429 with a Retry-After header and the standard envelope.",
             "Lockout and limit events are audited and alertable."]),
    dict(key="LS-027", epic="EPIC-02", type="Story", points=8, priority="P2", sprint="S14",
         component="Security", labels=["enterprise", "sso"], depends=["LS-024"],
         summary="OIDC and SAML single sign-on for enterprise tenants",
         narrative="As a plant IT head, I want staff to sign in with our corporate identity "
                   "provider, so that access is centrally governed.",
         ac=["OIDC and SAML both supported, configurable per tenant.",
             "Group-to-role mapping configurable per tenant with a documented precedence order.",
             "Local password login can be disabled per tenant once SSO is enabled.",
             "Just-in-time user provisioning on first SSO login, with deactivation honoured."]),
    dict(key="LS-028", epic="EPIC-02", type="Story", points=5, priority="P2", sprint="S14",
         component="Security", labels=["integrations"], depends=["LS-024"],
         summary="Service accounts and scoped API keys",
         narrative="As an integrator, I want a non-human credential with narrow scope, so "
                   "that automated imports do not run as a person.",
         ac=["API keys are hashed at rest, prefixed for identification and displayed exactly once.",
             "Each key carries explicit scopes and an optional expiry; scope violations return 403.",
             "Keys are listable, revocable and show last-used time.",
             "Key usage is attributed in audit logs as the service account, never as a user."]),
]

# --------------------------------------------------------------------------------------
# EPIC-03 — Plant, Asset & Taxonomy Master Data
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-030", epic="EPIC-03", type="Story", points=3, priority="P0", sprint="S2",
         component="Domain", labels=["master-data"], depends=["LS-024"],
         summary="Plant and line CRUD",
         narrative="As a plant admin, I want to model my plant's lines, so that machines "
                   "and analytics have a hierarchy to roll up into.",
         ac=["Plant CRUD restricted to SUPER_ADMIN; line CRUD available to PLANT_ADMIN.",
             "Lines carry kind PRODUCTION or UTILITY, covering the utilities group without an extra hierarchy level.",
             "Line names are unique within a plant; conflicts return 409.",
             "Deleting a line with machines is refused with a clear, actionable error."]),
    dict(key="LS-031", epic="EPIC-03", type="Story", points=3, priority="P0", sprint="S2",
         component="Domain", labels=["master-data", "config"], depends=["LS-030"],
         summary="Plant settings: shifts, operating hours, downtime cost and thresholds",
         narrative="As a maintenance manager, I want plant-specific parameters, so that "
                   "KPIs and cost figures reflect my plant rather than a default.",
         ac=["Configurable shift definitions, operating hours per week, and downtime cost per line-hour in INR.",
             "Auto-approval confidence threshold configurable per plant with a documented default.",
             "Pattern detector thresholds (window months, minimum events) overridable per plant.",
             "Settings changes are audited with before and after values."]),
    dict(key="LS-032", epic="EPIC-03", type="Story", points=5, priority="P0", sprint="S2",
         component="Domain", labels=["master-data"], depends=["LS-030"],
         summary="Machine master CRUD with asset codes and criticality",
         narrative="As a plant admin, I want every machine registered with its code, so "
                   "that messy free text can be resolved to a real asset.",
         ac=["Machine carries name, asset code, line, type, criticality and commissioning date.",
             "Asset code is unique within a plant; conflicts return 409.",
             "Machines are searchable and paginated; a machine belongs to exactly one line.",
             "Deactivating a machine retains its history and excludes it from new resolution targets."]),
    dict(key="LS-033", epic="EPIC-03", type="Story", points=3, priority="P0", sprint="S2",
         component="Domain", labels=["taxonomy"], depends=["LS-030"],
         summary="Failure-mode taxonomy with plant-level extension",
         narrative="As a reliability engineer, I want a controlled failure vocabulary, so "
                   "that Pareto analysis groups the same failure consistently.",
         ac=["A seeded standard taxonomy ships with the product and is extensible per plant.",
             "Synonyms map to a canonical failure mode and are used by both extraction and search.",
             "Merging two failure modes re-points existing records and is audited.",
             "Taxonomy is exposed to the extraction prompt so the model chooses from a closed set."]),
    dict(key="LS-034", epic="EPIC-03", type="Story", points=3, priority="P0", sprint="S2",
         component="Domain", labels=["taxonomy", "parts"], depends=["LS-030"],
         summary="Spare parts catalogue with codes, synonyms and unit cost",
         narrative="As a maintenance manager, I want parts catalogued with the names people "
                   "actually type, so that '6205ZZ' and '6205 ZZ' are one part.",
         ac=["Part carries code, description, unit cost, unit of measure and optional lead time.",
             "Synonym list per part feeds both extraction and search expansion.",
             "Part codes are unique per plant; a normalised form is indexed for fuzzy lookup.",
             "Catalogue is importable in bulk and exportable as CSV."]),
    dict(key="LS-035", epic="EPIC-03", type="Story", points=5, priority="P1", sprint="S2",
         component="Domain", labels=["master-data", "onboarding"], depends=["LS-032", "LS-034"],
         summary="Bulk master-data import via CSV template",
         narrative="As a plant admin onboarding a new plant, I want to upload machines and "
                   "parts in bulk, so that setup takes an hour rather than a week.",
         ac=["Downloadable CSV templates for machines and parts with inline column documentation.",
             "Dry-run validation reports every row error before anything is written.",
             "Import is transactional per file: either all valid rows commit, or nothing does, per the chosen mode.",
             "Re-importing an existing code updates rather than duplicating, and the change is audited."]),
    dict(key="LS-036", epic="EPIC-03", type="Story", points=5, priority="P2", sprint="S3",
         component="Domain", labels=["onboarding", "integrations"], depends=["LS-035"],
         summary="Asset hierarchy import from an existing CMMS export",
         narrative="As a plant with SAP PM, I want my existing asset tree imported, so that "
                   "I do not retype 400 machines that already exist.",
         ac=["Importer accepts common SAP PM and generic CMMS functional-location exports.",
             "Hierarchy is flattened to the plant/line/machine model with a reviewable mapping report.",
             "Unmappable levels are reported rather than silently dropped.",
             "Original export is retained as an immutable artifact for traceability."]),
]

# --------------------------------------------------------------------------------------
# EPIC-04 — Maintenance Record Core & Provenance
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-040", epic="EPIC-04", type="Story", points=5, priority="P0", sprint="S2",
         component="Domain", labels=["core"], depends=["LS-032", "LS-033"],
         summary="Maintenance record entity, lifecycle and soft delete",
         narrative="As the system, I need one canonical record type, so that search, "
                   "analytics, patterns and AI all reason over the same thing.",
         ac=["Record carries date, machine, failure mode, action, downtime hours, technician, kind and source.",
             "Lifecycle ACTIVE to CORRECTED to DELETED (soft) is enforced by an explicit state machine.",
             "Deleted records are excluded from search, analytics and AI citations but retained in the database.",
             "Every state transition writes an audit row naming the actor."]),
    dict(key="LS-041", epic="EPIC-04", type="Story", points=5, priority="P0", sprint="S2",
         component="Domain", labels=["core", "trust"], depends=["LS-040"],
         summary="Immutable raw-record provenance chain powering View Source",
         narrative="As an engineer reading an AI answer, I want to see the original row, so "
                   "that I can judge the extraction myself.",
         ac=["Every maintenance record links to a raw_record; the link is non-nullable.",
             "raw_records are append-only with a RESTRICT foreign key; normalization never overwrites raw text.",
             "Provenance exposes file name, sheet, row number and the verbatim original text, or the WhatsApp conversation reference.",
             "A record with no raw ancestor cannot be created — enforced by a database constraint, not only by service code."]),
    dict(key="LS-042", epic="EPIC-04", type="Story", points=3, priority="P0", sprint="S3",
         component="Domain", labels=["core", "parts"], depends=["LS-040", "LS-034"],
         summary="Record-parts join and downtime normalisation to hours",
         narrative="As an analyst, I want parts and downtime in consistent units, so that "
                   "totals across three years of mixed formats are meaningful.",
         ac=["Many-to-many record-to-part join with quantity.",
             "Downtime normalised to decimal hours from minutes, hours, shifts and phrases such as '2 ghante'.",
             "Unparseable downtime is stored as null and counted in coverage reporting rather than guessed.",
             "Unit conversion rules are unit-tested against the real-file fixtures from LS-002."]),
    dict(key="LS-043", epic="EPIC-04", type="Story", points=5, priority="P0", sprint="S3",
         component="Domain", labels=["core", "audit"], depends=["LS-041"],
         summary="Manual record entry and audited correction with versioning",
         narrative="As an engineer, I want to correct a wrong record without destroying "
                   "history, so that the audit trail stays honest.",
         ac=["Manual entry creates a raw_record of kind MANUAL so the provenance invariant holds.",
             "Correction creates a new version; the prior version is retained and retrievable.",
             "Correction requires a reason; the diff, actor and reason are audited.",
             "Corrections trigger re-indexing and invalidate cached statistics for the affected machine."]),
    dict(key="LS-044", epic="EPIC-04", type="Story", points=3, priority="P0", sprint="S3",
         component="Domain", labels=["core", "api"], depends=["LS-040"],
         summary="Machine history endpoint with filters and pagination",
         narrative="As an engineer, I want a machine's full chronological history, so that "
                   "I can see everything that ever happened to it.",
         ac=["Filterable by date range, failure mode, kind, part and technician.",
             "Sorted newest-first by default with a stable secondary sort for deterministic paging.",
             "Each entry exposes a provenance link for View Source.",
             "Response time stays within budget on a machine with 10,000 records."]),
    dict(key="LS-045", epic="EPIC-04", type="Story", points=2, priority="P0", sprint="S3",
         component="Domain", labels=["events"], depends=["LS-040"],
         summary="Domain events for record created and updated",
         narrative="As a downstream module, I want to react to record changes, so that "
                   "indexing, stats invalidation and pattern rescans stay current.",
         ac=["In-process Spring application events published on create, update and delete.",
             "Consumers include search indexing, machine-stats cache invalidation and targeted pattern rescan.",
             "Event handling failures are retried and never roll back the originating transaction.",
             "No external broker is introduced, per the documented V1 scope decision."]),
    dict(key="LS-046", epic="EPIC-04", type="Story", points=3, priority="P1", sprint="S3",
         component="Domain", labels=["devex", "demo"], depends=["LS-041"],
         summary="Reference-plant seed data loader",
         narrative="As an engineer or a sales demo, I want a realistic populated plant in "
                   "one command, so that development and demos do not need a real customer.",
         ac=["Loader builds the reference plant hierarchy, machines, parts and records from reference doc 25.",
             "Runs only under the dev and demo profiles and refuses to run against prod.",
             "Seeded data reproduces the prototype's headline numbers exactly.",
             "Loader is idempotent and has a documented reset path."]),
]

# --------------------------------------------------------------------------------------
# EPIC-05 — Ingestion Pipeline
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-050", epic="EPIC-05", type="Story", points=5, priority="P0", sprint="S3",
         component="Ingestion", labels=["upload", "security"], depends=["LS-015"],
         summary="Secure file upload with type, size and magic-byte validation",
         narrative="As a security reviewer, I want uploads validated by content rather than "
                   "filename, so that a renamed executable cannot enter the system.",
         ac=["Accepts xlsx, xls, csv, pdf and common image formats; everything else is rejected with a clear error.",
             "Content type verified by magic bytes, not by extension or client-supplied header.",
             "Size cap enforced and configurable; oversize uploads fail before buffering the whole file.",
             "XML parsers are configured XXE-safe; a malicious xlsx fixture is covered by a regression test."]),
    dict(key="LS-051", epic="EPIC-05", type="Story", points=3, priority="P0", sprint="S3",
         component="Ingestion", labels=["storage"], depends=["LS-050", "LS-020"],
         summary="Immutable object storage client with tenant-prefixed keys",
         narrative="As a customer, I want my original files preserved and isolated, so that "
                   "provenance survives and no other tenant can reach them.",
         ac=["Pluggable StorageClient port with S3-compatible and local implementations.",
             "Object keys are prefixed by tenant and plant; cross-tenant key construction is impossible by design.",
             "Stored objects are never mutated; re-processing reads the original bytes.",
             "Download is served through a short-lived signed URL, never a public bucket."]),
    dict(key="LS-052", epic="EPIC-05", type="Story", points=5, priority="P0", sprint="S3",
         component="Ingestion", labels=["parsing"], depends=["LS-051"],
         summary="XLSX and CSV parsers producing verbatim raw records",
         narrative="As the system, I need every source row captured exactly as written, so "
                   "that normalization can never destroy the evidence.",
         ac=["Multi-sheet workbooks parsed with sheet name and row number retained per raw record.",
             "Merged cells, blank rows and inconsistent column counts handled without aborting the file.",
             "Cell values stored as original text; no type coercion at the raw layer.",
             "Parser is streaming so a 100,000-row workbook does not exhaust heap."]),
    dict(key="LS-053", epic="EPIC-05", type="Story", points=5, priority="P1", sprint="S4",
         component="Ingestion", labels=["parsing"], depends=["LS-052"],
         summary="PDF text extraction parser",
         narrative="As a plant whose history is in PDF reports, I want those ingested too, "
                   "so that I do not have to retype three years of records.",
         ac=["Text-layer PDFs extracted with page number retained per raw record.",
             "Tabular layouts detected and split into rows where structure permits.",
             "PDFs with no text layer are routed to the OCR path rather than failing.",
             "Page-level provenance is exposed through View Source."]),
    dict(key="LS-054", epic="EPIC-05", type="Story", points=8, priority="P1", sprint="S4",
         component="Ingestion", labels=["parsing", "ocr"], depends=["LS-053"],
         summary="Scanned-register OCR parser",
         narrative="As a plant with handwritten logbooks, I want scans converted to records, "
                   "so that the pre-digital years are searchable too.",
         ac=["Pluggable OCR provider port with at least one working implementation.",
             "Per-block OCR confidence retained and fed into overall extraction confidence.",
             "Low-confidence OCR output is routed to validation rather than auto-approved, regardless of extraction confidence.",
             "Original image is retained and shown side-by-side in the validation workbench."]),
    dict(key="LS-055", epic="EPIC-05", type="Story", points=8, priority="P0", sprint="S4",
         component="Ingestion", labels=["pipeline"], depends=["LS-052", "LS-015"],
         summary="Import job state machine with resume, cancel and retry",
         narrative="As an engineer importing 2,000 rows, I want the run to survive failures, "
                   "so that one bad row or a provider timeout does not cost me the whole file.",
         ac=["States CREATED, PARSED, MAPPED, NORMALIZING, RESOLVED, COMPLETED, CANCELLED, FAILED with legal transitions enforced.",
             "Cancel stops further processing without rolling back rows already committed, and the state is clearly reported.",
             "Retry resumes from the last completed stage rather than restarting the file.",
             "An LLM provider outage pauses at NORMALIZING and resumes cleanly when the provider returns."]),
    dict(key="LS-056", epic="EPIC-05", type="Story", points=5, priority="P0", sprint="S4",
         component="Ingestion", labels=["data-quality"], depends=["LS-052"],
         summary="Duplicate file and duplicate row detection",
         narrative="As a maintenance manager, I want re-uploads to be caught, so that my "
                   "downtime totals are not silently doubled.",
         ac=["File-level duplicate detected by content hash and returns 409 with a link to the earlier import.",
             "Row-level near-duplicate detection across imports flags candidates rather than auto-deleting.",
             "Flagged duplicates surface in the validation queue for a human decision.",
             "Deliberate re-import is possible through an explicit override that is audited."]),
    dict(key="LS-057", epic="EPIC-05", type="Story", points=3, priority="P0", sprint="S4",
         component="Ingestion", labels=["ux"], depends=["LS-052"],
         summary="Import preview API",
         narrative="As an engineer, I want to see what was detected before committing, so "
                   "that I catch a wrong sheet before spending twenty minutes.",
         ac=["Returns detected sheets, inferred header row, column names and the first N rows.",
             "Preview runs without persisting raw records or consuming AI tokens.",
             "Detected encoding and delimiter are reported for CSV files.",
             "Preview response is fast enough to feel instant on a typical customer file."]),
    dict(key="LS-058", epic="EPIC-05", type="Story", points=3, priority="P0", sprint="S4",
         component="Ingestion", labels=["data-quality", "trust"], depends=["LS-055"],
         summary="Skipped-row registry with reasons and export",
         narrative="As a maintenance manager, I want to know exactly what was not imported "
                   "and why, so that I can trust the totals I am shown.",
         ac=["Every skipped row is retained with a machine-readable reason code and human-readable explanation.",
             "Import summary reports detected, usable, skipped and needs-review counts that reconcile to the total.",
             "Skipped rows are exportable as CSV for the customer to review offline.",
             "Skipped rows can be reprocessed after the underlying cause is fixed."]),
]

# --------------------------------------------------------------------------------------
# EPIC-06 — Generative Extraction & Normalisation
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-060", epic="EPIC-06", type="Story", points=5, priority="P0", sprint="S4",
         component="AI", labels=["llm", "platform"], depends=["LS-010"],
         summary="Pluggable LlmClient port with retries, timeouts and a circuit breaker",
         narrative="As an engineer, I want the model provider behind a port, so that an "
                   "outage degrades the product instead of breaking it.",
         ac=["LlmClient interface with an Anthropic adapter as the default implementation.",
             "Configurable timeout, exponential-backoff retry and a circuit breaker with a half-open probe.",
             "Token usage, latency, model and cost are recorded for every call.",
             "A deterministic fake implementation backs tests so CI never calls a live provider."]),
    dict(key="LS-061", epic="EPIC-06", type="Story", points=8, priority="P0", sprint="S4",
         component="AI", labels=["llm", "extraction"], depends=["LS-060", "LS-052"],
         summary="Schema-constrained extraction with per-field confidence",
         narrative="As the system, I need messy shorthand turned into structured fields with "
                   "honest confidence, so that routing to review is based on real signal.",
         ac=["Extraction returns a strict JSON schema: date, machineText, failureMode, action, parts, downtimeHours, technician, kind.",
             "Every field carries its own confidence score; the model is instructed to return null rather than guess.",
             "Failure mode and part values are constrained to the plant's taxonomy where a confident match exists.",
             "Schema violations are rejected and retried once before the row is marked FAILED.",
             "Golden-set extraction F1 meets the threshold defined in LS-140."]),
    dict(key="LS-062", epic="EPIC-06", type="Story", points=5, priority="P0", sprint="S4",
         component="AI", labels=["llm", "cost"], depends=["LS-061"],
         summary="Batched extraction with prompt caching on the static prefix",
         narrative="As the business, I want extraction cost per 1,000 rows to be predictable "
                   "and low, so that unit economics survive a large historical import.",
         ac=["Rows batched at a configurable size (default approximately 20) per model call.",
             "The static prefix — schema, shorthand dictionary and plant context — is prompt-cached.",
             "Measured cost per 1,000 rows is recorded and reported per import.",
             "A partial batch failure retries only the failed rows, never the whole batch."]),
    dict(key="LS-063", epic="EPIC-06", type="Story", points=5, priority="P0", sprint="S4",
         component="AI", labels=["hinglish", "moat"], depends=["LS-061"],
         summary="Hinglish and shorthand dictionary shared by extraction and search",
         narrative="As a technician writing 'brng' and '2 ghante', I want the system to "
                   "understand me, so that my notes are as valuable as a typed report.",
         ac=["Dictionary covers shorthand (brng, m/c, algnmnt), Hinglish units ('2 ghante'), and Devanagari and Marathi equivalents.",
             "The same dictionary is applied at extraction time and at search-expansion time so behaviour matches.",
             "Per-plant entries can be added without a code deployment.",
             "New entries are versioned and their effect is measurable on the extraction golden set."]),
    dict(key="LS-064", epic="EPIC-06", type="Story", points=5, priority="P0", sprint="S5",
         component="AI", labels=["confidence", "routing"], depends=["LS-061", "LS-070"],
         summary="Confidence calibration and per-plant auto-approval routing",
         narrative="As a maintenance manager, I want only genuinely uncertain rows in my "
                   "review queue, so that validation is worth my engineers' time.",
         ac=["Overall confidence combines model self-score, resolver score and field completeness by a documented formula.",
             "Rows at or above the plant threshold auto-approve; the rest create validation items.",
             "Calibration is measured against the golden set: reported confidence tracks observed accuracy.",
             "Auto-approval rate is recorded per import and per plant as a first-class product metric."]),
    dict(key="LS-065", epic="EPIC-06", type="Story", points=8, priority="P1", sprint="S7",
         component="AI", labels=["agent", "intake"], depends=["LS-057", "LS-061", "LS-190"],
         summary="Intake Agent: file profiling and column-mapping proposal",
         narrative="As an engineer, I want the system to check the mapping before processing "
                   "2,000 rows, so that a wrong column does not waste twenty minutes and real money.",
         ac=["Agent profiles headers, data types, null density, sample values and merged-cell structure.",
             "Proposes a column mapping with per-column confidence and a plain-language rationale.",
             "Sample-extracts a stratified sample of roughly 25 rows and self-scores fill rate, resolver hit rate and date parse rate.",
             "If projected auto-approval falls below the plant threshold, the run stops and raises a mapping proposal citing the specific evidence.",
             "The engineer can accept, edit or override the proposal; the decision is audited."]),
    dict(key="LS-066", epic="EPIC-06", type="Story", points=5, priority="P1", sprint="S5",
         component="AI", labels=["agent", "quality"], depends=["LS-064"],
         summary="Extraction self-critique pass on mid-confidence rows",
         narrative="As a reviewer, I want the queue to contain sharper questions, so that I "
                   "spend my time on genuine ambiguity rather than on obvious rows.",
         ac=["Rows in the configurable mid-confidence band get a second pass that re-reads raw text against the extraction.",
             "The pass either raises confidence with a stated justification or names the specific ambiguous field.",
             "Reviewer-facing output shows which field is uncertain and why.",
             "Measured effect on reviewer time and on false auto-approvals is reported; the feature is reverted if accuracy drops."]),
    dict(key="LS-067", epic="EPIC-06", type="Story", points=3, priority="P0", sprint="S5",
         component="AI", labels=["reliability"], depends=["LS-061", "LS-055"],
         summary="Extraction failure handling, dead-letter and retry API",
         narrative="As an engineer, I want failed rows visible and retryable, so that a "
                   "transient provider error does not silently lose data.",
         ac=["Rows failing twice are marked FAILED with the error reason retained.",
             "Failed rows are listable per import and retryable individually or in bulk.",
             "Retry reuses the original raw text; the raw record is never re-parsed or altered.",
             "Persistent failure rate is a monitored metric with an alert threshold."]),
]

# --------------------------------------------------------------------------------------
# EPIC-07 — Entity Resolution & Alias Learning
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-070", epic="EPIC-07", type="Story", points=8, priority="P0", sprint="S4",
         component="AI", labels=["resolution", "moat"], depends=["LS-032"],
         summary="MachineResolverService cascade: exact, alias, fuzzy, semantic",
         narrative="As the system, I need 'Conv Motor-3' to become a real asset id, so that "
                   "messy text becomes analysable data.",
         ac=["Four-stage cascade: exact match, known alias, normalised-token fuzzy match, embedding similarity.",
             "Each stage returns candidates with calibrated confidence; the cascade stops at a confident match.",
             "The identical resolver is used by ingestion, search and the assistant — one code path, no divergence.",
             "Resolution is plant-scoped: a machine in another tenant is never a candidate.",
             "Precision@1 on the golden set meets the threshold in LS-141."]),
    dict(key="LS-071", epic="EPIC-07", type="Story", points=3, priority="P0", sprint="S4",
         component="AI", labels=["resolution"], depends=["LS-070"],
         summary="Machine alias store with provenance and confidence",
         narrative="As the system, I want learned aliases persisted with their origin, so "
                   "that a bad alias can be traced and reversed.",
         ac=["Alias records text, machine, confidence, source (IMPORT, VALIDATION, MANUAL) and creating actor.",
             "Alias text is unique per plant; a conflicting alias returns 409 with the existing mapping.",
             "Aliases are listable, editable and deletable by a plant admin, with every change audited.",
             "Deleting an alias does not alter records already resolved through it."]),
    dict(key="LS-072", epic="EPIC-07", type="Story", points=5, priority="P0", sprint="S5",
         component="AI", labels=["resolution", "learning"], depends=["LS-071", "LS-082"],
         summary="Alias learning from validation corrections",
         narrative="As a reviewer, I want my correction to teach the system permanently, so "
                   "that I never answer the same question twice.",
         ac=["Correcting a machine during validation creates or strengthens an alias automatically.",
             "The learned alias applies immediately to subsequent resolution without a restart.",
             "Learning is attributable: the alias records which validation action produced it.",
             "Measured effect: resolver hit rate on the next import of the same customer's data improves."]),
    dict(key="LS-073", epic="EPIC-07", type="Story", points=5, priority="P0", sprint="S5",
         component="AI", labels=["resolution", "learning"], depends=["LS-072", "LS-045"],
         summary="Re-resolution of pending rows when an alias is created",
         narrative="As a reviewer, I want one mapping to clear every matching row everywhere, "
                   "so that the queue shrinks faster than I work.",
         ac=["Creating an alias publishes an event that re-resolves matching unresolved rows across all pending imports.",
             "Re-resolution is asynchronous, idempotent and reports how many rows it cleared.",
             "Already-approved records are not retroactively altered without an explicit, audited action.",
             "Re-resolution respects plant scope and never crosses tenants."]),
    dict(key="LS-074", epic="EPIC-07", type="Story", points=5, priority="P1", sprint="S5",
         component="AI", labels=["resolution", "parts"], depends=["LS-034", "LS-033"],
         summary="Part and failure-mode resolution with synonym learning",
         narrative="As an analyst, I want '6205ZZ', '6205 ZZ' and 'bearing 6205' treated as "
                   "one part, so that consumption analysis is not fragmented.",
         ac=["Part resolution uses code normalisation, synonyms and fuzzy matching with confidence.",
             "Failure-mode resolution maps free text to the canonical taxonomy entry.",
             "Corrections during validation create synonyms, mirroring machine alias learning.",
             "Unresolvable parts are retained as free text on the record and reported, never silently dropped."]),
    dict(key="LS-075", epic="EPIC-07", type="Story", points=3, priority="P1", sprint="S5",
         component="AI", labels=["resolution", "devex"], depends=["LS-070"],
         summary="Resolver explain endpoint",
         narrative="As an engineer debugging a bad mapping, I want to see why the resolver "
                   "chose what it chose, so that I can fix the cause rather than the symptom.",
         ac=["Endpoint accepts free text and returns ranked candidates with per-stage scores.",
             "Response names which cascade stage produced each candidate.",
             "Restricted to ENGINEER and above; results are plant-scoped.",
             "Used by the support runbook for resolution complaints."]),
    dict(key="LS-076", epic="EPIC-07", type="Story", points=5, priority="P1", sprint="S9",
         component="AI", labels=["agent", "resolution"], depends=["LS-070", "LS-083", "LS-190"],
         summary="Resolver Agent clarifying-question flow for ambiguous clusters",
         narrative="As a reviewer, I want one well-framed question to unblock dozens of rows, "
                   "so that validation is a conversation rather than data entry.",
         ac=["Agent clusters mutually similar unresolved texts and detects genuine ambiguity between close candidates.",
             "Raises a single proposal per cluster showing the affected row count, the candidates and their scores.",
             "One decision maps the whole cluster, writes the alias and triggers re-resolution.",
             "Agent asks at most a configured number of questions per import so it never becomes a quiz."]),
]

# --------------------------------------------------------------------------------------
# EPIC-08 — Human-in-the-Loop Validation Workbench
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-080", epic="EPIC-08", type="Story", points=5, priority="P0", sprint="S5",
         component="Product", labels=["validation"], depends=["LS-064"],
         summary="Validation item model and queue API",
         narrative="As a reviewer, I want a prioritised queue of uncertain rows, so that I "
                   "work through the highest-impact ambiguity first.",
         ac=["validation_items created for every row below the plant confidence threshold.",
             "Queue filterable by import, machine, uncertainty type and age; sortable by impact.",
             "Each item exposes the raw text, the extraction, the per-field confidence and the resolver candidates.",
             "Items carry status OPEN or RESOLVED with the resolving action recorded."]),
    dict(key="LS-081", epic="EPIC-08", type="Story", points=3, priority="P0", sprint="S5",
         component="Product", labels=["validation", "api"], depends=["LS-080"],
         summary="Side-by-side raw-versus-extracted review payload",
         narrative="As a reviewer, I want the original text next to the extraction, so that "
                   "I can judge correctness in seconds without leaving the screen.",
         ac=["Payload returns verbatim raw text, the source file, sheet and row, and each extracted field.",
             "Fields below the confidence threshold are explicitly flagged for attention.",
             "For OCR-sourced rows, the original image region is returned alongside the text.",
             "The payload is sufficient to render the review screen without any follow-up request."]),
    dict(key="LS-082", epic="EPIC-08", type="Story", points=5, priority="P0", sprint="S5",
         component="Product", labels=["validation"], depends=["LS-081"],
         summary="Approve, edit-and-approve and reject with conflict handling",
         narrative="As a reviewer, I want to act on an item safely while colleagues work the "
                   "same queue, so that two people never silently overwrite each other.",
         ac=["Three actions supported: approve as-is, edit then approve, and reject with a reason.",
             "Optimistic locking returns 409 when another reviewer already resolved the item.",
             "Approval creates the maintenance record with full provenance; rejection excludes the row from index and statistics.",
             "Every action writes a validation_actions audit row naming the reviewer."]),
    dict(key="LS-083", epic="EPIC-08", type="Story", points=8, priority="P0", sprint="S5",
         component="Product", labels=["validation", "differentiator"], depends=["LS-082", "LS-073"],
         summary="Alias-group bulk mapping",
         narrative="As a reviewer facing 37 rows that all say 'Conv Motor-3', I want to map "
                   "them in one action, so that validation takes minutes rather than hours.",
         ac=["Unresolved machine texts are grouped and the affected row count is shown per group.",
             "One mapping action resolves every row in the group, creates the alias and triggers re-resolution elsewhere.",
             "A preview shows exactly which rows will be affected before the action is committed.",
             "The whole operation is transactional and produces a single audited action with the row count.",
             "Demonstrated on a group of at least 30 records as part of the pilot acceptance run."]),
    dict(key="LS-084", epic="EPIC-08", type="Story", points=5, priority="P1", sprint="S6",
         component="Product", labels=["validation"], depends=["LS-082"],
         summary="Bulk actions with partial-success reporting",
         narrative="As a reviewer, I want to approve a filtered set at once and see exactly "
                   "what failed, so that bulk work is safe rather than reckless.",
         ac=["Bulk approve and bulk reject operate over a selection or a filter.",
             "The response reports per-item success or failure with reasons; one failure never aborts the batch.",
             "Bulk operations are capped at a configured size and run asynchronously above a threshold, reporting progress.",
             "Each affected item still produces its own audit row."]),
    dict(key="LS-085", epic="EPIC-08", type="Story", points=3, priority="P0", sprint="S6",
         component="Product", labels=["validation", "audit"], depends=["LS-082"],
         summary="Validation action audit trail",
         narrative="As a plant admin, I want to see who approved what, so that data quality "
                   "questions have a definitive answer.",
         ac=["Every validation action records actor, timestamp, before and after values, and reason where applicable.",
             "The trail is queryable by reviewer, date range and import.",
             "Audit rows are append-only and immutable.",
             "A record's detail view can show the validation decision that created it."]),
    dict(key="LS-086", epic="EPIC-08", type="Story", points=3, priority="P1", sprint="S6",
         component="Product", labels=["validation", "metrics"], depends=["LS-085"],
         summary="Queue burn-down and reviewer-throughput metrics",
         narrative="As a maintenance manager, I want to see how fast the queue is clearing, "
                   "so that I know whether validation is a one-week task or a permanent tax.",
         ac=["Metrics for queue depth over time, items resolved per reviewer-hour and median time-to-resolution.",
             "Corrections per 100 records tracked as a data-quality indicator.",
             "Metrics are exposed per plant and feed the pilot scorecard from LS-008.",
             "Available through the API for the dashboard and for the per-tenant scorecard in LS-147."]),
    dict(key="LS-087", epic="EPIC-08", type="Story", points=3, priority="P2", sprint="S6",
         component="Product", labels=["validation", "ux"], depends=["LS-082"],
         summary="Keyboard-first reviewer workflow",
         narrative="As a reviewer clearing 200 items, I want to work without the mouse, so "
                   "that the queue takes twenty minutes instead of two hours.",
         ac=["Keyboard shortcuts for approve, reject, edit, next and previous.",
             "Focus advances automatically to the next item after an action.",
             "An undo window allows reversing the last action without reopening the item.",
             "Shortcuts are discoverable through an in-app help overlay."]),
]

# --------------------------------------------------------------------------------------
# EPIC-09 — Hybrid Search & Retrieval
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-090", epic="EPIC-09", type="Story", points=5, priority="P0", sprint="S6",
         component="AI", labels=["search"], depends=["LS-040"],
         summary="Full-text and trigram indexes over record text",
         narrative="As an engineer, I want fast keyword search over every record, so that "
                   "finding a past failure takes seconds.",
         ac=["PostgreSQL tsvector column maintained on insert and update, with a GIN index.",
             "pg_trgm indexes support typo-tolerant matching on machine and part text.",
             "Search is plant-scoped at the query level and verified by the cross-tenant suite.",
             "Query latency stays within budget on a one-million-record corpus."]),
    dict(key="LS-091", epic="EPIC-09", type="Story", points=5, priority="P0", sprint="S6",
         component="AI", labels=["search", "embeddings"], depends=["LS-090", "LS-060"],
         summary="Embedding client port and record embedding backfill job",
         narrative="As the system, I need semantic vectors for every record, so that "
                   "meaning-based retrieval works across languages.",
         ac=["Pluggable EmbeddingClient port; the model name and dimension are recorded per row.",
             "pgvector column with an appropriate index; dimension mismatches are rejected at write time.",
             "An idempotent, resumable backfill job embeds existing records and reports progress.",
             "New and corrected records are embedded automatically via domain events."]),
    dict(key="LS-092", epic="EPIC-09", type="Story", points=8, priority="P0", sprint="S6",
         component="AI", labels=["search"], depends=["LS-090", "LS-091"],
         summary="Hybrid retrieval with reciprocal-rank fusion",
         narrative="As an engineer, I want the best of keyword and semantic search, so that "
                   "both exact part codes and vague descriptions find the right records.",
         ac=["Full-text, trigram and vector result sets are fused by reciprocal rank fusion with documented weights.",
             "Filters for machine, line, date range, failure mode and part apply before fusion.",
             "Result count k is clamped server-side regardless of the requested value.",
             "nDCG@10 on the golden query set meets the threshold in LS-142."]),
    dict(key="LS-093", epic="EPIC-09", type="Story", points=5, priority="P0", sprint="S6",
         component="AI", labels=["search", "hinglish"], depends=["LS-092", "LS-063"],
         summary="Query expansion using the shorthand dictionary",
         narrative="As a technician searching 'brng gaya', I want bearing records, so that "
                   "I do not have to know the formal term.",
         ac=["Queries are expanded with shorthand, Hinglish, Hindi and Marathi equivalents before matching.",
             "The same dictionary used at extraction time is used here, so behaviour is consistent.",
             "Expansion is bounded so that a short query does not explode into an unselective one.",
             "Benchmark queries such as brng, BRG, bearng and 'bearing gaya' all retrieve the same core result set."]),
    dict(key="LS-094", epic="EPIC-09", type="Story", points=3, priority="P1", sprint="S6",
         component="AI", labels=["search", "trust"], depends=["LS-092"],
         summary="Why-this-matched explanation payload",
         narrative="As an engineer, I want to know why a result appeared, so that I trust "
                   "the search rather than second-guessing it.",
         ac=["Each result carries a why array naming the matched terms, expansions and retrieval strategies.",
             "Matched spans are identified so the UI can highlight them.",
             "Semantic-only matches are labelled as such and distinguished from keyword hits.",
             "The explanation is part of the API contract and covered by tests."]),
    dict(key="LS-095", epic="EPIC-09", type="Story", points=3, priority="P0", sprint="S6",
         component="AI", labels=["search", "reliability"], depends=["LS-092"],
         summary="Degraded search mode when the embedding provider is unavailable",
         narrative="As a user, I want search to keep working during a provider outage, so "
                   "that the product never goes fully dark.",
         ac=["Embedding failure falls back to full-text plus trigram retrieval automatically.",
             "The response indicates degraded mode so the UI can show an honest notice.",
             "Newly created records queue for embedding and are backfilled when the provider returns.",
             "Verified by a staging test that disables the embedding provider."]),
    dict(key="LS-096", epic="EPIC-09", type="Story", points=5, priority="P0", sprint="S6",
         component="AI", labels=["search", "quality"], depends=["LS-092", "LS-142"],
         summary="Retrieval quality benchmark wired into CI",
         narrative="As an engineer changing retrieval weights, I want immediate feedback, so "
                   "that a tuning change cannot silently make search worse.",
         ac=["Benchmark runs the golden query set and reports nDCG@10, recall@20 and MRR.",
             "Results are compared against the stored baseline; a regression beyond tolerance fails the build.",
             "The report names which queries regressed and by how much.",
             "Fusion weights are configuration, not hard-coded constants, so tuning does not require a release."]),
]

# --------------------------------------------------------------------------------------
# EPIC-10 — Deterministic Analytics & KPI Engine
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-100", epic="EPIC-10", type="Story", points=5, priority="P0", sprint="S6",
         component="Domain", labels=["analytics", "trust"], depends=["LS-042"],
         summary="Downtime, breakdown-count and record-count aggregates",
         narrative="As a maintenance manager, I want reliable totals, so that the number in "
                   "a chat answer and the number on the dashboard are always the same.",
         ac=["Aggregates computed in SQL, filterable by plant, line, machine, failure mode, part and date range.",
             "Records with null downtime are excluded from sums and counted in coverage, never treated as zero.",
             "The same service backs the dashboard, the API and the assistant tools — one implementation only.",
             "Results are deterministic: identical inputs produce identical outputs across runs."]),
    dict(key="LS-101", epic="EPIC-10", type="Story", points=5, priority="P0", sprint="S6",
         component="Domain", labels=["analytics", "kpi"], depends=["LS-100"],
         summary="MTTR, MTBF and availability calculators with documented formulas",
         narrative="As a reliability engineer, I want standard KPIs computed the way I would "
                   "compute them, so that I can defend the numbers to my plant head.",
         ac=["MTTR, MTBF and availability implemented with the exact formula and assumptions documented in-code and in user-facing help.",
             "Operating hours come from plant settings, not from a hard-coded constant.",
             "Insufficient data returns an explicit unavailable result rather than a misleading zero.",
             "Unit tests assert exact expected values against the reference fixture."]),
    dict(key="LS-102", epic="EPIC-10", type="Story", points=5, priority="P0", sprint="S7",
         component="Domain", labels=["analytics"], depends=["LS-100"],
         summary="Failure Pareto and trend series",
         narrative="As a maintenance manager, I want to see which failures dominate and "
                   "whether they are getting better, so that I know where to spend money.",
         ac=["Pareto by failure mode with count, downtime and cumulative percentage.",
             "Trend series bucketable by week, month and quarter with explicit handling of empty buckets.",
             "Scopable to plant, line or machine.",
             "Coverage is reported alongside every series so sparse data is visible, not hidden."]),
    dict(key="LS-103", epic="EPIC-10", type="Story", points=3, priority="P0", sprint="S7",
         component="Domain", labels=["analytics"], depends=["LS-100"],
         summary="Top machines and top lines ranking",
         narrative="As a plant head, I want to know my worst assets by a chosen metric, so "
                   "that improvement effort goes where the downtime actually is.",
         ac=["Ranking by downtime, breakdown count or MTTR, with configurable k.",
             "Ties broken deterministically so repeated calls return a stable order.",
             "Each entry carries the underlying counts so the ranking is auditable.",
             "Exposed as an assistant tool with server-side argument clamping."]),
    dict(key="LS-104", epic="EPIC-10", type="Story", points=5, priority="P0", sprint="S7",
         component="Domain", labels=["analytics", "parts"], depends=["LS-100", "LS-074"],
         summary="Part usage, share and replacement-interval statistics",
         narrative="As a maintenance manager, I want to see where a part is being consumed, "
                   "so that a concentration on one line becomes visible.",
         ac=["Per-part usage count, machine distribution, percentage share and mean replacement interval.",
             "Scopable by date range, line and machine.",
             "Answers the benchmark question about where a given bearing has been used, with the expected machine distribution.",
             "Backs both the parts screen and the assistant part_usage tool."]),
    dict(key="LS-105", epic="EPIC-10", type="Story", points=3, priority="P0", sprint="S7",
         component="Domain", labels=["analytics", "trust"], depends=["LS-100"],
         summary="Coverage reporting on every statistic",
         narrative="As an engineer, I want to know how much of the data a number is based "
                   "on, so that I do not over-trust a statistic drawn from three records.",
         ac=["Every aggregate returns a coverage object: records considered, records with a valid value, and the percentage.",
             "Coverage is rendered in assistant CALCULATED blocks, for example '7 records, 7/7 valid downtime'.",
             "Statistics below a configured coverage floor are labelled low-confidence in the response.",
             "Coverage is part of the API contract and is covered by tests."]),
    dict(key="LS-106", epic="EPIC-10", type="Story", points=5, priority="P0", sprint="S7",
         component="Domain", labels=["analytics", "performance"], depends=["LS-101", "LS-102"],
         summary="Dashboard composite endpoint with caching and invalidation",
         narrative="As a maintenance manager, I want the dashboard to load quickly, so that "
                   "I actually open it every morning.",
         ac=["One composite endpoint returns KPIs, trend, Pareto, top machines and open counts.",
             "Results cached per plant with event-driven invalidation on record create, update and delete.",
             "Cache is in-process; no Redis is introduced, per the documented scope decision.",
             "Dashboard reproduces the reference fixture's expected numbers exactly."]),
]

# --------------------------------------------------------------------------------------
# EPIC-11 — Agent Runtime & Tool Platform
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-110", epic="EPIC-11", type="Story", points=8, priority="P0", sprint="S7",
         component="AI-Platform", labels=["agent", "core"], depends=["LS-012", "LS-060"],
         summary="AgentRun and AgentStep persistence with a replayable trace schema",
         narrative="As an engineer and as a customer, I want every agent run recorded step "
                   "by step, so that 'why did it say that?' always has an answer.",
         ac=["AgentRun stores tenant, plant, agent type, trigger, input, policy snapshot, status and totals.",
             "AgentStep is append-only and ordered, capturing type, tool name, arguments, result, model, tokens, latency, cost and errors.",
             "Large tool results are stored by reference rather than inline to bound row size.",
             "Steps cannot be modified or deleted; enforced at the database role level.",
             "A completed run's trace is retrievable in full through one API call."]),
    dict(key="LS-111", epic="EPIC-11", type="Story", points=8, priority="P0", sprint="S7",
         component="AI-Platform", labels=["agent", "core"], depends=["LS-110", "LS-112"],
         summary="Plan, act, observe, critique loop executor",
         narrative="As the system, I need a controlled agent loop, so that multi-step "
                   "investigation is possible without unbounded cost or runaway behaviour.",
         ac=["Executor drives plan, tool call, observe and critique steps until an answer is ready or the budget is exhausted.",
             "Tool results are summarised before re-entering context; full results go only to the trace.",
             "The critique step is capped so the agent cannot loop indefinitely on self-doubt.",
             "An invalid plan is rejected before execution and triggers at most one replan.",
             "Every step is persisted as it happens, so a crashed run still has a partial trace."]),
    dict(key="LS-112", epic="EPIC-11", type="Story", points=5, priority="P0", sprint="S7",
         component="AI-Platform", labels=["agent", "tools"], depends=["LS-110"],
         summary="Typed tool registry with JSON schemas and argument validation",
         narrative="As a security reviewer, I want the model's tool access constrained by "
                   "code, so that a bad plan or an injection cannot reach anything unlisted.",
         ac=["Each tool declares a name, argument JSON schema, allowed roles, access class and result limits.",
             "Arguments are validated against the schema before execution; a violation is a step error, never a call.",
             "No tool executes free-form SQL, and an ArchUnit rule enforces it.",
             "Access class is READ or PROPOSE only; a DIRECT_WRITE tool fails a registry unit test."]),
    dict(key="LS-113", epic="EPIC-11", type="Story", points=5, priority="P0", sprint="S7",
         component="AI-Platform", labels=["agent", "security"], depends=["LS-112", "LS-024"],
         summary="Tool scoping by tenant, plant and role",
         narrative="As a customer, I want an agent to be able to reach only what the "
                   "requesting user can reach, so that agency never becomes privilege escalation.",
         ac=["Every tool execution carries the caller's tenant, plant and role, applied at the repository layer.",
             "A tool call naming an out-of-scope plant returns 404 and raises a security event.",
             "An agent invoked by a VIEWER cannot reach PROPOSE-class tools.",
             "Covered by the cross-tenant test suite from LS-021."]),
    dict(key="LS-114", epic="EPIC-11", type="Story", points=5, priority="P0", sprint="S7",
         component="AI-Platform", labels=["agent", "cost"], depends=["LS-111"],
         summary="Run budgets for steps, tokens, cost and wall-clock time",
         narrative="As the business, I want a hard ceiling on every agent run, so that one "
                   "pathological question cannot cost a day's margin.",
         ac=["Budget covers maximum steps, tokens, cost in INR and a wall-clock deadline, defaulted per agent type.",
             "Budgets are overridable per tenant and captured in the run's policy snapshot.",
             "Exceeding a limit ends the run as BUDGET_EXCEEDED and returns a partial, clearly labelled answer.",
             "Budget exhaustion emits a metric and is visible in the trace; it is never a silent truncation."]),
    dict(key="LS-115", epic="EPIC-11", type="Story", points=5, priority="P0", sprint="S7",
         component="AI-Platform", labels=["agent", "cost", "llm"], depends=["LS-060"],
         summary="Model router with task tiers and a fallback chain",
         narrative="As the business, I want each task on the cheapest model that does it "
                   "well, so that quality and cost are both deliberate choices.",
         ac=["Three tiers — fast, balanced and deep — mapped to task types by configuration, not by hard-coded model ids.",
             "A fallback chain handles provider overload or unavailability without failing the run.",
             "The model actually used is recorded per step for cost attribution and debugging.",
             "Tier assignment is changeable per tenant, for example capping the deep tier for a small plant."]),
    dict(key="LS-116", epic="EPIC-11", type="Story", points=8, priority="P1", sprint="S9",
         component="AI-Platform", labels=["agent", "memory", "moat"], depends=["LS-111", "LS-071"],
         summary="Three-tier agent memory: working, semantic and episodic",
         narrative="As a user, I want the agent to remember what matters, so that follow-up "
                   "questions work and it does not re-raise something I already dismissed.",
         ac=["Working memory carries resolved entities and intents across turns, never raw transcripts.",
             "Semantic memory exposes aliases, dictionaries, confirmed patterns and taxonomy to every agent.",
             "Episodic memory makes past runs, briefings and dismissed patterns retrievable.",
             "A follow-up such as 'and this year?' resolves against the previously resolved machine.",
             "A dismissed pattern is not re-raised within its cooling-off window."]),
    dict(key="LS-117", epic="EPIC-11", type="Story", points=5, priority="P0", sprint="S8",
         component="AI-Platform", labels=["agent", "governance"], depends=["LS-114", "LS-190"],
         summary="Per-tenant agent policy and autonomy level",
         narrative="As a plant IT head, I want to control what agents may do in my tenant, "
                   "so that I can start conservative and expand as trust grows.",
         ac=["Policy sets, per tenant and agent: enabled state, autonomy level L0 to L3, budgets and model tier.",
             "L4 (external system writes) is not representable in the model at all.",
             "The active policy is snapshotted into every run for retrospective auditability.",
             "Policy changes are audited and take effect without a deployment."]),
    dict(key="LS-118", epic="EPIC-11", type="Story", points=5, priority="P1", sprint="S9",
         component="AI-Platform", labels=["agent", "trust"], depends=["LS-110"],
         summary="Agent trace viewer API",
         narrative="As an engineer or a customer, I want to walk through an agent's "
                   "reasoning, so that the Glass Box claim is literally true.",
         ac=["Endpoint returns the ordered steps with tool arguments, results, timings and costs.",
             "Sensitive values are redacted according to the logging policy.",
             "Access is restricted to the run's tenant and to ENGINEER and above.",
             "The payload is sufficient to render the trace viewer UI in LS-247 without extra calls."]),
    dict(key="LS-119", epic="EPIC-11", type="Story", points=5, priority="P1", sprint="S9",
         component="AI-Platform", labels=["agent", "testing"], depends=["LS-110", "LS-111"],
         summary="Deterministic replay of a run against recorded tool outputs",
         narrative="As an engineer debugging a bad answer, I want to re-run it against the "
                   "exact same data, so that I can fix the prompt without chasing a moving target.",
         ac=["A stored run can be replayed with its recorded tool outputs substituted for live calls.",
             "Replay produces a comparable trace and highlights where behaviour diverged.",
             "Replays are marked as such and never create proposals or mutate state.",
             "Used as the reproduction mechanism in the AI incident runbook."]),
]

# --------------------------------------------------------------------------------------
# EPIC-12 — Reliability Copilot
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-120", epic="EPIC-12", type="Story", points=5, priority="P0", sprint="S8",
         component="AI", labels=["assistant"], depends=["LS-060", "LS-070"],
         summary="Query understanding: intent and entity extraction over a closed taxonomy",
         narrative="As a user asking in Hinglish, I want my question understood correctly, "
                   "so that the right tools run against the right machine and date range.",
         ac=["Intent classified into the closed set including ROOT_CAUSE_INVESTIGATION and OUT_OF_SCOPE.",
             "Entities extracted: machine text, part, failure mode, line, date range and language.",
             "Relative dates such as 'pichle 2 saal' and 'is saal' resolve against the plant's timezone.",
             "Output is JSON-schema constrained; an unparseable result triggers one retry then a clarifying question.",
             "Out-of-scope questions produce a polite refusal that lists actual capabilities."]),
    dict(key="LS-121", epic="EPIC-12", type="Story", points=8, priority="P0", sprint="S8",
         component="AI", labels=["assistant", "tools"], depends=["LS-112", "LS-100", "LS-092"],
         summary="Read-only assistant tool suite",
         narrative="As the Copilot, I need deterministic tools, so that every number I "
                   "report was computed rather than generated.",
         ac=["Tools registered: resolve_machine, machine_stats, stat_query, search_records, part_usage, top_machines, pattern_lookup, record_history.",
             "Every tool is READ access class, plant-scoped and argument-validated with server-side clamping.",
             "Each tool returns coverage metadata alongside its values.",
             "Tool outputs are captured in the run trace for verification and citation."]),
    dict(key="LS-122", epic="EPIC-12", type="Story", points=8, priority="P0", sprint="S8",
         component="AI", labels=["assistant", "agent"], depends=["LS-111", "LS-121"],
         summary="Multi-step investigation planner with replanning",
         narrative="As an engineer asking why something keeps failing, I want the system to "
                   "actually investigate, so that I get an analysis rather than a search result.",
         ac=["The planner chooses the next tool based on prior observations rather than a fixed chain.",
             "A ROOT_CAUSE_INVESTIGATION intent gets a larger step and token budget than a simple lookup.",
             "The benchmark investigation chains at least four dependent tool calls and reaches a cited conclusion.",
             "Simple factual questions still resolve in one or two steps — the planner does not over-investigate.",
             "Agentic evaluation suite success rate meets the threshold in LS-145."]),
    dict(key="LS-123", epic="EPIC-12", type="Story", points=5, priority="P0", sprint="S8",
         component="AI", labels=["assistant", "trust"], depends=["LS-122"],
         summary="Typed answer blocks with trust labels",
         narrative="As a user, I want to see at a glance what is fact, what is calculated "
                   "and what is speculation, so that I never mistake a guess for a finding.",
         ac=["Blocks typed SUMMARY, FACT, CALCULATED, PATTERN and HYPOTHESIS as a wire-format property.",
             "CALCULATED blocks carry the source tool and coverage; HYPOTHESIS blocks carry POSSIBLE or LIKELY plus the fixed disclaimer.",
             "The frontend renders badges directly from the label — trust is never a UI decision.",
             "Schema is versioned and covered by contract tests."]),
    dict(key="LS-124", epic="EPIC-12", type="Story", points=5, priority="P0", sprint="S8",
         component="AI", labels=["assistant", "trust"], depends=["LS-123", "LS-041"],
         summary="Citation builder linking every claim to source records",
         narrative="As an engineer, I want to click any claim and land on the original log "
                   "row, so that I can verify the system rather than trust it.",
         ac=["Citations link answer blocks to maintenance and raw record identifiers.",
             "Every FACT block carries at least one resolvable citation within the caller's scope.",
             "Citations persist with the message so a historical answer remains verifiable.",
             "Following a citation opens the View Source provenance from LS-041."]),
    dict(key="LS-125", epic="EPIC-12", type="Story", points=5, priority="P0", sprint="S9",
         component="AI", labels=["assistant", "memory"], depends=["LS-116", "LS-120"],
         summary="Conversation context carrying resolved entities across turns",
         narrative="As a user, I want follow-up questions to just work, so that I can have a "
                   "conversation instead of restating the machine every time.",
         ac=["Conversation state carries the last N turns' intents and resolved entities, not raw transcripts.",
             "A follow-up such as 'aur is saal?' resolves against the previously resolved machine and reports what it assumed.",
             "Context is bounded so a long conversation does not grow unboundedly in tokens.",
             "A user can start a fresh context explicitly."]),
    dict(key="LS-126", epic="EPIC-12", type="Story", points=5, priority="P0", sprint="S9",
         component="AI", labels=["assistant", "i18n"], depends=["LS-123"],
         summary="Multilingual answers in English, Hindi, Marathi and Hinglish",
         narrative="As a shop-floor user, I want answers in my language, so that the product "
                   "is usable by everyone in the plant, not only by managers.",
         ac=["Answers render in the user's selected language while numbers stay identical across languages.",
             "Trust badges are localised; raw log text is never translated.",
             "A Devanagari or Marathi question is answered correctly in the selected language.",
             "Covered by the assistant golden set in both Latin and Devanagari scripts."]),
    dict(key="LS-127", epic="EPIC-12", type="Story", points=3, priority="P0", sprint="S9",
         component="AI", labels=["assistant", "reliability"], depends=["LS-122"],
         summary="Graceful degradation when the model provider is unavailable",
         narrative="As a user during a provider outage, I want the deterministic parts to "
                   "still answer, so that the product stays useful when the model is not.",
         ac=["Provider failure returns deterministic blocks — statistics and retrieved records — with no generated prose.",
             "The response uses the documented 424 semantics and states plainly that AI composition is unavailable.",
             "The circuit breaker prevents repeated slow failures from degrading overall latency.",
             "Verified by a staging test that disables the model provider."]),
]

# --------------------------------------------------------------------------------------
# EPIC-13 — Trust, Guardrails & Verification
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-130", epic="EPIC-13", type="Story", points=8, priority="P0", sprint="S8",
         component="AI-Safety", labels=["guardrail", "differentiator"], depends=["LS-123", "LS-121"],
         summary="Numeric guardrail: every numeral traced to a tool output",
         narrative="As a plant head, I want certainty that the system never invents a "
                   "number, so that I can act on what it tells me.",
         ac=["Every numeral in a FACT or CALCULATED block is matched against values present in the run's tool outputs, including rounded forms.",
             "An unmatched numeral causes substitution with the tool value, or the block is dropped if unmappable.",
             "Every violation is logged with the run id and emits a metric.",
             "The golden answer set achieves 100% numeric accuracy; anything less fails CI.",
             "A deliberately hallucinating fake model is used in tests to prove the guardrail fires."]),
    dict(key="LS-131", epic="EPIC-13", type="Story", points=5, priority="P0", sprint="S8",
         component="AI-Safety", labels=["guardrail"], depends=["LS-123"],
         summary="Label enforcement: causal language forced into HYPOTHESIS",
         narrative="As a reliability engineer, I want speculation clearly marked, so that a "
                   "guess is never presented to my plant head as a confirmed root cause.",
         ac=["Causal markers in English, Hindi and Marathi are detected outside HYPOTHESIS blocks.",
             "Offending content is force-wrapped into a HYPOTHESIS block with the fixed disclaimer.",
             "HYPOTHESIS blocks are stripped of any new numerals not present in tool outputs.",
             "Detection patterns are unit-tested across all three languages."]),
    dict(key="LS-132", epic="EPIC-13", type="Story", points=5, priority="P0", sprint="S8",
         component="AI-Safety", labels=["guardrail"], depends=["LS-124"],
         summary="Citation completeness check",
         narrative="As a user, I want every stated fact to be verifiable, so that an "
                   "uncitable claim never reaches my screen.",
         ac=["FACT blocks without at least one resolvable citation are dropped before the response is returned.",
             "Citations pointing outside the caller's tenant or plant are treated as invalid and raise a security event.",
             "Dropped blocks are logged with the reason and counted as a metric.",
             "Citation validity on the golden set meets the configured threshold."]),
    dict(key="LS-133", epic="EPIC-13", type="Story", points=3, priority="P0", sprint="S10",
         component="AI-Safety", labels=["guardrail", "database"], depends=["LS-156"],
         summary="Human-only CONFIRMED transition enforced at the database",
         narrative="As a customer, I want a hard guarantee that no machine confirmed a root "
                   "cause, so that the trust principle cannot be bypassed by a code bug.",
         ac=["A database trigger rejects any transition to CONFIRMED where the actor is not a human user.",
             "Service-layer checks exist as well, but the trigger is the authority.",
             "An attempted machine confirmation raises a security event and fails the transaction.",
             "Covered by an integration test that attempts the transition as a system actor."]),
    dict(key="LS-134", epic="EPIC-13", type="Story", points=5, priority="P0", sprint="S8",
         component="AI-Safety", labels=["guardrail", "security"], depends=["LS-112", "LS-121"],
         summary="Prompt-injection defences",
         narrative="As a security reviewer, I want a hostile log line to be inert, so that "
                   "untrusted plant data cannot steer the system.",
         ac=["Retrieved record text and inbound messages are fenced and labelled as quoted data in every prompt.",
             "The system prompt states that quoted content is never an instruction.",
             "Because no tool has direct write access, a successful injection can at worst produce a proposal a human rejects.",
             "Injection canaries are part of the CI safety suite and of production sampling.",
             "A record containing an instruction-shaped payload is proven not to alter tool selection."]),
    dict(key="LS-135", epic="EPIC-13", type="Story", points=3, priority="P0", sprint="S10",
         component="AI-Safety", labels=["guardrail", "observability"], depends=["LS-130", "LS-131"],
         summary="Guardrail violation logging, metrics and alerting",
         narrative="As an engineer, I want to know immediately when guardrails start firing "
                   "more often, so that a bad prompt or model change is caught in hours.",
         ac=["Every violation records type, run id, agent, model and prompt version.",
             "Violation rate is a dashboard metric segmented by type and model.",
             "An alert fires when the rate exceeds the configured threshold over a rolling window.",
             "A spike is a documented trigger for prompt or model rollback via LS-206."]),
    dict(key="LS-136", epic="EPIC-13", type="Story", points=3, priority="P1", sprint="S10",
         component="AI-Safety", labels=["guardrail", "ux"], depends=["LS-120"],
         summary="Out-of-scope handling and honest refusals",
         narrative="As a user asking something the product cannot answer, I want a clear no "
                   "with alternatives, so that I am not misled by a confident non-answer.",
         ac=["Out-of-scope questions produce a polite refusal that lists what the product can actually do.",
             "Questions with no supporting data return an explicit 'not enough data' rather than an invented estimate.",
             "Refusals are localised into all supported languages.",
             "Refusal correctness is measured by the safety suite at 100%."]),
]

# --------------------------------------------------------------------------------------
# EPIC-14 — AI Evaluation & Quality Harness
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-140", epic="EPIC-14", type="Story", points=8, priority="P0", sprint="S5",
         component="AI-Quality", labels=["eval", "moat"], depends=["LS-002"],
         summary="Extraction golden set of 200 hand-labelled messy rows",
         narrative="As an engineer, I want a realistic labelled benchmark, so that "
                   "extraction quality is measured rather than assumed.",
         ac=["200 rows drawn from real design-partner files, anonymised, covering Hinglish, shorthand, Devanagari and OCR output.",
             "Every field hand-labelled with the correct value, including explicit nulls.",
             "Difficulty is stratified so the set is not dominated by easy rows.",
             "Stored under version control with a documented licence and anonymisation procedure.",
             "Baseline field F1 and auto-approval rate recorded as the reference point."]),
    dict(key="LS-141", epic="EPIC-14", type="Story", points=5, priority="P0", sprint="S5",
         component="AI-Quality", labels=["eval"], depends=["LS-002"],
         summary="Resolution golden set of 150 machine-text cases",
         narrative="As an engineer, I want resolver accuracy measured, so that a cascade "
                   "change cannot quietly break machine matching.",
         ac=["150 real machine texts with the correct target machine labelled, including deliberately ambiguous cases.",
             "Covers abbreviations, Hinglish, Devanagari, typos and genuinely unresolvable text.",
             "Unresolvable cases are labelled as such so over-eager matching is penalised.",
             "Baseline precision@1 and recall recorded."]),
    dict(key="LS-142", epic="EPIC-14", type="Story", points=5, priority="P0", sprint="S6",
         component="AI-Quality", labels=["eval"], depends=["LS-090"],
         summary="Retrieval golden set of 60 queries with relevance judgements",
         narrative="As an engineer tuning search, I want graded relevance data, so that "
                   "fusion-weight changes are evaluated rather than guessed.",
         ac=["60 realistic queries spanning shorthand, natural language, English, Hindi and Marathi.",
             "Graded relevance judgements per query over a fixed corpus.",
             "Includes queries expected to return nothing, to catch false-positive retrieval.",
             "Baseline nDCG@10, recall@20 and MRR recorded."]),
    dict(key="LS-143", epic="EPIC-14", type="Story", points=8, priority="P0", sprint="S8",
         component="AI-Quality", labels=["eval", "trust"], depends=["LS-123", "LS-140"],
         summary="Assistant golden set of 80 questions with gold facts and numbers",
         narrative="As an engineer, I want answer correctness measured against known truth, "
                   "so that the 100% numeric accuracy claim is continuously verified.",
         ac=["80 questions across every intent, in English, Hinglish and Devanagari.",
             "Each carries the expected numbers, the expected citation set and the expected block labels.",
             "Includes questions whose correct answer is 'not enough data'.",
             "Evaluated for numeric accuracy, citation validity and label correctness.",
             "Numeric accuracy below 100% is a build failure, not a warning."]),
    dict(key="LS-144", epic="EPIC-14", type="Story", points=5, priority="P0", sprint="S9",
         component="AI-Quality", labels=["eval", "security"], depends=["LS-134"],
         summary="Safety suite: injection, out-of-scope and PII probes",
         narrative="As a security reviewer, I want adversarial cases run continuously, so "
                   "that a prompt change cannot reopen a closed hole.",
         ac=["At least 30 cases covering prompt injection via record text, out-of-scope questions, PII extraction attempts and cross-tenant probing.",
             "Injection payloads are embedded in fixture maintenance records, exactly as a real attack would arrive.",
             "Expected behaviour declared per case; any deviation fails the build.",
             "New cases are added whenever a real incident is found in production."]),
    dict(key="LS-145", epic="EPIC-14", type="Story", points=8, priority="P0", sprint="S9",
         component="AI-Quality", labels=["eval", "tooling"], depends=["LS-140", "LS-141", "LS-142", "LS-143"],
         summary="Evaluation runner with thresholds and an HTML report",
         narrative="As an engineer, I want one command to tell me whether the AI got better "
                   "or worse, so that prompt work is engineering rather than vibes.",
         ac=["A single command runs every suite and prints a per-metric pass or fail against configured thresholds.",
             "An HTML report shows per-case results with diffs against the stored baseline.",
             "Suites are runnable individually for fast local iteration.",
             "Cost and latency of the evaluation run itself are reported.",
             "Includes the agentic suite: 25 multi-step investigations scored on task success, steps used and cost per run."]),
    dict(key="LS-146", epic="EPIC-14", type="Story", points=5, priority="P0", sprint="S9",
         component="AI-Quality", labels=["eval", "ci"], depends=["LS-145", "LS-018"],
         summary="CI gate blocking merges on evaluation regression",
         narrative="As a team, we want quality regressions blocked automatically, so that "
                   "nobody has to remember to run the evals.",
         ac=["Any PR touching prompts, tools, agent code or retrieval configuration triggers the evaluation suite.",
             "A regression beyond the per-metric tolerance fails the build and annotates the PR.",
             "Numeric accuracy and the safety suite are absolute gates with no tolerance.",
             "An override requires an explicit label and is recorded in the PR history.",
             "Evaluation runs against recorded fixtures where possible to keep CI cost bounded."]),
    dict(key="LS-147", epic="EPIC-14", type="Story", points=5, priority="P1", sprint="S13",
         component="AI-Quality", labels=["eval", "trust", "gtm"], depends=["LS-064", "LS-086"],
         summary="Per-tenant production quality scorecard shown in-product",
         narrative="As a customer, I want to see the system's own accuracy on my data, so "
                   "that I can trust it because it is transparent, not because it is confident.",
         ac=["Scorecard shows auto-approval rate, corrections per 100 records, queue burn-down time and resolver hit rate.",
             "Trends over time are visible, including the effect of each alias-mapping session.",
             "Visible to PLANT_ADMIN and above, and exportable for the customer's own reporting.",
             "Scores below the internal bar surface an explicit improvement action rather than being hidden."]),
]

# --------------------------------------------------------------------------------------
# EPIC-15 — Pattern Detection & Watchtower Agent
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-150", epic="EPIC-15", type="Story", points=5, priority="P0", sprint="S10",
         component="AI", labels=["patterns"], depends=["LS-100"],
         summary="Recurrence detector",
         narrative="As a reliability engineer, I want repeating failures surfaced with their "
                   "interval, so that I can act before the next one.",
         ac=["Detects at least three breakdowns of the same machine and failure mode with interval coefficient of variation within the configured bound.",
             "Reports event count, mean interval, variability and the next expected window as FACT metrics.",
             "Any causal explanation is emitted separately as a labelled HYPOTHESIS.",
             "Thresholds are overridable per plant; detector maths is unit-tested against fixtures."]),
    dict(key="LS-151", epic="EPIC-15", type="Story", points=5, priority="P0", sprint="S10",
         component="AI", labels=["patterns"], depends=["LS-100"],
         summary="Temporary-fix repeat detector",
         narrative="As a maintenance manager, I want to see where we keep applying a band-aid, "
                   "so that a permanent fix gets authorised.",
         ac=["Classifies actions as temporary (clean, tighten, reset, re-tension) versus permanent.",
             "Detects at least two cycles of a temporary fix followed within the window by the same failure mode.",
             "Reports the cycle count and the cumulative downtime consumed by the repeated fixes.",
             "Action classification is dictionary-driven and extensible per plant."]),
    dict(key="LS-152", epic="EPIC-15", type="Story", points=5, priority="P0", sprint="S10",
         component="AI", labels=["patterns"], depends=["LS-100"],
         summary="Cross-machine failure cluster detector",
         narrative="As a reliability engineer, I want to notice when a failure mode spreads "
                   "across a line, so that a systemic cause is not missed one machine at a time.",
         ac=["Detects the same failure mode on at least three machines of the same type or line within the window.",
             "Reports the affected machines, the timeline and the shared attributes.",
             "Scoped by line and machine type with per-plant thresholds.",
             "Evidence links to every contributing record."]),
    dict(key="LS-153", epic="EPIC-15", type="Story", points=3, priority="P0", sprint="S10",
         component="AI", labels=["patterns", "parts"], depends=["LS-104"],
         summary="Part concentration detector",
         narrative="As a maintenance manager, I want to see when one part is consumed "
                   "disproportionately in one place, so that I investigate the cause.",
         ac=["Detects a part exceeding the configured usage count with a share above the threshold on one line or machine group.",
             "Reports total uses, the distribution and the concentration percentage.",
             "Links to the underlying part-usage statistics for verification.",
             "Thresholds overridable per plant."]),
    dict(key="LS-154", epic="EPIC-15", type="Story", points=3, priority="P0", sprint="S10",
         component="AI", labels=["patterns"], depends=["LS-100"],
         summary="Downtime hotspot detector",
         narrative="As a plant head, I want to know which line carries most of my downtime, "
                   "so that improvement effort is aimed correctly.",
         ac=["Detects a line or machine whose downtime share exceeds the configured proportion of the plant total.",
             "Reports absolute hours, share and the comparison window.",
             "Applies the plant's downtime cost to express the hotspot in rupees.",
             "Excludes windows with insufficient coverage rather than reporting a misleading share."]),
    dict(key="LS-155", epic="EPIC-15", type="Story", points=5, priority="P0", sprint="S10",
         component="AI", labels=["patterns", "ux"], depends=["LS-150", "LS-151", "LS-152", "LS-153", "LS-154"],
         summary="Pattern fingerprinting, deduplication and dismissal memory",
         narrative="As an engineer, I want a dismissed pattern to stay dismissed, so that "
                   "the system does not nag me about something I already decided.",
         ac=["Each pattern has a stable fingerprint over its type, scope and evidence shape.",
             "A re-detected pattern updates the existing record rather than creating a duplicate.",
             "Dismissed patterns are suppressed for a configurable cooling-off period.",
             "A materially changed pattern — for example new evidence doubling the count — can re-surface with that change stated."]),
    dict(key="LS-156", epic="EPIC-15", type="Story", points=5, priority="P0", sprint="S10",
         component="AI", labels=["patterns", "trust"], depends=["LS-155"],
         summary="Pattern review lifecycle",
         narrative="As a reliability engineer, I want to triage detected patterns, so that "
                   "the system's suggestions become my team's decisions.",
         ac=["Lifecycle DETECTED to ACKNOWLEDGED to CONFIRMED or DISMISSED, with legal transitions enforced.",
             "Only a human user can move a pattern to CONFIRMED; enforced by the trigger in LS-133.",
             "Dismissal requires a reason, which feeds detector tuning.",
             "Every transition is audited with the actor and timestamp."]),
    dict(key="LS-157", epic="EPIC-15", type="Story", points=8, priority="P0", sprint="S10",
         component="AI", labels=["agent", "watchtower", "differentiator"], depends=["LS-155", "LS-111"],
         summary="Watchtower Agent: scheduled scan, triage and ranking",
         narrative="As a maintenance manager, I want the system to tell me what matters "
                   "without being asked, so that I do not have to remember to look.",
         ac=["Runs nightly on a schedule and on triggers such as a completed large import or a new record on a flagged machine.",
             "Runs all five detectors, deduplicates against dismissal memory, then ranks findings by severity, recency, downtime cost and confidence.",
             "Ranking function is configurable and unit-tested; the scan runs inside its documented budget.",
             "A targeted rescan after a new record completes quickly rather than rescanning the whole plant.",
             "Scan results are persisted as an agent run with a full trace."]),
    dict(key="LS-158", epic="EPIC-15", type="Story", points=8, priority="P0", sprint="S11",
         component="AI", labels=["agent", "watchtower", "retention"], depends=["LS-157", "LS-130"],
         summary="Daily and weekly plant briefing",
         narrative="As a maintenance manager, I want a short morning briefing, so that "
                   "LogSense becomes part of my routine rather than a tab I forget.",
         ac=["Briefing is capped at five ranked items; each carries FACT evidence and at most one labelled hypothesis.",
             "Numbers pass the numeric guardrail exactly as assistant answers do.",
             "Generated in the recipient's language, with every item linking to its evidence.",
             "Daily and weekly cadences are configurable per plant; an empty day produces an honest 'nothing notable' rather than filler.",
             "Delivered for 14 consecutive days to a real plant as the release exit criterion."]),
    dict(key="LS-159", epic="EPIC-15", type="Story", points=5, priority="P1", sprint="S11",
         component="AI", labels=["notifications"], depends=["LS-158"],
         summary="Alert routing and delivery preferences by role",
         narrative="As a user, I want to control what reaches me and how, so that alerts "
                   "stay useful instead of becoming noise I mute.",
         ac=["Routing rules by role: manager receives the briefing, engineer receives machine-level alerts, plant head receives the weekly roll-up.",
             "Per-user channel and frequency preferences, including full opt-out.",
             "Rate limiting prevents alert storms after a large import.",
             "Delivery outcomes are recorded so a missed alert can be investigated."]),
]

# --------------------------------------------------------------------------------------
# EPIC-16 — Generative Work Artifacts
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-160", epic="EPIC-16", type="Story", points=8, priority="P0", sprint="S11",
         component="Product", labels=["agent", "scribe"], depends=["LS-111", "LS-130", "LS-190"],
         summary="Scribe Agent framework: evidence gathering to drafted document",
         narrative="As an engineer, I want the system to draft documents from real evidence, "
                   "so that paperwork stops consuming my Friday.",
         ac=["Shared framework: gather evidence via read tools, draft against a template, verify, then raise a document proposal.",
             "Every generated document passes the numeric, citation and label guardrails before a human ever sees it.",
             "Document templates are versioned and configurable per tenant.",
             "Generation cost and latency are recorded per document.",
             "Drafts always land as proposals; no document is published without human approval."]),
    dict(key="LS-161", epic="EPIC-16", type="Story", points=8, priority="P0", sprint="S11",
         component="Product", labels=["agent", "scribe", "differentiator"], depends=["LS-160"],
         summary="Root-cause analysis draft generator",
         narrative="As a reliability engineer, I want an RCA drafted with the evidence "
                   "already assembled, so that a three-hour job becomes a ten-minute review.",
         ac=["Produces a 5-Why or Fishbone scaffold pre-filled from machine history, similar failures, patterns and part usage.",
             "Every factual claim carries an inline citation to a dated record.",
             "Causal branches are labelled as hypotheses requiring engineering validation — never as confirmed causes.",
             "The engineer can edit every section before approving; edits are retained and audited.",
             "Validated by an engineer approving and exporting a real RCA as a release exit criterion."]),
    dict(key="LS-162", epic="EPIC-16", type="Story", points=5, priority="P1", sprint="S11",
         component="Product", labels=["agent", "scribe"], depends=["LS-160"],
         summary="Shift-handover note generator",
         narrative="As an outgoing shift lead, I want the handover written for me, so that "
                   "knowledge survives the shift change instead of evaporating.",
         ac=["Summarises the shift's records, open breakdowns, pending validations and machines under watch.",
             "Generated in the recipient's language on the plant's configured shift boundaries.",
             "Reviewable and editable before it is issued.",
             "Issued notes are retained and searchable as part of plant history."]),
    dict(key="LS-163", epic="EPIC-16", type="Story", points=8, priority="P1", sprint="S12",
         component="Product", labels=["agent", "scribe"], depends=["LS-160", "LS-102"],
         summary="Monthly reliability review draft",
         narrative="As a maintenance manager, I want the monthly review drafted from data, "
                   "so that I stop rebuilding the same slides from memory.",
         ac=["Covers KPI movement against the prior period, Pareto shifts, top patterns and downtime cost.",
             "Every number is tool-derived and traceable; period-over-period deltas are computed, not narrated.",
             "Generated on a schedule with a configurable period start.",
             "Exportable through LS-166 with citations preserved."]),
    dict(key="LS-164", epic="EPIC-16", type="Story", points=8, priority="P1", sprint="S12",
         component="Product", labels=["agent", "scribe", "value"], depends=["LS-160", "LS-150"],
         summary="Preventive-maintenance interval change proposal",
         narrative="As a maintenance manager, I want an evidence-backed PM interval "
                   "recommendation, so that a schedule change is a decision rather than a guess.",
         ac=["Proposes an interval change from observed recurrence interval, downtime cost and part cost.",
             "Shows the current interval, proposed interval, supporting evidence and expected annual saving.",
             "Explicitly labelled as a recommendation requiring engineering approval.",
             "Approval records the decision in LogSense only — no write-back to any external CMMS, per the product principle."]),
    dict(key="LS-165", epic="EPIC-16", type="Story", points=5, priority="P1", sprint="S12",
         component="Product", labels=["agent", "scribe", "parts"], depends=["LS-160", "LS-104"],
         summary="Spare-stocking recommendation",
         narrative="As a stores manager, I want stocking levels backed by consumption "
                   "history, so that I avoid both stock-outs and dead inventory.",
         ac=["Recommends reorder point and quantity from consumption rate, lead time, criticality and concentration.",
             "States the assumptions and the evidence window explicitly.",
             "Flags parts whose consumption is accelerating relative to the prior period.",
             "Delivered as a proposal for human approval; nothing is ordered by the system."]),
    dict(key="LS-166", epic="EPIC-16", type="Story", points=5, priority="P1", sprint="S12",
         component="Product", labels=["export"], depends=["LS-161"],
         summary="Artifact export to PDF and DOCX with citations preserved",
         narrative="As an engineer, I want to export an RCA for an audit, so that the "
                   "citations survive outside the product.",
         ac=["Export to PDF and DOCX preserves structure, trust labels and inline citations.",
             "Citations render as resolvable references including record identifier and date.",
             "Plant branding and the document template are configurable per tenant.",
             "Exports are generated asynchronously with a pollable job and an audit record."]),
]

# --------------------------------------------------------------------------------------
# EPIC-17 — WhatsApp Field Agent
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-170", epic="EPIC-17", type="Story", points=5, priority="P0", sprint="S12",
         component="Integrations", labels=["whatsapp"], depends=["LS-060"],
         summary="WhatsApp Business API adapter with signature verification",
         narrative="As a security reviewer, I want inbound messages cryptographically "
                   "verified, so that nobody can inject records by forging a webhook.",
         ac=["Official WhatsApp Business API only; unofficial gateways are explicitly rejected in the adapter design.",
             "Webhook signature verified on every request; a failure returns 401 and raises a security event.",
             "Provider is behind a port so a second provider can be added without touching conversation logic.",
             "Outbound sending handles rate limits and template requirements."]),
    dict(key="LS-171", epic="EPIC-17", type="Story", points=5, priority="P0", sprint="S12",
         component="Integrations", labels=["whatsapp"], depends=["LS-170"],
         summary="Inbound webhook with idempotency and message persistence",
         narrative="As the system, I need duplicate deliveries handled safely, so that a "
                   "provider retry never creates two records from one message.",
         ac=["Every inbound message is persisted with its provider message id before processing.",
             "Duplicate message ids are acknowledged and ignored idempotently.",
             "The webhook acknowledges quickly and processes asynchronously to avoid provider timeouts.",
             "Unparseable payloads are stored for investigation rather than dropped."]),
    dict(key="LS-172", epic="EPIC-17", type="Story", points=5, priority="P0", sprint="S12",
         component="Integrations", labels=["whatsapp", "compliance"], depends=["LS-171", "LS-023"],
         summary="Technician contact registry with consented phone-number binding",
         narrative="As a compliance owner, I want technician phone numbers handled lawfully, "
                   "so that DPDP obligations are met from day one.",
         ac=["Technicians are registered by phone number and bound to a user and plant.",
             "Consent is captured and recorded with timestamp and purpose before any binding is active.",
             "Messages from unregistered numbers are rejected with a polite reply and are not stored as records.",
             "Numbers are treated as personal data: encrypted, access-controlled and erasable under LS-211."]),
    dict(key="LS-173", epic="EPIC-17", type="Story", points=8, priority="P0", sprint="S12",
         component="Integrations", labels=["whatsapp"], depends=["LS-172"],
         summary="Conversation state machine",
         narrative="As a technician, I want a short predictable exchange, so that reporting "
                   "a breakdown takes under a minute on my phone.",
         ac=["States NEW, EXTRACTING, AWAITING_FIELD, AWAITING_CONFIRMATION, CONFIRMED and ABANDONED with enforced transitions.",
             "Conversations time out to ABANDONED after a configured idle period without creating a record.",
             "Confirmation echoes a structured summary before anything is saved.",
             "Conversation state is durable across restarts."]),
    dict(key="LS-174", epic="EPIC-17", type="Story", points=8, priority="P0", sprint="S12",
         component="Integrations", labels=["agent", "whatsapp"], depends=["LS-173", "LS-061", "LS-070"],
         summary="Field Agent slot-filling dialogue",
         narrative="As a technician writing in Hinglish, I want to be asked only what is "
                   "missing, so that the system feels helpful rather than bureaucratic.",
         ac=["Extracts all available fields from the first message and asks only for genuinely missing required fields.",
             "Asks at most a configured number of follow-up questions before offering to save what it has.",
             "Replies in the language the technician used, including Hinglish and Devanagari.",
             "On confirmation, creates a staged record via the standard auto-approval path and replies with the record id.",
             "Technicians complete the flow with no training beyond one demonstration."]),
    dict(key="LS-175", epic="EPIC-17", type="Story", points=5, priority="P1", sprint="S12",
         component="Integrations", labels=["whatsapp"], depends=["LS-174"],
         summary="Voice-note transcription hook",
         narrative="As a technician with oily hands, I want to send a voice note, so that "
                   "reporting does not require typing.",
         ac=["Voice media is fetched and sent to a pluggable transcription provider, then follows the identical text path.",
             "Transcription confidence feeds overall extraction confidence; low confidence routes to validation.",
             "Original audio is retained as provenance and is playable in the validation workbench.",
             "Transcription failure produces a helpful reply asking for a typed message, never silence."]),
    dict(key="LS-176", epic="EPIC-17", type="Story", points=3, priority="P1", sprint="S12",
         component="Integrations", labels=["whatsapp", "differentiator"], depends=["LS-174", "LS-150"],
         summary="Recurrence callback on record creation",
         narrative="As a technician, I want to be told when this failure has happened before, "
                   "so that I know to escalate rather than just fix it again.",
         ac=["On confirmation, a recurrence check runs against the machine and failure mode.",
             "A recurrence produces a plain-language note, for example that this is the fifth bearing replacement with a mean interval of 92 days.",
             "The responsible engineer is alerted through the routing rules in LS-159.",
             "The callback uses only deterministic counts and intervals, never generated numbers."]),
    dict(key="LS-177", epic="EPIC-17", type="Story", points=5, priority="P2", sprint="S13",
         component="Integrations", labels=["whatsapp", "memory"], depends=["LS-174", "LS-116"],
         summary="Per-technician phrasing memory",
         narrative="As a frequent reporter, I want the system to learn how I write, so that "
                   "it stops asking me the same clarifying questions.",
         ac=["Per-technician vocabulary and phrasing patterns are stored in semantic memory.",
             "Learned phrasing reduces clarifying questions measurably over time.",
             "Learning is per plant and never shared across tenants.",
             "A technician can reset their learned profile; the reset is audited."]),
]

# --------------------------------------------------------------------------------------
# EPIC-18 — Plant Knowledge Base
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-180", epic="EPIC-18", type="Story", points=8, priority="P1", sprint="S12",
         component="AI", labels=["knowledge-base", "upsell"], depends=["LS-051", "LS-053"],
         summary="Document ingestion for manuals, SOPs and past RCAs",
         narrative="As a reliability engineer, I want the plant's documents searchable "
                   "alongside its records, so that answers draw on everything we know.",
         ac=["Accepts PDF, DOCX and scanned documents, classified by type: manual, SOP, RCA, drawing.",
             "Documents are linked to machines, lines or the plant as a whole.",
             "Original files are stored immutably with the same provenance guarantees as import files.",
             "Ingestion runs as a pollable async job with per-document status."]),
    dict(key="LS-181", epic="EPIC-18", type="Story", points=5, priority="P1", sprint="S12",
         component="AI", labels=["knowledge-base"], depends=["LS-180", "LS-091"],
         summary="Chunking and embedding with document-level provenance",
         narrative="As the system, I need retrievable document chunks that remember where "
                   "they came from, so that answers can cite a page rather than a file.",
         ac=["Documents are chunked with configurable size and overlap, respecting section boundaries where detectable.",
             "Every chunk retains document id, page number and section heading.",
             "Chunks are embedded using the same provider and dimension as record embeddings.",
             "Re-ingesting a document version supersedes the old chunks without breaking existing citations."]),
    dict(key="LS-182", epic="EPIC-18", type="Story", points=8, priority="P1", sprint="S13",
         component="AI", labels=["knowledge-base"], depends=["LS-181", "LS-092"],
         summary="Unified retrieval across records and documents",
         narrative="As a user, I want one search across history and manuals, so that I do "
                   "not have to guess which source holds the answer.",
         ac=["A single retrieval call returns fused results from both records and document chunks.",
             "Result type is clearly distinguished so the UI and the agent can treat them differently.",
             "Callers can restrict to records only, documents only, or both.",
             "Ranking is evaluated by an extension of the retrieval golden set."]),
    dict(key="LS-183", epic="EPIC-18", type="Story", points=5, priority="P1", sprint="S13",
         component="AI", labels=["knowledge-base", "trust"], depends=["LS-182", "LS-124"],
         summary="Document-grounded answers with page-level citations",
         narrative="As an engineer, I want manual-based answers cited to the page, so that "
                   "I can verify a torque spec before acting on it.",
         ac=["A search_documents tool is registered for the Copilot and the Scribe.",
             "Document-derived claims cite document, page and section.",
             "Document and record evidence are visually distinguished in the response schema.",
             "Manual-derived values are still subject to the numeric guardrail against the retrieved chunk text."]),
    dict(key="LS-184", epic="EPIC-18", type="Story", points=3, priority="P1", sprint="S13",
         component="AI", labels=["knowledge-base", "security"], depends=["LS-180", "LS-024"],
         summary="Access control for restricted documents",
         narrative="As a plant admin, I want to restrict sensitive documents, so that "
                   "commercial contracts are not retrievable by every technician.",
         ac=["Documents carry a minimum role for retrieval, defaulting to the plant's standard visibility.",
             "Retrieval filters by the caller's role before ranking, so restricted content never reaches the model context.",
             "Restricted-document access attempts are audited.",
             "Covered by the role-matrix test suite."]),
    dict(key="LS-185", epic="EPIC-18", type="Story", points=8, priority="P2", sprint="S13",
         component="AI", labels=["knowledge-base", "scribe"], depends=["LS-183", "LS-160"],
         summary="Job-plan generation from history and SOPs",
         narrative="As a new technician, I want to know how this plant usually fixes this "
                   "failure, so that tribal knowledge is available without finding the veteran.",
         ac=["Generates a job plan from historical actions, parts consumed and relevant SOP sections.",
             "States how many past occurrences informed the plan and links to each.",
             "Explicitly marked as guidance drawn from history, not as an approved work instruction.",
             "Available in all supported languages."]),
]

# --------------------------------------------------------------------------------------
# EPIC-19 — Proposal & Approval Inbox
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-190", epic="EPIC-19", type="Story", points=5, priority="P0", sprint="S7",
         component="Product", labels=["governance", "differentiator"], depends=["LS-016", "LS-110"],
         summary="Proposal entity as the universal agent write envelope",
         narrative="As a customer, I want every agent-initiated change to arrive as a "
                   "proposal, so that agency never becomes unsupervised authority.",
         ac=["Proposal stores type, payload, evidence, confidence, risk, status, proposing run and deciding user.",
             "Status lifecycle DRAFT, PENDING, APPROVED, REJECTED, APPLIED, REVERTED with enforced transitions.",
             "Every proposal links to the agent run and trace that produced it.",
             "No code path writes agent-originated data outside this envelope; enforced by an ArchUnit rule."]),
    dict(key="LS-191", epic="EPIC-19", type="Story", points=5, priority="P0", sprint="S10",
         component="Product", labels=["governance"], depends=["LS-190"],
         summary="Approval inbox API with filters and ageing",
         narrative="As an engineer, I want one place showing everything waiting on me, so "
                   "that proposals do not pile up unseen.",
         ac=["Inbox filterable by type, agent, risk, confidence and age; sortable by impact.",
             "Ageing indicators highlight proposals pending beyond the configured threshold.",
             "Each entry shows the evidence and a link to the full agent trace.",
             "Scoped to the caller's plants and roles."]),
    dict(key="LS-192", epic="EPIC-19", type="Story", points=8, priority="P0", sprint="S11",
         component="Product", labels=["governance"], depends=["LS-191"],
         summary="Approve and reject with effect application and reversibility",
         narrative="As an engineer, I want approving a proposal to apply it safely and "
                   "reversibly, so that a mistaken approval is not permanent.",
         ac=["Approval applies the effect transactionally and records the deciding user and timestamp.",
             "Every proposal type ships with an inverse operation; revert restores the prior state and is itself audited.",
             "Rejection requires a reason and feeds agent quality metrics.",
             "A partially applied effect can never be left behind — application either commits fully or rolls back.",
             "No agent-originated write reaches the database without a recorded human decision, verified by an integration test."]),
    dict(key="LS-193", epic="EPIC-19", type="Story", points=5, priority="P0", sprint="S11",
         component="Product", labels=["governance", "agent"], depends=["LS-192", "LS-117"],
         summary="Autonomy-level policy gate on every agent write",
         narrative="As a plant IT head, I want to decide how much autonomy each agent has, "
                   "so that we expand trust deliberately rather than by default.",
         ac=["Policy gate evaluates agent, proposal type, risk and confidence against the tenant's autonomy level.",
             "At L3, whitelisted low-risk high-confidence proposals auto-apply but still create an auditable proposal row with the decision recorded as automatic.",
             "L4 external writes are unreachable: no proposal type targets an external system.",
             "Changing autonomy level takes effect immediately and is audited."]),
    dict(key="LS-194", epic="EPIC-19", type="Story", points=3, priority="P1", sprint="S11",
         component="Product", labels=["governance", "notifications"], depends=["LS-191", "LS-159"],
         summary="Proposal notifications and reminders",
         narrative="As an engineer, I want to be told when something needs my decision, so "
                   "that work does not stall in an inbox I forgot to open.",
         ac=["Notification on new proposals, routed by type and role.",
             "Reminders for proposals pending beyond the ageing threshold, rate-limited to avoid nagging.",
             "Per-user preferences and opt-out honoured.",
             "High-risk proposals can be configured to notify immediately."]),
    dict(key="LS-195", epic="EPIC-19", type="Story", points=3, priority="P1", sprint="S13",
         component="Product", labels=["governance", "metrics"], depends=["LS-192"],
         summary="Proposal outcome analytics per agent",
         narrative="As a product owner, I want to see which agents produce proposals people "
                   "accept, so that autonomy is earned with evidence rather than granted by opinion.",
         ac=["Approval rate, rejection reasons and time-to-decision tracked per agent and proposal type.",
             "Trends visible over time and segmented per tenant.",
             "A low approval rate surfaces an explicit recommendation against raising that agent's autonomy level.",
             "Metrics feed the per-tenant scorecard in LS-147."]),
]

# --------------------------------------------------------------------------------------
# EPIC-20 — AI Observability, Cost & FinOps
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-200", epic="EPIC-20", type="Story", points=5, priority="P0", sprint="S13",
         component="Platform", labels=["finops", "observability"], depends=["LS-110"],
         summary="Token, latency and cost recorded per run and per step",
         narrative="As the business, I want the rupee cost of every AI operation visible, "
                   "so that pricing is grounded in measured unit economics.",
         ac=["Input and output tokens, model, latency and computed cost recorded on every step and aggregated per run.",
             "Cost computed from a configurable per-model rate table, versioned over time.",
             "Costs are attributable to tenant, plant, agent and trigger.",
             "Historical rate changes do not retroactively alter recorded costs."]),
    dict(key="LS-201", epic="EPIC-20", type="Story", points=5, priority="P0", sprint="S13",
         component="Platform", labels=["finops"], depends=["LS-200"],
         summary="Per-tenant cost ledger and monthly cost-per-plant report",
         narrative="As a founder, I want to know what each plant costs to serve, so that a "
                   "subscription price is a margin decision rather than a guess.",
         ac=["Ledger aggregates AI, storage, WhatsApp and compute cost per tenant per month.",
             "Cost per plant per month is reportable and trendable.",
             "Costs are broken down by workload: extraction, assistant, watchtower, artifacts.",
             "The report is exportable and feeds the pricing model in the vision document."]),
    dict(key="LS-202", epic="EPIC-20", type="Story", points=5, priority="P0", sprint="S13",
         component="Platform", labels=["finops"], depends=["LS-201", "LS-114"],
         summary="Budget enforcement with soft warning and hard stop",
         narrative="As the business, I want a runaway tenant to be capped, so that one "
                   "customer's usage cannot destroy the month's margin.",
         ac=["Per-tenant monthly budget with configurable soft-warning and hard-stop thresholds.",
             "Crossing the soft threshold notifies the account owner and internal operations.",
             "The hard stop degrades gracefully: deterministic features keep working, generative features are paused with a clear message.",
             "Budget state is visible in the admin UI and overridable by an authorised internal user, with the override audited."]),
    dict(key="LS-203", epic="EPIC-20", type="Story", points=5, priority="P0", sprint="S13",
         component="Platform", labels=["observability"], depends=["LS-013", "LS-110"],
         summary="OpenTelemetry traces spanning API, agent, tool and model calls",
         narrative="As an engineer debugging a slow answer, I want one trace covering the "
                   "whole path, so that I can attribute latency precisely.",
         ac=["A single trace spans the HTTP request, agent run, every tool call and every model call.",
             "Spans carry tenant, plant, agent, tool and model attributes.",
             "traceId from the error envelope correlates to the exported trace.",
             "Sampling is configurable, with errors and slow requests always sampled."]),
    dict(key="LS-204", epic="EPIC-20", type="Story", points=5, priority="P1", sprint="S13",
         component="Platform", labels=["observability", "privacy"], depends=["LS-203"],
         summary="Prompt and response sampling store with PII redaction",
         narrative="As an engineer improving quality, I want real examples to learn from, "
                   "so that prompt changes are informed by production rather than by guesses.",
         ac=["A configurable sample of prompts and responses is retained with a defined retention period.",
             "Technician names and phone numbers are redacted before storage.",
             "Sampling is disableable per tenant for customers who require it contractually.",
             "Access to samples is restricted and audited."]),
    dict(key="LS-205", epic="EPIC-20", type="Story", points=5, priority="P1", sprint="S13",
         component="Platform", labels=["observability", "finops"], depends=["LS-200", "LS-145"],
         summary="Model performance dashboard: quality against cost and latency",
         narrative="As a product owner, I want to compare model tiers on real workloads, so "
                   "that routing decisions are evidence-based.",
         ac=["Dashboard compares tiers on evaluation quality, production latency and cost per operation.",
             "Segmented by task type: extraction, planning, composition, synthesis.",
             "Highlights where a cheaper tier would meet the quality bar.",
             "Used as the input to the quarterly routing review."]),
    dict(key="LS-206", epic="EPIC-20", type="Story", points=5, priority="P0", sprint="S13",
         component="Platform", labels=["observability", "release"], depends=["LS-110"],
         summary="Prompt and model version registry with rollback",
         narrative="As an engineer, I want prompts versioned like code with a fast rollback, "
                   "so that a bad change is reversed in minutes.",
         ac=["Every prompt is versioned; the version used is recorded on every step.",
             "Model and prompt versions are changeable by configuration without a code deployment.",
             "Rollback to a prior version is a single operation and is audited.",
             "Evaluation results are stored against each version for comparison."]),
    dict(key="LS-207", epic="EPIC-20", type="Story", points=5, priority="P1", sprint="S14",
         component="Platform", labels=["release"], depends=["LS-206", "LS-135"],
         summary="Canary rollout for prompt and model changes",
         narrative="As an engineer, I want changes exposed to a slice of traffic first, so "
                   "that a regression affects a few runs rather than every customer.",
         ac=["Traffic can be split between prompt or model versions at a configurable percentage.",
             "Guardrail violation rate, latency and cost are compared between arms automatically.",
             "Automatic rollback triggers when the canary arm breaches a configured threshold.",
             "Canary state and outcome are visible in the release dashboard."]),
]

# --------------------------------------------------------------------------------------
# EPIC-21 — Security, Privacy & Compliance
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-210", epic="EPIC-21", type="Story", points=5, priority="P0", sprint="S14",
         component="Security", labels=["security"], depends=["LS-021"],
         summary="Encryption at rest and in transit with key management",
         narrative="As a plant IT head, I want a clear encryption story, so that my security "
                   "review can be completed rather than deferred.",
         ac=["TLS enforced on every external connection; internal service traffic encrypted where it crosses a trust boundary.",
             "Database and object storage encrypted at rest with managed keys.",
             "Key rotation procedure documented and rehearsed.",
             "Encryption posture is written into the one-page security FAQ from LS-006."]),
    dict(key="LS-211", epic="EPIC-21", type="Story", points=8, priority="P0", sprint="S14",
         component="Security", labels=["compliance", "dpdp"], depends=["LS-172", "LS-016"],
         summary="DPDP Act 2023 compliance for technician personal data",
         narrative="As a compliance owner, I want India's data protection obligations met, "
                   "so that handling technician names and numbers is lawful.",
         ac=["Personal data fields are inventoried with purpose and lawful basis documented.",
             "Consent capture and withdrawal implemented for WhatsApp phone-number binding.",
             "Erasure request handling removes or irreversibly pseudonymises personal data while preserving maintenance history integrity.",
             "Data-principal request handling has a documented SLA and an audit trail.",
             "Reviewed by legal counsel before the first production tenant."]),
    dict(key="LS-212", epic="EPIC-21", type="Story", points=3, priority="P0", sprint="S14",
         component="Security", labels=["compliance", "trust"], depends=["LS-060"],
         summary="Sub-processor register and zero-retention model configuration",
         narrative="As a plant head asking whether my data goes to a foreign AI company, I "
                   "want an honest, documented answer, so that I can approve the pilot.",
         ac=["Every sub-processor listed with purpose, data categories and location.",
             "Zero-retention or enterprise API configuration is available and documented as the default posture.",
             "A contractual commitment that customer data is never used to train models is implemented and verifiable in configuration.",
             "The register is customer-facing and versioned; changes are notified per the DPA."]),
    dict(key="LS-213", epic="EPIC-21", type="Story", points=5, priority="P0", sprint="S14",
         component="Security", labels=["compliance"], depends=["LS-211"],
         summary="Customer data export and deletion on contract exit",
         narrative="As a departing customer, I want my data back and then deleted, so that "
                   "the exit terms in the contract are real.",
         ac=["Full tenant export in open formats, including records, provenance, documents and audit logs.",
             "Deletion removes tenant data from primary storage, object storage and derived indexes within the contractual window.",
             "Backup expiry for deleted tenants is documented and enforced.",
             "A deletion certificate is produced and retained as evidence."]),
    dict(key="LS-214", epic="EPIC-21", type="Story", points=3, priority="P0", sprint="S14",
         component="Security", labels=["security"], depends=["LS-022"],
         summary="Secrets management and rotation runbook",
         narrative="As an operator, I want secrets managed properly, so that a leaked "
                   "credential is a contained incident rather than a breach.",
         ac=["No secret is present in source control, container images or logs; CI scans enforce it.",
             "Secrets are loaded from a managed store or injected environment at runtime.",
             "Rotation procedure documented for every secret class, with an owner and a cadence.",
             "The application fails fast and loudly on a missing required secret in production."]),
    dict(key="LS-215", epic="EPIC-21", type="Story", points=5, priority="P0", sprint="S14",
         component="Security", labels=["security", "ci"], depends=["LS-018"],
         summary="SAST, DAST, dependency and container scanning in CI",
         narrative="As a security owner, I want known vulnerability classes caught "
                   "automatically, so that security is continuous rather than annual.",
         ac=["Static analysis, dependency scanning and container image scanning run on every PR.",
             "Dynamic scanning runs against staging on a schedule.",
             "High and critical findings block release; the exception process requires a named approver and an expiry.",
             "Findings are tracked to closure with an agreed remediation SLA."]),
    dict(key="LS-216", epic="EPIC-21", type="Story", points=3, priority="P1", sprint="S14",
         component="Security", labels=["security"], depends=["LS-050"],
         summary="Upload malware scanning",
         narrative="As a security reviewer, I want uploaded files scanned, so that the "
                   "platform is not a malware distribution path between plants.",
         ac=["Files are scanned before processing; infected files are quarantined and the uploader is notified.",
             "Scanning failure blocks processing rather than failing open.",
             "Quarantined files are retained for investigation and are never downloadable by tenants.",
             "Scan outcomes are audited."]),
    dict(key="LS-217", epic="EPIC-21", type="Story", points=8, priority="P0", sprint="S15",
         component="Security", labels=["security", "gtm"], depends=["LS-025", "LS-215"],
         summary="Third-party penetration test and remediation",
         narrative="As a founder selling to enterprises, I want an independent security "
                   "assessment, so that procurement has evidence rather than assurances.",
         ac=["Scope covers authentication, tenant isolation, IDOR, upload abuse, prompt injection and the agent write path.",
             "All high and critical findings remediated and retested before the report is shared.",
             "An executive summary is produced that can be shared with prospects under NDA.",
             "Findings are converted into regression tests so they cannot recur."]),
    dict(key="LS-218", epic="EPIC-21", type="Story", points=13, priority="P1", sprint="S15",
         component="Security", labels=["compliance", "enterprise"], depends=["LS-210", "LS-214", "LS-215"],
         summary="SOC 2 Type I readiness",
         narrative="As a founder entering enterprise deals, I want the control framework in "
                   "place, so that a SOC 2 requirement does not stall a signed deal for six months.",
         ac=["Control framework mapped to the trust services criteria, with gaps listed and owned.",
             "Required policies written and approved: access control, change management, incident response, vendor management, business continuity.",
             "Evidence collection automated where possible rather than assembled manually at audit time.",
             "A readiness assessment is completed and a remediation plan with dates is agreed.",
             "Treated as a sales enabler with a trigger, not as a prerequisite for the first pilots."]),
]

# --------------------------------------------------------------------------------------
# EPIC-22 — Reliability, SRE & Deployment
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-220", epic="EPIC-22", type="Story", points=5, priority="P0", sprint="S14",
         component="Platform", labels=["deployment"], depends=["LS-011"],
         summary="Production container image and runtime configuration",
         narrative="As an operator, I want a minimal, reproducible image, so that deployment "
                   "is predictable and the attack surface is small.",
         ac=["Distroless or equivalent minimal base image running as a non-root user.",
             "Image build is reproducible and tagged with the commit SHA.",
             "Every environment-specific value is supplied by environment variable; the full matrix is documented.",
             "Flyway migration strategy on boot is explicit and documented for multi-instance startup."]),
    dict(key="LS-221", epic="EPIC-22", type="Story", points=8, priority="P0", sprint="S14",
         component="Platform", labels=["iac"], depends=["LS-220"],
         summary="Infrastructure as code for staging and production",
         narrative="As an operator, I want infrastructure defined in code, so that "
                   "environments are reproducible and drift is visible.",
         ac=["Terraform (or equivalent) defines compute, database, object storage, networking and secrets.",
             "Staging and production share modules and differ only by variables.",
             "Plan output is reviewed in the PR before any apply; state is stored remotely with locking.",
             "A new environment can be stood up from scratch by following the documented procedure."]),
    dict(key="LS-222", epic="EPIC-22", type="Story", points=5, priority="P0", sprint="S15",
         component="Platform", labels=["deployment"], depends=["LS-221"],
         summary="Blue/green deployment with automated rollback",
         narrative="As an operator, I want deploys to be boring and reversible, so that "
                   "shipping during the working day is safe.",
         ac=["New versions are deployed alongside the old and receive traffic only after health checks pass.",
             "Rollback is a single operation completing within the documented target time.",
             "Database migrations are backward-compatible so both versions can run during the switch.",
             "A deployment is proven and a rollback rehearsed in staging."]),
    dict(key="LS-223", epic="EPIC-22", type="Story", points=5, priority="P0", sprint="S15",
         component="Platform", labels=["sre"], depends=["LS-203"],
         summary="Service level objectives, error budgets and alerting",
         narrative="As an operator, I want defined reliability targets, so that 'is it "
                   "working?' has a measurable answer.",
         ac=["SLOs defined for API availability, API latency, ingestion throughput and assistant answer latency.",
             "Error budgets tracked with a documented policy for what happens when one is exhausted.",
             "Alerts fire on SLO burn rate rather than on raw error counts, and route to a named on-call owner.",
             "Every alert links to the runbook entry that resolves it."]),
    dict(key="LS-224", epic="EPIC-22", type="Story", points=5, priority="P0", sprint="S15",
         component="Platform", labels=["sre", "dr"], depends=["LS-221"],
         summary="Backup, restore and a rehearsed disaster-recovery drill",
         narrative="As a customer, I want confidence that my three years of history survives "
                   "an incident, so that adopting the product is not a data risk.",
         ac=["Automated backups of database and object storage with documented RPO and RTO targets.",
             "Restore procedure documented and executed end-to-end into a clean environment.",
             "The drill is timed and its result recorded; a missed target creates a follow-up item.",
             "The drill is scheduled to repeat quarterly with an owner."]),
    dict(key="LS-225", epic="EPIC-22", type="Story", points=3, priority="P0", sprint="S15",
         component="Platform", labels=["sre", "docs"], depends=["LS-223"],
         summary="Runbooks for the top ten operational failures",
         narrative="As an on-call engineer, I want a written procedure for likely incidents, "
                   "so that recovery does not depend on who is awake.",
         ac=["Runbooks cover model provider outage, embedding provider outage, WhatsApp provider failure, database saturation, storage exhaustion, stuck import job, runaway agent cost, failed migration, tenant isolation alert and backup failure.",
             "Each runbook states symptoms, diagnosis steps, remediation and escalation path.",
             "Runbooks are linked from the corresponding alerts.",
             "Each is validated at least once against a simulated incident."]),
    dict(key="LS-226", epic="EPIC-22", type="Story", points=8, priority="P0", sprint="S15",
         component="Platform", labels=["performance"], depends=["LS-106", "LS-092"],
         summary="Load and soak testing at one million records",
         narrative="As an operator, I want performance characterised before a customer finds "
                   "the limit, so that capacity planning is proactive.",
         ac=["A one-million-record dataset is generated with realistic distribution.",
             "Load tests cover search, dashboard, record listing and assistant queries at target concurrency.",
             "A soak test runs long enough to expose memory leaks and connection exhaustion.",
             "Slow queries are identified and indexed; results are documented as the capacity baseline."]),
    dict(key="LS-227", epic="EPIC-22", type="Story", points=3, priority="P1", sprint="S15",
         component="Platform", labels=["release"], depends=["LS-220"],
         summary="Feature-flag service for staged rollout",
         narrative="As a product owner, I want features enabled per tenant, so that a design "
                   "partner can trial something before it reaches everyone.",
         ac=["Flags evaluated per tenant and per user with a safe default when evaluation fails.",
             "Flag state is changeable without a deployment and every change is audited.",
             "Flags are listable with their owner and a removal date to prevent permanent accumulation.",
             "Flag state is recorded in the agent run policy snapshot where it affects behaviour."]),
]

# --------------------------------------------------------------------------------------
# EPIC-23 — Commercialization & Onboarding
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-230", epic="EPIC-23", type="Story", points=5, priority="P0", sprint="S15",
         component="GTM", labels=["billing"], depends=["LS-201"],
         summary="Usage metering per tenant",
         narrative="As a founder, I want usage measured per tenant, so that billing and "
                   "pricing reflect what customers actually consume.",
         ac=["Meters records ingested, questions asked, agent runs, artifacts generated, WhatsApp conversations and storage consumed.",
             "Metered data is aggregated per billing period and is immutable once the period closes.",
             "Usage is visible to the customer in-product, not only internally.",
             "Meter data reconciles with the cost ledger from LS-201."]),
    dict(key="LS-231", epic="EPIC-23", type="Story", points=5, priority="P1", sprint="S15",
         component="GTM", labels=["billing"], depends=["LS-230"],
         summary="Plan tiers and entitlement enforcement",
         narrative="As a founder, I want plans enforced in the product, so that upgrades "
                   "happen through the product rather than through a conversation.",
         ac=["Plan defines included plants, seats, agent features and usage allowances.",
             "Entitlements are enforced at the API boundary with a clear upgrade message, never a silent failure.",
             "Approaching a limit notifies the customer before the limit is reached.",
             "Plan changes take effect immediately and are audited."]),
    dict(key="LS-232", epic="EPIC-23", type="Story", points=5, priority="P1", sprint="S15",
         component="GTM", labels=["onboarding"], depends=["LS-035", "LS-065"],
         summary="Self-serve tenant onboarding checklist",
         narrative="As a new plant admin, I want a guided setup, so that onboarding plant "
                   "number three does not require a founder on site.",
         ac=["In-product checklist covering plant setup, machine import, user invites, first file import and first question.",
             "Progress is persisted and visible; each step links directly to the screen that completes it.",
             "Completion is measured as the onboarding funnel, with drop-off visible internally.",
             "A plant can reach its first answered question without any assistance from the vendor."]),
    dict(key="LS-233", epic="EPIC-23", type="Story", points=3, priority="P0", sprint="S15",
         component="GTM", labels=["metrics"], depends=["LS-232"],
         summary="Time-to-first-answer instrumentation",
         narrative="As a founder, I want to know how long a new plant takes to get value, so "
                   "that the four-week promise is measured rather than asserted.",
         ac=["Measures elapsed time from tenant creation to first successfully answered question with citations.",
             "Intermediate milestones tracked: first import, first validated record, first search.",
             "Reported per tenant and as a cohort trend.",
             "Feeds the pilot scorecard from LS-008."]),
    dict(key="LS-234", epic="EPIC-23", type="Story", points=8, priority="P1", sprint="S15",
         component="GTM", labels=["value", "retention"], depends=["LS-158", "LS-031"],
         summary="In-product return-on-investment report",
         narrative="As a maintenance manager justifying renewal, I want evidence of value, "
                   "so that the budget conversation is backed by data.",
         ac=["Reports downtime hours surfaced, recurring failures identified, engineer hours saved on reporting and validation, and records made searchable.",
             "Monetary value uses the plant's own configured downtime cost, never an industry average.",
             "Assumptions are stated explicitly and are adjustable by the customer.",
             "Exportable as a document for the customer's internal use."]),
    dict(key="LS-235", epic="EPIC-23", type="Story", points=5, priority="P2", sprint="S15",
         component="GTM", labels=["billing"], depends=["LS-231"],
         summary="Invoicing export and subscription administration",
         narrative="As a founder, I want billing data exportable to accounting, so that "
                   "invoicing does not become a manual monthly project.",
         ac=["Billing period data exportable in a format the accounting system accepts, including GST fields required in India.",
             "Subscription state, renewal dates and plan history are visible internally.",
             "Proration handled for mid-period plan changes.",
             "Export is reproducible for a closed period and never changes retroactively."]),
    dict(key="LS-236", epic="EPIC-23", type="Story", points=3, priority="P2", sprint="S15",
         component="GTM", labels=["trust"], depends=["LS-223"],
         summary="Public status page and incident communication",
         narrative="As a customer, I want to know when the service is degraded, so that I do "
                   "not waste time diagnosing a problem that is not mine.",
         ac=["Public status page reflecting real health checks, not manual updates alone.",
             "Incident communication template and escalation path documented.",
             "Subscribers receive updates on incident open, update and resolution.",
             "Post-incident reviews are published to affected customers within the agreed window."]),
]

# --------------------------------------------------------------------------------------
# EPIC-24 — Frontend Product Application
# --------------------------------------------------------------------------------------

STORIES += [
    dict(key="LS-240", epic="EPIC-24", type="Story", points=8, priority="P0", sprint="S2",
         component="Frontend", labels=["foundation"], depends=["LS-022"],
         summary="Frontend architecture decision and application shell",
         narrative="As a frontend engineer, I want the framework, routing, auth and i18n "
                   "settled once, so that feature work does not relitigate the basics.",
         ac=["Framework decision recorded as an ADR with reasoning.",
             "App shell provides routing, authenticated session handling with token refresh, error boundaries and a loading strategy.",
             "Internationalisation scaffolding supports English, Hindi and Marathi from the first screen.",
             "Build, lint, type-check and test run in CI alongside the backend."]),
    dict(key="LS-241", epic="EPIC-24", type="Story", points=5, priority="P0", sprint="S2",
         component="Frontend", labels=["design-system"], depends=["LS-240"],
         summary="Design system extracted from the demo prototype",
         narrative="As a team, we want the prototype's visual language preserved in reusable "
                   "components, so that the product looks like the demo customers approved.",
         ac=["Tokens for colour, spacing, typography and elevation extracted from the prototype CSS.",
             "Core components built: cards, tables, timeline, chat blocks, trust badges, drawers, toasts, wizard.",
             "Trust badges render directly from the wire-format label, never from a client-side decision.",
             "Components are documented and visually reviewed against the prototype screenshots."]),
    dict(key="LS-242", epic="EPIC-24", type="Story", points=8, priority="P0", sprint="S7",
         component="Frontend", labels=["dashboard"], depends=["LS-241", "LS-106"],
         summary="Plant dashboard with KPIs, charts and insight cards",
         narrative="As a maintenance manager, I want one screen showing my plant's health, "
                   "so that my morning check takes two minutes.",
         ac=["Renders KPIs, trend chart, failure Pareto, top machines and open counts from the composite endpoint.",
             "Insight cards display detected patterns with their trust labels.",
             "Loading, empty and error states are designed rather than default.",
             "Numbers match the API exactly; the frontend performs no arithmetic of its own."]),
    dict(key="LS-243", epic="EPIC-24", type="Story", points=8, priority="P0", sprint="S7",
         component="Frontend", labels=["machines"], depends=["LS-241", "LS-044"],
         summary="Machine master and machine detail with timeline and View Source",
         narrative="As an engineer, I want a machine's full story on one page, so that "
                   "investigating a breakdown starts with context.",
         ac=["Machine list with search, filters and pagination.",
             "Detail page shows statistics, failure Pareto, parts consumed and a chronological timeline.",
             "Every timeline entry opens a source drawer with the original raw text, file, sheet and row.",
             "Raw source text is never translated, even when the UI language is Hindi or Marathi."]),
    dict(key="LS-244", epic="EPIC-24", type="Story", points=8, priority="P0", sprint="S5",
         component="Frontend", labels=["import"], depends=["LS-241", "LS-055", "LS-057"],
         summary="Import wizard with live pipeline progress",
         narrative="As an engineer importing three years of history, I want to see what is "
                   "happening, so that a long run feels controlled rather than frozen.",
         ac=["Drag-and-drop upload with client-side type and size validation before transfer.",
             "Preview step shows detected sheets, headers and sample rows before commitment.",
             "Column mapping step presents an auto-suggested mapping with per-column confidence and allows editing; the Intake Agent's proposal (LS-065) populates this same step once it lands.",
             "Live progress through each pipeline stage with counts for detected, usable, skipped and needs-review.",
             "Completion summary links directly to the validation queue and to the skipped-row export."]),
    dict(key="LS-245", epic="EPIC-24", type="Story", points=8, priority="P0", sprint="S6",
         component="Frontend", labels=["validation"], depends=["LS-241", "LS-083"],
         summary="Validation workbench UI",
         narrative="As a reviewer, I want an efficient review screen, so that clearing the "
                   "queue is a short focused task.",
         ac=["Split-screen showing raw source beside the extraction, with low-confidence fields highlighted.",
             "Alias-group bulk mapping shows the affected row count and a preview before committing.",
             "Keyboard shortcuts per LS-087 with an in-app help overlay.",
             "Conflict when another reviewer resolved an item is handled gracefully, never as a raw error."]),
    dict(key="LS-246", epic="EPIC-24", type="Story", points=8, priority="P0", sprint="S10",
         component="Frontend", labels=["assistant"], depends=["LS-241", "LS-123", "LS-124"],
         summary="Assistant UI with labelled blocks, citations and trace access",
         narrative="As a user, I want answers I can interrogate, so that trust comes from "
                   "verification rather than from presentation.",
         ac=["Blocks render with trust badges driven by the wire-format label.",
             "Citations are clickable and open the source drawer.",
             "A trace toggle reveals which tools ran with what arguments, for engineers and above.",
             "Degraded and partial-answer states are rendered honestly with an explanation.",
             "Supports questions and answers in English, Hindi, Marathi and Hinglish."]),
    dict(key="LS-247", epic="EPIC-24", type="Story", points=8, priority="P1", sprint="S11",
         component="Frontend", labels=["governance"], depends=["LS-241", "LS-191", "LS-118"],
         summary="Approval inbox and agent trace viewer UI",
         narrative="As an engineer, I want to review agent proposals with their full "
                   "reasoning, so that approving something is an informed decision.",
         ac=["Inbox lists pending proposals with type, agent, confidence, risk and age.",
             "Each proposal shows its evidence and a link to the full agent trace.",
             "Trace viewer renders steps chronologically with tools, arguments, results, timings and cost.",
             "Approve, reject and revert are available inline with reason capture."]),
    dict(key="LS-248", epic="EPIC-24", type="Story", points=5, priority="P0", sprint="S10",
         component="Frontend", labels=["i18n"], depends=["LS-240"],
         summary="Multilingual UI across English, Hindi and Marathi",
         narrative="As a shop-floor user, I want the whole interface in my language, so that "
                   "the product is usable by the people who generate the data.",
         ac=["Every screen, badge, empty state and error message is translated across all three languages.",
             "Language is switchable from the login screen and from the top bar, and persists per user.",
             "Numbers, dates and units are formatted per locale while the underlying values stay identical.",
             "Raw log entries and machine codes are never translated."]),
    dict(key="LS-249", epic="EPIC-24", type="Story", points=5, priority="P1", sprint="S13",
         component="Frontend", labels=["accessibility"], depends=["LS-242", "LS-243", "LS-246"],
         summary="Accessibility and responsive pass",
         narrative="As a user on a tablet on the shop floor, I want the product to work on "
                   "my device, so that it is usable away from a desk.",
         ac=["WCAG 2.1 AA conformance for contrast, focus order, keyboard navigation and screen-reader labelling.",
             "Responsive layouts verified on phone, tablet and desktop breakpoints.",
             "Charts carry accessible text alternatives conveying the same information.",
             "Automated accessibility checks run in CI with manual verification of the primary flows."]),
]

# --------------------------------------------------------------------------------------
# Derived indexes and validation
# --------------------------------------------------------------------------------------

EPIC_BY_KEY = {e["key"]: e for e in EPICS}
STORY_BY_KEY = {s["key"]: s for s in STORIES}
RELEASE_BY_KEY = {r["key"]: r for r in RELEASES}
SPRINT_TO_RELEASE = {sp: r["key"] for r in RELEASES for sp in r["sprints"]}

PRIORITY_LABEL = {
    "P0": "P0 · Must",
    "P1": "P1 · Should",
    "P2": "P2 · Could",
}


def validate() -> list[str]:
    """Return a list of problems. Empty means the backlog is internally consistent."""
    problems: list[str] = []

    dupes = [k for k, n in Counter(s["key"] for s in STORIES).items() if n > 1]
    for key in sorted(dupes):
        problems.append(f"duplicate story key: {key}")

    for s in STORIES:
        if s["epic"] not in EPIC_BY_KEY:
            problems.append(f"{s['key']}: unknown epic {s['epic']}")
        if s["sprint"] not in SPRINT_TO_RELEASE:
            problems.append(f"{s['key']}: unknown sprint {s['sprint']}")
        if s["priority"] not in PRIORITY_LABEL:
            problems.append(f"{s['key']}: unknown priority {s['priority']}")
        if not s.get("ac"):
            problems.append(f"{s['key']}: no acceptance criteria")
        for dep in s["depends"]:
            if dep not in STORY_BY_KEY:
                problems.append(f"{s['key']}: depends on unknown story {dep}")
                continue
            dep_sprint = STORY_BY_KEY[dep]["sprint"]
            if SPRINT_ORDER.index(dep_sprint) > SPRINT_ORDER.index(s["sprint"]):
                problems.append(
                    f"{s['key']} (sprint {s['sprint']}) depends on {dep} "
                    f"scheduled later in {dep_sprint}"
                )
    return problems


def blocked_by_map() -> dict[str, list[str]]:
    blocks: dict[str, list[str]] = defaultdict(list)
    for s in STORIES:
        for dep in s["depends"]:
            blocks[dep].append(s["key"])
    return blocks


# --------------------------------------------------------------------------------------
# Markdown rendering
# --------------------------------------------------------------------------------------

def _points(stories) -> int:
    return sum(s["points"] for s in stories)


def render_markdown() -> str:
    out: list[str] = []
    w = out.append
    blocks = blocked_by_map()

    w("# 02 — Delivery Backlog")
    w("")
    w("> **Generated file — do not edit by hand.**  ")
    w("> Source of truth: [`tools/backlog.py`](../tools/backlog.py). "
      "Regenerate with `python3 tools/backlog.py`.  ")
    w("> Jira/Linear import: [`backlog/logsense-jira-import.csv`]"
      "(../backlog/logsense-jira-import.csv)")
    w("")
    w(f"**{len(STORIES)} stories · {len(EPICS)} epics · {_points(STORIES)} points · "
      f"{len(RELEASES)} releases · {len(SPRINT_ORDER)} sprints**")
    w("")
    w("Work the board top to bottom. Every story states who it is for, why it exists, and "
      "the acceptance criteria that close it. A story is not done until every criterion is "
      "demonstrably true — see [`04-WAYS-OF-WORKING.md`](04-WAYS-OF-WORKING.md).")
    w("")

    # ---- legend -----------------------------------------------------------------------
    w("## How to read this")
    w("")
    w("| Field | Meaning |")
    w("|---|---|")
    w("| **Type** | `Story` (user-visible change) · `Task` (engineering work) · "
      "`Spike` (time-boxed investigation) · `Chore` (hygiene) |")
    w("| **Priority** | `P0` cannot ship the release without it · `P1` should be in the "
      "release · `P2` cut first when time runs short |")
    w("| **Points** | Modified Fibonacci (1, 2, 3, 5, 8, 13). 13 means *split it before "
      "starting* unless it is a genuinely indivisible research effort |")
    w("| **Depends on** | Hard dependency. The board enforces that a dependency is never "
      "scheduled after its dependant |")
    w("| **Blocks** | Stories that cannot start until this one is done |")
    w("")

    # ---- release summary --------------------------------------------------------------
    w("## Releases")
    w("")
    w("| Release | Theme | Sprints | Stories | Points | Goal |")
    w("|---|---|---|---:|---:|---|")
    for r in RELEASES:
        rs = [s for s in STORIES if SPRINT_TO_RELEASE[s["sprint"]] == r["key"]]
        w(f"| **{r['key']}** | {r['name']} | {', '.join(r['sprints'])} | {len(rs)} | "
          f"{_points(rs)} | {r['goal']} |")
    w("")
    for r in RELEASES:
        w(f"### {r['key']} — {r['name']}: exit criteria")
        w("")
        for c in r["exit_criteria"]:
            w(f"- {c}")
        w("")

    # ---- epic summary -----------------------------------------------------------------
    w("## Epics")
    w("")
    w("| Epic | Name | Component | Stories | Points | Goal |")
    w("|---|---|---|---:|---:|---|")
    for e in EPICS:
        es = [s for s in STORIES if s["epic"] == e["key"]]
        w(f"| `{e['key']}` | {e['name']} | {e['component']} | {len(es)} | "
          f"{_points(es)} | {e['goal']} |")
    w("")

    # ---- sprint plan ------------------------------------------------------------------
    w("## Sprint plan")
    w("")
    w("Two-week sprints. Point totals assume a small team; rebalance against your own "
      "measured velocity after the first two sprints rather than trusting these numbers.")
    w("")
    w("| Sprint | Release | Stories | Points | Focus |")
    w("|---|---|---:|---:|---|")
    for sp in SPRINT_ORDER:
        ss = [s for s in STORIES if s["sprint"] == sp]
        if not ss:
            continue
        top_epics = Counter(s["epic"] for s in ss).most_common(3)
        focus = ", ".join(EPIC_BY_KEY[k]["name"] for k, _ in top_epics)
        w(f"| **{sp}** | {SPRINT_TO_RELEASE[sp]} | {len(ss)} | {_points(ss)} | {focus} |")
    w("")

    # ---- component summary ------------------------------------------------------------
    w("## Effort by component")
    w("")
    w("| Component | Stories | Points | Share |")
    w("|---|---:|---:|---:|")
    total = _points(STORIES)
    by_comp = defaultdict(list)
    for s in STORIES:
        by_comp[s["component"]].append(s)
    for comp in sorted(by_comp, key=lambda c: -_points(by_comp[c])):
        cs = by_comp[comp]
        w(f"| {comp} | {len(cs)} | {_points(cs)} | {_points(cs) * 100 // total}% |")
    w("")

    # ---- the stories ------------------------------------------------------------------
    w("---")
    w("")
    w("# The backlog")
    w("")
    for r in RELEASES:
        rs = [s for s in STORIES if SPRINT_TO_RELEASE[s["sprint"]] == r["key"]]
        w(f"## {r['key']} — {r['name']}")
        w("")
        w(f"*{r['goal']}*")
        w("")
        epics_here = [e for e in EPICS if any(s["epic"] == e["key"] for s in rs)]
        for e in epics_here:
            es = sorted(
                [s for s in rs if s["epic"] == e["key"]],
                key=lambda s: (SPRINT_ORDER.index(s["sprint"]), s["key"]),
            )
            w(f"### {e['key']} — {e['name']}")
            w("")
            w(f"**Goal:** {e['goal']}  ")
            w(f"**Component:** {e['component']} · **In this release:** {len(es)} stories, "
              f"{_points(es)} points")
            w("")
            for s in es:
                dep = ", ".join(f"`{d}`" for d in s["depends"]) if s["depends"] else "—"
                blk = ", ".join(f"`{b}`" for b in blocks.get(s["key"], [])) or "—"
                w(f"#### `{s['key']}` · {s['summary']}")
                w("")
                w(f"`{s['type']}` · **{PRIORITY_LABEL[s['priority']]}** · "
                  f"**{s['points']} pts** · Sprint **{s['sprint']}** · "
                  f"{s['component']} · {' '.join('`' + l + '`' for l in s['labels'])}")
                w("")
                w(f"> {s['narrative']}")
                w("")
                w("**Acceptance criteria**")
                w("")
                for a in s["ac"]:
                    w(f"- [ ] {a}")
                w("")
                w(f"*Depends on:* {dep} · *Blocks:* {blk}")
                w("")
        w("---")
        w("")

    # ---- critical path ----------------------------------------------------------------
    w("# Critical path")
    w("")
    w("The stories with the most downstream dependants. Slipping one of these slips a lot "
      "of other work, so they are the ones to protect, pair on, and never leave half-done.")
    w("")
    w("| Story | Summary | Sprint | Directly blocks |")
    w("|---|---|---|---:|")
    ranked = sorted(STORIES, key=lambda s: (-len(blocks.get(s["key"], [])), s["key"]))
    for s in ranked[:15]:
        n = len(blocks.get(s["key"], []))
        if n == 0:
            break
        w(f"| `{s['key']}` | {s['summary']} | {s['sprint']} | {n} |")
    w("")
    w("## Stories with no dependencies (safe parallel starts)")
    w("")
    free = [s for s in STORIES if not s["depends"]]
    w(", ".join(f"`{s['key']}`" for s in sorted(free, key=lambda s: s["key"])))
    w("")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------------------
# CSV rendering
# --------------------------------------------------------------------------------------

CSV_COLUMNS = [
    "Issue Type", "Issue Key", "Summary", "Description", "Acceptance Criteria",
    "Epic Key", "Epic Name", "Priority", "Story Points", "Sprint", "Release",
    "Component", "Labels", "Depends On", "Blocks",
]


def render_rows() -> list[dict]:
    blocks = blocked_by_map()
    rows: list[dict] = []

    for e in EPICS:
        es = [s for s in STORIES if s["epic"] == e["key"]]
        rows.append({
            "Issue Type": "Epic",
            "Issue Key": e["key"],
            "Summary": e["name"],
            "Description": e["goal"],
            "Acceptance Criteria": "",
            "Epic Key": "",
            "Epic Name": e["name"],
            "Priority": "P0",
            "Story Points": _points(es),
            "Sprint": "",
            "Release": e["release"],
            "Component": e["component"],
            "Labels": "epic",
            "Depends On": "",
            "Blocks": "",
        })

    for s in sorted(STORIES, key=lambda s: (SPRINT_ORDER.index(s["sprint"]), s["key"])):
        e = EPIC_BY_KEY[s["epic"]]
        rows.append({
            "Issue Type": s["type"],
            "Issue Key": s["key"],
            "Summary": s["summary"],
            "Description": s["narrative"],
            "Acceptance Criteria": "\n".join(f"- {a}" for a in s["ac"]),
            "Epic Key": s["epic"],
            "Epic Name": e["name"],
            "Priority": s["priority"],
            "Story Points": s["points"],
            "Sprint": s["sprint"],
            "Release": SPRINT_TO_RELEASE[s["sprint"]],
            "Component": s["component"],
            "Labels": " ".join(s["labels"]),
            "Depends On": " ".join(s["depends"]),
            "Blocks": " ".join(blocks.get(s["key"], [])),
        })
    return rows


def main() -> int:
    problems = validate()
    if problems:
        print("Backlog validation FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    if "--check" in sys.argv:
        print(f"OK: {len(STORIES)} stories, {len(EPICS)} epics, "
              f"{_points(STORIES)} points, no problems found.")
        return 0

    md_path = ROOT / "docs" / "02-BACKLOG.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_markdown(), encoding="utf-8")

    csv_path = ROOT / "backlog" / "logsense-jira-import.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(render_rows())

    print(f"wrote {md_path.relative_to(ROOT)}")
    print(f"wrote {csv_path.relative_to(ROOT)}")
    print(f"{len(STORIES)} stories · {len(EPICS)} epics · {_points(STORIES)} points")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
