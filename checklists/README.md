# Checklists

This directory contains review checklists primarily derived from `../conventions/ea-principles.md`.
Checklists are intended to be referenced from specs and skills as lightweight self-audits.

## How to use checklists

Before non-trivial coding, refactoring, or review, select checklist packs on two axes and read the union of the matched packs.

1. Activity lens:
   what kind of work is happening now.
2. Artifact lens:
   what kind of code or contract is being touched.

If a reusable skill also applies, open it only after the mandatory checklist packs have been read.

## Index

- [`testing.md`](testing.md) — Testing and contracts.
- [`git.md`](git.md) — Git hygiene and staging.
- [`code-hygiene.md`](code-hygiene.md) — DRY pass, helpers, and duplication control.
- [`data-model.md`](data-model.md) — Data model shape and invariants.
- [`api-design.md`](api-design.md) — API contracts, DTO shape, and CQS.
- [`operations.md`](operations.md) — Effectful responsibilities and orchestration boundaries.
- [`subprograms.md`](subprograms.md) — Common rules for any non-trivial function or method.
- [`calculations.md`](calculations.md) — Pure transformations and decision logic.
- [`integrations.md`](integrations.md) — External integrations and mapping.
- [`classes.md`](classes.md) — Class design, state, and effects.
- [`architecture.md`](architecture.md) — Dependency graphs and blast radius.

## Routing matrix

### Activity lens

- Fixing failing tests or changing test behavior:
  read [`testing.md`](testing.md).
- Designing or changing data shape, nullability, constructors, DTO fields, or serialization shape:
  read [`data-model.md`](data-model.md).
- Designing or changing an HTTP or RPC contract, DTO boundary, query parameter set, or response shape:
  read [`api-design.md`](api-design.md).
- Designing, implementing, or refactoring a non-trivial function, method, or helper:
  read [`subprograms.md`](subprograms.md).
- Designing, implementing, or refactoring an operation, use case, handler flow, or workflow orchestration:
  read [`subprograms.md`](subprograms.md) and [`operations.md`](operations.md).
- Designing, implementing, or refactoring external calls, mappers, persistence boundaries, adapters, or contract translation:
  read [`integrations.md`](integrations.md).
- Reviewing architecture, dependency structure, or class responsibilities:
  read [`classes.md`](classes.md) and [`architecture.md`](architecture.md).
- Changing class responsibilities, state ownership, or dependency graph shape:
  read [`classes.md`](classes.md) and [`architecture.md`](architecture.md).

### Artifact lens

- Test files, `src/test`, `*Test*`, `*HttpApi`, `*TestApi`, `*FixturePresets`, or failing test commands:
  read [`testing.md`](testing.md).
- Records, entities, value objects, data classes, DTOs, constructors, nullable fields, or serialization models:
  read [`data-model.md`](data-model.md).
- Controllers, OpenAPI, request and response DTOs, query params, status codes, or transport contracts:
  read [`api-design.md`](api-design.md).
- Repositories, DAOs, SQL, external clients, adapters, or mapping code:
  read [`integrations.md`](integrations.md).
- Operation code, service methods, handlers, or workflow orchestration:
  read [`subprograms.md`](subprograms.md) and [`operations.md`](operations.md).
- Pure transformation code, decision helpers, selectors, reducers, or validation calculations:
  read [`subprograms.md`](subprograms.md) and [`calculations.md`](calculations.md).
- Dependency wiring, large classes, mutable state, or cross-module changes:
  read [`classes.md`](classes.md) and [`architecture.md`](architecture.md).

## Example

If the task is to fix a failing test that surfaced a data-shape problem in a DTO or response model, the mandatory read set is:

- [`testing.md`](testing.md),
- [`data-model.md`](data-model.md),
- and, when the shape is part of a public transport contract, [`api-design.md`](api-design.md).
