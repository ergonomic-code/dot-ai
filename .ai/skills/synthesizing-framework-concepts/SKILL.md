---
name: synthesizing-framework-concepts
description: "Synthesis of an operational description of a new or modified framework concept based on sources (books/articles/methodologies/industry): extract invariants, variants, and anti-patterns, then produce a Concept spec plus a separate 'Sources and Attributions' section to add or revise materials in `concepts/`."
---

# Synthesizing framework concepts

## Concept Description

This instruction defines how to synthesize a stable, operational framework concept from a set of sources so that AI agents can apply it consistently.

The primary result is intended to be written to `concepts/<CONCEPT_SLUG>.md`.

See an example of a completed concept spec in `concepts/making-illegal-states-unrepresentable.md`.

## Input

* `CONCEPT_NAME` — the concept name, as used in the document title.
* `CONCEPT_SLUG` — a stable slug for the file path (`lowercase-with-hyphens`).
* `FRAMEWORK_STRUCTURE` — relevant framework paths, indexes, or structural notes needed to place the concept correctly.
* `SOURCES` — a list of source materials.
* Optional: `TARGET_CONCEPT_PATH` — target file path.
  Default: `concepts/<CONCEPT_SLUG>.md`.

## Output

1. A document for `TARGET_CONCEPT_PATH` strictly following the “Result Structure (strict)” below, including:
   * the Concept spec in section 2;
   * the “Sources and Attributions” section in section 3.

2. If sources or framework context are insufficient:
   * do **not** draft the Concept spec;
   * do **not** write the insufficiency output into `TARGET_CONCEPT_PATH`;
   * output only:
     * a short insufficiency note;
     * a checklist of blocking questions.

## Constraints

* The output document must be written in English.
* Do not retell the sources or teach the reader.
* Do not bind the concept too tightly to a single author, brand, or methodology unless the concept is explicitly that author’s own framework construct.
* Do not use terms without operational definitions, unless they are explicitly marked as `TBD`.
* Do not include source references inside the Concept spec body in section 2.
* Prefer statements that are verifiable against text, model, code, artifact, or explicit checks.
* Prefer revising an existing adjacent concept over creating a near-duplicate.
* If an adjacent concept already covers the same operational territory, revise it or split the boundaries explicitly instead of creating overlap by default.

## Source precedence

When sources differ in authority, use the following precedence order:

1. Existing concept files in this repository, if revising an existing concept.
2. Adjacent framework artifacts that constrain terminology, boundaries, or repository structure.
3. Primary sources.
4. Secondary interpretations, summaries, and commentary.

Do not silently override repository-established terminology or boundaries without recording the reason in section 3.4.

## Conflict handling

If sources conflict:

* If the conflict affects invariants:
  * do not average the positions;
  * declare explicit variants or profiles;
  * state selection criteria.
* If the conflict affects optional details:
  * choose the more universal formulation;
  * record the discrepancy in section 3.4 as a constraint-driven choice, not as final truth.

## Algorithm

1. Fix the task frame.

* Confirm `CONCEPT_NAME`.
* Confirm `TARGET_CONCEPT_PATH`.
* Determine the intended usage context at a high level:
  * what kinds of agent tasks this concept is expected to support;
  * what class of mistakes or ambiguity it is expected to reduce.

2. Load adjacent framework context.

Always inspect framework artifacts adjacent to the target concept before synthesis.

At minimum, inspect:

* `concepts/` for similar or neighboring concepts;
* relevant indexes, if they exist;
* relevant `conventions/`, `agents/`, `skills/`, or other files that constrain terminology, boundaries, or artifact style.

Goal:

* avoid duplicate concepts;
* reuse established terminology where appropriate;
* keep concept boundaries aligned with the framework.

3. Analyze sources as an internal working step.

Extract:

* candidate invariants;
* candidate variants or profiles;
* candidate anti-patterns;
* candidate boundaries and non-goals;
* candidate terms that require operational definitions.

Record source discrepancies without prematurely reconciling them.

4. Run a sufficiency gate before drafting.

Before drafting section 2, verify that the available material is sufficient to support all of the following:

* at least one stable intention for the concept;
* at least one clear boundary or distinction rule, or a justified note that such a boundary is currently `TBD`;
* at least two candidate invariant-level statements, or a justified note that the concept is mainly classificatory rather than invariant-heavy;
* enough adjacent framework context to place the concept without obvious duplication or terminology drift.

If this gate fails:

* do **not** draft section 2;
* do **not** modify `TARGET_CONCEPT_PATH`;
* output only:
  * a short insufficiency note;
  * blocking questions.

5. Synthesize the Concept spec in section 2.

* Formulate statements so they can be verified against text, model, code, artifact, or explicit checks.
* Ensure all terms used in invariants, notation, and the algorithm have operational definitions or are explicitly marked `TBD`.
* If variants or profiles exist:
  * express them explicitly;
  * provide selection criteria;
  * distinguish common invariants from variant-specific ones.

6. Add “Sources and Attributions” in section 3.

* List sources with enough precision for lookup.
* Mark near-direct borrowings separately from synthesized claims.
* Record discrepancies and how they were handled.
* Record any repository-local terminology or boundary constraints that influenced the synthesis.

7. Self-check.

Verify all of the following before finalizing:

* no source references appear inside section 2;
* all terms have operational definitions or explicit `TBD`;
* each invariant has a concrete verification method and a concrete falsifier;
* section 2.4 is present only if its inclusion criteria are met;
* section 3 contains enough traceability to audit the synthesis;
* the concept does not duplicate an adjacent concept without an explicit boundary split.

## Result Structure (strict)

### 1. Source Analysis (internal step)

Do not include this section in `concepts/<...>.md`.

Use it only as an internal working step and as the basis for section 3.

### 2. Concept spec: "{{CONCEPT_NAME}}"

#### 2.1. Intention

Describe:

* why the concept is used;
* what repeated ambiguity, judgment, or design choice it standardizes, reduces, or removes;
* in which tasks it provides observable benefit.

Keep this operational.
Do not teach the background literature here.

#### 2.2. Ontological Status

Describe:

* what the concept is:
  * model;
  * analysis method;
  * notation;
  * artifact;
  * design principle;
  * other.
* what it is not;
* one or more operational distinction rules, if confusion with adjacent concepts is likely;
* scope boundaries and non-goals.

#### 2.3. Concept Invariants

List the statements without which the concept ceases to be itself.

For each invariant, specify:

* how it can be verified from artifact, code, text, model, or explicit checks;
* what would falsify it, using a concrete counter-signal.

If the concept has variants or profiles, include:

* a list of variants;
* selection criteria for each;
* which invariants are common across all variants;
* which invariants are variant-specific.

If the concept is weakly invariant or mostly classificatory, state that explicitly and keep only the stable invariant core.

#### 2.4. Minimal Formalization (optional)

Include this section only if at least one of the following is true:

* the concept defines a structured artifact that must be produced or validated;
* the concept introduces stable element types that require an explicit list to prevent drift;
* machine-checkable structure is required for reliable application.

If included, choose the smallest adequate mode.

A) Artifact schema mode

Include:

* element types and their meaning;
* mandatory vs. optional elements;
* a minimal textual format suitable for validation;
* one minimal normative example, with no explanations.

B) Vocabulary mode

Include:

* the minimal set of terms required for correct application;
* operational definitions for each term.

If this section is omitted, ensure all necessary operational definitions appear in sections 2.2–2.3.

#### 2.5. Construction Algorithm

Describe how to construct the target artifact or apply the concept in practice.

Use numbered steps.

Formulate each step as a verifiable operation, not as advice.

For each step, specify:

* input;
* output:
  * what must appear in the artifact;
  * or, if the concept is a principle rather than an artifact, what observable code or design outcome must exist.

If the concept does not produce a standalone artifact, describe a procedure of application rather than a document-construction routine.

#### 2.6. Typical Errors (anti-patterns)

List typical mistakes and distortions.

For each error, specify:

* how to detect it from artifact, code, or text;
* what to highlight to the user;
* what may be auto-corrected without questions.

Auto-correction is limited to:

* structural formatting fixes;
* terminology normalization to existing repository terminology, but only when meaning is preserved and no source-conflict resolution or boundary change is introduced;
* explicit violations of the output contract.

Do **not** auto-correct:

* invariant meaning;
* boundary choices;
* variant selection;
* source-conflict resolution.

### 3. Sources and Attributions

#### 3.1. Sources

Provide a bibliography list with enough precision for lookup:

* author;
* title;
* year;
* section, pages, or URL, as applicable.

#### 3.2. Direct Borrowings

Enumerate statements or definitions that are near-direct borrowings.

For each borrowing, point to the corresponding source location.

#### 3.3. Synthesized Elements

Enumerate key synthesized claims, especially:

* invariants;
* variants;
* distinction rules;
* algorithm steps.

For each synthesized claim, list which sources support it, or mark it as `emergent synthesis`.

#### 3.4. Discrepancies and Resolutions

List source discrepancies relevant to the concept.

For each discrepancy, record how it was handled:

* variant or profile declared; or
* universal formulation chosen.

When a universal formulation is chosen, state the rationale as a constraint-driven framework choice, not as absolute truth.

Also record any repository-local terminology or boundary constraints that affected the resolution.
