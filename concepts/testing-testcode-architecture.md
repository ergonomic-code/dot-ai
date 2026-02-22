# Testing Test Code Architecture

## 2. Concept Spec: “EA Testing Test Code Architecture”

### 2.1. Intention

This concept defines a minimal, repeatable architecture for scenario-level test code in EA projects.
The goal is to keep test cases thin, stable under refactoring, and cheap to evolve.
The architecture controls coupling by introducing explicit test-layer component kinds and allowed dependencies.

### 2.2. Ontological Status

This concept is a dependency and responsibility model for test code.
It is expressed as a set of rules about where calls and knowledge are allowed to live.
It is not a production architecture and it does not dictate production package structure.

### 2.3. Vocabulary

The terms below are normative for this concept.

* **Test case** is a scenario-level test method that asserts observable outcomes of a scenario.
* **External scenario test** is a scenario test where the action is performed through `*HttpApi` and transport is part of the exercised contract.
* **Internal scenario test** is a scenario test where the action is performed by calling the SUT directly, while setup and observation/asserts use `*TestApi` and `*FixturePresets`.
* **`*HttpApi`** is a typed HTTP client for calling system entry points through transport.
* **`*TestApi`** is a typed façade for fixture setup and observation/asserts that is allowed to call production code directly (controllers, operations, repos).
  It is scoped to one resource and must not orchestrate multi-resource writes.
* **`*Fixture`** is a declarative data graph describing required state, inputs, and stubs for a scenario or a resource.
* **`*FixturePresets`** is a DI component that builds typical `*Fixture` graphs and inserts fixtures via production calls (directly or via `*TestApi`) and `Mock*Server`.
* **`Mock*Server`** is a wrapper over a stubbing tool (for example WireMock) that owns endpoint-level stubs and their defaults.
* **`*ObjectMother`** is a builder/factory for production data types used in fixtures and requests.
* **Assertions** are reusable domain assertions that encode domain-specific verification rules.
* **Test infra** is suite and per-test setup code that boots and resets the test environment.

### 2.4. Concept Invariants

The test code architecture remains an EA testing test code architecture only if all statements below hold.

* External scenario test cases do not call production code directly.
* Internal scenario tests call the SUT directly and use `*TestApi` only for fixture setup and observation/asserts.
* External scenario test cases do not use low-level transport clients directly and rely on `*HttpApi`.
* Simple fixture setup is expressed through direct `*TestApi` calls in the test case Arrange step.
* Complex fixture setup is extracted into `*FixturePresets`.
* Stubbing is centralized in `Mock*Server` wrappers and is not scattered across tests.
* Test infra is shared and extracted, not duplicated across test classes.

### 2.5. Allowed Dependencies (Operational Rules)

The rules below define allowed calls for scenario tests.

* A test case may call `*FixturePresets`, `*HttpApi` (external), `*TestApi` (setup and observation), and domain assertions.
* In internal scenario tests, the test case calls the SUT directly in the Act step and does not call other production code directly.
* `*FixturePresets` may call production code directly for fixture insertion and may extract reused sequences into `*TestApi`.
* `*FixturePresets` may call `Mock*Server` and `*ObjectMother`.
* `*HttpApi` may call low-level HTTP clients and must not leak them to test cases.
* `*TestApi` may call production code directly and must not be called by production code.
* `Mock*Server` may call the underlying stub framework and must expose scenario-friendly methods.
* Assertions may depend on production types, but must not call production behavior.

### 2.6. Minimal Graph Notation (for AI)

```yaml
nodes:
  - TestCase
  - SUT
  - HttpApi
  - TestApi
  - Fixture
  - FixturePresets
  - MockServer
  - ObjectMother
  - Assertions
  - TestInfra
  - ProductionCode

edges_allowed:
  - TestCase -> FixturePresets
  - TestCase -> HttpApi
  - TestCase -> TestApi
  - TestCase -> Assertions
  - TestCase -> SUT
  - FixturePresets -> TestApi
  - FixturePresets -> MockServer
  - FixturePresets -> ObjectMother
  - FixturePresets -> ProductionCode
  - HttpApi -> ProductionCode
  - TestApi -> ProductionCode
  - MockServer -> ProductionCode
```

Notes.

* `HttpApi -> ProductionCode` means “calls via transport to a port”, not direct method calls.
* `MockServer -> ProductionCode` means “serves stubbed endpoints used by production code”, not direct method calls.
* `FixturePresets -> ProductionCode` is allowed for one-off fixture insertion, and reused sequences should be extracted to `*TestApi`.
* `SUT` is a selected production component and is considered part of `ProductionCode`.
* `TestCase -> SUT` is allowed only for internal scenario tests and only for the selected SUT.

### 2.7. Construction Algorithm (When Adding a New Scenario Test)

1. Identify the entry point and its contract.
2. Decide whether the scenario is covered as an external or an internal scenario test.
3. If external, create or update a `*HttpApi` method that matches the entry point contract.
4. If internal, call the SUT directly in the Act step while keeping the same scenario-level outcomes.
5. Create or update `*TestApi` methods required for fixture setup and observation/asserts.
6. By default, arrange the scenario through direct `*TestApi` calls in the test case.
7. If the scenario requires complex or reused setup, create or update a `*Fixture` and materialize it via `*FixturePresets` (using direct production calls or `*TestApi` when reuse warrants it, and `Mock*Server`) instead of inline `*TestApi` calls.
8. Create or update domain assertions for the scenario outcomes.
9. Implement the test case as a thin script: arrange via direct `*TestApi` calls or via `*FixturePresets`, act via `*HttpApi` (external) or via the SUT call (internal), assert via domain assertions.
10. Extract any duplicated infra or stubbing into shared `TestInfra` and `Mock*Server` utilities.

### 2.8. Typical Errors (Anti-Patterns)

* External scenario test cases call production controllers/services/repos directly.
* Internal scenario tests call production code other than the SUT directly.
* Test cases instantiate or configure `WebTestClient` / `RestTestClient` directly.
* Test cases assemble complex or reused object graphs inline instead of using `*Fixture` and `*FixturePresets`.
* `*TestApi` methods orchestrate multiple resources instead of keeping `*TestApi` single-resource and moving orchestration to `*FixturePresets`.
* WireMock stubs are registered ad-hoc in test cases instead of being owned by `Mock*Server`.
* Multiple tests duplicate environment boot and reset logic instead of using shared test infra.
