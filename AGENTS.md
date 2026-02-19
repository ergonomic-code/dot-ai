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
- Language: all framework content Markdown documents must be written in English.

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

At the beginning of a new chat in this repository, ensure you can quickly locate a relevant skill later.
Prefer a cached, metadata-only skill index stored on disk, and only rebuild it when needed.

The skill index contains only YAML front matter metadata:
- `name`
- `description`

Index sources:
- `./skills/`
- `./.ai/skills/`

Caching and invalidation:
- Store the index at `.ai/.cache/skills-index.json`.
- Rebuild the index only if the cache is missing or if any `SKILL.md` in the sources has changed since the cache was built.
- Keep chat output minimal, and do not print the full index unless the user asks.

Cache format (minimal):
- `built_at_epoch_ms`: number
- `sources`: array of source directories scanned
- `files`: array of objects:
  - `path`: string (path to `SKILL.md`)
  - `mtime_epoch_ms`: number (last modified time when indexed)
  - `name`: string
  - `description`: string

Cache validity (mtime-based):
- If any indexed `SKILL.md` has a different `mtime` than recorded, rebuild.
- If any new `SKILL.md` appears in the sources that is not present in the cache, rebuild.
- If any cached `SKILL.md` no longer exists, rebuild.

Chat output:
- On cache hit or rebuild, print at most a single short status line (for example: `skills-index: loaded (N), cache_hit=true`).
- Only print the full index when the user asks.

When a specific skill is selected for use, only then read that skill's `SKILL.md` beyond its YAML front matter.
