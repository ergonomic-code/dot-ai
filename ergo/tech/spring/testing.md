# Kotlin: Testing Conventions

This document defines technological conventions for Spring/JUnit projects that align well with the Ergonomic Approach (EA).

## HTTP in Tests

In HTTP test clients (`*HttpApi`), use `RestTestClient` for Spring Boot 4 or `WebTestClient` for Spring Boot 3.
