# Testing Philosophy

## 2. Concept Spec: “EA Testing Philosophy”

### 2.1. Intention

EA testing philosophy defines what makes tests valuable and sustainable in the Ergonomic Approach (EA).
It provides decision rules for test levels, doubles, coupling, and speed.
The goal is to make tests fail on behavior and contract changes, not on refactoring.

### 2.2. Ontological Status

This concept is a set of constraints and decision rules for test design and organization.
It is not a specific testing framework, tooling choice, or “TDD school”.
It is not a replacement for requirements formalization.

### 2.3. Concept Invariants

EA testing philosophy remains EA testing philosophy only if all statements below hold.

* Tests primarily verify observable behavior and contracts.
* High-level tests do not encode production implementation structure as expectations.
* Doubles are minimized by default and introduced only with an explicit justification.
* Test speed is treated as a constraint with explicit budgets and regression ownership.
* Coupling between scenario tests and production code is controlled through dedicated test facades, and internal scenario tests call only the SUT directly.

### 2.4. Definition: “Good Test” in EA

A good test is a showcase of a scenario that a user or an integration cares about.
A good test is refactor-safe, meaning it does not fail when the implementation is reorganized without behavior change.
A good test uses a production-like configuration by default.
A good test is fast and deterministic within the project budgets.

### 2.5. Test Levels and Default Choice

EA distinguishes test levels by which boundary is exercised and which risks are targeted.

* **Scenario tests (preferred default)** exercise the system through its public entry points and assert externally observable outcomes.
* **Internal scenario tests** avoid transport overhead by calling the SUT directly, while using `*TestApi` only for fixture setup and observation/asserts.
* **Integration tests** focus on mapping and infrastructure behavior around one component boundary with real infrastructure or realistic emulators.
* **Unit tests** focus on pure logic and invariants and target high branch coverage for the covered code.
* **Tests with doubles** are scenario or integration tests where a dependency is replaced to simulate failure or to isolate an unmanaged dependency.
* In EA, a unit test is pure logic by definition and does not use doubles.

Default decision rules.

* Prefer scenario tests for entry points and external effects.
* Prefer internal scenario tests only when they materially reduce cost while preserving the verified contract.
* Prefer unit tests for pure logic branches that are expensive to reach through entry points without noise.
* Prefer integration tests when the primary risk is persistence, protocol behavior, or mapping between external and internal models.

### 2.6. Doubles Policy (Mocks, Fakes, Stubs)

A double is allowed only if it reduces cost without hiding the primary behavior risk.
A double is required when the dependency is unmanaged, unstable, or infeasible to run in a production-like way.
A double is allowed to simulate failure modes that are expensive or unsafe to reproduce in real infrastructure.
A double must not be used as a shortcut for missing test infrastructure or for avoiding proper test facades.

### 2.7. Coupling Policy (How Tests Touch Production Code)

In external scenario tests, test case code must not call production code directly.
In external scenario tests, calls to production code are allowed only inside dedicated test facades such as `*HttpApi` and `*TestApi`.
In external scenario tests, test case code must not use low-level transport clients directly and must rely on `*HttpApi`.
In internal scenario tests, the test case calls the SUT directly.
In internal scenario tests, all other production interactions (fixture setup and observation/asserts) are performed through `*TestApi` and `*FixturePresets`.
In unit tests, calling the pure SUT directly is allowed and expected.

### 2.8. Links

* EA principles: `../conventions/ea-principles.md` (EA.T1–EA.T3).
* Testing checklist: `../checklists/testing.md`.
* Test code architecture: `testing-testcode-architecture.md`.
* Speed budgets: `testing-speed-budgets.md`.
