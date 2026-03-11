# Git conventions

## Rule: New `src/` files are tracked (including multi-module repos)

If you create a new file under any `src/` directory (for example `src/...` or `app-core/src/...`), add it to git in the same branch or PR.
Do not leave new `*/src/**` files untracked locally at the end of the task.
This is a blocking rule: do not send a task-completion message while any new `*/src/**` files remain untracked.

### How to verify

Run `git status --porcelain` and ensure there are no unexpected `??` entries.
Optionally run `git ls-files --others --exclude-standard | grep -E '(^|/)src/'` for a focused check.

### How to fix

Stage new files with `git add -- <path>`.
If you created multiple files, stage them in one go after checking `.gitignore`.

Exceptions:
- Build artifacts and generated outputs that belong in `.gitignore`.
- Temporary local files.

## Rule: Task-created files are tracked (even outside `src/`)

If you create a new file that is part of the task deliverable (docs, configs, scripts), add it to git in the same branch or PR.
Do not leave task-created deliverables untracked locally at the end of the task.
If you are unsure whether an untracked file is a deliverable or a local artifact, stop and ask.

### How to verify

Run `git status --porcelain` and review `??` entries for task-created deliverables.
Optionally run `git ls-files --others --exclude-standard` for a focused list of untracked files.

### How to fix

Stage new files with `git add -- <path>`.
Prefer explicit paths over `git add -A` unless the user explicitly asks to stage everything.

## Rule: Default `tmp/` artifacts stay local

Treat new files under `tmp/` as local scratch, evidence, or generated artifacts by default.
Do not stage or commit new `tmp/**` files unless the user explicitly asks to version them or the repository already tracks that exact path family as part of the task.
This applies in particular to chat exports, review notes, extracted images, ad-hoc prompts, and similar working artifacts.

### How to verify

Run `git status --porcelain` and review `?? tmp/...` entries separately from real deliverables.
If a `tmp/` path is already tracked and the task intentionally updates it, treat that tracked change according to task scope instead of this default.

### How to fix

Leave local `tmp/**` artifacts unstaged by default.
If a file under `tmp/` must become a deliverable, move it to a tracked location or get explicit user confirmation before staging it.

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
