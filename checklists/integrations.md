# Checklist: Integrations

Primary reference is `../conventions/contracts.md` and `../conventions/ea-principles.md` (EA.F4, EA.T1).

## Contracts and mapping

- Integration keys, field names, encodings, and value sets have a single stated source of truth.
- Mapping between domain terms and integration terms is explicit and localized to adapters.
- Backward compatibility expectations are explicit for any externally consumed interface.

## Testing

- For each critical integration, tests verify the observable effect and the reaction to typical failures.
- Fakes or emulators are preferred for expensive or unstable external dependencies.

## Links

- Contracts: `../conventions/contracts.md`.
- EA principles: `../conventions/ea-principles.md`.
