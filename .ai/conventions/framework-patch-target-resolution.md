# Framework patch target resolution

## Purpose

This document defines the canonical procedure for resolving where a framework-improvement task is allowed to write changes.

It standardizes:

- `PATCH_MODE` resolution;
- framework root resolution;
- project-local root resolution;
- placeholder interpretation;
- writable-scope policy;
- ambiguity handling.

Use this procedure from framework-improvement skills instead of duplicating local resolver logic.

## When to use

Use this procedure whenever a task may patch:

- the framework repository currently being edited;
- a framework checkout embedded in a client repository;
- `<project-local>/...` in a client repository.

Typical cases:

- framework improvement from design feedback;
- framework improvement from implementation feedback;
- any future task that patches framework instructions based on evidence.

## Inputs

- `PROJECT_DIR` — the evidence repository for the current task.
- Optional `PATCH_MODE` — explicit target override.
- Canonical framework-root and project-local discovery rules from:
  - `AGENTS.md`;
  - `bootstrap/AGENTS.md`.

## Output variables

This procedure resolves:

- `PATCH_MODE`
- `FRAMEWORK_DIR`
- `PROJECT_LOCAL_DIR`

These variables define the only writable roots unless the prompt explicitly expands scope.

## Resolution algorithm

### 1. Treat `PROJECT_DIR` as the evidence repository

Use `PROJECT_DIR` as the repository that contains the task evidence.

This may be:

- a client repository with its own embedded framework checkout;
- the framework repository itself;
- a repository that contains exported evidence and references to framework artifacts.

### 2. Resolve the target mode

If `PATCH_MODE` is explicitly provided, use it.

Allowed values:

- `framework-repo`
- `consumer-project`

If `PATCH_MODE` is not provided, resolve it as follows.

First resolve `PROJECT_FRAMEWORK_DIR` from `PROJECT_DIR` using the canonical framework-root discovery rules.

Then resolve `CURRENT_FRAMEWORK_DIR` as the framework checkout currently being edited, if one exists.

Apply these rules in order:

1. If `PROJECT_FRAMEWORK_DIR` is not found, use `framework-repo`.
2. If both roots are found and resolve to the same filesystem path, use `framework-repo`.
3. If both roots are found and resolve to different filesystem paths, stop and ask which checkout to patch.
4. Otherwise use `consumer-project`.

Do not guess when two different writable framework roots are plausible.

### 3. Resolve `FRAMEWORK_DIR`

Resolve `FRAMEWORK_DIR` using the canonical framework-root discovery rules from:

- `AGENTS.md`
- `bootstrap/AGENTS.md`

If `PATCH_MODE=framework-repo`, resolve the framework checkout currently being edited.

If `PATCH_MODE=consumer-project`, use the already-resolved framework checkout inside `PROJECT_DIR`.

### 4. Resolve `PROJECT_LOCAL_DIR`

Resolve `PROJECT_LOCAL_DIR` by interpreting `<project-local>/...` via the canonical rules from:

- `AGENTS.md`
- `bootstrap/AGENTS.md`

If project-local resolution is unavailable in the current repository shape, keep `<project-local>/...` as a logical reference in framework text, but do not invent filesystem paths.

### 5. Interpret placeholders

In framework-improvement tasks:

- `<framework>/...` means paths under the resolved `FRAMEWORK_DIR`;
- `<project-local>/...` means paths under the resolved `PROJECT_LOCAL_DIR`.

In framework materials, keep project-local references written as `<project-local>/...`.

Use resolved filesystem paths only for:

- execution notes;
- terminal commands;
- local patch application.

Do not replace `<project-local>/...` with absolute or repo-specific paths inside reusable framework documents.

## Writable-scope policy

The default writable scope is strict.

Only change files under the resolved writable roots:

- `${FRAMEWORK_DIR}`
- `${PROJECT_LOCAL_DIR}`

Do not change anything outside those roots unless the prompt explicitly expands scope.

Do not modify:

- product code;
- application configuration unrelated to agent instructions;
- repository files outside the approved instruction scope;
- arbitrary files in the client repository.

If the task is in a client repository, this policy still applies.

The presence of evidence outside the writable roots does not expand write permissions.

## Placement policy

Patch the real enforcing artifact.

Do not default to adding new general knowledge under `ergo/core` or `ergo/tech`.

Add knowledge to `<framework>/ergo/core/` or `<framework>/ergo/tech/` only if both are true:

- the rule is genuinely cross-project;
- that layer is the correct enforcing layer.

Otherwise patch the actual enforcing artifact, for example:

- a role;
- a skill;
- a process;
- a template;
- a convention;
- a regression case;
- a script;
- `<project-local>/...`.

## Ambiguity handling

Stop and ask when ambiguity changes correctness, safety, or writable scope.

Typical stop conditions:

- two different framework checkouts are plausible patch targets;
- the writable root cannot be resolved confidently;
- a requested path appears to be outside the permitted roots;
- the prompt mixes framework evolution with product-code changes.

If ambiguity does not change correctness, safety, or allowed scope, document the least-risk assumption and proceed.

## Minimal execution notes format

When useful, record the resolution in short form:

- `PATCH_MODE=...`
- `FRAMEWORK_DIR=...`
- `PROJECT_LOCAL_DIR=...`

Keep these notes out of reusable framework documents unless they are part of an example.

## Definition of done

This procedure is applied correctly when:

- one patch target is resolved unambiguously or clarified explicitly;
- writable roots are explicit;
- placeholder interpretation is consistent;
- framework text keeps reusable `<project-local>/...` references;
- no changes are made outside the resolved writable scope.