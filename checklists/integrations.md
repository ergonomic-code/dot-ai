# Checklist: Integrations

Primary reference is `../conventions/contracts.md` and `../conventions/ea-principles.md` (EA.F4, EA.T1).

## Contracts and mapping

- Integration keys, field names, encodings, and value sets have a single stated source of truth.
- Mapping between domain terms and integration terms is explicit and localized to adapters.
- Boundary translators expose source and target vocabularies explicitly and do not mix in independent business decisions.
- Backward compatibility expectations are explicit for any externally consumed interface.

## Testing

- For each critical integration, tests verify the observable effect and the reaction to typical failures.
- Fakes or emulators are preferred for expensive or unstable external dependencies.

## DSL semantics

- If the integration uses a DSL with non-obvious semantics, restate the logic in the DSL terms and validate it with explicit examples.
- If the DSL has size, ordering, or expressiveness limits, make those limits explicit and design within them.

## Links

- Contracts: `../conventions/contracts.md`.
- EA principles: `../conventions/ea-principles.md`.
- Subprogram level of abstraction: `../concepts/subprogram-level-of-abstraction.md`.
