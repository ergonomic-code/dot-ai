# Checklist: API Design

Primary reference is `../conventions/ea-principles.md` (EA.D5, EA.F4, EA.F7) and `../conventions/contracts.md`.

## Contracts

- Canonical terms are consistent across HTTP/RPC, domain, persistence, and integrations.
- If a concept exists on multiple surfaces, a contract map explicitly documents naming, encoding, and sources of truth.

## Model shape

- API models do not encode “modes” as sets of optional/nullable fields.
- Illegal states implied by invariants are made unrepresentable where feasible, or rejected at the boundary with explicit validation and diagnostics.

## Behavior

- Commands change state and return only acknowledgment and generated data (e.g., ids, timestamps, server-assigned defaults, revision/version), not a read projection of existing state.
- Queries do not change observable state and do not have hidden effects.
- Mixed “change + return a read projection of state” operations are split into a command + a follow-up query, or recorded as an explicit exception.

## Links

- EA principles: `../conventions/ea-principles.md`.
- Contracts: `../conventions/contracts.md`.
- CQS: `../concepts/command-query-separation.md`.
- Illegal states: `../concepts/making-illegal-states-unrepresentable.md`.
- Skill: `../skills/api-design-cqs/SKILL.md`.
