# Kotlin: Object Mothers and Fixture Data Generation

This document defines conventions for coding `*ObjectMother` factories and related fixture data generation utilities.
The goal is to keep tests readable, keep defaults safe, and avoid hidden coupling through implicit data graphs.

## Scope

These conventions apply to JVM projects (Kotlin/Java) that use the EA test code architecture.
They complement:

- `testing.md` (how tests are structured and which fixture layers exist).
- `ubiquitous-test-fixtures.md` (baseline SQL seed and `the*` references).

## Vocabulary

- `the*` — a stable shared reference entity (often from baseline seed).
- `a*` / `an*` — a factory method that generates a new fixture value or entity.
- Required link — a mandatory reference (for example a non-null FK).

## Placement

Follow `../jvm/coding-conventions/packages.md` for test fixture package layout (`...tests.fixture.object_mothers...`).

## Naming

Follow `../jvm/coding-conventions/naming.md` for canonical fixture factory naming (`*ObjectMother`, `a*` / `an*`).
Use the `the*` prefix for baseline/shared entities.

## Rule: Required Links in `a*` / `an*` Generators

In `*ObjectMother` (and similar fixture factories), `a*` / `an*` methods often accept parameters for links to other entities.
For required links (foreign keys / mandatory references), `a*` / `an*` methods must follow one of these options.

- The parameter default value is a shared baseline reference (`the*`) or a reference to it (for example `Ref` or `id`).
- The parameter has no default value and must be provided explicitly by the caller.

`a*` / `an*` methods must not generate the linked entity implicitly as a default value.

## Rule: Defaults Must Not Hide Structure

Defaults are allowed only when they reduce noise without hiding an important relationship.
If a relationship matters to the scenario, prefer requiring it explicitly.

## Rule: Keep `*ObjectMother` Pure

`*ObjectMother` must not:

- Call production code.
- Perform IO.
- Insert data into the database.

Use `*FixturePresets` / `*TestApi` for insertion and orchestration.

## Notes

This document intentionally focuses on fixture value generation and small factories (`a*` / `an*`).
For fixture layering and insertion orchestration (`*Fixture`, `*FixturePresets`, `*TestApi`), see `testing.md` and `../../../concepts/testing-testcode-architecture.md`.
