---
id: sb4-0010
title: Oversized multipart requests stop returning an empty 413 response
stage: test
projects:
- qg-repo-main
error_signatures:
- tooling.generic.Execution.failed.for.task.app.test
- runtime.org.gradle.api.tasks.TaskExecutionException.Execution.failed.for.task.app.test
- runtime.org.gradle.api.internal.exceptions.MarkedVerificationException.There.were.failing.tests.See.the.report.at
affected_components:
- spring-web
- tomcat
confidence: medium
---

Context:
This issue was observed as failing application tests after upgrading to Spring Boot 4.
This issue was fixed by explicitly handling multipart size limit exceptions at the servlet filter level.

Symptom:
```text
Execution failed for task ':app:test'.
> There were failing tests.
```

Diagnosis:
The fix commit introduces a dedicated filter that catches multipart size limit exceptions and sets the HTTP status to 413 without writing a response body.

Fix:
Add an early servlet filter that catches multipart size limit exceptions and normalizes the response to an empty 413 status.
Handle both `MaxUploadSizeExceededException` and the underlying Tomcat `SizeLimitExceededException`.
