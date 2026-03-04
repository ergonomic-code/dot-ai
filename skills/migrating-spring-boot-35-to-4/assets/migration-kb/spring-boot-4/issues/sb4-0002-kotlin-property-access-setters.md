---
id: sb4-0002
title: Kotlin property access syntax breaks for Java setters ('val' cannot be reassigned)
stage: compile
projects:
- qg-repo-main
- el-repo-i9s-emias-main
error_signatures:
- compile.generic.val.cannot.be.reassigned
- tooling.generic.Execution.failed.for.task.app.compileKotlin
- runtime.org.gradle.api.tasks.TaskExecutionException.Execution.failed.for.task.app.compileKotlin
- tooling.generic.Execution.failed.for.task.compileTestKotlin
- runtime.org.gradle.api.tasks.TaskExecutionException.Execution.failed.for.task.compileTestKotlin
- runtime.org.gradle.workers.internal.DefaultWorkerExecutor.WorkExecutionException.A.failure.occurred.while.executing.org.jetbrains.kotlin.compilerRunner.GradleCompilerRunnerWithWorkers.GradleKotlinCompilerWorkAction
- runtime.org.jetbrains.kotlin.gradle.tasks.CompilationErrorException.Compilation.error.See.log.for.more.details
affected_components:
- spring-security
- kotlin
confidence: high
---

Context:
This issue was observed in Kotlin code that assigns to Java-bean style properties using Kotlin property access syntax.
This issue occurred in Spring Security configuration and test configuration code after upgrading to Spring Boot 4.

Symptom:
```text
e: .../WebSecurityConfig.kt:119:33 'val' cannot be reassigned.
```

Diagnosis:
Kotlin property access syntax (`obj.prop = value`) relies on a visible setter method to exist for `prop`.
After the Spring Boot 4 upgrade the setter was not usable via Kotlin property assignment, so Kotlin treated the member as read-only and rejected reassignment.

Fix:
Replace Kotlin property assignment with an explicit setter call, and suppress the Kotlin inspection if needed.
Use `obj.setProp(value)` instead of `obj.prop = value` when Kotlin reports `'val' cannot be reassigned`.

Notes:
The fix commit explicitly documents that Kotlin property access syntax stopped compiling after moving to Spring Boot 4.
