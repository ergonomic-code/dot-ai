# Spring Data JDBC: Repository Conventions

## Intention

This document defines conventions for implementing `*Repo` classes on top of Spring Data JDBC.
The goal is to keep repositories idiomatic, efficient, and easy to refactor.

## Defaults

### Rule: Depend on `JdbcAggregateOperations`, not `JdbcAggregateTemplate`

This is an application of the global rule "Prefer abstractions in dependencies" from `../../../conventions/code-hygiene.md`.
Prefer constructor-injecting `JdbcAggregateOperations` instead of `JdbcAggregateTemplate`.
Use a concrete class only when you need an API that is not available via the interface.

### Rule: A `JdbcAggregateOperations`-based `*Repo` implements `CrudRepository`

If a repository wraps `JdbcAggregateOperations` for one aggregate, implement `CrudRepository<T, ID>` by default.
Do not re-declare `save` and `saveAll` as ad-hoc methods on the repository unless you have a strong reason.

In Kotlin, prefer extending `SimpleJdbcRepository<T, ID>` for the aggregate type.
Extract the persistent entity lookup into a shared helper (for example `platform.spring.data.getRequiredPersistentEntity`) to keep repository classes small.

## Batching

### Rule: Persist collections in batch mode

When persisting multiple aggregates, use batch APIs (`saveAll`, `insertAll`, `updateAll`, or their equivalents) when they exist.
Do not implement batch persistence by looping a single-aggregate operation (`items.map(::save)`).

## Custom SQL

Use `JdbcClient` for custom SQL that is not naturally expressed via aggregate operations.
Prefer a single SQL round trip when the logic is naturally expressible in one statement.

## Views and read models

### Rule: Prefer mapped read models over manual mapping

If a method returns a `*View` / read model that matches a DB row shape, do not load the aggregate and map it by hand.
Prefer one of:

- `JdbcAggregateOperations.findById<YourView>(id)` for a table-mapped read model type.
- `JdbcClient` with an explicit query when you need joins or a non-trivial shape.

This is an application of "No isomorphic DTOs" from `../../../conventions/contracts.md`.


## Recommended template

### `getRequiredPersistentEntity` helper

Extract the persistent entity lookup into a shared helper (for example `platform.spring.data.getRequiredPersistentEntity`).
Keep this helper as the only place that touches `PersistentEntity` casting.
Recommended location is `platform/spring/data/CrudRepositoryExt.kt` (or an equivalent shared module).

```kotlin
package your.app.platform.spring.data

import org.springframework.data.jdbc.core.JdbcAggregateOperations
import org.springframework.data.mapping.PersistentEntity

@Suppress("UNCHECKED_CAST")
inline fun <reified T : Any> JdbcAggregateOperations.getRequiredPersistentEntity(): PersistentEntity<T, *> =
    this.converter.mappingContext.getRequiredPersistentEntity(T::class.java) as PersistentEntity<T, *>
```

### Repository base class

Extend `SimpleJdbcRepository` and use the shared helper.
Keep `JdbcAggregateOperations` as a non-property parameter if it is only needed for the base repository wiring.
Store it as a `private val` if you also need it for read model operations (for example `findById<YourView>(...)`).
Replace `Entity` and `UUID` with your aggregate type and id type.

```kotlin
import org.springframework.data.jdbc.core.JdbcAggregateOperations
import org.springframework.data.jdbc.repository.support.SimpleJdbcRepository
import org.springframework.jdbc.core.simple.JdbcClient
import org.springframework.stereotype.Repository
import java.util.UUID

import your.app.platform.spring.data.getRequiredPersistentEntity

@Repository
class EntitiesRepo(
    private val jdbcClient: JdbcClient,
    jdbcAggregateOperations: JdbcAggregateOperations,
) : SimpleJdbcRepository<Entity, UUID>(
    jdbcAggregateOperations,
    jdbcAggregateOperations.getRequiredPersistentEntity<Entity>(),
    jdbcAggregateOperations.converter,
) {

    // Custom SQL methods go here.

}
```
