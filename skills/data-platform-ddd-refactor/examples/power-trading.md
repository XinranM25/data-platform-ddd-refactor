# Worked example: a power-trading data platform

A real refactor, sanitised: no company, site, vendor or person names. It shows what each step produced in practice. Use it to show the user a concrete example of a step's output, whatever their domain.

## The system before

One person built it in a few months, script by script, for a wind portfolio in a Nordic bidding zone:

- Sources: a market-data API (day-ahead and imbalance prices), a power exchange API (intraday auctions, continuous trading, balancing), a SCADA portal (metering), a forecast vendor (sometimes only through a hand-pasted token), trade confirmations as spreadsheets in a counterparty's emails, a one-off spreadsheet a colleague filled by hand, and over a year of history in one workbook (1.78 million values).
- Outputs: curtailment-strategy backtests, a bid-availability report, a daily trading dashboard, an export in a simulation workbook's layout, an internal web app.

What the dependency baseline found:

- One 384-line `main()` fetched four sources, merged them, computed strategies, wrote CSVs and wrote the database.
- The storage module imported a data-source module, to know which metrics existed.
- One global metric-to-source map: one concept could have only one source.
- The dashboard project ran the other project's main script and read its table with raw SQL.
- One generic table (asset, source, metric, time, value) that any script wrote.
- A comment said "CSVs are the source of truth"; the database was.
- One derived metric mixed values computed from actuals and from forecasts.
- Forecast metrics with no producing code left.

## Assessment (in hindsight)

Verdict **A, full refactor**: many sources per concept, rules in spreadsheet formulas, outputs used for trading decisions, more sites and users coming, a domain owner available. Risks: one person, production running daily, DST change two weeks after the planned end.

## Glossary (Step 1)

18 decisions on the first day, 43 by the end. Examples:

| ID | Question | Decision |
|---|---|---|
| T1 | Output time zone (legacy used two zones with the same clock time) | One local zone everywhere; storage in UTC |
| T4 | Naming | Four quantity classes (energy, power, price, money), every name ends in its unit |
| T7 | Forecast, bid and trade volume | One concept in this business: the day-ahead trade |
| T10 | Missing input in a derived value | NULL, never 0 |
| T20 | Capacity in the spreadsheet differed from SCADA | SCADA is authoritative; the spreadsheet value was a rounded typo |
| T28 | Which forecast version for a past day | The day-ahead snapshot; backtests are honest only with it |
| T35/T37 | Periods with no trades or no auction result | A NULL row ("asked, no value"), never overwriting a real value |
| T40 | Colleague's manual file | Lowest source priority, last resort only |

Seven of them changed outputs or stored data. They were queued and done later in their own sub-steps.

## Context map (Step 2)

Ten contexts: assets (master data); market prices (keyed by bidding zone), metering, forecast, trading, weather (upstream); data quality (cross-cutting); strategy backtest, bid availability, trading dashboard (downstream). The shared kernel held the delivery day and period (DST-aware), units, asset ID, bidding zone, events and a source-priority function.

## How it ran

| Step | What happened |
|---|---|
| 0 | Production moved to a protected checkout; dev worktree with its own database copy; daily backups; golden master over strategy outputs, the export and the bid report |
| 1–2 | Glossary and context map, no code |
| 3 | Shared kernel; its tests exposed two DST bugs in legacy code, logged and left for the owner to schedule |
| 4 | Market prices as the template; ran on dev beside legacy for three days, first comparison 14,352 rows identical; then production switched |
| 5 | Assets, metering, forecast, trading, one at a time, read side only |
| 6 | An ingestion event; a data-quality context with per-source completeness and recovery windows (exchange 7 days, market data 30 days, inbox); a daily audit that backfills and alerts; a live fallback for the web app, labelled and never written |
| 7 | Strategy, bid report and dashboard moved onto services with identical outputs; then the queued behaviour changes, each with its diff reviewed; then legacy code deleted |
| 8 | One long table per context, numbered migrations; cutover rehearsed on a read-only production copy: 33 seconds, 0 mismatches over the full history |
| 9 | Health page and dashboards on services, built in a parallel session |
| 10 | A weather context added: it touched only master data (coordinates) and wiring |

About two weeks, 117 commits, production running every day. Every merge had a rollback tag.

## What it shows

- The glossary found more real problems than the code moves did.
- Running the new path beside the old for a few days is what made switching production calm.
- The data-quality context turned "did anything break overnight?" from a manual check into one page.
