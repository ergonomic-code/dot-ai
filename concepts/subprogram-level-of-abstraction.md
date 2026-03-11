# Level of Abstraction of a Subprogram

## 2. Concept spec: "Level of Abstraction of a Subprogram"

### 2.1. Intention
This concept standardizes how a subprogram should read, be reviewed, and be refactored so that its logic can be understood without repeatedly switching mental gears between business meaning, protocol mechanics, storage mechanics, UI mechanics, parsing details, and similar concerns.

It is used to reduce a recurring ambiguity: whether a subprogram expresses one coherent step of behavior or mixes essential concepts with lower-level implementation details.

It provides observable benefit in tasks such as:

- reviewing a function or method for readability and maintainability;
- deciding whether extraction or delegation is needed;
- generating code that reads as a top-down narrative;
- detecting where infrastructure details leak into domain logic;
- verifying that adapters and translators remain explicit boundaries.

---

### 2.2. Ontological Status
This concept is a **design principle and review criterion** for callable units of code.

A **subprogram** is any callable unit whose body forms a local narrative, for example:

- function
- method
- procedure
- command handler body
- query handler body
- mapper routine
- serializer routine

This concept is **not**:

- a metric about line count;
- a synonym for “single responsibility”;
- a synonym for cohesion;
- a full layering rule for the system;
- a naming rule alone.

Operational distinction rule:
- A subprogram violates this concept when the reader must constantly switch between different semantic vocabularies or abstraction scales while reading its body.
- A subprogram satisfies this concept when its body can be paraphrased as a sequence of steps that either stay within one semantic vocabulary or perform one explicit source-to-target translation, and all represent one step below the subprogram name.
- Cohesion asks whether the major steps serve one responsibility.
- Level of abstraction asks whether those steps stay within one dominant vocabulary and one local narrative level.

Scope boundaries:
- This concept applies to **one subprogram body**.
- It does not require a whole class or module to use a single vocabulary.
- It allows explicit translation routines between vocabularies.

---

### 2.3. Concept Invariants
Two variants of the concept exist.

1. **Single-vocabulary subprogram** (default)
2. **Translation subprogram**

Selection criteria:

- Use a **single-vocabulary subprogram** when expressing behavior inside one model or layer.
- Use a **translation subprogram** when converting or adapting between two vocabularies.

---

#### Common invariants

**Invariant 1 — Single abstraction level**
The body must be readable as steps at one local abstraction level.

Verification:
The body can be paraphrased as a short narrative where each step refines the subprogram name.

Falsification:
Statements combine domain decisions with low-level mechanics such as SQL fragments, serialization details, or protocol framing.

---

**Invariant 2 — Name one level above implementation**
The subprogram name denotes a concept one level above the steps inside the body.

Verification:
Each statement refines the meaning of the name.

Falsification:
The body contains details not implied by the name.

---

**Invariant 3 — Reviewable vocabulary shape**
A reviewable vocabulary shape can be identified from:

- the subprogram name
- parameters
- return type
- major local identifiers
- primary callees

Verification:

- A single-vocabulary subprogram exposes one dominant vocabulary.
- A translation subprogram exposes one explicit source/target vocabulary pair.

Falsification:
The body mixes several unrelated vocabularies equally.

---

**Invariant 4 — Delegation of lower-level mechanics**
Lower-level mechanics must appear behind helper routines whose names belong to that lower level.

Verification:
The enclosing subprogram remains narrative and intention-revealing.

Falsification:
Low-level details are written inline.

---

#### Variant A — Single-vocabulary subprogram

**Invariant A1**
Exactly one dominant vocabulary is used.

Examples:

- business domain vocabulary
- HTTP vocabulary
- RDBMS vocabulary
- UI vocabulary

Falsification:
Inline mixture such as domain + SQL + HTTP framing.

---

**Invariant A2**
Foreign vocabulary appears only inside delegated helpers.

Falsification:
Protocol, persistence, or serialization details appear inline.

---

#### Variant B — Translation subprogram

**Invariant B1**
At most two meaningful vocabularies exist.

Example:

- HTTP → domain
- domain → persistence
- JSON → domain

Falsification:
Three or more vocabularies appear in one routine.

---

**Invariant B2**
Translation direction is explicit.

Typical naming patterns:

- `toDomain`
- `fromHttp`
- `mapToDto`
- `encode`
- `decode`

---

**Invariant B3**
The translation routine does not contain independent business decisions.

Falsification:
Business policy, workflow orchestration, or retry logic appears inside a translator.

---

Stable invariant core:
A subprogram must use either:

- **one dominant vocabulary**, or
- **two vocabularies if it is explicitly a translator**.

---

### 2.4. Minimal Formalization

#### Vocabulary
A coherent set of terms belonging to one model or technical space.

Examples:

- business domain vocabulary
- HTTP vocabulary
- RDBMS vocabulary
- JSON vocabulary
- UI vocabulary

---

#### Dominant vocabulary

The vocabulary defining the subprogram’s purpose and most of its identifiers.

---

#### Foreign vocabulary

A vocabulary present in the body but not defining the routine’s purpose.

---

#### Translation subprogram

A routine whose purpose is converting between two vocabularies.

---

#### Abstraction step

An operation that refines the subprogram name without exposing unrelated lower-level mechanics.

---

Counting rule:
Language syntax, control flow keywords, and trivial standard library usage do not count as additional vocabularies.

---

### 2.5. Construction Algorithm
1. Define the responsibility of the subprogram in one sentence.
Output: responsibility statement.
2. Identify the vocabulary of that sentence.
Output: dominant vocabulary.
3. Inspect the candidate body and list vocabularies appearing in:

- names
- parameters
- return type
- major callees.

4. Classify the routine:

- single-vocabulary routine
- translation routine.

5. If more than two vocabularies appear, split the routine.
Output: smaller routines each belonging to one vocabulary or explicit translation.
6. Ensure each statement is one abstraction step below the subprogram name.
7. Extract lower-level mechanics into helpers.
8. Verify that the body can be read top-down without semantic context switching.
9. Verify naming:

- single-vocabulary routines use domain terminology
- translation routines reveal source and target vocabularies.

10. Reject the routine if a hidden third vocabulary remains.

---

### 2.6. Typical Errors
**Mixed narrative**
Domain decisions mixed with low-level mechanics.

Detection:
domain terms interleaved with SQL, JSON, or HTTP details.

---

**Hidden three-way junction**
Three vocabularies inside one routine.

Example:
domain + HTTP + RDBMS.

---

**Name/body mismatch**
The name suggests a higher abstraction than the body actually implements.

---

**Faux extraction**
Helpers extracted but still mixing vocabularies.

---

**Undeclared translation**
A routine translating between models but not marked as such.

---

**Vocabulary drift**
Multiple synonyms used for the same concept in one scope.

---

### 2.7. Links
- EA principles: `../conventions/ea-principles.md` (EA.F4).
- Checklists: `../checklists/subprograms.md`, `../checklists/operations.md`, `../checklists/integrations.md`.
- Related concept: `../concepts/cohesion.md`.

---

## 3. Sources and Attributions

### 3.1. Sources
Kent Beck — *Smalltalk Best Practice Patterns* (1997)
Robert C. Martin — *Clean Code* (2008)
Martin Fowler — *Ubiquitous Language* / *Bounded Context*
Microsoft Learn — *Anti-corruption Layer pattern*
Research on program comprehension and identifier naming.

---

### 3.2. Direct Borrowings

The rule that operations inside a method should stay at the same abstraction level originates from the **Composed Method** pattern by Kent Beck.

The rule that a function should consist of steps one level below its name comes from Robert C. Martin’s discussion of functions in *Clean Code*.

---

### 3.3. Synthesized Elements

Framework-level synthesis:
- application of abstraction levels specifically at **subprogram scope**
- vocabulary-based inspection of routines
- classification into **single-vocabulary routines** and **translation routines**
- the rule that translation routines contain **no more than two vocabularies**

---

### 3.4. Discrepancies and Resolutions

Classical sources discuss abstraction levels but do not formalize vocabulary boundaries.

The framework introduces vocabulary analysis because it allows operational checks during code review and automated agent analysis.

The rule “one vocabulary or two for translators” is a **framework-level strengthening** derived from readability principles rather than a direct statement from primary sources.
