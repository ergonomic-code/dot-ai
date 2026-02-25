# Checklist: Testing

Primary reference is `../conventions/ea-principles.md` (EA.T1–EA.T3).

## Coverage

- Every system entry point affected by the change is covered by tests through the public API.
- Every external write effect introduced or modified by the change is observable and asserted in tests.
- Pure business logic branches affected by the change are covered by unit tests with branch coverage enabled where feasible.
- Every regression bug fix is accompanied by a test that reproduces the bug and fails without the fix.

## Coupling

- External scenario test cases do not call production code directly.
- In external scenario tests, calls to production code are allowed only inside dedicated test facades (`*HttpApi`, `*TestApi`, `*FixturePresets`).
- Internal scenario tests call the SUT directly and use `*TestApi` and `*FixturePresets` only for fixture setup and observation/asserts.
- Smell: if a test or a `*HttpApi` models an HTTP response body as `Map<*, *>` or `Any`, treat it as a missing typed contract and refactor the client to decode the controller return type.
- Smell: if multiple tests create the same HTTP client/test infrastructure (for example `WebTestClient` creation, base URLs, object mappers), treat it as missing shared test infrastructure and extract it to a base test or a dedicated fixtures APIs.
- Smell: if a test case inlines low-level technical boilerplate (for example latches, futures, or executors), extract it to shared test platform helpers or fixture APIs.
- Smell: if a test case repeats expected error parsing or allowlisting, extract it into an outcome-returning `*HttpApi` method.
- Tests primarily assert behavior and contracts, not internal implementation details.
- In external scenario (HTTP/API) tests, prefer asserting the HTTP contract plus observable effects (published messages, outgoing calls, follow-up queries) over inspecting internal persistence or command-storage details.
- Mocks are used only for unmanaged external dependencies and for simulating failures.

## Test architecture

- External scenario test cases call HTTP entry points only through `*HttpApi` and do not use `WebTestClient` or `RestTestClient` directly.
- Complex fixture setup and insertion is implemented in `*FixturePresets`, using direct production calls or `*TestApi` when reuse warrants it.
- Stubs are defined only in `Mock*Server` wrappers and are not registered ad-hoc in test cases.
- Shared test infrastructure (boot, reset, clients) is extracted and reused.
- After changing shared HTTP test infrastructure (client wiring, base URLs, codecs, MockMvc vs real transport), run a sentinel smoke set that covers routing, authentication, serialization, and architecture rules.
- Test runtime is measured and kept within budgets, or deviations are explicitly recorded.

## Speed

- New tests keep typical per-test and suite runtime within the project budgets, or the deviation is explicitly recorded.
- Slow outlier tests are allowed only with an explicit justification and when the suite budget is still met.
- Local test runs provide duration feedback (for example, for the relevant test subset or the full suite).
- If a noticeable time regression is observed locally, it is recorded and has an owner.

## Links

- IRW analysis: `../concepts/irw-matrix-analysis.md`.
- Testing philosophy: `../concepts/testing-philosophy.md`.
- Test code architecture: `../concepts/testing-testcode-architecture.md`.
- Testing speed budgets: `../concepts/testing-speed-budgets.md`.
- Code hygiene: `../conventions/code-hygiene.md`.
- Kotlin testing conventions: `../ergo/tech/kotlin/testing.md`.
- Spring testing conventions: `../ergo/tech/spring/testing.md`.
