---
name: exporting-chat-artifacts
description: Export `transcript.md` + `brief.md` from the current chat to reduce rework by improving the framework’s rules, templates, and checklists.
---

# Chat transcript export

## When to use

Use after completing a task or a major stage.
Use immediately when repeated clarifications or rework become noticeable.

## What counts as a “transcript”

* Only **visible** messages in the current chat from **User** and **Assistant**.
* Do not include: system/developer instructions, tool calls/outputs, internal reasoning.
* Practical rule: **include only messages sent with role `User` or `Assistant`**.
* Any “service” blocks or preambles (even if visible in logs or context) — **exclude**.

### Markers that must be removed (if they appear in draft)

If any of the following appears in the text, it is not part of the transcript and must be deleted:

* `AGENTS.md instructions`
* `<permissions instructions>`
* `<environment_context>`
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

### Sanitization and security

Before writing files, remove or replace sensitive data.
Replace tokens, keys, names, internal URLs, and identifiers with placeholders.
Example placeholders: `<TOKEN>`, `<EMAIL>`, `<INTERNAL_URL>`, `<PERSON>`, `<PROJECT>`.

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
* Then messages in dialogue order:

  * `## User`
  * `## Assistant`
* Leave a blank line between messages.

## Export algorithm

1. Select Variant A or B and confirm target path.
2. Verify write conditions.
3. Do not overwrite files without explicit confirmation.
4. Collect transcript from current chat (visible user + assistant messages).
5. Remove service blocks and markers.
6. If transcript is “dirty,” clean it via script.
7. Use `python skills/chat-transcript-export/scripts/clean_transcript.py <file> --inplace`.
8. Perform sanitization (tokens, keys, names, internal URLs).
9. Write `transcript.md`.
10. If Variant A is selected, generate `brief.md` using the structure above and write it alongside.
11. Do not invent facts.
12. If information is missing, mark as `TBD` and list required clarifications.
13. Perform final self-check.

## Quality criteria (self-check)

* `transcript.md` contains no system/developer instructions or tool output.
* `transcript.md` contains no markers from the “Markers” section.
* `brief.md` includes at minimum: `Constraints`, `Decisions`, `Friction`, `Delta`.
* `Delta` includes 1–3 concrete framework changes.
* Neither file contains secrets or internal identifiers.

## Mini template (example structure)

```md
# Transcript

Generated: 2026-01-28

## User
...

## Assistant
...
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
