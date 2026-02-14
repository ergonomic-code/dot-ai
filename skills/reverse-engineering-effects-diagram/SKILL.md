---
name: reverse-engineering-effects-diagram
description: "Reverse engineering an effects diagram from existing code (when requirements are missing or insufficient): extracts events/operations/resources/effects from entry points and external resource accesses (input/output), records uncertainties, and saves the result in the textual effects diagram format (YAML/JSON). Use when analyzing an unknown system, planning refactoring, assessing regression risk, and reconstructing current (“as-is”) behavior."
---

# Effects diagram: reverse engineering from code

See the definition and format of the diagram in `concepts/effects-diagram.md`.

## Input

* `CODE_ROOT` — the root of the codebase or subsystem for which the diagram is being built.
  If `CODE_ROOT` is not explicitly specified, determine it from context (for example, from file/directory paths already mentioned in the task).
  Ask the user for `CODE_ROOT` only if the boundary is unclear or if there are multiple possible options.

* `DIAGRAM_PATH` — the path where the diagram should be saved (for example, `effects-diagram.as-is.yaml`).

* Optional: `DIAGRAM_VISUAL_PATH` — the path where a human-readable visual representation should be saved (for example, `effects-diagram.as-is.md` with Mermaid).

* Optional: a list of known entry points (endpoints, jobs, message handlers).

## Output

* Effects diagram in `DIAGRAM_PATH` using the format defined in `concepts/effects-diagram.md`.
* Mermaid visual representation of the diagram (if `DIAGRAM_VISUAL_PATH` is specified).
* A short report at the end of the response:

  * what was included in the `scope` boundary;
  * which `TBD` items remain;
  * which effects/resources appear risky in terms of regression.

## Algorithm

1. Determine `CODE_ROOT` and confirm the `scope` boundary.
2. Identify input events and entry operations.
   Locate methods/functions invoked externally by the platform (HTTP, queue, scheduler, CLI).
3. Create a draft of `events`, `operations`, and `triggers`.
   If a handler directly implements behavior, treat it as an operation.
   If a handler delegates to “application logic,” treat the delegated target method as the operation.
4. Identify resources.
   Include in `resources` all input/output and state elements accessed by operations (databases, queues, files, caches, external HTTP/gRPC/SOAP APIs).
5. Extract effects for each operation.
   For every resource access, add an `effect` with `kind: read|write` and minimal `data`.
   If the effect type is unclear, mark it as `TBD` and keep a `trace` pointing to the relevant code location.
6. Normalize names.
   Rename “technical” class names to stable resource and operation names where possible, without losing meaning.
7. Validate the model.
   Ensure there are no effects without corresponding operations/resources and that each entry operation has effects.
8. Generate a list of questions.
   Ask only about `TBD` items that affect behavioral boundaries (for example, unclear writes/integrations).
9. Save the diagram to `DIAGRAM_PATH`.
10. If `DIAGRAM_VISUAL_PATH` is specified, generate a Mermaid representation according to the rules in `concepts/effects-diagram.md` and save it.

## Code search hints (optional)

Adapt patterns to the technology stack.
Minimum heuristic: search for entry points and input/output boundaries.

* Entry points: `rg -n "<entry point patterns>" CODE_ROOT`
* Database access: `rg -n "<repository/DAO/SQL patterns>" CODE_ROOT`
* External calls: `rg -n "<HTTP client/SDK patterns>" CODE_ROOT`
* Queues/buses: `rg -n "<publish/consume patterns>" CODE_ROOT`

## Common warnings

* If the diagram turns into a “call graph,” stop and raise the abstraction level to operations with external intent.
* If a single operation performs 2+ independent `write`s, explicitly highlight the coupling risk and suggest clarifying transactional boundaries and possible decoupling options.
