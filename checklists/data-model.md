# Checklist: Data Model

Primary reference is `../conventions/ea-principles.md` (EA.D1–EA.D5).

## Immutability

- Domain records, entities, and value objects are immutable in the application core.
- State changes are expressed as creating a new value version and persisting it through a repository/resource.

## Shape and invariants

- The graph of references between domain types is acyclic (a DAG).
- Record, entity, and value object types stay within the field budget (<= 10 fields).
  If a type exceeds the budget, it is decomposed unless a project-level exception is explicitly recorded.
- Invariants are encoded in types and variants rather than as dependent nullable fields.
- Mutually exclusive “modes” are represented as explicit variants (sum types) rather than optional-field combinations.

## Links

- Data model concept: `../concepts/ergonomic-data-model.md`.
- Illegal states: `../concepts/making-illegal-states-unrepresentable.md`.
- Cross-surface contracts: `../conventions/contracts.md`.
