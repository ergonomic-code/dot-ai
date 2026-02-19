# Checklist: API Design

Primary reference is `../conventions/ea-principles.md` (EA.D5, EA.F4, EA.F7) and `../conventions/contracts.md`.

## Contracts

- Canonical terms are consistent across HTTP/RPC, domain, persistence, and integrations.
- If a concept exists on multiple surfaces, a contract map explicitly documents naming, encoding, and sources of truth.

## Model shape

- API models do not encode “modes” as sets of optional/nullable fields.
- Illegal states implied by invariants are made unrepresentable where feasible, or rejected at the boundary with explicit validation and diagnostics.

## Behavior

- Commands change state and do not return unnecessary data.
- Queries do not change state and do not have hidden effects.

## Links

- EA principles: `../conventions/ea-principles.md`.
- Contracts: `../conventions/contracts.md`.
- Illegal states: `../concepts/making-illegal-states-unrepresentable.md`.
