# Checklist: Operations

Primary reference is `../conventions/ea-principles.md` (EA.F1–EA.F7) and `../ergo/core/coding-conventions/operations.md`.

## Separation and boundaries

- Effects (I/O) and pure computations are separated, with mixing limited to thin orchestrators.
- Each subprogram inside an operation uses one dominant vocabulary and stays within one abstraction level, except explicit translation routines.
- Transport concerns do not leak into operations, and storage concerns stay in resources/adapters.

## Complexity and cohesion

- Cognitive complexity stays within the project budgets, or the deviation is explicitly recorded.
- Each function has one clear semantic responsibility and a single semantic goal.
- Sequential or communicational cohesion is acceptable when it is how one responsibility is completed.
- Shared execution order or shared data alone is not used as the only reason to keep steps together.
- Effects that are not intrinsic to the responsibility being completed are extracted.
- Orchestrators remain thin and primarily connect steps.

## Structure

- The operation has a readable “balanced form” structure: input branching, transformations, and output effects are visible.
- Effects on external resources are explicit.
  Observable effects are asserted in tests.

## Links

- EA principles: `../conventions/ea-principles.md`.
- Subprogram level of abstraction: `../concepts/subprogram-level-of-abstraction.md`.
- Cohesion: `../concepts/cohesion.md`.
- Balanced System Form: `../concepts/balanced-system-form.md`.
- Actions, Calculations, and Data: `../concepts/actions-calculations-data.md`.
- Operations conventions: `../ergo/core/coding-conventions/operations.md`.
- Ports conventions: `../ergo/core/coding-conventions/ports.md`.
