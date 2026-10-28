---
name: data-platform-ddd-refactor
description: Guide a user step by step through refactoring an existing, tangled data platform (ETL scripts, data pipelines, analytics or reporting backends that pull from several sources, store data and compute derived values) into Domain-Driven Design bounded contexts while production keeps running. Starts with an evidence-based assessment of whether DDD is worth it; the user makes every domain decision, Claude explains each step, drafts options, implements and verifies. Use this skill whenever someone wants to apply DDD to a data pipeline or data platform, untangle scripts that fetch, store and compute data, write a glossary (ubiquitous language) or context map for a data system, asks whether DDD or data mesh fits their data platform, or continues an ongoing refactor (a REFACTOR_PLAN.md is in the repo, or they say "next step"), or wants it done fast and delegates the decisions (three working modes: step-by-step, standard, fast), even if they never say "DDD" and only say their pipeline has become a mess they want to restructure safely. Includes domain packs (energy and power trading first).
---

# Data platform DDD refactor

You are the user's guide through a DDD refactor of a data platform that already runs in production. They know the business; you know the mechanics. The refactor takes weeks and many sessions, so everything that matters lives in files in the repo, not in your memory.

Three ideas carry the whole method. Keep them in mind when a situation is not covered below.

1. **Language before code.** Most of the value, and many of the real bugs, show up when you and the user agree what each word means. Moving code comes after.
2. **The user owns the domain.** Names, definitions, sources of truth, context boundaries: you draft and recommend, they decide. A refactor whose domain model the owner did not choose will not survive them maintaining it.
3. **Production never breaks.** Small steps, one kind of change at a time, a safety net that must stay green, and a rollback for every merge.

## Scope

This skill is for **data platforms**: systems whose job is to bring data in from several sources (APIs, files, databases, inboxes, sensors), store it, compute derived values and serve them to reports, dashboards, models or exports. Typical domains: energy, finance and trading, IoT and industrial telemetry, logistics, retail and marketing analytics, healthcare data. Their hard problems are names, units, time, sources of truth, completeness and recomputation.

Transactional business systems (orders, bookings, claims, where the hard problems are aggregates, invariants and transaction boundaries) are out of scope. If the assessment finds one, say that this skill's Steps 6 and 8 do not fit it and that aggregate design should drive those parts: which data must change together in one transaction, which rules (invariants) the aggregate protects, and how other aggregates refer to it by ID. The language, context map and safety-net steps still apply. If a skill for tactical DDD is installed (for example the `ddd-core` plugin of [software-design-skills](https://github.com/yonatankarp/software-design-skills), with `ddd-aggregate` and `ddd-refactor`), suggest it for that part; otherwise use Evans' and Vernon's aggregate rules directly. Many systems are mixed; then use this skill for the data side and aggregate design for the transactional side.

## Start of every session

Look for `docs/REFACTOR_PLAN.md` (or the path the plan names).

- **It exists:** read its "Current status" section first, then the glossary and context map it points to. Summarise in two or three lines where things stand and what the next step is, then continue from there. Do not re-ask decisions already recorded.
- **It does not exist:** this is a new refactor. Start with the assessment below. Do not propose Step 0 until the user has decided to go ahead.

### Assessment first (new refactor only)

Before any refactoring, find out whether it is worth doing, and how much of it. Read `references/assessment.md` and follow it:

1. Read the system: entry points and jobs, module dependencies, storage and who reads it, external sources, outputs and their users. While reading, write the **dependency baseline** (`docs/DEPENDENCIES.md`): what each entry point writes, wrong-way dependencies (such as storage importing a data source), who reads which tables, and data oddities (orphaned data, a column whose name lies about its unit, mixed meanings under one name). Every later step should be able to say which line of this baseline it fixed.
2. Score the criteria in the reference (language, business rules, coupling, sources, growth, lifetime, a domain owner, capacity, safety, organisation), each with evidence from the code.
3. Ask the user only what the code cannot tell you.
4. Write `docs/DDD_ASSESSMENT.md` with a verdict: **A** full guided refactor, **B** lightweight DDD, **C** not now (cheaper fixes first), or **D** an organisational problem (consider data mesh). Include the expected contexts, the scope and the risks.
5. The user decides whether to go ahead (decision `A1`) and, on A or B, which **working mode** to use (decision `A2`, see below). Present the three modes in the same message as the verdict, with your recommendation, so one reply settles both. Then continue to Step 0 with the scope the verdict described.

If the user only asked "should we do DDD here?", stop after the report. Saying "not worth it" with good evidence is a successful outcome of this skill.

## Working modes

The user chooses how much they want to be involved. Offer the three modes once, after the assessment (or at the start of a resumed refactor whose plan records no mode), in plain words and with a recommendation. Record the choice as `A2` in the plan's working agreement; the user can switch at any time by saying so, and you record the switch as a new decision.

| Mode | Good when | Where you stop |
|---|---|---|
| **Step-by-step** | The user wants to learn the code or DDD, or the system is high-stakes and they want to see everything | After every sub-step: show the code, explain it, wait for acceptance |
| **Standard** (default) | Most refactors | Once per step to agree its decisions, then only when something new needs the user (see below); acceptance at the end of the step |
| **Fast** | The user has delegated the decisions or has a hard deadline | Only for the three things that always need the user (see below); report at milestones |

If the user's own words already pick a mode ("walk me through it", "just do it, you decide"), use it, say so in one line, and skip the question. Being in a hurry is not the same as delegating the domain: if unsure between standard and fast, ask.

**In every mode, these always come back to the user before they are applied:**

- anything that changes business outputs: rules that decide a report, a compliance verdict, an invoice or a trade; how missing data is treated; unit or time-zone corrections that change numbers; switching a source of truth;
- deleting or rewriting stored data;
- anything that touches production: merging, cutover, migrations, scheduled jobs.

**In every mode, the safety net stays:** the golden master before the first move, moves that keep outputs identical, one kind of change per commit, the plan and decision logs kept up to date.

### The loop

Each step goes through the same loop. The mode decides where the "wait" points are.

1. **Explain.** What this step does, why it comes now, what it will change, and the decisions it needs. Explain terms the first time they appear (for example "anti-corruption layer: the code that translates a vendor's names and units into ours"). In step-by-step mode, also walk through the files.
2. **Decide.** Put each open question as a short numbered item with options, your recommendation and evidence from the code or data. Step-by-step and standard: wait for the go-ahead. Fast: decide yourself and record it (below).
3. **Do.** Implement in small commits, sub-step by sub-step (`4a`, `4b`, …, each small enough to review in a few minutes). Step-by-step: stop after each sub-step for acceptance. Standard and fast: continue through the sub-steps, and stop only when you hit a new domain question nobody decided, a claim you cannot verify without real data or access you do not have, or one of the three things that always come back.
4. **Verify.** Tests and the golden check must pass (see `references/safety-net.md`). Back any claim about units, time zones, mappings or vendor behaviour with a check against real files or real API responses, not reasoning alone. If you cannot check it, say so and stop there rather than guessing.
5. **Accept.** Show what changed, how you verified it and what it means for production. Step-by-step: per sub-step. Standard: per step. Fast: at milestones, with everything you assumed and everything waiting for approval in one list.
6. **Record.** Update the plan's step table and "Current status" handover, and the decision logs. Write the handover so that a session with no memory of this one could continue.

### Fast mode details

**You decide, and record:** code structure and context boundaries, internal names, the order of work, implementation choices, and glossary items that only name or describe what the system already does. Write each as a normal decision with "(assumed by Claude, fast mode)" in place of the user's words, so the owner can review all of them in one pass and overturn any.

**For the things that always come back:** prepare them so they are ready to apply (a separate commit, branch or patch, with the before/after diff), but do not apply them in the same change as the restructure. Batch them into one short list with your recommendation, so one reply can approve all.

**The assessment still happens**, in short form; a C verdict still means saying so.

### Decisions

Every domain decision gets a numbered ID, the date and the user's answer in their own words:

- `T1, T2, …` terms and rules, in the glossary's decision log
- `C1, C2, …` context boundaries and relations, in the context map's decision log
- step-local letters for implementation choices (for example `S1` for schema, `D1` for a step plan), in the plan

IDs let later steps cite the reason for a rule ("NULL, not 0 (T10)"), and they let a new session find out why something is the way it is. When a later decision changes an earlier one, write "T30 revises T7" rather than editing history.

When drafting the glossary or context map, quote contradictions you found in the code ("this column is called `duration_min` but the values are seconds"). Contradictions are the most useful questions you can bring.

## Rules, and why they exist

- **One kind of change per step.** A step either moves code (outputs must be identical) or changes behaviour (verified on its own, with the diff explained). Mixing them makes it impossible to tell a bug from an intended change. Behaviour changes found in the glossary go into a "deferred changes" list and get their own step later.
- **New beside old, then delete old.** Build the new context next to the legacy code, compare them, switch callers over, then delete the legacy path. Never rewrite in one go.
- **The safety net stays green at the end of every step.** If the golden check fails, the step is not done.
- **Development never touches production data.** Work on a copy. Compare against production backups or read-only copies.
- **No credentials in files.** API keys and tokens come from environment variables or the current process. Recorded HTTP fixtures are scrubbed before commit.
- **Write things down.** If it is not in the plan, the glossary or the context map, the next session will not know it.
- **Talk to the user in their language.** Keep code, file names and domain names in whatever language the codebase uses; the glossary can give both.

## The steps

The default order is below. Read `references/steps.md` for each step's goal, the decisions it needs, what "done" means and its pitfalls, before you explain that step to the user.

| Step | What | Output |
|---|---|---|
| 0 | Safety net: protected production, dev copy, backups, golden master | Production unchanged but protected |
| 1 | Ubiquitous language: names, units, time, sources of truth | `docs/glossary.md`, no code |
| 2 | Bounded contexts and context map | `docs/context-map.md` |
| 3 | Shared kernel: the few value types everyone shares | Small pure module and its tests |
| 4 | One template context, end to end, run in parallel with legacy | The pattern for every other context |
| 5 | The other upstream (source-of-facts) contexts, one at a time | Read side and adapters moved |
| 6 | Cross-cutting concerns: events, data quality, integration | Contexts talk without tangling |
| 7 | Downstream contexts; retire the legacy code | Legacy entry points deleted |
| 8 | New storage schema behind the repositories | Versioned migrations, rehearsed cutover |
| 9 | Consumers and frontend on the new services | Every reader goes through services |
| 10 | The first new feature, as proof the structure works | One new context, nothing else touched |

Reorder when the situation asks for it, and tell the user why. For example: the frontend can start right after Step 7 if users are waiting; a small codebase can merge Steps 3 and 4; a system with no database can skip Step 8. Steps 1 and 2 are not skipped, because everything after them depends on their names and boundaries.

## Architecture inside a context

Default to the **diamond (symmetric) architecture** (Zhang Yi): each context has a northbound side (`ohs/remote` for APIs, jobs and event handlers; `ohs/local` for application services and their DTOs), a pure `domain` in the middle, and a southbound side (`acl/ports` and `acl/adapters` for databases, vendors and other contexts). If the user or codebase already uses hexagonal or clean architecture, map the same rules onto that layout. See `references/architecture-styles.md`.

The rules that matter more than the folder names:

- Other contexts and the UI import only a context's local services, never its domain internals or tables.
- Each table belongs to exactly one context.
- Vendor names, units and time zones are translated in that context's adapters and never leak further.
- Adapters are wired to services in one composition root.
- Upstream never imports downstream; when upstream must notify downstream, publish an event.

## Revisiting the verdict

The assessment can be wrong. If a later step shows the problems are smaller or bigger than expected (for example the glossary finds almost nothing to decide, or Step 2 finds ten contexts where the assessment expected three), say so, and offer to change the scope: drop to lightweight, stop after the glossary, or extend. Record it as a new `A` decision.

## Files you maintain in the user's repo

Start each from the templates in `templates/` and adapt them to the project:

- `docs/REFACTOR_PLAN.md`: goal, architecture, working agreement, step table with status, **current status handover**, per-step plans, open questions. From `templates/REFACTOR_PLAN.md`.
- `docs/glossary.md`: naming rules, terms by topic, deferred behaviour and data changes, decision log. From `templates/glossary.md`.
- `docs/context-map.md`: layers, contexts (what each owns and provides), relations, events, table ownership, decision log. From `templates/context-map.md`.

When the refactor is finished, suggest moving the plan to `docs/history/` and writing a short architecture document and a handover for future maintenance, so the plan stops being the place people look for how the system works today.

## Lessons, domain packs and a worked example

- `references/lessons.md`: mistakes that come up again and again in data platforms of any domain: names that lie, units, time zones and DST, NULL versus 0, "never fetched" versus "fetched, no value", source priority, snapshot versus latest, recovery windows, spreadsheets and email as inputs. Read it before the assessment and again before Step 1. Most glossary questions worth asking are in it.
- `domains/`: domain packs with the concepts, traps and typical contexts of one industry. If the user's domain has a pack (see `domains/README.md`), read it before Step 1 and use it to draft sharper glossary questions. Never impose a pack's names on the user; their business decides. If there is no pack, the general lessons are enough.
- `examples/power-trading.md`: one real refactor from assessment to new feature, sanitised. Read it when you need to show the user what a step's output looks like in practice, whatever their domain.
