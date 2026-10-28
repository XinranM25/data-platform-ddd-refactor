# Assessment: is a DDD refactor worth it here?

Do this before Step 0 of a new refactor, or on its own when the user only wants to know. The result is a short report with evidence from their code and data, a verdict, and a decision the user makes. A refactor that should not happen is the most expensive one, so be willing to say no.

## How to assess

1. **Read the system first**, the same way as the dependency baseline: entry points and jobs, module dependencies, storage and who reads it, external sources, outputs and who uses them. Note real examples as you go (file and line, a column, a query); the report cites them.
2. **Classify the system**: a data platform (data comes in from sources, is stored, derived and served), a transactional system (users change state through commands: orders, bookings, claims), or mixed. This skill covers the data platform part; for a transactional system, say so in the report (see "Scope" in SKILL.md). Note the business domain and whether `domains/` has a pack for it.
3. **Score each criterion below** as for, against or unclear, with one line of evidence. Do not score from what the user says alone when the code can show it.
4. **Ask only what the code cannot tell you**: who uses the outputs and for what decisions, how long the system will live, plans for growth, who can make domain decisions, how much time is available, what downtime is acceptable.
5. **Give a verdict** (below), with the scope it implies and the main risks.
6. **Let the user decide.** Record the decision as `A1` in the plan (or in the assessment file if they decide not to proceed). On A or B, offer the three working modes (step-by-step, standard, fast; see SKILL.md) in the same message and record the choice as `A2`.

## Criteria

| # | Criterion | Points toward DDD when… | Points against when… |
|---|---|---|---|
| 1 | Language | One concept has several names, units or sources; names lie about units; spreadsheets, code and reports disagree | Few concepts, each with one obvious meaning |
| 2 | Business rules | Rules live in spreadsheet formulas, scripts and people's heads; outputs drive money or compliance decisions | Mostly moving and storing data, with little interpretation |
| 3 | Coupling pain | God functions; storage importing vendors; projects running each other's scripts; raw SQL on shared tables; small changes break distant things | Changes are local and predictable already |
| 4 | Sources and consumers | Several external sources and several consumers (reports, UI, models) | One source, one consumer |
| 5 | Growth | More assets, markets, sources, users or teams are expected | Scope is fixed |
| 6 | Lifetime | Years of maintenance ahead | A one-off or a system due for replacement |
| 7 | Domain owner | Someone can make and own decisions about names, definitions and sources of truth | Nobody can; a hard blocker, because DDD without decisions is only new folders |
| 8 | Capacity | Time for weeks of small steps, alongside normal work | No time beyond urgent fixes |
| 9 | Safety | Production can be protected and backed up, outputs can be compared | No way to test or roll back; fix that first whatever the verdict |
| 10 | Organisation | One person or one team owns the platform | Many teams produce and consume data and wait on each other |

Size alone is not a criterion. A small codebase with dense rules and many sources can benefit more than a large one that just moves bytes.

## Verdicts

- **A. Full guided refactor (Steps 0 to 10).** Most of 1 to 6 point toward DDD, and 7 and 8 are satisfied. Say how many contexts you expect and which one could be the template.
- **B. Lightweight DDD.** The language and coupling problems are real but the system is small or the time is short. Do Steps 0 to 2 fully (safety net, glossary, context map), then restructure only the two or three contexts that hurt most, with lighter layering. Skip or postpone events, data quality and the schema step unless a problem demands them.
- **C. Not now; cheaper fixes first.** Few criteria point toward DDD, or 7 or 8 fail. Recommend concrete smaller moves: a safety net and tests, renaming the worst names with units, extracting the god function, a short glossary without code changes. Say what would change the verdict.
- **D. Organisational problem.** Criterion 10 dominates: many teams, a central data team as the bottleneck. Recommend looking at data mesh or team boundaries, and note that bounded contexts are still the right first step, because contexts can later become independently owned data products.

When 9 fails, every verdict starts with building the safety net.

## Report format

Write `docs/DDD_ASSESSMENT.md` (or show it in chat if the user prefers):

```markdown
# DDD assessment: <system> (<date>)

**Verdict: <A/B/C/D> — <one sentence why>.**

## What the system is
<three to five lines: sources, storage, outputs, who uses them; type (data platform / transactional / mixed); domain and matching pack, if any>

## Evidence
| # | Criterion | Finding | Points |
|---|---|---|---|
| 1 | Language | `duration_min` holds seconds (src/x.py:12); the same quantity is called `qty`, `volume` and `units` in three files | for |
| … | | | |

## What the refactor would involve
<expected contexts (draft), the likely template context, which steps apply, rough duration in sessions or weeks>

## Risks and preconditions
<what could go wrong; what must be true before starting (backups, a domain owner, time)>

## Alternatives considered
<the cheaper options and why they are or are not enough>

## Questions for you
<only what the code could not answer>

## Decision
<filled in when the user decides: A1 — go with verdict X / not now / other; A2 — working mode step-by-step / standard / fast; date>
```

Keep it short enough to read in five minutes. The evidence column is what makes it convincing; one specific example beats three adjectives.
