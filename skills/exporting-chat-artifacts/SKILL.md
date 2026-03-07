---
name: exporting-chat-artifacts
description: Export `transcript.md` + `brief.md` from the current chat as an evidence package for framework improvement, preserving user-authored request text verbatim and capturing the artifacts, decisions, friction, and execution evidence needed for postmortems.
---

# Chat artifact export

## When to use

Use after completing a task or a major stage.
Use immediately when repeated clarifications, rewrites, or manual fixes become noticeable.
Use before running a framework-improvement skill that needs evidence instead of memory.

Typical cases:

- design-stage chats:
  - requirements formalization,
  - solution-space exploration,
  - HLD preparation,
  - execution-spec preparation;
- implementation-stage chats:
  - coding,
  - debugging,
  - test fixing,
  - review and patching;
- mixed chats where the key value is to preserve decisions and friction for later framework updates.

## Goal

Turn chat execution experience into a reusable evidence package.
The package must be good enough to support later framework changes without relying on memory.

## Output

By default, generate a two-file package in one folder:

- `transcript.md` as the source of facts and chronology.
- `brief.md` as a condensed package suitable for modifying the framework.

Optional:
- append or include a small artifact inventory section when design or implementation artifacts are central to understanding the chat.

## What counts as a “transcript”

A transcript is an evidence bundle for postmortems and framework improvements.
It must contain enough detail to reconstruct what happened, what was decided, where friction appeared, and what artifacts mattered.

Include:

- the dialogue as seen by the user:
  - messages from **User**,
  - messages from **Assistant**;
- user-provided runtime context that was part of the dialogue:
  - IDE context blocks,
  - environment context blocks,
  - repo paths,
  - filenames,
  - pasted prompts,
  - pasted requirements or constraints;
- a dedicated appendix with execution evidence when it is available and relevant;
- load-bearing guidance files when they shaped role selection, scope boundaries, workflow choice, or export decisions;
- explicit references to load-bearing artifacts mentioned or produced in the chat.

Keep user-authored request text verbatim wherever it is quoted or extracted into `transcript.md` or `brief.md`.
Do not paraphrase, translate, “improve,” or normalize that user-authored request text.
This verbatim rule has priority over the sanitization rules below.

Do not include:

- system instructions;
- developer instructions;
- sandbox / permission / launch-policy blocks;
- internal chain-of-thought reasoning;
- full raw tool dumps unless they are needed to understand the failure mode;
- assistant-side hidden planning text.

## Runtime context blocks

If the user message contains an IDE context block, keep it.
If the user message contains an `<environment_context>` block, keep at least `cwd` and `shell`.
Prefer normalizing such blocks into a compact `Context` subsection rather than pasting raw harness headings.
Do not include raw code excerpts from the IDE selection unless the user explicitly requests it and it is safe to export.

## Markers that must be removed from non-user-authored draft material

If any of the following appears as harness or assistant/service scaffolding in a draft, it is not part of the transcript and must be deleted.
Do not delete these strings when they are part of verbatim user-authored text that must be kept.

- `# AGENTS.md instructions`
- `<INSTRUCTIONS>`
- `<permissions instructions>`
- `developer message`
- `system prompt`
- any blocks containing assistant instructions, launch policies, or sandbox descriptions

## Why export

The purpose of export is to convert task execution experience into transferable artifacts.
These artifacts are then turned into more precise framework rules, templates, prompts, and checklists.
The resulting effect is reduced uncertainty, fewer clarifications, less rework, and shorter future chats.

## Recommended output layout

First propose Variant A.
If the user requests otherwise, switch to Variant B.

### Variant A (recommended): new file package

1. Ask for the topic or short task slug.
2. Ask for the export folder path.
3. If not specified, suggest default: `tmp/chat-export/YYYY-MM-DD/<slug>/`.
4. Inside the folder use fixed names:
   - `transcript.md`,
   - `brief.md`.
5. If files already exist, request explicit overwrite confirmation or suggest another path.

### Variant B: single transcript file

1. Into an open empty file.

   - Ask to confirm file path.
   - Verify that the file exists and is empty.
   - Otherwise suggest option (2) or request explicit overwrite confirmation.

2. Into a new file.

   - Ask for name/path.
   - If unspecified, suggest default: `tmp/chat-transcript-YYYY-MM-DD.md`.
   - Ensure file does not exist.
   - If it exists, suggest another name or request explicit overwrite confirmation.

## File format for `transcript.md`

Generate Markdown:

- header: `# Transcript`;
- metadata: local generation date;
- optional topic or short description when relevant;
- normalized context section when relevant;
- then messages in dialogue order:
  - `## User`,
  - `## Assistant`;
- leave a blank line between messages;
- add an appendix section for execution evidence when relevant.

## File format for `brief.md`

Use this structure:

- `# Brief`
- `## Task`
- `## Definition of Done`
- `## Context`
- `## Constraints`
- `## Decisions`
- `## Friction`
- `## Artifacts`
- `## Delta`
- `## Postmortem`

### Section contents

- `Task`:
  - the goal in one sentence;
- `Definition of Done`:
  - 3–7 bullet points;
- `Context`:
  - what must be known to understand the task;
- `Constraints`:
  - technologies, versions, prohibitions, time/resource limits, scope limits;
- `Decisions`:
  - forks, criteria, chosen option, consequences;
- `Friction`:
  - where clarification was required,
  - where the model misunderstood,
  - where most rewriting or backtracking occurred;
- `Artifacts`:
  - final prompts,
  - checklists,
  - templates,
  - commands,
  - repository file references,
  - produced or referenced documents;
- `Delta`:
  - 1–3 concrete framework changes that would shorten similar future work;
- `Postmortem`:
  - 5–10 lines on what worked and what did not.

When the brief includes user requests, copy them verbatim from the transcript.
Do not paraphrase, translate, “improve,” or normalize the wording.
This verbatim rule has priority over the sanitization rules below.

## Artifact inventory rules

When artifacts matter, add a short inventory in `brief.md` under `## Artifacts`.

For design-stage chats, prefer listing:

- requirements source,
- formal problem statement,
- solution options,
- HLD,
- execution spec,
- design-specific prompts/templates/checklists.

For implementation-stage chats, prefer listing:

- implementation prompt,
- result commit,
- fix commits,
- tests run,
- changed files,
- review comments,
- regression cases.

Only include artifacts that are load-bearing for understanding decisions or failure modes.
Do not dump every file mentioned in the chat.
When guidance-file selection explains the assistant's behavior, include only the load-bearing entries and keep the full detail in `transcript.md`.

## Guidance file evidence

When repository-visible guidance files shaped the work, add a `### Guidance files considered` subsection under `## Execution evidence` in `transcript.md`.
Use only guidance artifacts that the assistant could actually observe in the repository or in the visible chat.

Typical file families:

- `AGENTS.md`
- `AGENTS.local.md`
- `<project-local>/...`
- `.ai/ergo/...`
- `.ai/roles/...`
- `.ai/skills/...`
- `skills/...`
- `conventions/...`

For each entry, record:

- `path`
- `status`: `read` or `discovered_not_read`
- `source_of_awareness`
- `reason`

Use short, observable reasons for `reason`.
Prefer values such as `higher_priority_file`, `out_of_scope`, `question_only_turn`, `redundant_with_read_source`, `not_needed_for_no_edit_turn`, `required_for_role_selection`, `required_for_skill_execution`, or `required_for_scope_boundaries`.
Do not describe hidden harness, system, developer, sandbox, or launch-policy instructions as guidance files considered.
Do not claim that the model “knew” a file unless the transcript shows how that file became visible.
If no guidance files were read or explicitly considered, omit this subsection.

## Execution evidence appendix

At the end of `transcript.md`, add `## Execution evidence` when execution facts are relevant.
Prefer short, structured facts over long logs.
Include only what is load-bearing for reproducing or understanding outcomes.

Suggested subsections:

- `### Commands`
- `### Guidance files considered`
- `### Git`
- `### Commits`
- `### Tests`
- `### Files changed`
- `### Errors`

### Design-stage evidence

If the chat is design-oriented, prefer adding:

- artifact paths that were read or written;
- guidance files that defined source-of-truth priority or scope boundaries;
- key clarification rounds;
- chosen option and rejected options;
- explicit source-of-truth decisions;
- acceptance-criteria or contract decisions that shaped later artifacts.

### Implementation-stage evidence

If the chat is implementation-oriented, prefer adding:

- commands that were run and their intent;
- branch and commit SHAs when relevant;
- relevant commits produced during the chat;
- test commands and pass/fail status;
- high-level changed-file list;
- key error excerpts and the chosen fix.

### Commit mapping rule

If the work includes git commits, add a `### Commits` subsection.
List the relevant commits with SHA and subject.
Prefer extracting them via `git log --oneline --decorate <range>` or `git log --oneline -n 20` when the range is unknown.
If possible, add a short “why/trigger” note per commit by referencing the corresponding user request from the transcript.
If you are not sure about the mapping, label it as `approx`.

## Sanitization and security

Before writing files, sanitize only assistant-authored summaries, metadata, placeholder text, and execution evidence.
Do not redact or rewrite verbatim user-authored requests that you quote or extract into `transcript.md` or `brief.md`.

Replace sensitive data in non-user-authored text with placeholders when needed.
Example placeholders:

- `<TOKEN>`
- `<EMAIL>`
- `<INTERNAL_URL>`
- `<PERSON>`
- `<PROJECT>`

In the execution evidence appendix, redact secrets and truncate large outputs to the minimum needed excerpt.
If verbatim user-authored text contains obvious secrets and the export destination or sharing scope is unclear, stop and ask whether to export that text as-is or omit the affected section.

## Export algorithm

1. Select Variant A or B and confirm target path.
2. Verify write conditions.
3. Do not overwrite files without explicit confirmation.
4. Collect the transcript from the current chat:
   - visible user messages,
   - visible assistant messages.
5. Keep user-provided runtime context blocks, but normalize them.
6. Remove system, developer, and service scaffolding.
7. Record repository-visible guidance files that were read or explicitly considered when they affected the outcome, along with `status`, `source_of_awareness`, and `reason`.
   If this step produces at least one guidance-file entry, `## Execution evidence` becomes required and must include `### Guidance files considered`.
8. Resolve `EXPORT_SKILL_DIR` as the directory that contains this `SKILL.md`.
9. If the transcript is “dirty,” clean it via:

```bash
python ${EXPORT_SKILL_DIR}/scripts/clean_transcript.py <file> --inplace --mode verbose
```

10. Preserve extracted user-authored request text verbatim.
11. Sanitize only assistant-authored text, metadata, and execution evidence.
12. Append `## Execution evidence` when relevant.
    It is mandatory when guidance-file evidence, commits, commands, tests, or other load-bearing execution facts were recorded.
13. Write `transcript.md`.
14. If Variant A is selected, generate `brief.md` using the required structure and write it alongside.
15. Do not invent facts.
16. If information is missing, mark it as `TBD` and list the exact missing data.
17. Perform a final self-check.

## Quality criteria

-   `transcript.md` contains no system or developer instructions.
-   `transcript.md` keeps normalized runtime context when it existed in the dialogue.
-   user-authored request text quoted in `transcript.md` or `brief.md` remains verbatim.
-   `brief.md` is short enough to support framework editing without reopening the full chat.
-   `brief.md` contains concrete friction and delta items instead of generic observations.
-   execution evidence is concise and load-bearing.
-   guidance-file evidence is included when relevant and uses observable facts instead of mental-state claims.
-   no secrets remain in assistant-authored metadata or evidence.

## Interop

This skill is the evidence-export layer for framework improvement.
Use its output as input for:

-   designer-framework improvement from design evidence;
-   coder-framework improvement from implementation evidence.

Do not use this skill itself to patch the framework.
Its job is to produce evidence, not policy changes.
