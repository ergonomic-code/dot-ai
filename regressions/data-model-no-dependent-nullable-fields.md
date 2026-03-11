# Regression: Dependent nullable field groups are forbidden as model shape

## Prompt fragment

- RU: "два нуллабельных поля, одно из которых обязано быть не нуллабельным".
- RU: "если `a == null`, то `b != null`" / "`(a == null) == (b == null)`".
- EN: "two nullable fields where one must actually be non-null".
- EN: "if `a == null` then `b != null`" / "`(a == null) == (b == null)`".

## Expected behavior

- The agent must not model invariants as flat groups of nullable fields whose legality depends on relationships between those fields.
- Such shapes must be replaced with explicit variants, refined types, or boundary validation with clear diagnostics.
- The same prohibition applies to domain models, commands, and API contracts.

## Framework hook

- `bootstrap/AGENTS.md` (Task triage).
- `INDEX.md` (Task triage).
- `checklists/README.md` (Routing matrix).
- `conventions/ea-principles.md` (EA.D4 — Do not encode invariants as “dependent nullable fields”).
- `checklists/data-model.md` (Shape and invariants).
- `checklists/api-design.md` (Model shape).
