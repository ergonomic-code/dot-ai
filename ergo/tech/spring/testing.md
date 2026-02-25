# Spring: Testing Conventions

This document defines technological conventions for Spring/JUnit projects that align well with the Ergonomic Approach (EA).

## HTTP in Tests

In HTTP test clients (`*HttpApi`), use `RestTestClient` for Spring Boot 4 or `WebTestClient` for Spring Boot 3.
Test cases must not call `WebTestClient` or `RestTestClient` directly.
Test cases call HTTP entry points through `*HttpApi` fixtures APIs.
For a step-by-step procedure, see `../../../skills/refactoring-http-tests-to-httpapi/SKILL.md`.

When the project uses `MockMvcWebTestClient` (MockMvc-backed `WebTestClient`) to speed up tests, treat it as a `WebTestClient` implementation detail inside shared test infrastructure.
Do not leak `MockMvc` or `MockMvcWebTestClient` knowledge into test cases.
For a step-by-step procedure, see `../../../skills/migrating-spring-http-tests-to-mockmvc/SKILL.md`.

## Test Fixture Wiring

Wire fixture components (`*TestApi`, `*FixturePresets`) into the Spring test context via a dedicated `*Conf` class in test sources.
Prefer `@ComponentScan` (or `@Import`) on the config class, and include it in `@SpringBootTest(classes = [...])` (or import it from a base test).
In Spring Boot tests, prefer `@TestConfiguration` for such configs.
With `@ComponentScan` without explicit packages, scanning defaults to the package of the config class.

Avoid introducing an `@Component` that aggregates multiple fixture beans only to make injection “convenient”.
Such an aggregator defeats `spring.main.lazy-initialization` and pulls unrelated fixture code into tests that do not need it.

Example.

```kotlin
@TestConfiguration
@ComponentScan
class TestFixturesConf

@SpringBootTest(classes = [App::class, TestFixturesConf::class])
abstract class BaseIntegrationTest
```

Inject the specific fixture beans you need (for example `OrdersFixturePresets` and `UsersTestApi`) directly into each test class.

## `*HttpApi` Design

Public `*HttpApi` methods accept and return the same Kotlin types as the corresponding controller method parameters and return type.
Do not introduce intermediate `*Request` or `*Response` DTOs in tests or fixtures when the controller already defines the transport contract.
Use the `*ForResponse` pattern to expose a response spec for HTTP-level assertions in tests.
Use the `*ForError` pattern for negative cases to validate the error contract and return a typed error representation or a response spec.
For non-deterministic test cases (usually due to concurrency) where a given HTTP call may legitimately succeed or return an expected error, prefer the `*ForOutcome` pattern.
`*ForOutcome` returns a typed value outcome (for example `HttpOutcome<SuccessBody, ErrorBody>`).
Expected errors are returned as values, while unexpected responses throw exceptions (fail-fast).
Keep the set of expected errors centralized and reusable (for example `only(HttpStatus.CONFLICT with <errorCode>)`).
For generic Kotlin types, decode using `ParameterizedTypeReference<T>` (or a project helper built on it).

## `WebTestClient` request conventions (inside `*HttpApi`)

Prefer a dedicated request builder DSL for cross-cutting concerns such as authentication headers.
If many call sites build `Authorization: Bearer ...`, extract a helper like `authorized(token)` in shared test code and use it consistently.

Prefer simple URI templates over `uri { uriBuilder -> ... }` when the URI is a static path with a small number of query parameters.
This keeps diffs small and reduces incidental complexity in migrations.

Do not use `ThreadLocal` to pick routing, base URLs, or per-test client configuration.
Make the client and its base configuration explicit (constructor parameters or per-test wiring in shared infra).

If the project uses a custom Jackson `ObjectMapper`, ensure the `WebTestClient` codecs use it.
If the codecs are not aligned, migrations often fail with `CodecException` or `InvalidDefinitionException` and hide real behavior changes.

## Low-level technical details in test cases

Do not inline low-level technical boilerplate in test cases.
This includes concurrency primitives (latches, futures, executors) and ad-hoc request/response plumbing.
Extract such details into test platform code and fixture APIs (`*HttpApi`, `*TestApi`, `*FixturePresets`).
For concurrent execution, use a shared helper (for example `executeSimultaneously(requestsCount) { ... }`).
Keep the test case as a thin script that contains only scenario logic and assertions over typed outcomes.

## JSON Schema Verification

`*HttpApi` methods must validate JSON request and response bodies against JSON schemas when the project provides schemas for the endpoint.
Schema verification happens inside `*HttpApi` before decoding the response body into Kotlin objects.
Tests focus on business rules and observable behavior beyond the transport contract.
If schema verification fails, preserve the original validation exception in the thrown failure (as `cause` or `suppressed`).
If a client validates the same body against multiple schemas (for example, “success” vs “error”), keep diagnostics for all failed validations.
