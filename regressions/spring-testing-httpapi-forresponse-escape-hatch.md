# Regression: Avoid one-off `*HttpApi` methods by making `*ForResponse` invertible for negative cases

## Prompt fragment

- RU: "удали `get*ForResponseWithRaw*`" / "нужно передать невалидное значение query параметра" / "нужен raw вызов для негативного кейса".
- EN: "remove `get*ForResponseWithRaw*`" / "need to send an invalid query param value" / "need a raw call for a negative case".

## Expected behavior

- If an external scenario test needs to send an invalid or out-of-contract value (for example an unknown enum constant), the agent must add an escape hatch to the canonical `*ForResponse` (for example `queryParams: Map<String, String?>`) and delegate typed overloads to it.
- The agent must not add a dedicated `*HttpApi` method per invalid field (for example `getNewsForResponseWithRawPlatform`).
- Overloads must delegate to a single canonical implementation rather than duplicating request-building logic.

## Framework hook

- `ergo/tech/spring/testing.md` (`*HttpApi` design rules).
- `skills/refactoring-http-tests-to-httpapi/SKILL.md` (Raw transport escape hatch guidance).
- `conventions/code-hygiene.md` (Overloads delegate to a canonical implementation).
