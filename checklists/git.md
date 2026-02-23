# Checklist: Git

Primary reference is `../conventions/git.md`.

## Working tree hygiene

- `git status --porcelain` shows only intentional changes (no accidental changes or generated artifacts).
- No new files under any `*/src/**` directory remain untracked (`?? */src/...`).
- Renames and moves are staged (no accidental `D` + `??` pairs, especially under `*/src/**`).

## Staging new files

- New `*/src/` files created for the task are staged with `git add -- <path>`.
- Stage new `*/src/` files immediately after creating them (do not wait until the end of the task).
- New files are not added when they are intentionally ignored by `.gitignore`.

## Links

- Git conventions: `../conventions/git.md`.
