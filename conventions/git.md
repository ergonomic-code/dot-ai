# Git conventions

## Rule: New `src/` files are tracked (including multi-module repos)

If you create a new file under any `src/` directory (for example `src/...` or `app-core/src/...`), add it to git in the same branch or PR.
Do not leave new `*/src/**` files untracked locally at the end of the task.

### How to verify

Run `git status --porcelain` and ensure there are no unexpected `??` entries.
Optionally run `git ls-files --others --exclude-standard | grep -E '(^|/)src/'` for a focused check.

### How to fix

Stage new files with `git add -- <path>`.
If you created multiple files, stage them in one go after checking `.gitignore`.

Exceptions:
- Build artifacts and generated outputs that belong in `.gitignore`.
- Temporary local files.

## Rule: Renames and moves are staged (especially under `src/`)

If you rename or move a tracked file, stage the rename before reporting task completion or making a commit.
Prefer `git mv` for renames and moves to avoid leaving a deleted + untracked pair in the working tree.

### How to verify

Run `git status --porcelain` and ensure there are no unexpected `D` / `??` pairs that represent an unstaged rename.
Treat this as a hard rule for any `*/src/**` path.

### How to fix

Either redo the operation with `git mv`, or stage both paths explicitly.

Examples:

- `git add -- <old-path> <new-path>`
- `git add -A -- <dir>`
