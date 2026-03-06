# Regression: Framework feedback skill must use canonical path resolution and the real enforcing lever

## Prompt fragment

- RU: "доработай фреймворк по fix-up commit'ам".
- RU: "внеси правки в skill / role / bootstrap по истории git".
- EN: "improve the framework from fix-up commits".
- EN: "patch the skill / role / bootstrap based on git history".

## Expected behavior

- The skill must treat `PROJECT_DIR` as the evidence repository for git inspection.
- The skill must resolve the framework root and `<project-local>` via `AGENTS.md` and `bootstrap/AGENTS.md` instead of hardcoding a single checkout path.
- In framework materials, project-local references must stay written as `<project-local>/...`.
- `framework-repo` mode must clearly distinguish the framework patch target from the evidence repository.
- If both the current framework repo and a framework checkout inside `PROJECT_DIR` are available and resolve to different filesystem paths, the skill must ask for explicit `PATCH_MODE` instead of guessing.
- The skill must allow framework patches in the actual enforcing artifact, including `agents/`, `skills/`, `processes/`, `bootstrap/`, `conventions/`, `concepts/`, `regressions/`, and scripts/assets, instead of forcing every change into `ergo/core|tech`.

## Framework hook

- `.ai/skills/improving-framework-from-feedback/SKILL.md` (Inputs).
- `.ai/skills/improving-framework-from-feedback/SKILL.md` (Output).
- `.ai/skills/improving-framework-from-feedback/SKILL.md` (Resolve the evidence repo, framework root, and project-local root).
- `.ai/skills/improving-framework-from-feedback/SKILL.md` (Decide where the fix belongs: framework layer vs project-local).
- `.ai/skills/improving-framework-from-feedback/SKILL.md` (Implement minimal framework patches).
- `.ai/skills/improving-framework-from-feedback/agents/openai.yaml`.
- `AGENTS.md` (Artifact paths when integrating the framework).
- `bootstrap/AGENTS.md` (Project-local references).
