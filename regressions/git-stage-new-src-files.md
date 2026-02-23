# Regression: Stage new `src/` files immediately (avoid forgotten untracked files)

## Prompt fragment

- RU: "добавь новый файл" / "вынеси в отдельный файл" / "создай helper".
- EN: "add a new file" / "extract to a new file" / "create a helper".

## Expected behavior

- If the agent creates a new file under any `src/` directory, it must stage it immediately after creation.
- Before reporting task completion, the agent must verify with `git status --porcelain` that there are no `??` entries under any `*/src/**` path.
- The agent must not report completion while a task-created `*/src/**` file is still untracked.

## Framework hook

- `agents/roles.md` (Developer base rules for staging).
- `conventions/git.md` (New `src/` files are tracked).
- `checklists/git.md` (Staging new files).
- `skills/git-working-tree-hygiene/SKILL.md` (Procedure and done gate).
