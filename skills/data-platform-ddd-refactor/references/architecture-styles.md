# Architecture inside a bounded context

The default is the diamond (symmetric) architecture described by Zhang Yi (张逸). If the codebase or the user prefers hexagonal (ports and adapters) or clean architecture, use the mapping table below; the rules are the same.

## Diamond layout

```
contexts/<context>/
  domain/            pure rules and values, no I/O; names come from the glossary
  acl/               southbound gateway (anti-corruption layer)
    ports.py         what this context needs from outside, in its own language:
                     repositories, vendor feeds, other contexts, event publishing
    adapters/        implementations: storage, vendor clients, calls into other
                     contexts' local services, file and inbox readers
  ohs/               northbound gateway (open host service)
    local/           application services + DTOs (the published language);
                     the only thing other contexts and the UI may import
    remote/          web routes, scheduled job functions, event subscribers
```

Outside the contexts:

- `shared_kernel/`: small value types and pure functions every context uses (time grid, units, IDs, events). Changing it affects everyone, so changes need the user's agreement.
- a composition root (for example `ops/composition.py`): the one place where adapters are created and wired into services, and event subscribers are registered.
- job entry points and the web shell, which call the composition root.

The shape is a diamond because both sides are gateways: north serves callers, south talks to the outside world, and the domain sits between them, unaware of either.

## Rules

1. Dependencies point inward: `remote` → `local` → `domain`; `adapters` implement `ports`; `domain` imports nothing outside itself and the shared kernel.
2. Between contexts, the downstream context declares a port in its own `acl/ports` and implements it with an adapter that calls the upstream context's `ohs/local`. Downstream code never imports upstream domain objects or reads upstream tables.
3. Each table belongs to exactly one context.
4. External systems appear only in their context's adapters, which translate names, units and time zones.
5. Adapters are wired only in the composition root.
6. Upstream never imports downstream. When upstream must notify downstream (new data arrived), it publishes an event; downstream subscribes in its `ohs/remote`.

## Mapping to other styles

| Concept | Diamond | Hexagonal | Clean architecture |
|---|---|---|---|
| Business rules | `domain/` | domain (core) | entities |
| Use cases / services | `ohs/local/` | application services (driving ports) | use cases (interactors) |
| Inbound delivery (HTTP, jobs, events) | `ohs/remote/` | driving adapters | controllers / presenters |
| Interfaces to the outside | `acl/ports` | driven ports | gateways (interfaces) |
| Implementations (DB, vendors) | `acl/adapters/` | driven adapters | frameworks and drivers |
| Calls to another context | adapter calling its `ohs/local` | driven adapter | gateway implementation |
| Wiring | composition root | composition root | main / dependency injection |

Pick one style and use it the same way in every context. A consistent layout lets the user find anything without reading the code first.

## How much structure

Scale the layering to the context. A small downstream context with one service and no storage may need only `domain/` and `ohs/local/` plus a port or two. Do not create empty folders to complete the shape. What must never be skipped is the rule set: no table reading across contexts, vendor translation only in adapters, wiring in one place.
