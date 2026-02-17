## 2. Concept spec: “Structure Chart”

### 2.1. Intention

A Structure Chart is used to represent a system’s modular structure as (1) a hierarchical control decomposition and (2) explicit inter-module interfaces.

It replaces informal reasoning such as “what calls what, under which conditions, and what crosses the boundary” with a verifiable artifact that supports structural review and improvement before (and during) implementation.

Measurable benefit: the artifact makes it possible to evaluate and change structure using fan-in / fan-out (span of control), interface complexity, coupling types, cohesion signals, and the presence of coordination-heavy modules.

---

### 2.2. Ontological Status

A Structure Chart is a structural design model: a graph of modules with a distinguished control hierarchy (a rooted DAG, typically a tree) plus explicit interface relations and optional procedural annotations.

It is not:

* a statement-level flowchart;
* a runtime trace;
* a dependency injection graph;
* a data schema.

Operational distinction rule:

If the artifact primarily answers “modules, control hierarchy, interfaces, and structural quality signals,” it is a Structure Chart.
If it primarily answers “statement sequencing / algorithmic control flow,” it is not.

---

### 2.3. Concept Invariants

1. Control hierarchy is explicit and acyclic.
   Verification: `control_calls` form an acyclic directed graph; every module has 0 or 1 control parent (0 only for roots).

2. Invocation is represented only via control calls.
   Verification: any module that can be executed due to another module must be reachable by `control_calls` (including behavior passed as a parameter).

3. Interfaces are explicit.
   Verification: any cross-module dependency is represented as either (a) a data couple, (b) a control couple, or (c) an explicit dependency on a shared “data-only” module; no “invisible” cross-boundary dependency is allowed in the chart.

4. Procedural structure, when important, is represented as annotations on control calls (not as a replacement for structural decomposition).
   Verification: loops/conditionals/one-shot execution appear only as annotations on calls, not as standalone flowchart logic.

5. Lexical inclusion is a separate relation (orthogonal to control).
   Verification: if a module is defined within the lexical boundaries of another (e.g., lambda/local function), this is represented by `lexical_inclusions`, and does not change the control-parent rule.

---

### 2.4. Minimal Notation

Mandatory element types:

* `module`

  * `id`
  * `name`

* `control_call`

  * `from`
  * `to`

Optional element types:

* `data_couple`

  * `from`
  * `to`
  * `items` (list of names)

* `control_couple`

  * `from`
  * `to`
  * `signals` (list of names)

* `lexical_inclusion`

  * `outer`
  * `inner`

* `data_only_module`

  * a `module` with `type: data_only` that represents a shared environment explicitly

Recommended module attributes:

* `type`: `control` | `transform` | `lambda` | `data_only` | `mixed`
* `notes`

Recommended call annotations:

* `one_shot: true`
* `iteration: <text>`
* `condition: <text>`

Minimal YAML serialization:

```yaml
modules:
  - id: M0
    name: updateRegistry
    type: control

  - id: M1
    name: transactionTemplate.execute
    type: control

  - id: L0
    name: TxBody
    type: lambda

  - id: M2
    name: violationsRegistriesService.updateViolationsRegistry
    type: control

  - id: L1
    name: updateRow
    type: lambda

  - id: E0
    name: UpdateRowClosureEnv
    type: data_only

control_calls:
  - from: M0
    to: M1

  - from: M1
    to: L0

  - from: L0
    to: M2

  - from: M2
    to: L1
    iteration: "for each row in currentRegistryVersion.rows"

data_couples:
  - from: L0
    to: M2
    items: [currentRegistryVersion, updateRow]

  - from: E0
    to: L1
    items: [settings, parsedCorrections, fileCorrectionMap]

lexical_inclusions:
  - outer: M0
    inner: L0
  - outer: M0
    inner: L1
```

Machine-checkable rules (minimum):

* all referenced module IDs exist;
* control graph is acyclic;
* each module has at most one control parent;
* couples reference existing modules.

---

### 2.5. Construction Algorithm

1. Establish boundary and root(s).
   Input: operation / system boundary statement.
   Output: root module(s) in `modules`.

2. Extract candidate modules.
   Input: code/design context.
   Operation:

* add a module for each named unit of work (function/method/service/module);
* add a module for each behavior parameter that is invoked (lambda/function parameter);
* optionally add a data-only module for shared environments that would otherwise be implicit.
  Output: populated `modules`.

3. Build the control hierarchy.
   Input: call/invocation structure.
   Operation:

* add `control_calls` for each conditioned transfer / invocation;
* for higher-order calls: add `control_call(receiver -> lambda_module)` where the receiver invokes the behavior.
  Output: acyclic `control_calls`.

4. Add lexical inclusion (orthogonal).
   Input: where code is physically defined.
   Operation:

* if a module is defined within another module’s lexical boundaries (lambda/local function), add `lexical_inclusions(outer -> inner)`.
  Output: `lexical_inclusions`.

5. Declare interfaces.
   Input: parameters/returns/flags/shared environment usage.
   Operation:

* add `data_couples` for explicit parameters and returned data across module boundaries;
* add `control_couples` for control flags/modes/signals crossing boundaries;
* if a dependency is “captured” (closure) or globally reachable, model it either as:

  * explicit `data_couples(outer_or_env -> consumer)`, or
  * a `data_only` module referenced by data couples.
    Output: explicit interface relations.

6. Annotate only the non-trivial procedural aspects.
   Input: known critical loops/one-shot/conditionals.
   Operation:

* attach annotations to relevant `control_calls` (iteration/condition/one_shot).
  Output: annotated calls without turning the chart into a flowchart.

7. Evaluate structural quality signals (from the artifact).
   Compute:

* fan-out (span of control) per module;
* fan-in per module;
* interface complexity = number of coupled items/signals per connection (approx);
* “control heaviness” markers: high fan-out + many control couples.
  Output: a list of design-review findings tied to specific modules/edges.

---

### 2.6. Typical Errors (anti-patterns)

1. “Lambda is invisible.”
   Detect: there is a behavior parameter that is invoked, but no module node exists for it.
   Highlight: hidden control transfer and hidden coupling.
   Auto-correct: introduce `module(type: lambda)` and `control_call(receiver -> lambda)`.

2. “Lambda has two parents.”
   Detect: lambda is placed under both the caller and the callee in the control tree.
   Highlight: confusion between control parent and lexical container.
   Auto-correct: keep a single control parent (the invoker); represent definition site with `lexical_inclusions`.

3. “Closure coupling is implicit.”
   Detect: lambda uses external values but there are no couples representing them.
   Highlight: implicit common-environment coupling.
   Auto-correct: add a `data_only` env module (or explicit `data_couples`) listing captured items.

4. “Control coupling via flags proliferates.”
   Detect: many `control_couples` or large `signals` sets on edges.
   Highlight: fragile structure and authority inversion risk.
   Auto-correct: split into distinct subordinates by mode, or refactor interfaces to data coupling.

5. “Pancake / excessive span of control.”
   Detect: very high fan-out at a coordinator.
   Highlight: missing intermediate levels or mixed responsibilities.
   Auto-correct: introduce intermediate coordinator modules guided by cohesion.

6. “Over-compression destroys fan-in.”
   Detect: eliminating a small atomic module with high fan-in causes duplication.
   Highlight: modularity loss and maintenance cost increase.
   Auto-correct: preserve the shared module; if runtime overhead is the concern, mark as definition-time inclusion / inlined segment (if applicable in the environment).

---

## 3. Skill spec: using “Structure Chart” by an AI agent

### 3.1. Usage Triggers

Use when the user is:

* decomposing an operation/system into modules;
* reviewing orchestration and coordination logic;
* refactoring call structure or boundaries;
* using higher-order functions (lambdas/function parameters) where behavior and data coupling become hard to see.

Do not use when the task is primarily:

* data schema design only;
* state machine/scenario modeling only;
* runtime debugging/tracing without structural change.

---

### 3.2. Questions to the User

Ask in this order:

1. What is the boundary and root module name for this chart (operation/system)?
2. Which invocations matter at design level (ignore trivial library calls, keep structural ones)?
3. Which behavior parameters are invoked (lambdas/function parameters)?
4. For each lambda: what external values does it capture (or should it be parameterized instead)?
5. Are there non-trivial loops/decisions/one-shot calls worth annotating?

Allowed as `TBD` without blocking:

* exact names of data items/signals (can be placeholders);
* whether an optimization should be “inlined” versus “subroutine” (can be deferred).

Blocking if missing:

* system/operation boundary;
* identification of invoked behavior parameters when they materially affect structure.

---

### 3.3. Quality Criteria

Good enough when:

* control hierarchy is acyclic and each module has ≤1 control parent;
* every invoked behavior parameter is a module node with an invocation edge;
* closure/shared-environment dependencies are explicit via data couples or data-only modules;
* fan-in/fan-out and interface complexity can be computed from the artifact.

Further work required when:

* lambdas capture large implicit environments;
* control coupling dominates interfaces;
* a coordinator has excessive fan-out without intermediate layers;
* multiple “meanings” are packed into a single low-cohesion module.

---

## 4. Workflow Integration

Use:

* after a behavioral view is stable enough (e.g., effects diagram / use cases) and before implementation details harden;
* during refactoring that changes coordination boundaries or introduces higher-order composition.

Output artifact:

* `concepts/structure-chart.md` (concept) and `structure-chart.yaml` per operation/system.

Feeds into:

* coupling/cohesion review;
* operation decomposition and implementation planning;
* detection of “hidden dependencies” caused by closures and shared state.

---

## 5. Sources and Attributions

Structured Design foundations used here:

* Structure charts as structural representation with optional procedural annotations for one-shot calls, loops, and conditional decisions. 
* Lexical inclusion is an explicit, separate relationship and must be represented independently of other relationships. 
* Fan-in/fan-out (span of control) as design-review signals; fan-in as designer responsibility. 
* Treatment of very small modules, fan-in trade-offs, and the option of in-line inclusion to avoid runtime overhead while preserving modularity.  
* Coupling/decoupling: converting implicit references into explicit ones as a decoupling method; common-environment coupling and localization.  
* Representing common environments explicitly (e.g., as a named “data-only” module) to avoid pathological clutter and to make shared dependencies visible. 
* “Inversion of authority” as a structural smell correlated with extra flags/switches (control coupling pressure). 

Structured Programming is treated as secondary background on composition/scale, and does not override the Structured Design choices above. 
