---
id: sb4p-002
title: "Jackson 3 migration to tools.jackson and ecosystem compatibility"
tags:
  - migration
  - spring-boot-4
affected_components:
  - jackson
  - testing
---

What it is:
Spring Boot 4 migration commonly includes Jackson 3 adoption, which uses repackaged `tools.jackson.*` APIs and can require upgrades in dependent libraries.

Typical symptoms:
- `compile.kotlin.unresolved-reference.jacksonObjectMapper`.
- `compile.kotlin.unresolved-reference.module`.
- `compile.kotlin.unresolved-reference.KotlinModule`.
- `compile.kotlin.unresolved-reference.JavaTimeModule`.
- `runtime.java.lang.NullPointerException.unknown`.

Typical causes:
- Source code still imports `com.fasterxml.jackson.*` symbols while the build classpath expects `tools.jackson.*` symbols.
- Custom deserializers still use Jackson 2 APIs like `JsonDeserializer` and `parser.codec.readTree`.
- Test libraries or plugins depend on Jackson 2 behavior and break at runtime after switching to Jackson 3.

Typical fixes:
- Update imports to `tools.jackson.*` and update custom deserializers to the observed Jackson 3 APIs.
- Exclude `com.fasterxml.jackson` artifacts from compile classpaths when the dependency graph still pulls in Jackson 2.
- Upgrade test libraries to versions observed to work with the Jackson 3 migration commits.

Related issues:
- `sb4-0007`.
- `sb4-0008`.
- `sb4-0009`.
- `sb4-0012`.
