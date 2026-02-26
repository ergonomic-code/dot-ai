# Testing Infrastructure Slices (Experimental)

This document defines a compositional pattern for integration test infrastructure.
The goal is to avoid inheritance-based base test classes and instead assemble per-test infrastructure from small, reusable slices.
This pattern is experimental.

## Problem

Inheritance-based test infrastructure tends to accumulate responsibilities.
Each new test kind forces refactoring an inheritance tree and coupling unrelated concerns.
This makes it hard to compose infrastructure capabilities (for example DB only, HTTP only, or DB + HTTP) per test.

## Applicability

This pattern applies when integration tests need different infrastructure combinations across the suite.
It is especially useful when you expect new infrastructure capabilities to appear over time.
Examples include adding a database container, a web layer client, or a messaging broker.

## Invariants

The pattern is considered correctly applied only if all statements below hold.

* Tests do not rely on inheritance to obtain infrastructure.
* Each slice has one primary responsibility.
* Each slice is opt-in and can be composed with other slices.
* A test explicitly declares which slices it uses.
* Adding a new infrastructure capability does not require modifying existing slices.
* Adding a new infrastructure capability may require updating composed tests or slice bundles.

## Slice Vocabulary

The terms below are normative for this pattern.

* **Test infrastructure slice** is a small, reusable unit that contributes a single kind of test environment capability.
* **Slice** is a synonym of test infrastructure slice.
* **Slice composition** is the act of assembling a test’s environment by combining multiple slices.
* **Composed test** is a test class whose environment is defined only by slice composition, not by inheritance.
* **Base test class** is a superclass used to provide shared test environment setup.

## Slice Kinds

A slice must belong to exactly one of the kinds below.

* **Runtime slice** configures environment-wide and per-test runtime behavior.
* **Resource slice** configures a specific external resource (for example a database).
* **Integration adapter slice** configures a mechanism to interact with the SUT (for example HTTP or messaging).
* **Test framework slice** configures test framework integration (for example Spring test context or JUnit extensions).

## Construction Rule

To create or refactor test infrastructure into slices:

1. List all distinct infrastructure concerns currently provided by a base test class.
2. Partition them into slice candidates with one primary responsibility each.
3. Implement each slice as a composable unit.
4. Update tests to declare their slices explicitly.
5. Ensure no slice depends on concrete tests.

## Reference Implementation (Spring Boot + Kotlin)

This section sketches a minimal implementation approach for Spring Boot and JUnit 5.
The exact split between annotations, configs, and extensions depends on your suite.

### Runtime slice (JUnit extension + profile)

Use a JUnit extension for per-test runtime setup.

```kotlin
import org.junit.jupiter.api.extension.BeforeEachCallback
import org.junit.jupiter.api.extension.ExtensionContext

object ResetRandomExtension : BeforeEachCallback {
  override fun beforeEach(context: ExtensionContext) {
    // Reset stable random seed and generators.
  }
}
```

Attach it via a meta-annotation.
TBD: document a stable-random-based test data generation pattern that stays reproducible and debuggable across the suite.

```kotlin
import org.junit.jupiter.api.extension.ExtendWith
import org.springframework.test.context.ActiveProfiles

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@ActiveProfiles("test")
@ExtendWith(ResetRandomExtension::class)
annotation class RuntimeSlice
```

### Resource slice (DB config)

Provide DB wiring through a dedicated `@TestConfiguration`.
Prefer a reusable singleton `DataSource` holder when suites have multiple test contexts.
Use the `DbTestConf` pattern described in `reusable-test-datasource.md`.

Use `DbTestConf` as the implementation of the DB slice.

```kotlin
import org.springframework.context.annotation.Import

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@Import(DbTestConf::class)
annotation class DbSlice
```

### Integration adapter slice (HTTP)

Provide HTTP client wiring as a separate slice.
Keep `RestTestClient` or `WebTestClient` knowledge out of test cases.

```kotlin
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Bean

class HotelsHttpApi

@TestConfiguration
class HttpSliceConf {
  @Bean
  fun hotelsHttpApi(): HotelsHttpApi = HotelsHttpApi()
}
```

```kotlin
import org.springframework.context.annotation.Import

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@Import(HttpSliceConf::class)
annotation class HttpSlice
```

### Composed slice bundle (`@ApiTest`)

When many tests share the same slice set, bundle it into a higher-level meta-annotation.

```kotlin
import org.springframework.boot.test.context.SpringBootTest

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@RuntimeSlice
@DbSlice
@HttpSlice
@SpringBootTest(classes = [HotelsApp::class])
annotation class ApiTest
```

### Composed test

A composed test opts into only the slices it needs.

```kotlin
@ApiTest
class ReserveRoomApiOpTest {
  // Inject only slice-provided fixtures needed by the test.
}
```

## Verification

Pick two tests with different infrastructure needs.
Ensure they can be expressed without a shared base class.
Add a new infrastructure capability and verify existing slices do not require changes, aside from composed tests or bundles.

## Failure Modes and Remedies

* If a slice grows multiple responsibilities, split it along the responsibility boundary.
* If slices become coupled by hard dependencies, invert the dependency into the composed test.
* If composition is hidden behind a new base class, remove the base class and restore explicit slice selection.
* If a slice pulls a full application bootstrap incidentally, tighten the slice scope to only the required capability.
