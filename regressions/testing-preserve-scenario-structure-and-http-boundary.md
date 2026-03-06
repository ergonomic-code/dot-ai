# Regression: Preserve existing scenario-test structure and keep HTTP coverage on the HTTP boundary

## Prompt fragment

- RU: "добавь тест".
- RU: "проверь контроллер".
- RU: "кейсы всегда должны быть разбиты на блоки `Given`/`When`/`Then`".

## Expected behavior

- When editing existing scenario tests, the agent must preserve the touched file's established structure and naming style, including `// Given`, `// When`, `// Then` blocks and business-language names, unless the prompt explicitly requests a style migration.
- When editing an existing test without explicit migration scope, preserving the current test boundary takes priority over opportunistic boundary modernization.
- The agent must not delete or replace an existing scenario test merely to satisfy coverage or make the suite green without proving redundancy or explicit approval.
- If the test is meant to verify controller behavior, routing, binding, validation, security, or default request semantics, it must execute through the HTTP or MVC boundary via `*HttpApi` or an MVC slice, not via a direct controller call.

## Framework hook

- `agents/roles.md` (Role: developer, test-editing rules).
- `checklists/testing.md` (Editing existing tests and test architecture).
- `ergo/tech/spring/testing.md` (controller-boundary coverage).
