---
name: api-design-cqs
description: "Design and refactor an API to follow Command–Query Separation (CQS): pick a profile, classify operations, split mixed routines, and add enforcement to prevent hidden effects in query paths."
---

# API design: Command–Query Separation (CQS)

See `../../concepts/command-query-separation.md`.

## Input

- `API_SURFACE` — the boundary to apply CQS to (module, service API, controller endpoints, public interfaces).
- Optional: `CQS_PROFILE` — Profile A/B/C from `../../concepts/command-query-separation.md`.
- Optional: `OBSERVABLE_STATE_DEFINITION` — a short written definition of what counts as observable state for this surface.
- Optional: `EXCEPTIONS_POLICY` — which mixed routines are allowed and how exceptions are recorded.

## Output

- `OPERATIONS_INVENTORY` — an operation list classified as Command or Query, with rationale for non-obvious cases.
- `MIXED_OPERATIONS_LIST` — operations that both mutate and return a read projection of state, with the chosen split strategy.
- `ENFORCEMENT_NOTES` — review checklist items and/or automated checks aligned with the chosen profile.

## Algorithm

1. Define `API_SURFACE` precisely.
   List the concrete artifacts (interfaces, classes, endpoints) that form the API surface.
2. Choose `CQS_PROFILE` and record `OBSERVABLE_STATE_DEFINITION`.
   Use Profile A unless you have a concrete reason to require the stricter Profile B, or the result-returning Profile C.
3. Build `OPERATIONS_INVENTORY`.
   For each operation, record: name, signature, classification, and a one-line justification.
4. Audit queries.
   For every Query, verify it has no abstract side effects (and no observable effects at all if using Profile B).
5. Audit commands.
   For every Command, verify it does not act as a read API for existing state.
   Returning generated data (ids, timestamps, server-assigned defaults, revision/version) is allowed.
6. Refactor mixed operations.
   Split into `CommandX()` + `QueryX()` with an explicit call order at call sites, or record an exception with its rationale and containment rules.
7. Add enforcement.
   Ensure the project has at least one enforcement mechanism that prevents regression (review checklist, lint/architecture checks, or tests).
8. Iterate until stable.
   Repeat steps 3–7 until there are no ambiguous operations and no undocumented exceptions.

## Enforcement options (pick at least one)

- Review checklist: add CQS checks using `../../checklists/api-design.md`.
- Architectural checks: forbid writes and domain-significant emissions on query paths (framework- and language-specific).
- Query contract tests: demonstrate that query-only sequences do not change non-secret query results for the chosen observable state definition.

## Common pitfalls

- Confusing CQS with CQRS (operation-level rule vs read/write model architecture).
- Treating transport verbs (e.g., HTTP `GET`) as the source of truth for command/query classification.
- Returning entity snapshots from commands and gradually turning commands into read APIs.
