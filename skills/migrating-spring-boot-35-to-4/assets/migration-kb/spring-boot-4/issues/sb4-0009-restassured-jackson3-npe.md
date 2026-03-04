---
id: sb4-0009
title: RestAssured upgrade resolves NullPointerException in tests after Jackson 3
  migration
stage: test
projects:
- qg-repo-main
error_signatures:
- runtime.java.lang.NullPointerException.unknown
affected_components:
- jackson
- testing
confidence: medium
---

Context:
This issue was observed in end-to-end tests using RestAssured after migrating the project to Jackson 3.
This issue happened during the `:app:test` task.

Symptom:
```text
AuthTests ... FAILED
    java.lang.NullPointerException
```

Diagnosis:

Fix:
Upgrade RestAssured to the version observed in the fix commit.
Avoid mixing test libraries that assume Jackson 2 APIs with a codebase migrated to Jackson 3.
