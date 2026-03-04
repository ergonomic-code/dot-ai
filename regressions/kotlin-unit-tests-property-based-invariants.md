# Regression: Prefer property-based unit tests for invariants when available

## Prompt fragment

- RU: "покрой инварианты юнит тестами" / "проверь, что для любых входов выполняется условие".
- EN: "add unit tests for invariants" / "for any input, it must hold that ...".

## Expected behavior

- If the project already has property-testing tooling, the agent should prefer property-based unit tests for pure invariants.
- The agent must keep generation bounded and reproducible to avoid flakiness.
- The agent must not add new property-testing dependencies unless the user explicitly asks.
- If property-testing tooling is not available, the agent should write example-based unit tests that focus on the invariant boundaries.

## Framework hook

- `ergo/tech/kotlin/testing.md` (Property-based tests).
- `checklists/testing.md` (Coverage).
