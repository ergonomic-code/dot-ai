# Spring: Testing Conventions

This document defines technological conventions for Spring/JUnit projects that align well with the Ergonomic Approach (EA).

## HTTP in Tests

In HTTP test clients (`*HttpApi`), use `RestTestClient` for Spring Boot 4 or `WebTestClient` for Spring Boot 3.
Test cases must not call `WebTestClient` or `RestTestClient` directly.
Test cases call HTTP entry points through `*HttpApi` fixtures APIs.
For a step-by-step procedure, see `../../../skills/refactoring-http-tests-to-httpapi/SKILL.md`.

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
For generic Kotlin types, decode using `ParameterizedTypeReference<T>` (or a project helper built on it).

## JSON Schema Verification

`*HttpApi` methods must validate JSON request and response bodies against JSON schemas when the project provides schemas for the endpoint.
Schema verification happens inside `*HttpApi` before decoding the response body into Kotlin objects.
Tests focus on business rules and observable behavior beyond the transport contract.
