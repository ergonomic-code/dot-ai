# Checklist: Subprograms

Primary reference is `../conventions/ea-principles.md` (EA.F1–EA.F7).

Apply this checklist to any non-trivial subprogram first.
Specialized checklists for operations and calculations add only domain-specific constraints.

## Semantic clarity

- The subprogram has one clear semantic goal.
- Each part of the subprogram contributes directly to that goal.
- Sequential or communicational cohesion is acceptable only when it is how one responsibility is completed.
- Shared execution order or shared data alone is not used as the only reason to keep steps together.
- Names expose intent rather than incidental mechanism.

## Abstraction and vocabulary

- Each subprogram uses one dominant vocabulary.
- Each subprogram stays within one abstraction level, except explicit translation routines.
- Translation between vocabularies is explicit and local.
- Control flow stays readable without mentally jumping between abstraction layers.

## Form and readability

- The subprogram is readable as a local whole: the reader can follow how inputs are turned into results without excessive mental jumps.
- Prefer the simplest control form that keeps the semantic flow obvious.
- Prefer guard clauses and shallow branching over deeply nested conditionals when they improve readability.
- Prefer standard collection transformations over manual loops when they express intent more directly.
- Avoid manual iteration or branching when they only simulate standard mapping, filtering, grouping, or predicate checks.
- DRY is applied at the level of intent, not by forcing unrelated steps into one abstraction.

## Complexity

- Cognitive complexity stays within the project budgets, or the deviation is explicitly recorded.
- Intermediate values are introduced when they reduce mental stack load.
- Local reasoning is preserved: the reader can understand each step without carrying excessive hidden context.

## Separation of concerns

- Data transformation is separated from effect execution when possible.
- Transport, storage, and framework concerns do not leak into domain-level logic unless the subprogram is explicitly responsible for translation.

## Links

- EA principles: `../conventions/ea-principles.md`.
- Subprogram level of abstraction: `../concepts/subprogram-level-of-abstraction.md`.
- Cohesion: `../concepts/cohesion.md`.
- Balanced System Form: `../concepts/balanced-system-form.md`.
- Actions, Calculations, and Data: `../concepts/actions-calculations-data.md`.
