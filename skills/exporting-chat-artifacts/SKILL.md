---
name: exporting-chat-artifacts
description: Export `transcript.md` + `brief.md` from the current chat to reduce rework by improving the framework’s rules, templates, and checklists.
---

# Chat transcript export

## When to use

Use after completing a task or a major stage.
Use immediately when repeated clarifications or rework become noticeable.

## What counts as a “transcript”

A transcript is an evidence bundle for postmortems and framework improvements.
It must contain enough detail to reconstruct what happened and why.

Include:

* The dialogue as seen by the user (messages from **User** and **Assistant**).
* User-provided runtime context that was part of the dialogue (for example IDE context blocks and environment context blocks).
* A dedicated appendix with execution evidence (commands, changed files, test runs, errors) when it is available and relevant.

Keep user-authored request text verbatim wherever it is quoted or extracted into `transcript.md` or `brief.md`.
Do not paraphrase, translate, “improve,” or normalize that user-authored request text.
This verbatim rule has priority over the sanitization rules below.

Do not include:

* System/developer instructions (system prompt, developer message, sandbox/permission policy blocks).
* Internal chain-of-thought reasoning.
* Full raw tool dumps unless they are needed to understand the failure mode.

### Runtime context blocks (keep, but normalize)

If the user message contains an IDE context block (active file, open tabs, request), keep it.
If the user message contains an `<environment_context>` block, keep at least `cwd` and `shell`.
Prefer normalizing such blocks into a compact “Context” subsection rather than pasting raw harness headings.
Do not include raw code excerpts from the IDE selection unless the user explicitly requests it and it is safe to export.

### Markers that must be removed from non-user-authored draft material

If any of the following appears as harness or assistant/service scaffolding in a draft, it is not part of the transcript and must be deleted.
Do not delete these strings when they are part of verbatim user-authored text that must be kept.

* `# AGENTS.md instructions`
* `<INSTRUCTIONS>`
* `<permissions instructions>`
* `developer message`
* `system prompt`
* Any blocks containing assistant instructions / launch policies / sandbox descriptions

## Why export (purpose)

The purpose of export is to convert task execution experience into transferable artifacts.
These artifacts are then turned into more precise framework rules, templates, and checklists.
The resulting effect is reduced uncertainty, fewer clarifications, less rework, and shorter future chats.

## Recommended output: a two-file package

By default, generate a package in a single folder:

* `transcript.md` as the source of facts and context.
* `brief.md` as a condensed package suitable for modifying the framework.

If the chat contains multiple topics, ask which topic should be used for `brief.md`.
`transcript.md` remains complete within the chat scope.

## Structure of `brief.md`

* `# Brief`
* `## Task`
* `## Definition of Done`
* `## Context`
* `## Constraints`
* `## Decisions`
* `## Friction`
* `## Artifacts`
* `## Delta`
* `## Postmortem`

### Section contents

* `Task`: the goal in one sentence.
* `Definition of Done`: 3–7 bullet points.
* `Context`: what must be known to understand the task.
* `Constraints`: technologies, versions, prohibitions, time/resource limits.
* `Decisions`: forks, criteria, chosen option, consequences.
* `Friction`: where clarification was required, where the model misunderstood, where most rewriting occurred.
* `Artifacts`: final prompts, checklists, templates, commands, repository file references.
* `Delta`: 1–3 concrete framework changes to shorten similar future work.
* `Postmortem`: 5–10 lines on what worked and what did not.

When the brief includes user requests (for example in `Task`, `Definition of Done`, `Constraints`, `Friction`, or `Decisions`), copy them verbatim from the transcript.
Do not paraphrase, translate, “improve,” or normalize the wording.
This verbatim rule has priority over the sanitization rules below.

### Sanitization and security

Before writing files, sanitize only assistant-authored summaries, metadata, placeholder text, and execution evidence.
Do not redact or rewrite verbatim user-authored requests that you quote or extract into `transcript.md` or `brief.md`.
Replace sensitive data in non-user-authored text with placeholders when needed.
Example placeholders: `<TOKEN>`, `<EMAIL>`, `<INTERNAL_URL>`, `<PERSON>`, `<PROJECT>`.
In the execution evidence appendix, redact secrets and truncate large outputs to the minimum needed excerpt.
If verbatim user-authored text contains obvious secrets and the export destination or sharing scope is unclear, stop and ask whether to export that text as-is or omit the affected section.

## Where to export (variant selection)

First propose Variant A.
If the user requests otherwise, switch to Variant B.

### Variant A (recommended): new file package

1. Ask for the topic or short task slug.
2. Ask for the export folder path.
3. If not specified, suggest default: `tmp/chat-export/YYYY-MM-DD/<slug>/`.
4. Inside the folder use fixed names: `transcript.md` and `brief.md`.
5. If files already exist, request explicit overwrite confirmation or suggest another path.

### Variant B: single transcript file

1. **Into an open empty file** (active IDE tab).

   * Ask to confirm file path (e.g., `engineering-log/.../transcript.md`).
   * Verify that the file exists and is **empty** (size 0).
   * Otherwise suggest option (2) or request explicit overwrite confirmation.

2. **Into a new file**.

   * Ask for name/path.
   * If unspecified, suggest default: `tmp/chat-transcript-YYYY-MM-DD.md` (within repository).
   * Ensure file does not exist.
   * If it exists, suggest another name or request explicit overwrite confirmation.

## File format (Markdown)

Generate Markdown:

* Header: `# Transcript`
* Metadata: local generation date.
* Optionally add topic or short description if relevant.
* Add an appendix section for execution evidence (required by default).
* Then messages in dialogue order:

  * `## User`
  * `## Assistant`
* Leave a blank line between messages.

### Execution evidence appendix (required by default)

At the end of `transcript.md`, add a section `## Execution evidence`.
Prefer short, structured facts over long logs.
Include only what is load-bearing for reproducing or understanding outcomes.

Suggested subsections:

* `### Commands` (commands that were executed and their intent).
* `### Git` (branch, commit SHAs, staged/unstaged state when relevant).
* `### Commits` (list of commits produced during the chat, plus a best-effort mapping to the relevant user requests).
* `### Tests` (what was run, pass/fail, key error lines if failed).
* `### Files changed` (high-level list, optionally with `git diff --stat`).
* `### Errors` (key stack traces excerpts and the chosen fix).

## Export algorithm

1. Select Variant A or B and confirm target path.
2. Verify write conditions.
3. Do not overwrite files without explicit confirmation.
4. Collect transcript from current chat (visible user + assistant messages).
5. Keep user-provided runtime context blocks, but normalize them (IDE context and `<environment_context>`).
6. Remove system/developer/service blocks and markers.
7. Resolve `EXPORT_SKILL_DIR` as the directory that contains this `SKILL.md`.
8. If transcript is “dirty,” clean it via `python ${EXPORT_SKILL_DIR}/scripts/clean_transcript.py <file> --inplace --mode verbose` while preserving extracted user-authored request text verbatim and normalizing only the surrounding runtime context wrappers.
9. Append `## Execution evidence` to `transcript.md`.
10. Perform sanitization only on assistant-authored text, metadata, and execution evidence.
11. Keep quoted or extracted user-authored request text verbatim.
12. Write `transcript.md`.
13. If Variant A is selected, generate `brief.md` using the structure above and write it alongside.
14. Do not invent facts.
15. If information is missing, mark as `TBD` and list required clarifications.
16. Perform final self-check.

### Commit mapping rule (best-effort)

If the work includes git commits, add a `### Commits` subsection to `## Execution evidence`.
List the relevant commits with SHA and subject.
Prefer extracting them via `git log --oneline --decorate <range>` (or `git log --oneline -n 20` if the range is unknown).
If possible, add a short “why/trigger” note per commit by referencing the corresponding user request from the transcript.
If you are not sure about the mapping, label it as `approx`.

## Quality criteria (self-check)

* `transcript.md` contains no system/developer instructions or sandbox/permission policy blocks.
* `transcript.md` keeps (normalized) IDE and environment context when it existed in the dialogue.
* `transcript.md` contains an `## Execution evidence` appendix with load-bearing commands/results.
* `transcript.md` contains no markers from the “Markers” section outside verbatim user-authored text that must be kept.
* `brief.md` includes at minimum: `Constraints`, `Decisions`, `Friction`, `Delta`.
* `Delta` includes 1–3 concrete framework changes.
* Quoted or extracted user-authored requests remain verbatim wherever they appear.
* Sanitization does not rewrite quoted or extracted user-authored requests.
* Non-user-authored text and execution evidence do not contain secrets or internal identifiers.

## Mini template (example structure)

```md
# Transcript

Generated: 2026-01-28

## User
...

## Assistant
...

## Execution evidence

### Commands
- ...

### Commits
- `<sha>` `<subject>` — `<trigger>`

### Tests
- ...
```

## Mini template `brief.md`

```md
# Brief

Generated: 2026-01-28
Topic: <slug>

## Task
...

## Definition of Done
- ...

## Context
...

## Constraints
- ...

## Decisions
- ...

## Friction
- ...

## Artifacts
- ...

## Delta
- ...

## Postmortem
...
```
