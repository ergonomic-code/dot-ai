# Regression: Cohesion guidance must allow sequential and communicational profiles under one responsibility

## Prompt fragment

- RU: "уточни cohesion" / "обнови EA.F3" / "оставим функцию целой, потому что шаги идут по порядку".
- RU: "это один метод, потому что всё работает с одним DTO".
- EN: "clarify cohesion" / "update EA.F3" / "keep the function together because the steps run in order".
- EN: "this stays one method because everything touches the same DTO".

## Expected behavior

- Function cohesion guidance must require one primary responsibility as the gate for high cohesion.
- Functional cohesion must remain the target profile.
- Sequential and communicational cohesion must remain acceptable profiles when they best explain how one responsibility is completed.
- Thin orchestrators may legitimately use sequential or communicational cohesion while staying within one scenario and one work item.
- Grouping by phase alone must remain insufficient.
- The subprogram checklist must keep the primary-responsibility and cohesion guidance.
- The operations checklist must phrase effect guidance in terms of intrinsic versus non-intrinsic effects.
- When this risky default is clarified, the principle, concept, and checklist must stay aligned.

## Framework hook

- `conventions/ea-principles.md` (EA.F3 — Ensure high function cohesion).
- `concepts/cohesion.md` (Invariant 2, Ordered cohesion profiles, Selection criteria).
- `checklists/subprograms.md` (Semantic clarity, Complexity).
- `checklists/operations.md` (Cohesion).
