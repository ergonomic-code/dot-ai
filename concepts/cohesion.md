## Concept spec: "Cohesion"

### 2.1. Intention
Cohesion is used to judge whether a single subprogram groups together work that belongs together.
It standardizes decisions such as whether a method or function should stay intact, be split, have a helper extracted, move an effect outward, or be replaced by dispatch or composition.
It reduces ambiguity in code review, refactoring, code generation, and maintenance by giving an operational answer to the question: "Is this one routine doing one problem-related job, or merely accumulating nearby work?"
It is especially useful for modern codebases with mixed styles such as OO methods, top-level functions, local functions, pipeline stages, async procedures, and AI-generated routines, where the absence of a shared class model does not remove the need for stable subprogram boundaries.

### 2.2. Ontological Status
Cohesion is a design principle and an analysis lens for a single subprogram.
In this concept, a subprogram means a method, function, procedure, local function, or equivalent callable unit.
Cohesion is not a complexity metric.
Cohesion is not coupling.
Cohesion is not class cohesion or package cohesion.
Cohesion is not purity.
A subprogram may be cohesive and still contain branching, iteration, mutation, or side effects, as long as those elements are all required for one problem-related responsibility.

Operational distinction rules.
A complexity metric answers: "How hard is this control flow to read or reason about?"
Cohesion answers: "Do the internal steps of this subprogram belong to one responsibility?"
Level of abstraction answers: "Are those steps expressed within one dominant vocabulary and one local narrative level?"
A routine may be low in complexity and still have low cohesion if it bundles unrelated work.
A routine may be non-trivial in complexity and still be highly cohesive if all of its steps are essential to one responsibility.

Scope boundaries and non-goals.
This concept applies at subprogram scope only.
It does not define how to evaluate cohesion of classes, packages, services, or bounded contexts.
It does not require one-line functions, extreme extraction, or maximal fragmentation.
It does not require removal of every auxiliary step, only of steps that are not essential to the same responsibility.

### 2.3. Concept Invariants

#### Invariant 1. Cohesion is about relatedness of steps within one subprogram
A cohesion judgment is valid only when the unit of judgment is one concrete subprogram and the question is whether its significant steps belong to the same responsibility.

Verifiable by:
- identifying one concrete callable unit;
- enumerating its significant internal steps;
- judging the relationship among those steps.

Falsified by:
- judging a class, package, or workflow instead of a single callable unit;
- treating naming style alone as the entire evaluation;
- evaluating only one fragment of the routine while ignoring the rest.

#### Invariant 2. High cohesion means one primary problem-related responsibility
A highly cohesive subprogram performs one responsibility to completion, including only those supporting steps that are essential to that responsibility.

Verifiable by:
- describing the subprogram with one precise verb-object responsibility statement;
- showing that all major steps either realize that responsibility directly or are indispensable support for it;
- confirming that callers invoke it for one purpose rather than several unrelated ones.

Falsified by:
- a responsibility statement that requires "and", "or", "then", "before", or "after" to remain accurate;
- major internal steps that exist for different business intentions;
- call sites that rely on the same routine for materially different jobs.

#### Invariant 3. Sequence alone is not enough
Merely executing steps in one order does not establish high cohesion by itself.
Sequential cohesion is valid when that step-to-step flow is intrinsic to completing one responsibility.

Verifiable by:
- showing that the order exists because intermediate results or required effects form one responsibility chain;
- showing that extraction or rearrangement would damage one responsibility rather than just one sequence.

Falsified by:
- "startup", "cleanup", "before X", "after X" being the strongest relationship present;
- grouping steps only because they happen in the same execution phase.

#### Invariant 4. Shared data alone is not enough
Several operations on the same record, DTO, request, or entity do not become highly cohesive merely because they touch the same data.
Communicational cohesion is valid when coordinated work on that shared data is intrinsic to completing one responsibility.

Verifiable by:
- showing that the shared data is the medium of one responsibility;
- showing that each operation contributes to one result or semantic effect.

Falsified by:
- a routine that formats, validates, persists, logs, and emits notifications for the same object without one responsibility binding those actions.

#### Invariant 5. Side effects are acceptable only when they are intrinsic to the responsibility
A side effect does not reduce cohesion if it is part of completing the responsibility itself.
An incidental side effect does reduce cohesion.

Verifiable by:
- identifying the essential effect boundary of the subprogram;
- showing that mutation, persistence, emission, or I/O is required for the responsibility named for the routine.

Falsified by:
- mixing core calculation with optional logging, metrics, tracing, formatting, retries, notification, cache warming, or persistence that belongs to another responsibility.

#### Invariant 6. Different reasons to change indicate lower cohesion
If independent changes are likely to target disjoint internal parts of the same subprogram, cohesion is lower than it should be.

Verifiable by:
- listing likely change triggers;
- mapping each trigger to the internal steps it affects;
- confirming that most meaningful changes affect the routine as one unit.

Falsified by:
- one routine containing separate business policy, transport mapping, persistence detail, presentation formatting, and operational concerns that commonly change for different reasons;
- mode flags or type switches that add new behaviors without changing the shared responsibility.

#### Ordered cohesion profiles
Cohesion is an ordered diagnostic scale with these profiles, from strongest to weakest:
1. Functional — major steps directly realize one responsibility without their main relatedness depending on pipeline flow or shared-data handling.
2. Sequential — one responsibility is completed through an essential pipeline where output or effect of one step feeds the next.
3. Communicational — one responsibility is completed through coordinated work on the same data slice or evolving work item.
4. Procedural — steps grouped mainly by execution order.
5. Temporal — steps grouped by execution phase.
6. Logical — steps grouped by category selected by flag or discriminator.
7. Coincidental — steps have no strong relationship.

Selection criteria.
First test whether one precise responsibility statement explains all significant steps.
If it does not, the subprogram is not highly cohesive and should usually be decomposed.
If it does, classify the subprogram by the strongest relation that explains how its major steps cohere.
Use functional when the steps directly realize the responsibility, sequential when pipeline flow is dominant, and communicational when coordinated work on one data slice or work item is dominant.
Functional is preferred when achievable, but sequential and communicational are normal acceptable profiles, especially for thin orchestrators.
If different internal groups are held together by different weaker relations, the weakest relevant relation governs the assessment.

### 2.4. Minimal Formalization
Artifact schema for evaluation:
- Subprogram
- Responsibility
- Inputs
- Outputs
- Essential effects
- Incidental effects
- Observed step groups
- Profile
- Decision

Minimal example:
Subprogram: calculate_net_salary
Responsibility: Calculate net salary for one employee for one pay period.
Inputs: employee, payroll_rules, time_slice
Outputs: net_salary
Essential effects: none
Incidental effects: none
Observed step groups: gross calculation; mandatory deductions; net amount
Profile: functional
Decision: keep

### 2.5. Construction Algorithm
1. Select one target subprogram.
2. Write one responsibility sentence.
3. Enumerate significant internal steps.
4. Mark externally visible outputs and effect boundaries.
5. Group steps by purpose.
6. Determine the strongest cohesion relation.
7. Check for independent reasons to change.
8. Decide the action (keep, split, extract, move effect).
9. Apply the smallest refactoring that increases cohesion.
10. Re-verify the responsibility and cohesion profile.

### 2.6. Typical Errors (anti-patterns)
- Mistaking one phase for one responsibility.
- Mistaking shared data for high cohesion.
- Hiding multiple behaviors behind mode flags or type switches.
- Mixing responsibility with incidental operational concerns.
- Chasing tiny routines instead of cohesive routines.
- Confusing complexity metrics with cohesion.

## 2.7. Links
- EA principles: `../conventions/ea-principles.md` (EA.F3).
- Checklist: `../checklists/operations.md`.
- Related concept: `../concepts/subprogram-level-of-abstraction.md`.
- Related concept: `../concepts/actions-calculations-data.md`.
- Related concept: `../concepts/balanced-system-form.md`.

## Sources and Attributions
- Constantine, L. and Yourdon, E. *Structured Design: Fundamentals of a Discipline of Computer Program and Systems Design*.
- Page-Jones, M. *The Practical Guide to Structured Systems Design*.
- Fowler, M. *Refactoring* and related essays on extract function and abstraction levels.
- Modern static-analysis and IDE documentation regarding method-level complexity metrics.
