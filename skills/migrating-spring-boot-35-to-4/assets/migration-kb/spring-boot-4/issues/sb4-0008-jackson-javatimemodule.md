---
id: sb4-0008
title: JavaTimeModule import and registration fails in tests during Jackson 3 migration
stage: compile
projects:
- ergo-arch-hotels
error_signatures:
- compile.kotlin.unresolved-reference.datatype
- compile.kotlin.unresolved-reference.JavaTimeModule
- tooling.generic.Execution.failed.for.task.compileTestKotlin
- runtime.org.gradle.api.tasks.TaskExecutionException.Execution.failed.for.task.compileTestKotlin
affected_components:
- jackson
confidence: high
---

Context:
This issue was observed while compiling Kotlin test sources after moving a project toward Jackson 3.
This issue happened in test JSON infrastructure code that manually registers Jackson modules.

Symptom:
```text
e: .../Json.kt:6:30 Unresolved reference 'datatype'.
e: .../Json.kt:13:16 Unresolved reference 'JavaTimeModule'.
```

Diagnosis:
Test code imported and registered `JavaTimeModule` from the `com.fasterxml.jackson.datatype` namespace, which no longer matched the project dependencies during the Jackson 3 migration.
The fix commit removes manual `JavaTimeModule` registration and migrates Jackson imports to `tools.jackson.*`.

Fix:
Remove the `JavaTimeModule` import and registration from test object mapper setup when it does not match the Jackson version used by the project.
Migrate Jackson imports to the `tools.jackson.*` namespace during Jackson 3 adoption.

Notes:
This issue matches seed `seed-004-javatimemodule-jackson` by signature and by the observed diff that removes `JavaTimeModule` registration.
