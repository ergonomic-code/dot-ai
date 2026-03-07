# Regression: Exported chat artifacts must record considered guidance files with observable reasons

## Prompt fragment

- RU: "экспортируй артефакты чата".
- RU: "укажи, какие guidance-файлы были прочитаны и какие были осознанно пропущены".
- EN: "export the chat artifacts".
- EN: "show which guidance files were read and which were intentionally skipped".

## Expected behavior

- When repository-visible guidance artifacts materially shaped role selection, scope boundaries, workflow choice, or export decisions, exported `transcript.md` must include `## Execution evidence`.
- The appendix must include a `### Guidance files considered` subsection.
- Each listed entry must record the repository path, `status` (`read` or `discovered_not_read`), `source_of_awareness`, and a short observable `reason`.
- The section may include only guidance artifacts that the assistant actually discovered from the visible chat or the repository.
- The export skill must not list hidden harness, system, developer, sandbox, or launch-policy instructions as considered guidance files.
- The export skill must not claim that the model “knew” a file without observable evidence in the transcript.
- If no guidance files were read or explicitly considered, the subsection may be omitted.

## Framework hook

- `skills/exporting-chat-artifacts/SKILL.md` (What counts as a “transcript”).
- `skills/exporting-chat-artifacts/SKILL.md` (Artifact inventory rules).
- `skills/exporting-chat-artifacts/SKILL.md` (Guidance file evidence).
- `skills/exporting-chat-artifacts/SKILL.md` (Execution evidence appendix).
- `skills/exporting-chat-artifacts/SKILL.md` (Export algorithm).
- `skills/exporting-chat-artifacts/SKILL.md` (Quality criteria).
