---
name: git-working-tree-hygiene
description: "Pre-flight git hygiene before commits and before reporting completion: resolve untracked `*/src/**` files, stage renames/moves, and verify that the staged set matches the intended commit scope."
---

# Git: Working Tree Hygiene

## Goal

Keep the working tree clean and correctly staged before commits and before reporting task completion.
Prevent forgotten untracked `*/src/**` files and accidental delete + untracked pairs after moves.
Prevent “I forgot to add files” incidents by verifying staged vs unstaged changes.

## Procedure

1. Run `git status --porcelain` and read the entire output.
2. If there are untracked files under any `*/src/**` path (`??` entries), decide for each file whether it belongs to the task.
3. For task-created `*/src/**` files, stage them with `git add -- <path>`.
4. For accidental or generated `*/src/**` files, delete them or add them to `.gitignore` only if they are truly generated artifacts.
5. If there are untracked files outside `*/src/**`, do not modify them unless the user explicitly asks.
6. If a rename/move appears as a `D` entry plus an untracked `??` entry, stage both paths or redo the operation with `git mv`.
   Example: `git add -- <old-path> <new-path>`.
7. Re-run `git status --porcelain` and ensure the output matches expectations.
8. Run `git diff --name-status --cached` and ensure all intended changes for the next commit are staged.
9. Run `git diff --name-status` and ensure there are no intended changes left unstaged.
10. Before committing, run `git diff --stat --cached` and ensure only intentional files are included.

## Done gate

- `git status --porcelain` shows no unexpected changes for the commit you are about to make.
- `git diff --name-status --cached` matches the intended commit scope.
- `git diff --name-status` shows no intended changes left unstaged.
- There are no untracked files under any `*/src/**` path.
- There are no accidental `D` + `??` pairs that represent an unstaged rename or move.

## Notes

- Prefer staging explicit paths over `git add -A` unless the user explicitly asks to stage everything.
- If you are making a partial commit, explicitly list what is intentionally left unstaged.
- If you are not sure whether a file is generated or should be tracked, stop and ask the user.
- References: `../../conventions/git.md` and `../../checklists/git.md`.
