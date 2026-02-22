# Regression: When the user asks to “use a skill”, open and follow `SKILL.md`

## Prompt fragment

- RU: "используй скилл".
- EN: "use a skill."
- RU: "используй скилл `<path-to-skill>`".
- EN: "use the skill at `<path-to-skill>`."

## Expected behavior

- If the user provides a path to a skill directory, the agent must open `<path>/SKILL.md` and follow it.
- The agent must not claim that the skill is “unavailable” just because a global skill list is missing.
- If the skill cannot be found, the agent must ask the user for the exact path to the skill directory.

## Framework hook

- `agents/roles.md` (Skills section).
- `bootstrap/AGENTS.md` (Skill invocation rule).
- `skills/README.md` (skills index).
