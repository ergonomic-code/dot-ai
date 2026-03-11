# Regression: Tests must not drive permanent production hacks

## Prompt fragment

- RU: "почини тесты".
- RU: "не хачь продовый код ради тестов".
- EN: "fix the tests".
- EN: "do not hack production code for tests".

## Expected behavior

- The agent must not weaken, widen, or distort production code or public contracts only to make tests pass.
- If a failing test exposed a real production boundary mismatch, the final fix must be applied at the production boundary or in test infrastructure.
- A temporary test-only shim may be used only to unblock diagnosis and must be removed before the task is done.

## Framework hook

- `bootstrap/AGENTS.md` (Task triage).
- `INDEX.md` (Task triage).
- `checklists/README.md` (Routing matrix).
- `conventions/ea-principles.md` (EA.T2 — Minimize coupling between tests and implementation).
- `checklists/testing.md` (Coupling, Editing existing tests).
