# AGENTS (template)

## 0. Priority

1. If `AGENTS.local.md` exists in this repository, read it before proceeding and follow it with higher priority than this file.
2. Global rules: see `.ai/ergo/agents/roles.md` and the relevant files under `.ai/ergo/conventions/`.
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
9. Before staging, committing, pushing, or reporting task completion after making file changes, locate the framework root if needed, read `<framework-root>/conventions/git.md`, and use the `git-working-tree-hygiene` skill.
10. Before making branch or git workflow decisions such as branch creation or naming, commit messages, merge requests, or pull/rebase strategy, read `<project-local>/GIT-CONVENTIONS.md` if it exists. If `<project-local>/GIT-CONVENTIONS.md` does not exist, continue with the framework git conventions only.

## 1. Context loading

For narrow questions, prefer the smallest context that can answer the task correctly.
If the user references a concrete file, symbol, test, or error, read that target before any repository-wide context documents.
For implementation and review tasks with a concrete target, inspect that target and its immediate neighbors before selecting checklist packs.
After mandatory startup materials, load nearby code lazily: referenced types, helper functions, direct call sites, and adjacent tests.
Do not read `APPLICATION-CONTEXT.md` or `SYSTEM-CONTEXT.md` by default for a single-file or single-symbol question.
Open high-level context documents only when local code is insufficient, repository or module boundaries are unclear, or the task is architectural or cross-repo.
Before opening another broad document, ask whether it is likely to change the answer materially; if not, continue with local code search.

## 2. Task triage

Before non-trivial coding, refactoring, or review, locate the framework root (the directory that contains `agents/roles.md`, `skills/`, and `processes/`) and use its `INDEX.md` and `checklists/README.md` to perform task triage.
Determine the current activity lens and artifact lens from the concrete target, failing command, or directly adjacent code first, not from the broad ticket text alone.
Start with the smallest mandatory checklist set justified by that visible evidence.
When the same concern is covered by overlapping packs, prefer the more specific pack set selected by the routing matrix instead of preloading every plausible pack.
If local inspection reveals another real concern, load the additional mandatory pack just before making that class of change.
If a reusable skill matches, open it after the mandatory checklist packs have been read.

## 3. Project context

- `APPLICATION-CONTEXT.md` — the repository structure.
- `SYSTEM-CONTEXT.md` — the structure of the entire system/workspace.

## 4. Development commands (example)

- Tests: `<command>`
- Linter/static analysis: `<command>`
- Build: `<command>`

## 5. Project exceptions

Only project-specific rules and exceptions are described here.

## 6. Project-local references

- Canonical project-local root in the target repository: `.ai/project-local/`.
- In framework materials, project-local links must be written as `<project-local>/...`.
- Interpret `<project-local>/...` as a link to project-local contexts that live in the target repository, not in the framework submodule.
- First, check the file at `.ai/project-local/...` by substituting the suffix from `<project-local>/...`.
- If the file does not exist at the canonical path, find it by searching the repository by file name and use the discovered path.
- If multiple candidates are found, ask the user to specify the correct path.
- If there are no candidates, ask the user where project-local is located in the project and use that path.
