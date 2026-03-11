# AGENTS (template)

## 0. Priority

1. If `AGENTS.local.md` exists in this repository, read it before proceeding and follow it with higher priority than this file.
2. Global rules: see `.ai/ergo/agents/roles.md` and `.ai/ergo/conventions/`.
3. Framework index (start here): see `.ai/ergo/INDEX.md`.
4. If the framework is not located at `.ai/ergo/`, find `agents/roles.md` in the repository and open `INDEX.md` in the same directory tree.
5. Reusable skills: see `.ai/ergo/skills`.
6. Internal processes: see `.ai/ergo/processes`.
7. If the user asks to “use a skill”, open that skill’s `SKILL.md` and follow it.
   - If the user provides a path: open `<path>/SKILL.md`.
   - If the user provides a skill name: locate the framework root (the directory that contains `agents/roles.md`, `skills/`, and `processes/`) and open `skills/<name>/SKILL.md`.
   - If `skills/<name>/SKILL.md` does not exist: look for a unique matching `<framework-root>/processes/**/<name>/SKILL.md` as a backward-compatible fallback.
   - If the lookup is not unique or is not found: ask the user for the exact path to the skill or process step directory.
8. If the user provides a path to a process step directory, open `<path>/SKILL.md` and follow it.
   - If the user provides only a process step directory name: locate the framework root (the directory that contains `agents/roles.md`, `skills/`, and `processes/`) and follow a unique matching `<framework-root>/processes/**/<name>/SKILL.md`.
   - If the lookup is not unique or is not found: ask the user for the exact path to the process step directory.
9. Before committing/pushing, and before reporting task completion, use the `git-working-tree-hygiene` skill.

## 1. Task triage

Before non-trivial coding, refactoring, or review, locate the framework root (the directory that contains `agents/roles.md`, `skills/`, and `processes/`) and use its `INDEX.md` and `checklists/README.md` to perform task triage.
Determine the current activity lens and artifact lens.
Read the union of mandatory checklist packs before proceeding with the main task.
If a reusable skill matches, open it after the mandatory checklist packs have been read.

## 2. Project context

- `APPLICATION-CONTEXT.md` — the repository structure.
- `SYSTEM-CONTEXT.md` — the structure of the entire system/workspace.

## 3. Development commands (example)

- Tests: `<command>`
- Linter/static analysis: `<command>`
- Build: `<command>`

## 4. Project exceptions

Only project-specific rules and exceptions are described here.

## 5. Project-local references

- Canonical project-local root in the target repository: `.ai/project-local/`.
- In framework materials, project-local links must be written as `<project-local>/...`.
- Interpret `<project-local>/...` as a link to project-local contexts that live in the target repository, not in the framework submodule.
- First, check the file at `.ai/project-local/...` by substituting the suffix from `<project-local>/...`.
- If the file does not exist at the canonical path, find it by searching the repository by file name and use the discovered path.
- If multiple candidates are found, ask the user to specify the correct path.
- If there are no candidates, ask the user where project-local is located in the project and use that path.
