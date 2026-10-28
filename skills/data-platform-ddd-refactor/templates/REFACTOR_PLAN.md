# DDD refactor plan

<!-- The single source of truth for the refactor: steps, status and handover. Update it at the end of every session. A new session reads "Current status" first. -->

Assessment: verdict <A full / B lightweight> (A1, YYYY-MM-DD), see `docs/DDD_ASSESSMENT.md`. Baseline: `docs/DEPENDENCIES.md`.

## Goal

<!-- Two to four bullets: what the platform should look like when the refactor is done, and why. Example: "storage is the single entry point, backed up and versioned; every vendor behind an adapter; derived values recomputed when inputs change". -->

## Architecture

<!-- The style (diamond by default) and the folder layout every context follows. List the contexts once Step 2 has decided them, with a pointer to docs/context-map.md. -->

```
contexts/<context>/
  domain/        pure rules, no I/O
  acl/ports.py   what the context needs from outside
  acl/adapters/  storage, vendors, other contexts
  ohs/local/     services + DTOs (the only public entry)
  ohs/remote/    API routes, jobs, event subscribers
shared_kernel/   shared value types
ops/             composition root, job entry point
```

Rules:

- Other contexts and the UI import only `ohs/local`.
- Each table belongs to one context.
- Vendors appear only in adapters.
- Wiring happens only in the composition root.
- Upstream notifies downstream through events.

## Working agreement

- Production runs from `<prod checkout>` (branch `prod`); development happens in `<dev worktree>` (branch `dev`) with its own data copy. Development never touches production data.
- New code grows beside the legacy code and takes over one piece at a time; legacy code is deleted after takeover.
- One kind of change per step: move code (identical outputs) or change behaviour (verified separately).
- At the end of every step, tests and `golden check` pass.
- Working mode (A2): <step-by-step / standard / fast>, chosen YYYY-MM-DD. Step-by-step: accept every sub-step. Standard: agree each step's decisions, accept each step. Fast: Claude decides and records assumptions, reports at milestones.
- In every mode, output-changing fixes, deleting or rewriting stored data, and anything touching production come back to the owner before they are applied.

## Steps and status

| Step | Content | Status |
|---|---|---|
| 0 | Safety net: protected production, dev worktree, backups, golden master | |
| 1 | Ubiquitous language → `docs/glossary.md` (no code; the owner decides) | |
| 2 | Bounded contexts and context map → `docs/context-map.md` | |
| 3 | Shared kernel | |
| 4 | Template context: `<name>` | |
| 5 | Other upstream contexts: `<names, in order>` | |
| 6 | Events, data quality, integration | |
| 7 | Downstream contexts: `<names>`; retire legacy | |
| 8 | New storage schema behind repositories | |
| 9 | Consumers and frontend | |
| 10 | First new feature: `<name>` | |

<!-- Status examples: "✅ 2026-10-09 (dev abc1234)", "in progress: 5b done, 5c next", "merged to prod 2026-10-12 (merge-4, rollback tag prod-pre-4)". -->

## Current status (YYYY-MM-DD)

<!-- The handover. Write it so a session with no memory can continue. Cover:
- What runs in production now (commit or tag, jobs, anything still on legacy code).
- What is done on dev but not merged, and what blocks the merge.
- The next step and its first sub-step.
- Known issues the owner decided not to fix yet, and why.
- Operational notes (how to restart services, on-demand commands, gotchas).
-->

## Step N plan (YYYY-MM-DD)

<!-- One section per large step, written when the step starts:
- sub-steps (Na, Nb, …), each with what it changes and how it is verified;
- decisions for this step (D1, D2, … or S1, S2, …) with the owner's answers;
- the merge order and rollback.
Mark sub-steps ✅ with date and commit as they finish. -->

## Open questions

<!-- Numbered questions waiting for the owner. Strike through when answered and point to the decision ID. -->

## Later (not part of the refactor)

<!-- Ideas and new features that came up; they go to a backlog when the refactor ends. -->
