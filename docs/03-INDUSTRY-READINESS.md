# 03 — Industry Readiness

What separates a working demo from something a manufacturing group will run on their plant
data. Each section states the bar, the stories that reach it, and — importantly — the
**trigger** that makes it urgent. Building all of this before the first pilot would be as
much a mistake as building none of it before the tenth.

> **Sequencing principle:** the first pilot needs *credibility*, the tenth needs
> *compliance*. Do not buy a SOC 2 audit before you have a paying customer, and do not sell
> to a third plant without tenant isolation you can prove.

---

## 1. Multi-tenancy

| | |
|---|---|
| **Bar** | A bug in application code cannot leak data across tenants |
| **Stories** | `LS-020`, `LS-021`, `LS-113` |
| **Trigger** | The second customer. Non-negotiable before then |

Model: `Organisation → Plant → Line → Machine`. Every business table carries a non-null
`tenant_id`, and every composite index leads with it.

Defence in depth, because one layer always eventually fails:

1. **PostgreSQL row-level security** — the database refuses cross-tenant rows regardless of
   what the query says. This is the authority.
2. **Hibernate interceptor** — sets the tenant GUC on connection checkout.
3. **ArchUnit rule** — an unscoped repository method fails the build.
4. **Automated probe suite** (`LS-021`) — attempts cross-tenant access on every endpoint and
   expects `404`.

**`404`, never `403`.** A `403` confirms the resource exists, which tells an attacker (or a
competitor with a trial account) that a given plant is a customer. Existence is itself
confidential.

The probe suite's report is a sales asset: hand it to a plant IT head and the isolation
conversation ends in one meeting instead of three.

## 2. Data privacy — India DPDP Act 2023

| | |
|---|---|
| **Bar** | Technician personal data is processed lawfully and erasable on request |
| **Stories** | `LS-006`, `LS-172`, `LS-211`, `LS-212`, `LS-213` |
| **Trigger** | The first pilot that touches a real technician's name or phone number |

The personal data in this product is narrow but real: technician names in maintenance
records, and phone numbers bound to WhatsApp identities. That is enough to be a Data
Fiduciary under the DPDP Act.

Required before the first production tenant:

- **Inventory** of every personal-data field with purpose and lawful basis.
- **Consent** captured and withdrawable for WhatsApp phone-number binding, with timestamp
  and purpose recorded (`LS-172`).
- **Erasure** that removes or irreversibly pseudonymises personal data *while preserving
  maintenance history integrity* — the breakdown record survives, the person's identity does
  not (`LS-211`).
- **Data-principal request handling** with a documented SLA and audit trail.

### The question every plant will ask

> *"Does our maintenance data go to a foreign AI company?"*

Have the honest answer ready before it is asked, not after (`LS-212`):

- A **sub-processor register**, customer-facing and versioned, naming every processor, what
  it receives and where it runs.
- **Zero-retention / enterprise API configuration as the default posture**, not an upsell.
- A **contractual commitment never to train on customer data** — which the architecture
  makes genuinely true, because learning lives in the resolver, dictionaries and semantic
  memory rather than in model weights (see `01-AGENTIC-ARCHITECTURE.md` §2.5).

That third point is worth more than any security certification in an early sales
conversation, because it is a structural claim rather than a promise.

## 3. Security

| | |
|---|---|
| **Bar** | OWASP ASVS Level 2; no high findings open at release |
| **Stories** | `LS-025`, `LS-026`, `LS-050`, `LS-134`, `LS-210`, `LS-214` – `LS-217` |
| **Trigger** | Continuous. The pen test (`LS-217`) triggers on the first enterprise deal |

| Area | Control | Story |
|---|---|---|
| Authentication | Short-lived access tokens, refresh rotation, reuse detection, lockout | `LS-022`, `LS-026` |
| Authorization | Per-plant RBAC through one service; generated role-matrix suite covering every endpoint | `LS-024`, `LS-025` |
| IDOR | Ownership-scoped queries returning `404`; probed automatically | `LS-021`, `LS-025` |
| Upload abuse | Magic-byte validation, size caps, XXE-safe parsers, malware scanning | `LS-050`, `LS-216` |
| Prompt injection | Fenced data, whitelisted tools, no direct-write tools, output verification | `LS-134` |
| Secrets | Never in source, images or logs; managed store; documented rotation | `LS-214` |
| Supply chain | SAST, DAST, dependency and container scanning gating release | `LS-215` |
| Encryption | TLS everywhere; at-rest encryption with rotation procedure | `LS-210` |

**The agentic addition to the threat model.** Traditional security asks "can an attacker
reach data they shouldn't?" An agentic product must also ask "can an attacker make the
system *act*?" The answer here is structural: no tool has direct write access, so the worst
outcome of a successful prompt injection is a *proposal* a human then rejects (`LS-190`,
`LS-192`). Include the agent write path explicitly in the pen test scope.

## 4. Reliability & SRE

| | |
|---|---|
| **Bar** | Defined SLOs with alerting, and a rehearsed restore |
| **Stories** | `LS-220` – `LS-227` |
| **Trigger** | The first customer who depends on it during their shift |

Starting SLO set — deliberately modest, because an SLO you miss is worse than one you did
not publish:

| Service | Target | Notes |
|---|---|---|
| API availability | 99.5% → 99.9% | Raise only once you have on-call cover, not before |
| API latency (p95) | < 800 ms | Excluding assistant and agent endpoints |
| Assistant answer (p95) | < 8 s | Multi-step investigations get their own budget |
| Ingestion throughput | ≥ 2,000 rows / 10 min | The pilot-sized file, end to end |
| Data durability | RPO 24 h, RTO 4 h | Tightened when a customer contracts for it |

**A backup you have never restored is not a backup.** `LS-224` requires an actual timed
restore into a clean environment, repeated quarterly with a named owner. Most startups
discover their restore is broken during the incident.

Runbooks (`LS-225`) cover the ten failures this architecture actually has — model provider
outage, embedding provider outage, WhatsApp provider failure, database saturation, storage
exhaustion, stuck import job, runaway agent cost, failed migration, tenant isolation alert,
backup failure. Each is linked from the alert that fires it.

## 5. Delivery engineering

| | |
|---|---|
| **Bar** | Any engineer can ship safely on their first week |
| **Stories** | `LS-011`, `LS-012`, `LS-018`, `LS-146`, `LS-206`, `LS-207`, `LS-221`, `LS-222`, `LS-227` |
| **Trigger** | The second engineer |

- **Trunk-based** with short-lived branches. Long-lived branches and a two-person team are a
  bad combination.
- **PR gates**: build, unit and integration tests on Testcontainers, coverage, ArchUnit
  boundaries, migration lint, OpenAPI diff, and — uniquely for this product — the
  **AI evaluation gate** (`LS-146`).
- **Forward-only migrations.** Never a destructive down-migration against customer data.
- **Blue/green with automated rollback** (`LS-222`), which requires backward-compatible
  migrations so both versions can run during the switch.
- **Infrastructure as code** (`LS-221`) — a new environment from scratch by following a
  document, not by remembering.
- **Feature flags** (`LS-227`) with an owner and a removal date, so they do not accumulate
  into permanent dead configuration.

### The gate that is specific to this product

Ordinary software has tests: same input, same output, pass or fail. This product has a
component that is **non-deterministic and silently degradable** — a prompt change can make
answers subtly worse in a way no unit test catches and no reviewer notices.

`LS-145` and `LS-146` are therefore not "nice testing hygiene", they are the release gate.
Numeric accuracy and the safety suite are **absolute** (no tolerance); everything else has a
declared regression tolerance. Without this, you will ship a quality regression to a paying
plant and find out from them.

## 6. AI FinOps

| | |
|---|---|
| **Bar** | Cost per plant per month is measured, attributable and capped |
| **Stories** | `LS-062`, `LS-114`, `LS-200` – `LS-202`, `LS-205` |
| **Trigger** | Before pricing is quoted to the second customer |

The founder guide is right that unit economics must be known from day one. Concretely:

| Lever | Mechanism | Story |
|---|---|---|
| Prompt caching | Static prefix (schema + dictionary + plant context) cached across thousands of extraction calls | `LS-062` |
| Batching | ~20 rows per extraction call | `LS-062` |
| Tier routing | Fast tier for extraction, balanced for dialogue, deep only for synthesis | `LS-115` |
| Observation summarisation | Multi-step runs never carry raw tool JSON forward | `LS-111` |
| Run budgets | Hard ceiling per run on steps, tokens, cost and wall-clock | `LS-114` |
| Tenant budgets | Soft warning, then graceful hard stop that keeps deterministic features alive | `LS-202` |

**Cost is a product metric, not a finance metric.** A tenant whose cost per month exceeds
their subscription is a product problem with a deadline. `LS-201` makes that visible monthly
rather than at the annual review.

## 7. Commercial readiness

| | |
|---|---|
| **Bar** | Plant number three onboards without a founder in the room |
| **Stories** | `LS-230` – `LS-236`, `LS-232`, `LS-147` |
| **Trigger** | The third customer, or the first one you did not personally sell |

- **Metering** (`LS-230`) of records, questions, agent runs, artifacts, WhatsApp
  conversations and storage — visible to the customer, not only internally.
- **Entitlements enforced at the API boundary** with a clear upgrade path, never a silent
  failure.
- **Self-serve onboarding checklist** (`LS-232`) taking a new plant to its first answered
  question unaided — which is also the honest test of whether the four-week promise is real.
- **Time-to-first-answer** (`LS-233`) measured per tenant, because that is the promise.
- **In-product ROI report** (`LS-234`) using the plant's *own* configured downtime cost, not
  an industry average. Renewal conversations should be arithmetic, not persuasion.
- **Quality scorecard** (`LS-147`) shown to the customer. Showing your own accuracy — including
  when it is imperfect — is the strongest trust move available, and it is very hard for a
  competitor to copy because it requires actually being good.

## 8. Compliance sequencing (what to do when)

| Milestone | Do now | Explicitly defer |
|---|---|---|
| **Before first pilot** | NDA, DPA, security FAQ, sub-processor register, encryption, tenant isolation | SOC 2, SSO, pen test, status page |
| **Before second customer** | Proven tenant isolation suite, backup + restore drill, audit coverage, DPDP erasure | SOC 2 audit, SCIM |
| **Before first enterprise deal** | Pen test (`LS-217`), SSO (`LS-027`), SLOs with alerting, runbooks | SOC 2 Type II, multi-region |
| **Before Series A / large group** | SOC 2 Type I (`LS-218`), formal incident process, status page | Multi-region HA, data warehouse |

**SOC 2 is a sales enabler with a trigger, not a prerequisite.** `LS-218` is deliberately
scheduled in R4 and marked P1. Pulling it earlier burns runway on controls nobody has asked
for yet. Pulling it *later* than the first enterprise procurement conversation costs a deal.

## 9. Scale triggers (when to add the expensive things)

Carried forward from `reference/logsense-backend/docs/27-v1-vs-future.md`, because scope
discipline is a business weapon and every one of these has an operational cost:

| Addition | Add it when — and only when |
|---|---|
| Kafka or an event broker | A second deployable, or an external consumer of domain events, actually exists |
| Elasticsearch / OpenSearch | Corpus well beyond 10⁷ records, or relevance needs exceed what rank fusion gives |
| Microservice extraction | Team beyond roughly eight engineers, or ingestion and AI genuinely need independent scaling |
| Kubernetes | More than a handful of instances. One VM or a managed container runs V1 fine |
| Redis | Multi-instance cache coherence or distributed rate limiting is genuinely needed |
| Multi-region HA | A signed contract demands it |
| Data warehouse / BI export | Analytics needs exceed the operational dashboard |

Each of these is a real cost in operational complexity, on-call burden and hiring. The
architecture is shaped so that adding them later is an extraction, not a rewrite — which is
exactly why they can wait.
