# Regression: Default `tmp/` artifacts stay local unless the task explicitly versions them

## Prompt fragment

- RU: "сделай выгрузку артефактов чата".
- RU: "подготовь заметки в `tmp/`".
- EN: "export the chat artifacts".
- EN: "write the scratch notes into `tmp/`".

## Expected behavior

- New files under `tmp/` are treated as local scratch, evidence, or generated artifacts by default.
- The agent must not auto-stage or commit new `tmp/**` files unless the user explicitly asks to version them or the repository already tracks that exact path family as part of the task.
- During git hygiene, `?? tmp/...` entries must be reviewed as local artifacts first, not as missing deliverables.
- If a `tmp/` file really must be versioned, the agent must either move it to a tracked location or get explicit user confirmation before staging it.

## Framework hook

- `conventions/git.md` (Default `tmp/` artifacts stay local).
- `checklists/git.md` (Working tree hygiene and staging new files).
- `skills/git-working-tree-hygiene/SKILL.md` (Procedure and done gate).
- `skills/exporting-chat-artifacts/SKILL.md` (Artifact inventory rules).
