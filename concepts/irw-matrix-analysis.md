# IRW Analysis (IRW Matrix Analysis)

## 2. Concept Spec: “IRW Analysis”

### 2.1. Intention

IRW analysis is used to design and validate an ergonomic data model by mapping operations to the data elements they read and modify.
The technique replaces informal reasoning such as “which operations touch which data and how broadly” with a verifiable artifact.

The primary result is the IRW matrix, which can be used to detect overloaded operations, unstable aggregate boundaries, and gaps in the operation set.

The technique complements the effects diagram by clarifying the participation of internal data paths in operations (see `concepts/effects-diagram.md`).

---

### 2.2. Ontological Status

IRW analysis is a method of data model analysis and design that uses tabular notation as the artifact for recording results.

The IRW matrix is an artifact (a table or textual serialization of a table) that serves as the source of truth for conclusions drawn from IRW analysis.

IRW analysis is not:

* a data model (ERD/class diagram) and does not replace it;
* an invariant specification and does not explain causal motivations for changes;
* a flow/temporal diagram and does not describe the order of steps inside an operation;
* an access-control or responsibility matrix.

Operational distinction (“similar but not it”): if an artifact does not record coverage of “data element × operation” using markers `I | R | W | ∅`, then it is not an IRW matrix.

---

### 2.3. Concept Invariants

IRW analysis remains IRW analysis if the following hold.

**Scope is fixed.**
The artifact explicitly states for which feature/context the matrix is built and which operations are included.
Check: the artifact contains a `scope` field (or equivalent) describing boundaries and assumptions.

**Operation is defined as a unit of behavior within the feature context.**
An operation is a command/scenario/use-case/endpoint/job (according to chosen definitions) for which data reads and writes can be enumerated.
Check: each matrix column has an operation name and can be traced to requirements or code via `trace`.

**Rows represent data elements as stable data paths.**
A row is a data path inside a record/aggregate sufficient to distinguish independent lifecycles and invariants.
Check: each row follows the data path notation rules and has a stable name.

**Cell alphabet is restricted.**
Each cell contains one of: `I` (initialize), `R` (read), `W` (write/change), or is empty.
Check: no other values appear in matrix cells.

**Operation completeness is ensured for included data paths.**
If a data path is included, the matrix includes all operations in scope that read or write it.
Check: when adding a row, all candidate operations are enumerated and verified; gaps are recorded as `tbd` with explicit questions.

**Row granularity is declared and refined iteratively.**
The matrix starts coarse and is refined only upon signal.
Check: the artifact lists applied granularity rules and reasons for splits.

**Derived/projection fields are marked.**
If a data element is derived (denormalized/projection), it is marked separately so joint `W` does not imply required atomic coupling.
Check: derived rows contain `derived: true` (or equivalent).

---

### 2.4. Minimal Notation

An IRW matrix consists of rows, columns, and cells.
The source of truth should be stored in a textual format (YAML/JSON) or in a Markdown table suitable for machine validation.

#### Element Types

**Operation (`Operation`)** — named unit of feature behavior.
Recognition: phrasing “the system shall …” or a stable entry point (endpoint/job/handler).

**Data element (`DataPath`)** — named data path inside a record/aggregate.
Recognition: attribute, composite/value object, collection, leaf within a composite, field of a collection element, or reference to another record (if modeled).

**Participation marker (`IRW`)** — cell value capturing the role of the data element in the operation.
Allowed values: `I`, `R`, `W`, `∅`.

---

#### Terms and Assumptions (Minimum)

The ergonomic data model is treated as a set of records and aggregates where attributes may be scalar, composite/value objects, collections of values, and optionally references to other records.
See `concepts/ergonomic-data-model.md` for formal specification if needed.

An aggregate is treated as a consistency boundary within which operations preserve data integrity and invariants.

Ownership rule: a record/entity belongs to exactly one aggregate within the chosen model.

Invariants are data integrity and behavioral rules specified separately from the IRW matrix and used to interpret its signals.

---

#### Cell Semantics

`I` (Initialize): the element receives its first value within the chosen lifecycle model.
`R` (Read): the element is used without modification (for response, validation, branching, calculation).
`W` (Write/Change): the element is modified (overwrite/update/mutate), including composite leaves and collection element fields.
`∅` (empty): the operation does not use the element.

The marker `RW` is intentionally not used.

---

#### DataPath Notation (Minimum)

`A.x` — simple field of aggregate/record `A`.
`A.comp` — composite attribute as a whole.
`A.comp.y` — leaf within a composite (if needed).
`A.items[]` — collection as structure (membership: add/remove/reorder).
`A.items[].y` — field of a collection element.
`A.items[].*` — aggregated row for element fields if detailing is premature.

---

#### Row Granularity Rules (G0–G5)

**G0 (start coarse):** begin with top-level aggregate attributes, including composites and collections as single elements.

**G1 (split only upon signal):** split row `X` into sub-rows only if different operations stably use different parts of `X` and it affects conclusions.

**G2 (composite as whole):** keep composite as a single row if parts are created/changed together, participate in the same invariant, or are transferred as a unit.

**G3 (collections):** distinguish `A.items[]` (membership) from `A.items[].field` (element state), using `A.items[].*` as temporary aggregation.

**G4 (leaf detail):** descend to leaf level only if leaves change independently, participate in different invariants, or are required to justify aspect/subaggregate boundaries.

**G5 (projections/denormalization):** include derived fields as rows but mark them as derived to avoid treating joint `W` as required atomic coupling of sources.

---

#### Canonical Text Format (for AI)

The minimal format must allow:

1. listing `operations` and `data_paths`,
2. storing the `I/R/W` matrix,
3. recording `tbd` without violating the cell alphabet.

(YAML structure remains unchanged from the original.)

---

#### Derived Representation (for humans)

If stored in YAML/JSON, a Markdown table is a derived representation.
The table may be regenerated without semantic change.

---

### 2.5. Construction Algorithm

The algorithm is defined as a sequence of verifiable steps and ends at a fixpoint over operations and data paths.

1. Fix `scope`.
2. Select starting point (`aggregate` or `operation`).
3. Form initial sets at G0 granularity.
4. Fill matrix for current coverage.
5. Expand to fixpoint under completeness rule.
6. Refine granularity only upon signal (G1–G5).
7. Mark derived elements.
8. Validate invariants and record `tbd`.
9. Produce decision signals (e.g., broad `W` footprint, cross-aggregate `W`, empty rows, `I` without `R`, read-only rows).

---

### 2.6. Typical Errors (Anti-Patterns)

**Violation of operation completeness.**
Add missing operations or record `tbd`.

**Mixing meaning and participation.**
Matrix records participation only; invariants are separate.

**Incorrect use of `I` and `W`.**
Distinguish first initialization from subsequent modification.

**Premature over-detailing (noise).**
Collapse unnecessary leaf rows.

**Insufficient detail (hidden independent lifecycles).**
Split rows per G1–G4.

**Collection structure and element state conflated.**
Separate `A.items[]` from `A.items[].field`.

**Unmarked derived fields.**
Mark `derived: true`.

---

## 3. Skill Spec: Using “IRW Analysis” by an AI Agent

### 3.1. Usage Triggers

The agent should propose IRW analysis if at least one applies:

* designing/changing a feature data model and mapping operations to data;
* clarifying aggregate boundaries or identifying lifecycle-based aspects;
* localizing broad `W` footprint of an operation;
* mitigating regression risk by making read/write usage explicit;
* detecting unused or “written but never read” elements.

The agent should not propose IRW analysis if:

* no mutable data is involved (pure computation);
* scope is too broad and no feature/context is isolated;
* a current IRW matrix of sufficient granularity already exists.

---

### 3.2. Questions to the User

Prioritized by impact on matrix correctness:

1. What is the matrix `scope` and which operations count as operations in this scope?
2. What is the starting point (aggregate or operation), and its name?
3. What is the source of truth for operations and data, and how to reference it (`trace`)?
4. Which elements are derived/projections?
5. Which invariants matter for aggregate boundary decisions, and where are they specified?

Unknown answers are recorded as `tbd`.

---

### 3.3. Result Quality Criteria

An IRW matrix is “good enough” if:

* fixpoint reached within declared scope;
* cell alphabet respected (`I/R/W/∅` only);
* completeness rule satisfied or gaps recorded as `tbd`;
* row granularity justified and goal-aligned;
* derived elements marked.

Work must continue if:

* `tbd` remains in critical `W` areas;
* operation/data path names remain unstable;
* matrix is too noisy or too coarse to produce stable clusters.
