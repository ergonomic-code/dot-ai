# Coding conventions: Package layout

## Intention

This document defines a default package layout for JVM backend services.
The goal is to make the codebase navigable, keep boundaries explicit, and make Ports, Operations, and Resources easy to locate.

This layout is a soft recommendation.
Projects may adopt it as-is, adapt it, or ignore it.

## Scope

These conventions apply to Kotlin/Java package structure (and analogous folder/namespace layouts in other languages).

## Canonical top-level packages

Use the following top-level packages as the default vocabulary.

- `app` — Ports and Operations (what the system does).
- `domain` — Domain Resources and domain model (what the system is).
- `i9ns` — external integrations (resources owned by other organizations).
- `infra` — factories and wiring/adapters required to run the system.
- `platform` — cross-domain reusable utilities and components.

Aliases.

- `core` is a common alias for `domain`.
- `integrations` is a common alias for `i9ns`.

## `app` decomposition

Split `app` into subpackages using one primary axis for the subsystem.
Choose one of the following decomposition styles.

- Use cases (closest to requirements).
- Client applications and their UI structure.
- Mirroring the `domain` structure.
- REST API resources.
- Features (a developer-defined unit of change).
- A custom decomposition, explicitly defined by the project.

Rule.

- Prefer one dominant decomposition style per subsystem.
- Allow exceptions only when they improve discoverability and are explicitly recorded in project context.

## `domain` decomposition

Split `domain` by resources at the first level.
Each resource package may then contain stable subpackages for model, DTOs, and persistence details.

Canonical resource package structure (recommended).

- `<root>.domain.<resource>/`
  - `<resource>Repo` (or another resource façade) at the package root.
  - `model/` — conceptual domain model.
  - `views/` — outward-facing read models.
  - `persistence/` — persistence model and DB access details (if the resource has a dedicated persistence model).
  - `commands/` — DTOs for state-changing requests.
  - `queries/` — DTOs for complex read requests.

## `platform` and `infra` at any level

You may add `platform` and `infra` packages at any level.
Use them to localize shared code to a scope and to keep wiring separate from business code.

### `*.platform`

Use `*.platform` for:

- top-level functions and small reusable types shared by multiple siblings under the parent package;
- components for which multiple runtime instances are created (for example, `FileStorage(name)` used by multiple resources).

### `*.infra`

Use `*.infra` for factories and wiring for the parent scope.
In Spring, this typically includes `@Configuration` classes and bean factories.

## Example tree

```text
<org.my.app>
  app/
      <module-or-feature>/
        <Something>Controller
        <Something>Listener
        <Something>Scheduler
        <Something>Op
      infra/
        <Something>Conf

  domain/
    <resource>/
      <Resource>Repo
      model/
        ...
      views/
        ...
      commands/
        ...
      queries/
        ...
      persistence/ (if the resource has a dedicated persistence model)
        <Resource>Row
        <Resource>Dao

  i9ns/
    <integration>/
      <Integration>Client
      <Integration>Channel
      <Integration>Queue

  infra/
    <System>Conf

  platform/
    errors/
      ...
    kotlin/
      ...
    spring/
      ...
```
