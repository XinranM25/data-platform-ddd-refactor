# Safety net

How to change a running system without breaking it. Set this up in Step 0 and use it at the end of every step.

## Production and development

- **Two checkouts.** Production runs from a protected branch (for example `prod`) in its own directory. Development happens in a separate git worktree on `dev`, with its own environment and its own copy of the data. Production jobs, services and schedules point only at the production directory.
- **Data never flows from dev to prod by hand.** Code reaches production only by fast-forward merge. Dev data is refreshed from production backups, never the live store.
- **Backups.** Automatic, daily, with a few kept. Test a restore once. Take an extra backup before every merge that includes a migration.

## Golden master

A golden master answers one question: did this step change any business output?

1. **Freeze inputs.** Copy the relevant data into a read-only snapshot, dated (for example `golden_snapshot_YYYYMMDD`). Never compare against live data, which changes daily.
2. **Choose outputs.** The user picks the outputs that matter: derived columns, reports, exports, key query results. Prefer many small comparable values to one big file.
3. **Record.** For each output, a `produce_<output>()` function computes it from the snapshot through the current code path, and the result is saved as the baseline.
4. **Check.** `golden check` re-runs every `produce_*` function and compares with the baseline, with a tolerance only where floating point requires one. Print OK or the first differences per output.
5. **Point at new code.** When a step moves logic, change the `produce_*` function to call the new path. The baseline does not change. That is what proves the move.
6. **Regenerate only on purpose.** When an approved behaviour change (from the glossary's deferred list) is implemented, show the user the diff (how many values changed, by how much, why), and only then regenerate the baseline. Record which decision it implements.

If the snapshot's storage format changes (Step 8), migrate the snapshot with the same migration script as production, so the check keeps working.

## Parallel runs

When a step replaces something production does every day (fetching, computing, writing), run the new path on dev on the same schedule for a few days, writing to the dev store, and compare it with production's results each day (read production's latest backup, never the live store). A compare script that prints "N rows identical" or the differing rows is enough. Merge once the agreed number of days is clean.

## Tests

- Unit tests for domain rules and the shared kernel, with edge cases (DST days, empty inputs, missing values).
- Adapter tests against **recorded HTTP responses**, re-recorded by setting an environment flag. Strip auth headers when recording and search the recordings for real credentials before committing.
- Tests that build empty stores from the real schema, not from hand-written test schemas that drift.
- Real files (vendor exports, emailed reports) that cannot be committed stay in an ignored local folder; tests that need them skip when they are absent.

## Cutover rehearsal (storage changes)

Before switching production to a new store:

1. Copy the production store to a read-only file.
2. Run the migration against it, time it, and read the reconciliation report (row counts and sums per series, plus anything the script refused).
3. Compare old code on the old store against new code on the new store over the full history.
4. Write the cutover checklist: exact commands, the order, expected durations, checks after each step, and the rollback. Pick a quiet window, and avoid days with known risk (DST change, month end, a deadline).

## Merge checklist

See "Merging to production" in `references/steps.md`. Tags `merge-N` (what was merged) and `prod-pre-N` (where production was before) make every merge reversible with one reset.

## Several sessions in one workspace

A long refactor often runs in several AI sessions (for example a backend one and a frontend one) on the same dev checkout. Agree who owns which folders. Commit only explicitly listed paths, never "add everything", or you will commit another session's half-done work. After changing anything a running dev server loads (config, composition root, service interfaces), restart it.
