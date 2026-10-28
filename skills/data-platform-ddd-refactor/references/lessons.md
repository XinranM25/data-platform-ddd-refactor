# Lessons for data platform refactors

Mistakes that come up again and again when a data platform or pipeline is refactored, in any domain. Use them to draft glossary questions in Step 1 and to review adapters in Steps 4 to 8. Before claiming one of these applies, check it against the user's real data. For industry-specific traps, see the matching pack in `domains/`.

## Names

- **Names lie.** A column called `duration_min` that holds seconds, `revenue` that excludes refunds in one report and includes them in another, `actual` that is really a forecast. The glossary step exists to find these; check values, not just names.
- **One concept, one name; one name, one concept.** If the same quantity is called `qty`, `volume` and `units` in different files, decide whether it is one concept (one name) or several (several names, each defined).
- **Put the unit in the name** (`_kwh`, `_kg`, `_celsius`, `_usd`, `_seconds`, `_per_hour`). Most unit bugs disappear when the unit is visible at every use.
- **Amount versus rate.** Energy versus power, distance versus speed, total versus per-period: define the conversion once and do it only in adapters or the shared kernel.
- **Spreadsheet headers and column letters are not names.** Replace `D`, `aq` or "Col 7" with business names; keep the spreadsheet's names only in the adapter that reads or writes it.
- **External names stay at the edge.** Vendor field names, legacy IDs and aliases live in adapters or in a master-data registry, never in the domain.

## Time

- **Store one zone, show another.** Store UTC; define the business day (trading day, shift, reporting day) in the zone the business uses, and output in that zone. Write both in the glossary.
- **A day is not always 24 hours.** Around DST changes a local day has 23 or 25 hours, so a day of 15-minute periods has 92 or 100 instead of 96. Any helper that adds "one day" to a local timestamp, or assumes a fixed count, is a bug. Put the day-to-UTC-range function in the shared kernel and forbid computing it by hand.
- **Ambiguous local times.** Parsing local timestamps on the fall-back day needs an explicit rule; many libraries raise an error or guess. Vendor files in local time without an offset are the usual source.
- **Identify a period by its start** (or end, but decide), and say so in the glossary.
- **Mixed granularities.** Hourly, 15-minute, 10-minute and daily data in one system need explicit aggregation rules (sum for amounts, mean for rates, last for states).

## Missing data

- **Missing is not zero.** A derived value with a missing input is missing (NULL), never 0. A silent 0 becomes a wrong total, a wrong invoice line or a wrong model feature.
- **"Never fetched" versus "fetched, no value".** No row means "not fetched yet". A row with NULL means "asked, and the source had no value" (no transactions, sensor offline, event not held). Without this distinction completeness checks retry forever. Make sure a NULL never overwrites a real value.
- **Text placeholders** ("-", "n/a", "#N/A") in migrated spreadsheets must become missing values, not strings in a numeric column.
- **Expected counts differ per series.** Some series cover only part of a day or only working days. Define the expected count per series instead of assuming a full grid.

## Sources

- **Several sources for one concept is normal.** Give each concept an ordered source priority (authoritative first, manual files last), keep every source's rows, and choose at read time. Make the priority easy to change.
- **Check overlaps.** Where two sources cover the same periods, compare them on real data before declaring one authoritative, and record how you compared.
- **Master data from the system of record.** Capacities, IDs, locations and hierarchies come from the operational system, not from a spreadsheet where someone typed a rounded number. Derived constants follow master data instead of being literals.
- **Orphaned data** (values no code produces any more): keep it out of normal reads, for example in a backup table, but let the user decide before deleting it.

## Revisions

- **Latest versus as-known.** Forecasts, prices, inventories and settlements get revised. A backtest or audit of a decision must use the version available at decision time (a snapshot), not the latest. Decide per concept which version is stored; store both if both are needed.
- **Derived values must be recomputed** when an input is backfilled or corrected. Drive this with an event from ingestion, limited to the affected periods.

## Sources over time

- **Every source has a recovery window.** Some APIs return only the last 7 or 30 days; an inbox keeps mail until someone deletes it; a person's file arrives once. Data quality must know each window and alert before data becomes unrecoverable, which is why an audit has to run daily.
- **Short-lived credentials** (tokens pasted by hand) belong in the current process only. Design such jobs to run on demand when a token is available, and let the audit flag what is still missing.
- **No API yet?** Spreadsheets and email attachments are adapters like any other: they translate into domain names, units and time zone at the edge, and the core never sees their format.
- **Measure vendor behaviour.** Publishing delays, revision patterns and limits: measure them on real responses, then write them in the glossary with how they were measured.

## Storage

- **One table per context, owned by it.** For time series, a long table keyed by (subject, kind, period, source) handles new quantities without schema changes. For entity data, normal tables owned by one context.
- **Readers never touch tables.** Dashboards, notebooks and other projects that run raw SQL on another context's tables are what made the old system tangled.
- **Migrations are append-only and numbered.** A migration that already ran is never edited.

## Process

- **Behaviour changes found in the glossary wait** for their own step. Mixing them into code moves is how a refactor loses trust.
- **The handover is part of the work.** Update the plan's current status at the end of every session.
