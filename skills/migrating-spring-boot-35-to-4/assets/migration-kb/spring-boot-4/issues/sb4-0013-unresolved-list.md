---
id: sb4-0013
title: Unresolved reference 'list' in DAOs after Spring Boot 4 upgrade
stage: compile
projects:
- qg-repo-main
error_signatures:
- compile.kotlin.unresolved-reference.list
affected_components:
- spring-data-jdbc
confidence: low
---

Context:
This issue was observed in Kotlin DAO code after a Spring Boot 4 version bump.

Symptom:
```text
e: .../GoogleAccountsDao.kt:55:14 Unresolved reference 'list'.
e: .../GoogleCalendarsDao.kt:63:14 Unresolved reference 'list'.
```

Diagnosis:
After the Spring Boot 4 upgrade, the Kotlin compiler reports that a symbol named `list` is not available at the call site in DAO code.

Fix:
