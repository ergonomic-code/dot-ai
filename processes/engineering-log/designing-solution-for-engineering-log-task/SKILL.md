---
name: designing-solution-for-engineering-log-task
description: 'Conceptual solution design for a task in engineering-log: read TASK_DIR/01-problem-statement-formal.md when it exists and is non-empty, otherwise fall back to TASK_DIR/01-problem-statement.md, choose a mode (explore solution space or use a single obvious option), run the corresponding guided dialogue, and write results to 02-solution-options.md / 03-solution-hld.md and chats/*.'
---

# Process step: engineering-log solution design

## Input

- `TASK_DIR` is the task base directory (a repo-relative path or an absolute path).
- The working problem statement file must be selected in this order:
  - `TASK_DIR/01-problem-statement-formal.md` when it exists and is non-empty.
  - Otherwise `TASK_DIR/01-problem-statement.md`.
- At least one of those files must exist and contain the problem statement.

## Output

- Mode `space` (solution space exploration):
  - `TASK_DIR/02-solution-options.md`
  - `TASK_DIR/03-solution-hld.md`
  - `TASK_DIR/chats/02-solution-options-chat-1.md`
- Mode `single` (single obvious option):
  - `TASK_DIR/03-solution-hld.md`
  - `TASK_DIR/chats/02-solution-hld-chat-1.md`

## Algorithm

### 1) Determine the task directory

- If the user did not provide `TASK_DIR`, ask for it.
- Select the working problem statement file:
  - Use `TASK_DIR/01-problem-statement-formal.md` when it exists and is non-empty.
  - Otherwise use `TASK_DIR/01-problem-statement.md`.
- If neither file is available with content, stop and ask for the correct path.
- If `TASK_DIR/chats/` does not exist, create it.

### 2) Choose the mode: `space` or `single`

Read the selected working problem statement file, then do a quick classification.

Choose `space` if any of these is true:
- there are 2+ reasonable approaches and you need to choose deliberately;
- requirements/constraints are incomplete and you cannot proceed without Q&A;
- the cost of a wrong decision is high (wide changes, high regression risk, complex integration).

Choose `single` if:
- the solution is truly obvious and alternatives are not meaningful;
- scope boundaries are clear and the choice does not affect architecture/contracts.

If in doubt, default to proposing `space`.

After classification:
- briefly explain why this mode fits;
- ask the user to confirm the mode: `space` or `single`.

### 3) Follow the corresponding prompt strictly

- Set `{{PROBLEM_STATEMENT_FILE}}` to the selected working problem statement file before following the prompt.
- If `space` is chosen, open and follow `references/exec-spec-space.md`.
- If `single` is chosen, open and follow `references/exec-spec-single.md`.

Do not mix prompts.
Do not violate their stop points and file-writing rules.
Write `TASK_DIR/02-solution-options.md` (if applicable) and `TASK_DIR/03-solution-hld.md` in English.

## Transcript export

Both prompts require saving the current chat transcript into `TASK_DIR/chats/...`.
Append to the transcript as you go, after each completed step, instead of waiting until the end.
If you cannot save the transcript automatically, do not fabricate it.
Ask the user to help, or use the `exporting-chat-artifacts` skill.
