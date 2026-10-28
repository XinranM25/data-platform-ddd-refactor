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
| 4 | Template context: market_prices | proposed 2026-10-26, waiting for D1–D6 |
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
- 2026-10-26: step 4 explained to the owner; draft plan below. Nothing implemented yet.
  Waiting for answers to D1–D6 before starting 4a. Shared-kernel tests still pass
  (3/3, run by hand; pytest is not installed in this environment).

## Step 4 plan (draft 2026-10-26, waiting for decisions)

Template context `market_prices`, built beside legacy `sources/prices.py`. Code move only:
the price rows written to `market_data` must stay identical (golden baseline unchanged).

Sub-steps:

- 4a domain: `PricePoint` (zone, period start UTC, kind, value EUR/MWh, may be NULL),
  kinds `day_ahead_price_eur_per_mwh` and `imbalance_price_eur_per_mwh` (T2, T3).
  Unit tests incl. DST days via `DeliveryDay`. Verify: unit tests.
- 4b southbound: `acl/ports.py` (`PriceFeed`, `PriceRepository`); adapters
  `market_data_api.py` (translates vendor names/units/time, recorded fixtures, no keys in files)
  and `sqlite_market_data.py` (current `market_data` table, `src='prices'`, legacy metric
  names and ts string format kept until step 8). Verify: adapter tests on fixtures and an
  empty store built from the real schema.
- 4c northbound local: `PriceService.ingest(day, zone)` / `prices_for(day, zone)` returning
  DTOs; `ops/composition.py` wires it. Verify: tests + golden check.
- 4d parallel run on dev for the agreed number of days, compare with production backup,
  then merge (`merge-4`, rollback `prod-pre-4`) and switch production per D4.
- 4e remote: per D6.

Decisions (owner's answers go here):

- D1 bidding zone value and where it comes from until `assets` exists (step 5). — open
- D2 DTO shape (long rows vs wide frame). — open
- D3 fetch window: reproduce legacy exactly in step 4? — open
- D4 who writes `src='prices'` rows after the switch, and how `main.py` gets prices. — open
- D5 parity: number of clean days and comparison rule. — open
- D6 delete `sources/prices.py` now or later; 4e API now or skip. — open

Things to verify on the dev copy before 4b (not yet checked, no DB in this checkout):

- V1 exact `ts` string format of existing `src='prices'` rows (tz-aware or naive?).
- V2 whether `market_data` holds `day_ahead`/`imbalance` = 0 at 10-minute SCADA
  timestamps (expected from the outer join + `fillna(0)` in `main.py`).
- V3 price granularity in a real API response (15-min or hourly) and how far back
  `prices.fetch` actually fetches ("30 days lookback").
- V4 how often yesterday's imbalance is missing at 06:00 (T3: published 1 day late).

## Open questions

1. D1–D6 above (step 4).
2. Context map C4 lists `AssetId` and `BiddingZone` in the shared kernel, but step 3
   delivered only `DeliveryDay` and units. Add `BiddingZone` in step 4 (see D1)?
