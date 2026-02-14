# Kotlin: Testing Conventions

This document defines technological conventions for Kotlin/JUnit projects that align well with the Ergonomic Approach (EA).

## Assertions

Use `kotest-assertions`.

## Test Structure

Test cases should be divided into blocks and separated with comments:

* `// Given`
* `// When`
* `// Then`

## Test Data and System Interaction

Avoid direct interaction with production code inside test cases.

Conventions:

* Create test data using `*ObjectMother` factories.
* Perform actions and read results through test APIs (`*TestApi`).

## Naming

Annotate test classes with `@DisplayName` (in Russian) using the name of the SUT.

Test case names should be phrased using “should”, so that `@DisplayName + test name` reads as a requirement.

## Determinism

Do not use non-deterministic randomness in tests.

If randomized input is required, use [datafaker](https://www.datafaker.net/) and custom wrappers in a way that keeps generation controlled.
