# Regression: In Kotlin tests, move method `@DisplayName` text into backtick function names

## Prompt fragment

- RU: "заменить `@DisplayName` на методах на имя метода в backticks. `@DisplayName` допустимо использовать для слишком длинных имён."
- EN: "replace method-level `@DisplayName` with backtick function names. `@DisplayName` is allowed for names that are too long."
- RU: "нет, тебе надо было не имена методов в `@DisplayName` перенести, а перенести `@DisplayName` в имя метода и удалить `@DisplayName`: пример: `reservationPersistenceTest` -> ``fun `должна возвращать ...`() { ... }``."
- EN: "move the human-readable `@DisplayName` text into the backtick function name, then remove `@DisplayName`."

## Expected behavior

- If asked to replace method-level `@DisplayName` with backtick function names, the agent must move the human-readable `@DisplayName` text into the function name and remove `@DisplayName`.
- The agent must not set `@DisplayName` to the function identifier (for example, `reservationPersistenceTest`).
- The agent must preserve the repository’s established naming style (backticks vs identifiers + `@DisplayName`) unless the prompt explicitly requests a migration.

## Framework hook

- `ergo/tech/kotlin/testing.md` (Naming, refactors between styles).
