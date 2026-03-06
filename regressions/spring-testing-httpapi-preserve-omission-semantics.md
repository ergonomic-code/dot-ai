# Regression: `*HttpApi` must preserve omitted query parameters as omission

## Prompt fragment

- RU: "при запросе без `languageTag` должна возвращать только `ru` новости".
- RU: "`languageTag` / `platform` / `appVersion` а вот это для МП оставь".

## Expected behavior

- If a scenario depends on a query parameter being omitted, the test client must be able to omit that key entirely.
- The agent must not represent “parameter omitted” by constructing a typed request object that serializes a default value.
- The agent must add a raw or relaxed `*ForResponse` or success overload when omission semantics cannot be expressed via the typed contract.

## Framework hook

- `ergo/tech/spring/testing.md` (`*HttpApi` design).
- `skills/refactoring-http-tests-to-httpapi/SKILL.md` (raw and relaxed transport guidance).
