# APPLICATION/SERVICE-CONTEXT (template)

Goal: briefly but sufficiently describe the structure of the repository so that an agent can work effectively without re-scanning the entire codebase.

## 1. Project Overview

`<name>` — `<what this repository is>`.

## 2. Tech Stack

* Language: `<version>`
* Runtime: `<version>`
* Build: `<tool>`
* Storage/DB: `<...>`
* Messaging: `<...>`

## 3. Architecture

### 3.1 Modularity / Composition

Describe the module structure and how the application is assembled.

### 3.2 Layers and Dependencies

Describe the layering conventions and dependency rules.

### 3.3 Code Layout and Naming

Describe the top-level package layout used by the project.
Recommended default vocabulary is `app/domain/i9ns/infra/platform`, with common aliases `core` and `integrations`.

List naming conventions enforced by the project.
Recommended default suffix taxonomy includes `*Controller`, `*Listener`, `*Scheduler`, `*Op`, `*Repo`, `*Client`, `*Channel`, `*Queue`, `*Conf`, `*Rq`, `*View`, `*Rs`, `*Row`, and `*Dao`.

Record any project-specific exceptions (for example, allowed `*Service` usage and a migration plan).

## 4. Key Files & Directories

List of key directories and files.

## 5. Entry Points

Where the entry points are located (runtime, API, jobs, listeners).

## 6. Dependencies Map

Simplified dependency map.

## 7. Build & Dev Workflow

Build, run, and test commands.

## 8. Project-specific Notes

Rules that apply only to this project.
