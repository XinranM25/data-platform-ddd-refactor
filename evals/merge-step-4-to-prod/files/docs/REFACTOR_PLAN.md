# DDD refactor plan

Assessment: verdict A full (A1, 2026-09-01), see `docs/DDD_ASSESSMENT.md`.

## Goal

- Storage is the single entry point, backed up and versioned.
- Every vendor behind an adapter; names and units from the glossary.
- Derived values recomputed when inputs change.

## Architecture

Diamond: `contexts/<context>/{domain, acl/ports.py, acl/adapters, ohs/local, ohs/remote}`,
`shared_kernel/`, composition root in `ops/composition.py`.

## Working agreement

- Production runs from `~/windfarm-prod` (branch `prod`); development in `~/windfarm-dev`
  (branch `dev`) with its own database copy.
- One kind of change per step. Tests and golden check pass at the end of every step.
- Explain each step and its decisions first; wait for the go-ahead.

## Steps and status

| Step | Content | Status |
|---|---|---|
| 0 | Safety net | ✅ 2026-09-02 |
| 1 | Glossary | ✅ 2026-09-03 (T1–T8) |
| 2 | Context map | ✅ 2026-09-04 (C1–C4) |
| 3 | Shared kernel | ✅ 2026-09-05 (DeliveryDay, units; 3 tests) |
| 4 | Template context: market_prices | 4a–4c ✅ dev; 4d trial running since 2026-09-08 |
| 5 | assets → metering → forecast | |
| 6 | Events, data quality | |
| 7 | Downstream: revenue report | |
| 8 | New schema | |
| 9 | Consumers | |
| 10 | First new feature | |


## Current status (2026-09-11)

- Production: legacy `main.py`, cron 06:00 in `~/windfarm-prod`, tag `merge-3`.
- Dev: step 4a–4c done (D1–D6 approved 2026-09-06, zone DE-LU). `main.py` on dev gets prices
  through `PriceService.ingest(day)`.
- 4d trial: dev cron 06:30 runs the new path, 07:10 `scripts/compare_prices_with_prod.py`
  compares with prod's 06:45 backup. Log: `logs/compare_prices.log`.
- To merge: the new code needs `MARKETDATA_API_KEY` in prod's environment (dev has it).
- Rollback idea not written yet.
