---
id: sb4p-003
title: "Spring Boot autoconfiguration package relocation"
tags:
  - migration
  - spring-boot-4
affected_components:
  - spring-boot-autoconfigure
---

What it is:
Spring Boot 4 moves some autoconfiguration classes out of `org.springframework.boot.autoconfigure.*` into feature-specific packages and modules.

Typical symptoms:
- `compile.kotlin.unresolved-reference.OAuth2ClientProperties`.
- `compile.kotlin.unresolved-reference.security`.

Typical causes:
- Imports reference packages that existed in earlier Spring Boot versions but have moved in Spring Boot 4.

Typical fixes:
- Update imports to the new Spring Boot 4 packages for the same types.
- Ensure the feature starter that provides the moved class is present in the build.

Related issues:
- `sb4-0004`.
