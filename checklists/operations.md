# Checklist: Operations

Primary reference is `../conventions/ea-principles.md` (EA.F1–EA.F7), `../concepts/actions-calculations-data.md`, `../ergo/core/coding-conventions/operations.md`, and `subprograms.md`.

Apply `subprograms.md` first.
This checklist contains only operation-specific constraints.

## Separation and boundaries

- Effects (I/O) and pure computations are separated, with mixing limited to thin orchestrators.
- Transport concerns do not leak into operation logic unless the operation is explicitly a transport adapter.
- Storage concerns stay in resources and adapters unless the operation is explicitly a persistence adapter.
- Framework-specific mechanics stay outside business orchestration unless they are the purpose of the operation.

## Operation structure

- If the operation requires more than one branch type among input, transformation, and output, it has a readable balanced-form structure where those branch types remain visible.
- The operation makes external effects explicit.
- Input branching, decision points, and effectful output steps remain visible.
- Orchestrators remain thin and primarily connect steps.
- Effects that are not intrinsic to the responsibility being completed are extracted or delegated.
- Pure decision logic is moved out of the operation when it can be expressed as a calculation.

## CQS at operation level

- The operation is classified as either a command or a query at its own abstraction level.
- A command changes state and may return only acknowledgment and generated data, not a read projection of existing state.
- A query does not change observable state.
- A query may write only secret state whose changes cannot affect the answer of any repeated non-secret query with the same explicit parameters.

## Cohesion

- The operation keeps together only the steps required to complete one effectful responsibility.
- Sequential or communicational cohesion is acceptable when it reflects the natural completion flow of that responsibility.
- Effect grouping is justified by semantic responsibility, not merely by timing or shared data.

## Testability

- Effects on external resources are explicit.
- Observable effects are asserted in tests.
- Pure parts of the operation are testable independently from effect execution.

## Links

- EA principles: `../conventions/ea-principles.md`.
- Actions, Calculations, and Data: `../concepts/actions-calculations-data.md`.
- Command-Query Separation: `../concepts/command-query-separation.md`.
- Cohesion: `../concepts/cohesion.md`.
- Balanced System Form: `../concepts/balanced-system-form.md`.
- Subprograms checklist: `subprograms.md`.
- Calculations checklist: `calculations.md`.
- Operations conventions: `../ergo/core/coding-conventions/operations.md`.
- Ports conventions: `../ergo/core/coding-conventions/ports.md`.
