# Kotlin: Testing Conventions

This document defines technological conventions for Kotlin/JUnit projects that align well with the Ergonomic Approach (EA).

## Assertions

Use `kotest-assertions`.

## Test Structure

Test cases must be divided into blocks and separated with comments:

* `// Given`
* `// When`
* `// Then`

Do not remove these blocks when editing an existing test.
Keep “Act” in `// When` and keep assertions in `// Then`.

## Test Location

Test classes should be located in the same module as the SUT and in a mirrored package.

## Adding Test Cases

When adding new test cases, append them to the end of the file or to the end of the relevant existing test case group, not at the beginning.

## Test Data and System Interaction

Avoid direct interaction with production code inside external scenario test cases.

Conventions:

* Create test data using `*ObjectMother` factories.
* Follow `../jvm/coding-conventions/naming.md` for fixture-factory naming (`*ObjectMother` and similar components).
* Call HTTP entry points only through `*HttpApi`.
* In internal scenario tests, call the SUT directly in the Act step.
* Use `*TestApi` for fixture setup and observation/asserts when reuse warrants a dedicated facade.
* Keep each `*TestApi` scoped to one resource.
* Set up DB state via `*TestApi` and/or `*FixturePresets`, not SQL scripts, except for a minimal ubiquitous standard fixture.
* Describe complex scenario setup as a `*Fixture` and insert it via `*FixturePresets` (using direct production calls or `*TestApi` when reuse warrants it, and stubbing wrappers).

See `../../../concepts/testing-testcode-architecture.md` for the normative test-layering model.
See `ubiquitous-test-fixtures.md` for the minimal baseline fixture pattern (SQL seed + `the*` references).
See `object-mothers-and-fixture-data.md` for conventions on coding `*ObjectMother` factories and fixture data generation.

## Kotlin-first APIs in tests

Prefer Kotlin-generic APIs over Java `Class` tokens.
For example, prefer `.expectBody<T>()` over `.expectBody(T::class.java)` when both are available.

This is a general Kotlin convention and applies to production code as well.
See `../../../conventions/kotlin.md`.

## Naming

Prefer naming that reads as a requirement in test reports.

### Class `@DisplayName`

Annotate test classes with `@DisplayName` using a human-readable name of the SUT or operation.
Prefer the project language over identifiers.

### Test case names

In Kotlin, prefer backtick function names for readable test case names.
Phrase the human-readable name as a requirement (for example, “should ...” or its project-language equivalent).

Rules:

- If using backtick function names, do not add `@DisplayName` on the method.
- Use method-level `@DisplayName` only when the backtick name would be too long, or when required by JUnit features (for example, parameterized tests).

If the codebase uses identifier method names + `@DisplayName`, keep that style.
In that style, `@DisplayName` must contain the human-readable requirement text, not the function identifier.

### Refactors between styles

If the user asks to “replace `@DisplayName` on methods with the method name in backticks”, interpret it as:

- Move the human-readable `@DisplayName` text into the function name in backticks.
- Remove `@DisplayName` from the method.

If the prompt is ambiguous, ask one clarifying question before editing.

## Determinism

Do not use non-deterministic randomness in tests.

If randomized input is required, use [datafaker](https://www.datafaker.net/) and custom wrappers in a way that keeps generation controlled.
