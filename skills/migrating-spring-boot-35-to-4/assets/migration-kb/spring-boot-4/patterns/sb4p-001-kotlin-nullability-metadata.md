---
id: sb4p-001
title: "Kotlin compilation breaks due to stricter nullability metadata"
tags:
  - migration
  - spring-boot-4
affected_components:
  - kotlin
  - spring-web
  - spring-data-jdbc
---

What it is:
Spring Boot 4 upgrades libraries such that Kotlin-visible API types become more strictly nullable or non-null, which breaks Kotlin code that relied on platform types.

Typical symptoms:
- `compile.kotlin.argument-type-mismatch.nullability.URI`.
- `compile.kotlin.type-argument-out-of-bounds.Any`.
- `compile.generic.save.overrides.nothing.Potential.signatures.for.overriding`.
- `compile.kotlin.argument-type-mismatch.Nullable.StringNullable-to-String`.
- `compile.generic.addArgumentResolvers.overrides.nothing.Potential.signatures.for.overriding`.

Typical causes:
- Kotlin overrides no longer match updated method signatures because generic nullability and parameter nullability changed.
- Kotlin code that returned or stored nullable values now needs nullable Kotlin types, or needs explicit null checks.

Typical fixes:
- Add non-null bounds like `<T : Any>` where required by the new API surface.
- Make properties and return types nullable when the new API allows null, and update call sites accordingly.
- Update Spring MVC configuration overrides to match the updated parameter element nullability.

Related issues:
- `sb4-0001`.
- `sb4-0006`.
