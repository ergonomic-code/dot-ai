# Regression: Stage renames and moves (avoid accidental `D` + `??` pairs)

## Prompt fragment

- RU: "переименуй/перемести файл".
- EN: "rename/move this file."

## Expected behavior

- If the agent renames or moves a tracked file, it must stage the rename or move.
- Prefer `git mv` for renames and moves.
- If `git mv` is not used, stage both paths explicitly (for example via `git add -- <old-path> <new-path>` or `git add -A -- <dir>`).
- The agent must verify with `git status --porcelain` that no unexpected `D` / `??` pairs remain.
- Treat this as a hard rule for any `*/src/**` path.

## Framework hook

- `agents/roles.md` (Developer base rules for staging and hygiene).
- `conventions/git.md` (Renames and moves are staged).
- `checklists/git.md` (Working tree hygiene).
