# Regression: Subprogram level of abstraction must allow explicit translators as a first-class case

## Prompt fragment

- RU: "разреши оба случая" / "переводчик допустим" / "это не только boundary mapper".
- EN: "allow both cases" / "an explicit translator is valid" / "this is not only a boundary mapper".

## Expected behavior

- The concept must allow both a single-vocabulary subprogram and an explicit translation subprogram.
- The concept must describe a valid translator as one source-to-target translation rather than as a violation of the rule.
- EA.F4 must allow explicit translation routines generally, not only at boundaries.
- The operations checklist must apply the vocabulary rule to subprograms inside an operation, not to the operation as a whole.
- Translation routines must expose the translation direction and must not add independent business decisions.
- The concept, principle, and checklists must stay aligned when this risky default is clarified.

## Framework hook

- `concepts/subprogram-level-of-abstraction.md`.
- `conventions/ea-principles.md` (EA.F4 — Keep one abstraction level per function).
- `checklists/operations.md`.
- `checklists/integrations.md`.
