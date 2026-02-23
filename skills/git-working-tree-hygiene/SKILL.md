---
name: git-working-tree-hygiene
description: "Pre-flight git hygiene before commits and before reporting completion: detect and resolve untracked `*/src/**` files and unstaged renames/moves."
---

# Git: Working Tree Hygiene

## Goal

Keep the working tree clean and correctly staged before commits and before reporting task completion.
Prevent forgotten untracked `*/src/**` files and accidental delete + untracked pairs after moves.

## Procedure

1. Run `git status --porcelain` and read the entire output.
2. If there are untracked files under any `*/src/**` path, decide for each file whether it belongs to the task.
3. For task-created `*/src/**` files, stage them with `git add -- <path>`.
4. For accidental or generated files under `*/src/**`, delete them or add them to `.gitignore` only if they are truly generated artifacts.
5. If a rename/move appears as a `D` entry plus an untracked `??` entry, stage both paths or redo the operation with `git mv`.
   Example: `git add -- <old-path> <new-path>`.
6. Re-run `git status --porcelain` and ensure the output matches expectations.
7. Before committing, run `git diff --stat` and ensure only intentional files are included.

## Done gate

- `git status --porcelain` shows no unexpected changes.
- There are no untracked files under any `*/src/**` path.
- There are no accidental `D` + `??` pairs that represent an unstaged rename or move.

## Notes

- Prefer staging explicit paths over `git add -A` unless the user explicitly asks to stage everything.
- If you are not sure whether a file is generated or should be tracked, stop and ask the user.
- References: `../../conventions/git.md` and `../../checklists/git.md`.
