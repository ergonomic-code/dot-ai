# Regression: Verify staged vs unstaged vs untracked before committing

## Prompt fragment

- RU: "закоммить правки" / "и закоммитай это" / "сделай commit".
- EN: "commit these changes" / "make a commit" / "commit and push".

## Expected behavior

- Before making a commit, the agent must run `git status --porcelain` and read the entire output.
- If there are untracked files under any `*/src/**` path (`??` entries) that belong to the task, the agent must stage them (or explicitly remove/ignore them) before committing.
- If there are untracked files outside `*/src/**`, the agent must not modify them unless the user explicitly asks.
- The agent must review the staged set with `git diff --name-status --cached` and ensure it matches the intended commit scope.
- The agent must review the unstaged set with `git diff --name-status` and ensure no intended changes are left unstaged.
- If the user asked for a partial commit, the agent must explicitly list what is intentionally left unstaged before committing.

## Framework hook

- `skills/git-working-tree-hygiene/SKILL.md` (Procedure and done gate).
- `checklists/git.md` (Working tree hygiene).
- `agents/roles.md` (Developer base rules for git hygiene before commits).
