# 📄 Execution Specification (Execution-Spec)

> **Contract (for Codex)**
>
> **EN**
> - Execute this document literally; do not add requirements or “improvements”.
> - Sources of truth: this file + `AGENTS.md` + `AGENTS.local.md`.
> - If something is ambiguous or missing, ask a question; do not guess.
>

---

## 0. Document purpose

**Document origin:**
This Execution-Spec is created **from the `=== RESULT FOR EXECUTION-SPEC ===` block in `03-solution-hld.md`**:

```
=== RESULT FOR EXECUTION-SPEC ===
<...>
```

That block is considered the **input data** for filling in all sections below.

**Goal:**
Implement the functionality *strictly according to* this document.

**Forbidden:**

- any deviations from the requirements;
- “at your discretion” improvements and optimizations;
- rethinking the architecture;
- adding unspecified requirements.

**Implementer role:**

- the implementer must treat this document and the rules from `AGENTS.md` / `AGENTS.local.md` as the *only sources of truth*;
- if a requirement is not described in the document and does not follow from `AGENTS.md` / `AGENTS.local.md`, the implementer must treat it as **non-existent**;
- if something is ambiguous, the implementer must **ask a question** instead of guessing;
- the implementer must follow TDD (for each test case from section 9): write a test → verify it fails → write/change production code → verify the test passes.

---

## 1. Context and constraints

### 1.1 System context

- Brief description: <...>
- Language / version: <...>
- Stack / frameworks: <...>
- Application type: <...>
- Module / subsystem: <...>
- Integration points (if any): <...>

### 1.2 Hard constraints

- <...> (compatibility / backward compatibility)
- <...> (security / access control)
- <...> (performance / timeouts / resource limits)
- <...> (contract mapping and sources of truth, see `../../../conventions/contracts.md`)
- Always follow the development and testing rules from `AGENTS.md` and `AGENTS.local.md`.

> This section is mandatory.
> Constraints take precedence over all other requirements.

---

## 2. Terms and definitions

| Term | Meaning |
| ------ | -------- |
| <...> | <...> |
| <...> | <...> |

If a term is **not defined here**, it **must not be used** in the implementation.

---

## 3. Required behavior (Behavior specification)

### 3.1 Main scenario

Step by step, without explanations:

1. <...>
2. <...>
3. <...>

### 3.2 Alternative scenarios and errors

- If <...> → <...>
- If <...> → <...> (error/status/code/message)

---

## 4. Rules and invariants

Format: statements only, no explanations.

- <...>
- <...>
- <...>

---

## 5. Data contracts

### 5.0 Contract map (cross-surface naming and encoding)

Use the conventions from `../../../conventions/contracts.md`.
If a concept exists in multiple surfaces, it must appear in this table.

| Concept | HTTP (field/param) | Persistence (table/column/path) | Integration (keys) | Encoding | Source of truth |
| --- | --- | --- | --- | --- | --- |
| <...> | <...> | <...> | <...> | <...> | <...> |
| <...> | <...> | <...> | <...> | <...> | <...> |

### 5.1 DTO / API models

```kotlin
// DTO / API models: <...>
```

### 5.2 Domain model

```kotlin
// Domain model: <...>
```

Serialization / Jackson / nullability:
- Required vs optional fields: <...>
- Default values: <...>
- Discriminators and polymorphism: <...>
- Date/time formats: <...>
- Unknown fields handling: <...>

---

## 6. Persistence and infrastructure

- Storage: <...>
- Tables / collections: <...>
- Data format: <...>
- Mapping / data access: <...>
- Indexes / constraints: <...>
- Migrations (if any): <...> (include ordering, backfill, and idempotence requirements)

---

## 7. Scope boundaries (Out of scope)

Explicitly forbidden:

- <...>
- <...>
- <...>

---

## 8. Implementation requirements

### 8.1 What must be done

If any public API changes, this section **must** include a requirement to update the OpenAPI specification file (state the exact path).

#### Add

- <...>
- <...>

#### Change

- <...>
- <...>

#### Delete (if applicable)

- <...>

### 8.2 What **not** to do

- <...>
- <...>
- <...>
- Do not use deprecated symbols unless explicitly allowed in this document.

---

## 9. Testing

- Approach: TDD (see section 0, “Implementer role”).
- Test oracle (assertion source of truth): <...>

### 9.1 Test case list (must drive the implementation)

Describe the test work as a diff relative to the current test cases in the codebase.
For each **changed** or **deleted** test case, include a code reference to the current implementation (a repository path with a line number).

#### Added test cases

List new test cases that must be created.
Format (hierarchy: **SUT → method → Given/When/Then**):

1. <...> (SUT; used in `@DisplayName`)
   1. <...> (method name)
      1. Given — <...> (content of the `// Given` block)
      2. When — <...>
      3. Then — <...>

#### Changed test cases

List existing test cases that must be modified.
For each item, include:
- Code reference (current): `<path/to/test/File.kt:123>`
- Target change (what the test must become): <...>

#### Deleted test cases

List existing test cases that must be removed.
For each item, include:
- Code reference (current): `<path/to/test/File.kt:123>`
- Deletion target (what is being removed): <...>

Write test cases at the level of system entry points: HTTP requests, queue messages (RabbitMQ, Kafka), and `@Scheduled` jobs.

---

## 10. Definition of Done

- ✅ The behavior from section 3 is implemented
- ✅ The constraints from section 1.2 are satisfied
- ✅ All tests from section 9 pass
- ✅ The document contains no unfilled placeholders

---

## 11. Decision history (Rationale — read‑only)

> A section to preserve the intent behind decisions.
>
> **The implementer is forbidden from using this section to make changes.**

- <...> (why this approach was chosen)
- <...> (which alternatives were considered and why they were rejected)
- <...> (which key trade-offs were accepted)
