# Actions, Calculations, and Data

## 2. Concept spec: "Actions, Calculations, and Data"

### 2.1. Intention

The concept distinguishes three categories of behavior to enable mechanical reasoning about time- and repetition-sensitive code.
By classifying each unit as an **Action** (effectful operation), **Calculation** (pure operation), or **Data** (inert representation), the designer can separate “doing” from “thinking” and from “facts.”
This replaces ad-hoc judgment about whether a call is safe to repeat or reorder with a stable classification and a systematic refactoring direction (move logic from effectful operations → pure operations → inert data when possible).

In combination with other operation-shaping concepts:

- With **Command–Query Separation (CQS)**, **Commands** correspond to Actions (effectful operations) and **Queries** correspond to Calculations (pure operations).
  This makes explicit that queries must remain free of external side effects, while commands encapsulate all state changes.
- With **Balanced System Form**, the **afferent** and **efferent** branches correspond to Actions (effectful operations) and the **transform** branch corresponds to Calculations.
  Data flows between branches as inert representations, and the orchestrator coordinates by consuming data, invoking calculations, and then triggering effectful operations.

Measurable benefits include:

- Isolating environment-dependent behavior (Actions) so that the majority of logic becomes unit-testable without special setup.
- Reducing hidden side effects in read paths.
- Refactoring flows to expose plans/data for later execution.
- Improving API and system design reviews by making effectful code easy to locate.

### 2.2. Ontological Status

What it is: a code-and-design classification and refactoring lens that partitions behavior into three kinds using operational criteria.
It is a planning discipline that encourages producing plans as **Data** and **Calculations** that emit those plans, with **Actions** (a.k.a. effectful operations) executing them.

What it is not: a full architecture style, a type-system technique, or a definition of functional programming.
It does not eliminate actions, only isolates and minimizes them.
It does not decide module boundaries or persistence strategies.

Operational distinction:

- **Action** (a.k.a. effectful operation): a unit whose externally observable outcome depends on when it runs or how many times it runs.
  Actions perform I/O, access shared mutable state, read the current time, use randomness, or rely on any implicit input.
  They may include internal calculations, but they are classified by their dependence on time/repetition and side effects.
- **Calculation** (a.k.a. pure operation): a unit that deterministically maps explicit inputs to outputs and performs no externally observable effects.
  Its result can replace the call itself without changing program behavior.
- **Data**: an inert representation of facts/values.
  It cannot be “run”.
  It may be stored, transmitted, or compared structurally.
  It is meaningful without execution.

Scope boundaries / non-goals:
The concept does not prescribe immutability mechanisms, concurrency models, transaction handling, error handling, module layering, or domain modeling.
It does not attempt to remove Actions.
Rather, it defines a direction for moving logic out of them.

### 2.3. Concept Invariants

Invariant 1 — Total classification.
- Statement: Every relevant unit of behavior (function/module step) is classifiable as an Action, Calculation, or Data.
- Verification: for each unit apply the operational criteria above; reviewers should reach the same classification given the same observable signals.
- Falsified by: classification based primarily on naming/style preferences rather than observable dependence on time/repetition/effects/inertness.

Invariant 2 — Actions depend on time or repetition.
- Statement: A unit is an Action if its externally observable outcome changes when run at different times or repeated.
- Verification: identify at least one implicit input or side effect (reading/writing shared state, I/O, system time, randomness, network or database state at call time).
- Falsified by: an allegedly effectful operation that is fully determined by explicit inputs and has no externally observable effects.

Invariant 3 — Calculations are referentially transparent.
- Statement: For the same explicit inputs, the output is identical; repeated calls are safe and do not change external state.
- Verification: replacing the call by its result does not change behavior; the unit reads no implicit inputs and writes no implicit outputs.
- Falsified by: output varies across calls for the same inputs; or the unit reads global mutable state, performs I/O, or mutates externally visible state.

Invariant 4 — Data is inert.
- Statement: A representation is Data if it cannot be “executed” to produce effects and can be stored/transmitted/compared without running code.
- Verification: data can be inspected or serialized without causing effects; multiple consumers can interpret it.
- Falsified by: a value that triggers effects when inspected or contains embedded callbacks/closures that drive side effects.

Invariant 5 — Effectful behavior spreads unless isolated.
- Statement: If a function calls an Action (directly or indirectly), it inherits action constraints.
  It must be treated as an Action unless all effectful calls are isolated behind explicit extraction boundaries.
- Verification: examine call graphs; functions that transitively depend on an Action are labeled as Actions, or refactored to extract effectful parts.
- Falsified by: treating a function that calls effectful code as a pure Calculation.

Invariant 6 — Refactoring moves logic toward Data and Calculations.
- Statement: Where possible, convert implicit inputs to explicit parameters and implicit outputs to return values or plans (Data).
  Extract Calculations from Actions and move decisions into Data.
- Verification: new features show stable interfaces where decisions/plans are produced as values and executed separately; effectful code is thin.
- Falsified by: business rules implemented primarily inside Actions with hidden environment coupling.

Variants / profiles (to handle borderline cases)

Variant A — Conservative (safety-first).
- Definition: any read of shared mutable state or local mutation qualifies the unit as an Action.
- Use when: concurrency/timing bugs are costly.

Variant B — Boundary-focused (pragmatic).
- Definition: local mutation is allowed in Calculations if it is not externally observable and fully contained; reads of immutable caches are allowed.
- Use when: performance requires local mutation but leakage can be prevented.

Common across variants:
- Invariants 1–6 remain unchanged.
  Variant choice only affects the treatment of local mutation and shared state reads.

### 2.4. Minimal Formalization

Vocabulary mode (minimal terms)

- **Action (effectful operation):** behavior whose externally observable outcome depends on when or how many times it runs (implicit input/output; side effects).
- **Calculation (pure operation):** deterministic transformation of explicit inputs to outputs with no externally observable effects.
- **Data:** inert representation of facts/values; not executable.
- **Explicit input:** information provided via parameters or explicit dependency injection.
- **Implicit input:** information read without explicit declaration (globals, ambient context, system time, randomness, environment variables).
- **Explicit output:** declared return value(s) of a unit.
- **Implicit output:** externally observable effect not represented as a return value (writes to state, I/O, events).
- **Plan:** data describing intended future actions (e.g., “list of emails to send”) produced by calculations and executed by actions.

### 2.5. Construction Algorithm

1. Select scope.
   - Input: code region and runtime context.
   - Output: list of units (functions/blocks/steps) to classify.

2. Enumerate dependencies and effects.
   - For each unit, record implicit inputs (e.g., global state, system time), implicit outputs (state changes, I/O), explicit inputs, and explicit outputs.
   - Output: per-unit checklist of dependencies/effects.

3. Classify units.
   - Apply the operational criteria to label each unit as Action (effectful operation), Calculation (pure operation), or Data.
   - Provide a one-line justification based on time/repetition dependence, determinism, and inertness.
   - Output: classification map.

4. Isolate effectful operations.
   - Designate a minimal set of Actions as effectful boundaries.
   - Functions that call effectful operations are treated as Actions unless effectful code is extracted.
   - Output: list of Action boundaries.

5. Extract calculations from actions.
   - For each Action that contains both effectful and deterministic logic, convert implicit inputs into explicit parameters and implicit outputs into return values.
   - Move deterministic logic into separate Calculations.
   - Output: new Calculation functions; Action rewritten to gather inputs, call Calculations, and perform effects.

6. Convert decisions into plans as data.
   - When an Action interleaves decision logic and effects, extract the decision logic into a Calculation that returns a plan (Data).
   - The Action then executes the plan.
   - Output: plan-producing Calculations and plan-executing Actions.

7. Record and review.
   - Maintain an artifact (table or notes) containing classification, action boundaries, extracted calculations, and chosen variant profile.
   - Use this artifact to drive refactoring and to check classification consistency.

### 2.6. Typical Errors (anti-patterns)

1. **“Everything is an action”:** logic is embedded in effectful operations; tests require full environment setup.
   - Detect: functions perform multiple implicit reads/writes; calculations are not extracted.
   - Highlight: separate decision logic and data production into pure functions; minimize effectful operations.
   - Auto-correct: extract deterministic sub-logic into pure functions; return plans or values instead of performing effects inline.

2. **Hidden actions inside “calculations”:** a unit classified as Calculation reads current time, global mutable state, random, or performs I/O.
   - Detect: unexpected dependence on environment; non-repeatable results.
   - Highlight: convert implicit inputs to explicit parameters; move I/O to effectful operation boundaries.
   - Auto-correct: refactor to accept dependencies explicitly and relocate side effects.

3. **Treating data as executable:** data structures contain callbacks that trigger effects during interpretation.
   - Detect: inspecting or deserializing data triggers actions; data cannot be safely serialized/compared.
   - Highlight: separate code from data; use declarative tags instead of embedded callbacks.
   - Auto-correct: replace executable fields with declarative markers; interpret at effectful boundaries.

4. **Interleaving planning and execution:** an Action both decides and performs effects in a single loop.
   - Detect: decision logic and side effects intermingle; partial failure handling is hard.
   - Highlight: inability to test decisions independently; poor failure semantics.
   - Auto-correct: two-phase approach—first produce a plan (Data) via a Calculation; then execute the plan via an Action.

5. **Over-fragmentation without stable boundaries:** too many micro-calculations without clear effectful boundaries or vocabulary.
   - Detect: classification disagreement among reviewers; drift over time.
   - Highlight: need for minimal vocabulary and consistent boundaries.
   - Auto-correct: reintroduce stable boundaries; enforce vocabulary and classification consistency.

6. **Misapplying local mutation rule:** local mutation leaks via shared references, making outputs depend on call ordering.
   - Detect: side effects become externally observable; calculations behave differently depending on call order.
   - Highlight: classification must reflect leakage; treat as Action if leakage cannot be prevented.
   - Auto-correct: enforce copy-on-write/defensive copying; restrict sharing; reclassify as Action where appropriate.

### 2.7. Links

- EA principles: `../conventions/ea-principles.md` (EA.F1).
- Checklist: `../checklists/operations.md`.
- Related concept: `../concepts/command-query-separation.md`.
- Related concept: `../concepts/balanced-system-form.md`.

## 3. Sources and Attributions

### 3.1. Sources

- Eric Normand, *Grokking Simplicity: Taming complex software with functional thinking*, Manning, 2021.
  Primary material: Chapters 1–5 describing “actions, calculations and data” and refactoring patterns.

### 3.2. Direct Borrowings

- The tri-part distinction among actions, calculations, and data.
- Criteria for actions: dependence on “when/how many times,” presence of implicit inputs/outputs, and side effects.
- Criteria for calculations: referential transparency, deterministic mapping from inputs to outputs, absence of side effects.
- Criteria for data: inert representation of values/facts.
- Observation that effectful behavior spreads through call graphs unless isolated, motivating extraction of calculations from actions.
- Refactoring direction: convert implicit inputs/outputs into explicit ones and move logic toward data and calculations.

### 3.3. Synthesized Elements

- Introduction of **Effectful Operation** and **Pure Operation** aliases to align with frameworks that use the term “operation.”
- Explicit variant profile (Conservative vs Boundary-focused) to handle borderline cases (local mutation and shared state reads).
- Construction algorithm unifying classification, boundary isolation, calculation extraction, plan production, and record keeping.
- Anti-pattern catalog expressed in detect/highlight/auto-correct format.
- Interoperation notes with **Command–Query Separation** and **Balanced System Form**, clarifying how actions map to commands and afferent/efferent branches, and calculations map to queries and transform branches.

### 3.4. Discrepancies and Resolutions

- **Local mutation vs purity:** some sources allow mutation in “calculations” if it is not externally observable.
  Others classify any mutation as an Action.
  Resolved by defining profile A (conservative) and profile B (boundary-focused) and stating selection criteria.
- **Terminology drift (Action vs Operation):** resolved by introducing the alias “Effectful Operation” for Action and “Pure Operation” for Calculation.
  Definitions are explicit to prevent confusion with broader meanings of “operation” in other frameworks.
- **Scope overlap with CQS and Balanced System Form:** the concept clarifies that commands correspond to effectful operations and queries correspond to calculations.
  It also clarifies that the Balanced System Form’s afferent/efferent and transform branches align with actions and calculations respectively.
