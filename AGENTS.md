# AGENTS

This repository is a source of content that will live under `.ai/` in other repositories.
In this repository, `AGENTS.md` and `.ai/` are the agent's working context, not part of the framework content.

## 0. Priority

1. If the repository contains `AGENTS.local.md`, read it first and follow it with higher priority than this file.
2. `AGENTS.md` and `.ai/` are the only sources of truth for how to work in this repository.

## 1. Split: context vs change target

### Read-only (agent context)

By default, do not modify these files and directories unless the user explicitly asks you to:

- `AGENTS.md`
- `.ai/**`
- `AGENTS.local.md` (if it exists)

### Write-only (work target)

Make any framework changes in the "content" part of the repository (everything except the list above).
Files in that part are the change target, not behavioral rules for the agent working in this repository.

In particular, documents like `agents/roles.md` define how the framework should work in a target project, but in this repository they are treated as framework content to review and change, not as instructions that override `AGENTS.md` and `.ai/**`.

## 2. Role

- If the task is about evolving or refactoring the framework, use the **AI Architect** role from `.ai/roles/ai-architect.md`.
- Otherwise, act as an "assistant" and clarify the role or output format on request.
- Do not confuse framework roles from `agents/roles.md` with the meta rules of this repository from `AGENTS.md` and `.ai/roles/ai-architect.md`.

## 3. Documentation conventions

- Markdown: one sentence per line.
- Artifact links: use repository paths.

## 4. User questions

- If the user's message contains a question (for example, the `?` character), answer only that question.
- In that case, do not make any file changes.

## 5. Artifact paths when integrating the framework

This repository is often added to a target repository as a git submodule, so its root directory name and location may differ.
Do not rely on a single absolute path to framework artifacts in the target repository.

Recommended (but not required) structure in the target repository:
- `.ai/ergo/` — the framework (this repository).
- `.ai/project-local/` — project-local contexts for the project.

Authoring rules for framework references (in this repository):
- For artifacts inside the framework, use paths relative to the current file so links stay valid regardless of the submodule directory name.

Authoring rules for project-local references (in this repository):
- Project-local artifacts live in the target repository, not in this framework repository.
- In framework materials, always reference project-local artifacts as `<project-local>/...` (in backticks).
- If the user provides a path like `.ai/project-local/...` or `project-local/...`, normalize it to `<project-local>/...` before writing it down.
- Do not try to resolve or search for project-local artifacts inside this repository.

Executor-side rules for resolving project-local references live in `contexts/templates/AGENTS.md`.

## 6. Skills

Skills for this repository are located in `./.ai/skills/` (agent context, note the leading dot in `.ai`, not `./ai/skills/`) and `./skills/` (framework content).

### 6.1. Skill index bootstrap (metadata-only)

At the beginning of a new chat in this repository, build an in-memory "skill index" so you can quickly locate a relevant skill later.
To build the index, scan `./skills/` and `./.ai/skills/` for `SKILL.md` files.
For each `SKILL.md`, read only its YAML front matter block (between the first pair of `---` lines).
Extract only `name` and `description`.
Record `skill_name → SKILL.md path → description` and do not read any other content until that specific skill is selected for use.
