---
name: migrating-spring-boot-35-to-4
description: Evidence-based workflow for migrating a codebase from Spring Boot 3.5 to Spring Boot 4 using the inlined knowledge base snapshot under `assets/migration-kb/spring-boot-4/`. Use when upgrading Spring Boot to 4 and fixing resulting dependency, compilation, test, runtime, or tooling failures by mapping symptoms to KB issues and applying the documented fixes.
---

# Spring Boot 3.5 to 4 migration (evidence-based)

## Inputs

- A target repository to migrate and a branch to work on.
- The build command used by the project (Gradle or Maven) and its failing output.
- The inlined migration knowledge base snapshot under `assets/migration-kb/spring-boot-4/`.

## Outputs

- A minimal sequence of build file and source changes that make the project build and tests pass.
- A migration report that maps each failure family to a KB issue or to an explicitly unknown bucket.
- Links to the KB issues that were used as guidance.

## Knowledge base entry points

- Start with `assets/migration-kb/spring-boot-4/README.md` to understand scope and limitations.
- Use `assets/migration-kb/spring-boot-4/index.yaml` as the canonical list of issues and patterns.
- Read the linked issue files under `assets/migration-kb/spring-boot-4/issues/` before applying changes.
- Use the pattern files under `assets/migration-kb/spring-boot-4/patterns/` when multiple errors share the same ecosystem change.

## Workflow

### 1) Establish a failing baseline

1. Create a dedicated migration branch.
2. Upgrade the project to Spring Boot 4 using the project’s normal dependency management mechanism.
3. Run the smallest build that reproduces failures and capture the full output.
4. Split failures into dependency, compile, test, runtime, and tooling buckets based on the first meaningful error.

### 2) Cluster errors by root cause

1. Group errors by shared classes, packages, artifacts, or API names.
2. Treat multiple compiler errors as one issue when they stem from the same type relocation or signature change.
3. Prefer one fix per root cause cluster, and rerun the build after each cluster is addressed.

### 3) Map clusters to KB issues and patterns

1. Search `assets/migration-kb/` for high-signal tokens from the failing output.
2. Use issue titles and `error_signatures` blocks to confirm that the symptom family matches.
3. If multiple issues match, prefer the one whose evidence diff touches the same dependency or imports.

### 4) Apply the fix using diff evidence

1. In the selected issue file, follow the “Fix” section first.
2. Replicate the minimal changes in the target repository.
3. If the fix is ambiguous, apply the smallest safe change, and note uncertainty in the report.

### 5) Validate and iterate

1. Rerun the failing build step after each fix cluster.
2. When the build reaches the test phase, fix test failures by mapping them to KB test-stage issues and patterns.
3. Keep a running report using `references/sb4-migration-report-template.md`.

## Quick mapping hints (KB-backed)

- Use `sb4p-001` when Kotlin compilation errors mention stricter nullability metadata in Spring APIs and issues resemble `sb4-0001` or `sb4-0006`.
- Use `sb4p-002` when errors mention `tools.jackson.*`, missing Jackson Kotlin helpers, or Jackson 3 related test breakage and issues resemble `sb4-0007`, `sb4-0008`, `sb4-0009`, or `sb4-0012`.
- Use `sb4p-003` when code imports `org.springframework.boot.autoconfigure.*` classes that no longer resolve and issues resemble `sb4-0004`.
- Use `sb4p-004` when tests fail around `DuplicateKeyException` semantics and issues resemble `sb4-0011`.
- Use `sb4p-005` when Kotlin code uses property assignment against Java setters and errors resemble `sb4-0002`.

## Unknowns

- If a cluster does not match any KB issue, record it as “unmapped” and do not guess a root cause.
- If the user wants to extend the KB, add a new issue only after collecting concrete failing output and a fix diff for the target repository.
