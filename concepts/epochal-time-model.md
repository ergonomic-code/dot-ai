# Epochal Time Model

## 2. Concept spec: “Epochal Time Model”

### 2.1. Intention

The epochal time model is used to reason about “changing state” without relying on in-place mutation as the primary mental model.
It frames change as a sequence of discrete, atomic transitions between immutable snapshots.
It replaces informal reasoning like “the object changes over time” with an operational model that is checkable in design and code review: identities persist; snapshots do not change; “state” is an identity’s associated snapshot at a particular step; time is the ordering of those steps.

Measurable benefits:
* clearer correctness arguments under concurrency (observers operate on whole snapshots);
* more testable update logic (transitions can be validated as snapshot-to-snapshot computations);
* explicit atomicity-scope decisions (what must advance together vs independently);
* reduced incidental complexity caused by conflating identity, value, and time.

### 2.2. Ontological Status

What it is:
* A conceptual model for time and change in software systems based on:
  * immutable value snapshots;
  * stable identities associated with successive snapshots;
  * a time construct that provides atomic advancement and snapshot perception within a declared scope.

Operational definitions:
* Value snapshot: an immutable representation of “the whole value” being associated with an identity at an epoch.
* Identity: a stable logical entity (key/handle) whose associated snapshot may differ across epochs.
* Epoch: a logical position in an ordered sequence of committed states (at minimum a before/after ordering).
* Time construct: the mechanism/contract that (a) returns snapshots on read and (b) advances state by atomically associating the identity with the next snapshot.

What it is not:
* A model of physical time (wall-clock, durations, scheduling).
* A specific library, language feature, or concurrency primitive.
* A distributed consistency protocol (it can be used in distributed systems but does not define cross-node guarantees by itself).

Operational rule to distinguish “similar but not the same”:
* Matches epochal time if: state change is represented by producing a new immutable snapshot and atomically making it the next state of an identity, and reads yield whole snapshots (no torn composites) within the declared scope.
* Does not match epochal time if: change is represented as in-place mutation of the snapshot value (or its semantically significant parts), such that intermediate/partial states are meaningful or observable (even conceptually) during an update.

Scope boundaries / non-goals:
* Does not define how to align epochs with physical time.
* Does not require retaining history; history retention (if any) is a separate design choice.
* Does not require a single global timeline; multiple independent timelines are allowed.

### 2.3. Concept Invariants

Invariant 1 — Snapshot immutability.
* Statement: A value snapshot does not change; change is represented only by producing a new snapshot.
* Verifiable by: update logic can be expressed as `new = f(old, input)` where `old` and `new` are snapshots.
* Falsified by: an update requires mutating fields of the “current snapshot” (or any semantically significant shared structure) in place.

Invariant 2 — Identity/value separation.

* Statement: Identity is not the snapshot; it is a stable handle that can be associated with different snapshots over epochs.
* Verifiable by: design/code clearly distinguishes (a) the identity carrier (key/handle/reference) from (b) the immutable snapshot value; it is meaningful to speak about “same identity, different snapshots.”
* Falsified by: identity is modeled as an object whose internal fields are mutated in place and those mutable fields constitute the state (so partial/intermediate states are semantically meaningful or observable).

Invariant 3 — State as an epoch-indexed association.

* Statement: “State” is the association of an identity with a snapshot at an epoch; state does not “change,” it is succeeded.
* Verifiable by: designs and discussions use “next state / successive states” semantics; state can be treated as a snapshot at a logical moment.
* Falsified by: state is defined as “the current mutable contents” of a container, updated incrementally.

Invariant 4 — Time as ordering (epoch order) at minimum.

* Statement: The model requires an epoch ordering relation (before/after) for committed transitions; metric time is optional metadata.
* Verifiable by: the design specifies how transitions are ordered (monotonic marker / total order within scope / explicit transaction order).
* Falsified by: the only sequencing rule is wall-clock timestamps without an explicit commit-order semantics.

Invariant 5 — Atomic state succession within the declared scope.

* Statement: Advancing from one state to the next is atomic within the chosen atomicity scope.
* Verifiable by: the design declares the scope and states that observers cannot observe a partially advanced state for that scope.
* Falsified by: observers can observe mixtures of old/new state for the same identity (or for a declared coordinated set) without that being explicitly permitted.

Invariant 6 — Snapshot perception on read within the declared scope.

* Statement: A read yields a whole snapshot corresponding to a single logical moment for the identity (and, if declared, for a coordinated set).
* Verifiable by: the read contract defines the snapshot boundary and the consistency boundary for multi-identity views (if required).
* Falsified by: correctness assumes point-in-time views, but reads are allowed to return torn or time-mixed composites across the assumed boundary.

### 2.4 Variants / profiles

Common invariants: 1–6 remain common across variants.

Variant A — Per-identity linearization.

* Definition: atomicity and ordering are guaranteed per identity; each identity has its own independent timeline.
* Selection criteria: use when operations primarily update a single identity and cross-identity invariants can be handled outside the time construct (coordination, convergence, compensation).

Variant B — Coordinated region (multi-identity atomicity).

* Definition: a declared region covers multiple identities; atomic advancement and snapshot reads apply to that region.
* Selection criteria: use when correctness requires multiple identities to advance together (cross-identity invariants must hold atomically).

Variant C — History retention.

* Options:

  * C1 latest-only: only the current snapshot is retained/visible.
  * C2 versioned: multiple snapshots per identity are retained and addressable by epoch.
* Selection criteria: C2 when audit/debug/as-of queries are a requirement; otherwise C1.

### 2.5. Construction Algorithm

1. Identify identities and snapshot boundaries.

* Input: operation list and the “things that persist” across operations.
* Output: a list of identities (identity keys/handles) and a definition of the snapshot boundary for each (what the snapshot must contain to support transitions).

2. Rewrite updates as transitions.

* Input: for each operation, its intent and inputs.
* Output: a transition definition of the form `new_snapshot = f(old_snapshot, input)` plus any preconditions that must hold for the transition to be applicable.

3. Choose the atomicity scope variant.

* Input: invariants that must never be observed violated.
* Output: selected scope (Variant A or B) recorded as an explicit design decision, with the concrete boundary stated (per identity vs coordinated region).

4. Specify read semantics (snapshot perception).

* Input: requirements for decision/reporting reads (single identity vs coordinated view).
* Output: explicit snapshot-read contract: what a read returns, and the consistency boundary it guarantees within the chosen scope.

5. Define conflict and retry semantics (if concurrency is in scope).

* Input: expected contention and correctness constraints under concurrent updates.
* Output: explicit rule whether transition computation may be retried, and the required property of transition computation under retries (no irreversible external effects).

6. Place external effects relative to commit.

* Input: list of external effects implied by operations (I/O, integrations).
* Output: explicit boundary rule: whether effects occur before/after snapshot advancement, and what safety property is required (idempotency/deduplication) if effects can be retried.

### 2.6. Typical Errors (anti-patterns)

Error 1 — In-place mutation presented as “state update”.

* Detect: updates are described as “set fields” without producing a new snapshot.
* Highlight: where partial/intermediate states become meaningful or observable.
* Auto-correct: rewrite as `new = f(old, input)` and define the snapshot boundary.

Error 2 — Identity conflated with a mutable stateful object.

* Detect: identity is treated as “the mutable object,” and state is its mutable fields.
* Highlight: that the model no longer guarantees snapshot perception or clear succession semantics.
* Auto-correct: separate identity (handle) from snapshot (immutable value); model change as atomic repointing to a new snapshot.

Error 3 — Atomicity scope is implicit.

* Detect: claims of “atomic updates” without stating whether it is per identity or coordinated.
* Highlight: which invariants force coordinated atomicity (or do not).
* Auto-correct: default to Variant A, and mark Variant B as required if cross-identity invariants must hold atomically.

Error 4 — Snapshot-read consistency is assumed but not specified.

* Detect: correctness assumes point-in-time reads across multiple identities, but read semantics are unspecified.
* Highlight: the exact consistency boundary needed.
* Auto-correct: define the read contract and, if needed, declare a coordinated region boundary.

Error 5 — Irreversible external effects inside retryable transition computation.

* Detect: conflict/retry semantics exist, and the transition computation includes I/O or irreversible actions.
* Highlight: risk of duplicated effects and non-determinism under contention.
* Auto-correct: move effects after commit and require idempotency/deduplication, or change retry policy.

Error 6 — Epoch treated as wall-clock sequencing without commit-order semantics.

* Detect: timestamps are used as the sole ordering mechanism while “before/after” of commits is not defined.
* Highlight: difference between ordering of committed states and physical time.
* Auto-correct: define explicit commit-order semantics (monotonic ordering) and treat wall-clock time as optional metadata.

---

## 3. Sources and Attributions

### 3.1. Sources

1. Rich Hickey. “Are We There Yet? A Deconstruction of Object-Oriented Time.” JVM Language Summit (PDF). ([JVMLangSummit][1])
2. Rich Hickey. “Persistent Data Structures and Managed References.” QCon London (PDF). ([QCon London 2009][2])
3. “Values and Change: Clojure’s approach to Identity and State.” (Article). ([Clojure][3])
4. “Atoms.” (Reference documentation; notes about retries and side effects under `swap!`). ([Clojure][4])
5. Donny Winston. “The Materials Paradigm and Epochal Time.” (Article). ([Donny Winston][5])
6. `swap!` documentation note (“f may be called multiple times… free of side effects”). ([ClojureDocs][6])
7. Rich Hickey. “The Database as a Value.” (Slides PDF). ([Parallel Data Lab][7])

### 3.2. Direct Borrowings

B1) The conceptual separation of identity, state, value, and time; and the notion of “epochal time” characterized by atomic state succession and point-in-time value perception (as properties required of a time construct). ([JVMLangSummit][1])

B2) The characterization of “identity appears to change because it becomes associated with different state values over time,” and the framing of observation as obtaining a stable value snapshot. ([Clojure][3])

B3) The operational constraint that an atomic update mechanism may retry by invoking the transition function multiple times, therefore transition computation must be free of side effects under retry semantics. ([Clojure][4])

B4) The claim that the conceptual distinctions and approach are not language-specific ideas, used here as a justification to keep the concept language-agnostic. ([QCon London 2026][2])

### 3.3. Synthesized Elements

S1) The invariant set in section 2.3 (immutability, identity/value separation, epoch ordering, atomic succession, snapshot perception) is a synthesis of the epochal framing and identity/state/value definitions, expressed as verifiable/falsifiable checks suitable for design review. ([JVMLangSummit][1])

S2) The variants/profiles (per-identity vs coordinated region; latest-only vs versioned history) generalize “time constructs with different semantics” into explicit selection decisions and scope declarations. ([JVMLangSummit][1])

S3) The construction algorithm (section 2.5) is an operationalization intended for consistent application in design/review: it is “emergent synthesis” assembled from the recurring requirements and constraints across the sources rather than copied as a single procedure. ([JVMLangSummit][1])

### 3.4. Discrepancies and Resolutions

D1) Ordering vs physical time.

* Discrepancy: sources emphasize time as an ordering of states; practical systems often store wall-clock timestamps.
* Resolution: treat commit ordering (epochs as ordering) as invariant; treat wall-clock as optional metadata. ([JVMLangSummit][1])

D2) Atomicity scope: per-identity vs coordinated multi-identity regions.

* Discrepancy: different time constructs offer different scopes; some discussions focus on per-identity constructs, others on coordinated transactions/regions.
* Resolution: declare this as an explicit variant choice (Variant A vs B) with selection criteria; do not assume one default. ([JVMLangSummit][1])

D3) History retention.

* Discrepancy: some materials use “current value” semantics, others emphasize time-aware, versioned models.
* Resolution: keep history retention as a variant (C1 latest-only vs C2 versioned) driven by requirements (audit/as-of). ([JVMLangSummit][1])

[1]: https://wiki.jvmlangsummit.com/images/a/ab/HickeyJVMSummit2009.pdf "Are We There Yet? - JVMLangSummit"
[2]: https://qconlondon.com/london-2009/qconlondon.com/dl/qcon-london-2009/slides/RichHickey_PersistentDataStructuresAndManagedReferences.pdf "Clojure's approach to Identity and State"
[3]: https://clojure.org/about/state "Values and Change: Clojure's approach to Identity and State"
[4]: https://clojure.org/reference/atoms "Atoms"
[5]: https://donnywinston.com/posts/the-materials-paradigm-and-epochal-timem "The Materials Paradigm and Epochal Time"
[6]: https://clojuredocs.org/clojure.core/swap%21 "swap! - clojure.core"
[7]: https://www.pdl.cmu.edu/SDI/2013/slides/hickey-dbasvaluecmu.pdf "Rich Hickey"
