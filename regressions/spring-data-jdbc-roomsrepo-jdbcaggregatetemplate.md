# RoomsRepo via `jdbcAggregateTemplate` prompt should still produce idiomatic Spring Data JDBC code.

## Prompt fragment

Make `RoomsRepo.kt` a class that works via `jdbcAggregateTemplate`.

## Expected behavior

- Use `JdbcAggregateOperations` in the constructor when possible.
- Expose standard CRUD via `CrudRepository` instead of local `save` wrappers.
- Prefer extending `SimpleJdbcRepository` for CRUD instead of hand-written delegation.
- Ensure bulk persistence uses `saveAll` (batch) rather than `map(save)`.
- Keep custom SQL methods minimal and avoid redundant DB round trips when it is safe to do so.

## Framework hook

This is a regression case for the Spring Data JDBC repository conventions in `../ergo/tech/spring/data-jdbc.md`.
