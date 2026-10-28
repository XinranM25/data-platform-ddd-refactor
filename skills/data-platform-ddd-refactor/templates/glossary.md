# Ubiquitous language (glossary)

<!-- Output of Step 1. Code, tables and UI follow these names, not the other way round. Status line: draft / decided (date). -->

Status: **draft**. Claude drafts from code and data; `<owner>` decides each item (see "Decision log").

Entry format: **Term** (domain name; current name in code) — definition. Unit / source / notes.

Markers:

- 🔧 **Behaviour change**: the agreed meaning differs from what the code outputs today. Done in its own later step, verified separately.
- 🗄 **Data change**: stored data must be fixed. Usually done during the storage migration.

## 0. Naming rules

<!-- Rules that apply to every name. Examples:
- Quantities end in their unit: `_kwh`, `_kg`, `_celsius`, `_usd`, `_per_hour`, `_seconds`.
- Conversions happen only in adapters or the shared kernel.
- External names (vendor fields, spreadsheet headers, column letters) appear only in adapters.
- Legacy names stay in storage until the schema step; adapters map them.
-->

## 1. Time

<!-- Storage zone; business-day definition and zone; period length and how a period is identified; DST day lengths. -->

## 2. Entities and master data

<!-- The core entities (asset, site, customer, instrument…), canonical IDs, aliases and where they are registered, the system of record for their attributes. -->

## 3. <Topic>

<!-- One section per group of concepts (measurements, prices, forecasts, transactions, derived values…). For each term: domain name, current name, definition, unit, sources with priority, notes, markers. -->

## Sources

| Source label | What it is | Coverage / recovery window | Notes |
|---|---|---|---|
| | | | |

Source priority per concept: <!-- for example "sensor temperature: telemetry_api > nightly_export > manual_backfill" -->

## Rules for missing data

<!-- Missing input → derived value is missing (NULL), never 0. "No row" versus "NULL row". Expected periods per series. -->

## Deferred changes

| Type | Change | Decision | Planned in |
|---|---|---|---|
| 🔧 | | T? | Step 7 |
| 🗄 | | T? | Step 8 |

## Decision log

| Date | ID | Decision (owner's words) |
|---|---|---|
| | T1 | |
