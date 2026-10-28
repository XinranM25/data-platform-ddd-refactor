# Domain pack: energy and power trading (Europe)

For data platforms around electricity generation and trading: renewable or thermal assets, market prices, metering, production forecasts, trades, imbalance and settlement. Rules differ by country and market; confirm everything against the user's data and documents.

## Core concepts

- **Asset / site / unit.** A wind or solar farm, a battery or a plant, with an operational hierarchy (portfolio → site → turbine or inverter). The SCADA or monitoring portal is usually the system of record for capacity, units and coordinates. Every vendor has its own name or ID for the same site; register aliases in one master-data context.
- **Bidding zone.** Prices are per bidding zone (or market area), not per asset. An asset belongs to one zone. Keying prices by asset is a classic modelling bug.
- **Markets for the same MWh**, in time order: forward and futures; the **day-ahead** auction (one price per zone and period, cleared the day before); **intraday auctions**, which may cover only part of the delivery day; **continuous intraday** trading (many trades per period, summarised as VWAP, high, low, last, volume); **balancing** markets (aFRR, mFRR); **imbalance settlement** after delivery.
- **Volumes.** Forecast production, bid or nominated volume, traded volume, metered (actual) production, curtailed or lost production, available or potential power. In some businesses several of these are the same number; decide in the glossary which are distinct concepts.
- **Money.** Spot revenue, imbalance cost, balancing revenue, fees and tariffs, guarantees of origin, PPA settlement. Define each formula once, and whether totals include the PPA.
- **Forecasts.** Several providers and models; quantiles (P10, P50, P90); many revisions per day. The version used for a day-ahead decision differs from the latest.
- **Curtailment.** Reducing output when prices are negative or on grid instruction. The platform that sends the command is a mechanism, not a strategy; keep the two apart in names.

## Time and units

- **Delivery day** in market local time (CET/CEST in most of continental Europe; check local rules). Store UTC.
- **Market time unit.** European day-ahead and intraday markets moved to 15-minute products in 2025; older data and some sources are hourly. A delivery day has 96 quarter-hours, 92 on the spring DST day and 100 in autumn (hourly: 24, 23, 25).
- **Energy versus power.** Energy per period in MWh, power in MW; energy per 15-minute period = average power / 4. Vendors label these inconsistently; a column named `_mw` often holds MWh per period. Suffix every name with its unit.
- **Prices** in EUR/MWh (or local currency). Negative prices are normal, not errors.
- **SCADA** data often arrives in kW and 10-minute intervals; aggregation rules (sum energy, average power and wind speed) belong in the adapter.

## Traps

- Range helpers that add "one day" in local time lose or gain an hour on DST days; vendor files in local time without an offset fail on the autumn day.
- Mixing hourly and 15-minute data without explicit conversion.
- Intraday auctions covering only part of the day: expected-period counts must follow the auction, not the full day.
- Continuous trading with no trades in a period: store a NULL row ("asked, no trades"), not a missing row and not 0.
- Imbalance prices published late and revised; exchange and market-data APIs often allow only 7 to 30 days of lookback, so gaps must be backfilled before the window closes.
- Trade confirmations arriving as spreadsheets in email; forecast vendors with short-lived tokens or no API; manual backfill files from colleagues. Treat each as an adapter with a source priority.
- Capacity typed as a rounded literal in a spreadsheet, so derived limits (for example a minimum output floor) are slightly wrong.
- Backtests using the latest forecast instead of the day-ahead snapshot look better than reality.

## Typical contexts

| Context | Keyed by | Holds |
|---|---|---|
| Assets (master data) | asset | hierarchy, capacity, units, coordinates, zone, aliases |
| Market prices | bidding zone | day-ahead, intraday, imbalance, balancing prices |
| Metering | asset | actual production, losses, potential power, live readings |
| Forecast | asset | production forecasts by provider, version and quantile |
| Trading | asset or portfolio | day-ahead and intraday volumes, confirmations |
| Weather | asset or zone | wind speed, irradiance, temperature, forecast and observed |
| Data quality | series | completeness, recovery windows, audits, backfills |
| Strategy / backtest | asset | simulated decisions and their P&L |
| Bidding support, dashboards, reports | asset or portfolio | decision inputs and outputs for people |

## Typical sources

Market-data APIs, power exchange APIs, TSO transparency platforms, SCADA or monitoring portals, forecast vendors, counterparty or route-to-market reports by email, weather APIs, internal spreadsheets.

## Glossary questions to ask

1. What is the delivery day, in which zone, and how are periods identified?
2. Is each volume column energy per period or power? Check the values.
3. For each price: which market, which source is authoritative, which is backup?
4. Which forecast version counts for a past day: latest or day-ahead snapshot?
5. Are forecast, bid and traded volume the same concept in this business?
6. What is the source of truth for capacity and units, and does any formula use a typed literal instead?
7. What should a derived value be when an input is missing?
8. What counts as "no data" for continuous trading or partial-day auctions?
9. How far back can each source be fetched again?
10. Which revenue and cost formulas exist, and what does each total include?
