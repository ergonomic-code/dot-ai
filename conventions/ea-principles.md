# Ergonomic Approach (EA): Principles

This document is the top layer of the EA framework: a set of principles that guide design decisions and act as review criteria.
It states what must be true and how to verify it; implementation details belong in concept specs / skills / checklists.

## 0. Scope, goals, and non-goals

### 0.1. Scope

EA targets application systems where the dominant cost is changing behavior and integrations:

- backend services (HTTP/RPC + async messaging),
- modular monoliths / services with explicit modules,
- systems with a database and multiple external integrations,
- operations/scenarios with business rules and side effects.

### 0.2. Goals

- Changeability: localized changes without cascading consequences.
- Behavioral predictability: observable behavior is fixed and verifiable.
- Fast feedback: tests are the primary regression control mechanism.
- Clear boundaries of responsibility: effects and pure logic are separated.

### 0.3. Non-goals

- Maximum performance at any cost.
- Universality for hard real-time / embedded / UI-first applications.
- “Perfect purity” as an end in itself (rules allow conscious exceptions).

## 1. TL;DR

Testing: cover 100% of observable behavior; test through the public API; keep tests fast.

Data: use immutable records; avoid cycles; keep models compact; encode invariants in types; do not encode “modes” as sets of nullable fields.

Behavior: separate I/O and pure logic; respect complexity budgets; keep one abstraction level; prefer straightforward implementations; maintain a balanced form; follow CQS where possible.

Classes: avoid cycles; keep classes small and cohesive; limit dependency-chain depth; avoid mutable state; minimize blast radius.

## 2. Resolving conflicts between principles

Priority order when principles conflict:

1) Correctness and observable system behavior.
2) Clarity of the model and responsibility boundaries.
3) Low coupling and locality of change.
4) Test speed and engineering efficiency.

## 3. Budgets (targets)

Budgets are target constraints.
They may be overridden per project (for example in `<project-local>/PROJECT-CONTEXT.md` or a dedicated `<project-local>/budgets.yaml`), but any deviation must be explicit and recorded.

- Test time: a single test case < 10 seconds; full service test suite < 300 seconds.
- Cognitive complexity: I/O functions <= 4; pure functions <= 15.
- Record/entity/value object size: up to 10 fields.
- Class size: 7 ± 2 fields.
- Application-level dependency chain depth: no more than 5–6 classes.

---

# 4. Principle cards

Each card follows the same format:

- Statement — normative rule.
- Why — rationale.
- How to verify — audit hooks (no implementation details).
- Links — references to the lower layer (concepts/skills/checklists).
- Exceptions / trade-offs — when deviations are allowed.

## 4.1. Testing

### EA.T1 — Cover 100% of observable behavior and contracts

Statement

- 100% of system entry points are covered by tests through the public API.
- 100% of exit points (effects on external resources) are observable and verified.
- 100% of branches in pure business logic are covered by tests.

Why

- This makes system behavior fixed, observable, and resistant to regressions.

How to verify

- For each entry point there are tests for all meaningful outcomes (successes and failures, including error representation).
- For each external integration there is a test that confirms the observable effect (what exactly was written/sent/requested) and the system reaction to typical failures (when the integration participates in critical scenarios).
- Branch coverage is enabled for pure logic and the target threshold is met.
- The effects diagram (or equivalent) is closed by tests: for each edge “entrypoint → operation → effect” there is a corresponding test case.

Links

- Concepts: `../concepts/effects-diagram.md`, `../concepts/irw-matrix-analysis.md`.
- Skills: `../skills/designing-effects-diagram-from-requirements/`, `../skills/reverse-engineering-effects-diagram/`, `../skills/irw-matrix-analysis/` (TODO).
- Checklists: `../checklists/testing.md`.

Exceptions / trade-offs

- Legacy without tests: incremental closure of contracts is allowed, but the goal is to close 100% of observable behavior.
- Unstable/expensive integrations: contract testing via a stable emulator is allowed if a production-like run is not feasible.

### EA.T2 — Minimize coupling between tests and implementation

Statement

- Tests primarily interact through the system public API, not through implementation classes.
- In test case code, calls to production code are prohibited.
- Calls to production code are allowed only inside dedicated test facades (fixtures API).
- For “expensive” inbound dependencies, prefer fakes; mocks are used only to simulate system failures and/or to verify interactions with unmanaged (external) dependencies.

Why

- Tests must fail when behavior/contract changes, not during refactoring.

How to verify

- Test reviews ensure interactions go through the public API or test facades, not through internal implementation classes.
- The project has a rule/check that forbids tests from importing internal implementation packages (outside fixtures).
- Mocks appear only where justified: either an unmanaged external dependency, or simulation of a system failure.

Links

- Concepts: `../concepts/testing-philosophy.md` (TODO).
- Skills: `../skills/kotlin-testing-conventions/` (TODO), `../skills/refactor-testcases-guideline/` (TODO).
- Checklists: `../checklists/testing.md`.

Exceptions / trade-offs

- If the public API does not expose a needed effect, a temporary test facade is allowed and should later become part of the test API.

### EA.T3 — Keep tests fast (speed as a constraint)

Statement

- Test speed is a first-class constraint; time regressions are treated as an engineering-quality defect.

Why

- Slow tests destroy feedback loops and undermine quality discipline.

How to verify

- Test duration is measured (locally and/or in CI), and regressions are recorded and have an owner.
- The test suite meets the target budgets, or a deviation is explicitly documented.

Links

- Concepts: `../concepts/testing-speed-budgets.md` (TODO).
- Skills: `../skills/test-infra-optimization/` (TODO).
- Checklists: `../checklists/testing.md`.

Exceptions / trade-offs

- Projects may set different budgets, but the principle “speed is controlled and measured” remains mandatory.

---

## 4.2. Data design (records / data classes)

### EA.D1 — Use immutable data models

Statement

- Domain records, entities, and value objects are represented as immutable types.

Why

- This reduces hidden state and makes local reasoning, testing, and evolution cheaper.

How to verify

- The domain model has no mutating methods and no mutable fields.
- State changes are expressed as creating a new value version plus persisting it via a repository/resource.

Links

- Concepts: `../concepts/ergonomic-data-model.md`.
- Skills: `../skills/data-model-refactoring/` (TODO).
- Checklists: `../checklists/data-model.md`.

Exceptions / trade-offs

- Technical DTO/ORM adapters may be mutable at the boundary only in very rare cases and with serious justification; the domain model is not.

### EA.D2 — Do not allow cycles in data dependencies

Statement

- The graph of references between domain types (inclusion/associations) must be a DAG.

Why

- Cycles increase coupling, complicate loading/serialization, and obstruct decomposition.

How to verify

- An architectural check (or review) confirms there are no cycles between domain types.

Links

- Concepts: `../concepts/ergonomic-data-model.md`.
- Skills: `../skills/ergonomic-data-modeling/` (TODO).
- Checklists: `../checklists/data-model.md`.

Exceptions / trade-offs

- The exception applies only to code-level type dependencies: a cyclic dependency between a public API and a hidden implementation is allowed if the implementation factory/registration is embedded in the API.
  In particular, the root of a sealed hierarchy may know about its inheritors.

### EA.D3 — Respect the attribute budget

Statement

- Target budget: up to 10 fields per record/entity/value object; exceeding this is a trigger to decompose.

Why

- Wide structures cause cascading changes and hide heterogeneous responsibilities.

How to verify

- Count the fields: if there are more than 10, the principle is violated and decomposition is required (or a project-level exception is pre-recorded).

Links

- Concepts: `../concepts/ergonomic-data-model.md`.
- Skills: `../skills/data-decomposition/` (TODO).
- Checklists: `../checklists/data-model.md`.

Exceptions / trade-offs

- Protocol-level DTOs may be wider, but in the domain model any excess requires justification.

### EA.D4 — Do not encode invariants as “dependent nullable fields”

Statement

- Invariants like “if A != null then B != null and C == null” must be encoded in types/variants, not as conventions.

Why

- Implicit invariants create hidden modes and destroy maintainability.

How to verify

- Invalid field combinations are unrepresentable at the type level (or are rejected at the boundary by explicit validation with clear diagnostics).

Links

- Concepts: `../concepts/ergonomic-data-model.md`.
- Skills: `../skills/model-invariants-with-types/` (TODO).
- Checklists: `../checklists/data-model.md`.

Exceptions / trade-offs

- Boundary validation is acceptable as a temporary measure when type-level encoding would require disproportionate change.

### EA.D5 — Do not encode “modes” as sets of optional fields

Statement

- If an object has meaningful alternatives (“either this or that”), encode them as explicit variants (sum types / sealed variants), not as combinations of optional/nullable fields.

Why

- “Wide DTOs with modes” cause API/operation sprawl and growth of hidden branching logic.

How to verify

- Domain models and commands contain no structures where nullable fields act as behavior switches.
- Different behaviors are modeled as different types/operations, or via composition over a base behavior.

Links

- Concepts: `../concepts/ergonomic-data-model.md`.
- Skills: `../skills/sum-types-and-variants/` (TODO).
- Checklists: `../checklists/data-model.md`, `../checklists/api-design.md`.

Exceptions / trade-offs

- Optional fields are allowed at the external protocol level (HTTP), but must be reduced to explicit variants inside the system.

---

## 4.3. Methods and functions design

### EA.F1 — Separate I/O and pure functions

Statement

- I/O functions are responsible for effects; pure functions are responsible for computations/rules.
  Mixing is allowed only in thin orchestrators.

Why

- This keeps testing and reasoning local and cheap.

How to verify

- Pure logic is tested without infrastructure.
- Orchestrators are thin: they mostly connect steps and do not contain heavy computations.

Links

- Concepts: `../concepts/effects-diagram.md`, `../concepts/functional-core-imperative-shell.md` (TODO).
- Skills: `../skills/designing-operations/` (TODO).
- Checklists: `../checklists/operations.md`.

Exceptions / trade-offs

- In small scenarios mixing is acceptable, but once branching/integrations grow separation is required.

### EA.F2 — Respect cognitive complexity budgets

Statement

- I/O functions: cognitive complexity <= 4; pure functions <= 15.

Why

- Complexity limits reduce regression risk and make behavior changes cheaper.

How to verify

- CI/review enforces cognitive complexity.
- Budget breaches come with a decomposition plan or an explicit exception.

Links

- Concepts: `../concepts/complexity-budgets.md` (TODO).
- Skills: `../skills/refactor-to-budgets/` (TODO).
- Checklists: `../checklists/operations.md`.

Exceptions / trade-offs

- Generated code and configuration glue may be excluded from the metric.

### EA.F3 — Ensure high function cohesion

Statement

- Functions must have functional/sequential/communicational cohesion; unrelated effects/reads are not mixed without need.

Why

- High cohesion reduces the change surface and simplifies tests.

How to verify

- Reviews confirm the function steps serve a single semantic goal.
- When independent behavior branches appear, the function is decomposed.

Links

- Concepts: `../concepts/cohesion.md` (TODO).
- Skills: `../skills/improve-cohesion/` (TODO).
- Checklists: `../checklists/operations.md`.

Exceptions / trade-offs

- Orchestrators may connect multiple steps if they belong to one scenario and remain thin.

### EA.F4 — Keep one abstraction level per function

Statement

- A function must not operate on terms from different technical domains simultaneously (e.g., HTTP and SQL), except explicit mapping at the integration boundary.

Why

- Mixing levels makes code brittle and prevents integration replacement.

How to verify

- Reviews confirm integration terms are concentrated in adapters/integration layers.
- Domain-layer functions do not know transport/storage details.

Links

- Concepts: `../concepts/layers-and-boundaries.md` (TODO).
- Skills: `../skills/integration-mapping/` (TODO).
- Checklists: `../checklists/operations.md`, `../checklists/integrations.md`.

Exceptions / trade-offs

- The integration layer may keep domain and integration terms together for mapping.

### EA.F5 — Prefer straightforward implementations

Statement

- Prefer simple, linear solutions when they do not reduce testability, change locality, or clarity.

Why

- Complex abstractions increase maintenance cost.

How to verify

- Reviews require justification for abstractions: each must exist due to real variability or reuse.

Links

- Concepts: `../concepts/straightforward-design.md` (TODO).
- Skills: `../skills/simplify-implementation/` (TODO).
- Checklists: `../checklists/operations.md`.

Exceptions / trade-offs

- If simplicity breaks key invariants/boundaries, a more complex composition is allowed with explicit documentation.

### EA.F6 — Maintain a balanced form (structural design)

Statement

- Separate code into orchestration, input (afferent branches), transformations, and output (efferent branches).

Why

- This makes scenarios transparent and localizes change.

How to verify

- Reviews can read the operation “shape”: where input is, where computation is, where output effects are.
- Orchestration does not contain heavy logic.

Links

- Concepts: `../concepts/structural-design-balanced-form.md` (TODO).
- Skills: `../skills/designing-operations/` (TODO).
- Checklists: `../checklists/operations.md`.

Exceptions / trade-offs

- Very small operations may be denser; once branching grows, the layout is required.

### EA.F7 — Follow Command–Query Segregation (CQS) where possible

Statement

- Commands change state and return minimal information; queries do not change state.

Why

- This improves predictability and simplifies testing.

How to verify

- Reviews ensure there are no hidden effects in query methods.
- Command operations have explicit effects and diagnosable errors.

Links

- Concepts: `../concepts/cqs.md` (TODO).
- Skills: `../skills/api-design-cqs/` (TODO).
- Checklists: `../checklists/api-design.md`.

Exceptions / trade-offs

- Exceptions are allowed for technical optimizations or when a side effect is explicitly required by requirements (for example, tracking the number of record reads), as long as the effect is explicitly documented and tested.

---

## 4.4. Classes design

### EA.C1 — Do not allow dependency cycles between application classes

Statement

- The application-level dependency graph must be a DAG.

Why

- Cycles increase coupling and break modularity.

How to verify

- An architectural check (or module review) confirms there are no cycles.

Links

- Concepts: `../concepts/modularity.md` (TODO).
- Skills: `../skills/remove-dependency-cycles/` (TODO).
- Checklists: `../checklists/architecture.md`.

Exceptions / trade-offs

- Temporary exceptions are allowed only with an explicit cycle-breaking plan.

### EA.C2 — Respect the class field budget

Statement

- Target budget: 7 ± 2 fields; exceeding this is a trigger to decompose.

Why

- Large classes usually mix multiple responsibilities and have a wide change surface.

How to verify

- Reviews record the breach and the chosen decomposition (or the breach is prevented by design).

Links

- Concepts: `../concepts/class-design.md` (TODO).
- Skills: `../skills/refactor-large-class/` (TODO).
- Checklists: `../checklists/classes.md`.

Exceptions / trade-offs

- As a rule, there are no exceptions: exceeding the budget requires decomposition.

### EA.C3 — Limit application dependency-chain depth

Statement

- No more than 5–6 application classes in a call/dependency chain; infrastructure does not count if it does not add application-level coupling.

Why

- Deep chains reduce traceability and increase regression risk.

How to verify

- Reviews of an operation/scenario assess chain depth; breaches trigger graph simplification.

Links

- Concepts: `../concepts/dependency-graphs.md` (TODO).
- Skills: `../skills/flatten-call-chain/` (TODO).
- Checklists: `../checklists/architecture.md`.

Exceptions / trade-offs

- Deep chains are acceptable in infrastructure stacks if the application part remains thin.

### EA.C4 — Ensure high class cohesion

Statement

- A class’s fields must serve a single responsibility; narrow operation classes (one public method) are preferred.

Why

- High cohesion reduces blast radius and lowers maintenance cost.

How to verify

- Reviews ensure the class fields are used by most methods.
- When “subsets of methods use subsets of fields” appear, the class is decomposed.

Links

- Concepts: `../concepts/cohesion.md` (TODO).
- Skills: `../skills/extract-operation-class/` (TODO).
- Checklists: `../checklists/classes.md`.

Exceptions / trade-offs

- Orchestrators may have lower cohesion if they remain thin.

### EA.C5 — Avoid mutable state in application classes

Statement

- Application classes avoid mutable fields and also avoid “immutable fields holding mutable types”.

Why

- Mutability increases hidden state and makes behavior non-obvious.

How to verify

- There are no mutable fields in the application layer (or equivalents), except strictly justified cases.
- Changing state is moved into explicit resources/repositories.

Links

- Concepts: `../concepts/state-and-effects.md` (TODO).
- Skills: `../skills/remove-mutable-state/` (TODO).
- Checklists: `../checklists/classes.md`.

Exceptions / trade-offs

- Technical caching/buffering components may be exceptions with clear invariants and tests.

### EA.C6 — Minimize a class blast radius

Statement

- A class must have a narrow surface of effects: the minimal set of external resources it reads/writes.

Why

- The fewer independent resources a component touches, the easier it is to understand and predict the consequences of changes; secondarily, the lower the cost of change and the risk of cascading regressions.

How to verify

- Effects on resources are explicitly listed for the class/operation (via an effects diagram or equivalent).
- Reviews disallow adding “optional effects” into an existing class without considering extraction into a separate component.
- Adding a new write effect requires justification (invariant/transactional atomicity) or considering decoupling via an event.

Links

- Concepts: `../concepts/effects-diagram.md`.
- Skills: `../skills/designing-effects-diagram-from-requirements/`, `../skills/split-effects/` (TODO).
- Checklists: `../checklists/architecture.md`, `../checklists/operations.md`.

Exceptions / trade-offs

- If multiple effects must be atomic due to a business invariant, co-locating them is allowed with an explicit recorded reason.
