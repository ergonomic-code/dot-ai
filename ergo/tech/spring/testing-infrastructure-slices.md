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

### Runtime slice (`@RuntimeTest`)

Use a meta-annotation to centralize suite-wide runtime behavior.
This slice is responsible for the test profile and per-test JUnit integration.

```kotlin
package com.example.testinfra.annotations

import org.junit.jupiter.api.extension.BeforeEachCallback
import org.junit.jupiter.api.extension.ExtendWith
import org.junit.jupiter.api.extension.ExtensionContext
import org.springframework.test.context.ActiveProfiles

object ResetRandomExtension : BeforeEachCallback {
  override fun beforeEach(context: ExtensionContext) {
    // Reset stable random seed and generators.
  }
}

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@MustBeDocumented
@ActiveProfiles("test")
@ExtendWith(ResetRandomExtension::class)
annotation class RuntimeTest
```

### Resource slice (`@DbTest`)

Model the database as a single opt-in slice.
This slice can import Spring configuration and also apply per-test DB reset rules.
By default, `@Sql` runs before each test method.

```kotlin
package com.example.testinfra.annotations

import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Import
import org.springframework.test.context.jdbc.Sql

@TestConfiguration
class DbTestConfig

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@MustBeDocumented
@RuntimeTest
@Sql("classpath:db/reset-data.sql")
@Import(DbTestConfig::class)
annotation class DbTest
```

### Integration adapter slice (HTTP)

Model SUT interaction as an adapter slice.
This slice should provide a stable, test-friendly API that hides transport details like Spring MVC, JSON serialization, and ports.
Prefer exposing a factory of domain-level HTTP clients instead of exposing transport clients directly.

```kotlin
package com.example.testinfra.annotations

import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Import

@TestConfiguration
class HttpClientTestConfig

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@MustBeDocumented
@Import(HttpClientTestConfig::class)
annotation class HttpTest
```

To keep test code expressive, encapsulate HTTP transport into a factory bean and expose role-based clients.
This prevents transport-level APIs (like `RestTestClient`) from leaking into test cases.
`RestTestClient` is available in Spring Boot 4+.

```kotlin
package com.example.fixtures.clients

import org.springframework.test.web.servlet.client.RestTestClient
import tools.jackson.databind.json.JsonMapper

class HttpClientFactory(
    client: RestTestClient,
    jsonMapper: JsonMapper
) {
    val aGuest = Guest(client, jsonMapper)
}
```

### Composed bundle (`@ApiTest`)

When many tests share the same slice set, bundle it into a higher-level annotation.
Bundles should remain a thin composition layer and not introduce new behavior.

```kotlin
package com.example.testinfra.annotations

import org.springframework.boot.SpringBootConfiguration
import org.springframework.boot.test.context.SpringBootTest

@SpringBootConfiguration
class App

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@MustBeDocumented
@RuntimeTest
@DbTest
@HttpTest
@SpringBootTest(
  classes = [App::class],
  webEnvironment = SpringBootTest.WebEnvironment.MOCK
)
annotation class ApiTest
```

### Narrower bundle (`@JdbcSliceTest`)

When the SUT interaction does not require HTTP, compose a narrower bundle.

```kotlin
package com.example.testinfra.annotations

import org.springframework.boot.data.jdbc.test.autoconfigure.DataJdbcTest
import org.springframework.boot.jdbc.test.autoconfigure.AutoConfigureTestDatabase
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Import

@TestConfiguration
class JdbcConfig

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
@MustBeDocumented
@DbTest
@DataJdbcTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Import(JdbcConfig::class)
annotation class JdbcSliceTest
```

### Composed test

Tests pick the smallest bundle that provides what they need.
Avoid abstract base test classes.
If you need shared client fixtures, expose them as beans and inject them.

## Verification

Pick two tests with different infrastructure needs.
Ensure they can be expressed without a shared base class.
Add a new infrastructure capability and verify existing slices do not require changes, aside from composed tests or bundles.

## Failure Modes and Remedies

* If a slice grows multiple responsibilities, split it along the responsibility boundary.
* If slices become coupled by hard dependencies, invert the dependency into the composed test.
* If composition is hidden behind a new base class, remove the base class and restore explicit slice selection.
* If a slice pulls a full application bootstrap incidentally, tighten the slice scope to only the required capability.
