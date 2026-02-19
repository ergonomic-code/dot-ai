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

## Rule: Make illegal states unrepresentable

Prefer type shape that makes invalid states not representable.
Prefer sum types for mutually exclusive states and refined types for constrained values.
If surface constraints make this impossible, enforce invariants at construction time at the boundary, and use validation only as a last resort.
See `../concepts/making-illegal-states-unrepresentable.md`.

## Rule: State sources of truth for value sets and dictionaries

For any value set that is validated or constrained, name the single source of truth.
Prefer reuse of an existing shared artifact (a validator, a constant list, a module-level API) over creating a local enum or duplicate list.
If a duplicate is required, state why and how drift is prevented.
