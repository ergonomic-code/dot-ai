---
id: sb4p-004
title: "DuplicateKeyException propagation changes in Spring Data JDBC"
tags:
  - migration
  - spring-boot-4
affected_components:
  - spring-data-jdbc
---

What it is:
Spring Data JDBC persistence exceptions can change shape during Spring Boot 4 migration, which breaks code that unwraps `DbActionExecutionException` to find `DuplicateKeyException`.

Typical symptoms:
- `tooling.generic.Execution.failed.for.task.test`.
- `runtime.org.gradle.api.tasks.TaskExecutionException.Execution.failed.for.task.test`.

Typical causes:
- Exception mapping code assumes `DbActionExecutionException` wraps a `DataAccessException`, but the thrown exception is already a `DuplicateKeyException`.

Typical fixes:
- Catch `DuplicateKeyException` directly in DAO or repository boundaries where domain exceptions are created.
- Remove custom exception translators that only exist to unwrap `DbActionExecutionException`.

Related issues:
- `sb4-0011`.
