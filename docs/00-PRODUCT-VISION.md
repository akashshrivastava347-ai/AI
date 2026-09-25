# 00 — Product Vision: LogSense v2, the Agentic Reliability Colleague

> **V1 promise (unchanged, still the wedge):**
> *"Your plant's entire breakdown history, searchable in plain Hindi/English, in 4 weeks, without a single sensor."*
>
> **V2 promise (the improvisation):**
> *"…and it doesn't wait to be asked. Every morning it tells your engineers what is about to break, why it thinks so, and drafts the paperwork — with every number traceable to a real log line."*

---

## 1. What exists today

| Asset | State | Where |
|---|---|---|
| Clickable demo prototype (9-minute story, EN/HI/MR) | Working, mock data | `reference/logsense-demo/` |
| Backend architecture & API specification | 33 docs, 19 modules, 105 endpoints, 30 tables | `reference/logsense-backend/` |
| Founder/GTM guide | Written | `reference/logsense-founder-guide.md` |
| Production code | **None** | — |

The blueprint is unusually good for a pre-seed startup. Its five trust rules — numbers only
from SQL, every statement cited, hypothesis ≠ fact, low confidence goes to a human, raw data
is immutable — are the real intellectual property. **Nothing in this document weakens them.**
Everything here extends them.

## 2. The honest problem with V1 as designed

V1 is a **grounded question-answering system**. A user asks, a fixed six-step pipeline runs,
labelled blocks come back. It is correct, it is trustworthy, and it is *reactive*.

Reactive tools have a predictable failure curve in industrial pilots:

```
Week 1   Novelty. Everyone asks questions. Usage looks great.
Week 2   The obvious questions are answered. Usage halves.
Week 3   Engineers are firefighting; nobody opens a browser tab to ask a search box anything.
Week 4   "The pilot went fine" — and nobody renews.
```

The founder guide already names this risk in §9: *"If engineers stop asking questions in
week 3, the pilot is failing even if nobody says so."* A search box makes retention a
function of user discipline. That is the weakest possible foundation for a subscription in
a plant where the maintenance manager's actual job is interruption-driven.

**The fix is not more features. It is inverting who starts the conversation.**

## 3. The improvisation in one sentence

> Stop building a product people have to remember to use, and build a colleague that shows
> up with work already done — while keeping every claim it makes auditable back to a raw log
> line.

Three shifts, one thing deliberately held constant:

| # | Shift | From (V1) | To (V2) |
|---|---|---|---|
| 1 | **Reactive → Proactive** | User asks a question | Agents run on schedule and on events, and deliver briefings, alerts and recurrence warnings |
| 2 | **Fixed pipeline → Planned investigation** | One hard-coded 6-step chain | A planner chooses the next tool based on what it just learned, within a hard budget |
| 3 | **Answers → Artifacts** | Chat blocks on a screen | RCA drafts, shift-handover notes, PM-revision proposals, monthly reviews, spare-stocking recommendations |
| — | **Held constant: agency ≠ authority** | Human validates low-confidence data | **Every agent write is a _Proposal_ a human approves.** No agent ever mutates plant reality on its own |

Shift 3 is the commercial one. A maintenance manager will not pay ₹40k/month for a better
search bar. They will pay for something that removes Sunday-evening report writing and
catches the failure that costs ₹1,25,000 per line-hour.

## 4. The moat: the Glass Box

Every AI competitor in this space will eventually claim "AI for maintenance". The
differentiator is not the model — it is what the customer can *inspect*.

LogSense's architecture makes four properties structurally true, not marketing claims:

1. **Every number is reproducible.** Computed by SQL, injected into the prompt, and
   re-verified against tool output after generation. Same data → same number, forever,
   across model upgrades.
2. **Every claim is citable.** Click any sentence, land on the original Excel row with the
   technician's own messy handwriting-turned-text intact.
3. **Every agent run is replayable.** A persisted trace of every plan step, tool call,
   argument, result, token count and cost — replayable against recorded outputs. When a
   plant head asks *"why did it say that?"*, you show them, step by step.
4. **Every action is human-approved.** The approval inbox is the product's conscience and
   its best demo moment.

That is the **Glass Box**. It is the opposite of "trust the AI", and it is exactly what a
plant head who has been burned by a dashboard vendor needs to hear. It is also the honest
answer to *"why not just use ChatGPT?"* — ChatGPT cannot cite your Line 3 conveyor motor's
2023 bearing failures, and it will happily invent a downtime figure.

## 5. The autonomy ladder (how we sell agency without scaring anyone)

Agency is a slider per tenant, not a binary. This framing de-risks enterprise procurement
and gives a natural expansion path.

| Level | Name | What the agent may do | Default |
|---|---|---|---|
| **L0** | Observe | Read and log only. No user-visible output. | Shadow mode for new tenants |
| **L1** | Inform | Answer questions, produce briefings and alerts. | **Pilot default** |
| **L2** | Propose | Draft artifacts (RCA, handover, PM change) and data proposals (column maps, aliases) into an approval inbox. | Month 2+ |
| **L3** | Auto-apply (bounded) | Apply only reversible, low-risk, high-confidence, explicitly whitelisted actions — e.g. auto-approving extractions above the plant's confidence threshold. | Opt-in per action type |
| **L4** | Write to external systems (SAP/CMMS write-back) | — | **Never. Out of scope by product principle.** |

L4 stays closed on purpose. The founder guide's §7 warning is right: drifting into CMMS
replacement destroys the wedge ("keep everything you have, we make it searchable"). Agents
read the plant's world and write only into LogSense's own artifacts.

## 6. The agent roster

Seven named agents, each with a job a human would recognise. Full technical design in
[`01-AGENTIC-ARCHITECTURE.md`](01-AGENTIC-ARCHITECTURE.md).

| Agent | Trigger | What it does | Writes |
|---|---|---|---|
| **Intake** | File uploaded | Profiles the sheet, proposes the column mapping, sample-extracts, self-scores quality before committing to a 2,000-row run | Proposal: column map |
| **Extraction** | Import batch | Schema-constrained extraction of date/machine/failure/action/parts/downtime from Hinglish shorthand, with per-field confidence | Staged records |
| **Resolver** | Per row, and on validation | `"Conv Motor-3"` → `CONV-L3-MTR-01`; asks the one clarifying question that unblocks 37 rows; learns the alias permanently | Proposal: alias |
| **Copilot** | User question | Multi-step investigation: history → similar failures → parts → patterns → cross-machine, replanning as it learns | Nothing (read-only) |
| **Watchtower** | Cron + events | Runs detectors, triages and ranks findings, composes the morning briefing, fires recurrence alerts | Patterns, briefings |
| **Field** | WhatsApp inbound | Slot-filling dialogue in Hinglish; asks only what's missing; tells the technician "this is the 5th bearing on this motor" | Staged records |
| **Scribe** | Request or schedule | Drafts RCA documents, shift handovers, monthly reliability reviews, PM-change proposals | Proposal: document |

Plus a **Verifier** pass — deterministic numeric/citation/label checks — gating every
user-visible generative output. The Verifier is not optional and cannot be disabled.

## 7. What genuinely changes for the customer

| Moment | V1 experience | V2 experience |
|---|---|---|
| Monday 7:00 am | — | Maintenance manager's phone: *"3 findings. Line 3 conveyor bearing is 4 days from its 92-day recurrence window. Line 2 VFD trips now on 3 machines. Weekend downtime 6.2 h, 71% on Line 4."* |
| A breakdown happens | Engineer searches, reads, decides | Copilot has already assembled history, similar failures across the plant, part consumption and the ranked hypotheses — as a briefing, not a search result |
| After the breakdown | Engineer writes the RCA in Word, badly, on Friday | Scribe drafts the 5-Why with evidence pre-filled and cited; engineer edits and approves in 10 minutes |
| Shift change | Verbal handover, knowledge evaporates | Handover note generated from the shift's records, reviewed in 2 minutes |
| Month end | Manager builds slides from memory | Monthly reliability review draft, every number traceable |
| New technician joins | Asks whoever remembers | Asks LogSense "how do we usually fix this?" and gets the plant's own history + SOP |

## 8. Ideal customer profile & wedge (unchanged, sharpened)

- **ICP:** discrete/process manufacturing plants in India, 100–1,000 employees, 3–10 lines,
  existing maintenance history in Excel/SAP exports, downtime cost ≥ ₹50,000/line-hour.
- **Economic buyer:** Plant Head or IT Head. **Champion:** Maintenance Manager. **Daily
  users:** reliability engineers + technicians (WhatsApp).
- **Wedge:** *"Keep every system you have. In 4 weeks your last 3 years of maintenance
  history becomes searchable in Hindi, English or Hinglish — and then it starts warning you."*
- **Real competitor:** Excel + institutional memory + "we manage". Not another vendor.
- **Moat:** Hinglish/shorthand/regional-language extraction accuracy on genuinely messy
  Indian plant data, compounded by per-plant alias and dictionary learning. Every correction
  a customer makes deepens their own switching cost — and none of it requires model training.

## 9. Pricing hypothesis

Value-anchored, per the founder guide §6 (do not price like a ₹2k SaaS tool):

| Tier | Target | Price (hypothesis, to be validated) | Includes |
|---|---|---|---|
| **Pilot** | One plant, 4 weeks | ₹75,000 one-time | Import + search + assistant, L1 autonomy |
| **Plant** | Per plant / month | ₹35,000–₹60,000 | Full V1 + Watchtower briefings, L2 autonomy, 10 seats |
| **Group** | 3+ plants | Negotiated, per-plant discount | Cross-plant analytics, SSO, knowledge base |
| **Add-on** | Knowledge Base (manuals/SOPs/RCA corpus) | +₹10,000/plant/month | Document-grounded answers |

Gate the price on one number: if LogSense surfaces one avoidable line-hour per month at
₹1,25,000/hour, a ₹50,000/month subscription returns 2.5×. Instrument that claim in-product
(story `LS-234`, the ROI report) rather than asserting it in a deck.

## 10. The number the whole business rests on

From the founder guide §2, restated as an engineering SLO rather than an aspiration:

> **Auto-approval rate** — the % of real customer rows that extract at high enough confidence
> to skip human review.

- Demo: ~97% (1,747/1,790). **Real messy data: assume 60% until measured.**
- Internal bar: **≥85% after the first alias-mapping session.** Below that, the pilot is a
  *product* problem, not a sales problem.
- It is measured per tenant, in production, continuously (`LS-147`), and shown to the
  customer. Transparency on this metric is a trust asset, not a liability.

Secondary truth-telling metrics: corrections per 100 records, validation-queue burn-down
time, resolver precision@1, answer numeric accuracy (**must be 100%**), weekly active
engineers, WhatsApp records/week, time-to-first-answer for a new user.

## 11. Explicit non-goals (scope discipline is a business weapon)

Carried forward from `reference/logsense-backend/docs/27-v1-vs-future.md` and extended for
the agentic layer:

- ❌ Not a CMMS. No work-order scheduling, planning or execution.
- ❌ No SAP/CMMS write-back, ever (L4 autonomy is closed).
- ❌ No sensors, no IoT ingestion, no predictive-maintenance ML models. The positioning is
  literally "without a single sensor".
- ❌ No confirmed root causes. Agents produce ranked **hypotheses**; only humans confirm.
- ❌ No free-form text-to-SQL. Numbers come only from whitelisted, argument-validated tools.
- ❌ No autonomous external actions — no emails to vendors, no purchase orders, no
  write-backs. Agents propose; humans dispose.
- ❌ No model fine-tuning on customer data. Corrections improve the **resolver and
  dictionaries**, not the model. This is what lets you tell a plant "we never train on your
  data" and mean it.
- ❌ No Kubernetes, Kafka, Elasticsearch or microservices until the documented triggers fire.

## 12. Staging the bet

| Release | Theme | Business milestone it unlocks |
|---|---|---|
| **R0** | Validation & foundation | Design partner signed; repo, CI, tenancy, auth live |
| **R1** | The pilot slice | One real customer file imported end-to-end; **auto-approval % measured on real data** |
| **R2** | Intelligence | Search, analytics, agent runtime, Copilot, guardrails, evals — the plant can ask anything |
| **R3** | Proactive & field | Watchtower briefings, generative artifacts, WhatsApp — the product stops waiting |
| **R4** | Industry hardening | Multi-tenant, DPDP-compliant, SOC 2-ready, metered and billable — sellable to a second and third plant without heroics |

R1 is the only release that can kill the company. It is where the messy-data promise meets
real files. Everything before it exists to reach it faster; everything after it assumes it
succeeded.

Full story-by-story plan: [`02-BACKLOG.md`](02-BACKLOG.md).
