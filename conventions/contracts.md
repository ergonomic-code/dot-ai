# Contracts and Sources of Truth

## Intention

This document defines conventions that reduce rework caused by terminology drift and contract mismatches.
The goal is to make cross-surface changes (HTTP ↔ domain ↔ DB ↔ integrations) explicit and testable.

## Rule: One canonical term per concept

Pick one canonical name for each domain concept.
Define it once in the spec glossary.
Do not introduce synonyms in different layers (for example, `languageCohort` vs `languageTag` for the same thing).

## Rule: Create a contract map for cross-surface concepts

If a concept appears in more than one contract surface, document the mapping explicitly.
Use a table that maps the same concept across:

- HTTP (field / query param / header / payload path).
- Persistence (table / column / JSON path).
- Integration keys (external tags, headers, message fields).
- Encoding (casing, allowed values, discriminator representation, JSON vs DB format).

This contract map is a primary rework minimizer.

## Rule: No isomorphic DTOs (DTO == domain)

An isomorphic DTO is a DTO type that is identical to the domain model in:

- field set and field types,
- required vs optional fields (nullability),
- default values,
- discriminators and polymorphism (if any),
- contract encoding (field names, casing, date formats, unknown fields handling).

Rules:

- If the HTTP/API contract is isomorphic to the domain model, introducing a dedicated DTO type is forbidden.
- In that case, the API must reuse the domain types as API models.
- Dedicated DTO types are allowed only if there is an explicit contract delta (at least one intentional contract difference).
- If a dedicated DTO exists, the contract delta must be documented in the Execution-Spec.
- If an isomorphic DTO is proposed “for layering / cleanliness / dependencies”, the author must stop and ask for explicit approval, and record the reason as a hard constraint.

Allowed reasons for a dedicated DTO:

- backward compatibility (deprecated/alias fields),
- security / permissions shaping (hide or expose fields intentionally),
- different encoding (field names/casing/date formats/unknown fields policy),
- different value sets or validation rules,
- different variant shape or discriminator strategy.

## Rule: Make illegal states unrepresentable

Prefer type shape that makes invalid states not representable.
Prefer sum types for mutually exclusive states and refined types for constrained values.
If surface constraints make this impossible, enforce invariants at construction time at the boundary, and use validation only as a last resort.
See `../concepts/making-illegal-states-unrepresentable.md`.

## Rule: State sources of truth for value sets and dictionaries

For any value set that is validated or constrained, name the single source of truth.
Prefer reuse of an existing shared artifact (a validator, a constant list, a module-level API) over creating a local enum or duplicate list.
If a duplicate is required, state why and how drift is prevented.
