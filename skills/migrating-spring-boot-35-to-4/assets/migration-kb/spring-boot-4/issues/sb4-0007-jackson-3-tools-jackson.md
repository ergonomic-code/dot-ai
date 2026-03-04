---
id: sb4-0007
title: Jackson 3 repackaging to tools.jackson breaks imports and custom deserializers
stage: compile
projects:
- qg-repo-main
- el-repo-i9s-emias-main
error_signatures:
- compile.kotlin.unresolved-reference.module
- compile.kotlin.unresolved-reference.KotlinModule
- compile.kotlin.unresolved-reference.jacksonObjectMapper
- compile.kotlin.unresolved-reference.textValue
- compile.generic.No.get.operator.method.providing.array.access
- compile.kotlin.no-applicable-candidates
- tooling.generic.Execution.failed.for.task.app.compileTestKotlin
- runtime.org.gradle.api.tasks.TaskExecutionException.Execution.failed.for.task.app.compileTestKotlin
affected_components:
- jackson
confidence: high
---

Context:
This issue was observed in Kotlin test code and shared libraries that depend on Jackson APIs and Kotlin module helpers.
This issue happened after upgrading to Spring Boot 4, which is compatible with Jackson 3 and its repackaged namespace.

Symptom:
```text
e: ... Unresolved reference 'module'.
e: ... Unresolved reference 'jacksonObjectMapper'.
e: ... Unresolved reference 'textValue'.
```

Diagnosis:
Jackson 3 uses repackaged `tools.jackson.*` types, so code importing `com.fasterxml.jackson.*` Kotlin helpers and Jackson classes can stop compiling.
Custom deserializers can also require API updates, such as switching from `JsonDeserializer` to `ValueDeserializer` and using `parser.readValueAsTree` instead of `parser.codec.readTree`.

Fix:
Update imports and dependencies to the Jackson 3 `tools.jackson.*` namespace where required.
Update custom deserializers to use `ValueDeserializer` and the updated `JsonParser` tree APIs.
When dependency graphs still bring Jackson 2, exclude `com.fasterxml.jackson` artifacts from compile classpaths to avoid mixed compile-time APIs.

Notes:
