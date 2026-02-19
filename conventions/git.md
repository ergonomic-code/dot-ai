# Git conventions

## Rule: New `src/` files are tracked

If you create a new file under `src/`, add it to git in the same branch or PR.
Do not leave new `src/` files untracked locally at the end of the task.

### How to verify

Run `git status --porcelain -- src/` and ensure there are no `??` entries.
Optionally run `git ls-files --others --exclude-standard -- src/` for a focused check.

### How to fix

Stage new files with `git add -- <path>`.
If you created multiple files under `src/`, use `git add -- src/` after checking `.gitignore`.

Exceptions:
- Build artifacts and generated outputs that belong in `.gitignore`.
- Temporary local files.
