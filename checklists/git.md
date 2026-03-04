# Checklist: Git

Primary reference is `../conventions/git.md`.

## Working tree hygiene

- `git status --porcelain` shows only intentional changes (no accidental changes or generated artifacts).
- The staged set for the next commit matches the intended commit scope (`git diff --name-status --cached`).
- No intended changes are left unstaged (`git diff --name-status`).
- No new files under any `*/src/**` directory remain untracked (`?? */src/...`).
- Untracked files outside `*/src/**` are not staged or committed unless explicitly required by the task.
- Renames and moves are staged (no accidental `D` + `??` pairs, especially under `*/src/**`).
- `.gitignore` is modified only when the task explicitly requires changing ignore rules.

## Staging new files

- New `*/src/` files created for the task are staged with `git add -- <path>`.
- Stage new `*/src/` files immediately after creating them (do not wait until the end of the task).
- Prefer `git add -- <path>` over `git add -A` to avoid accidentally staging unrelated files.
- New files are not added when they are intentionally ignored by `.gitignore`.

## Links

- Git conventions: `../conventions/git.md`.
