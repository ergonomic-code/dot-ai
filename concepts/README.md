# Concepts

This directory contains concept specifications used by agents and humans.
Each concept is written as a verifiable operational spec.

## Index

- [`command-query-separation.md`](command-query-separation.md) — Command–Query Separation (CQS) as an operation-level contract rule (commands change state, queries do not).
- [`effects-diagram.md`](effects-diagram.md) — A behavioral model “event → operation → effects on resources.”
- [`epochal-time-model.md`](epochal-time-model.md) — A model for reasoning about change as atomic transitions between immutable snapshots.
- [`ergonomic-components-structure.md`](ergonomic-components-structure.md) — A runtime structure model for backend services as a graph of long-lived components.
- [`ergonomic-data-model.md`](ergonomic-data-model.md) — A data modeling discipline with budgets and constraints to keep change local.
- [`irw-matrix-analysis.md`](irw-matrix-analysis.md) — IRW analysis and the IRW matrix for mapping operations to data reads/writes.
- [`making-illegal-states-unrepresentable.md`](making-illegal-states-unrepresentable.md) — A modeling technique that prevents invalid state combinations through representation and construction boundaries.
- [`structure-chart.md`](structure-chart.md) — A structural design model for control decomposition and explicit inter-module interfaces.
- [`testing-philosophy.md`](testing-philosophy.md) — What “good tests” mean in EA and how to choose test levels and doubles.
- [`testing-speed-budgets.md`](testing-speed-budgets.md) — How to treat test speed as a constraint with budgets and regressions handling.
- [`testing-testcode-architecture.md`](testing-testcode-architecture.md) — A dependency model for scenario test code (`*HttpApi`, `*TestApi`, `*Fixture`, `*FixturePresets`).
