---
name: migrating-spring-http-tests-to-mockmvc
description: Migrate Spring/JUnit HTTP tests to a MockMvc-backed `WebTestClient` (`MockMvcWebTestClient`) without breaking routing, security, serialization, or test-fixture architecture, while keeping the suite green incrementally.
---

# Migrate Spring HTTP Tests To MockMvc-backed `WebTestClient`

## Goal

Speed up HTTP-heavy Spring test suites by switching `*HttpApi` clients from real HTTP transport to a MockMvc-backed client.
Keep test-case code stable by changing only shared test infrastructure and fixture wiring.
Preserve correctness by explicitly handling routing (`contextPath`), security filters, and JSON codecs.

## Preconditions

External scenario tests call entry points only through `*HttpApi`.
Test cases do not instantiate or configure `WebTestClient` directly.
Shared test infrastructure owns the HTTP client creation and base configuration.
The project uses `WebTestClient` in tests (typically Spring Boot 3).
If the project uses `RestTestClient` (typically Spring Boot 4), this skill does not apply.

If these preconditions do not hold, run `../refactoring-http-tests-to-httpapi/SKILL.md` first.

## Procedure

1. Make the migration incremental.
2. After every small step, run the smallest relevant test subset and keep the branch green.
3. If the suite has both fast and slow tests, keep both green throughout the migration.

### Phase A: Remove legacy HTTP test clients (optional)

If the suite uses multiple HTTP client stacks (for example RestAssured plus `WebTestClient`), remove them one at a time.
Migrate one endpoint or one `*HttpApi` method at a time to reduce regressions.
Delete dependencies and fixtures only after all call sites are migrated.

### Phase B: Switch `WebTestClient` wiring to MockMvc

1. Identify the shared test infrastructure location where `WebTestClient` is created.
2. Replace the real-transport client with `MockMvcWebTestClient` in that shared location.
3. Keep the public surface of shared infra stable so `*HttpApi` code does not change.
4. Ensure routing is preserved by configuring the same base URL and `contextPath` behavior that production transport uses.
5. Ensure security is preserved by applying the same filters and authentication mechanisms as before.
6. Ensure JSON codecs are preserved by wiring the project `ObjectMapper` into `WebTestClient` exchange strategies.

Example wiring sketch (keep it inside shared test infrastructure).

```kotlin
val strategies = ExchangeStrategies.builder()
  .codecs { codecs ->
    codecs.defaultCodecs().jackson2JsonEncoder(Jackson2JsonEncoder(objectMapper))
    codecs.defaultCodecs().jackson2JsonDecoder(Jackson2JsonDecoder(objectMapper))
  }
  .build()

val client = MockMvcWebTestClient.bindTo(mockMvc)
  .baseUrl("http://localhost$contextPath")
  .exchangeStrategies(strategies)
  .build()
```

If `MockMvc` is constructed manually, ensure it applies the same security filter chain as the real transport.
If routing breaks, first suspect `contextPath` and the base URL.

### Phase C: Fix the typical regression classes first

Prioritize fixes in this order because they tend to block most tests at once.

1. Routing regressions.
2. Security regressions (unexpected `401` or missing handler mapping).
3. Serialization regressions (`CodecException`, `InvalidDefinitionException`).
4. Rate-limit and time-based tests, including tests that require a real server.
5. Flaky initialization caused by eager bean construction in tests.

## Done Gate

The suite runs with MockMvc-backed `WebTestClient` without test-case changes beyond migrations already required by Phase A.
Tests pass in a clean rerun.
No architecture or layering rules were weakened to “make it pass”.

## Sentinel smoke set (after infra changes)

After each infra-level change, run a small smoke set that exercises the most failure-prone areas.
Pick 4–6 sentinel tests that cover authentication, routing, serialization, rate limits, and architecture rules.
Prefer tests that are stable, fast, and have clear failure signals.

## Common pitfalls and fixes

If many tests fail with `401` or “no handler”, suspect routing or security filter wiring.
If many tests fail with codec or Jackson errors, suspect mismatched `ObjectMapper` and exchange strategies.
If a subset of tests becomes flaky with connection errors, suspect eager initialization and make clients or fixtures lazy in tests.
If an architecture test reports a new cycle, fix the dependency graph structurally by making the client dependency explicit and avoiding hidden factory coupling.

## References

- Spring testing conventions: `../../ergo/tech/spring/testing.md`.
- Kotlin testing conventions: `../../ergo/tech/kotlin/testing.md`.
- Refactor tests to `*HttpApi`: `../refactoring-http-tests-to-httpapi/SKILL.md`.
- Testing checklist: `../../checklists/testing.md`.
