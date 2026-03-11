# Checklist: Calculations

Primary reference is `../conventions/ea-principles.md` (EA.F1–EA.F7), `../concepts/actions-calculations-data.md`, and `subprograms.md`.

Apply `subprograms.md` first.
This checklist contains only calculation-specific constraints.

## Purity and contract

- The calculation is pure relative to its contract.
- Input data is sufficient to derive the result.
- Hidden reads, hidden writes, and implicit effect dependencies are absent.
- Time, randomness, environment, and external lookup are passed in explicitly when needed.

## Calculation structure

- The result is derived by explicit transformation of input data.
- Branching logic remains locally understandable.
- Intermediate values are named by meaning when this reduces mental stack load.
- Prefer compositional transformations over stateful step-by-step mutation when this improves clarity.
- Mutable accumulators and manual control flow are avoided unless they are clearly simpler than declarative alternatives.

## Complexity budget

- Cognitive complexity budget for calculations is up to 15.
- Nested branching is minimized.
- Each transformation step is locally derivable from the previous one.
- The reader can reconstruct why the result is correct without tracking hidden state transitions.

## Modeling quality

- The result shape makes illegal states harder or impossible to represent.
- Mixed responsibilities such as validation, enrichment, and effect execution are not hidden inside the calculation.
- Domain rules are encoded in data shape or explicit transformation steps rather than dispersed incidental branching.

## Links

- EA principles: `../conventions/ea-principles.md`.
- Actions, Calculations, and Data: `../concepts/actions-calculations-data.md`.
- Subprogram level of abstraction: `../concepts/subprogram-level-of-abstraction.md`.
- Cohesion: `../concepts/cohesion.md`.
- Making illegal states unrepresentable: `../concepts/making-illegal-states-unrepresentable.md`.
