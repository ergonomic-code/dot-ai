# Checklist: Operations

Primary reference is `../conventions/ea-principles.md` (EA.F1–EA.F7) and `../ergo/core/coding-conventions/operations.md`.

## Separation and boundaries

- Effects (I/O) and pure computations are separated, with mixing limited to thin orchestrators.
- Each operation stays within one abstraction level except at explicit mapping boundaries.
- Transport concerns do not leak into operations, and storage concerns stay in resources/adapters.

## Complexity and cohesion

- Cognitive complexity stays within the project budgets, or the deviation is explicitly recorded.
- Each function has high cohesion and a single semantic goal.
- Orchestrators remain thin and primarily connect steps.

## Structure

- The operation has a readable “balanced form” structure: input branching, transformations, and output effects are visible.
- Effects on external resources are explicit.
  Observable effects are asserted in tests.

## Links

- EA principles: `../conventions/ea-principles.md`.
- Balanced System Form: `../concepts/balanced-system-form.md`.
- Actions, Calculations, and Data: `../concepts/actions-calculations-data.md`.
- Operations conventions: `../ergo/core/coding-conventions/operations.md`.
- Ports conventions: `../ergo/core/coding-conventions/ports.md`.
