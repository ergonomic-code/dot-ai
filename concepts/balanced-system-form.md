# Balanced System Form

## 2. Concept spec: "Balanced System Form"

### 2.1. Intention

Balanced System Form is used to make operation implementations mechanically readable at a higher abstraction level:

* Raise the abstraction level of operation code by splitting it into named sub-operations with clear roles (read / transform / write).
* Make it easier to track the effects of an operation by confining effects to explicit, role-typed sub-operations.
* Make it easier to control and review that the same data is not read from the database multiple times within one operation (reads are gathered and localized).
* Provide a stable pattern for separating I/O (DB/network/files/etc.) from business transformations.
* Increase the degree of I/O packaging (batching/coalescing reads and writes) to improve efficiency (fewer round-trips, higher throughput).

Optional additional benefit (when relevant): localize the impact of physical/device/format changes.

### 2.2. Ontological Status

* What it is:
  * A morphology constraint on an operation’s call hierarchy (or dependency graph) aligned with a 3-phase flow: **Afferent (Read)** → **Transform (Calculate)** → **Efferent (Write)**, with a **Coordinator (Orchestrator)** at the top of that operation.
  * A role discipline that can be applied fractally: a complex sub-operation may itself be structured as a smaller balanced operation.
* What it is not:
  * Not a complete architecture style (it does not prescribe layering names, deployment topology, DI usage, persistence strategy).
  * Not “make it symmetric visually”.
  * Not a generic command/query rule for all APIs.
    However, when applied to a chosen abstraction level, it implies CQS-style obligations for the **roots of the branches** (see below).
* Operational rule to distinguish “similar but not the same”:
  * A system is **not** in balanced form (at the chosen abstraction level) if any **Transform sub-operation invoked by the operation orchestrator** performs I/O or requires physical/format-shaped data at its public boundary.
  * Note: I/O branches may contain local transformation blocks that operate on physical representations; this does not violate balanced form as long as those transforms remain confined within the I/O branches.
* Scope boundaries / non-goals:
  * This concept is defined “per operation (or per use-case handler)”.
    It may be applied at module/service level, but its primary target is the shape of complex operations.
  * It does not decide *what* the domain model is.

CQS-aligned semantics at one abstraction level (branch-root obligations)

When balanced form is applied to a given operation abstraction level:

1) The **operation orchestrator** may be a command or a query (it depends on the operation’s intent).
2) Every **afferent branch root** (if any) **must be a query**.
3) Every **transform branch root** (if any) **must be a query** (functionally pure calculation).
4) Every **efferent branch root** (if any) **must be a command**.

There may be multiple branches of each kind.
Those branch roots may themselves be orchestrators at their own (lower) abstraction level.

### 2.3. Concept Invariants

Invariant 1 — Role partition is explicit.
* Statement: At the chosen abstraction level, each direct child sub-operation of an operation orchestrator is classifiable by primary role as one of:
  * **Coordinate**: sequencing/branching/wiring.
  * **Afferent (Read)**: obtain and refine inputs upward.
  * **Transform (Calculate)**: compute logical outputs from logical inputs.
  * **Efferent (Write)**: refine outputs downward and perform writes/outputs.
* Verification: a reviewable inventory/diagram exists (structure chart, call graph, package/module boundaries) where modules are labeled with one primary role.
* Falsifier: role mixing is pervasive such that classification is ambiguous.

Invariant 2 — Branch-root CQS obligations hold at the chosen abstraction level.
* Statement: For an operation orchestrator:
  * every afferent branch root is a query;
  * every transform branch root is a query;
  * every efferent branch root is a command;
  * the orchestrator itself may be a command or a query.
* Verification: public signatures/contracts (and call sites) treat those roots accordingly (queries used in read contexts; commands used for effects).
* Falsifier: an afferent root performs writes as part of its primary behavior; an efferent root is used as a read API; a transform root is stateful/impure.

Invariant 3 — Transform sub-operations invoked by the orchestrator are functionally pure.
* Statement: Transform sub-operations (invoked by the operation orchestrator) are referentially transparent with respect to the operation’s observable behavior: outputs are determined solely by explicit inputs.
  They perform no I/O and do not mutate domain state in-place.
  They may use *secret (concrete-only) state* (e.g., caches) provided it cannot change the value of any non-secret query.
* Verification:
  * dependency rules: no imports/calls to I/O resources from transform modules;
  * architecture rules: no writes to domain state/persistence from transform modules;
  * tests/analysis: for the same explicit inputs (under declared environment assumptions), outputs are stable under repeated evaluation.
* Falsifier:
  * transform reads time/random/global mutable state as an implicit input;
  * transform writes domain state/persistence;
  * secret state can change observable results (directly or indirectly).

Invariant 4 — I/O is confined to I/O branches (with local transforms allowed).
* Statement: I/O (DB/network/files/etc.) occurs in afferent/efferent branches.
  Those branches may include local transformation blocks that operate on physical representations, but such transforms are confined within the branch and do not become orchestrator-invoked transform sub-operations.
* Verification: I/O calls are reachable only within afferent/efferent subgraphs; orchestrator-invoked transforms depend only on logical data.
* Falsifier: any orchestrator-invoked transform performs I/O or takes physical/format-shaped data.

Invariant 5 — The morphology is applicable fractally.
* Statement: If a sub-operation grows complex, it may be re-expressed as its own balanced operation, such that its parent sees it as a single role-typed sub-operation (read query / transform query / write command).
* Verification: decomposition boundaries exist where complex sub-operations become orchestrators with their own read/transform/write internals.
* Falsifier: complexity growth forces pulling reads/writes back into the parent orchestrator’s transforms.

Variants / profiles

Profile A — Minimal Balanced (role visibility).
* Common invariants: 1–4.
* Additional constraint: none.

Profile B — Fractal Balanced Operations.
* Common invariants: 1–5.
* Use when: operations are large and you want repeatable decomposition rules across levels.

Recommended discipline (strong, not mandatory): “Read-before-Transform, Write-after” (Recawr Sandwich).
* Rule of thumb: collect all required reads before invoking the pure transform; perform writes only after the transform returns.
* Status: not an invariant; violations are allowed but should be explicit exceptions.

### 2.4. Minimal Formalization

Vocabulary mode (minimal terms)

* Operation orchestrator: the top-level coordinator for a (use-case) operation at the chosen abstraction level.
* Afferent branch root: the topmost sub-operation that belongs to the read/ingress side for that orchestrator.
* Transform branch root: a topmost calculation sub-operation invoked by the orchestrator (there may be several).
* Efferent branch root: the topmost sub-operation that belongs to the write/egress side for that orchestrator.
* Physical data: data shaped by a device/transport/storage/format.
* Logical data: normalized/edited data independent of physical representation.
* Secret (concrete-only) state: internal representation state that may change without changing observable behavior (e.g., caches that cannot influence any non-secret query result).
* I/O-local transform: a transformation block inside an afferent/efferent branch that may operate on physical data and remains confined within that branch.
* I/O packaging: deliberate batching/coalescing of reads and/or writes (e.g., fewer DB round-trips; bulk reads; bulk writes).

### 2.5. Construction Algorithm

1. Define the operation boundary and its orchestrator.
   * Input: a use-case / endpoint / message handler / scheduled job.
   * Output: an explicit “operation orchestrator” definition.

2. Identify all external reads and writes required by the operation.
   * Input: operation requirements.
   * Output: a list of reads (sources) and writes (sinks).

3. Define logical contracts for the orchestrator↔branches boundary.
   * Input: read/write list.
   * Output: logical input bundle(s) for transforms and logical output bundle(s) from transforms.

4. Build afferent sub-operations (queries).
   * Input: each required read.
   * Output: afferent branch roots as queries that return logical data (may internally include I/O-local transforms).
   * Default optimization output: packaged reads (batch/coalesce) where applicable.

5. Build transform sub-operations (queries).
   * Input: logical input bundle(s).
   * Output: transform branch root(s) as pure calculations returning:
     * logical outputs, and optionally
     * “result-as-data” for effects (state deltas / events / effect-commands to execute).

6. Build efferent sub-operations (commands).
   * Input: logical outputs and/or effect-commands.
   * Output: efferent branch roots as commands that perform writes (may internally include I/O-local transforms).
   * Default optimization output: packaged writes (batch/coalesce) where applicable.

7. Compose in the orchestrator.
   * Input: afferent queries, transform query(ies), efferent commands.
   * Output: orchestrator implementation that calls: reads (queries) → transform(s) (pure) → writes (commands).

8. Apply the “Read-before-Transform, Write-after” discipline by default.
   * Input: orchestrator implementation.
   * Output: evidence in code/structure that all reads are completed before transforms and all writes happen after transforms.
   * Exception handling output: if violating this rule, record an explicit exception (reason + containment tests).

9. Apply fractal decomposition where needed.
   * Input: any sub-operation that grows complex.
   * Output: that sub-operation becomes its own orchestrator, while the parent continues to see it as a single role-typed child.

10. Add enforceable checks.
   * Input: module boundaries / build tooling.
   * Output: architecture tests/lints that enforce:
     * no I/O in orchestrator-invoked transforms;
     * branch-root CQS obligations;
     * optional: recawr discipline (no reads after transforms; no writes before transforms).

### 2.6. Typical Errors (anti-patterns)

1. “Transform does I/O.”
* Detect: orchestrator-invoked transform imports/calls DB/network/files.
* Highlight: “Move I/O to afferent/efferent; keep orchestrator-invoked transforms pure.”
* Auto-correct: extract into afferent/efferent sub-operations.

2. “Reads scattered through the operation.”
* Detect: multiple reads interleaved with transformations; the same data re-read.
* Highlight: “Harder effect tracking; harder to review duplicate reads; violates default recawr discipline.”
* Auto-correct: pull reads up into afferent queries; pass results into transforms.

3. “Writes occur before the operation’s main transform.”
* Detect: early writes/side effects before the calculation is completed.
* Highlight: “Complicates reasoning; increases rollback/compensation needs.”
* Auto-correct: defer writes to efferent commands after transforms; if unavoidable, record an explicit exception.

4. “Afferent root performs writes.”
* Detect: read sub-operation changes persistent state.
* Highlight: “Breaks branch-root obligations; hides effects inside reads.”
* Auto-correct: split into query + command; keep the afferent root query-only.

5. “Efferent root used as a read API.”
* Detect: callers rely on command return payload as a read projection of existing state.
* Highlight: “Command-as-read coupling; weakens query contracts.”
* Auto-correct: split into command + query; constrain exceptions.

6. “Under-packaged I/O.”
* Detect: a large number of small reads/writes where batching is available; repeated round-trips for adjacent data.
* Highlight: “Hurts efficiency; defeats the packaging intent.”
* Auto-correct: introduce packaged reads/writes at the afferent/efferent roots; keep transforms unchanged.

7. “Orchestrator becomes a monolith.”
* Detect: orchestrator contains substantial calculation logic or low-level I/O mechanics.
* Highlight: “Loses abstraction; loses role visibility.”
* Auto-correct: extract pure transforms and role-typed sub-operations.

### 2.7. Links

- EA principles: `../conventions/ea-principles.md` (EA.F6).
- Checklist: `../checklists/operations.md`.
- Related concept: `../concepts/command-query-separation.md`.
- Related concept: `../concepts/structure-chart.md`.
- Related concept: `../concepts/actions-calculations-data.md`.

## 3. Sources and Attributions

### 3.1. Sources

* Larry L. Constantine, Edward Yourdon, “Structured Design: Fundamentals of a Discipline of Computer Program and Systems Design” (2nd ed.).
  Sections 8.4–8.6 (afferent/efferent/transform/coordinate; morphologies) and transform analysis sections.
* Meilir Page-Jones, “The Practical Guide to Structured Systems Design” (1980).
  Section 8.3 (system shape), including balanced vs input/output-driven.
* Aleksey Zhidkov, “Структурный дизайн. Древний секрет простого и быстрого кода” (Nov 17, 2024).
  https://azhidkov.pro/posts/24/11/structured-design/
* Mark Seemann (ploeh), “Recawr Sandwich” (Jan 13, 2025).
  https://blog.ploeh.dk/2025/01/13/recawr-sandwich/

### 3.2. Direct Borrowings

* The afferent/transform/efferent/coordinate role vocabulary (paraphrased).
* The “balanced vs input/output-driven” framing (paraphrased).
* Allowing transformation/editing steps inside afferent/efferent branches (local transforms confined within the I/O branches) is consistent with the original structured design treatment of I/O refinement paths.
* The “read → calculate → write” sandwich specialization label (Recawr Sandwich) and its core role assignment.

### 3.3. Synthesized Elements

* Re-centering the concept’s intention on operation-level abstraction, effect tracing, and database-read control.
* Branch-root CQS obligations stated as an operational discipline at a chosen abstraction level.
* Explicitly highlighting I/O packaging (batching/coalescing) as a first-class intent enabled by the morphology.
* Fractal application rule for composing balanced operations.

### 3.4. Discrepancies and Resolutions

* Structured design literature focuses on system/module morphology; this concept specializes the idea to operation orchestration to support effect tracing, database-read control, and I/O packaging.
* Recawr Sandwich is framed as a strong rule of thumb, not a hard invariant; exceptions are allowed but must be explicit and contained.
