# Code hygiene

## Intention

This document defines universal coding conventions for keeping codebases simple, coherent, and easy to evolve.
In this context, `duplication` includes semantically equivalent code that can be deduplicated with small, low-risk refactoring.
It is not limited to textually identical snippets.

## Rule: Overloads delegate to a canonical implementation

If multiple overloads represent the same operation, choose one canonical implementation and delegate the other overloads to it.

### How to verify

- Overloads do not re-implement the same logic (even if the code is not textually identical), for example serialization, schema loading, or common request building.
- A reader can point to one canonical overload that contains the real implementation.

### How to fix

- Keep one overload as canonical.
- Rewrite other overloads to delegate to it by adapting parameters.

### Exceptions

- External API compatibility, when the overload set is constrained by a public interface.

## Rule: No dead parameters in shared helpers

Do not add or keep parameters that do not change observable behavior at any call site.

### How to verify

- Every parameter is used either in the function body or by at least one call site for an observable behavior difference.

### How to fix

- Remove the parameter and simplify call sites.
- If the parameter must exist for compatibility, deprecate it and record a removal plan.

### Exceptions

- Public API stability requirements, when the parameter cannot be removed yet.
