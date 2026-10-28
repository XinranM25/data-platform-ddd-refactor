# Glossary

Status: decided 2026-09-03.

- **Delivery day**: local day (Europe/Berlin), 96/92/100 quarter-hours (T1).
- **Day-ahead price** `day_ahead_price_eur_per_mwh`; legacy `day_ahead`. Source: market-data API (T2).
- **Imbalance price** `imbalance_price_eur_per_mwh`; legacy `imbalance`. Source: market-data API, published with 1 day delay (T3).
- **Metered energy** `export_energy_mwh`; from SCADA kW 10-min, converted in the adapter (T4).
- **Forecast energy** `forecast_energy_mwh`; legacy `forecast_mw` is MWh per 15 min (T5).
- **Missing input**: derived value is NULL, never 0 (T6) 🔧 step 7.
- **Revenue** `spot_revenue_eur` = export_energy_mwh × day_ahead_price (T7).
- Storage in UTC, outputs in local time (T8).

## Decision log

| Date | ID | Decision |
|---|---|---|
| 2026-09-03 | T1 | Europe/Berlin |
| 2026-09-03 | T2 | market-data API is the only price source for now |
| 2026-09-03 | T3 | keep imbalance even though late |
| 2026-09-03 | T4 | convert in adapter |
| 2026-09-03 | T5 | rename to forecast_energy_mwh |
| 2026-09-03 | T6 | NULL, fix in step 7 |
| 2026-09-03 | T7 | spot revenue only, no imbalance cost yet |
| 2026-09-03 | T8 | UTC in db |
