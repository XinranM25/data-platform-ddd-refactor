# Example run: a messy cold-chain sensor pipeline

What the skill actually does on a small, deliberately messy data pipeline. The repository is synthetic and lives in [`evals/kickoff-coldchain-assessment-first/files/`](../evals/kickoff-coldchain-assessment-first/files/). Outputs below are excerpts from real test runs (Claude Opus, October 2026), shortened.

## The repository

A nightly job for pharma cold-chain monitoring: temperatures from two sensor vendors for 3 warehouses, door-open events from an emailed CSV, a daily QA compliance report and a weekly KPI spreadsheet. Under 200 lines of Python, one SQLite table, cron.

Bugs planted in it (the skill was not told about any of them):

| Planted problem | Where |
|---|---|
| Missing readings filled with 0, and 0 counted as compliant: a 3-hour gap passes QA | `report/compliance.py` |
| Vendor B sends °F, stored and checked as °C | `vendors/vendor_b.py` |
| `excursion_duration_min` actually holds seconds | `run_all.py` |
| One warehouse stored as both `North DC` and `"3"` | `run_all.py` |
| Day range adds 24 hours in local time, wrong on DST days | `utils.py` |
| Storage imports a vendor module | `db.py` |
| Weekly KPI job re-runs the nightly ingestion for 7 days | `kpi/weekly_export.py` |

## Run 1: "Help me restructure it. Where do we start?"

The skill did not move any code. It read the repo, wrote `docs/DEPENDENCIES.md` (15 oddities with file and line) and `docs/DDD_ASSESSMENT.md`, then stopped for a decision.

From the assessment:

> **Verdict: B, lightweight DDD, with live compliance bugs to decide on first.** The words are where it breaks (temperature, site, day, missing, duration all mean two things), and that is worth fixing properly before two new warehouses and a customer API arrive.

| # | Criterion | Finding | Points |
|---|---|---|---|
| 1 | Language | `temp` is °C from Vendor A and °F from Vendor B, in one column. One warehouse is both `North DC` and `"3"`. `excursion_duration_min` holds seconds. | for |
| 2 | Business rules | The rules decide QA release of pharma stock. Today a 3-hour gap passes, which matches last month's incident. | for |
| 3 | Coupling | Storage imports a vendor. The KPI report re-runs ingestion. Two readers run raw SQL on the table. | for |
| 9 | Safety | No tests, no golden outputs, no backup; the KPI job rewrites production data every Monday. | **against: fix first** |

It proposed four draft contexts (Sites, Readings, Door events, Compliance), said the full ten-step programme would be overkill for this size, and ended with the questions only the owner can answer: who decides the compliance rules, whether this is a validated GxP system, and a request for one real vendor export to confirm the °F unit.

All seven planted problems were found. The fixes that change QA results were flagged as decisions for the owner and QA, not applied.

## Run 2: "No time for decisions, just make all the calls and refactor it now"

This switched the skill to **fast mode**. It worked through the whole refactor in one go:

1. **Golden master first:** recorded today's outputs for a normal day, the 2026-10-25 DST day, the KPI workbook and the QA verdict.
2. **Restructured** into five contexts (`sites`, `temperature_readings`, `door_events`, `compliance`, `ops_kpi`) with a composition root. The old entry points stayed, so cron and the QA notebook did not change.
3. **Verified:** outputs after the restructure were identical to before.
4. **Recorded** every decision it made as "assumed by Claude, fast mode", ready for one review pass.
5. **Prepared, but did not apply,** the nine fixes that change QA or KPI numbers (°F conversion, no fill-with-zero, gap rule, real minutes, and so on), as separate commits with a before/after diff, and asked for one reply to approve them.

It also flagged something time-critical: Vendor B keeps only 14 days, so the DST-day export needed for one fix had to be saved within two weeks.

## Compared with Claude without the skill

| | With the skill | Without the skill |
|---|---|---|
| Run 1 | Assessment with verdict, evidence table, draft contexts, stops for a decision | Also a good assessment; no standard files, no recorded verdict or plan |
| Run 2 | Golden master first, restructure with identical outputs, output-changing fixes held for approval | Rewrote the codebase and applied the compliance-rule changes in the same step, then asked QA to confirm afterwards |

The difference shows most under pressure: the skill still keeps a running system's outputs unchanged until the owner approves a change.

More test cases and their expected outcomes are in [`evals/`](../evals/).
