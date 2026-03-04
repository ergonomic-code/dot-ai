---
id: sb4-0006
title: Spring Data JDBC Kotlin helpers break due to RowMapper and Converter signature
  changes
stage: compile
projects:
- qg-repo-main
error_signatures:
- compile.kotlin.argument-type-mismatch.Class.T.1.of.fun.T.taDataClassRowMapper-to-Class.uninferred.T.of.fun.T.Any.newInstance
- compile.generic.Not.enough.information.to.infer.type.argument.for.T
- compile.kotlin.unresolved-reference.conversionService
- compile.kotlin.argument-type-mismatch.List.R.of.fun.T.R.Page.T.mapContent-to-MutableList.uninferred.T.of.class.PageImpl.T.Any
- compile.kotlin.override-return-type-not-subtype.convert
affected_components:
- spring-jdbc
- spring-data-jdbc
confidence: high
---

Context:
This issue was observed in a Kotlin codebase that defines helper functions around Spring JDBC and Spring Data JDBC.
This issue happened after upgrading to Spring Boot 4 and compiling the main application sources.

Symptom:
```text
e: .../RowMapperExt.kt:... Argument type mismatch: actual type is 'Class<T>', but 'Class<... : Any>' was expected.
e: .../RowMapperExt.kt:... Unresolved reference 'conversionService'.
e: .../ObjectToJsonbConverters.kt:... Return type of 'convert' is not a subtype of the overridden member.
```

Diagnosis:
Spring JDBC and Spring Data converter APIs changed in a way that impacts Kotlin helper code that relies on older method signatures and nullability assumptions.
The fix commit changes Kotlin helper signatures, uses updated `DataClassRowMapper.newInstance` construction, and adjusts converter nullability.

Fix:
Update Kotlin helper functions to match the updated Spring signatures and nullability expectations.
Pass a `ConversionService` via the supported `DataClassRowMapper.newInstance` overload instead of assigning to `conversionService`.
Adjust `Converter` implementations to return nullable values when the overridden signature expects nullable.
Update page mapping helpers to accept `List<T>` and use `T : Any` bounds when required by the target API.
