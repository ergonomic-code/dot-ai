# Skills

This directory contains reusable skills expressed as procedural specifications.
Each skill lives in its own directory and is defined by a `SKILL.md` file with YAML front matter.
Internal multi-step workflows live under `../processes/`.

## Requirements and framework feedback

- [`formalizing-task-requirements/SKILL.md`](formalizing-task-requirements/SKILL.md) — Turn an informal task into a formal, testable problem statement.
- [`exporting-chat-artifacts/SKILL.md`](exporting-chat-artifacts/SKILL.md) — Export the current chat transcript and brief for framework improvements.

## Git workflow

- [`git-working-tree-hygiene/SKILL.md`](git-working-tree-hygiene/SKILL.md) — Ensure git working tree hygiene before commits and before reporting completion.

## API design workflows

- [`api-design-cqs/SKILL.md`](api-design-cqs/SKILL.md) — Design and refactor APIs to follow Command–Query Separation (CQS).
- [`choosing-http-status-codes/SKILL.md`](choosing-http-status-codes/SKILL.md) — Choose HTTP status codes for an HTTP/JSON endpoint.

## Testing workflows

- [`refactoring-http-tests-to-httpapi/SKILL.md`](refactoring-http-tests-to-httpapi/SKILL.md) — Refactor Spring/JUnit HTTP tests to typed `*HttpApi` clients.
- [`migrating-spring-http-tests-to-mockmvc/SKILL.md`](migrating-spring-http-tests-to-mockmvc/SKILL.md) — Switch `*HttpApi` clients to a MockMvc-backed `WebTestClient` while keeping routing, security, and codecs correct.
- [`refactoring-test-setup-to-fixturepresets-and-testapi/SKILL.md`](refactoring-test-setup-to-fixturepresets-and-testapi/SKILL.md) — Refactor scenario test setup to `*Fixture` + `*FixturePresets` + `*TestApi`.

## Effects diagram workflow

- [`designing-effects-diagram-from-requirements/SKILL.md`](designing-effects-diagram-from-requirements/SKILL.md) — Build a new effects diagram from requirements.
- [`reverse-engineering-effects-diagram/SKILL.md`](reverse-engineering-effects-diagram/SKILL.md) — Reverse engineer an effects diagram from existing code.

## Platform migration workflows

- [`migrating-spring-boot-35-to-4/SKILL.md`](migrating-spring-boot-35-to-4/SKILL.md) — Migrate a codebase from Spring Boot 3.5 to Spring Boot 4 using the evidence-based migration KB.

## Internal processes

- See [`../processes/engineering-log/README.md`](../processes/engineering-log/README.md) for the `engineering-log/` process and its process-local step specs.
