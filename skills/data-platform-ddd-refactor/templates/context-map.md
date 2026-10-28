# Context map

<!-- Output of Step 2. Which bounded contexts exist, what each owns, and how they interact. All names come from docs/glossary.md. -->

Status: **draft**. Decisions in "Decision log".

## 1. Layers

```
<master data context>          (top: everything refers to its IDs)
        │
<upstream contexts>            facts from the outside world, each with its own storage
        │  ohs/local services + events (e.g. ObservationsIngested)
        ▼
<downstream contexts>          decisions, reports, exports

<cross-cutting contexts>       e.g. data quality: audits upstream, triggers backfills
```

Dependencies point one way. Where a lower layer must tell an upper one something, it publishes an event.

## 2. Contexts

### Shared kernel

<!-- Not a context. Only small value types and pure functions everyone uses: time grid, units, IDs, events. Changes need everyone's agreement. -->

### <context name>

- **Role:** master data / upstream / downstream / cross-cutting
- **Keyed by:** <!-- asset, device, site, market, customer… -->
- **Owns:** <!-- tables, config, derived values -->
- **Provides (ohs/local):** <!-- services and what they answer -->
- **Needs:** <!-- other contexts' services, through its own ports -->
- **External systems:** <!-- vendors, files, inboxes, behind its adapters -->

<!-- repeat per context -->

## 3. Relations

| Downstream | Upstream | How | Notes |
|---|---|---|---|
| | | port + adapter calling upstream `ohs/local` | |

## 4. Events

| Event | Published by | When | Subscribers and what they do |
|---|---|---|---|
| | | | |

## 5. Ownership of tables and data

| Table / data | Owning context | Written by | Read through |
|---|---|---|---|
| | | | |

## Decision log

| Date | ID | Decision |
|---|---|---|
| | C1 | |
