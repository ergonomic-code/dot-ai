# Regression: Keep `*TestApi` single-resource and avoid fixture aggregators in Spring tests

## Prompt fragment

- "Make `HotelsTestApi.kt` a preset - `*TestApi` cannot write to multiple resources."
- "Where is the declarative graph in the spirit of `NewHotelFixture`?"

## Expected behavior

- If a setup helper writes to multiple resources, the agent must implement it in `*FixturePresets`, not in `*TestApi`.
- The agent must keep each `*TestApi` scoped to a single resource.
- The agent must model complex setup as a declarative `*Fixture` graph and insert it via `*FixturePresets.insertFixture`.
- In Spring tests that rely on lazy initialization, the agent must not introduce an `@Component` that aggregates many fixture beans just to simplify injection.
- The agent must wire fixture components into the Spring test context via a dedicated `*Conf` class (for example, `@ComponentScan`) and inject only the specific beans needed by a test class.

## Framework hook

- `concepts/testing-testcode-architecture.md` (Vocabulary and anti-patterns).
- `skills/refactoring-test-setup-to-fixturepresets-and-testapi/SKILL.md` (Boundaries and checklists).
- `ergo/tech/kotlin/testing.md` (Test data conventions).
- `ergo/tech/spring/testing.md` (Test fixture wiring).
