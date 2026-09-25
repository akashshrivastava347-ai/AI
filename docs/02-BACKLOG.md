# 02 — Delivery Backlog

> **Generated file — do not edit by hand.**  
> Source of truth: [`tools/backlog.py`](../tools/backlog.py). Regenerate with `python3 tools/backlog.py`.  
> Jira/Linear import: [`backlog/logsense-jira-import.csv`](../backlog/logsense-jira-import.csv)

**199 stories · 25 epics · 1021 points · 5 releases · 16 sprints**

Work the board top to bottom. Every story states who it is for, why it exists, and the acceptance criteria that close it. A story is not done until every criterion is demonstrably true — see [`04-WAYS-OF-WORKING.md`](04-WAYS-OF-WORKING.md).

## How to read this

| Field | Meaning |
|---|---|
| **Type** | `Story` (user-visible change) · `Task` (engineering work) · `Spike` (time-boxed investigation) · `Chore` (hygiene) |
| **Priority** | `P0` cannot ship the release without it · `P1` should be in the release · `P2` cut first when time runs short |
| **Points** | Modified Fibonacci (1, 2, 3, 5, 8, 13). 13 means *split it before starting* unless it is a genuinely indivisible research effort |
| **Depends on** | Hard dependency. The board enforces that a dependency is never scheduled after its dependant |
| **Blocks** | Stories that cannot start until this one is done |

## Releases

| Release | Theme | Sprints | Stories | Points | Goal |
|---|---|---|---:|---:|---|
| **R0** | Validation & Foundation | S0, S1 | 25 | 99 | Prove somebody will pay before writing the expensive parts; stand up the platform, tenancy and CI that everything else assumes. |
| **R1** | The Pilot Slice | S2, S3, S4, S5 | 45 | 218 | Take one real customer file from upload to searchable, validated records — and measure the auto-approval rate the whole business model rests on. |
| **R2** | Intelligence | S6, S7, S8, S9 | 51 | 278 | Make the plant's history answerable. Search, deterministic analytics, the agent runtime, the Reliability Copilot, and the guardrails and evals that make its output trustworthy. |
| **R3** | Proactive & Field | S10, S11, S12 | 36 | 202 | Stop waiting to be asked. Watchtower briefings, generative work artifacts, the WhatsApp field agent and the approval inbox that governs every agent write. |
| **R4** | Industry Hardening | S13, S14, S15 | 42 | 224 | Make it sellable to a second and third plant without heroics: compliant, observable, metered, recoverable and penetration-tested. |

### R0 — Validation & Foundation: exit criteria

- At least one paid design partner signed with a written pilot SOW.
- Three real (anonymised) maintenance files in hand and manually audited.
- App boots from one compose command; CI green with coverage and ArchUnit gates.
- Multi-tenant isolation proven by an automated cross-tenant test suite.

### R1 — The Pilot Slice: exit criteria

- A design partner's real file imports end-to-end without engineering intervention.
- Auto-approval rate measured on real data and reported to the customer.
- Alias bulk-mapping demonstrably maps a 30+ record group in one action.
- Every record traceable to its original file, sheet and row.

### R2 — Intelligence: exit criteria

- Copilot answers the six benchmark questions with correct numbers and citations.
- Answer numeric accuracy is 100% on the golden set; CI blocks regressions.
- Agent runs are fully traced, budgeted and replayable.
- Degraded mode verified by killing the LLM provider in staging.

### R3 — Proactive & Field: exit criteria

- Daily briefing delivered to a real plant for 14 consecutive days.
- An engineer approves an agent-drafted RCA and exports it with citations intact.
- Technicians create records via WhatsApp without training beyond one demo.
- No agent write reaches the database without a recorded human approval.

### R4 — Industry Hardening: exit criteria

- Third-party penetration test passed with all high findings remediated.
- DPDP obligations implemented; sub-processor register and DPA ready for signature.
- SLOs defined with alerting; a restore drill executed end-to-end.
- Cost per plant per month measured and inside the pricing model.

## Epics

| Epic | Name | Component | Stories | Points | Goal |
|---|---|---|---:|---:|---|
| `EPIC-00` | Discovery & Design-Partner Validation | GTM | 8 | 32 | Find out whether anyone will pay, before the expensive engineering starts. |
| `EPIC-01` | Platform Foundation & Developer Experience | Platform | 10 | 31 | A boring, fast, well-instrumented base every other epic builds on. |
| `EPIC-02` | Identity, Tenancy & Access Control | Security | 9 | 49 | Multi-tenant isolation and per-plant RBAC that is proven, not assumed. |
| `EPIC-03` | Plant, Asset & Taxonomy Master Data | Domain | 7 | 27 | The asset hierarchy and vocabulary every record resolves against. |
| `EPIC-04` | Maintenance Record Core & Provenance | Domain | 7 | 26 | The system of record, with an immutable chain back to the original raw row. |
| `EPIC-05` | Ingestion Pipeline | Ingestion | 9 | 45 | Files in any shape become verbatim raw records, safely and resumably. |
| `EPIC-06` | Generative Extraction & Normalisation | AI | 8 | 44 | Turn Hinglish shorthand into structured fields with calibrated confidence. |
| `EPIC-07` | Entity Resolution & Alias Learning | AI | 7 | 34 | "Conv Motor-3" resolves to a real asset, and the system never asks twice. |
| `EPIC-08` | Human-in-the-Loop Validation Workbench | Product | 8 | 35 | Make reviewing 200 uncertain rows a 20-minute job, not a 2-day job. |
| `EPIC-09` | Hybrid Search & Retrieval | AI | 7 | 34 | Find the right records from shorthand, Hindi, Marathi or English. |
| `EPIC-10` | Deterministic Analytics & KPI Engine | Domain | 7 | 31 | Every number in the product, computed in SQL and reproducible forever. |
| `EPIC-11` | Agent Runtime & Tool Platform | AI-Platform | 10 | 59 | The planner, tool registry, budgets, memory and traces all agents share. |
| `EPIC-12` | Reliability Copilot | AI | 8 | 44 | Multi-step investigation that answers 'why does this keep happening?'. |
| `EPIC-13` | Trust, Guardrails & Verification | AI-Safety | 7 | 32 | Structurally prevent the product from ever stating an ungrounded number. |
| `EPIC-14` | AI Evaluation & Quality Harness | AI-Quality | 8 | 49 | Know whether a prompt change made the product better or worse, before shipping. |
| `EPIC-15` | Pattern Detection & Watchtower Agent | AI | 10 | 52 | The product stops waiting to be asked and starts bringing findings to people. |
| `EPIC-16` | Generative Work Artifacts | Product | 7 | 47 | Draft the documents engineers hate writing, with citations intact. |
| `EPIC-17` | WhatsApp Field Agent | Integrations | 8 | 44 | Capture new records where technicians already are, in the language they use. |
| `EPIC-18` | Plant Knowledge Base | AI | 6 | 37 | Ground answers in manuals, SOPs and past RCAs, not only in log rows. |
| `EPIC-19` | Proposal & Approval Inbox | Product | 6 | 29 | The governed write path: agents propose, named humans dispose, everything reverts. |
| `EPIC-20` | AI Observability, Cost & FinOps | Platform | 8 | 40 | Know the quality, latency and rupee cost of every agent run and every tenant. |
| `EPIC-21` | Security, Privacy & Compliance | Security | 9 | 53 | Survive a plant IT head's security review and India's DPDP Act. |
| `EPIC-22` | Reliability, SRE & Deployment | Platform | 8 | 42 | Ship safely, stay up, and be able to prove you can restore from backup. |
| `EPIC-23` | Commercialization & Onboarding | GTM | 7 | 34 | Meter it, bill it, and onboard plant number three without a founder present. |
| `EPIC-24` | Frontend Product Application | Frontend | 10 | 71 | Turn the demo prototype into the real multilingual product UI. |

## Sprint plan

Two-week sprints. Point totals assume a small team; rebalance against your own measured velocity after the first two sprints rather than trusting these numbers.

| Sprint | Release | Stories | Points | Focus |
|---|---|---:|---:|---|
| **S0** | R0 | 11 | 36 | Platform Foundation & Developer Experience, Discovery & Design-Partner Validation |
| **S1** | R0 | 14 | 63 | Identity, Tenancy & Access Control, Platform Foundation & Developer Experience, Discovery & Design-Partner Validation |
| **S2** | R1 | 10 | 45 | Plant, Asset & Taxonomy Master Data, Maintenance Record Core & Provenance, Frontend Product Application |
| **S3** | R1 | 9 | 34 | Maintenance Record Core & Provenance, Ingestion Pipeline, Plant, Asset & Taxonomy Master Data |
| **S4** | R1 | 12 | 66 | Ingestion Pipeline, Generative Extraction & Normalisation, Entity Resolution & Alias Learning |
| **S5** | R1 | 14 | 73 | Entity Resolution & Alias Learning, Human-in-the-Loop Validation Workbench, Generative Extraction & Normalisation |
| **S6** | R2 | 15 | 71 | Hybrid Search & Retrieval, Human-in-the-Loop Validation Workbench, Deterministic Analytics & KPI Engine |
| **S7** | R2 | 15 | 86 | Agent Runtime & Tool Platform, Deterministic Analytics & KPI Engine, Frontend Product Application |
| **S8** | R2 | 11 | 67 | Reliability Copilot, Trust, Guardrails & Verification, Agent Runtime & Tool Platform |
| **S9** | R2 | 10 | 54 | Agent Runtime & Tool Platform, Reliability Copilot, AI Evaluation & Quality Harness |
| **S10** | R3 | 14 | 66 | Pattern Detection & Watchtower Agent, Trust, Guardrails & Verification, Frontend Product Application |
| **S11** | R3 | 9 | 58 | Generative Work Artifacts, Proposal & Approval Inbox, Pattern Detection & Watchtower Agent |
| **S12** | R3 | 13 | 78 | WhatsApp Field Agent, Generative Work Artifacts, Plant Knowledge Base |
| **S13** | R4 | 15 | 77 | AI Observability, Cost & FinOps, Plant Knowledge Base, AI Evaluation & Quality Harness |
| **S14** | R4 | 12 | 63 | Security, Privacy & Compliance, Identity, Tenancy & Access Control, Reliability, SRE & Deployment |
| **S15** | R4 | 15 | 84 | Commercialization & Onboarding, Reliability, SRE & Deployment, Security, Privacy & Compliance |

## Effort by component

| Component | Stories | Points | Share |
|---|---:|---:|---:|
| AI | 46 | 245 | 23% |
| Platform | 26 | 113 | 11% |
| Product | 21 | 111 | 10% |
| Security | 18 | 102 | 9% |
| Domain | 21 | 84 | 8% |
| Frontend | 10 | 71 | 6% |
| GTM | 15 | 66 | 6% |
| AI-Platform | 10 | 59 | 5% |
| AI-Quality | 8 | 49 | 4% |
| Ingestion | 9 | 45 | 4% |
| Integrations | 8 | 44 | 4% |
| AI-Safety | 7 | 32 | 3% |

---

# The backlog

## R0 — Validation & Foundation

*Prove somebody will pay before writing the expensive parts; stand up the platform, tenancy and CI that everything else assumes.*

### EPIC-00 — Discovery & Design-Partner Validation

**Goal:** Find out whether anyone will pay, before the expensive engineering starts.  
**Component:** GTM · **In this release:** 8 stories, 32 points

#### `LS-001` · Run 15 structured discovery interviews with maintenance leaders

`Spike` · **P0 · Must** · **5 pts** · Sprint **S0** · GTM · `discovery` `founder-led`

> As a founder, I want evidence of who owns the pain and who signs the cheque, so that I do not build a product for a buyer who does not exist.

**Acceptance criteria**

- [ ] Interview guide asks about the last three breakdowns and how each was diagnosed — listen first, never pitch.
- [ ] At least 15 interviews completed across at least 8 distinct plants.
- [ ] Notes captured in one shared repository, tagged by pain, role and plant size.
- [ ] Written synthesis names the top three pains and, per plant, who signs a purchase order.
- [ ] Explicit kill/continue call recorded: if nobody will share a file or discuss a paid pilot, the wedge changes before any backend code is written.

*Depends on:* — · *Blocks:* `LS-002`, `LS-003`, `LS-007`

#### `LS-002` · Collect and manually audit three real historical maintenance files

`Spike` · **P0 · Must** · **5 pts** · Sprint **S0** · GTM · `discovery` `data-risk`

> As a founder, I want to know what real plant data actually looks like, so that the messy-data promise is tested before it is sold.

**Acceptance criteria**

- [ ] At least three real (anonymised) files obtained under NDA from different plants.
- [ ] 100 random rows per file extracted by hand into the target schema.
- [ ] Achievable per-field accuracy recorded per file (date, machine, failure mode, action, parts, downtime).
- [ ] Worst-case formats catalogued: merged cells, multi-sheet layouts, scanned registers, free-text-only columns.
- [ ] Findings feed the extraction golden set (LS-140) and the realistic auto-approval target.

*Depends on:* `LS-001` · *Blocks:* `LS-004`, `LS-140`, `LS-141`

#### `LS-003` · Define and price the four-week paid pilot offer

`Task` · **P0 · Must** · **3 pts** · Sprint **S0** · GTM · `pricing` `legal`

> As a founder, I want a repeatable written pilot offer, so that every sales conversation converges instead of being renegotiated from scratch.

**Acceptance criteria**

- [ ] One-page SOW covering success criteria, data scope, timeline, named champion, pilot fee and the annual price if it succeeds.
- [ ] Success criteria are objectively measurable (for example: ten real historical questions answered correctly with citations).
- [ ] Internal floor price agreed and documented; free pilots are explicitly excluded.
- [ ] Reviewed by a CA or lawyer for Indian contracting norms.

*Depends on:* `LS-001` · *Blocks:* `LS-004`, `LS-008`

#### `LS-005` · Clear the product name: trademark and domain search

`Task` · **P1 · Should** · **2 pts** · Sprint **S0** · GTM · `legal` `brand`

> As a founder, I want naming risk resolved before the name is on a contract, so that a rename after ten pilots never happens.

**Acceptance criteria**

- [ ] Indian trademark search completed in classes 9 and 42; conflicting marks listed.
- [ ] Primary domain and the obvious variants checked and secured.
- [ ] Go/no-go decision on the name recorded with reasoning; fallback name shortlisted.
- [ ] Company and IP assignment position documented for review with a lawyer.

*Depends on:* — · *Blocks:* —

#### `LS-006` · Draft NDA, data-processing terms and a one-page security FAQ

`Task` · **P0 · Must** · **3 pts** · Sprint **S0** · GTM · `legal` `security` `trust`

> As a plant IT head, I want clear answers about where my maintenance data goes, so that I can approve a pilot without a three-month review.

**Acceptance criteria**

- [ ] NDA and DPA drafted covering ownership, deletion or return on exit, and a no-training-on-customer-data commitment.
- [ ] LLM sub-processor disclosure written in plain language, including the zero-retention option.
- [ ] One-page security FAQ covers encryption, per-plant isolation, audit logs, backups and access control.
- [ ] DPDP Act 2023 consent and purpose language drafted for technician personal data.
- [ ] Reviewed by a lawyer before being sent to any prospect.

*Depends on:* — · *Blocks:* `LS-004`

#### `LS-004` · Sign the first paid design partner

`Story` · **P0 · Must** · **8 pts** · Sprint **S1** · GTM · `design-partner`

> As a founder, I want one plant paying for a pilot, so that the pain is proven with money rather than politeness.

**Acceptance criteria**

- [ ] Signed SOW and NDA with a named champion and an executive sponsor.
- [ ] Pilot fee invoiced and received — a free pilot does not satisfy this story.
- [ ] Historical data scope agreed, with a date for the first file handover.
- [ ] Pricing protection and case-study permission negotiated in exchange for design-partner status.

*Depends on:* `LS-002`, `LS-003`, `LS-006` · *Blocks:* —

#### `LS-007` · Competitive teardown against CMMS incumbents and general-purpose chatbots

`Spike` · **P1 · Should** · **3 pts** · Sprint **S1** · GTM · `positioning`

> As a founder, I want a sharp answer to 'why not UpKeep, or just ChatGPT?', so that the wedge holds up in a real sales meeting.

**Acceptance criteria**

- [ ] Teardown of at least five relevant players covering positioning, pricing and India presence.
- [ ] One-paragraph differentiated answer written for each of: an incumbent CMMS, a generic chatbot, and doing nothing.
- [ ] The 'do nothing / Excel and memory' competitor is treated as the primary one.
- [ ] Findings folded into the pitch and into docs/00-PRODUCT-VISION.md.

*Depends on:* `LS-001` · *Blocks:* —

#### `LS-008` · Define the north-star metric tree and the per-pilot scorecard

`Task` · **P0 · Must** · **3 pts** · Sprint **S1** · GTM · `metrics`

> As a founder, I want agreed leading indicators, so that a failing pilot is visible in week two rather than at renewal.

**Acceptance criteria**

- [ ] North-star metric selected and justified; supporting input metrics mapped beneath it.
- [ ] Pilot scorecard defines auto-approval %, corrections per 100 records, queue burn-down time, weekly active engineers, WhatsApp records per week and time-to-first-answer.
- [ ] Internal red lines set (for example: auto-approval below 85% after alias mapping is a product problem, not a sales problem).
- [ ] Scorecard template ready to be populated manually before LS-147 automates it.

*Depends on:* `LS-003` · *Blocks:* —

### EPIC-01 — Platform Foundation & Developer Experience

**Goal:** A boring, fast, well-instrumented base every other epic builds on.  
**Component:** Platform · **In this release:** 10 stories, 31 points

#### `LS-010` · Bootstrap the Spring Boot 3 / Java 21 modular-monolith skeleton

`Story` · **P0 · Must** · **3 pts** · Sprint **S0** · Platform · `foundation`

> As an engineer, I want a running application with enforced module boundaries, so that the monolith stays extractable later.

**Acceptance criteria**

- [ ] Spring Boot 3.x on Java 21 builds and boots with an actuator health endpoint.
- [ ] Package structure com.logsense.<module> created for every module in reference doc 02.
- [ ] Constructor injection, DTO-at-the-boundary and no-entity-serialization conventions documented.
- [ ] Application starts with no database present in a 'lite' profile for fast unit tests.

*Depends on:* — · *Blocks:* `LS-011`, `LS-013`, `LS-018`, `LS-060`

#### `LS-011` · One-command local dev stack via Docker Compose

`Story` · **P0 · Must** · **3 pts** · Sprint **S0** · Platform · `devex`

> As an engineer, I want the whole stack up with one command, so that onboarding is minutes rather than a day.

**Acceptance criteria**

- [ ] docker compose up starts PostgreSQL 16 with pgvector and pg_trgm, plus MinIO.
- [ ] Application connects to all services with zero manual configuration.
- [ ] Named volumes persist data across restarts; a documented reset command wipes them.
- [ ] README documents prerequisites and the full first-run sequence.

*Depends on:* `LS-010` · *Blocks:* `LS-012`, `LS-220`

#### `LS-012` · Flyway migrations with a forward-only policy

`Story` · **P0 · Must** · **2 pts** · Sprint **S0** · Platform · `database`

> As an engineer, I want schema changes versioned and forward-only, so that production schema drift is impossible.

**Acceptance criteria**

- [ ] Flyway wired with a documented V<n>__<description>.sql naming convention.
- [ ] ddl-auto is validate in every profile except the throwaway test profile.
- [ ] A CI lint rejects edits to already-applied migration files.
- [ ] Rollback policy documented: forward fixes only, never destructive down-migrations.

*Depends on:* `LS-011` · *Blocks:* `LS-015`, `LS-016`, `LS-020`, `LS-110`

#### `LS-013` · Standard error envelope, stable error codes and a traceId filter

`Story` · **P0 · Must** · **3 pts** · Sprint **S0** · Platform · `api-contract`

> As an API consumer, I want every failure to look the same, so that clients handle errors generically and support can trace any incident.

**Acceptance criteria**

- [ ] A single @RestControllerAdvice renders the error envelope from reference doc 17.
- [ ] Every response carries a traceId, propagated into logs and OpenTelemetry spans.
- [ ] Error codes are stable string constants, enumerated and documented.
- [ ] Contract tests assert the envelope shape for 400, 401, 403, 404, 409, 422, 424, 429 and 500.

*Depends on:* `LS-010` · *Blocks:* `LS-014`, `LS-015`, `LS-203`

#### `LS-014` · Uniform pagination, filtering and sorting kernel

`Story` · **P0 · Must** · **2 pts** · Sprint **S0** · Platform · `api-contract`

> As an API consumer, I want identical paging semantics everywhere, so that I write list-handling code once.

**Acceptance criteria**

- [ ] Shared page/size/sort request binding with server-side clamping of size.
- [ ] Consistent page response envelope with content, page, size, totalElements, totalPages.
- [ ] Sort fields are whitelisted per resource; an unknown field returns 400, never a 500.
- [ ] Deep-paging guard prevents unbounded offsets on million-row tables.

*Depends on:* `LS-013` · *Blocks:* `LS-017`

#### `LS-018` · CI pipeline with coverage and architecture gates

`Story` · **P0 · Must** · **5 pts** · Sprint **S0** · Platform · `ci` `quality`

> As an engineer, I want the build to enforce our standards, so that quality does not depend on reviewer memory.

**Acceptance criteria**

- [ ] CI runs build, unit tests, integration tests on Testcontainers, and static analysis on every PR.
- [ ] Coverage gate fails the build below the agreed line and branch thresholds.
- [ ] ArchUnit rules enforce module boundaries, no cross-module repository access, and no JPA entity on a controller signature.
- [ ] Full pipeline completes in under 20 minutes; failures annotate the PR.

*Depends on:* `LS-010` · *Blocks:* `LS-146`, `LS-215`

#### `LS-015` · Database-backed async job framework with pollable status

`Story` · **P0 · Must** · **5 pts** · Sprint **S1** · Platform · `async`

> As a user starting a long import, I want to poll progress, so that the UI shows real movement instead of a spinner.

**Acceptance criteria**

- [ ] jobs table with type, status, progress percentage, result reference and error detail.
- [ ] GET /api/v1/jobs/{id} returns live status; terminal states are immutable.
- [ ] Jobs survive an application restart and resume or fail cleanly, never hang in RUNNING.
- [ ] Worker concurrency is bounded and configurable; no Kafka or external broker is introduced.

*Depends on:* `LS-012`, `LS-013` · *Blocks:* `LS-050`, `LS-055`

#### `LS-016` · Append-only audit log service

`Story` · **P0 · Must** · **3 pts** · Sprint **S1** · Platform · `audit` `compliance`

> As a compliance reviewer, I want every consequential action recorded immutably, so that an audit can reconstruct who did what.

**Acceptance criteria**

- [ ] audit_logs table is append-only; UPDATE and DELETE are revoked at the database role level.
- [ ] Records actor, tenant, plant, action, entity type, entity id, before/after summary and timestamp.
- [ ] A single AuditService is the only write path; an ArchUnit rule forbids direct repository access.
- [ ] Audit writes participate in the caller's transaction so an action and its audit row commit together.

*Depends on:* `LS-012` · *Blocks:* `LS-190`, `LS-211`

#### `LS-017` · OpenAPI generation, Swagger UI and a spec-diff CI gate

`Story` · **P1 · Should** · **3 pts** · Sprint **S1** · Platform · `api-contract` `ci`

> As an API consumer, I want an accurate spec and advance warning of breaking changes, so that integrations do not break silently.

**Acceptance criteria**

- [ ] springdoc generates the spec; Swagger UI is enabled in dev and disabled in prod.
- [ ] The committed spec is regenerated in CI and a drift check fails the build.
- [ ] A breaking-change diff against the previous release fails the build unless an override label is applied.
- [ ] Every endpoint documents auth requirements, roles and error codes.

*Depends on:* `LS-014` · *Blocks:* —

#### `LS-019` · Architecture Decision Record process and repository documentation layout

`Chore` · **P2 · Could** · **2 pts** · Sprint **S1** · Platform · `docs`

> As a future engineer, I want decisions and their reasoning recorded, so that settled questions are not relitigated every quarter.

**Acceptance criteria**

- [ ] ADR template and numbered docs/adr/ directory established.
- [ ] Backfilled ADRs for: modular monolith, PostgreSQL with pgvector, agents-propose-humans-dispose, no fine-tuning on customer data.
- [ ] Contribution guide explains when an ADR is required.
- [ ] Documentation layout described in the repository README.

*Depends on:* — · *Blocks:* —

### EPIC-02 — Identity, Tenancy & Access Control

**Goal:** Multi-tenant isolation and per-plant RBAC that is proven, not assumed.  
**Component:** Security · **In this release:** 7 stories, 36 points

#### `LS-020` · Organisation/tenant model with tenant_id on every table

`Story` · **P0 · Must** · **5 pts** · Sprint **S1** · Security · `multi-tenancy`

> As a company selling to multiple plants, I want tenancy in the schema from the first migration, so that retrofitting it later never happens.

**Acceptance criteria**

- [ ] organisations table sits above plants; every business table carries a non-null tenant_id.
- [ ] A migration lint fails CI if a new table omits tenant_id without an explicit allowlist entry.
- [ ] Tenant context is resolved from the JWT and held in a request-scoped holder.
- [ ] Composite indexes lead with tenant_id on every hot query path.

*Depends on:* `LS-012` · *Blocks:* `LS-021`, `LS-022`, `LS-051`

#### `LS-021` · Enforce tenant isolation with row-level security and an automated cross-tenant suite

`Story` · **P0 · Must** · **8 pts** · Sprint **S1** · Security · `multi-tenancy` `security`

> As a plant IT head, I want proof that another customer cannot see my data, so that a security review does not stall the deal.

**Acceptance criteria**

- [ ] PostgreSQL row-level security policies applied to every tenant-scoped table.
- [ ] A Hibernate interceptor sets the tenant GUC on every connection checkout.
- [ ] An automated suite attempts cross-tenant reads and writes on every endpoint and expects 404, never 403 or an empty 200.
- [ ] A deliberately unscoped repository method fails the build via an ArchUnit rule.
- [ ] Test evidence is exportable as an artifact for customer security questionnaires.

*Depends on:* `LS-020` · *Blocks:* `LS-210`

#### `LS-022` · JWT access and refresh token lifecycle with rotation and revocation

`Story` · **P0 · Must** · **5 pts** · Sprint **S1** · Security · `auth`

> As a user, I want long sessions without long-lived credentials, so that a stolen token has a short blast radius.

**Acceptance criteria**

- [ ] Short-lived access token and long-lived refresh token with rotation on each use.
- [ ] Refresh-token reuse detection revokes the whole family and raises a security event.
- [ ] Logout, password change and deactivation all revoke outstanding tokens.
- [ ] JWT secret is required from the environment in prod; the app refuses to start without it.

*Depends on:* `LS-020` · *Blocks:* `LS-023`, `LS-026`, `LS-214`, `LS-240`

#### `LS-023` · User CRUD, invite flow and first-login password set

`Story` · **P0 · Must** · **5 pts** · Sprint **S1** · Security · `auth`

> As a plant admin, I want to invite my team by email, so that onboarding does not require me to share passwords.

**Acceptance criteria**

- [ ] Invite issues a single-use, time-limited token; the invitee sets their own password on first login.
- [ ] Password policy enforced with BCrypt hashing; passwords never appear in logs or audit payloads.
- [ ] Deactivation is soft: login is blocked, history and authorship are retained.
- [ ] Every user lifecycle action writes an audit row.

*Depends on:* `LS-022` · *Blocks:* `LS-024`, `LS-172`

#### `LS-024` · Per-plant role assignment and a central PlantAccessService

`Story` · **P0 · Must** · **5 pts** · Sprint **S1** · Security · `rbac`

> As a plant admin, I want roles granted per plant, so that a group engineer can see one plant without seeing all of them.

**Acceptance criteria**

- [ ] Five roles supported: SUPER_ADMIN (global), PLANT_ADMIN, ENGINEER, TECHNICIAN, VIEWER (per plant).
- [ ] A single PlantAccessService answers 'can user X act on plant Y as role Z' and is the only authority.
- [ ] Method-level authorization applied on every controller; a missing annotation fails an ArchUnit rule.
- [ ] Access to an out-of-scope plant returns 404 so plant existence cannot be probed.

*Depends on:* `LS-023` · *Blocks:* `LS-025`, `LS-027`, `LS-028`, `LS-030`, `LS-113`, `LS-184`

#### `LS-025` · Automated role-matrix authorization test suite

`Story` · **P0 · Must** · **5 pts** · Sprint **S1** · Security · `rbac` `testing`

> As a security reviewer, I want every endpoint tested against every role, so that an IDOR is caught by CI rather than by a customer.

**Acceptance criteria**

- [ ] A generated matrix exercises every endpoint against all five roles plus anonymous.
- [ ] Expected outcomes are declared per endpoint; an undeclared endpoint fails the suite.
- [ ] Ownership-scoped resources are probed with another user's identifier and expect 404.
- [ ] The suite runs on every PR and its report is attached to the build.

*Depends on:* `LS-024` · *Blocks:* `LS-217`

#### `LS-026` · Login rate limiting and brute-force lockout

`Story` · **P0 · Must** · **3 pts** · Sprint **S1** · Security · `auth` `hardening`

> As a security reviewer, I want credential stuffing to fail fast, so that exposed passwords elsewhere do not compromise this system.

**Acceptance criteria**

- [ ] Per-identity and per-IP rate limits on login, refresh and password-reset endpoints.
- [ ] Progressive backoff and temporary lockout after a configured failure count.
- [ ] Rate-limit responses use 429 with a Retry-After header and the standard envelope.
- [ ] Lockout and limit events are audited and alertable.

*Depends on:* `LS-022` · *Blocks:* —

---

## R1 — The Pilot Slice

*Take one real customer file from upload to searchable, validated records — and measure the auto-approval rate the whole business model rests on.*

### EPIC-03 — Plant, Asset & Taxonomy Master Data

**Goal:** The asset hierarchy and vocabulary every record resolves against.  
**Component:** Domain · **In this release:** 7 stories, 27 points

#### `LS-030` · Plant and line CRUD

`Story` · **P0 · Must** · **3 pts** · Sprint **S2** · Domain · `master-data`

> As a plant admin, I want to model my plant's lines, so that machines and analytics have a hierarchy to roll up into.

**Acceptance criteria**

- [ ] Plant CRUD restricted to SUPER_ADMIN; line CRUD available to PLANT_ADMIN.
- [ ] Lines carry kind PRODUCTION or UTILITY, covering the utilities group without an extra hierarchy level.
- [ ] Line names are unique within a plant; conflicts return 409.
- [ ] Deleting a line with machines is refused with a clear, actionable error.

*Depends on:* `LS-024` · *Blocks:* `LS-031`, `LS-032`, `LS-033`, `LS-034`

#### `LS-031` · Plant settings: shifts, operating hours, downtime cost and thresholds

`Story` · **P0 · Must** · **3 pts** · Sprint **S2** · Domain · `master-data` `config`

> As a maintenance manager, I want plant-specific parameters, so that KPIs and cost figures reflect my plant rather than a default.

**Acceptance criteria**

- [ ] Configurable shift definitions, operating hours per week, and downtime cost per line-hour in INR.
- [ ] Auto-approval confidence threshold configurable per plant with a documented default.
- [ ] Pattern detector thresholds (window months, minimum events) overridable per plant.
- [ ] Settings changes are audited with before and after values.

*Depends on:* `LS-030` · *Blocks:* `LS-234`

#### `LS-032` · Machine master CRUD with asset codes and criticality

`Story` · **P0 · Must** · **5 pts** · Sprint **S2** · Domain · `master-data`

> As a plant admin, I want every machine registered with its code, so that messy free text can be resolved to a real asset.

**Acceptance criteria**

- [ ] Machine carries name, asset code, line, type, criticality and commissioning date.
- [ ] Asset code is unique within a plant; conflicts return 409.
- [ ] Machines are searchable and paginated; a machine belongs to exactly one line.
- [ ] Deactivating a machine retains its history and excludes it from new resolution targets.

*Depends on:* `LS-030` · *Blocks:* `LS-035`, `LS-040`, `LS-070`

#### `LS-033` · Failure-mode taxonomy with plant-level extension

`Story` · **P0 · Must** · **3 pts** · Sprint **S2** · Domain · `taxonomy`

> As a reliability engineer, I want a controlled failure vocabulary, so that Pareto analysis groups the same failure consistently.

**Acceptance criteria**

- [ ] A seeded standard taxonomy ships with the product and is extensible per plant.
- [ ] Synonyms map to a canonical failure mode and are used by both extraction and search.
- [ ] Merging two failure modes re-points existing records and is audited.
- [ ] Taxonomy is exposed to the extraction prompt so the model chooses from a closed set.

*Depends on:* `LS-030` · *Blocks:* `LS-040`, `LS-074`

#### `LS-034` · Spare parts catalogue with codes, synonyms and unit cost

`Story` · **P0 · Must** · **3 pts** · Sprint **S2** · Domain · `taxonomy` `parts`

> As a maintenance manager, I want parts catalogued with the names people actually type, so that '6205ZZ' and '6205 ZZ' are one part.

**Acceptance criteria**

- [ ] Part carries code, description, unit cost, unit of measure and optional lead time.
- [ ] Synonym list per part feeds both extraction and search expansion.
- [ ] Part codes are unique per plant; a normalised form is indexed for fuzzy lookup.
- [ ] Catalogue is importable in bulk and exportable as CSV.

*Depends on:* `LS-030` · *Blocks:* `LS-035`, `LS-042`, `LS-074`

#### `LS-035` · Bulk master-data import via CSV template

`Story` · **P1 · Should** · **5 pts** · Sprint **S2** · Domain · `master-data` `onboarding`

> As a plant admin onboarding a new plant, I want to upload machines and parts in bulk, so that setup takes an hour rather than a week.

**Acceptance criteria**

- [ ] Downloadable CSV templates for machines and parts with inline column documentation.
- [ ] Dry-run validation reports every row error before anything is written.
- [ ] Import is transactional per file: either all valid rows commit, or nothing does, per the chosen mode.
- [ ] Re-importing an existing code updates rather than duplicating, and the change is audited.

*Depends on:* `LS-032`, `LS-034` · *Blocks:* `LS-036`, `LS-232`

#### `LS-036` · Asset hierarchy import from an existing CMMS export

`Story` · **P2 · Could** · **5 pts** · Sprint **S3** · Domain · `onboarding` `integrations`

> As a plant with SAP PM, I want my existing asset tree imported, so that I do not retype 400 machines that already exist.

**Acceptance criteria**

- [ ] Importer accepts common SAP PM and generic CMMS functional-location exports.
- [ ] Hierarchy is flattened to the plant/line/machine model with a reviewable mapping report.
- [ ] Unmappable levels are reported rather than silently dropped.
- [ ] Original export is retained as an immutable artifact for traceability.

*Depends on:* `LS-035` · *Blocks:* —

### EPIC-04 — Maintenance Record Core & Provenance

**Goal:** The system of record, with an immutable chain back to the original raw row.  
**Component:** Domain · **In this release:** 7 stories, 26 points

#### `LS-040` · Maintenance record entity, lifecycle and soft delete

`Story` · **P0 · Must** · **5 pts** · Sprint **S2** · Domain · `core`

> As the system, I need one canonical record type, so that search, analytics, patterns and AI all reason over the same thing.

**Acceptance criteria**

- [ ] Record carries date, machine, failure mode, action, downtime hours, technician, kind and source.
- [ ] Lifecycle ACTIVE to CORRECTED to DELETED (soft) is enforced by an explicit state machine.
- [ ] Deleted records are excluded from search, analytics and AI citations but retained in the database.
- [ ] Every state transition writes an audit row naming the actor.

*Depends on:* `LS-032`, `LS-033` · *Blocks:* `LS-041`, `LS-042`, `LS-044`, `LS-045`, `LS-090`

#### `LS-041` · Immutable raw-record provenance chain powering View Source

`Story` · **P0 · Must** · **5 pts** · Sprint **S2** · Domain · `core` `trust`

> As an engineer reading an AI answer, I want to see the original row, so that I can judge the extraction myself.

**Acceptance criteria**

- [ ] Every maintenance record links to a raw_record; the link is non-nullable.
- [ ] raw_records are append-only with a RESTRICT foreign key; normalization never overwrites raw text.
- [ ] Provenance exposes file name, sheet, row number and the verbatim original text, or the WhatsApp conversation reference.
- [ ] A record with no raw ancestor cannot be created — enforced by a database constraint, not only by service code.

*Depends on:* `LS-040` · *Blocks:* `LS-043`, `LS-046`, `LS-124`

#### `LS-042` · Record-parts join and downtime normalisation to hours

`Story` · **P0 · Must** · **3 pts** · Sprint **S3** · Domain · `core` `parts`

> As an analyst, I want parts and downtime in consistent units, so that totals across three years of mixed formats are meaningful.

**Acceptance criteria**

- [ ] Many-to-many record-to-part join with quantity.
- [ ] Downtime normalised to decimal hours from minutes, hours, shifts and phrases such as '2 ghante'.
- [ ] Unparseable downtime is stored as null and counted in coverage reporting rather than guessed.
- [ ] Unit conversion rules are unit-tested against the real-file fixtures from LS-002.

*Depends on:* `LS-040`, `LS-034` · *Blocks:* `LS-100`

#### `LS-043` · Manual record entry and audited correction with versioning

`Story` · **P0 · Must** · **5 pts** · Sprint **S3** · Domain · `core` `audit`

> As an engineer, I want to correct a wrong record without destroying history, so that the audit trail stays honest.

**Acceptance criteria**

- [ ] Manual entry creates a raw_record of kind MANUAL so the provenance invariant holds.
- [ ] Correction creates a new version; the prior version is retained and retrievable.
- [ ] Correction requires a reason; the diff, actor and reason are audited.
- [ ] Corrections trigger re-indexing and invalidate cached statistics for the affected machine.

*Depends on:* `LS-041` · *Blocks:* —

#### `LS-044` · Machine history endpoint with filters and pagination

`Story` · **P0 · Must** · **3 pts** · Sprint **S3** · Domain · `core` `api`

> As an engineer, I want a machine's full chronological history, so that I can see everything that ever happened to it.

**Acceptance criteria**

- [ ] Filterable by date range, failure mode, kind, part and technician.
- [ ] Sorted newest-first by default with a stable secondary sort for deterministic paging.
- [ ] Each entry exposes a provenance link for View Source.
- [ ] Response time stays within budget on a machine with 10,000 records.

*Depends on:* `LS-040` · *Blocks:* `LS-243`

#### `LS-045` · Domain events for record created and updated

`Story` · **P0 · Must** · **2 pts** · Sprint **S3** · Domain · `events`

> As a downstream module, I want to react to record changes, so that indexing, stats invalidation and pattern rescans stay current.

**Acceptance criteria**

- [ ] In-process Spring application events published on create, update and delete.
- [ ] Consumers include search indexing, machine-stats cache invalidation and targeted pattern rescan.
- [ ] Event handling failures are retried and never roll back the originating transaction.
- [ ] No external broker is introduced, per the documented V1 scope decision.

*Depends on:* `LS-040` · *Blocks:* `LS-073`

#### `LS-046` · Reference-plant seed data loader

`Story` · **P1 · Should** · **3 pts** · Sprint **S3** · Domain · `devex` `demo`

> As an engineer or a sales demo, I want a realistic populated plant in one command, so that development and demos do not need a real customer.

**Acceptance criteria**

- [ ] Loader builds the reference plant hierarchy, machines, parts and records from reference doc 25.
- [ ] Runs only under the dev and demo profiles and refuses to run against prod.
- [ ] Seeded data reproduces the prototype's headline numbers exactly.
- [ ] Loader is idempotent and has a documented reset path.

*Depends on:* `LS-041` · *Blocks:* —

### EPIC-05 — Ingestion Pipeline

**Goal:** Files in any shape become verbatim raw records, safely and resumably.  
**Component:** Ingestion · **In this release:** 9 stories, 45 points

#### `LS-050` · Secure file upload with type, size and magic-byte validation

`Story` · **P0 · Must** · **5 pts** · Sprint **S3** · Ingestion · `upload` `security`

> As a security reviewer, I want uploads validated by content rather than filename, so that a renamed executable cannot enter the system.

**Acceptance criteria**

- [ ] Accepts xlsx, xls, csv, pdf and common image formats; everything else is rejected with a clear error.
- [ ] Content type verified by magic bytes, not by extension or client-supplied header.
- [ ] Size cap enforced and configurable; oversize uploads fail before buffering the whole file.
- [ ] XML parsers are configured XXE-safe; a malicious xlsx fixture is covered by a regression test.

*Depends on:* `LS-015` · *Blocks:* `LS-051`, `LS-216`

#### `LS-051` · Immutable object storage client with tenant-prefixed keys

`Story` · **P0 · Must** · **3 pts** · Sprint **S3** · Ingestion · `storage`

> As a customer, I want my original files preserved and isolated, so that provenance survives and no other tenant can reach them.

**Acceptance criteria**

- [ ] Pluggable StorageClient port with S3-compatible and local implementations.
- [ ] Object keys are prefixed by tenant and plant; cross-tenant key construction is impossible by design.
- [ ] Stored objects are never mutated; re-processing reads the original bytes.
- [ ] Download is served through a short-lived signed URL, never a public bucket.

*Depends on:* `LS-050`, `LS-020` · *Blocks:* `LS-052`, `LS-180`

#### `LS-052` · XLSX and CSV parsers producing verbatim raw records

`Story` · **P0 · Must** · **5 pts** · Sprint **S3** · Ingestion · `parsing`

> As the system, I need every source row captured exactly as written, so that normalization can never destroy the evidence.

**Acceptance criteria**

- [ ] Multi-sheet workbooks parsed with sheet name and row number retained per raw record.
- [ ] Merged cells, blank rows and inconsistent column counts handled without aborting the file.
- [ ] Cell values stored as original text; no type coercion at the raw layer.
- [ ] Parser is streaming so a 100,000-row workbook does not exhaust heap.

*Depends on:* `LS-051` · *Blocks:* `LS-053`, `LS-055`, `LS-056`, `LS-057`, `LS-061`

#### `LS-053` · PDF text extraction parser

`Story` · **P1 · Should** · **5 pts** · Sprint **S4** · Ingestion · `parsing`

> As a plant whose history is in PDF reports, I want those ingested too, so that I do not have to retype three years of records.

**Acceptance criteria**

- [ ] Text-layer PDFs extracted with page number retained per raw record.
- [ ] Tabular layouts detected and split into rows where structure permits.
- [ ] PDFs with no text layer are routed to the OCR path rather than failing.
- [ ] Page-level provenance is exposed through View Source.

*Depends on:* `LS-052` · *Blocks:* `LS-054`, `LS-180`

#### `LS-054` · Scanned-register OCR parser

`Story` · **P1 · Should** · **8 pts** · Sprint **S4** · Ingestion · `parsing` `ocr`

> As a plant with handwritten logbooks, I want scans converted to records, so that the pre-digital years are searchable too.

**Acceptance criteria**

- [ ] Pluggable OCR provider port with at least one working implementation.
- [ ] Per-block OCR confidence retained and fed into overall extraction confidence.
- [ ] Low-confidence OCR output is routed to validation rather than auto-approved, regardless of extraction confidence.
- [ ] Original image is retained and shown side-by-side in the validation workbench.

*Depends on:* `LS-053` · *Blocks:* —

#### `LS-055` · Import job state machine with resume, cancel and retry

`Story` · **P0 · Must** · **8 pts** · Sprint **S4** · Ingestion · `pipeline`

> As an engineer importing 2,000 rows, I want the run to survive failures, so that one bad row or a provider timeout does not cost me the whole file.

**Acceptance criteria**

- [ ] States CREATED, PARSED, MAPPED, NORMALIZING, RESOLVED, COMPLETED, CANCELLED, FAILED with legal transitions enforced.
- [ ] Cancel stops further processing without rolling back rows already committed, and the state is clearly reported.
- [ ] Retry resumes from the last completed stage rather than restarting the file.
- [ ] An LLM provider outage pauses at NORMALIZING and resumes cleanly when the provider returns.

*Depends on:* `LS-052`, `LS-015` · *Blocks:* `LS-058`, `LS-067`, `LS-244`

#### `LS-056` · Duplicate file and duplicate row detection

`Story` · **P0 · Must** · **5 pts** · Sprint **S4** · Ingestion · `data-quality`

> As a maintenance manager, I want re-uploads to be caught, so that my downtime totals are not silently doubled.

**Acceptance criteria**

- [ ] File-level duplicate detected by content hash and returns 409 with a link to the earlier import.
- [ ] Row-level near-duplicate detection across imports flags candidates rather than auto-deleting.
- [ ] Flagged duplicates surface in the validation queue for a human decision.
- [ ] Deliberate re-import is possible through an explicit override that is audited.

*Depends on:* `LS-052` · *Blocks:* —

#### `LS-057` · Import preview API

`Story` · **P0 · Must** · **3 pts** · Sprint **S4** · Ingestion · `ux`

> As an engineer, I want to see what was detected before committing, so that I catch a wrong sheet before spending twenty minutes.

**Acceptance criteria**

- [ ] Returns detected sheets, inferred header row, column names and the first N rows.
- [ ] Preview runs without persisting raw records or consuming AI tokens.
- [ ] Detected encoding and delimiter are reported for CSV files.
- [ ] Preview response is fast enough to feel instant on a typical customer file.

*Depends on:* `LS-052` · *Blocks:* `LS-065`, `LS-244`

#### `LS-058` · Skipped-row registry with reasons and export

`Story` · **P0 · Must** · **3 pts** · Sprint **S4** · Ingestion · `data-quality` `trust`

> As a maintenance manager, I want to know exactly what was not imported and why, so that I can trust the totals I am shown.

**Acceptance criteria**

- [ ] Every skipped row is retained with a machine-readable reason code and human-readable explanation.
- [ ] Import summary reports detected, usable, skipped and needs-review counts that reconcile to the total.
- [ ] Skipped rows are exportable as CSV for the customer to review offline.
- [ ] Skipped rows can be reprocessed after the underlying cause is fixed.

*Depends on:* `LS-055` · *Blocks:* —

### EPIC-06 — Generative Extraction & Normalisation

**Goal:** Turn Hinglish shorthand into structured fields with calibrated confidence.  
**Component:** AI · **In this release:** 7 stories, 36 points

#### `LS-060` · Pluggable LlmClient port with retries, timeouts and a circuit breaker

`Story` · **P0 · Must** · **5 pts** · Sprint **S4** · AI · `llm` `platform`

> As an engineer, I want the model provider behind a port, so that an outage degrades the product instead of breaking it.

**Acceptance criteria**

- [ ] LlmClient interface with an Anthropic adapter as the default implementation.
- [ ] Configurable timeout, exponential-backoff retry and a circuit breaker with a half-open probe.
- [ ] Token usage, latency, model and cost are recorded for every call.
- [ ] A deterministic fake implementation backs tests so CI never calls a live provider.

*Depends on:* `LS-010` · *Blocks:* `LS-061`, `LS-091`, `LS-110`, `LS-115`, `LS-120`, `LS-170`, `LS-212`

#### `LS-061` · Schema-constrained extraction with per-field confidence

`Story` · **P0 · Must** · **8 pts** · Sprint **S4** · AI · `llm` `extraction`

> As the system, I need messy shorthand turned into structured fields with honest confidence, so that routing to review is based on real signal.

**Acceptance criteria**

- [ ] Extraction returns a strict JSON schema: date, machineText, failureMode, action, parts, downtimeHours, technician, kind.
- [ ] Every field carries its own confidence score; the model is instructed to return null rather than guess.
- [ ] Failure mode and part values are constrained to the plant's taxonomy where a confident match exists.
- [ ] Schema violations are rejected and retried once before the row is marked FAILED.
- [ ] Golden-set extraction F1 meets the threshold defined in LS-140.

*Depends on:* `LS-060`, `LS-052` · *Blocks:* `LS-062`, `LS-063`, `LS-064`, `LS-065`, `LS-067`, `LS-174`

#### `LS-062` · Batched extraction with prompt caching on the static prefix

`Story` · **P0 · Must** · **5 pts** · Sprint **S4** · AI · `llm` `cost`

> As the business, I want extraction cost per 1,000 rows to be predictable and low, so that unit economics survive a large historical import.

**Acceptance criteria**

- [ ] Rows batched at a configurable size (default approximately 20) per model call.
- [ ] The static prefix — schema, shorthand dictionary and plant context — is prompt-cached.
- [ ] Measured cost per 1,000 rows is recorded and reported per import.
- [ ] A partial batch failure retries only the failed rows, never the whole batch.

*Depends on:* `LS-061` · *Blocks:* —

#### `LS-063` · Hinglish and shorthand dictionary shared by extraction and search

`Story` · **P0 · Must** · **5 pts** · Sprint **S4** · AI · `hinglish` `moat`

> As a technician writing 'brng' and '2 ghante', I want the system to understand me, so that my notes are as valuable as a typed report.

**Acceptance criteria**

- [ ] Dictionary covers shorthand (brng, m/c, algnmnt), Hinglish units ('2 ghante'), and Devanagari and Marathi equivalents.
- [ ] The same dictionary is applied at extraction time and at search-expansion time so behaviour matches.
- [ ] Per-plant entries can be added without a code deployment.
- [ ] New entries are versioned and their effect is measurable on the extraction golden set.

*Depends on:* `LS-061` · *Blocks:* `LS-093`

#### `LS-064` · Confidence calibration and per-plant auto-approval routing

`Story` · **P0 · Must** · **5 pts** · Sprint **S5** · AI · `confidence` `routing`

> As a maintenance manager, I want only genuinely uncertain rows in my review queue, so that validation is worth my engineers' time.

**Acceptance criteria**

- [ ] Overall confidence combines model self-score, resolver score and field completeness by a documented formula.
- [ ] Rows at or above the plant threshold auto-approve; the rest create validation items.
- [ ] Calibration is measured against the golden set: reported confidence tracks observed accuracy.
- [ ] Auto-approval rate is recorded per import and per plant as a first-class product metric.

*Depends on:* `LS-061`, `LS-070` · *Blocks:* `LS-066`, `LS-080`, `LS-147`

#### `LS-066` · Extraction self-critique pass on mid-confidence rows

`Story` · **P1 · Should** · **5 pts** · Sprint **S5** · AI · `agent` `quality`

> As a reviewer, I want the queue to contain sharper questions, so that I spend my time on genuine ambiguity rather than on obvious rows.

**Acceptance criteria**

- [ ] Rows in the configurable mid-confidence band get a second pass that re-reads raw text against the extraction.
- [ ] The pass either raises confidence with a stated justification or names the specific ambiguous field.
- [ ] Reviewer-facing output shows which field is uncertain and why.
- [ ] Measured effect on reviewer time and on false auto-approvals is reported; the feature is reverted if accuracy drops.

*Depends on:* `LS-064` · *Blocks:* —

#### `LS-067` · Extraction failure handling, dead-letter and retry API

`Story` · **P0 · Must** · **3 pts** · Sprint **S5** · AI · `reliability`

> As an engineer, I want failed rows visible and retryable, so that a transient provider error does not silently lose data.

**Acceptance criteria**

- [ ] Rows failing twice are marked FAILED with the error reason retained.
- [ ] Failed rows are listable per import and retryable individually or in bulk.
- [ ] Retry reuses the original raw text; the raw record is never re-parsed or altered.
- [ ] Persistent failure rate is a monitored metric with an alert threshold.

*Depends on:* `LS-061`, `LS-055` · *Blocks:* —

### EPIC-07 — Entity Resolution & Alias Learning

**Goal:** "Conv Motor-3" resolves to a real asset, and the system never asks twice.  
**Component:** AI · **In this release:** 6 stories, 29 points

#### `LS-070` · MachineResolverService cascade: exact, alias, fuzzy, semantic

`Story` · **P0 · Must** · **8 pts** · Sprint **S4** · AI · `resolution` `moat`

> As the system, I need 'Conv Motor-3' to become a real asset id, so that messy text becomes analysable data.

**Acceptance criteria**

- [ ] Four-stage cascade: exact match, known alias, normalised-token fuzzy match, embedding similarity.
- [ ] Each stage returns candidates with calibrated confidence; the cascade stops at a confident match.
- [ ] The identical resolver is used by ingestion, search and the assistant — one code path, no divergence.
- [ ] Resolution is plant-scoped: a machine in another tenant is never a candidate.
- [ ] Precision@1 on the golden set meets the threshold in LS-141.

*Depends on:* `LS-032` · *Blocks:* `LS-064`, `LS-071`, `LS-075`, `LS-076`, `LS-120`, `LS-174`

#### `LS-071` · Machine alias store with provenance and confidence

`Story` · **P0 · Must** · **3 pts** · Sprint **S4** · AI · `resolution`

> As the system, I want learned aliases persisted with their origin, so that a bad alias can be traced and reversed.

**Acceptance criteria**

- [ ] Alias records text, machine, confidence, source (IMPORT, VALIDATION, MANUAL) and creating actor.
- [ ] Alias text is unique per plant; a conflicting alias returns 409 with the existing mapping.
- [ ] Aliases are listable, editable and deletable by a plant admin, with every change audited.
- [ ] Deleting an alias does not alter records already resolved through it.

*Depends on:* `LS-070` · *Blocks:* `LS-072`, `LS-116`

#### `LS-072` · Alias learning from validation corrections

`Story` · **P0 · Must** · **5 pts** · Sprint **S5** · AI · `resolution` `learning`

> As a reviewer, I want my correction to teach the system permanently, so that I never answer the same question twice.

**Acceptance criteria**

- [ ] Correcting a machine during validation creates or strengthens an alias automatically.
- [ ] The learned alias applies immediately to subsequent resolution without a restart.
- [ ] Learning is attributable: the alias records which validation action produced it.
- [ ] Measured effect: resolver hit rate on the next import of the same customer's data improves.

*Depends on:* `LS-071`, `LS-082` · *Blocks:* `LS-073`

#### `LS-073` · Re-resolution of pending rows when an alias is created

`Story` · **P0 · Must** · **5 pts** · Sprint **S5** · AI · `resolution` `learning`

> As a reviewer, I want one mapping to clear every matching row everywhere, so that the queue shrinks faster than I work.

**Acceptance criteria**

- [ ] Creating an alias publishes an event that re-resolves matching unresolved rows across all pending imports.
- [ ] Re-resolution is asynchronous, idempotent and reports how many rows it cleared.
- [ ] Already-approved records are not retroactively altered without an explicit, audited action.
- [ ] Re-resolution respects plant scope and never crosses tenants.

*Depends on:* `LS-072`, `LS-045` · *Blocks:* `LS-083`

#### `LS-074` · Part and failure-mode resolution with synonym learning

`Story` · **P1 · Should** · **5 pts** · Sprint **S5** · AI · `resolution` `parts`

> As an analyst, I want '6205ZZ', '6205 ZZ' and 'bearing 6205' treated as one part, so that consumption analysis is not fragmented.

**Acceptance criteria**

- [ ] Part resolution uses code normalisation, synonyms and fuzzy matching with confidence.
- [ ] Failure-mode resolution maps free text to the canonical taxonomy entry.
- [ ] Corrections during validation create synonyms, mirroring machine alias learning.
- [ ] Unresolvable parts are retained as free text on the record and reported, never silently dropped.

*Depends on:* `LS-034`, `LS-033` · *Blocks:* `LS-104`

#### `LS-075` · Resolver explain endpoint

`Story` · **P1 · Should** · **3 pts** · Sprint **S5** · AI · `resolution` `devex`

> As an engineer debugging a bad mapping, I want to see why the resolver chose what it chose, so that I can fix the cause rather than the symptom.

**Acceptance criteria**

- [ ] Endpoint accepts free text and returns ranked candidates with per-stage scores.
- [ ] Response names which cascade stage produced each candidate.
- [ ] Restricted to ENGINEER and above; results are plant-scoped.
- [ ] Used by the support runbook for resolution complaints.

*Depends on:* `LS-070` · *Blocks:* —

### EPIC-08 — Human-in-the-Loop Validation Workbench

**Goal:** Make reviewing 200 uncertain rows a 20-minute job, not a 2-day job.  
**Component:** Product · **In this release:** 4 stories, 21 points

#### `LS-080` · Validation item model and queue API

`Story` · **P0 · Must** · **5 pts** · Sprint **S5** · Product · `validation`

> As a reviewer, I want a prioritised queue of uncertain rows, so that I work through the highest-impact ambiguity first.

**Acceptance criteria**

- [ ] validation_items created for every row below the plant confidence threshold.
- [ ] Queue filterable by import, machine, uncertainty type and age; sortable by impact.
- [ ] Each item exposes the raw text, the extraction, the per-field confidence and the resolver candidates.
- [ ] Items carry status OPEN or RESOLVED with the resolving action recorded.

*Depends on:* `LS-064` · *Blocks:* `LS-081`

#### `LS-081` · Side-by-side raw-versus-extracted review payload

`Story` · **P0 · Must** · **3 pts** · Sprint **S5** · Product · `validation` `api`

> As a reviewer, I want the original text next to the extraction, so that I can judge correctness in seconds without leaving the screen.

**Acceptance criteria**

- [ ] Payload returns verbatim raw text, the source file, sheet and row, and each extracted field.
- [ ] Fields below the confidence threshold are explicitly flagged for attention.
- [ ] For OCR-sourced rows, the original image region is returned alongside the text.
- [ ] The payload is sufficient to render the review screen without any follow-up request.

*Depends on:* `LS-080` · *Blocks:* `LS-082`

#### `LS-082` · Approve, edit-and-approve and reject with conflict handling

`Story` · **P0 · Must** · **5 pts** · Sprint **S5** · Product · `validation`

> As a reviewer, I want to act on an item safely while colleagues work the same queue, so that two people never silently overwrite each other.

**Acceptance criteria**

- [ ] Three actions supported: approve as-is, edit then approve, and reject with a reason.
- [ ] Optimistic locking returns 409 when another reviewer already resolved the item.
- [ ] Approval creates the maintenance record with full provenance; rejection excludes the row from index and statistics.
- [ ] Every action writes a validation_actions audit row naming the reviewer.

*Depends on:* `LS-081` · *Blocks:* `LS-072`, `LS-083`, `LS-084`, `LS-085`, `LS-087`

#### `LS-083` · Alias-group bulk mapping

`Story` · **P0 · Must** · **8 pts** · Sprint **S5** · Product · `validation` `differentiator`

> As a reviewer facing 37 rows that all say 'Conv Motor-3', I want to map them in one action, so that validation takes minutes rather than hours.

**Acceptance criteria**

- [ ] Unresolved machine texts are grouped and the affected row count is shown per group.
- [ ] One mapping action resolves every row in the group, creates the alias and triggers re-resolution elsewhere.
- [ ] A preview shows exactly which rows will be affected before the action is committed.
- [ ] The whole operation is transactional and produces a single audited action with the row count.
- [ ] Demonstrated on a group of at least 30 records as part of the pilot acceptance run.

*Depends on:* `LS-082`, `LS-073` · *Blocks:* `LS-076`, `LS-245`

### EPIC-14 — AI Evaluation & Quality Harness

**Goal:** Know whether a prompt change made the product better or worse, before shipping.  
**Component:** AI-Quality · **In this release:** 2 stories, 13 points

#### `LS-140` · Extraction golden set of 200 hand-labelled messy rows

`Story` · **P0 · Must** · **8 pts** · Sprint **S5** · AI-Quality · `eval` `moat`

> As an engineer, I want a realistic labelled benchmark, so that extraction quality is measured rather than assumed.

**Acceptance criteria**

- [ ] 200 rows drawn from real design-partner files, anonymised, covering Hinglish, shorthand, Devanagari and OCR output.
- [ ] Every field hand-labelled with the correct value, including explicit nulls.
- [ ] Difficulty is stratified so the set is not dominated by easy rows.
- [ ] Stored under version control with a documented licence and anonymisation procedure.
- [ ] Baseline field F1 and auto-approval rate recorded as the reference point.

*Depends on:* `LS-002` · *Blocks:* `LS-143`, `LS-145`

#### `LS-141` · Resolution golden set of 150 machine-text cases

`Story` · **P0 · Must** · **5 pts** · Sprint **S5** · AI-Quality · `eval`

> As an engineer, I want resolver accuracy measured, so that a cascade change cannot quietly break machine matching.

**Acceptance criteria**

- [ ] 150 real machine texts with the correct target machine labelled, including deliberately ambiguous cases.
- [ ] Covers abbreviations, Hinglish, Devanagari, typos and genuinely unresolvable text.
- [ ] Unresolvable cases are labelled as such so over-eager matching is penalised.
- [ ] Baseline precision@1 and recall recorded.

*Depends on:* `LS-002` · *Blocks:* `LS-145`

### EPIC-24 — Frontend Product Application

**Goal:** Turn the demo prototype into the real multilingual product UI.  
**Component:** Frontend · **In this release:** 3 stories, 21 points

#### `LS-240` · Frontend architecture decision and application shell

`Story` · **P0 · Must** · **8 pts** · Sprint **S2** · Frontend · `foundation`

> As a frontend engineer, I want the framework, routing, auth and i18n settled once, so that feature work does not relitigate the basics.

**Acceptance criteria**

- [ ] Framework decision recorded as an ADR with reasoning.
- [ ] App shell provides routing, authenticated session handling with token refresh, error boundaries and a loading strategy.
- [ ] Internationalisation scaffolding supports English, Hindi and Marathi from the first screen.
- [ ] Build, lint, type-check and test run in CI alongside the backend.

*Depends on:* `LS-022` · *Blocks:* `LS-241`, `LS-248`

#### `LS-241` · Design system extracted from the demo prototype

`Story` · **P0 · Must** · **5 pts** · Sprint **S2** · Frontend · `design-system`

> As a team, we want the prototype's visual language preserved in reusable components, so that the product looks like the demo customers approved.

**Acceptance criteria**

- [ ] Tokens for colour, spacing, typography and elevation extracted from the prototype CSS.
- [ ] Core components built: cards, tables, timeline, chat blocks, trust badges, drawers, toasts, wizard.
- [ ] Trust badges render directly from the wire-format label, never from a client-side decision.
- [ ] Components are documented and visually reviewed against the prototype screenshots.

*Depends on:* `LS-240` · *Blocks:* `LS-242`, `LS-243`, `LS-244`, `LS-245`, `LS-246`, `LS-247`

#### `LS-244` · Import wizard with live pipeline progress

`Story` · **P0 · Must** · **8 pts** · Sprint **S5** · Frontend · `import`

> As an engineer importing three years of history, I want to see what is happening, so that a long run feels controlled rather than frozen.

**Acceptance criteria**

- [ ] Drag-and-drop upload with client-side type and size validation before transfer.
- [ ] Preview step shows detected sheets, headers and sample rows before commitment.
- [ ] Column mapping step presents an auto-suggested mapping with per-column confidence and allows editing; the Intake Agent's proposal (LS-065) populates this same step once it lands.
- [ ] Live progress through each pipeline stage with counts for detected, usable, skipped and needs-review.
- [ ] Completion summary links directly to the validation queue and to the skipped-row export.

*Depends on:* `LS-241`, `LS-055`, `LS-057` · *Blocks:* —

---

## R2 — Intelligence

*Make the plant's history answerable. Search, deterministic analytics, the agent runtime, the Reliability Copilot, and the guardrails and evals that make its output trustworthy.*

### EPIC-06 — Generative Extraction & Normalisation

**Goal:** Turn Hinglish shorthand into structured fields with calibrated confidence.  
**Component:** AI · **In this release:** 1 stories, 8 points

#### `LS-065` · Intake Agent: file profiling and column-mapping proposal

`Story` · **P1 · Should** · **8 pts** · Sprint **S7** · AI · `agent` `intake`

> As an engineer, I want the system to check the mapping before processing 2,000 rows, so that a wrong column does not waste twenty minutes and real money.

**Acceptance criteria**

- [ ] Agent profiles headers, data types, null density, sample values and merged-cell structure.
- [ ] Proposes a column mapping with per-column confidence and a plain-language rationale.
- [ ] Sample-extracts a stratified sample of roughly 25 rows and self-scores fill rate, resolver hit rate and date parse rate.
- [ ] If projected auto-approval falls below the plant threshold, the run stops and raises a mapping proposal citing the specific evidence.
- [ ] The engineer can accept, edit or override the proposal; the decision is audited.

*Depends on:* `LS-057`, `LS-061`, `LS-190` · *Blocks:* `LS-232`

### EPIC-07 — Entity Resolution & Alias Learning

**Goal:** "Conv Motor-3" resolves to a real asset, and the system never asks twice.  
**Component:** AI · **In this release:** 1 stories, 5 points

#### `LS-076` · Resolver Agent clarifying-question flow for ambiguous clusters

`Story` · **P1 · Should** · **5 pts** · Sprint **S9** · AI · `agent` `resolution`

> As a reviewer, I want one well-framed question to unblock dozens of rows, so that validation is a conversation rather than data entry.

**Acceptance criteria**

- [ ] Agent clusters mutually similar unresolved texts and detects genuine ambiguity between close candidates.
- [ ] Raises a single proposal per cluster showing the affected row count, the candidates and their scores.
- [ ] One decision maps the whole cluster, writes the alias and triggers re-resolution.
- [ ] Agent asks at most a configured number of questions per import so it never becomes a quiz.

*Depends on:* `LS-070`, `LS-083`, `LS-190` · *Blocks:* —

### EPIC-08 — Human-in-the-Loop Validation Workbench

**Goal:** Make reviewing 200 uncertain rows a 20-minute job, not a 2-day job.  
**Component:** Product · **In this release:** 4 stories, 14 points

#### `LS-084` · Bulk actions with partial-success reporting

`Story` · **P1 · Should** · **5 pts** · Sprint **S6** · Product · `validation`

> As a reviewer, I want to approve a filtered set at once and see exactly what failed, so that bulk work is safe rather than reckless.

**Acceptance criteria**

- [ ] Bulk approve and bulk reject operate over a selection or a filter.
- [ ] The response reports per-item success or failure with reasons; one failure never aborts the batch.
- [ ] Bulk operations are capped at a configured size and run asynchronously above a threshold, reporting progress.
- [ ] Each affected item still produces its own audit row.

*Depends on:* `LS-082` · *Blocks:* —

#### `LS-085` · Validation action audit trail

`Story` · **P0 · Must** · **3 pts** · Sprint **S6** · Product · `validation` `audit`

> As a plant admin, I want to see who approved what, so that data quality questions have a definitive answer.

**Acceptance criteria**

- [ ] Every validation action records actor, timestamp, before and after values, and reason where applicable.
- [ ] The trail is queryable by reviewer, date range and import.
- [ ] Audit rows are append-only and immutable.
- [ ] A record's detail view can show the validation decision that created it.

*Depends on:* `LS-082` · *Blocks:* `LS-086`

#### `LS-086` · Queue burn-down and reviewer-throughput metrics

`Story` · **P1 · Should** · **3 pts** · Sprint **S6** · Product · `validation` `metrics`

> As a maintenance manager, I want to see how fast the queue is clearing, so that I know whether validation is a one-week task or a permanent tax.

**Acceptance criteria**

- [ ] Metrics for queue depth over time, items resolved per reviewer-hour and median time-to-resolution.
- [ ] Corrections per 100 records tracked as a data-quality indicator.
- [ ] Metrics are exposed per plant and feed the pilot scorecard from LS-008.
- [ ] Available through the API for the dashboard and for the per-tenant scorecard in LS-147.

*Depends on:* `LS-085` · *Blocks:* `LS-147`

#### `LS-087` · Keyboard-first reviewer workflow

`Story` · **P2 · Could** · **3 pts** · Sprint **S6** · Product · `validation` `ux`

> As a reviewer clearing 200 items, I want to work without the mouse, so that the queue takes twenty minutes instead of two hours.

**Acceptance criteria**

- [ ] Keyboard shortcuts for approve, reject, edit, next and previous.
- [ ] Focus advances automatically to the next item after an action.
- [ ] An undo window allows reversing the last action without reopening the item.
- [ ] Shortcuts are discoverable through an in-app help overlay.

*Depends on:* `LS-082` · *Blocks:* —

### EPIC-09 — Hybrid Search & Retrieval

**Goal:** Find the right records from shorthand, Hindi, Marathi or English.  
**Component:** AI · **In this release:** 7 stories, 34 points

#### `LS-090` · Full-text and trigram indexes over record text

`Story` · **P0 · Must** · **5 pts** · Sprint **S6** · AI · `search`

> As an engineer, I want fast keyword search over every record, so that finding a past failure takes seconds.

**Acceptance criteria**

- [ ] PostgreSQL tsvector column maintained on insert and update, with a GIN index.
- [ ] pg_trgm indexes support typo-tolerant matching on machine and part text.
- [ ] Search is plant-scoped at the query level and verified by the cross-tenant suite.
- [ ] Query latency stays within budget on a one-million-record corpus.

*Depends on:* `LS-040` · *Blocks:* `LS-091`, `LS-092`, `LS-142`

#### `LS-091` · Embedding client port and record embedding backfill job

`Story` · **P0 · Must** · **5 pts** · Sprint **S6** · AI · `search` `embeddings`

> As the system, I need semantic vectors for every record, so that meaning-based retrieval works across languages.

**Acceptance criteria**

- [ ] Pluggable EmbeddingClient port; the model name and dimension are recorded per row.
- [ ] pgvector column with an appropriate index; dimension mismatches are rejected at write time.
- [ ] An idempotent, resumable backfill job embeds existing records and reports progress.
- [ ] New and corrected records are embedded automatically via domain events.

*Depends on:* `LS-090`, `LS-060` · *Blocks:* `LS-092`, `LS-181`

#### `LS-092` · Hybrid retrieval with reciprocal-rank fusion

`Story` · **P0 · Must** · **8 pts** · Sprint **S6** · AI · `search`

> As an engineer, I want the best of keyword and semantic search, so that both exact part codes and vague descriptions find the right records.

**Acceptance criteria**

- [ ] Full-text, trigram and vector result sets are fused by reciprocal rank fusion with documented weights.
- [ ] Filters for machine, line, date range, failure mode and part apply before fusion.
- [ ] Result count k is clamped server-side regardless of the requested value.
- [ ] nDCG@10 on the golden query set meets the threshold in LS-142.

*Depends on:* `LS-090`, `LS-091` · *Blocks:* `LS-093`, `LS-094`, `LS-095`, `LS-096`, `LS-121`, `LS-182`, `LS-226`

#### `LS-093` · Query expansion using the shorthand dictionary

`Story` · **P0 · Must** · **5 pts** · Sprint **S6** · AI · `search` `hinglish`

> As a technician searching 'brng gaya', I want bearing records, so that I do not have to know the formal term.

**Acceptance criteria**

- [ ] Queries are expanded with shorthand, Hinglish, Hindi and Marathi equivalents before matching.
- [ ] The same dictionary used at extraction time is used here, so behaviour is consistent.
- [ ] Expansion is bounded so that a short query does not explode into an unselective one.
- [ ] Benchmark queries such as brng, BRG, bearng and 'bearing gaya' all retrieve the same core result set.

*Depends on:* `LS-092`, `LS-063` · *Blocks:* —

#### `LS-094` · Why-this-matched explanation payload

`Story` · **P1 · Should** · **3 pts** · Sprint **S6** · AI · `search` `trust`

> As an engineer, I want to know why a result appeared, so that I trust the search rather than second-guessing it.

**Acceptance criteria**

- [ ] Each result carries a why array naming the matched terms, expansions and retrieval strategies.
- [ ] Matched spans are identified so the UI can highlight them.
- [ ] Semantic-only matches are labelled as such and distinguished from keyword hits.
- [ ] The explanation is part of the API contract and covered by tests.

*Depends on:* `LS-092` · *Blocks:* —

#### `LS-095` · Degraded search mode when the embedding provider is unavailable

`Story` · **P0 · Must** · **3 pts** · Sprint **S6** · AI · `search` `reliability`

> As a user, I want search to keep working during a provider outage, so that the product never goes fully dark.

**Acceptance criteria**

- [ ] Embedding failure falls back to full-text plus trigram retrieval automatically.
- [ ] The response indicates degraded mode so the UI can show an honest notice.
- [ ] Newly created records queue for embedding and are backfilled when the provider returns.
- [ ] Verified by a staging test that disables the embedding provider.

*Depends on:* `LS-092` · *Blocks:* —

#### `LS-096` · Retrieval quality benchmark wired into CI

`Story` · **P0 · Must** · **5 pts** · Sprint **S6** · AI · `search` `quality`

> As an engineer changing retrieval weights, I want immediate feedback, so that a tuning change cannot silently make search worse.

**Acceptance criteria**

- [ ] Benchmark runs the golden query set and reports nDCG@10, recall@20 and MRR.
- [ ] Results are compared against the stored baseline; a regression beyond tolerance fails the build.
- [ ] The report names which queries regressed and by how much.
- [ ] Fusion weights are configuration, not hard-coded constants, so tuning does not require a release.

*Depends on:* `LS-092`, `LS-142` · *Blocks:* —

### EPIC-10 — Deterministic Analytics & KPI Engine

**Goal:** Every number in the product, computed in SQL and reproducible forever.  
**Component:** Domain · **In this release:** 7 stories, 31 points

#### `LS-100` · Downtime, breakdown-count and record-count aggregates

`Story` · **P0 · Must** · **5 pts** · Sprint **S6** · Domain · `analytics` `trust`

> As a maintenance manager, I want reliable totals, so that the number in a chat answer and the number on the dashboard are always the same.

**Acceptance criteria**

- [ ] Aggregates computed in SQL, filterable by plant, line, machine, failure mode, part and date range.
- [ ] Records with null downtime are excluded from sums and counted in coverage, never treated as zero.
- [ ] The same service backs the dashboard, the API and the assistant tools — one implementation only.
- [ ] Results are deterministic: identical inputs produce identical outputs across runs.

*Depends on:* `LS-042` · *Blocks:* `LS-101`, `LS-102`, `LS-103`, `LS-104`, `LS-105`, `LS-121`, `LS-150`, `LS-151`, `LS-152`, `LS-154`

#### `LS-101` · MTTR, MTBF and availability calculators with documented formulas

`Story` · **P0 · Must** · **5 pts** · Sprint **S6** · Domain · `analytics` `kpi`

> As a reliability engineer, I want standard KPIs computed the way I would compute them, so that I can defend the numbers to my plant head.

**Acceptance criteria**

- [ ] MTTR, MTBF and availability implemented with the exact formula and assumptions documented in-code and in user-facing help.
- [ ] Operating hours come from plant settings, not from a hard-coded constant.
- [ ] Insufficient data returns an explicit unavailable result rather than a misleading zero.
- [ ] Unit tests assert exact expected values against the reference fixture.

*Depends on:* `LS-100` · *Blocks:* `LS-106`

#### `LS-102` · Failure Pareto and trend series

`Story` · **P0 · Must** · **5 pts** · Sprint **S7** · Domain · `analytics`

> As a maintenance manager, I want to see which failures dominate and whether they are getting better, so that I know where to spend money.

**Acceptance criteria**

- [ ] Pareto by failure mode with count, downtime and cumulative percentage.
- [ ] Trend series bucketable by week, month and quarter with explicit handling of empty buckets.
- [ ] Scopable to plant, line or machine.
- [ ] Coverage is reported alongside every series so sparse data is visible, not hidden.

*Depends on:* `LS-100` · *Blocks:* `LS-106`, `LS-163`

#### `LS-103` · Top machines and top lines ranking

`Story` · **P0 · Must** · **3 pts** · Sprint **S7** · Domain · `analytics`

> As a plant head, I want to know my worst assets by a chosen metric, so that improvement effort goes where the downtime actually is.

**Acceptance criteria**

- [ ] Ranking by downtime, breakdown count or MTTR, with configurable k.
- [ ] Ties broken deterministically so repeated calls return a stable order.
- [ ] Each entry carries the underlying counts so the ranking is auditable.
- [ ] Exposed as an assistant tool with server-side argument clamping.

*Depends on:* `LS-100` · *Blocks:* —

#### `LS-104` · Part usage, share and replacement-interval statistics

`Story` · **P0 · Must** · **5 pts** · Sprint **S7** · Domain · `analytics` `parts`

> As a maintenance manager, I want to see where a part is being consumed, so that a concentration on one line becomes visible.

**Acceptance criteria**

- [ ] Per-part usage count, machine distribution, percentage share and mean replacement interval.
- [ ] Scopable by date range, line and machine.
- [ ] Answers the benchmark question about where a given bearing has been used, with the expected machine distribution.
- [ ] Backs both the parts screen and the assistant part_usage tool.

*Depends on:* `LS-100`, `LS-074` · *Blocks:* `LS-153`, `LS-165`

#### `LS-105` · Coverage reporting on every statistic

`Story` · **P0 · Must** · **3 pts** · Sprint **S7** · Domain · `analytics` `trust`

> As an engineer, I want to know how much of the data a number is based on, so that I do not over-trust a statistic drawn from three records.

**Acceptance criteria**

- [ ] Every aggregate returns a coverage object: records considered, records with a valid value, and the percentage.
- [ ] Coverage is rendered in assistant CALCULATED blocks, for example '7 records, 7/7 valid downtime'.
- [ ] Statistics below a configured coverage floor are labelled low-confidence in the response.
- [ ] Coverage is part of the API contract and is covered by tests.

*Depends on:* `LS-100` · *Blocks:* —

#### `LS-106` · Dashboard composite endpoint with caching and invalidation

`Story` · **P0 · Must** · **5 pts** · Sprint **S7** · Domain · `analytics` `performance`

> As a maintenance manager, I want the dashboard to load quickly, so that I actually open it every morning.

**Acceptance criteria**

- [ ] One composite endpoint returns KPIs, trend, Pareto, top machines and open counts.
- [ ] Results cached per plant with event-driven invalidation on record create, update and delete.
- [ ] Cache is in-process; no Redis is introduced, per the documented scope decision.
- [ ] Dashboard reproduces the reference fixture's expected numbers exactly.

*Depends on:* `LS-101`, `LS-102` · *Blocks:* `LS-226`, `LS-242`

### EPIC-11 — Agent Runtime & Tool Platform

**Goal:** The planner, tool registry, budgets, memory and traces all agents share.  
**Component:** AI-Platform · **In this release:** 10 stories, 59 points

#### `LS-110` · AgentRun and AgentStep persistence with a replayable trace schema

`Story` · **P0 · Must** · **8 pts** · Sprint **S7** · AI-Platform · `agent` `core`

> As an engineer and as a customer, I want every agent run recorded step by step, so that 'why did it say that?' always has an answer.

**Acceptance criteria**

- [ ] AgentRun stores tenant, plant, agent type, trigger, input, policy snapshot, status and totals.
- [ ] AgentStep is append-only and ordered, capturing type, tool name, arguments, result, model, tokens, latency, cost and errors.
- [ ] Large tool results are stored by reference rather than inline to bound row size.
- [ ] Steps cannot be modified or deleted; enforced at the database role level.
- [ ] A completed run's trace is retrievable in full through one API call.

*Depends on:* `LS-012`, `LS-060` · *Blocks:* `LS-111`, `LS-112`, `LS-118`, `LS-119`, `LS-190`, `LS-200`, `LS-203`, `LS-206`

#### `LS-111` · Plan, act, observe, critique loop executor

`Story` · **P0 · Must** · **8 pts** · Sprint **S7** · AI-Platform · `agent` `core`

> As the system, I need a controlled agent loop, so that multi-step investigation is possible without unbounded cost or runaway behaviour.

**Acceptance criteria**

- [ ] Executor drives plan, tool call, observe and critique steps until an answer is ready or the budget is exhausted.
- [ ] Tool results are summarised before re-entering context; full results go only to the trace.
- [ ] The critique step is capped so the agent cannot loop indefinitely on self-doubt.
- [ ] An invalid plan is rejected before execution and triggers at most one replan.
- [ ] Every step is persisted as it happens, so a crashed run still has a partial trace.

*Depends on:* `LS-110`, `LS-112` · *Blocks:* `LS-114`, `LS-116`, `LS-119`, `LS-122`, `LS-157`, `LS-160`

#### `LS-112` · Typed tool registry with JSON schemas and argument validation

`Story` · **P0 · Must** · **5 pts** · Sprint **S7** · AI-Platform · `agent` `tools`

> As a security reviewer, I want the model's tool access constrained by code, so that a bad plan or an injection cannot reach anything unlisted.

**Acceptance criteria**

- [ ] Each tool declares a name, argument JSON schema, allowed roles, access class and result limits.
- [ ] Arguments are validated against the schema before execution; a violation is a step error, never a call.
- [ ] No tool executes free-form SQL, and an ArchUnit rule enforces it.
- [ ] Access class is READ or PROPOSE only; a DIRECT_WRITE tool fails a registry unit test.

*Depends on:* `LS-110` · *Blocks:* `LS-111`, `LS-113`, `LS-121`, `LS-134`

#### `LS-113` · Tool scoping by tenant, plant and role

`Story` · **P0 · Must** · **5 pts** · Sprint **S7** · AI-Platform · `agent` `security`

> As a customer, I want an agent to be able to reach only what the requesting user can reach, so that agency never becomes privilege escalation.

**Acceptance criteria**

- [ ] Every tool execution carries the caller's tenant, plant and role, applied at the repository layer.
- [ ] A tool call naming an out-of-scope plant returns 404 and raises a security event.
- [ ] An agent invoked by a VIEWER cannot reach PROPOSE-class tools.
- [ ] Covered by the cross-tenant test suite from LS-021.

*Depends on:* `LS-112`, `LS-024` · *Blocks:* —

#### `LS-114` · Run budgets for steps, tokens, cost and wall-clock time

`Story` · **P0 · Must** · **5 pts** · Sprint **S7** · AI-Platform · `agent` `cost`

> As the business, I want a hard ceiling on every agent run, so that one pathological question cannot cost a day's margin.

**Acceptance criteria**

- [ ] Budget covers maximum steps, tokens, cost in INR and a wall-clock deadline, defaulted per agent type.
- [ ] Budgets are overridable per tenant and captured in the run's policy snapshot.
- [ ] Exceeding a limit ends the run as BUDGET_EXCEEDED and returns a partial, clearly labelled answer.
- [ ] Budget exhaustion emits a metric and is visible in the trace; it is never a silent truncation.

*Depends on:* `LS-111` · *Blocks:* `LS-117`, `LS-202`

#### `LS-115` · Model router with task tiers and a fallback chain

`Story` · **P0 · Must** · **5 pts** · Sprint **S7** · AI-Platform · `agent` `cost` `llm`

> As the business, I want each task on the cheapest model that does it well, so that quality and cost are both deliberate choices.

**Acceptance criteria**

- [ ] Three tiers — fast, balanced and deep — mapped to task types by configuration, not by hard-coded model ids.
- [ ] A fallback chain handles provider overload or unavailability without failing the run.
- [ ] The model actually used is recorded per step for cost attribution and debugging.
- [ ] Tier assignment is changeable per tenant, for example capping the deep tier for a small plant.

*Depends on:* `LS-060` · *Blocks:* —

#### `LS-117` · Per-tenant agent policy and autonomy level

`Story` · **P0 · Must** · **5 pts** · Sprint **S8** · AI-Platform · `agent` `governance`

> As a plant IT head, I want to control what agents may do in my tenant, so that I can start conservative and expand as trust grows.

**Acceptance criteria**

- [ ] Policy sets, per tenant and agent: enabled state, autonomy level L0 to L3, budgets and model tier.
- [ ] L4 (external system writes) is not representable in the model at all.
- [ ] The active policy is snapshotted into every run for retrospective auditability.
- [ ] Policy changes are audited and take effect without a deployment.

*Depends on:* `LS-114`, `LS-190` · *Blocks:* `LS-193`

#### `LS-116` · Three-tier agent memory: working, semantic and episodic

`Story` · **P1 · Should** · **8 pts** · Sprint **S9** · AI-Platform · `agent` `memory` `moat`

> As a user, I want the agent to remember what matters, so that follow-up questions work and it does not re-raise something I already dismissed.

**Acceptance criteria**

- [ ] Working memory carries resolved entities and intents across turns, never raw transcripts.
- [ ] Semantic memory exposes aliases, dictionaries, confirmed patterns and taxonomy to every agent.
- [ ] Episodic memory makes past runs, briefings and dismissed patterns retrievable.
- [ ] A follow-up such as 'and this year?' resolves against the previously resolved machine.
- [ ] A dismissed pattern is not re-raised within its cooling-off window.

*Depends on:* `LS-111`, `LS-071` · *Blocks:* `LS-125`, `LS-177`

#### `LS-118` · Agent trace viewer API

`Story` · **P1 · Should** · **5 pts** · Sprint **S9** · AI-Platform · `agent` `trust`

> As an engineer or a customer, I want to walk through an agent's reasoning, so that the Glass Box claim is literally true.

**Acceptance criteria**

- [ ] Endpoint returns the ordered steps with tool arguments, results, timings and costs.
- [ ] Sensitive values are redacted according to the logging policy.
- [ ] Access is restricted to the run's tenant and to ENGINEER and above.
- [ ] The payload is sufficient to render the trace viewer UI in LS-247 without extra calls.

*Depends on:* `LS-110` · *Blocks:* `LS-247`

#### `LS-119` · Deterministic replay of a run against recorded tool outputs

`Story` · **P1 · Should** · **5 pts** · Sprint **S9** · AI-Platform · `agent` `testing`

> As an engineer debugging a bad answer, I want to re-run it against the exact same data, so that I can fix the prompt without chasing a moving target.

**Acceptance criteria**

- [ ] A stored run can be replayed with its recorded tool outputs substituted for live calls.
- [ ] Replay produces a comparable trace and highlights where behaviour diverged.
- [ ] Replays are marked as such and never create proposals or mutate state.
- [ ] Used as the reproduction mechanism in the AI incident runbook.

*Depends on:* `LS-110`, `LS-111` · *Blocks:* —

### EPIC-12 — Reliability Copilot

**Goal:** Multi-step investigation that answers 'why does this keep happening?'.  
**Component:** AI · **In this release:** 8 stories, 44 points

#### `LS-120` · Query understanding: intent and entity extraction over a closed taxonomy

`Story` · **P0 · Must** · **5 pts** · Sprint **S8** · AI · `assistant`

> As a user asking in Hinglish, I want my question understood correctly, so that the right tools run against the right machine and date range.

**Acceptance criteria**

- [ ] Intent classified into the closed set including ROOT_CAUSE_INVESTIGATION and OUT_OF_SCOPE.
- [ ] Entities extracted: machine text, part, failure mode, line, date range and language.
- [ ] Relative dates such as 'pichle 2 saal' and 'is saal' resolve against the plant's timezone.
- [ ] Output is JSON-schema constrained; an unparseable result triggers one retry then a clarifying question.
- [ ] Out-of-scope questions produce a polite refusal that lists actual capabilities.

*Depends on:* `LS-060`, `LS-070` · *Blocks:* `LS-125`, `LS-136`

#### `LS-121` · Read-only assistant tool suite

`Story` · **P0 · Must** · **8 pts** · Sprint **S8** · AI · `assistant` `tools`

> As the Copilot, I need deterministic tools, so that every number I report was computed rather than generated.

**Acceptance criteria**

- [ ] Tools registered: resolve_machine, machine_stats, stat_query, search_records, part_usage, top_machines, pattern_lookup, record_history.
- [ ] Every tool is READ access class, plant-scoped and argument-validated with server-side clamping.
- [ ] Each tool returns coverage metadata alongside its values.
- [ ] Tool outputs are captured in the run trace for verification and citation.

*Depends on:* `LS-112`, `LS-100`, `LS-092` · *Blocks:* `LS-122`, `LS-130`, `LS-134`

#### `LS-122` · Multi-step investigation planner with replanning

`Story` · **P0 · Must** · **8 pts** · Sprint **S8** · AI · `assistant` `agent`

> As an engineer asking why something keeps failing, I want the system to actually investigate, so that I get an analysis rather than a search result.

**Acceptance criteria**

- [ ] The planner chooses the next tool based on prior observations rather than a fixed chain.
- [ ] A ROOT_CAUSE_INVESTIGATION intent gets a larger step and token budget than a simple lookup.
- [ ] The benchmark investigation chains at least four dependent tool calls and reaches a cited conclusion.
- [ ] Simple factual questions still resolve in one or two steps — the planner does not over-investigate.
- [ ] Agentic evaluation suite success rate meets the threshold in LS-145.

*Depends on:* `LS-111`, `LS-121` · *Blocks:* `LS-123`, `LS-127`

#### `LS-123` · Typed answer blocks with trust labels

`Story` · **P0 · Must** · **5 pts** · Sprint **S8** · AI · `assistant` `trust`

> As a user, I want to see at a glance what is fact, what is calculated and what is speculation, so that I never mistake a guess for a finding.

**Acceptance criteria**

- [ ] Blocks typed SUMMARY, FACT, CALCULATED, PATTERN and HYPOTHESIS as a wire-format property.
- [ ] CALCULATED blocks carry the source tool and coverage; HYPOTHESIS blocks carry POSSIBLE or LIKELY plus the fixed disclaimer.
- [ ] The frontend renders badges directly from the label — trust is never a UI decision.
- [ ] Schema is versioned and covered by contract tests.

*Depends on:* `LS-122` · *Blocks:* `LS-124`, `LS-126`, `LS-130`, `LS-131`, `LS-143`, `LS-246`

#### `LS-124` · Citation builder linking every claim to source records

`Story` · **P0 · Must** · **5 pts** · Sprint **S8** · AI · `assistant` `trust`

> As an engineer, I want to click any claim and land on the original log row, so that I can verify the system rather than trust it.

**Acceptance criteria**

- [ ] Citations link answer blocks to maintenance and raw record identifiers.
- [ ] Every FACT block carries at least one resolvable citation within the caller's scope.
- [ ] Citations persist with the message so a historical answer remains verifiable.
- [ ] Following a citation opens the View Source provenance from LS-041.

*Depends on:* `LS-123`, `LS-041` · *Blocks:* `LS-132`, `LS-183`, `LS-246`

#### `LS-125` · Conversation context carrying resolved entities across turns

`Story` · **P0 · Must** · **5 pts** · Sprint **S9** · AI · `assistant` `memory`

> As a user, I want follow-up questions to just work, so that I can have a conversation instead of restating the machine every time.

**Acceptance criteria**

- [ ] Conversation state carries the last N turns' intents and resolved entities, not raw transcripts.
- [ ] A follow-up such as 'aur is saal?' resolves against the previously resolved machine and reports what it assumed.
- [ ] Context is bounded so a long conversation does not grow unboundedly in tokens.
- [ ] A user can start a fresh context explicitly.

*Depends on:* `LS-116`, `LS-120` · *Blocks:* —

#### `LS-126` · Multilingual answers in English, Hindi, Marathi and Hinglish

`Story` · **P0 · Must** · **5 pts** · Sprint **S9** · AI · `assistant` `i18n`

> As a shop-floor user, I want answers in my language, so that the product is usable by everyone in the plant, not only by managers.

**Acceptance criteria**

- [ ] Answers render in the user's selected language while numbers stay identical across languages.
- [ ] Trust badges are localised; raw log text is never translated.
- [ ] A Devanagari or Marathi question is answered correctly in the selected language.
- [ ] Covered by the assistant golden set in both Latin and Devanagari scripts.

*Depends on:* `LS-123` · *Blocks:* —

#### `LS-127` · Graceful degradation when the model provider is unavailable

`Story` · **P0 · Must** · **3 pts** · Sprint **S9** · AI · `assistant` `reliability`

> As a user during a provider outage, I want the deterministic parts to still answer, so that the product stays useful when the model is not.

**Acceptance criteria**

- [ ] Provider failure returns deterministic blocks — statistics and retrieved records — with no generated prose.
- [ ] The response uses the documented 424 semantics and states plainly that AI composition is unavailable.
- [ ] The circuit breaker prevents repeated slow failures from degrading overall latency.
- [ ] Verified by a staging test that disables the model provider.

*Depends on:* `LS-122` · *Blocks:* —

### EPIC-13 — Trust, Guardrails & Verification

**Goal:** Structurally prevent the product from ever stating an ungrounded number.  
**Component:** AI-Safety · **In this release:** 4 stories, 23 points

#### `LS-130` · Numeric guardrail: every numeral traced to a tool output

`Story` · **P0 · Must** · **8 pts** · Sprint **S8** · AI-Safety · `guardrail` `differentiator`

> As a plant head, I want certainty that the system never invents a number, so that I can act on what it tells me.

**Acceptance criteria**

- [ ] Every numeral in a FACT or CALCULATED block is matched against values present in the run's tool outputs, including rounded forms.
- [ ] An unmatched numeral causes substitution with the tool value, or the block is dropped if unmappable.
- [ ] Every violation is logged with the run id and emits a metric.
- [ ] The golden answer set achieves 100% numeric accuracy; anything less fails CI.
- [ ] A deliberately hallucinating fake model is used in tests to prove the guardrail fires.

*Depends on:* `LS-123`, `LS-121` · *Blocks:* `LS-135`, `LS-158`, `LS-160`

#### `LS-131` · Label enforcement: causal language forced into HYPOTHESIS

`Story` · **P0 · Must** · **5 pts** · Sprint **S8** · AI-Safety · `guardrail`

> As a reliability engineer, I want speculation clearly marked, so that a guess is never presented to my plant head as a confirmed root cause.

**Acceptance criteria**

- [ ] Causal markers in English, Hindi and Marathi are detected outside HYPOTHESIS blocks.
- [ ] Offending content is force-wrapped into a HYPOTHESIS block with the fixed disclaimer.
- [ ] HYPOTHESIS blocks are stripped of any new numerals not present in tool outputs.
- [ ] Detection patterns are unit-tested across all three languages.

*Depends on:* `LS-123` · *Blocks:* `LS-135`

#### `LS-132` · Citation completeness check

`Story` · **P0 · Must** · **5 pts** · Sprint **S8** · AI-Safety · `guardrail`

> As a user, I want every stated fact to be verifiable, so that an uncitable claim never reaches my screen.

**Acceptance criteria**

- [ ] FACT blocks without at least one resolvable citation are dropped before the response is returned.
- [ ] Citations pointing outside the caller's tenant or plant are treated as invalid and raise a security event.
- [ ] Dropped blocks are logged with the reason and counted as a metric.
- [ ] Citation validity on the golden set meets the configured threshold.

*Depends on:* `LS-124` · *Blocks:* —

#### `LS-134` · Prompt-injection defences

`Story` · **P0 · Must** · **5 pts** · Sprint **S8** · AI-Safety · `guardrail` `security`

> As a security reviewer, I want a hostile log line to be inert, so that untrusted plant data cannot steer the system.

**Acceptance criteria**

- [ ] Retrieved record text and inbound messages are fenced and labelled as quoted data in every prompt.
- [ ] The system prompt states that quoted content is never an instruction.
- [ ] Because no tool has direct write access, a successful injection can at worst produce a proposal a human rejects.
- [ ] Injection canaries are part of the CI safety suite and of production sampling.
- [ ] A record containing an instruction-shaped payload is proven not to alter tool selection.

*Depends on:* `LS-112`, `LS-121` · *Blocks:* `LS-144`

### EPIC-14 — AI Evaluation & Quality Harness

**Goal:** Know whether a prompt change made the product better or worse, before shipping.  
**Component:** AI-Quality · **In this release:** 5 stories, 31 points

#### `LS-142` · Retrieval golden set of 60 queries with relevance judgements

`Story` · **P0 · Must** · **5 pts** · Sprint **S6** · AI-Quality · `eval`

> As an engineer tuning search, I want graded relevance data, so that fusion-weight changes are evaluated rather than guessed.

**Acceptance criteria**

- [ ] 60 realistic queries spanning shorthand, natural language, English, Hindi and Marathi.
- [ ] Graded relevance judgements per query over a fixed corpus.
- [ ] Includes queries expected to return nothing, to catch false-positive retrieval.
- [ ] Baseline nDCG@10, recall@20 and MRR recorded.

*Depends on:* `LS-090` · *Blocks:* `LS-096`, `LS-145`

#### `LS-143` · Assistant golden set of 80 questions with gold facts and numbers

`Story` · **P0 · Must** · **8 pts** · Sprint **S8** · AI-Quality · `eval` `trust`

> As an engineer, I want answer correctness measured against known truth, so that the 100% numeric accuracy claim is continuously verified.

**Acceptance criteria**

- [ ] 80 questions across every intent, in English, Hinglish and Devanagari.
- [ ] Each carries the expected numbers, the expected citation set and the expected block labels.
- [ ] Includes questions whose correct answer is 'not enough data'.
- [ ] Evaluated for numeric accuracy, citation validity and label correctness.
- [ ] Numeric accuracy below 100% is a build failure, not a warning.

*Depends on:* `LS-123`, `LS-140` · *Blocks:* `LS-145`

#### `LS-144` · Safety suite: injection, out-of-scope and PII probes

`Story` · **P0 · Must** · **5 pts** · Sprint **S9** · AI-Quality · `eval` `security`

> As a security reviewer, I want adversarial cases run continuously, so that a prompt change cannot reopen a closed hole.

**Acceptance criteria**

- [ ] At least 30 cases covering prompt injection via record text, out-of-scope questions, PII extraction attempts and cross-tenant probing.
- [ ] Injection payloads are embedded in fixture maintenance records, exactly as a real attack would arrive.
- [ ] Expected behaviour declared per case; any deviation fails the build.
- [ ] New cases are added whenever a real incident is found in production.

*Depends on:* `LS-134` · *Blocks:* —

#### `LS-145` · Evaluation runner with thresholds and an HTML report

`Story` · **P0 · Must** · **8 pts** · Sprint **S9** · AI-Quality · `eval` `tooling`

> As an engineer, I want one command to tell me whether the AI got better or worse, so that prompt work is engineering rather than vibes.

**Acceptance criteria**

- [ ] A single command runs every suite and prints a per-metric pass or fail against configured thresholds.
- [ ] An HTML report shows per-case results with diffs against the stored baseline.
- [ ] Suites are runnable individually for fast local iteration.
- [ ] Cost and latency of the evaluation run itself are reported.
- [ ] Includes the agentic suite: 25 multi-step investigations scored on task success, steps used and cost per run.

*Depends on:* `LS-140`, `LS-141`, `LS-142`, `LS-143` · *Blocks:* `LS-146`, `LS-205`

#### `LS-146` · CI gate blocking merges on evaluation regression

`Story` · **P0 · Must** · **5 pts** · Sprint **S9** · AI-Quality · `eval` `ci`

> As a team, we want quality regressions blocked automatically, so that nobody has to remember to run the evals.

**Acceptance criteria**

- [ ] Any PR touching prompts, tools, agent code or retrieval configuration triggers the evaluation suite.
- [ ] A regression beyond the per-metric tolerance fails the build and annotates the PR.
- [ ] Numeric accuracy and the safety suite are absolute gates with no tolerance.
- [ ] An override requires an explicit label and is recorded in the PR history.
- [ ] Evaluation runs against recorded fixtures where possible to keep CI cost bounded.

*Depends on:* `LS-145`, `LS-018` · *Blocks:* —

### EPIC-19 — Proposal & Approval Inbox

**Goal:** The governed write path: agents propose, named humans dispose, everything reverts.  
**Component:** Product · **In this release:** 1 stories, 5 points

#### `LS-190` · Proposal entity as the universal agent write envelope

`Story` · **P0 · Must** · **5 pts** · Sprint **S7** · Product · `governance` `differentiator`

> As a customer, I want every agent-initiated change to arrive as a proposal, so that agency never becomes unsupervised authority.

**Acceptance criteria**

- [ ] Proposal stores type, payload, evidence, confidence, risk, status, proposing run and deciding user.
- [ ] Status lifecycle DRAFT, PENDING, APPROVED, REJECTED, APPLIED, REVERTED with enforced transitions.
- [ ] Every proposal links to the agent run and trace that produced it.
- [ ] No code path writes agent-originated data outside this envelope; enforced by an ArchUnit rule.

*Depends on:* `LS-016`, `LS-110` · *Blocks:* `LS-065`, `LS-076`, `LS-117`, `LS-160`, `LS-191`

### EPIC-24 — Frontend Product Application

**Goal:** Turn the demo prototype into the real multilingual product UI.  
**Component:** Frontend · **In this release:** 3 stories, 24 points

#### `LS-245` · Validation workbench UI

`Story` · **P0 · Must** · **8 pts** · Sprint **S6** · Frontend · `validation`

> As a reviewer, I want an efficient review screen, so that clearing the queue is a short focused task.

**Acceptance criteria**

- [ ] Split-screen showing raw source beside the extraction, with low-confidence fields highlighted.
- [ ] Alias-group bulk mapping shows the affected row count and a preview before committing.
- [ ] Keyboard shortcuts per LS-087 with an in-app help overlay.
- [ ] Conflict when another reviewer resolved an item is handled gracefully, never as a raw error.

*Depends on:* `LS-241`, `LS-083` · *Blocks:* —

#### `LS-242` · Plant dashboard with KPIs, charts and insight cards

`Story` · **P0 · Must** · **8 pts** · Sprint **S7** · Frontend · `dashboard`

> As a maintenance manager, I want one screen showing my plant's health, so that my morning check takes two minutes.

**Acceptance criteria**

- [ ] Renders KPIs, trend chart, failure Pareto, top machines and open counts from the composite endpoint.
- [ ] Insight cards display detected patterns with their trust labels.
- [ ] Loading, empty and error states are designed rather than default.
- [ ] Numbers match the API exactly; the frontend performs no arithmetic of its own.

*Depends on:* `LS-241`, `LS-106` · *Blocks:* `LS-249`

#### `LS-243` · Machine master and machine detail with timeline and View Source

`Story` · **P0 · Must** · **8 pts** · Sprint **S7** · Frontend · `machines`

> As an engineer, I want a machine's full story on one page, so that investigating a breakdown starts with context.

**Acceptance criteria**

- [ ] Machine list with search, filters and pagination.
- [ ] Detail page shows statistics, failure Pareto, parts consumed and a chronological timeline.
- [ ] Every timeline entry opens a source drawer with the original raw text, file, sheet and row.
- [ ] Raw source text is never translated, even when the UI language is Hindi or Marathi.

*Depends on:* `LS-241`, `LS-044` · *Blocks:* `LS-249`

---

## R3 — Proactive & Field

*Stop waiting to be asked. Watchtower briefings, generative work artifacts, the WhatsApp field agent and the approval inbox that governs every agent write.*

### EPIC-13 — Trust, Guardrails & Verification

**Goal:** Structurally prevent the product from ever stating an ungrounded number.  
**Component:** AI-Safety · **In this release:** 3 stories, 9 points

#### `LS-133` · Human-only CONFIRMED transition enforced at the database

`Story` · **P0 · Must** · **3 pts** · Sprint **S10** · AI-Safety · `guardrail` `database`

> As a customer, I want a hard guarantee that no machine confirmed a root cause, so that the trust principle cannot be bypassed by a code bug.

**Acceptance criteria**

- [ ] A database trigger rejects any transition to CONFIRMED where the actor is not a human user.
- [ ] Service-layer checks exist as well, but the trigger is the authority.
- [ ] An attempted machine confirmation raises a security event and fails the transaction.
- [ ] Covered by an integration test that attempts the transition as a system actor.

*Depends on:* `LS-156` · *Blocks:* —

#### `LS-135` · Guardrail violation logging, metrics and alerting

`Story` · **P0 · Must** · **3 pts** · Sprint **S10** · AI-Safety · `guardrail` `observability`

> As an engineer, I want to know immediately when guardrails start firing more often, so that a bad prompt or model change is caught in hours.

**Acceptance criteria**

- [ ] Every violation records type, run id, agent, model and prompt version.
- [ ] Violation rate is a dashboard metric segmented by type and model.
- [ ] An alert fires when the rate exceeds the configured threshold over a rolling window.
- [ ] A spike is a documented trigger for prompt or model rollback via LS-206.

*Depends on:* `LS-130`, `LS-131` · *Blocks:* `LS-207`

#### `LS-136` · Out-of-scope handling and honest refusals

`Story` · **P1 · Should** · **3 pts** · Sprint **S10** · AI-Safety · `guardrail` `ux`

> As a user asking something the product cannot answer, I want a clear no with alternatives, so that I am not misled by a confident non-answer.

**Acceptance criteria**

- [ ] Out-of-scope questions produce a polite refusal that lists what the product can actually do.
- [ ] Questions with no supporting data return an explicit 'not enough data' rather than an invented estimate.
- [ ] Refusals are localised into all supported languages.
- [ ] Refusal correctness is measured by the safety suite at 100%.

*Depends on:* `LS-120` · *Blocks:* —

### EPIC-15 — Pattern Detection & Watchtower Agent

**Goal:** The product stops waiting to be asked and starts bringing findings to people.  
**Component:** AI · **In this release:** 10 stories, 52 points

#### `LS-150` · Recurrence detector

`Story` · **P0 · Must** · **5 pts** · Sprint **S10** · AI · `patterns`

> As a reliability engineer, I want repeating failures surfaced with their interval, so that I can act before the next one.

**Acceptance criteria**

- [ ] Detects at least three breakdowns of the same machine and failure mode with interval coefficient of variation within the configured bound.
- [ ] Reports event count, mean interval, variability and the next expected window as FACT metrics.
- [ ] Any causal explanation is emitted separately as a labelled HYPOTHESIS.
- [ ] Thresholds are overridable per plant; detector maths is unit-tested against fixtures.

*Depends on:* `LS-100` · *Blocks:* `LS-155`, `LS-164`, `LS-176`

#### `LS-151` · Temporary-fix repeat detector

`Story` · **P0 · Must** · **5 pts** · Sprint **S10** · AI · `patterns`

> As a maintenance manager, I want to see where we keep applying a band-aid, so that a permanent fix gets authorised.

**Acceptance criteria**

- [ ] Classifies actions as temporary (clean, tighten, reset, re-tension) versus permanent.
- [ ] Detects at least two cycles of a temporary fix followed within the window by the same failure mode.
- [ ] Reports the cycle count and the cumulative downtime consumed by the repeated fixes.
- [ ] Action classification is dictionary-driven and extensible per plant.

*Depends on:* `LS-100` · *Blocks:* `LS-155`

#### `LS-152` · Cross-machine failure cluster detector

`Story` · **P0 · Must** · **5 pts** · Sprint **S10** · AI · `patterns`

> As a reliability engineer, I want to notice when a failure mode spreads across a line, so that a systemic cause is not missed one machine at a time.

**Acceptance criteria**

- [ ] Detects the same failure mode on at least three machines of the same type or line within the window.
- [ ] Reports the affected machines, the timeline and the shared attributes.
- [ ] Scoped by line and machine type with per-plant thresholds.
- [ ] Evidence links to every contributing record.

*Depends on:* `LS-100` · *Blocks:* `LS-155`

#### `LS-153` · Part concentration detector

`Story` · **P0 · Must** · **3 pts** · Sprint **S10** · AI · `patterns` `parts`

> As a maintenance manager, I want to see when one part is consumed disproportionately in one place, so that I investigate the cause.

**Acceptance criteria**

- [ ] Detects a part exceeding the configured usage count with a share above the threshold on one line or machine group.
- [ ] Reports total uses, the distribution and the concentration percentage.
- [ ] Links to the underlying part-usage statistics for verification.
- [ ] Thresholds overridable per plant.

*Depends on:* `LS-104` · *Blocks:* `LS-155`

#### `LS-154` · Downtime hotspot detector

`Story` · **P0 · Must** · **3 pts** · Sprint **S10** · AI · `patterns`

> As a plant head, I want to know which line carries most of my downtime, so that improvement effort is aimed correctly.

**Acceptance criteria**

- [ ] Detects a line or machine whose downtime share exceeds the configured proportion of the plant total.
- [ ] Reports absolute hours, share and the comparison window.
- [ ] Applies the plant's downtime cost to express the hotspot in rupees.
- [ ] Excludes windows with insufficient coverage rather than reporting a misleading share.

*Depends on:* `LS-100` · *Blocks:* `LS-155`

#### `LS-155` · Pattern fingerprinting, deduplication and dismissal memory

`Story` · **P0 · Must** · **5 pts** · Sprint **S10** · AI · `patterns` `ux`

> As an engineer, I want a dismissed pattern to stay dismissed, so that the system does not nag me about something I already decided.

**Acceptance criteria**

- [ ] Each pattern has a stable fingerprint over its type, scope and evidence shape.
- [ ] A re-detected pattern updates the existing record rather than creating a duplicate.
- [ ] Dismissed patterns are suppressed for a configurable cooling-off period.
- [ ] A materially changed pattern — for example new evidence doubling the count — can re-surface with that change stated.

*Depends on:* `LS-150`, `LS-151`, `LS-152`, `LS-153`, `LS-154` · *Blocks:* `LS-156`, `LS-157`

#### `LS-156` · Pattern review lifecycle

`Story` · **P0 · Must** · **5 pts** · Sprint **S10** · AI · `patterns` `trust`

> As a reliability engineer, I want to triage detected patterns, so that the system's suggestions become my team's decisions.

**Acceptance criteria**

- [ ] Lifecycle DETECTED to ACKNOWLEDGED to CONFIRMED or DISMISSED, with legal transitions enforced.
- [ ] Only a human user can move a pattern to CONFIRMED; enforced by the trigger in LS-133.
- [ ] Dismissal requires a reason, which feeds detector tuning.
- [ ] Every transition is audited with the actor and timestamp.

*Depends on:* `LS-155` · *Blocks:* `LS-133`

#### `LS-157` · Watchtower Agent: scheduled scan, triage and ranking

`Story` · **P0 · Must** · **8 pts** · Sprint **S10** · AI · `agent` `watchtower` `differentiator`

> As a maintenance manager, I want the system to tell me what matters without being asked, so that I do not have to remember to look.

**Acceptance criteria**

- [ ] Runs nightly on a schedule and on triggers such as a completed large import or a new record on a flagged machine.
- [ ] Runs all five detectors, deduplicates against dismissal memory, then ranks findings by severity, recency, downtime cost and confidence.
- [ ] Ranking function is configurable and unit-tested; the scan runs inside its documented budget.
- [ ] A targeted rescan after a new record completes quickly rather than rescanning the whole plant.
- [ ] Scan results are persisted as an agent run with a full trace.

*Depends on:* `LS-155`, `LS-111` · *Blocks:* `LS-158`

#### `LS-158` · Daily and weekly plant briefing

`Story` · **P0 · Must** · **8 pts** · Sprint **S11** · AI · `agent` `watchtower` `retention`

> As a maintenance manager, I want a short morning briefing, so that LogSense becomes part of my routine rather than a tab I forget.

**Acceptance criteria**

- [ ] Briefing is capped at five ranked items; each carries FACT evidence and at most one labelled hypothesis.
- [ ] Numbers pass the numeric guardrail exactly as assistant answers do.
- [ ] Generated in the recipient's language, with every item linking to its evidence.
- [ ] Daily and weekly cadences are configurable per plant; an empty day produces an honest 'nothing notable' rather than filler.
- [ ] Delivered for 14 consecutive days to a real plant as the release exit criterion.

*Depends on:* `LS-157`, `LS-130` · *Blocks:* `LS-159`, `LS-234`

#### `LS-159` · Alert routing and delivery preferences by role

`Story` · **P1 · Should** · **5 pts** · Sprint **S11** · AI · `notifications`

> As a user, I want to control what reaches me and how, so that alerts stay useful instead of becoming noise I mute.

**Acceptance criteria**

- [ ] Routing rules by role: manager receives the briefing, engineer receives machine-level alerts, plant head receives the weekly roll-up.
- [ ] Per-user channel and frequency preferences, including full opt-out.
- [ ] Rate limiting prevents alert storms after a large import.
- [ ] Delivery outcomes are recorded so a missed alert can be investigated.

*Depends on:* `LS-158` · *Blocks:* `LS-194`

### EPIC-16 — Generative Work Artifacts

**Goal:** Draft the documents engineers hate writing, with citations intact.  
**Component:** Product · **In this release:** 7 stories, 47 points

#### `LS-160` · Scribe Agent framework: evidence gathering to drafted document

`Story` · **P0 · Must** · **8 pts** · Sprint **S11** · Product · `agent` `scribe`

> As an engineer, I want the system to draft documents from real evidence, so that paperwork stops consuming my Friday.

**Acceptance criteria**

- [ ] Shared framework: gather evidence via read tools, draft against a template, verify, then raise a document proposal.
- [ ] Every generated document passes the numeric, citation and label guardrails before a human ever sees it.
- [ ] Document templates are versioned and configurable per tenant.
- [ ] Generation cost and latency are recorded per document.
- [ ] Drafts always land as proposals; no document is published without human approval.

*Depends on:* `LS-111`, `LS-130`, `LS-190` · *Blocks:* `LS-161`, `LS-162`, `LS-163`, `LS-164`, `LS-165`, `LS-185`

#### `LS-161` · Root-cause analysis draft generator

`Story` · **P0 · Must** · **8 pts** · Sprint **S11** · Product · `agent` `scribe` `differentiator`

> As a reliability engineer, I want an RCA drafted with the evidence already assembled, so that a three-hour job becomes a ten-minute review.

**Acceptance criteria**

- [ ] Produces a 5-Why or Fishbone scaffold pre-filled from machine history, similar failures, patterns and part usage.
- [ ] Every factual claim carries an inline citation to a dated record.
- [ ] Causal branches are labelled as hypotheses requiring engineering validation — never as confirmed causes.
- [ ] The engineer can edit every section before approving; edits are retained and audited.
- [ ] Validated by an engineer approving and exporting a real RCA as a release exit criterion.

*Depends on:* `LS-160` · *Blocks:* `LS-166`

#### `LS-162` · Shift-handover note generator

`Story` · **P1 · Should** · **5 pts** · Sprint **S11** · Product · `agent` `scribe`

> As an outgoing shift lead, I want the handover written for me, so that knowledge survives the shift change instead of evaporating.

**Acceptance criteria**

- [ ] Summarises the shift's records, open breakdowns, pending validations and machines under watch.
- [ ] Generated in the recipient's language on the plant's configured shift boundaries.
- [ ] Reviewable and editable before it is issued.
- [ ] Issued notes are retained and searchable as part of plant history.

*Depends on:* `LS-160` · *Blocks:* —

#### `LS-163` · Monthly reliability review draft

`Story` · **P1 · Should** · **8 pts** · Sprint **S12** · Product · `agent` `scribe`

> As a maintenance manager, I want the monthly review drafted from data, so that I stop rebuilding the same slides from memory.

**Acceptance criteria**

- [ ] Covers KPI movement against the prior period, Pareto shifts, top patterns and downtime cost.
- [ ] Every number is tool-derived and traceable; period-over-period deltas are computed, not narrated.
- [ ] Generated on a schedule with a configurable period start.
- [ ] Exportable through LS-166 with citations preserved.

*Depends on:* `LS-160`, `LS-102` · *Blocks:* —

#### `LS-164` · Preventive-maintenance interval change proposal

`Story` · **P1 · Should** · **8 pts** · Sprint **S12** · Product · `agent` `scribe` `value`

> As a maintenance manager, I want an evidence-backed PM interval recommendation, so that a schedule change is a decision rather than a guess.

**Acceptance criteria**

- [ ] Proposes an interval change from observed recurrence interval, downtime cost and part cost.
- [ ] Shows the current interval, proposed interval, supporting evidence and expected annual saving.
- [ ] Explicitly labelled as a recommendation requiring engineering approval.
- [ ] Approval records the decision in LogSense only — no write-back to any external CMMS, per the product principle.

*Depends on:* `LS-160`, `LS-150` · *Blocks:* —

#### `LS-165` · Spare-stocking recommendation

`Story` · **P1 · Should** · **5 pts** · Sprint **S12** · Product · `agent` `scribe` `parts`

> As a stores manager, I want stocking levels backed by consumption history, so that I avoid both stock-outs and dead inventory.

**Acceptance criteria**

- [ ] Recommends reorder point and quantity from consumption rate, lead time, criticality and concentration.
- [ ] States the assumptions and the evidence window explicitly.
- [ ] Flags parts whose consumption is accelerating relative to the prior period.
- [ ] Delivered as a proposal for human approval; nothing is ordered by the system.

*Depends on:* `LS-160`, `LS-104` · *Blocks:* —

#### `LS-166` · Artifact export to PDF and DOCX with citations preserved

`Story` · **P1 · Should** · **5 pts** · Sprint **S12** · Product · `export`

> As an engineer, I want to export an RCA for an audit, so that the citations survive outside the product.

**Acceptance criteria**

- [ ] Export to PDF and DOCX preserves structure, trust labels and inline citations.
- [ ] Citations render as resolvable references including record identifier and date.
- [ ] Plant branding and the document template are configurable per tenant.
- [ ] Exports are generated asynchronously with a pollable job and an audit record.

*Depends on:* `LS-161` · *Blocks:* —

### EPIC-17 — WhatsApp Field Agent

**Goal:** Capture new records where technicians already are, in the language they use.  
**Component:** Integrations · **In this release:** 7 stories, 39 points

#### `LS-170` · WhatsApp Business API adapter with signature verification

`Story` · **P0 · Must** · **5 pts** · Sprint **S12** · Integrations · `whatsapp`

> As a security reviewer, I want inbound messages cryptographically verified, so that nobody can inject records by forging a webhook.

**Acceptance criteria**

- [ ] Official WhatsApp Business API only; unofficial gateways are explicitly rejected in the adapter design.
- [ ] Webhook signature verified on every request; a failure returns 401 and raises a security event.
- [ ] Provider is behind a port so a second provider can be added without touching conversation logic.
- [ ] Outbound sending handles rate limits and template requirements.

*Depends on:* `LS-060` · *Blocks:* `LS-171`

#### `LS-171` · Inbound webhook with idempotency and message persistence

`Story` · **P0 · Must** · **5 pts** · Sprint **S12** · Integrations · `whatsapp`

> As the system, I need duplicate deliveries handled safely, so that a provider retry never creates two records from one message.

**Acceptance criteria**

- [ ] Every inbound message is persisted with its provider message id before processing.
- [ ] Duplicate message ids are acknowledged and ignored idempotently.
- [ ] The webhook acknowledges quickly and processes asynchronously to avoid provider timeouts.
- [ ] Unparseable payloads are stored for investigation rather than dropped.

*Depends on:* `LS-170` · *Blocks:* `LS-172`

#### `LS-172` · Technician contact registry with consented phone-number binding

`Story` · **P0 · Must** · **5 pts** · Sprint **S12** · Integrations · `whatsapp` `compliance`

> As a compliance owner, I want technician phone numbers handled lawfully, so that DPDP obligations are met from day one.

**Acceptance criteria**

- [ ] Technicians are registered by phone number and bound to a user and plant.
- [ ] Consent is captured and recorded with timestamp and purpose before any binding is active.
- [ ] Messages from unregistered numbers are rejected with a polite reply and are not stored as records.
- [ ] Numbers are treated as personal data: encrypted, access-controlled and erasable under LS-211.

*Depends on:* `LS-171`, `LS-023` · *Blocks:* `LS-173`, `LS-211`

#### `LS-173` · Conversation state machine

`Story` · **P0 · Must** · **8 pts** · Sprint **S12** · Integrations · `whatsapp`

> As a technician, I want a short predictable exchange, so that reporting a breakdown takes under a minute on my phone.

**Acceptance criteria**

- [ ] States NEW, EXTRACTING, AWAITING_FIELD, AWAITING_CONFIRMATION, CONFIRMED and ABANDONED with enforced transitions.
- [ ] Conversations time out to ABANDONED after a configured idle period without creating a record.
- [ ] Confirmation echoes a structured summary before anything is saved.
- [ ] Conversation state is durable across restarts.

*Depends on:* `LS-172` · *Blocks:* `LS-174`

#### `LS-174` · Field Agent slot-filling dialogue

`Story` · **P0 · Must** · **8 pts** · Sprint **S12** · Integrations · `agent` `whatsapp`

> As a technician writing in Hinglish, I want to be asked only what is missing, so that the system feels helpful rather than bureaucratic.

**Acceptance criteria**

- [ ] Extracts all available fields from the first message and asks only for genuinely missing required fields.
- [ ] Asks at most a configured number of follow-up questions before offering to save what it has.
- [ ] Replies in the language the technician used, including Hinglish and Devanagari.
- [ ] On confirmation, creates a staged record via the standard auto-approval path and replies with the record id.
- [ ] Technicians complete the flow with no training beyond one demonstration.

*Depends on:* `LS-173`, `LS-061`, `LS-070` · *Blocks:* `LS-175`, `LS-176`, `LS-177`

#### `LS-175` · Voice-note transcription hook

`Story` · **P1 · Should** · **5 pts** · Sprint **S12** · Integrations · `whatsapp`

> As a technician with oily hands, I want to send a voice note, so that reporting does not require typing.

**Acceptance criteria**

- [ ] Voice media is fetched and sent to a pluggable transcription provider, then follows the identical text path.
- [ ] Transcription confidence feeds overall extraction confidence; low confidence routes to validation.
- [ ] Original audio is retained as provenance and is playable in the validation workbench.
- [ ] Transcription failure produces a helpful reply asking for a typed message, never silence.

*Depends on:* `LS-174` · *Blocks:* —

#### `LS-176` · Recurrence callback on record creation

`Story` · **P1 · Should** · **3 pts** · Sprint **S12** · Integrations · `whatsapp` `differentiator`

> As a technician, I want to be told when this failure has happened before, so that I know to escalate rather than just fix it again.

**Acceptance criteria**

- [ ] On confirmation, a recurrence check runs against the machine and failure mode.
- [ ] A recurrence produces a plain-language note, for example that this is the fifth bearing replacement with a mean interval of 92 days.
- [ ] The responsible engineer is alerted through the routing rules in LS-159.
- [ ] The callback uses only deterministic counts and intervals, never generated numbers.

*Depends on:* `LS-174`, `LS-150` · *Blocks:* —

### EPIC-18 — Plant Knowledge Base

**Goal:** Ground answers in manuals, SOPs and past RCAs, not only in log rows.  
**Component:** AI · **In this release:** 2 stories, 13 points

#### `LS-180` · Document ingestion for manuals, SOPs and past RCAs

`Story` · **P1 · Should** · **8 pts** · Sprint **S12** · AI · `knowledge-base` `upsell`

> As a reliability engineer, I want the plant's documents searchable alongside its records, so that answers draw on everything we know.

**Acceptance criteria**

- [ ] Accepts PDF, DOCX and scanned documents, classified by type: manual, SOP, RCA, drawing.
- [ ] Documents are linked to machines, lines or the plant as a whole.
- [ ] Original files are stored immutably with the same provenance guarantees as import files.
- [ ] Ingestion runs as a pollable async job with per-document status.

*Depends on:* `LS-051`, `LS-053` · *Blocks:* `LS-181`, `LS-184`

#### `LS-181` · Chunking and embedding with document-level provenance

`Story` · **P1 · Should** · **5 pts** · Sprint **S12** · AI · `knowledge-base`

> As the system, I need retrievable document chunks that remember where they came from, so that answers can cite a page rather than a file.

**Acceptance criteria**

- [ ] Documents are chunked with configurable size and overlap, respecting section boundaries where detectable.
- [ ] Every chunk retains document id, page number and section heading.
- [ ] Chunks are embedded using the same provider and dimension as record embeddings.
- [ ] Re-ingesting a document version supersedes the old chunks without breaking existing citations.

*Depends on:* `LS-180`, `LS-091` · *Blocks:* `LS-182`

### EPIC-19 — Proposal & Approval Inbox

**Goal:** The governed write path: agents propose, named humans dispose, everything reverts.  
**Component:** Product · **In this release:** 4 stories, 21 points

#### `LS-191` · Approval inbox API with filters and ageing

`Story` · **P0 · Must** · **5 pts** · Sprint **S10** · Product · `governance`

> As an engineer, I want one place showing everything waiting on me, so that proposals do not pile up unseen.

**Acceptance criteria**

- [ ] Inbox filterable by type, agent, risk, confidence and age; sortable by impact.
- [ ] Ageing indicators highlight proposals pending beyond the configured threshold.
- [ ] Each entry shows the evidence and a link to the full agent trace.
- [ ] Scoped to the caller's plants and roles.

*Depends on:* `LS-190` · *Blocks:* `LS-192`, `LS-194`, `LS-247`

#### `LS-192` · Approve and reject with effect application and reversibility

`Story` · **P0 · Must** · **8 pts** · Sprint **S11** · Product · `governance`

> As an engineer, I want approving a proposal to apply it safely and reversibly, so that a mistaken approval is not permanent.

**Acceptance criteria**

- [ ] Approval applies the effect transactionally and records the deciding user and timestamp.
- [ ] Every proposal type ships with an inverse operation; revert restores the prior state and is itself audited.
- [ ] Rejection requires a reason and feeds agent quality metrics.
- [ ] A partially applied effect can never be left behind — application either commits fully or rolls back.
- [ ] No agent-originated write reaches the database without a recorded human decision, verified by an integration test.

*Depends on:* `LS-191` · *Blocks:* `LS-193`, `LS-195`

#### `LS-193` · Autonomy-level policy gate on every agent write

`Story` · **P0 · Must** · **5 pts** · Sprint **S11** · Product · `governance` `agent`

> As a plant IT head, I want to decide how much autonomy each agent has, so that we expand trust deliberately rather than by default.

**Acceptance criteria**

- [ ] Policy gate evaluates agent, proposal type, risk and confidence against the tenant's autonomy level.
- [ ] At L3, whitelisted low-risk high-confidence proposals auto-apply but still create an auditable proposal row with the decision recorded as automatic.
- [ ] L4 external writes are unreachable: no proposal type targets an external system.
- [ ] Changing autonomy level takes effect immediately and is audited.

*Depends on:* `LS-192`, `LS-117` · *Blocks:* —

#### `LS-194` · Proposal notifications and reminders

`Story` · **P1 · Should** · **3 pts** · Sprint **S11** · Product · `governance` `notifications`

> As an engineer, I want to be told when something needs my decision, so that work does not stall in an inbox I forgot to open.

**Acceptance criteria**

- [ ] Notification on new proposals, routed by type and role.
- [ ] Reminders for proposals pending beyond the ageing threshold, rate-limited to avoid nagging.
- [ ] Per-user preferences and opt-out honoured.
- [ ] High-risk proposals can be configured to notify immediately.

*Depends on:* `LS-191`, `LS-159` · *Blocks:* —

### EPIC-24 — Frontend Product Application

**Goal:** Turn the demo prototype into the real multilingual product UI.  
**Component:** Frontend · **In this release:** 3 stories, 21 points

#### `LS-246` · Assistant UI with labelled blocks, citations and trace access

`Story` · **P0 · Must** · **8 pts** · Sprint **S10** · Frontend · `assistant`

> As a user, I want answers I can interrogate, so that trust comes from verification rather than from presentation.

**Acceptance criteria**

- [ ] Blocks render with trust badges driven by the wire-format label.
- [ ] Citations are clickable and open the source drawer.
- [ ] A trace toggle reveals which tools ran with what arguments, for engineers and above.
- [ ] Degraded and partial-answer states are rendered honestly with an explanation.
- [ ] Supports questions and answers in English, Hindi, Marathi and Hinglish.

*Depends on:* `LS-241`, `LS-123`, `LS-124` · *Blocks:* `LS-249`

#### `LS-248` · Multilingual UI across English, Hindi and Marathi

`Story` · **P0 · Must** · **5 pts** · Sprint **S10** · Frontend · `i18n`

> As a shop-floor user, I want the whole interface in my language, so that the product is usable by the people who generate the data.

**Acceptance criteria**

- [ ] Every screen, badge, empty state and error message is translated across all three languages.
- [ ] Language is switchable from the login screen and from the top bar, and persists per user.
- [ ] Numbers, dates and units are formatted per locale while the underlying values stay identical.
- [ ] Raw log entries and machine codes are never translated.

*Depends on:* `LS-240` · *Blocks:* —

#### `LS-247` · Approval inbox and agent trace viewer UI

`Story` · **P1 · Should** · **8 pts** · Sprint **S11** · Frontend · `governance`

> As an engineer, I want to review agent proposals with their full reasoning, so that approving something is an informed decision.

**Acceptance criteria**

- [ ] Inbox lists pending proposals with type, agent, confidence, risk and age.
- [ ] Each proposal shows its evidence and a link to the full agent trace.
- [ ] Trace viewer renders steps chronologically with tools, arguments, results, timings and cost.
- [ ] Approve, reject and revert are available inline with reason capture.

*Depends on:* `LS-241`, `LS-191`, `LS-118` · *Blocks:* —

---

## R4 — Industry Hardening

*Make it sellable to a second and third plant without heroics: compliant, observable, metered, recoverable and penetration-tested.*

### EPIC-02 — Identity, Tenancy & Access Control

**Goal:** Multi-tenant isolation and per-plant RBAC that is proven, not assumed.  
**Component:** Security · **In this release:** 2 stories, 13 points

#### `LS-027` · OIDC and SAML single sign-on for enterprise tenants

`Story` · **P2 · Could** · **8 pts** · Sprint **S14** · Security · `enterprise` `sso`

> As a plant IT head, I want staff to sign in with our corporate identity provider, so that access is centrally governed.

**Acceptance criteria**

- [ ] OIDC and SAML both supported, configurable per tenant.
- [ ] Group-to-role mapping configurable per tenant with a documented precedence order.
- [ ] Local password login can be disabled per tenant once SSO is enabled.
- [ ] Just-in-time user provisioning on first SSO login, with deactivation honoured.

*Depends on:* `LS-024` · *Blocks:* —

#### `LS-028` · Service accounts and scoped API keys

`Story` · **P2 · Could** · **5 pts** · Sprint **S14** · Security · `integrations`

> As an integrator, I want a non-human credential with narrow scope, so that automated imports do not run as a person.

**Acceptance criteria**

- [ ] API keys are hashed at rest, prefixed for identification and displayed exactly once.
- [ ] Each key carries explicit scopes and an optional expiry; scope violations return 403.
- [ ] Keys are listable, revocable and show last-used time.
- [ ] Key usage is attributed in audit logs as the service account, never as a user.

*Depends on:* `LS-024` · *Blocks:* —

### EPIC-14 — AI Evaluation & Quality Harness

**Goal:** Know whether a prompt change made the product better or worse, before shipping.  
**Component:** AI-Quality · **In this release:** 1 stories, 5 points

#### `LS-147` · Per-tenant production quality scorecard shown in-product

`Story` · **P1 · Should** · **5 pts** · Sprint **S13** · AI-Quality · `eval` `trust` `gtm`

> As a customer, I want to see the system's own accuracy on my data, so that I can trust it because it is transparent, not because it is confident.

**Acceptance criteria**

- [ ] Scorecard shows auto-approval rate, corrections per 100 records, queue burn-down time and resolver hit rate.
- [ ] Trends over time are visible, including the effect of each alias-mapping session.
- [ ] Visible to PLANT_ADMIN and above, and exportable for the customer's own reporting.
- [ ] Scores below the internal bar surface an explicit improvement action rather than being hidden.

*Depends on:* `LS-064`, `LS-086` · *Blocks:* —

### EPIC-17 — WhatsApp Field Agent

**Goal:** Capture new records where technicians already are, in the language they use.  
**Component:** Integrations · **In this release:** 1 stories, 5 points

#### `LS-177` · Per-technician phrasing memory

`Story` · **P2 · Could** · **5 pts** · Sprint **S13** · Integrations · `whatsapp` `memory`

> As a frequent reporter, I want the system to learn how I write, so that it stops asking me the same clarifying questions.

**Acceptance criteria**

- [ ] Per-technician vocabulary and phrasing patterns are stored in semantic memory.
- [ ] Learned phrasing reduces clarifying questions measurably over time.
- [ ] Learning is per plant and never shared across tenants.
- [ ] A technician can reset their learned profile; the reset is audited.

*Depends on:* `LS-174`, `LS-116` · *Blocks:* —

### EPIC-18 — Plant Knowledge Base

**Goal:** Ground answers in manuals, SOPs and past RCAs, not only in log rows.  
**Component:** AI · **In this release:** 4 stories, 24 points

#### `LS-182` · Unified retrieval across records and documents

`Story` · **P1 · Should** · **8 pts** · Sprint **S13** · AI · `knowledge-base`

> As a user, I want one search across history and manuals, so that I do not have to guess which source holds the answer.

**Acceptance criteria**

- [ ] A single retrieval call returns fused results from both records and document chunks.
- [ ] Result type is clearly distinguished so the UI and the agent can treat them differently.
- [ ] Callers can restrict to records only, documents only, or both.
- [ ] Ranking is evaluated by an extension of the retrieval golden set.

*Depends on:* `LS-181`, `LS-092` · *Blocks:* `LS-183`

#### `LS-183` · Document-grounded answers with page-level citations

`Story` · **P1 · Should** · **5 pts** · Sprint **S13** · AI · `knowledge-base` `trust`

> As an engineer, I want manual-based answers cited to the page, so that I can verify a torque spec before acting on it.

**Acceptance criteria**

- [ ] A search_documents tool is registered for the Copilot and the Scribe.
- [ ] Document-derived claims cite document, page and section.
- [ ] Document and record evidence are visually distinguished in the response schema.
- [ ] Manual-derived values are still subject to the numeric guardrail against the retrieved chunk text.

*Depends on:* `LS-182`, `LS-124` · *Blocks:* `LS-185`

#### `LS-184` · Access control for restricted documents

`Story` · **P1 · Should** · **3 pts** · Sprint **S13** · AI · `knowledge-base` `security`

> As a plant admin, I want to restrict sensitive documents, so that commercial contracts are not retrievable by every technician.

**Acceptance criteria**

- [ ] Documents carry a minimum role for retrieval, defaulting to the plant's standard visibility.
- [ ] Retrieval filters by the caller's role before ranking, so restricted content never reaches the model context.
- [ ] Restricted-document access attempts are audited.
- [ ] Covered by the role-matrix test suite.

*Depends on:* `LS-180`, `LS-024` · *Blocks:* —

#### `LS-185` · Job-plan generation from history and SOPs

`Story` · **P2 · Could** · **8 pts** · Sprint **S13** · AI · `knowledge-base` `scribe`

> As a new technician, I want to know how this plant usually fixes this failure, so that tribal knowledge is available without finding the veteran.

**Acceptance criteria**

- [ ] Generates a job plan from historical actions, parts consumed and relevant SOP sections.
- [ ] States how many past occurrences informed the plan and links to each.
- [ ] Explicitly marked as guidance drawn from history, not as an approved work instruction.
- [ ] Available in all supported languages.

*Depends on:* `LS-183`, `LS-160` · *Blocks:* —

### EPIC-19 — Proposal & Approval Inbox

**Goal:** The governed write path: agents propose, named humans dispose, everything reverts.  
**Component:** Product · **In this release:** 1 stories, 3 points

#### `LS-195` · Proposal outcome analytics per agent

`Story` · **P1 · Should** · **3 pts** · Sprint **S13** · Product · `governance` `metrics`

> As a product owner, I want to see which agents produce proposals people accept, so that autonomy is earned with evidence rather than granted by opinion.

**Acceptance criteria**

- [ ] Approval rate, rejection reasons and time-to-decision tracked per agent and proposal type.
- [ ] Trends visible over time and segmented per tenant.
- [ ] A low approval rate surfaces an explicit recommendation against raising that agent's autonomy level.
- [ ] Metrics feed the per-tenant scorecard in LS-147.

*Depends on:* `LS-192` · *Blocks:* —

### EPIC-20 — AI Observability, Cost & FinOps

**Goal:** Know the quality, latency and rupee cost of every agent run and every tenant.  
**Component:** Platform · **In this release:** 8 stories, 40 points

#### `LS-200` · Token, latency and cost recorded per run and per step

`Story` · **P0 · Must** · **5 pts** · Sprint **S13** · Platform · `finops` `observability`

> As the business, I want the rupee cost of every AI operation visible, so that pricing is grounded in measured unit economics.

**Acceptance criteria**

- [ ] Input and output tokens, model, latency and computed cost recorded on every step and aggregated per run.
- [ ] Cost computed from a configurable per-model rate table, versioned over time.
- [ ] Costs are attributable to tenant, plant, agent and trigger.
- [ ] Historical rate changes do not retroactively alter recorded costs.

*Depends on:* `LS-110` · *Blocks:* `LS-201`, `LS-205`

#### `LS-201` · Per-tenant cost ledger and monthly cost-per-plant report

`Story` · **P0 · Must** · **5 pts** · Sprint **S13** · Platform · `finops`

> As a founder, I want to know what each plant costs to serve, so that a subscription price is a margin decision rather than a guess.

**Acceptance criteria**

- [ ] Ledger aggregates AI, storage, WhatsApp and compute cost per tenant per month.
- [ ] Cost per plant per month is reportable and trendable.
- [ ] Costs are broken down by workload: extraction, assistant, watchtower, artifacts.
- [ ] The report is exportable and feeds the pricing model in the vision document.

*Depends on:* `LS-200` · *Blocks:* `LS-202`, `LS-230`

#### `LS-202` · Budget enforcement with soft warning and hard stop

`Story` · **P0 · Must** · **5 pts** · Sprint **S13** · Platform · `finops`

> As the business, I want a runaway tenant to be capped, so that one customer's usage cannot destroy the month's margin.

**Acceptance criteria**

- [ ] Per-tenant monthly budget with configurable soft-warning and hard-stop thresholds.
- [ ] Crossing the soft threshold notifies the account owner and internal operations.
- [ ] The hard stop degrades gracefully: deterministic features keep working, generative features are paused with a clear message.
- [ ] Budget state is visible in the admin UI and overridable by an authorised internal user, with the override audited.

*Depends on:* `LS-201`, `LS-114` · *Blocks:* —

#### `LS-203` · OpenTelemetry traces spanning API, agent, tool and model calls

`Story` · **P0 · Must** · **5 pts** · Sprint **S13** · Platform · `observability`

> As an engineer debugging a slow answer, I want one trace covering the whole path, so that I can attribute latency precisely.

**Acceptance criteria**

- [ ] A single trace spans the HTTP request, agent run, every tool call and every model call.
- [ ] Spans carry tenant, plant, agent, tool and model attributes.
- [ ] traceId from the error envelope correlates to the exported trace.
- [ ] Sampling is configurable, with errors and slow requests always sampled.

*Depends on:* `LS-013`, `LS-110` · *Blocks:* `LS-204`, `LS-223`

#### `LS-204` · Prompt and response sampling store with PII redaction

`Story` · **P1 · Should** · **5 pts** · Sprint **S13** · Platform · `observability` `privacy`

> As an engineer improving quality, I want real examples to learn from, so that prompt changes are informed by production rather than by guesses.

**Acceptance criteria**

- [ ] A configurable sample of prompts and responses is retained with a defined retention period.
- [ ] Technician names and phone numbers are redacted before storage.
- [ ] Sampling is disableable per tenant for customers who require it contractually.
- [ ] Access to samples is restricted and audited.

*Depends on:* `LS-203` · *Blocks:* —

#### `LS-205` · Model performance dashboard: quality against cost and latency

`Story` · **P1 · Should** · **5 pts** · Sprint **S13** · Platform · `observability` `finops`

> As a product owner, I want to compare model tiers on real workloads, so that routing decisions are evidence-based.

**Acceptance criteria**

- [ ] Dashboard compares tiers on evaluation quality, production latency and cost per operation.
- [ ] Segmented by task type: extraction, planning, composition, synthesis.
- [ ] Highlights where a cheaper tier would meet the quality bar.
- [ ] Used as the input to the quarterly routing review.

*Depends on:* `LS-200`, `LS-145` · *Blocks:* —

#### `LS-206` · Prompt and model version registry with rollback

`Story` · **P0 · Must** · **5 pts** · Sprint **S13** · Platform · `observability` `release`

> As an engineer, I want prompts versioned like code with a fast rollback, so that a bad change is reversed in minutes.

**Acceptance criteria**

- [ ] Every prompt is versioned; the version used is recorded on every step.
- [ ] Model and prompt versions are changeable by configuration without a code deployment.
- [ ] Rollback to a prior version is a single operation and is audited.
- [ ] Evaluation results are stored against each version for comparison.

*Depends on:* `LS-110` · *Blocks:* `LS-207`

#### `LS-207` · Canary rollout for prompt and model changes

`Story` · **P1 · Should** · **5 pts** · Sprint **S14** · Platform · `release`

> As an engineer, I want changes exposed to a slice of traffic first, so that a regression affects a few runs rather than every customer.

**Acceptance criteria**

- [ ] Traffic can be split between prompt or model versions at a configurable percentage.
- [ ] Guardrail violation rate, latency and cost are compared between arms automatically.
- [ ] Automatic rollback triggers when the canary arm breaches a configured threshold.
- [ ] Canary state and outcome are visible in the release dashboard.

*Depends on:* `LS-206`, `LS-135` · *Blocks:* —

### EPIC-21 — Security, Privacy & Compliance

**Goal:** Survive a plant IT head's security review and India's DPDP Act.  
**Component:** Security · **In this release:** 9 stories, 53 points

#### `LS-210` · Encryption at rest and in transit with key management

`Story` · **P0 · Must** · **5 pts** · Sprint **S14** · Security · `security`

> As a plant IT head, I want a clear encryption story, so that my security review can be completed rather than deferred.

**Acceptance criteria**

- [ ] TLS enforced on every external connection; internal service traffic encrypted where it crosses a trust boundary.
- [ ] Database and object storage encrypted at rest with managed keys.
- [ ] Key rotation procedure documented and rehearsed.
- [ ] Encryption posture is written into the one-page security FAQ from LS-006.

*Depends on:* `LS-021` · *Blocks:* `LS-218`

#### `LS-211` · DPDP Act 2023 compliance for technician personal data

`Story` · **P0 · Must** · **8 pts** · Sprint **S14** · Security · `compliance` `dpdp`

> As a compliance owner, I want India's data protection obligations met, so that handling technician names and numbers is lawful.

**Acceptance criteria**

- [ ] Personal data fields are inventoried with purpose and lawful basis documented.
- [ ] Consent capture and withdrawal implemented for WhatsApp phone-number binding.
- [ ] Erasure request handling removes or irreversibly pseudonymises personal data while preserving maintenance history integrity.
- [ ] Data-principal request handling has a documented SLA and an audit trail.
- [ ] Reviewed by legal counsel before the first production tenant.

*Depends on:* `LS-172`, `LS-016` · *Blocks:* `LS-213`

#### `LS-212` · Sub-processor register and zero-retention model configuration

`Story` · **P0 · Must** · **3 pts** · Sprint **S14** · Security · `compliance` `trust`

> As a plant head asking whether my data goes to a foreign AI company, I want an honest, documented answer, so that I can approve the pilot.

**Acceptance criteria**

- [ ] Every sub-processor listed with purpose, data categories and location.
- [ ] Zero-retention or enterprise API configuration is available and documented as the default posture.
- [ ] A contractual commitment that customer data is never used to train models is implemented and verifiable in configuration.
- [ ] The register is customer-facing and versioned; changes are notified per the DPA.

*Depends on:* `LS-060` · *Blocks:* —

#### `LS-213` · Customer data export and deletion on contract exit

`Story` · **P0 · Must** · **5 pts** · Sprint **S14** · Security · `compliance`

> As a departing customer, I want my data back and then deleted, so that the exit terms in the contract are real.

**Acceptance criteria**

- [ ] Full tenant export in open formats, including records, provenance, documents and audit logs.
- [ ] Deletion removes tenant data from primary storage, object storage and derived indexes within the contractual window.
- [ ] Backup expiry for deleted tenants is documented and enforced.
- [ ] A deletion certificate is produced and retained as evidence.

*Depends on:* `LS-211` · *Blocks:* —

#### `LS-214` · Secrets management and rotation runbook

`Story` · **P0 · Must** · **3 pts** · Sprint **S14** · Security · `security`

> As an operator, I want secrets managed properly, so that a leaked credential is a contained incident rather than a breach.

**Acceptance criteria**

- [ ] No secret is present in source control, container images or logs; CI scans enforce it.
- [ ] Secrets are loaded from a managed store or injected environment at runtime.
- [ ] Rotation procedure documented for every secret class, with an owner and a cadence.
- [ ] The application fails fast and loudly on a missing required secret in production.

*Depends on:* `LS-022` · *Blocks:* `LS-218`

#### `LS-215` · SAST, DAST, dependency and container scanning in CI

`Story` · **P0 · Must** · **5 pts** · Sprint **S14** · Security · `security` `ci`

> As a security owner, I want known vulnerability classes caught automatically, so that security is continuous rather than annual.

**Acceptance criteria**

- [ ] Static analysis, dependency scanning and container image scanning run on every PR.
- [ ] Dynamic scanning runs against staging on a schedule.
- [ ] High and critical findings block release; the exception process requires a named approver and an expiry.
- [ ] Findings are tracked to closure with an agreed remediation SLA.

*Depends on:* `LS-018` · *Blocks:* `LS-217`, `LS-218`

#### `LS-216` · Upload malware scanning

`Story` · **P1 · Should** · **3 pts** · Sprint **S14** · Security · `security`

> As a security reviewer, I want uploaded files scanned, so that the platform is not a malware distribution path between plants.

**Acceptance criteria**

- [ ] Files are scanned before processing; infected files are quarantined and the uploader is notified.
- [ ] Scanning failure blocks processing rather than failing open.
- [ ] Quarantined files are retained for investigation and are never downloadable by tenants.
- [ ] Scan outcomes are audited.

*Depends on:* `LS-050` · *Blocks:* —

#### `LS-217` · Third-party penetration test and remediation

`Story` · **P0 · Must** · **8 pts** · Sprint **S15** · Security · `security` `gtm`

> As a founder selling to enterprises, I want an independent security assessment, so that procurement has evidence rather than assurances.

**Acceptance criteria**

- [ ] Scope covers authentication, tenant isolation, IDOR, upload abuse, prompt injection and the agent write path.
- [ ] All high and critical findings remediated and retested before the report is shared.
- [ ] An executive summary is produced that can be shared with prospects under NDA.
- [ ] Findings are converted into regression tests so they cannot recur.

*Depends on:* `LS-025`, `LS-215` · *Blocks:* —

#### `LS-218` · SOC 2 Type I readiness

`Story` · **P1 · Should** · **13 pts** · Sprint **S15** · Security · `compliance` `enterprise`

> As a founder entering enterprise deals, I want the control framework in place, so that a SOC 2 requirement does not stall a signed deal for six months.

**Acceptance criteria**

- [ ] Control framework mapped to the trust services criteria, with gaps listed and owned.
- [ ] Required policies written and approved: access control, change management, incident response, vendor management, business continuity.
- [ ] Evidence collection automated where possible rather than assembled manually at audit time.
- [ ] A readiness assessment is completed and a remediation plan with dates is agreed.
- [ ] Treated as a sales enabler with a trigger, not as a prerequisite for the first pilots.

*Depends on:* `LS-210`, `LS-214`, `LS-215` · *Blocks:* —

### EPIC-22 — Reliability, SRE & Deployment

**Goal:** Ship safely, stay up, and be able to prove you can restore from backup.  
**Component:** Platform · **In this release:** 8 stories, 42 points

#### `LS-220` · Production container image and runtime configuration

`Story` · **P0 · Must** · **5 pts** · Sprint **S14** · Platform · `deployment`

> As an operator, I want a minimal, reproducible image, so that deployment is predictable and the attack surface is small.

**Acceptance criteria**

- [ ] Distroless or equivalent minimal base image running as a non-root user.
- [ ] Image build is reproducible and tagged with the commit SHA.
- [ ] Every environment-specific value is supplied by environment variable; the full matrix is documented.
- [ ] Flyway migration strategy on boot is explicit and documented for multi-instance startup.

*Depends on:* `LS-011` · *Blocks:* `LS-221`, `LS-227`

#### `LS-221` · Infrastructure as code for staging and production

`Story` · **P0 · Must** · **8 pts** · Sprint **S14** · Platform · `iac`

> As an operator, I want infrastructure defined in code, so that environments are reproducible and drift is visible.

**Acceptance criteria**

- [ ] Terraform (or equivalent) defines compute, database, object storage, networking and secrets.
- [ ] Staging and production share modules and differ only by variables.
- [ ] Plan output is reviewed in the PR before any apply; state is stored remotely with locking.
- [ ] A new environment can be stood up from scratch by following the documented procedure.

*Depends on:* `LS-220` · *Blocks:* `LS-222`, `LS-224`

#### `LS-222` · Blue/green deployment with automated rollback

`Story` · **P0 · Must** · **5 pts** · Sprint **S15** · Platform · `deployment`

> As an operator, I want deploys to be boring and reversible, so that shipping during the working day is safe.

**Acceptance criteria**

- [ ] New versions are deployed alongside the old and receive traffic only after health checks pass.
- [ ] Rollback is a single operation completing within the documented target time.
- [ ] Database migrations are backward-compatible so both versions can run during the switch.
- [ ] A deployment is proven and a rollback rehearsed in staging.

*Depends on:* `LS-221` · *Blocks:* —

#### `LS-223` · Service level objectives, error budgets and alerting

`Story` · **P0 · Must** · **5 pts** · Sprint **S15** · Platform · `sre`

> As an operator, I want defined reliability targets, so that 'is it working?' has a measurable answer.

**Acceptance criteria**

- [ ] SLOs defined for API availability, API latency, ingestion throughput and assistant answer latency.
- [ ] Error budgets tracked with a documented policy for what happens when one is exhausted.
- [ ] Alerts fire on SLO burn rate rather than on raw error counts, and route to a named on-call owner.
- [ ] Every alert links to the runbook entry that resolves it.

*Depends on:* `LS-203` · *Blocks:* `LS-225`, `LS-236`

#### `LS-224` · Backup, restore and a rehearsed disaster-recovery drill

`Story` · **P0 · Must** · **5 pts** · Sprint **S15** · Platform · `sre` `dr`

> As a customer, I want confidence that my three years of history survives an incident, so that adopting the product is not a data risk.

**Acceptance criteria**

- [ ] Automated backups of database and object storage with documented RPO and RTO targets.
- [ ] Restore procedure documented and executed end-to-end into a clean environment.
- [ ] The drill is timed and its result recorded; a missed target creates a follow-up item.
- [ ] The drill is scheduled to repeat quarterly with an owner.

*Depends on:* `LS-221` · *Blocks:* —

#### `LS-225` · Runbooks for the top ten operational failures

`Story` · **P0 · Must** · **3 pts** · Sprint **S15** · Platform · `sre` `docs`

> As an on-call engineer, I want a written procedure for likely incidents, so that recovery does not depend on who is awake.

**Acceptance criteria**

- [ ] Runbooks cover model provider outage, embedding provider outage, WhatsApp provider failure, database saturation, storage exhaustion, stuck import job, runaway agent cost, failed migration, tenant isolation alert and backup failure.
- [ ] Each runbook states symptoms, diagnosis steps, remediation and escalation path.
- [ ] Runbooks are linked from the corresponding alerts.
- [ ] Each is validated at least once against a simulated incident.

*Depends on:* `LS-223` · *Blocks:* —

#### `LS-226` · Load and soak testing at one million records

`Story` · **P0 · Must** · **8 pts** · Sprint **S15** · Platform · `performance`

> As an operator, I want performance characterised before a customer finds the limit, so that capacity planning is proactive.

**Acceptance criteria**

- [ ] A one-million-record dataset is generated with realistic distribution.
- [ ] Load tests cover search, dashboard, record listing and assistant queries at target concurrency.
- [ ] A soak test runs long enough to expose memory leaks and connection exhaustion.
- [ ] Slow queries are identified and indexed; results are documented as the capacity baseline.

*Depends on:* `LS-106`, `LS-092` · *Blocks:* —

#### `LS-227` · Feature-flag service for staged rollout

`Story` · **P1 · Should** · **3 pts** · Sprint **S15** · Platform · `release`

> As a product owner, I want features enabled per tenant, so that a design partner can trial something before it reaches everyone.

**Acceptance criteria**

- [ ] Flags evaluated per tenant and per user with a safe default when evaluation fails.
- [ ] Flag state is changeable without a deployment and every change is audited.
- [ ] Flags are listable with their owner and a removal date to prevent permanent accumulation.
- [ ] Flag state is recorded in the agent run policy snapshot where it affects behaviour.

*Depends on:* `LS-220` · *Blocks:* —

### EPIC-23 — Commercialization & Onboarding

**Goal:** Meter it, bill it, and onboard plant number three without a founder present.  
**Component:** GTM · **In this release:** 7 stories, 34 points

#### `LS-230` · Usage metering per tenant

`Story` · **P0 · Must** · **5 pts** · Sprint **S15** · GTM · `billing`

> As a founder, I want usage measured per tenant, so that billing and pricing reflect what customers actually consume.

**Acceptance criteria**

- [ ] Meters records ingested, questions asked, agent runs, artifacts generated, WhatsApp conversations and storage consumed.
- [ ] Metered data is aggregated per billing period and is immutable once the period closes.
- [ ] Usage is visible to the customer in-product, not only internally.
- [ ] Meter data reconciles with the cost ledger from LS-201.

*Depends on:* `LS-201` · *Blocks:* `LS-231`

#### `LS-231` · Plan tiers and entitlement enforcement

`Story` · **P1 · Should** · **5 pts** · Sprint **S15** · GTM · `billing`

> As a founder, I want plans enforced in the product, so that upgrades happen through the product rather than through a conversation.

**Acceptance criteria**

- [ ] Plan defines included plants, seats, agent features and usage allowances.
- [ ] Entitlements are enforced at the API boundary with a clear upgrade message, never a silent failure.
- [ ] Approaching a limit notifies the customer before the limit is reached.
- [ ] Plan changes take effect immediately and are audited.

*Depends on:* `LS-230` · *Blocks:* `LS-235`

#### `LS-232` · Self-serve tenant onboarding checklist

`Story` · **P1 · Should** · **5 pts** · Sprint **S15** · GTM · `onboarding`

> As a new plant admin, I want a guided setup, so that onboarding plant number three does not require a founder on site.

**Acceptance criteria**

- [ ] In-product checklist covering plant setup, machine import, user invites, first file import and first question.
- [ ] Progress is persisted and visible; each step links directly to the screen that completes it.
- [ ] Completion is measured as the onboarding funnel, with drop-off visible internally.
- [ ] A plant can reach its first answered question without any assistance from the vendor.

*Depends on:* `LS-035`, `LS-065` · *Blocks:* `LS-233`

#### `LS-233` · Time-to-first-answer instrumentation

`Story` · **P0 · Must** · **3 pts** · Sprint **S15** · GTM · `metrics`

> As a founder, I want to know how long a new plant takes to get value, so that the four-week promise is measured rather than asserted.

**Acceptance criteria**

- [ ] Measures elapsed time from tenant creation to first successfully answered question with citations.
- [ ] Intermediate milestones tracked: first import, first validated record, first search.
- [ ] Reported per tenant and as a cohort trend.
- [ ] Feeds the pilot scorecard from LS-008.

*Depends on:* `LS-232` · *Blocks:* —

#### `LS-234` · In-product return-on-investment report

`Story` · **P1 · Should** · **8 pts** · Sprint **S15** · GTM · `value` `retention`

> As a maintenance manager justifying renewal, I want evidence of value, so that the budget conversation is backed by data.

**Acceptance criteria**

- [ ] Reports downtime hours surfaced, recurring failures identified, engineer hours saved on reporting and validation, and records made searchable.
- [ ] Monetary value uses the plant's own configured downtime cost, never an industry average.
- [ ] Assumptions are stated explicitly and are adjustable by the customer.
- [ ] Exportable as a document for the customer's internal use.

*Depends on:* `LS-158`, `LS-031` · *Blocks:* —

#### `LS-235` · Invoicing export and subscription administration

`Story` · **P2 · Could** · **5 pts** · Sprint **S15** · GTM · `billing`

> As a founder, I want billing data exportable to accounting, so that invoicing does not become a manual monthly project.

**Acceptance criteria**

- [ ] Billing period data exportable in a format the accounting system accepts, including GST fields required in India.
- [ ] Subscription state, renewal dates and plan history are visible internally.
- [ ] Proration handled for mid-period plan changes.
- [ ] Export is reproducible for a closed period and never changes retroactively.

*Depends on:* `LS-231` · *Blocks:* —

#### `LS-236` · Public status page and incident communication

`Story` · **P2 · Could** · **3 pts** · Sprint **S15** · GTM · `trust`

> As a customer, I want to know when the service is degraded, so that I do not waste time diagnosing a problem that is not mine.

**Acceptance criteria**

- [ ] Public status page reflecting real health checks, not manual updates alone.
- [ ] Incident communication template and escalation path documented.
- [ ] Subscribers receive updates on incident open, update and resolution.
- [ ] Post-incident reviews are published to affected customers within the agreed window.

*Depends on:* `LS-223` · *Blocks:* —

### EPIC-24 — Frontend Product Application

**Goal:** Turn the demo prototype into the real multilingual product UI.  
**Component:** Frontend · **In this release:** 1 stories, 5 points

#### `LS-249` · Accessibility and responsive pass

`Story` · **P1 · Should** · **5 pts** · Sprint **S13** · Frontend · `accessibility`

> As a user on a tablet on the shop floor, I want the product to work on my device, so that it is usable away from a desk.

**Acceptance criteria**

- [ ] WCAG 2.1 AA conformance for contrast, focus order, keyboard navigation and screen-reader labelling.
- [ ] Responsive layouts verified on phone, tablet and desktop breakpoints.
- [ ] Charts carry accessible text alternatives conveying the same information.
- [ ] Automated accessibility checks run in CI with manual verification of the primary flows.

*Depends on:* `LS-242`, `LS-243`, `LS-246` · *Blocks:* —

---

# Critical path

The stories with the most downstream dependants. Slipping one of these slips a lot of other work, so they are the ones to protect, pair on, and never leave half-done.

| Story | Summary | Sprint | Directly blocks |
|---|---|---|---:|
| `LS-100` | Downtime, breakdown-count and record-count aggregates | S6 | 10 |
| `LS-110` | AgentRun and AgentStep persistence with a replayable trace schema | S7 | 8 |
| `LS-060` | Pluggable LlmClient port with retries, timeouts and a circuit breaker | S4 | 7 |
| `LS-092` | Hybrid retrieval with reciprocal-rank fusion | S6 | 7 |
| `LS-024` | Per-plant role assignment and a central PlantAccessService | S1 | 6 |
| `LS-061` | Schema-constrained extraction with per-field confidence | S4 | 6 |
| `LS-070` | MachineResolverService cascade: exact, alias, fuzzy, semantic | S4 | 6 |
| `LS-111` | Plan, act, observe, critique loop executor | S7 | 6 |
| `LS-123` | Typed answer blocks with trust labels | S8 | 6 |
| `LS-160` | Scribe Agent framework: evidence gathering to drafted document | S11 | 6 |
| `LS-241` | Design system extracted from the demo prototype | S2 | 6 |
| `LS-040` | Maintenance record entity, lifecycle and soft delete | S2 | 5 |
| `LS-052` | XLSX and CSV parsers producing verbatim raw records | S3 | 5 |
| `LS-082` | Approve, edit-and-approve and reject with conflict handling | S5 | 5 |
| `LS-190` | Proposal entity as the universal agent write envelope | S7 | 5 |

## Stories with no dependencies (safe parallel starts)

`LS-001`, `LS-005`, `LS-006`, `LS-010`, `LS-019`

