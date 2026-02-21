# Spring Data JDBC repos must avoid manual mapping for simple view reads.

## Prompt fragment

Приведи ReservationsRepo.kt к актуальному гайдлайну

## Expected behavior

- When a `*Repo` exposes a `find*ById` method that returns a `*View` / read model, it must not load the aggregate and map it manually when the view is a direct DB row shape.
- Prefer `JdbcAggregateOperations.findById<ViewType>(id)` for table-mapped read models.
- If a Kotlin view contains value-class-typed properties, prefer a concrete data class read model (with stable bean getter names via `@get:JvmName`) over an interface projection.

## Framework hook

This is a regression case for the "Views and read models" rules in `../ergo/tech/spring/data-jdbc.md`.
