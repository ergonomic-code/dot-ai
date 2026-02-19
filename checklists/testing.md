# Checklist: Testing

Primary reference is `../conventions/ea-principles.md` (EA.T1–EA.T3).

## Coverage

- Every system entry point affected by the change is covered by tests through the public API.
- Every external write effect introduced or modified by the change is observable and asserted in tests.
- Pure business logic branches affected by the change are covered by unit tests with branch coverage enabled where feasible.

## Coupling

- Test cases do not call production code directly except via dedicated test facades (fixtures APIs).
- HTTP entry points are exercised through `*HttpApi` fixtures APIs, and transport-contract checks (for example JSON schema validation) are implemented in the client rather than duplicated in test cases.
- Smell: if a test or a `*HttpApi` models an HTTP response body as `Map<*, *>` or `Any`, treat it as a missing typed contract and refactor the client to decode the controller return type.
- Tests primarily assert behavior and contracts, not internal implementation details.
- Mocks are used only for unmanaged external dependencies and for simulating failures.

## Speed

- New tests keep per-test and suite runtime within the project budgets, or the deviation is explicitly recorded.
- Local test runs provide duration feedback (for example, for the relevant test subset or the full suite).
- If a noticeable time regression is observed locally, it is recorded and has an owner.

## Links

- IRW analysis: `../concepts/irw-matrix-analysis.md`.
- Kotlin testing conventions: `../ergo/tech/kotlin/testing.md`.
- Spring testing conventions: `../ergo/tech/spring/testing.md`.
