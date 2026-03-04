# Regression: Name Kotlin tests as business requirements

## Prompt fragment

- RU: "добавь тест" / "переименуй тесты" / "имена тестов должны звучать как требования".
- EN: "add a test" / "rename tests" / "test names must read as requirements".

## Expected behavior

- When adding or renaming Kotlin tests, the agent must name test cases as requirements in the project's business/domain language.
- The agent must prefer backtick function names whose text reads well in test reports.
- The agent must avoid implementation vocabulary and internal type names in test names when a domain term exists.
- Before finishing a test-related change, the agent must skim the diff for new or renamed test cases and verify that their names read as requirements.

## Framework hook

- `ergo/tech/kotlin/testing.md` (Naming).
- `checklists/testing.md` (Naming).
