---
name: designing-effects-diagram-from-requirements
description: "Building an effects diagram from requirements (user stories, scenarios, list of integrations, external operation contracts): extracts events/operations/resources, records reads/writes as effects, identifies requirement gaps through questions, and saves the diagram in textual format (YAML/JSON). Use when formalizing requirements, estimating scope, planning implementation, and validating target behavior before changes."
---

# Effects diagram: design new diagram from requirements

See the definition and format of the diagram in `concepts/effects-diagram.md`.

## Input

- `REQUIREMENTS` — requirements text (scenarios, epic, list of external operations, integrations, constraints).
- `TARGET_DIAGRAM_PATH` — path where the diagram should be saved (e.g., `effects-diagram.target.yaml`).
- Optional: `TARGET_DIAGRAM_VISUAL_PATH` — path where a human-readable visual representation should be saved (e.g., `effects-diagram.target.md` with Mermaid).

## Output

- Effects diagram in `TARGET_DIAGRAM_PATH`.
- Mermaid visual representation of the diagram (if `TARGET_DIAGRAM_VISUAL_PATH` is provided).
- List of requirement-related questions that block unambiguous effect definition (`TBD`).

## Algorithm

1. Fix the `scope` boundary.  
   Clarify which part of the system the requirements describe and what level of detail is needed.
2. Extract events (`events`).  
   Collect input types expressed as “when/upon/on schedule”.  
   For each event, add at least one target operation or mark as `TBD`.
3. Extract operations (`operations`).  
   Collect verbal statements like “the system shall …” as separate operations.  
   Merge duplicates and split “overly large” operations by distinct external goals.
4. Extract resources (`resources`).  
   Collect storages and integrations as resources.  
   Verify that each resource represents either a state domain or an external interface (API).
5. Build effects (`effects`).  
   For each operation, record which resources are read (`read`) and which are modified (`write`).  
   Add minimally sufficient `data` to make effects testable (what exactly is read/written).
6. Add triggers (`triggers`).  
   Link events to operations.
7. Validation and questions.  
   Check invariants from `concepts/effects-diagram.md`.  
   Produce a minimal list of questions resolving `TBD` in `write` effects and input events.
8. Save the result to `TARGET_DIAGRAM_PATH`.
9. If `TARGET_DIAGRAM_VISUAL_PATH` is provided, generate a Mermaid representation according to the rules in `concepts/effects-diagram.md` and save it.

## Minimal order of clarification questions

Ask questions strictly in order of impact on system behavior.

1. Which events are entry points (and which are critical)?
2. Which resources are sources of truth (where does state live)?
3. Which operations must perform writes, and which are read-only?
4. Where is atomicity required (which writes must be consistent)?
5. Which effects are forbidden (what must “not” happen)?

## Common warnings

- If requirements describe user steps, do not convert them directly into operations.  
  Operations must describe system intentions and its effects on resources.
- If an operation results in multiple independent `write` effects, explicitly highlight the risk and request clarification on consistency constraints.
