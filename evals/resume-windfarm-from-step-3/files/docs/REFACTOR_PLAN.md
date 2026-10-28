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
| 4 | Template context: market_prices | |
| 5 | assets → metering → forecast | |
| 6 | Events, data quality | |
| 7 | Downstream: revenue report | |
| 8 | New schema | |
| 9 | Consumers | |
| 10 | First new feature | |

## Current status (2026-09-05)

- Production still runs legacy `main.py` daily at 06:00 from the prod checkout.
- Steps 0–3 done on dev and merged to prod (tag `merge-3`). Shared kernel has
  `DeliveryDay` and `mw_to_mwh_per_period`.
- Known legacy bug, owner decided NOT to fix now (2026-09-05): `main.py` fills missing
  inputs with 0 (T6 says NULL); fix belongs to step 7.
- Next: step 4, template context `market_prices` (C2: keyed by bidding zone).
