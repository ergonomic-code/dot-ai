---
name: synthesizing-framework-concepts
description: "Synthesis of an operational description of a new or modified framework concept based on sources (books/articles/methodologies/industry): extract invariants/variations/anti-patterns, then produce Concept spec + Skill spec + Workflow integration and a separate 'Sources and Attributions' section in order to add or revise materials in `concepts/`."
---

# Concept Description

This instruction describes how to synthesize a stable concept from a set of sources so that AI agents can use it.

The result is intended to be written to `concepts/<concept>.md` and used for further creation or updating of skills in `skills/`.

See an example of a completed concept spec in `concepts/effects-diagram.md`.

## Input

* `CONCEPT_NAME` — the name of the concept (as in the document title).
* `CONCEPT_SLUG` — a stable slug for the file path (lowercase + hyphen).
* `FRAMEWORK_STRUCTURE` — a brief description of the framework structure (concepts / skills / processes) or links to relevant files in the repository.
* `SOURCES` — a list of sources.
* Optional: `TARGET_CONCEPT_PATH` — target file path (default `concepts/<CONCEPT_SLUG>.md`).
* Optional: `TARGET_SKILLS` — a list of skills to create or update after the concept is finalized.

## Output

* A document structured according to sections 2–5 below (without section 1).
* A checklist of blocking questions if sources or context are insufficient.

## Constraints

* Do not retell the sources or “teach the reader.”
* Do not bind tightly to a single author or methodology.
* Do not use terms without operational definitions.
* Do not include sources inside the Concept spec body.
* If sources conflict, choose the more universal formulation and record the discrepancy in the “Sources and Attributions” section.

## Algorithm

1. Fix the task frame.

   * Confirm `CONCEPT_NAME` and `TARGET_CONCEPT_PATH`.
   * Determine which agents and tasks will use the concept.
2. Load the framework context.

   * Read `README.md` and `skills/README.md` if the structure is unclear.
   * Check whether a similar concept already exists in `concepts/`.
3. Analyze sources (internal step).

   * Extract invariants.
   * Extract variable elements.
   * Collect typical mistakes and distortions.
   * Record discrepancies between sources without attempting to “reconcile” them.
4. Synthesize the Concept spec.

   * Formulate each statement so it can be verified against text, model, or artifact.
   * Define minimal notation sufficient for AI, without overloading.
   * Describe the construction algorithm as verifiable operations, not advice.
5. Synthesize the Skill spec.

   * Define usage triggers and prohibitions.
   * Compile mandatory user questions in priority order.
   * Define quality criteria and signals to continue work.
6. Describe Workflow integration.

   * Indicate where in the typical process the concept should be invoked and what artifact is expected.
7. Add “Sources and Attributions.”

   * List sources.
   * Mark direct borrowings and synthesized elements.
8. Self-check.

   * No source references inside the Concept spec body.
   * All terms have operational definitions or explicit `TBD`.
   * Minimal notation is compatible with text serialization (YAML/JSON/table).
   * Sections 2–5 are present and completed.

## Result Structure (strict)

Below is the structure that must be followed in the final document.

### 1. Source Analysis (internal step)

Do not include this section in `concepts/<...>.md`.
Use it only as an internal working step and as a basis for the “Sources and Attributions” section.

### 2. Concept spec: "{{CONCEPT_NAME}}"

#### 2.1. Intention

* Why the concept is used.
* What mental work it replaces.
* In which tasks it provides measurable benefit.

#### 2.2. Ontological Status

* Define what it is (model / analysis method / notation / artifact / other).
* List what it is not.
* Provide an operational rule for distinguishing “similar but not the same.”

#### 2.3. Concept Invariants

* List statements without which the concept ceases to be itself.
* For each invariant, specify how it can be verified.

#### 2.4. Minimal Notation

* List element types (nodes/relations/fields) and their meaning.
* Separate mandatory and optional elements.
* Provide a minimal textual format (YAML/JSON/table) suitable for machine validation.

#### 2.5. Construction Algorithm

1. …
2. …
3. …

Formulate steps as verifiable operations.
For each step, specify input and output (what must appear in the artifact).

#### 2.6. Typical Errors (anti-patterns)

* List errors.
* For each error, specify:

  * how to detect it from the artifact;
  * what to highlight to the user;
  * what can be auto-corrected without questions.

### 3. Skill spec: using "{{CONCEPT_NAME}}" by an AI agent

#### 3.1. Usage Triggers

* Under which input signals the agent should propose the tool.
* Under which it should not.

#### 3.2. Questions to the User

* What questions to ask.
* In what order.
* Which answers may be marked as `TBD` without blocking progress.

#### 3.3. Quality Criteria

* Indicators of “good enough.”
* Indicators that further work is required.
