---
name: synthesizing-framework-concepts
description: "Synthesis of an operational description of a new or modified framework concept based on sources (books/articles/methodologies/industry): extract invariants/variations/anti-patterns, then produce a Concept spec plus a separate 'Sources and Attributions' section to add or revise materials in `concepts/`."
---

# Synthesizing framework concepts

## Concept Description

This instruction describes how to synthesize a stable, operational concept from a set of sources so that AI agents can apply it consistently.

The primary result is intended to be written to `concepts/<CONCEPT_SLUG>.md`.

See an example of a completed concept spec in `concepts/making-illegal-states-unrepresentable.md`.

## Input

* `CONCEPT_NAME` — the concept name (as in the document title).
* `CONCEPT_SLUG` — a stable slug for the file path (lowercase + hyphen).
* `FRAMEWORK_STRUCTURE` — a brief description of the framework structure (or links to relevant files in the repository).
* `SOURCES` — a list of sources.
* Optional: `TARGET_CONCEPT_PATH` — target file path (default `concepts/<CONCEPT_SLUG>.md`).

## Output

1. A document for `TARGET_CONCEPT_PATH` strictly following the “Result Structure (strict)” below, including:

* the Concept spec (section 2),
* the “Sources and Attributions” section (section 3).

2. If sources or context are insufficient: a checklist of blocking questions (separate from the concept document body).

## Constraints

* The output document must be written in English.
* Do not retell the sources or “teach the reader.”
* Do not bind tightly to a single author or methodology.
* Do not use terms without operational definitions (or mark them explicitly as `TBD`).
* Do not include source references inside the Concept spec body (section 2).
* If sources conflict:

   * If the conflict affects invariants: do not “average.” Declare explicit variants/profiles and state selection criteria.
   * If the conflict affects optional details: choose a more universal formulation and record the discrepancy in “Sources and Attributions.”
* Prefer statements that are verifiable against text, model, code, or artifact.

## Algorithm

1. Fix the task frame.

* Confirm `CONCEPT_NAME` and `TARGET_CONCEPT_PATH`.
* Determine intended usage context at a high level (what kinds of tasks this concept supports).

2. Load the framework context.

* If the structure is unclear, read `README.md` and any concept index files.
* Check whether a similar concept already exists in `concepts/` (avoid duplicates; prefer revision).

3. Analyze sources (internal step).

* Extract candidate invariants.
* Extract candidate variations (options that preserve invariants).
* Collect typical mistakes and distortions (anti-patterns).
* Record discrepancies between sources without attempting to “reconcile” them.

4. Synthesize the Concept spec (section 2).

* Formulate each statement so it can be verified against text, model, code, or artifact.
* Ensure all terms used in invariants, notation (if present), and algorithm have operational definitions (or `TBD`).
* If variants/profiles exist, express them explicitly and provide selection criteria.

5. Add “Sources and Attributions” (section 3).

* List sources with sufficient precision for lookup (author/title/year/section or URL).
* Mark direct borrowings vs. synthesized claims.
* Record discrepancies and how they were handled (variants vs. chosen universal formulation).

6. Self-check.

* No source references inside section 2.
* All terms have operational definitions or explicit `TBD`.
* Each invariant has a concrete verification method.
* Section 2.4 is present only if applicable (per its rules).
* Section 3 contains enough traceability to audit the synthesis.

## Result Structure (strict)

### 1. Source Analysis (internal step)

Do not include this section in `concepts/<...>.md`.
Use it only as an internal working step and as a basis for section 3.

### 2. Concept spec: "{{CONCEPT_NAME}}"

#### 2.1. Intention

* Why the concept is used.
* What mental work it replaces.
* In which tasks it provides measurable benefit.

#### 2.2. Ontological Status

* What it is (model / analysis method / notation / artifact / design principle / other).
* What it is not.
* An operational rule for distinguishing “similar but not the same.”
* Scope boundaries / non-goals (what it intentionally does not address).

#### 2.3. Concept Invariants

List statements without which the concept ceases to be itself.

For each invariant, specify:

* how it can be verified (from artifact, code, text, or explicit checks);
* what would falsify it (a concrete counter-signal).

If the concept has variants/profiles, include:

* a list of variants,
* selection criteria (when to use which),
* which invariants remain common vs. variant-specific.

#### 2.4. Minimal Formalization (optional)

Include this section only if at least one is true:

* the concept defines a structured artifact that must be produced/validated (diagram/table/schema/YAML/JSON/etc.);
* the concept introduces stable element types (nodes/relations/fields) that require an explicit list to prevent drift;
* machine-checkable structure is required to apply the concept reliably.

If included, choose the smallest adequate mode:

A) Artifact schema mode

* Element types (nodes/relations/fields) and their meaning.
* Mandatory vs. optional elements.
* A minimal textual format (YAML/JSON/table) suitable for validation.
* One minimal normative example (no explanations).

B) Vocabulary mode

* Minimal set of terms required for correct application.
* Operational definitions for each term.

If not included, ensure all necessary operational definitions appear in sections 2.2–2.3.

#### 2.5. Construction Algorithm

Describe how to construct the target artifact or apply the concept in practice.

* Use numbered steps (1…, 2…, 3…).
* Formulate steps as verifiable operations (not advice).
* For each step, specify:

   * input,
   * output (what must appear in the artifact/code/decision log).

If the concept is a principle (not an artifact), interpret outputs as observable code/design outcomes (e.g., introduced types, removed invalid states, enforced construction boundary).

#### 2.6. Typical Errors (anti-patterns)

List typical mistakes and distortions.

For each error, specify:

* how to detect it from the artifact/code;
* what to highlight to the user;
* what can be auto-corrected without questions.

### 3. Sources and Attributions

#### 3.1. Sources

* Bibliography list with enough precision for lookup (author/title/year/section/pages or URL).

#### 3.2. Direct Borrowings

* Enumerate statements/definitions that are near-direct borrowings.
* Point to the corresponding source location.

#### 3.3. Synthesized Elements

* Enumerate key synthesized claims (especially invariants, variants, and algorithm steps).
* For each, list which sources support it (or indicate “emergent synthesis”).

#### 3.4. Discrepancies and Resolutions

* List source discrepancies relevant to the concept.
* Record how each discrepancy was handled:

   * variant/profile declared, or
   * universal formulation chosen (with rationale stated as a constraint-driven choice, not as “truth”).
