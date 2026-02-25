---
name: refactoring-http-tests-to-httpapi
description: Refactor Spring/JUnit HTTP tests to typed `*HttpApi` clients (controller-typed signatures, `*ForResponse`, optional `*ForError`/`*ForOutcome`, and JSON schema verification inside the client) when migrating away from direct WebTestClient/RestTestClient usage.
---

# Refactor HTTP Tests To `*HttpApi`

## Goal

Move all HTTP calls out of test cases into `*HttpApi` fixture APIs.
Keep `*HttpApi` method signatures aligned with controller method signatures.
Keep transport-contract checks (status, headers, JSON schema) inside `*HttpApi`.
Keep test cases focused on business assertions and observable behavior.
For non-deterministic test cases (usually due to concurrency) where multiple outcomes are legitimate, return expected errors as values and fail fast on unexpected responses.

## Procedure

1. Identify the HTTP entry point under test and locate the corresponding controller method.
2. Record the controller method parameters and return type as the target contract for the `*HttpApi` public method.
3. Create or update a `*HttpApi` fixture class for this controller or resource.
4. Implement `*ForResponse` that builds the request and returns a response spec for HTTP-level assertions in tests.
5. Implement a typed success method that calls `*ForResponse`, asserts the expected status, verifies the response schema, and decodes the response into the controller return type.
6. If the migrated tests include negative cases, implement `*ForError` when the call is expected to fail, or `*ForOutcome` when the test cannot know whether a given call will succeed or return an expected error.
7. Replace direct client calls in the test case with calls to the typed `*HttpApi` methods.
8. Extract shared HTTP client setup into shared test infrastructure and remove duplication.

## Notes

Do not use `WebTestClient` or `RestTestClient` directly in test cases.
Preserve the existing `// Given`, `// When`, `// Then` block structure in test cases while migrating.
For generic return types, decode using `ParameterizedTypeReference<T>` (or a project helper built on it).
Do not create ad-hoc `*Request` or `*Response` DTOs in tests or fixtures when the controller already defines the transport contract.
If the controller contract is not decodable as-is, fix the contract in production code by introducing an explicit transport DTO.
If the project provides JSON schemas, validate both request and response bodies inside `*HttpApi` before decoding.
If the client validates the same response body against multiple schemas (for example, “success” vs “error”), keep diagnostics for all failed validations.
Do not name a successful method as `*ForError`, and do not implement a successful method by calling `*ForError` internally.
If a `*ForError` method becomes unused after migration, delete it instead of keeping it “just in case”.

In Kotlin, prefer Kotlin-generic APIs over Java `Class` tokens where possible.
For example, prefer `.expectBody<T>()` over `.expectBody(T::class.java)` when both are available.

Prefer simple URI templates over `uri { uriBuilder -> ... }` when the URI is a static path with a small number of query parameters.
This keeps diffs small and makes migrations more incremental.

## Done Gate

All HTTP calls in the migrated area are performed through `*HttpApi`.
No test case uses `WebTestClient` or `RestTestClient` directly.
`*HttpApi` public method signatures match the corresponding controller contracts.
Transport-contract checks live in `*HttpApi`, and test cases assert business rules and observable behavior.
`*ForError` methods are used only for negative cases, and successful methods do not delegate to `*ForError`.

## References

Framework rules and conventions:

- `../../ergo/tech/spring/testing.md`.
- `../../conventions/kotlin.md`.
- `../../concepts/testing-testcode-architecture.md`.
