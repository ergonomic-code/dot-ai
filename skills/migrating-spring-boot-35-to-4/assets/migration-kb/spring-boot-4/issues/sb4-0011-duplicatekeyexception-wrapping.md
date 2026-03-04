---
id: sb4-0011
title: DuplicateKeyException handling changes in Spring Data JDBC
stage: test
projects:
- el-repo-config-main
- qg-repo-main
error_signatures:
- tooling.generic.Execution.failed.for.task.test
- runtime.org.gradle.api.tasks.TaskExecutionException.Execution.failed.for.task.test
- runtime.org.gradle.api.internal.exceptions.MarkedVerificationException.There.were.failing.tests.See.the.report.at
affected_components:
- spring-data-jdbc
confidence: medium
---

Context:
This issue was observed while running tests after upgrading Spring Boot to 4 and using Spring Data JDBC.
This issue involves application code that previously unwrapped `DbActionExecutionException` to reach `DuplicateKeyException`.

Symptom:
```text
Execution failed for task ':test'.
> There were failing tests.
```

Diagnosis:
The fix commit that made tests pass in `el-repo-config-main` changes exception handling from `DbActionExecutionException` unwrapping to catching `DuplicateKeyException` directly.
A similar change is present in `qg-repo-main`, where custom exception translation and unwrapping logic is removed.

Fix:
Catch `DuplicateKeyException` directly at the boundary where persistence exceptions are mapped to domain errors.
Remove custom translators that assume `DbActionExecutionException` always wraps a `DataAccessException`.
