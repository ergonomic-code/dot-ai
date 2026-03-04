---
id: sb4-0005
title: TypeInformation moves from org.springframework.data.util to org.springframework.data.core
stage: compile
projects:
- qg-repo-main
error_signatures:
- compile.kotlin.unresolved-reference.TypeInformation
affected_components:
- spring-data
confidence: high
---

Context:
This issue was observed in Kotlin code using Spring Data JDBC repository support classes.
This issue happened after upgrading to Spring Boot 4 and compiling application sources.

Symptom:
```text
e: .../FilesMetaDataRepo.kt:7:38 Unresolved reference 'TypeInformation'.
```

Diagnosis:
The `TypeInformation` type used by the code was no longer available under the previous import path.
The fix commit updates imports from `org.springframework.data.util.TypeInformation` to `org.springframework.data.core.TypeInformation`.

Fix:
Update Spring Data `TypeInformation` imports to the new package.
Replace `org.springframework.data.util.TypeInformation` with `org.springframework.data.core.TypeInformation`.
