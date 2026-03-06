# Regression: Exported chat artifacts must keep user-authored requests verbatim

## Prompt fragment

- RU: "экспортируй транскрипт" / "сделай brief".
- RU: "сохрани просьбу пользователя дословно".
- EN: "export the transcript" / "make a brief".
- EN: "keep the user's request verbatim".

## Expected behavior

- If `transcript.md` or `brief.md` quotes or extracts a user-authored request, that request text must remain verbatim.
- The export skill must not paraphrase, normalize, translate, or selectively redact quoted or extracted user-authored requests.
- If runtime context wrappers are normalized, the extracted user-authored request text must still remain verbatim.
- Sanitization may change only assistant-authored summaries, metadata, placeholder text, and execution evidence.
- If obvious secrets appear inside verbatim user-authored text and the export scope is unclear, the skill must ask whether to export that text as-is or omit the affected section.

## Framework hook

- `skills/exporting-chat-artifacts/SKILL.md` (What counts as a “transcript”).
- `skills/exporting-chat-artifacts/SKILL.md` (Structure of `brief.md`).
- `skills/exporting-chat-artifacts/SKILL.md` (Sanitization and security).
- `skills/exporting-chat-artifacts/SKILL.md` (Export algorithm).
- `skills/exporting-chat-artifacts/SKILL.md` (Quality criteria).
- `skills/exporting-chat-artifacts/scripts/clean_transcript.py`.
