# Command–Query Separation (CQS)

## 2. Concept spec: "Command–Query Separation (CQS)"

### 2.1. Intention

CQS is used to make an API mechanically readable: from a name/signature/contract a reader (or tool) can infer whether calling an operation can change the observable state of the object/system.

It replaces repeated manual reasoning about call safety (reordering, repetition, use inside assertions, use in logging/diagnostics).

It provides measurable benefit in tasks such as: API design reviews, refactoring for testability, preventing “diagnostics that mutate”, strengthening contracts, and reducing hidden side effects in read paths.

### 2.2. Ontological Status

What it is: a design principle and contract discipline for class/service operations (routines/methods/features) that partitions them into two categories with non-overlapping obligations.

What it is not:
- Not CQRS: CQS is an operation-level semantic rule; CQRS is a broader architectural separation of read and write models/paths.
- Not a general prohibition of mutation: mutation is allowed (via commands).
- Not a transport rule (e.g., “HTTP GET is always a query”): transports may align, but CQS is defined by semantics, not verbs.

Operational rule to distinguish “similar but not the same”:
- If, for an operation treated as a *query*, it is acceptable that calling it can change the value of any *non-secret query* (i.e., the observable state as seen through the API), then the API is not applying CQS.
- If the “separation” is expressed only as “different endpoints/models for reads vs writes” while individual operations are still allowed to mix “change + return a read projection of state” as a normal pattern, that is a CQRS-style separation, not CQS.

Scope boundaries / non-goals:
- CQS does not prescribe persistence strategy, transaction boundaries, concurrency model, or system-level read/write topology.
- CQS does not guarantee determinism of queries; it constrains self-induced observable state change, not time-varying answers.

Interoperation with Balanced System Form (operation-level morphology)

When used together with Balanced System Form:

* At a chosen operation abstraction level, branch-root obligations typically align as:
  * afferent roots are queries,
  * transform roots are queries (pure calculation),
  * efferent roots are commands,
  * an orchestrator may be a query (read operation) or a command (write operation).
* A strong (optional) discipline is the “Read-before-Transform, Write-after” rule of thumb: complete reads before the pure calculation; perform writes after the calculation.

### 2.3. Concept Invariants

Invariant 1 — Total classification of operations.
- Statement: Every operation in the target API surface is classified as either a Command or a Query.
- Verification: a reviewable inventory exists (interface list, module API list, annotations, or enforced naming + lint rules) where each operation is tagged as Command or Query.
- Falsified by: operations with ambiguous semantics at call sites; operations whose category can only be inferred by reading deep implementation.

Invariant 2 — Queries do not produce abstract side effects.
- Statement: A Query must not change the observable state of the object/system as exposed by non-secret queries.
- Verification:
  - contract/tests: for a stable environment and without intervening commands, repeating a query does not change the results of any non-secret query;
  - architecture/lint: query paths forbid writes to domain state and forbid emitting domain-significant external effects.
- Falsified by: “get/find/calculate” operations that modify business flags, persist changes, emit domain events/messages, advance workflows, or otherwise change non-secret query results.

Invariant 3 — Commands may change state but are not used to return domain information.
- Statement: A Command exists to change state and/or trigger domain-significant external effects.
  It may return an acknowledgment payload (profile-dependent) and *generated result data* (e.g., new ids, created timestamps, server-assigned defaults, revision/version).
  It must not return arbitrary domain projections as a substitute for a Query of the system’s state.
- Verification: signatures return either nothing, a control-result, or a generated-result payload.
  API review finds no “update-and-return-read-model” patterns where the returned data is used as a read API for existing state.
- Falsified by: commands used to fetch/return domain information that should be obtained via queries (e.g., “update-and-return-snapshot” for caller convenience).

Invariant 4 — No mixed routine semantics (beyond generated results) in the baseline API.
- Statement: A single operation is not simultaneously treated as both a Command and a Query.
  Commands may return generated result data, but they do not serve as queries for reading state.
- Verification: inventory shows no operations with both roles; any known exceptions are isolated (see variants) and recorded.
- Falsified by: “pop()”-style APIs (remove + return removed element) treated as normal design across the API surface.

Variants / profiles

Profile A — Meyer-compatible CQS (abstract-state rule).
- Definition: Queries are allowed to produce *concrete-only* internal changes provided they do not change any non-secret query result (no abstract side effects).
- Use when: you need practical freedom for internal caching, representation preparation, cursor movement with restoration, and other hidden mechanics.

Profile B — Strict observational CQS.
- Definition: Queries produce no externally observable side effects of any kind (including internal state changes detectable by any non-secret query, now or later); they are safe for “diagnostics/observations”.
- Use when: you want maximal safety for debugging, logging, metrics extraction, and assertions, and you can centralize caching/telemetry outside queries.

Profile C — CQS with result-returning commands.
- Definition: Same as Profile A or B for queries.
  Commands may return a *control result* and/or *generated result data* (ids, timestamps, defaults, revision/version), while still not acting as a read API for existing domain state.
- Use when: you need return-based outcomes and/or you want the command to return server-generated data needed by the caller.

Common vs variant-specific
- Common invariants: 1, 2, 4.
- Variant-specific: whether queries may change internal state (A allows concrete-only; B forbids); whether commands may return a result payload (C allows).

Selection criteria
- Prefer Profile A when internal caching/representation preparation is important and you can precisely define “observable state” via non-secret queries.
- Prefer Profile B when you want to treat queries as “diagnostic-safe reads” and can enforce that in code.
- Prefer Profile C when the layer needs return-based outcomes and/or needs server-generated data returned by commands, and you can keep the payload from becoming a read API for existing domain state.

### 2.4. Minimal Formalization (Vocabulary mode)

Command: an operation whose primary purpose is to change state and/or trigger domain-significant external effects.

Query: an operation whose primary purpose is to return information; it must not produce abstract side effects.

Observable state: the set of facts about an object/system that can be observed through non-secret queries in the target API surface.

Concrete state: internal representation details that may change without changing observable state.

Concrete side effect: an internal state change performed during evaluation of a query.

Abstract side effect: a concrete side effect that changes the value of at least one non-secret query.

Non-secret query: any query visible to at least one client outside the implementation boundary (including selectively exported queries).

Control result: a return value that communicates only execution outcome (success/failure/validation errors/correlation id) and does not embed domain data.

Generated result data: data produced by executing a command that was not available to the caller before the call.
Examples: new identifiers, creation timestamp, server-assigned defaults, or a new revision/version/etag.
Non-example: returning a read projection of existing domain state for caller convenience.

Mixed operation: a single operation that both changes observable state and returns a read projection of domain state in the same call (beyond generated result data).

### 2.5. Construction Algorithm

1) Define the target API surface.
- Input: boundary definition (package/module/service interface/controller endpoints).
- Output: operation list with name, signature, and intended clients.

2) Declare the CQS profile.
- Input: layer constraints (performance, caching, observability, error signaling conventions).
- Output: chosen profile (A/B/C) and a written policy of what queries/commands may return/do.

3) Classify operations.
- Input: operation list and intended behavior.
- Output: each operation tagged Command or Query, with rationale based on observable effects.

4) Enforce Query contracts.
- Input: query implementations.
- Output: evidence that queries do not produce abstract side effects:
  - tests asserting no change in non-secret query results after query-only sequences,
  - or architectural rules forbidding writes/domain emissions on query paths,
  - and an explicit definition of what counts as observable state for the layer.

5) Refactor mixed operations.
- Input: operations that both mutate and return a read projection of state.
- Output: either:
  - split into `CommandX()` + `QueryX()` with updated call sites; or
  - record as an exception with a stated reason (atomicity/concurrency semantics), plus containment rules and tests.

6) Enforce Command result policy.
- Input: command implementations.
- Output: commands do not act as read APIs for existing state.
  Commands may return only acknowledgment and generated result data (profile-dependent).

7) Add automated checks.
- Input: build/tooling.
- Output: lint/architecture tests or code-review checklist items mapping to invariants 1–4 and chosen profile.

### 2.6. Typical Errors (anti-patterns)

1) “Read that writes” (query with abstract side effect).
- Detect: query call causes changes visible via any non-secret query; or emits domain-significant effects.
- Highlight: “This query changes observable state; split into command + query or redesign.”
- Auto-correctable: sometimes by reclassifying and renaming to a command; otherwise requires refactor.

2) “Command returning a snapshot”.
- Detect: command returns an entity/projection/value object that is used as a read API for existing state (beyond generated result data).
- Highlight: “Mixes responsibilities; callers start depending on command-as-read, which weakens query contracts and hides read semantics.”
- Auto-correctable: split into command + follow-up query.
  If atomicity is required, record an exception and constrain it with explicit containment rules and tests.

3) “Hidden cursor advance / IO in a query” without an explicit two-step API.
- Detect: queries that implicitly advance input cursors, consume streams, or otherwise make subsequent reads differ.
- Highlight: “Observation changes what will be observed next; redesign as an explicit two-step API (advance command + current query).”
- Auto-correctable: often requires API split.

4) “Misclassified caching”.
- Detect: internal caching/representation preparation is treated as violation even when it cannot change any non-secret query.
- Highlight: “Concrete-only changes are allowed in Profile A; validate against abstract side effect definition.”
- Auto-correctable: clarify profile and observable state definition.

5) “Profile drift”.
- Detect: queries gradually accumulate effects that contradict the declared profile.
- Highlight: “The layer no longer matches its chosen profile; re-establish constraints.”
- Auto-correctable: move effects behind standardized interceptors/decorators consistent with the profile.

### 2.7. Links

- EA principles: `../conventions/ea-principles.md` (EA.F7).
- Checklist: `../checklists/api-design.md`.
- Skill: `../skills/api-design-cqs/SKILL.md`.
- Related concept: `../concepts/balanced-system-form.md`.
- Related concept: `../concepts/actions-calculations-data.md`.

## 3. Sources and Attributions

### 3.1. Sources

- Bertrand Meyer, Object-Oriented Software Construction (2nd edition), Prentice Hall, 1997.
  Chapter 23 (principles of class design), section on side effects in functions and the Command-Query Separation principle; plus glossary/definitions appendix.
- Bertrand Meyer, Eiffel: The Language (historical attribution and original formulation context).
- Martin Fowler, “CommandQuerySeparation” (Bliki).
- Wikipedia, “Command–query separation”.
- Martin Fowler, “CQRS” (Bliki) for the relationship and non-equivalence between CQS and CQRS.

### 3.2. Direct Borrowings

- The shorthand statement “asking a question should not change the answer” as an informal restatement of the principle.
- The “pop” example as a canonical illustration of a mixed routine.
- The use of “observable state” as a framing for what queries must not change.

### 3.3. Synthesized Elements

- The profile/variant structure (Meyer-compatible vs stricter observational profiles; optional control-result commands) as an operationalization for heterogeneous language ecosystems.
- The construction algorithm and verification obligations (inventory, profile selection, refactor steps, automated checks).
- The explicit vocabulary that aligns “abstract side effect” with “observable state through non-secret queries”.

### 3.4. Discrepancies and Resolutions

- Strictness of side-effect prohibition in queries: resolved by defining Profile A (no abstract side effects) and Profile B (no observable effects at all).
- Command return values: resolved by allowing Profile C (control-result and/or generated-result) as a compatibility profile while preserving “no domain information returned by commands”.
- Mixed operations required for atomicity: resolved by requiring explicit exception recording and containment tests rather than weakening baseline invariants.
