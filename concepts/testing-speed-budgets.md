# Testing Speed Budgets

## 2. Concept Spec: “EA Testing Speed Budgets”

### 2.1. Intention

This concept defines how EA projects treat test speed as a first-class constraint.
The goal is to preserve fast feedback loops while keeping tests production-like and refactor-safe.
The output of applying this concept is a measurable budget, a measurement mechanism, and an ownership rule for regressions.

### 2.2. Ontological Status

This concept is a discipline for setting and maintaining test time budgets.
It is not an optimization guide for a specific stack.
It is not a requirement to have only unit tests.

### 2.3. Concept Invariants

Testing speed budgets remain a valid EA testing speed discipline only if all statements below hold.

* A budget exists for the typical (average) test case duration and for the relevant test suite duration.
* Individual tests may exceed the per-test budget if the suite budget is respected and the exception is explicit.
* Budgets are measured regularly (locally and/or in CI).
* A time regression is treated as a defect with an owner and an explicit follow-up.
* Optimizations preserve the verified contracts and do not silently reduce coverage.

### 2.4. Budgets (Default Targets)

Default targets are defined in `../conventions/ea-principles.md` (EA budgets section).
Projects may override the numbers, but the existence of budgets and measurement remains mandatory.
Per-test budgets are targets for typical tests, not a hard limit for every individual test.

### 2.5. Suite Setup vs Per-Test Setup

Test runtime is typically dominated by environment boot, infrastructure I/O, and repeated setup.
To control cost, separate the work into two layers.

* **Suite setup** boots shared infrastructure and the application context once per suite run when feasible.
* **Per-test setup** resets state to a known baseline and inserts only scenario-specific data.

The boundary is valid only if per-test setup is deterministic and does not leak state between tests.

### 2.6. Typical Optimization Levers

The techniques below are common across stacks and map to concrete implementations in tech conventions.

* Avoid application context restarts as part of a single suite run.
* Prefer shared boot + fast per-test reset over full environment recreation per test.
* Keep a minimal shared baseline fixture and reset to it efficiently between tests.
* Prefer stable “test facades” (`*HttpApi`, `*TestApi`, `*FixturePresets`) over ad-hoc setup in test cases.
* Use controlled randomness and deterministic seeds for generated data.

### 2.7. Measurement and Regression Handling

Measure runtime for the relevant test subset locally during development and in CI for the main suite.
When a regression is detected, record the delta, the suspected cause, and the owner in a project-local engineering log or a tracking system.
If a budget cannot be met, document the deviation explicitly and justify it.

### 2.8. Links

* EA principle card: `../conventions/ea-principles.md` (EA.T3).
* Testing checklist: `../checklists/testing.md`.
* Test code architecture: `testing-testcode-architecture.md`.
