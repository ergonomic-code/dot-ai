# Coding conventions: Component naming (suffixes)

## Intention

This document defines a default naming taxonomy for class suffixes.
The goal is to make component kind and boundary visible at the call site and in code search results.

The suffix taxonomy aligns with the Ergonomic Components Structure (Ports, Operations, Resources, and Primitive Resources).
See `../../../../concepts/ergonomic-components-structure.md`.

## Scope

These conventions apply to JVM backend services (Kotlin/Java) and can be adapted to other stacks.

## Canonical suffixes

### Ports (entry points)

- `*Controller` — HTTP request handlers (a Port).
- `*Listener` — event/message handlers (Spring events, RabbitMQ, Kafka, and similar).
- `*Scheduler` — scheduled trigger handlers (a Port invoked by a scheduler).

Port behavior constraints are defined in `../../../core/coding-conventions/ports.md`.

### Operations (scenarios)

- `*Op` — an application operation implementing one scenario (an Operation).

Operation behavior constraints are defined in `../../../core/coding-conventions/operations.md`.

### Resources (effects and state)

- `*Repo` — a Resource façade for state and stateful effects (DB, storage, etc.).
- `*Client` — a Resource façade for an external system API.
- `*Channel`, `*Queue` — a Resource façade for messaging infrastructure.

### Infrastructure wiring

- `*Conf` — DI configuration and factories (for example Spring `@Configuration`).

### DTOs and data records

- `*Rq` — a request DTO (both commands and queries).
- `*View` — an outward-facing view/read model DTO.
- `*Rs` — a transport response DTO when it is distinct from `*View`.
- `*Row` — a persistence row/record DTO.

### Test-only suffixes (test sources)

- `*HttpApi` — a typed HTTP client used by tests to call ports through transport.
- `*TestApi` — a typed façade used by tests and fixture insertion to call production code directly.
- `*Fixture` — a declarative data graph for scenario state and stubs.
- `*FixturePresets` — a fixture builder and inserter that materializes `*Fixture` via production calls (directly or via `*TestApi`) and `Mock*Server`.
- `Mock*Server` — a wrapper over a stubbing tool (for example WireMock) that owns stubs and defaults.
- `*ObjectMother` — factories/builders for production data types used in tests.

Rule.

- In `*ObjectMother` (and similar fixture factories), method names that generate fixture objects and values must start with the `a` / `an` prefix (for example `aHotel`, `aRoom`, `aReservationPeriod`, `anObserver`, `anEvent`).

### Primitive resources (implementation details)

- `*Dao` — a low-level persistence or infrastructure detail used to implement a higher-level Resource.

## Placement hints (package layout)

These placement hints assume the canonical package layout from `packages.md`.
See `packages.md` in this directory.

- `*Controller`, `*Listener`, `*Scheduler`, and `*Op` belong under `app`.
- `*Repo` belongs under `domain.<resource>` (usually at the package root).
- `*Dao` and `*Row` belong under `domain.<resource>.persistence`.
- `*Client`, `*Channel`, and `*Queue` belong under `i9ns.<integration>`.
- `*Conf` belongs under `infra` or `*.infra` for the relevant scope.

## Rules

### Rule: One primary suffix per class

A class name should communicate one primary responsibility.
If a class naturally wants multiple suffixes, split it.

### Rule: Prefer specific suffixes over `*Service`

`*Service` is discouraged.
Treat it as a smell indicating that a component kind is unclear or responsibilities are mixed.

Allowed transitional use.

- If existing code uses `*Service`, keep it as a temporary name only when a rename would be disruptive.
- Record a follow-up refactor to replace `*Service` with an explicit suffix (`*Op`, `*Repo`, `*Client`, etc.) or to split responsibilities.
