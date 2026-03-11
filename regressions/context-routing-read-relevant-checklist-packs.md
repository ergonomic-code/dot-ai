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
- The agent must read the union of the mandatory checklist packs selected by those lenses before proceeding with the main task.
- For a task that combines failing tests with data-shape or contract-shape work, the read set must include `testing.md` and `data-model.md`, and must also include `api-design.md` when a public transport contract is involved.
- The framework must not rely on the agent to “remember” where such rules live without routing it there.

## Framework hook

- `bootstrap/AGENTS.md` (Task triage).
- `INDEX.md` (Task triage).
- `checklists/README.md` (How to use checklists, Routing matrix, Example).
