---
id: sb4-0004
title: Spring Boot autoconfiguration classes move out of org.springframework.boot.autoconfigure.*
stage: compile
projects:
- qg-repo-main
error_signatures:
- compile.kotlin.unresolved-reference.security
- compile.kotlin.unresolved-reference.OAuth2ClientProperties
- compile.kotlin.unresolved-reference.registration
- compile.kotlin.unresolved-reference.clientId
- compile.kotlin.unresolved-reference.clientSecret
affected_components:
- spring-boot-autoconfigure
- security
confidence: high
---

Context:
This issue was observed in Kotlin code importing Spring Boot autoconfiguration and properties classes.
This issue happened after upgrading to Spring Boot 4, when compiling application Kotlin sources.

Symptom:
```text
e: .../GoogleCalendarsClient.kt:... Unresolved reference 'security'.
e: .../GoogleCalendarsClient.kt:... Unresolved reference 'OAuth2ClientProperties'.
e: .../GoogleCalendarsClient.kt:... Unresolved reference 'registration'.
```

Diagnosis:
Spring Boot 4 relocates some autoconfiguration classes to feature-specific packages and modules.
Code importing `org.springframework.boot.autoconfigure.*` classes can fail to compile because the types are now in new packages.

Fix:
Update imports to the new Spring Boot 4 packages.
Replace `org.springframework.boot.autoconfigure.security.oauth2.client.OAuth2ClientProperties` with `org.springframework.boot.security.oauth2.client.autoconfigure.OAuth2ClientProperties`.

Notes:
