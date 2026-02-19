# Checklist: Architecture

Primary reference is `../conventions/ea-principles.md` (EA.C1, EA.C3, EA.C6).

## Dependency graph

- The application-level dependency graph is acyclic.
- Module boundaries are explicit, and cross-module dependencies are intentional.
- Application dependency chains stay within the depth budget, or the deviation is explicitly recorded.

## Effects and blast radius

- Prefer having an explicit inventory of external effects per operation or class (resources read/written, outbound calls).
  Prefer grouping effects at reusable abstraction levels over exhaustive low-level per-operation lists.
- When adding new write effects, reassess operation/class cohesion and blast radius.
  If an operation reaches 5+ independent effects on external resources/integrations, explicitly consider decoupling effects via an event.

## Links

- EA principles: `../conventions/ea-principles.md`.
- Structure chart: `../concepts/structure-chart.md`.
