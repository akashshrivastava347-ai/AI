# LogSense — Agentic Maintenance Intelligence

> *"Your plant's entire breakdown history, searchable in plain Hindi/English, in 4 weeks,
> without a single sensor — and it doesn't wait to be asked."*

Product, architecture and delivery plan for turning the LogSense demo prototype and backend
blueprint into an industry-grade, agentic AI product for Indian manufacturing plants.

**This repository currently holds planning artifacts and the reference prototype. No
production code exists yet** — implementation starts at `LS-010` in the backlog below.

---

## Start here

| Read this | When you want |
|---|---|
| **[docs/00-PRODUCT-VISION.md](docs/00-PRODUCT-VISION.md)** | The idea, sharpened: why a reactive Q&A tool loses at week 4, and what replaces it. ICP, wedge, moat, autonomy ladder, pricing, non-goals |
| **[docs/01-AGENTIC-ARCHITECTURE.md](docs/01-AGENTIC-ARCHITECTURE.md)** | The technical design of the agentic and generative layer: seven agents, the runtime, tools, budgets, memory, guardrails, model routing, evals |
| **[docs/02-BACKLOG.md](docs/02-BACKLOG.md)** | **The work.** 199 stories across 25 epics, sprint-ordered with acceptance criteria and dependencies |
| **[docs/03-INDUSTRY-READINESS.md](docs/03-INDUSTRY-READINESS.md)** | Multi-tenancy, DPDP compliance, security, SRE, AI FinOps — with the trigger that makes each one urgent |
| **[docs/04-WAYS-OF-WORKING.md](docs/04-WAYS-OF-WORKING.md)** | Definition of ready and done, estimation, branching, and the rules for working on non-deterministic code |

## The plan in one table

| Release | Sprints | Theme | The milestone it unlocks |
|---|---|---|---|
| **R0** | S0–S1 | Validation & Foundation | A paid design partner signed; platform, tenancy and CI standing |
| **R1** | S2–S5 | The Pilot Slice | A real customer file imported end-to-end, **auto-approval rate measured on real data** |
| **R2** | S6–S9 | Intelligence | Search, analytics, agent runtime, Reliability Copilot, guardrails, evals |
| **R3** | S10–S12 | Proactive & Field | Watchtower briefings, generative artifacts, WhatsApp, the approval inbox |
| **R4** | S13–S15 | Industry Hardening | Compliant, observable, metered, recoverable, penetration-tested |

**199 stories · 25 epics · 1,021 points · 16 two-week sprints.**

R1 is the only release that can kill the company: it is where the messy-data promise meets
real plant files. Everything before it exists to reach it faster.

## What makes this different from "AI for maintenance"

Four properties that are structurally true rather than marketing claims — together, the
**Glass Box**:

1. **Every number is reproducible.** Computed by SQL, injected into the prompt, and
   re-verified against tool output after generation. The LLM never produces an operational
   figure.
2. **Every claim is citable.** Click any sentence, land on the original Excel row with the
   technician's own shorthand intact.
3. **Every agent run is replayable.** A persisted trace of every plan step, tool call,
   argument, result, token count and cost.
4. **Every agent action is human-approved.** Agents emit *proposals*; named humans approve
   them; every proposal has an inverse.

The sixth rule, added on top of the blueprint's original five: **agents propose, humans
dispose.** No agent-initiated change reaches plant reality without a recorded human decision.

## The backlog is code

`docs/02-BACKLOG.md` and `backlog/logsense-jira-import.csv` are **generated** from
`tools/backlog.py`, so the document and the board can never disagree about scope, points or
sequencing.

```bash
python3 tools/backlog.py            # regenerate both outputs
python3 tools/backlog.py --check    # validate only (wire into CI)
```

The validator enforces unique keys, resolvable references, non-empty acceptance criteria,
and — most usefully — that **no story is scheduled before a story it depends on**. It has
already caught real sequencing errors, including agentic stories planned before the agent
runtime they need.

Import `backlog/logsense-jira-import.csv` into Jira, Linear or Azure Boards: epics first,
then stories in sprint order, with priority, points, sprint, component, labels and
dependency columns.

## Repository layout

```
docs/                       vision, architecture, backlog, readiness, ways of working
backlog/                    generated Jira/Linear import CSV
tools/backlog.py            backlog as code — the source of truth for the plan
reference/
  logsense-backend/         original backend blueprint: 33 docs, 19 modules,
                            105 endpoints, 30 tables (design only, no code)
  logsense-demo/            clickable frontend prototype, EN/HI/MR, mock data
  logsense-founder-guide.md GTM and first-time-founder guidance
```

`reference/` is the prior work this plan builds on, vendored so that every document
reference resolves. The uploaded archive also contained an unrelated Spring Boot
store-management project, which was deliberately not vendored to keep this repository
focused.

## Running the prototype

```bash
cd reference/logsense-demo && python3 -m http.server 8000
# then open http://localhost:8000 and click "Demo login"
```

Nine-minute demo script: dashboard → import → validation queue → machine detail →
assistant → patterns → WhatsApp → closing. All data is fictitious demo-plant data.

## Non-goals

Scope discipline is a business weapon, not just an engineering preference:

- Not a CMMS — no work-order scheduling, planning or execution.
- No SAP or CMMS write-back, ever. Agents read the plant's world and write only into
  LogSense's own artifacts.
- No sensors, no IoT, no predictive ML models — the positioning is literally
  *"without a single sensor"*.
- No confirmed root causes. Agents rank **hypotheses**; only humans confirm.
- No fine-tuning on customer data. Learning lives in the resolver, dictionaries and semantic
  memory — which is what makes "we never train on your data" a structural fact rather than a
  promise.
