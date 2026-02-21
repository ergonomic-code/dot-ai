# Checklist: Classes

Primary reference is `../conventions/ea-principles.md` (EA.C1–EA.C6).

## Dependency shape

- The application-level dependency graph is acyclic.
- Application dependency chains stay within the depth budget, or the deviation is explicitly recorded.
- Constructor-injected dependencies prefer interfaces/abstract classes over concrete implementations.

## Size and cohesion

- Classes stay within the field budget (7 ± 2) or are decomposed.
- Class fields serve a single responsibility and are used by most methods.

## State and effects

- Application classes avoid mutable fields and avoid “immutable fields holding mutable types”.
- Effects per class are minimized to the smallest set of external resources required by the responsibility.

## Naming

- Class suffixes reflect the component kind (`*Controller`, `*Listener`, `*Scheduler`, `*Op`, `*Repo`, `*Client`, `*Conf`, and DTO suffixes).
- `*Service` usage is explicitly justified and tracked as a refactoring target toward a more specific suffix.

## Links

- EA principles: `../conventions/ea-principles.md`.
- Component naming: `../ergo/tech/jvm/coding-conventions/naming.md`.
