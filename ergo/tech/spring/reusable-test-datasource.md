# Reusable Test DataSource (Spring)

This document defines a reusable `DataSource` pattern for Spring integration tests.
The goal is to reduce test runtime and friction by reusing a single connection pool and a single database container across multiple Spring test application contexts within one JVM test run.

This pattern is typically used as the DB slice in a slice-composed test infrastructure.
See `testing-infrastructure-slices.md`.

## Problem

Spring integration tests often pay repeated costs for database wiring.
A typical failure mode is “each test context builds its own container wiring and its own pool”.
This increases suite time and creates non-deterministic startup issues.

## Applicability

This pattern applies when a project runs integration tests with a real database via Testcontainers and Spring Boot.
It is most useful when multiple test application contexts exist (for example different `@SpringBootTest(classes = ...)` combinations).

## Invariants

The pattern is considered correctly applied only if all statements below hold.

* The database container is started lazily and at most once per JVM test run.
* The `DataSource` instance is created lazily and at most once per (container, database) pair per JVM test run.
* The Spring application context does not “own” the container lifecycle.
* The Spring application context receives the `DataSource` via a dedicated test configuration (`@TestConfiguration` + `@Bean`).
* The test profile allows overriding the production `DataSource` bean definition (`spring.main.allow-bean-definition-overriding: true`) when a production `DataSource` exists.
* Database state is reset before each test to preserve isolation despite container and pool reuse.
* The pool configuration is optimized for tests and fast startup, not for maximum throughput.

## Database State Reset

This pattern assumes tests do not rely on database state leaking across test cases.
If the same DB container and pool are reused across contexts, any missing reset will eventually cause flakiness due to order dependence and leftover data.

Reset the database state before each test (or at least before each test class) using a project-standard mechanism.

## Reference Implementation (Spring Boot + Kotlin)

Use a JVM-singleton holder for the container and the pool.
In Kotlin, this is typically an `object` with `by lazy`.

```kotlin
import com.zaxxer.hikari.HikariDataSource
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Bean
import org.testcontainers.containers.PostgreSQLContainer
import javax.sql.DataSource

private val container: PostgreSQLContainer<*> by lazy {
  PostgreSQLContainer("postgres:18-alpine").apply { start() }
}

val dataSource: HikariDataSource by lazy {
  HikariDataSource().apply {
    jdbcUrl = container.jdbcUrl
    username = container.username
    password = container.password
    minimumIdle = 0
    maximumPoolSize = 2
    leakDetectionThreshold = 0
  }
}

@TestConfiguration
class DbTestConf {
  @Bean(destroyMethod = "")
  fun dataSource(): DataSource = dataSource
}
```

Disable the bean destroy method (`@Bean(destroyMethod = "")`) so Spring does not accidentally close a shared pool when a test context is shut down.
Return `DataSource` from the `@Bean` method, not `HikariDataSource`, as an extra safeguard against destroy-method inference.

Enable bean overriding for the test profile.
In Spring Boot, this is typically done in `src/test/resources/application-test.yaml`.

```yaml
spring:
  main:
    allow-bean-definition-overriding: true
```

## Migration Notes (from `ApplicationContextInitializer`)

If the test setup uses an `ApplicationContextInitializer` (for example a custom `TestContainerDbContextInitializer`) to build and inject DB properties, migrate as follows.

* Remove the initializer from base test wiring.
* Move container startup into the JVM-singleton holder (`by lazy`).
* Provide a `@TestConfiguration` with a `DataSource` bean as shown above.
* Ensure base integration tests import the config (for example via `@SpringBootTest(classes = [..., DbTestConf::class])`).

## Verification

Pick a sentinel integration test that exercises DB access through the normal application path.
Run that test twice in the same JVM (as part of the suite).
Ensure the second run does not re-bootstrap the container and does not re-create the pool.

## Failure Modes and Remedies

* If the `@Bean` method returns `HikariDataSource`, Spring may close it during context shutdown.
* If bean overriding is not enabled, the test context may fail with a duplicate `DataSource` bean definition error.
* If tests execute in parallel, `maximumPoolSize = 2` may be too small and should be adjusted based on the parallelism budget.
