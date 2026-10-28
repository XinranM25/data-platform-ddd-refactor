# The steps in detail

Read the section for a step before explaining it to the user. Each section has: goal, why it comes here, what you do, decisions for the user, done when, pitfalls.

## Contents

- Step 0: Safety net
- Step 1: Ubiquitous language (glossary)
- Step 2: Bounded contexts and context map
- Step 3: Shared kernel
- Step 4: Template context
- Step 5: Remaining upstream contexts
- Step 6: Cross-cutting concerns (events, data quality, integration)
- Step 7: Downstream contexts and retiring legacy
- Step 8: Storage schema
- Step 9: Consumers and frontend
- Step 10: First new feature
- Merging to production (every step)

---

## Step 0: Safety net

**Goal.** Make it safe to change anything: production is protected, there is a separate place to work, and there is an automatic way to tell whether outputs changed.

**Why first.** Every later step is a change to a running system. Without a net, the user will (rightly) stop trusting the refactor after the first surprise.

**What you do.**

- Check that the dependency baseline from the assessment is still current (see `references/assessment.md`).
- Separate production from development. With git, a common setup is a `prod` branch checked out where production runs, and a `dev` branch in a separate worktree with its own environment and its own copy of the data. Production jobs point only at the production checkout.
- Make sure production data is backed up automatically, and that a backup can be restored. Turn on safe settings the store supports (for SQLite, WAL mode and online backups).
- Build the **golden master**: freeze a read-only snapshot of input data, and record the outputs that matter (reports, derived columns, exports) computed from it. A `check` command recomputes them through the current code path and compares. See `references/safety-net.md`.
- Get the existing tests running, however few. Add a test runner if there is none.

**Decisions for the user.** Which outputs are business-critical (these go in the golden master); where production runs and when it is quiet enough to merge; how long backups are kept.

**Done when.** Production runs from the protected checkout; backups run; `golden check` passes on dev and on production.

**Pitfalls.** A golden master that compares against live data drifts every day; freeze the snapshot. Do not fix bugs in Step 0, even obvious ones; list them for later, or the baseline is not a baseline.

---

## Step 1: Ubiquitous language (glossary)

**Goal.** One agreed name, definition, unit and source of truth for every business concept. No code changes.

**Why here.** Every later step names things: contexts, services, columns. Names chosen without this step get renamed later at much higher cost. And this is where real bugs hide: two files meaning different things by one word.

**What you do.**

- Read `references/lessons.md` first, and the domain pack in `domains/` if one matches.
- Extract every concept from code, column names, spreadsheet headers, config, reports and the user's vocabulary. Check real data for each: units, ranges, time zones, which sources overlap and whether they agree.
- Draft `docs/glossary.md` from `templates/glossary.md`: naming rules first (for example "every quantity name ends in its unit"), then terms grouped by topic. Each term gets: domain name; current name(s) in code; definition; unit; source(s) and priority; notes.
- Turn every contradiction or ambiguity into a numbered question (T1, T2, …) with your recommendation and the evidence.
- Mark terms whose agreed meaning differs from what the code does today: **behaviour change** (outputs will change) or **data change** (stored data must be fixed). List them in "deferred changes" with the step that will do them. Do not fix them now.

**Decisions for the user.** All of the T questions. Typical ones: the canonical name and ID of each core entity; time zone for storage and for output; which source is authoritative and which are fallback; what "missing" means for derived values; which version of a revisable value counts (latest or as-known-at-decision-time); what to do with orphaned data.

**Done when.** Every T question has an answer recorded in the decision log, and deferred changes each have a target step.

**Pitfalls.** Do not let the existing column names define the domain names; the glossary leads and code follows. Do not ask questions the data can answer: check first, then ask with the evidence. Keep external names (vendor fields, spreadsheet headers) as aliases that appear only in adapters.

---

## Step 2: Bounded contexts and context map

**Goal.** Decide which contexts exist, what each owns (data, rules, tables), and who may call whom.

**Why here.** With the language fixed, boundaries become visible: a context is where a set of terms has one consistent meaning and one owner.

**What you do.**

- Group the glossary into candidate contexts. Typical layering for a data platform: **master data** at the top (assets, customers, instruments), **upstream contexts** that hold facts from the outside world (prices, measurements, forecasts, trades), **supporting or cross-cutting** contexts (data quality), and **downstream contexts** that turn facts into decisions (strategies, reports, dashboards).
- For each context: what it owns, what it provides (services), what it needs from others, external systems it talks to.
- Draw the relations. Dependencies point one way; where the lower layer must notify the upper, plan an event.
- Decide what goes in the shared kernel: only small value types that every context needs and that rarely change.
- Write `docs/context-map.md` from `templates/context-map.md`. The decisions come first; the picture comes after them.
- If the user wants a diagram, draw it from the agreed `context-map.md`, not before. Hand it to a diagram skill if one is installed (for example archify), passing the contexts, what each owns and the relations; otherwise draw a simple one yourself. Keep the diagram's source next to the docs so it can be redrawn when a C decision changes.

**Decisions for the user (C1, C2, …).** Borderline ownership (which context owns a derived value; whether an export is its own context or a service of another); what each context is keyed by (for example prices keyed by market rather than by asset, weather keyed by location rather than by device); whether master data is a context or just config; what stays out of the shared kernel.

**Done when.** Every table, metric and job has exactly one owning context, and the C decisions are logged.

**Pitfalls.** A context per database table is too fine; one context for "data" is too coarse. A big shared kernel is a monolith in disguise. Splitting by team or by vendor rather than by meaning gives the wrong boundaries.

---

## Step 3: Shared kernel

**Goal.** Implement the few shared value types as pure, well-tested code.

**Why here.** Every context will use them, and they are where the nastiest bugs live (time, units). Getting them right once removes a class of bugs everywhere.

**What you do.** Typical contents: the time grid (period, delivery or business day with DST handling), unit types or naming conventions with conversion helpers, entity IDs, market or zone identifiers, event base types, and small generic algorithms the user approves (for example "pick a value by source priority"). No I/O. Exhaustive tests, including DST days, leap years and boundaries.

This is also where **primitive obsession** ends for the shared concepts: a temperature, an amount of energy or a business day passed around as a bare `float` or `str` is how units and zones get mixed. Turn the ones the glossary flagged into small value types that validate on creation and carry their unit (`Celsius`, `EnergyMwh`, `DeliveryDay`), converting at the input boundary. Keep it to the concepts that caused real bugs; not every number needs a class.

**Decisions for the user.** How strict the kernel is; which granularities and currencies to support now (support only what is used; YAGNI).

**Done when.** The kernel and its tests pass, and nothing else changed yet.

**Pitfalls.** Tests here often expose bugs in legacy code (for example a date-range helper that loses an hour on DST days). Record them; fixing legacy behaviour is a separate, user-approved change, or it waits until the legacy code is replaced.

---

## Step 4: Template context

**Goal.** Build one context end to end, run it in parallel with the legacy code, and switch production to it. It becomes the pattern every other context copies.

**Why here.** One complete example teaches more than any rule, and it surfaces the hard wiring questions (composition root, configuration, job entry points, DTO shape) while the stakes are small.

**What you do.** Pick an upstream context that is important but self-contained (often the primary data feed: market prices, sensor readings, shipment events, transactions). Sub-steps:

- 4a domain: value objects, entities, rules, using glossary names. Put behaviour on the domain objects rather than in procedural helper functions (no anaemic model): for example a `PricePoint` that refuses a timestamp off the period grid, or a series that knows its expected period count. Legacy code is usually procedural; move one operation at a time, with the old function delegating until it can be removed.
- 4b southbound: ports, plus adapters for the existing storage (keep the current schema for now; Step 8 changes it) and for the external source.
- 4c northbound local: application services and DTOs; a composition root that wires adapters to services.
- 4d parallel run: schedule the new path on dev beside the legacy one for a few days and compare every row. Then merge, and switch production jobs to the new path. Keep the legacy path only where something else still depends on it, and note that in the plan.
- 4e northbound remote: an API endpoint or job entry, if useful.

Record HTTP responses as test fixtures so adapter tests do not call vendors.

**Decisions for the user.** Which context is the template; the DTO shape; when to switch production; whether legacy code can be deleted now or must wait for a later step.

**Done when.** Production runs the new path, the comparison was clean for the agreed number of days, and the plan describes the layout as the template.

**Pitfalls.** Over-engineering the template: it will be copied, so complexity multiplies. Forgetting that another legacy process may still write the same data.

---

## Step 5: Remaining upstream contexts

**Goal.** Move every other source-of-facts context into the new structure, one at a time.

**What you do.** Order by dependency: master data first (other contexts look up IDs, aliases and capacities there), then each upstream context. For each one: domain, ports and adapters, local services, parity check against legacy outputs, then merge. Walk the user through the files of the first one or two in detail if they want to learn the code. Apply the same tactical moves as in the template context: bare values that carry a unit or an ID become value types, rules move onto domain objects, and storage access goes behind a repository interface defined in the domain's language. For a catalogue of these code-level refactorings (anaemic model to behavioural entity, primitive obsession to value object, leaky repository to domain repository), the `ddd-refactor` skill in [software-design-skills](https://github.com/yonatankarp/software-design-skills) is a good companion if installed. Usually this step does only the read side and adapter moves, without new production jobs, so production behaviour stays the same.

**Decisions for the user.** Order; per-context naming questions that the glossary did not settle (add them to the glossary as new T items); master-data format (often a config file read by a read-only adapter).

**Done when.** All upstream contexts serve their data through local services, verified identical to legacy.

**Pitfalls.** Downstream code should get upstream data through its own port (a downstream ACL), not by importing upstream DTOs everywhere. Vendor exports often carry extra columns; do not ingest what the glossary did not define.

---

## Step 6: Cross-cutting concerns (events, data quality, integration)

**Goal.** Let contexts cooperate without tangling: events for "something new arrived", a data-quality context that knows what is missing and how to recover it, and any read-through or fallback behaviour.

**What you do (adapt to the system).**

- An event such as `ObservationsIngested`, published by upstream ingestion after a write; a simple in-process bus in the composition root; subscribers (for example "recompute derived values for affected days"). A failing subscriber must not undo data already written.
- A data-quality context: for each tracked series, the expected count per day, the actual count, the gaps, and how a gap can be recovered (API backfill, only within a vendor's window, only from an inbox or a person). An audit job that backfills what it can through upstream ingestion and alerts on what it cannot, before the recovery window expires.
- If consumers need fresh data not yet stored: a composite adapter that reads storage first and fetches live only for the gap, labelled as live, cached briefly and never written on the read path.

**Decisions for the user.** Which series are tracked and their expected counts; whether completeness is computed on the fly or stored; per-source or merged completeness (per-source shows a failing primary even when a backup covers it); alert channel and timing; which data may be read live.

**Done when.** The audit replaces any legacy gap-check scripts in production after a trial run, and recomputation is triggered by events, not by legacy glue.

**Pitfalls.** Persistent queues and stored ledgers are often unnecessary: recomputed gaps can be the queue. Live fallbacks hide data problems unless they are labelled.

---

## Step 7: Downstream contexts and retiring legacy

**Goal.** Move the decision-making parts (strategies, reports, dashboards, exports) onto upstream services, then delete the legacy code.

**What you do.** One downstream context per sub-step. The first sub-step for each is a move with identical outputs (golden check). Then, as separate sub-steps, do the behaviour changes queued in the glossary, each with its own diff review and, if intended, a regenerated golden master. Finally, a sub-step that deletes the legacy entry points, scripts, glue and tests that only compared against legacy code (keep tests that check real data).

**Decisions for the user.** Order; each behaviour change's acceptance; what to archive rather than delete; when legacy is retired in production (often a few clean days after the move).

**Done when.** No production job calls legacy code, the legacy directories are deleted on dev, and the deferred behaviour changes for this step are done.

**Pitfalls.** Regenerating the golden master to make a failing check pass, without understanding the diff. Slipping a "small fix" into a move.

---

## Step 8: Storage schema

**Goal.** Replace the legacy storage layout with one owned by the contexts, behind the repository ports, so no business code changes.

**What you do.**

- Design one table (or a few) per context, using glossary names. For time series, a long table keyed by (subject, kind, period, source) is simple and handles many sources and priorities.
- Versioned, append-only migrations (numbered SQL files plus a version table), never editing a migration that has run.
- A migration script from old to new storage that refuses to continue on anything unexpected, writes to a temporary file and renames on success, and produces a reconciliation report (row counts and sums per series must match).
- The queued data changes from the glossary (renames, merges, removing bad rows), done inside the migration and visible in the report.
- New repository implementations with the same interface; compare old and new repositories over the full history.
- A rehearsal on a read-only copy of production, then a cutover checklist with timings and rollback (see `references/safety-net.md`).

**Decisions for the user.** Table layout; what to clean during migration; whether the old store is kept as a fallback and for how long; cutover date.

**Done when.** Production runs on the new store, the old one is untouched and kept as a fallback, and the reconciliation report showed zero mismatches.

**Pitfalls.** Cutting over just before a known risky date (DST change, month end) without a rehearsal. Leaving old repositories in place after the cutover; delete them in a follow-up.

---

## Step 9: Consumers and frontend

**Goal.** Every reader (web app, notebooks, exports) uses local services, never tables or vendor APIs directly.

**What you do.** Inventory every place that reads storage or calls a vendor outside an adapter, and move each onto services. If a UI is being built or redesigned, this can run in parallel from Step 7 on, possibly in a separate session with its own handover file; agree on who edits which folders.

**Decisions for the user.** UI stack and design; which pages first; who owns the frontend folder.

**Done when.** Searching the consumer code for SQL, table names or vendor URLs finds nothing.

---

## Step 10: First new feature

**Goal.** Add something new the business asked for, to prove the structure. Ideally a new context (a new data source or a new decision tool).

**Done when.** The feature touched only its own context, master data if needed, and the composition root. If it needed edits all over the code, revisit the boundaries with the user.

After this, suggest closing the refactor: move the plan to `docs/history/`, write a current-state architecture document, a backlog, a changelog and a maintenance handover.

---

## Merging to production (every step)

Explain this checklist to the user before the first merge and follow it every time:

1. Before: today's production jobs succeeded; on dev, all tests and the golden check pass; nothing half-done is in the commits to merge. Tag the commit to merge (`merge-N`).
2. Timing: choose a window with no production jobs running.
3. Production: tag the current state for rollback (`prod-pre-N`). If there is a migration, take a backup first.
4. Stop running services, fast-forward production to `merge-N`, run migrations, update scheduled jobs.
5. Start services, run tests and the golden check on production, look at the outputs, run the affected jobs once by hand if needed.
6. Update the plan's handover and step table.

Rollback: stop services, reset production to `prod-pre-N`, restore the backup if a migration ran, re-register the old jobs, start services.
