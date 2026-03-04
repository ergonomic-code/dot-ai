---
id: sb4p-005
title: "Kotlin property access syntax breaks for Java setters"
tags:
  - migration
  - spring-boot-4
affected_components:
  - kotlin
---

What it is:
After Spring Boot 4 upgrades, Kotlin code that assigns to Java-bean properties using `obj.prop = value` can fail to compile with `'val' cannot be reassigned`.

Typical symptoms:
- `compile.generic.val.cannot.be.reassigned`.

Typical causes:
- The setter is no longer visible or usable via Kotlin property access conventions for the referenced Java type.

Typical fixes:
- Replace property assignment with an explicit setter call like `obj.setProp(value)` when the compiler rejects reassignment.

Related issues:
- `sb4-0002`.
