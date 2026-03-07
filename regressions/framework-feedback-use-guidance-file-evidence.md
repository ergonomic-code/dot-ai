# Regression: Framework-feedback skills must use exported guidance-file evidence when present

## Prompt fragment

- RU: "улучши фреймворк по exported chat artifacts".
- RU: "в транскрипте есть guidance files considered".
- EN: "improve the framework from exported chat artifacts".
- EN: "the transcript includes guidance files considered".

## Expected behavior

- If exported `transcript.md` contains `### Guidance files considered`, framework-feedback skills must inspect that section.
- The analysis must distinguish at least three cases:
  - wrong guidance selection;
  - wrong guidance precedence;
  - right guidance read, but not enforced by the workflow.
- The chosen patch must prefer the real enforcing lever that governs read order, source of truth, scope boundaries, or stage sequencing.
- The skills must not treat guidance-file evidence as proof of hidden instructions or as evidence about files that were never visibly discovered.

## Framework hook

- `.ai/skills/improving-coder-framework-from-feedback/SKILL.md` (Inputs).
- `.ai/skills/improving-coder-framework-from-feedback/SKILL.md` (Establish the evidence bundle).
- `.ai/skills/improving-coder-framework-from-feedback/SKILL.md` (Extract mistake patterns).
- `.ai/skills/improving-coder-framework-from-feedback/SKILL.md` (Map each mistake pattern to a framework lever).
- `.ai/skills/improving-coder-framework-from-feedback/SKILL.md` (Quality criteria).
- `.ai/skills/improving-designer-framework-from-feedback/SKILL.md` (Inputs).
- `.ai/skills/improving-designer-framework-from-feedback/SKILL.md` (Establish the evidence bundle).
- `.ai/skills/improving-designer-framework-from-feedback/SKILL.md` (Extract design failure patterns).
- `.ai/skills/improving-designer-framework-from-feedback/SKILL.md` (Map each failure pattern to a framework lever).
- `.ai/skills/improving-designer-framework-from-feedback/SKILL.md` (Quality criteria).
