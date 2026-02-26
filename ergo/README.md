# Ergo

This directory contains technology-agnostic (`core/`) and technology-specific (`tech/`) conventions.
Keep domain and project-specific information out of this layer.

## Core

- [`core/coding-conventions/ports.md`](core/coding-conventions/ports.md) — Ports and dependency-direction conventions.
- [`core/coding-conventions/operations.md`](core/coding-conventions/operations.md) — Operations modeling conventions.

## Tech

- [`tech/jvm/coding-conventions/packages.md`](tech/jvm/coding-conventions/packages.md) — Package layout conventions.
- [`tech/jvm/coding-conventions/naming.md`](tech/jvm/coding-conventions/naming.md) — Component naming suffix taxonomy.
- [`tech/kotlin/testing.md`](tech/kotlin/testing.md) — Kotlin testing conventions.
- [`tech/kotlin/object-mothers-and-fixture-data.md`](tech/kotlin/object-mothers-and-fixture-data.md) — `*ObjectMother` conventions and fixture data generation rules.
- [`tech/kotlin/ubiquitous-test-fixtures.md`](tech/kotlin/ubiquitous-test-fixtures.md) — A minimal baseline fixture pattern (SQL seed + `the*` references).
- [`tech/spring/testing.md`](tech/spring/testing.md) — Spring testing conventions.
- [`tech/spring/reusable-test-datasource.md`](tech/spring/reusable-test-datasource.md) — A reusable DB `DataSource` pattern for Spring integration tests.
- [`tech/spring/testing-infrastructure-slices.md`](tech/spring/testing-infrastructure-slices.md) — An experimental pattern for composing test infrastructure from small slices instead of base test classes.
- [`tech/spring/data-jdbc.md`](tech/spring/data-jdbc.md) — Spring Data JDBC repository conventions.
