---
name: git-working-tree-hygiene
description: "Pre-flight git hygiene before commits and before reporting completion: resolve untracked task-created files (especially `*/src/**`), stage renames/moves, and verify that the staged set matches the intended commit scope."
---

# Git: Working Tree Hygiene

## Goal

Keep the working tree clean and correctly staged before commits and before reporting task completion.
Prevent forgotten untracked `*/src/**` files and accidental delete + untracked pairs after moves.
Prevent “I forgot to add files” incidents by verifying staged vs unstaged changes.
Prevent accidental commits of local `tmp/**` evidence and scratch artifacts.

## Procedure

1. Run `git status --porcelain` and read the entire output.
2. Identify which changes belong to the task deliverable (tracked and untracked).
3. If there are untracked files under any `*/src/**` path (`??` entries), decide for each file whether it belongs to the task.
4. For task-created `*/src/**` files, stage them with `git add -- <path>`.
5. For accidental or generated `*/src/**` files, delete them or add them to `.gitignore` only if they are truly generated artifacts.
6. If there are untracked files outside `*/src/**`, decide for each file whether it belongs to the task deliverable.
7. If there are untracked files under `tmp/`, treat them as local artifacts by default.
8. Do not auto-stage those `tmp/**` files.
   Delete or ignore them only when you know they are disposable artifacts created for this task.
   Otherwise leave them untouched unless the task explicitly requires versioning or cleanup, or the repository already tracks that exact path family.
9. For task-created non-`src/` files outside `tmp/` (docs, configs, scripts), stage them with `git add -- <path>`.
10. For accidental or generated non-`src/` files outside `tmp/`, delete them or add them to `.gitignore` only if they are truly generated artifacts.
11. If a rename/move appears as a `D` entry plus an untracked `??` entry, stage both paths or redo the operation with `git mv`.
   Example: `git add -- <old-path> <new-path>`.
12. Re-run `git status --porcelain` and ensure the output matches expectations.
13. Run `git diff --name-status --cached` and ensure all intended changes for the next commit are staged.
14. Run `git diff --name-status` and ensure there are no intended changes left unstaged.
15. Before committing, run `git diff --stat --cached` and ensure only intentional files are included.

## Done gate

- `git status --porcelain` shows no unexpected changes for the commit you are about to make.
- `git diff --name-status --cached` matches the intended commit scope.
- `git diff --name-status` shows no intended changes left unstaged.
- There are no untracked files under any `*/src/**` path.
- There are no task-created deliverable files left untracked outside `*/src/**`.
- There are no unintentionally staged local `tmp/**` artifacts.
- There are no accidental `D` + `??` pairs that represent an unstaged rename or move.

## Notes

- Prefer staging explicit paths over `git add -A` unless the user explicitly asks to stage everything.
- If you are making a partial commit, explicitly list what is intentionally left unstaged.
- Treat `tmp/**` as local by default unless the task scope clearly says otherwise.
- If you are not sure whether a file is generated or should be tracked, stop and ask the user.
- References: `../../conventions/git.md` and `../../checklists/git.md`.
