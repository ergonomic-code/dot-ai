---
id: sb4-0012
title: logstash-logback-encoder decorator API changes to MapperBuilderDecorator
stage: compile
projects:
- el-repo-i9s-emias-main
error_signatures:
- compile.kotlin.unresolved-reference.MapperBuilderDecorator
- compile.generic.decorate.overrides.nothing
- tooling.generic.Execution.failed.for.task.compileKotlin
- runtime.org.gradle.api.tasks.TaskExecutionException.Execution.failed.for.task.compileKotlin
- runtime.org.gradle.workers.internal.DefaultWorkerExecutor.WorkExecutionException.A.failure.occurred.while.executing.org.jetbrains.kotlin.compilerRunner.GradleCompilerRunnerWithWorkers.GradleKotlinCompilerWorkAction
- runtime.org.jetbrains.kotlin.gradle.tasks.CompilationErrorException.Compilation.error.See.log.for.more.details
affected_components:
- logging
- jackson
confidence: high
---

Context:
This issue was observed in Kotlin code that integrates `logstash-logback-encoder` with Jackson.

Symptom:
```text
e: .../LoggingDateDecorator.kt:... Unresolved reference 'MapperBuilderDecorator'.
e: .../LoggingDateDecorator.kt:... 'decorate' overrides nothing.
```

Diagnosis:
The rollback commit changes `logstash-logback-encoder` from `9.0` back to `8.1` while the code still references `MapperBuilderDecorator` and `JsonMapper.Builder`.
This mismatch makes the decorator interface unavailable and breaks the `decorate` override.

Fix:
Keep `logstash-logback-encoder` on the version that provides `MapperBuilderDecorator`, and update decorator implementations to the new API.
Implement `MapperBuilderDecorator<JsonMapper, JsonMapper.Builder>` and override `decorate(builder)` instead of decorating `JsonFactory`.
