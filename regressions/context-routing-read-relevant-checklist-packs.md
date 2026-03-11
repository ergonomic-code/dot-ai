# Regression: The framework must route the agent to the relevant checklist packs before implementation or review

## Prompt fragment

- RU: "почини падающий тест".
- RU: "поправь DTO / data class / nullable поле".
- RU: "исправь JSON decoding error" / "`@JsonCreator`" / "nullability".
- RU: "сделай архитектурное ревью".
- EN: "fix a failing test".
- EN: "change a DTO / data class / nullable field".
- EN: "fix a JSON decoding error" / "`@JsonCreator`" / "nullability".
- EN: "review the architecture".

## Expected behavior

- Before non-trivial coding, refactoring, or review, the agent must perform task triage by activity lens and artifact lens.
- When the task exposes a concrete file, symbol, test, or failing command, triage must start from that concrete target instead of from the broad ticket text alone.
- The initial mandatory read set must be the smallest checklist-pack union justified by directly visible evidence from that target and its immediate neighbors.
- The agent must read the union of the mandatory checklist packs selected by those current lenses before proceeding with the main task.
- Additional mandatory packs may be loaded later, but only when local inspection shows that another concern or lens is actually in play.
- For a task that combines failing tests with data-shape or contract-shape work, the read set must include `testing.md` and `data-model.md`, and must also include `api-design.md` when a public transport contract is involved.
- For operation-shaped work, routing must not stop at a generic operations label.
  The framework must route the agent to the common subprogram pack and, when pure logic is extracted, to the calculations pack.
- The framework must not rely on the agent to “remember” where such rules live without routing it there.

## Framework hook

- `bootstrap/AGENTS.md` (Task triage).
- `INDEX.md` (Task triage).
- `checklists/README.md` (How to use checklists, Routing matrix, Example).
- `checklists/subprograms.md` (Common checklist that operation and calculation routing must include).
- `checklists/calculations.md` (Pure-logic-specific constraints used when logic is extracted from operations).
- `checklists/operations.md` (Operation-specific constraints with an explicit dependency on `subprograms.md`).
