# Kotlin: Testing Conventions

This document defines technological conventions for Kotlin/JUnit projects that align well with the Ergonomic Approach (EA).

## Assertions

Use `kotest-assertions`.

## Test Structure

Test cases should be divided into blocks and separated with comments:

* `// Given`
* `// When`
* `// Then`

## Test Location

Test classes should be located in the same module as the SUT and in a mirrored package.

## Adding Test Cases

When adding new test cases, append them to the end of the file or to the end of the relevant existing test case group, not at the beginning.

## Test Data and System Interaction

Avoid direct interaction with production code inside external scenario test cases.

Conventions:

* Create test data using `*ObjectMother` factories.
* Call HTTP entry points only through `*HttpApi`.
* In internal scenario tests, call the SUT directly in the Act step.
* Use `*TestApi` for fixture setup and observation/asserts when reuse warrants a dedicated facade.
* Set up DB state via `*TestApi` and/or `*FixturePresets`, not SQL scripts, except for a minimal ubiquitous standard fixture.
* Describe complex scenario setup as a `*Fixture` and insert it via `*FixturePresets` (using direct production calls or `*TestApi` when reuse warrants it, and stubbing wrappers).

See `../../../concepts/testing-testcode-architecture.md` for the normative test-layering model.

## Naming

Annotate test classes with `@DisplayName` (in Russian) using the name of the SUT.

Test case names should be phrased using “should”, so that `@DisplayName + test name` reads as a requirement.

## Determinism

Do not use non-deterministic randomness in tests.

If randomized input is required, use [datafaker](https://www.datafaker.net/) and custom wrappers in a way that keeps generation controlled.
