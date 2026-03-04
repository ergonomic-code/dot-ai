---
id: sb4-0003
title: DaoAuthenticationProvider API change breaks test security configuration
stage: compile
projects:
- qg-repo-main
error_signatures:
- compile.kotlin.argument-type-mismatch.PasswordEncoder-to-UserDetailsService
- compile.kotlin.unresolved-reference.setUserDetailsService
- tooling.generic.Execution.failed.for.task.app.compileTestFixturesKotlin
- runtime.org.gradle.api.tasks.TaskExecutionException.Execution.failed.for.task.app.compileTestFixturesKotlin
affected_components:
- security
confidence: high
---

Context:
This issue was observed in Kotlin-based Spring Security test configuration.
This issue happened while compiling `testFixtures` sources after upgrading to Spring Boot 4.

Symptom:
```text
e: .../TestPasswordEncoderConfig.kt:... Argument type mismatch: actual type is 'PasswordEncoder', but 'UserDetailsService' was expected.
e: .../TestPasswordEncoderConfig.kt:... Unresolved reference 'setUserDetailsService'.
```

Diagnosis:
The `DaoAuthenticationProvider` constructor and configuration methods changed, so code written for the previous API no longer compiles.
The failing code used `DaoAuthenticationProvider(passwordEncoder)` and then called `setUserDetailsService`, which is not available with the updated API.

Fix:
Instantiate `DaoAuthenticationProvider` with `UserDetailsService` and set the password encoder using `setPasswordEncoder`.
Replace `DaoAuthenticationProvider(fastPasswordEncoder())` plus `setUserDetailsService(userDetailsService)` with `DaoAuthenticationProvider(userDetailsService)` plus `setPasswordEncoder(fastPasswordEncoder())`.
