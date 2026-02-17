# Git conventions

## Rule: New `src/` files are tracked

If you create new files under `src/`, add them to git in the same branch/PR.
Do not leave new `src/` files untracked locally.

Exceptions:
- build artifacts and generated outputs that belong in `.gitignore`;
- temporary local files.
