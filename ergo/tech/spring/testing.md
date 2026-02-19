# Spring: Testing Conventions

This document defines technological conventions for Spring/JUnit projects that align well with the Ergonomic Approach (EA).

## HTTP in Tests

In HTTP test clients (`*HttpApi`), use `RestTestClient` for Spring Boot 4 or `WebTestClient` for Spring Boot 3.

Test cases must not call `WebTestClient` or `RestTestClient` directly.

Test cases call HTTP entry points through `*HttpApi` fixtures APIs.

## `*HttpApi` Design

Public `*HttpApi` methods accept the same Kotlin parameter types as the corresponding controller method parameters.
If the controller returns `ResponseEntity<T>`, the `*HttpApi` method returns `T`.
Expose status, headers, and raw-body assertions via `*ForResponse` / `*ForError` variants when needed.

Use the `*ForResponse` pattern to expose a response spec for HTTP-level assertions in tests.

Use the `*ForError` pattern for negative cases to validate the error contract and return a typed error representation or a response spec.

## JSON Schema Verification

`*HttpApi` methods must validate JSON request and response bodies against JSON schemas when the project provides schemas for the endpoint.

Schema verification happens inside `*HttpApi` before decoding the response body into Kotlin objects.

Tests focus on business rules and observable behavior beyond the transport contract.
