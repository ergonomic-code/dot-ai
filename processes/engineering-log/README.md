# Process: engineering-log

This process defines the internal framework workflow for preparing and specifying tasks in `engineering-log/`.
It combines reusable skills with process-local step specs.

## Flow

1. [`initializing-engineering-log-task/SKILL.md`](initializing-engineering-log-task/SKILL.md) — create the task directory and seed files.
2. [`../../skills/formalizing-task-requirements/SKILL.md`](../../skills/formalizing-task-requirements/SKILL.md) — formalize the problem statement into `01-problem-statement-formal.md`.
3. [`designing-solution-for-engineering-log-task/SKILL.md`](designing-solution-for-engineering-log-task/SKILL.md) — produce solution options and HLD from the formalized problem statement when it is available.
4. [`generating-execution-spec/SKILL.md`](generating-execution-spec/SKILL.md) — generate the final Execution-Spec.
5. [`../../skills/exporting-chat-artifacts/SKILL.md`](../../skills/exporting-chat-artifacts/SKILL.md) — optionally export transcript and brief.

## Process-specific defaults

When step 2 uses `formalizing-task-requirements`, apply these defaults:

- Read from `TASK_DIR/01-problem-statement.md` when `TASK_DIR` is provided.
- Write to `TASK_DIR/01-problem-statement-formal.md` by default.
- Step 3 must use `TASK_DIR/01-problem-statement-formal.md` when that file exists and is non-empty.
- Step 3 may fall back to `TASK_DIR/01-problem-statement.md` only when problem formalization was intentionally skipped or has not been completed yet.
- Overwrite `TASK_DIR/01-problem-statement.md` only if the user explicitly asks.

## Transcript defaults

- Step 2 transcript: `TASK_DIR/chats/01-problem-formalization-chat-1.md`.
- Step 3 transcript in `space` mode: `TASK_DIR/chats/02-solution-options-chat-1.md`.
- Step 3 transcript in `single` mode: `TASK_DIR/chats/02-solution-hld-chat-1.md`.
- Step 4 transcript: `TASK_DIR/chats/03-execution-spec-chat-1.md`.
- Implementation transcript: `TASK_DIR/chats/04-implementation-chat-1.md`.
