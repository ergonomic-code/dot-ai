---
id: sb4-0001
title: Kotlin compilation fails due to stricter nullability metadata in Spring APIs
stage: compile
projects:
- ergo-arch-hotels
- qg-repo-main
error_signatures:
- compile.kotlin.argument-type-mismatch.nullability.URI
- compile.kotlin.type-argument-out-of-bounds.Any
- compile.kotlin.return-type-mismatch
- compile.generic.Cannot.infer.type.for.this.parameter.Specify.it.explicitly
- compile.kotlin.overload-resolution-ambiguity.candidates
- compile.kotlin.argument-type-mismatch.Map.String.StringNullable-to-MutableMap.uninferred.K.of.fun.K.Any.V.Any.fromSingleValue.uninferred.V.of.fun.K.Any.V.Any.fromSingleValue
- compile.generic.Conflicting.overloads
- compile.generic.save.overrides.nothing.Potential.signatures.for.overriding
- compile.kotlin.argument-type-mismatch.Nullable.StringNullable-to-String
- compile.generic.addArgumentResolvers.overrides.nothing.Potential.signatures.for.overriding
affected_components:
- spring-web
- spring-data-jdbc
- kotlin
confidence: high
---

Context:
This issue was observed after upgrading a codebase to Spring Boot 4 and compiling Kotlin sources.
This issue manifests in Kotlin code that overrides Spring interfaces or models Spring framework types.

Symptom:
```text
e: .../ErrorResponse.kt:34:9 Argument type mismatch: actual type is 'URI?', but 'URI' was expected.
e: .../ResponseEntityExt.kt:14:42 Type argument is not within its bounds: must be subtype of 'Any'.
e: .../ResponseEntityExt.kt:15:5 Return type mismatch: expected 'ResponseEntity<T>', actual 'ResponseEntity<T & Any>'.
```

Diagnosis:
Spring Boot 4 upgrades Spring libraries that carry stricter nullability information, which changes Kotlin-visible API types.
Kotlin code that previously compiled with platform types starts failing because generics become non-null by default and nullable members become explicit in the type system.

Fix:
Make Kotlin nullability explicit at the call sites and in overrides, and align generic bounds with the updated APIs.
Replace unconstrained generics like `<T>` with non-null constrained generics like `<T : Any>` where the API now requires non-null.
Change fields and accessors that now receive nullable values to use nullable Kotlin types, and update tests and schemas accordingly.

Notes:
This issue matches seed `seed-002-problemdetails-type` and seed `seed-003-jspecify-kotlin-nullability` by signature and by the observed fixes in diffs.
