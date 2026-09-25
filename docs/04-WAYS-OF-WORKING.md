# 04 — Ways of Working

How the backlog in [`02-BACKLOG.md`](02-BACKLOG.md) actually gets delivered. Short on
ceremony, because a team of two to six people does not need a process framework — it needs
agreement on what "done" means and a rule for what to do when the plan meets reality.

---

## 1. Cadence

| | |
|---|---|
| **Sprint length** | 2 weeks |
| **Planning** | 1 hour at sprint start — pull from the top of the backlog, do not re-plan the world |
| **Daily sync** | 10 minutes, blockers only. Not a status parade |
| **Review** | 30 minutes — **demo against acceptance criteria**, not against slides |
| **Retro** | 30 minutes, every second sprint, with one committed action |

The sprint point totals in the backlog are an **estimate made before the team existed**.
After two sprints, measure actual velocity and rebalance. Do not treat the plan's numbers as
a commitment you have to hit — treat them as a hypothesis you are testing.

## 2. Definition of Ready

A story is not pulled into a sprint until:

- [ ] Acceptance criteria are written and are objectively verifiable.
- [ ] Dependencies are done or scheduled earlier (the generator enforces the ordering).
- [ ] It is estimated, and the estimate is 8 points or fewer. **A 13 gets split first.**
- [ ] For AI stories: the evaluation case that will prove it works is identified.
- [ ] For API stories: the contract is agreed with whoever consumes it.

## 3. Definition of Done

A story is done when **every one** of these is true. Not most.

- [ ] Every acceptance criterion demonstrably passes — demoed, not asserted.
- [ ] Tests written at the right level: unit for logic, integration on Testcontainers for
      persistence and API, contract tests for the wire format.
- [ ] Coverage gate passes; no new ArchUnit violations.
- [ ] Migrations are forward-only and run cleanly against a copy of realistic data.
- [ ] OpenAPI spec regenerated; any breaking change is deliberate and flagged.
- [ ] Audit rows written for every consequential action.
- [ ] Tenant scoping applied and covered by the cross-tenant probe suite.
- [ ] For AI changes: the evaluation suite runs and does not regress.
- [ ] Observability: the new path emits traces and metrics.
- [ ] Documentation updated where behaviour changed; an ADR written if a decision was made.
- [ ] Reviewed and merged to trunk. **Not "done on my branch".**

### The two absolute gates

Everything above has judgement in it. These two do not:

1. **Numeric accuracy on the assistant golden set must be 100%.** Not 99%. A single
   fabricated number in front of a plant head ends the deal, and the guardrail exists
   precisely so that this is enforceable rather than aspirational.
2. **The safety suite must pass completely.** Prompt injection, out-of-scope handling and
   cross-tenant probes have no tolerance band.

If either fails, the build fails. There is no override label for these.

## 4. Estimation

Modified Fibonacci: 1, 2, 3, 5, 8, 13.

| Points | Means |
|---|---|
| 1 | Trivial, well understood, under half a day |
| 2 | Small, no unknowns |
| 3 | Standard story, one or two days |
| 5 | Substantial, some unknowns, most of a sprint week |
| 8 | Large. Fine, but it is the biggest thing one person carries at a time |
| 13 | **Too big.** Split it, or make it a spike first |

Estimate *relative complexity and uncertainty*, not hours. The one 13 in the backlog
(`LS-218`, SOC 2 readiness) stays whole because it is an externally driven programme rather
than a divisible engineering task.

## 5. Branching and review

- Trunk-based. Branch names: `feat/LS-123-short-description`, `fix/…`, `chore/…`.
- **One story per PR** wherever possible. A PR that closes three stories is a PR nobody
  reviews properly.
- Commit messages reference the story key: `LS-123: add numeric guardrail`.
- Every PR needs one approving review. Self-merge only for documentation typos.
- CI must be green before merge. **Never merge red with the intention of fixing it after** —
  that is how a broken trunk blocks everyone.

## 6. Working with AI-dependent code

This product's hardest engineering problem is that part of it is non-deterministic. Rules
that keep that manageable:

1. **Never assert on exact LLM output in a unit test.** Assert on structure, on schema
      conformance, and on guardrail behaviour. Quality belongs in the evaluation suite.
2. **Every AI feature ships with evaluation cases.** A prompt without an eval case is
      unverifiable and will silently regress.
3. **Prompts are versioned like code** (`LS-206`). The version used is recorded on every
      step, so a quality change is always attributable.
4. **Use the fake LLM client in CI.** Tests that call a live provider are slow, flaky and
      expensive, and they fail when the provider has an incident.
5. **Replay before you theorise** (`LS-119`). When an answer is wrong, replay the run against
      its recorded tool outputs rather than guessing at the prompt.
6. **A guardrail violation is a bug, not a curiosity.** Rising violation rates are a rollback
      trigger (`LS-135`, `LS-207`).

## 7. When the plan meets reality

It will. Rules for the common cases:

| Situation | What to do |
|---|---|
| A story is bigger than estimated | Split it mid-sprint. Do not silently carry a half-done story across the boundary |
| A dependency slipped | Re-sequence in `tools/backlog.py` and regenerate — the validator will catch any ordering you break |
| Scope pressure at the end of a release | Cut `P2` first, then `P1`. **Never cut a `P0`** — if a `P0` must go, the release date moves instead |
| A pilot reveals a wrong assumption | That is the pilot working. Rewrite the affected stories; do not build the wrong thing on schedule |
| Auto-approval rate is below the bar | Stop feature work. This is the number the business rests on (`LS-064`, `LS-147`) |

**The last row is the important one.** The temptation when a pilot underperforms is to ship
more features to compensate. The founder guide is right: a pilot below the auto-approval bar
is a *product* problem, and no amount of new surface area fixes it.

## 8. Maintaining the backlog

The backlog is code. Edit [`tools/backlog.py`](../tools/backlog.py), then:

```bash
python3 tools/backlog.py            # regenerate the doc and the Jira CSV
python3 tools/backlog.py --check    # validate only — wire this into CI
```

The validator enforces:

- Unique story keys.
- Every epic, sprint and priority reference resolves.
- Every story has acceptance criteria.
- **No story is scheduled before a story it depends on.** This has already caught real
  sequencing errors — agents planned before the runtime they need, and a benchmark scheduled
  before its own golden data set.

Never hand-edit `docs/02-BACKLOG.md` or `backlog/logsense-jira-import.csv`; both are
generated, and an edit will be overwritten on the next run.

### Importing into a tracker

`backlog/logsense-jira-import.csv` carries epics first, then stories in sprint order, with
`Issue Type`, `Issue Key`, `Epic Key`, `Priority`, `Story Points`, `Sprint`, `Component`,
`Labels`, `Depends On` and `Blocks`. Jira, Linear and Azure Boards all accept this shape;
map `Epic Key` to the parent link and `Depends On` to the blocking relationship during
import.

Keep `tools/backlog.py` as the source of truth even after import, or accept the tracker as
the source of truth and stop regenerating — but do not run both, or they will diverge within
a fortnight.
