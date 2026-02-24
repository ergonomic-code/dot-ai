# Regression: Export transcript with commit list and message-to-commit mapping

## Prompt fragment

- RU: "экспортируй транскрипт" + "привяжи сообщения к коммитам".
- EN: "export the transcript" + "link messages to commits".

## Expected behavior

- If the work includes git commits, the exported `transcript.md` must include an `## Execution evidence` appendix.
- The appendix must include a `### Commits` section with a list of relevant commit SHAs and subjects.
- If possible, each listed commit must include a best-effort “trigger” note that references the corresponding user request from the transcript.
- If the mapping is uncertain, it must be labeled as `approx`.

## Framework hook

- `skills/exporting-chat-artifacts/SKILL.md` (Execution evidence and commit mapping rule).
