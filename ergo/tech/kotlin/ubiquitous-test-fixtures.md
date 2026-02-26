# Ubiquitous Test Fixtures (Baseline Seed)

This document defines a baseline fixture pattern for integration tests.
The goal is to keep scenario setup inside `*TestApi` / `*FixturePresets`, while still allowing a minimal ubiquitous set of reference entities to exist in every test database.

## Problem

Some domains rely on “reference” entities that are used by many tests as link targets.
Examples include a single default tenant, a default hotel, a set of roles, or other stable rows referenced by foreign keys.
Creating them repeatedly in every test adds noise and is slower.
Creating them through production code in every test can also be harder than inserting stable rows once.

## Rule

- Use SQL scripts only for a minimal ubiquitous baseline fixture.
- Treat everything else as scenario setup and build it via `*TestApi` and `*FixturePresets`.
- For each baseline entity inserted by SQL, provide a `the*` constant (or value) in the relevant `*ObjectMother` so tests can reference it.
- See `object-mothers-and-fixture-data.md` for `*ObjectMother` placement and naming conventions.

## SQL Baseline Fixture

Keep baseline inserts in a SQL script executed on DB reset.
The exact mechanism is project-specific.
Prefer a dedicated reset step that runs `baseline.sql` after truncation.
Using `data.sql` on application boot works only if boot reliably happens after each reset (or if each test gets a fresh database).

Baseline rows must be:

- Deterministic (stable IDs, stable business keys).
- Minimal (only what most tests truly need).
- Restorable by reset (tests may mutate them, as long as the next reset reliably returns them to the baseline state).

## `the*` Values in `*ObjectMother`

Define `the*` values as stable references to baseline rows.
They must match exactly what SQL inserts.

Example (Kotlin):

```kotlin
object HotelsObjectMother {
    // Inserted by baseline SQL (for example baseline.sql executed during DB reset)
    val theHotel = HotelInfo(
        Hotel.ref(UUID.fromString("0196f8b0-2b3c-7f12-8a45-1c2d3e4f5a6b")),
        mapOf(RoomType.LUX to 1)
    )

    fun aHotel(): Hotel = Hotel()
}
```

Keep `the*` values inside the relevant `*ObjectMother` object.
If a `the*` value is shared across many fixtures, keep it near the top of the relevant `*ObjectMother`.

## Failure Modes

- Baseline grows into a second production dataset.
- Tests start relying on baseline mutations.
- IDs in code diverge from SQL, causing confusing FK failures.

## Verification

- Deleting all `*TestApi` / `*FixturePresets` fixture insertions should still allow the application to boot, but not allow most scenarios to pass.
- Running a single test in isolation should produce the same baseline rows as running the full suite.
