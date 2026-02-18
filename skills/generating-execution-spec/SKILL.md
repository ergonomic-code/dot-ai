---
name: generating-execution-spec
description: "Fill the Execution-Spec template for a engineering-log task: read TASK_DIR/03-solution-hld.md (must contain === RESULT FOR EXECUTION-SPEC ===) and TASK_DIR/04-execution-spec.md (template), ask only factual clarifying questions if needed, then overwrite 04-execution-spec.md with a complete unambiguous spec and (optionally) save chat transcript to TASK_DIR/chats/02-execution-spec-chat-1.md."
---

# engineering-log: execution spec

## Input

- `TASK_DIR` is the task base directory (a repo-relative path or an absolute path).
- These files must exist:
  - `TASK_DIR/03-solution-hld.md` (must include `=== RESULT FOR EXECUTION-SPEC ===`).
  - `TASK_DIR/04-execution-spec.md` (the template that must be fully filled and overwritten).

If `TASK_DIR` is not provided, ask for it.
If the required files are missing, stop and ask for the correct path.
If the template is missing, ask the user to run the task init skill first.

## Output

- Overwritten `TASK_DIR/04-execution-spec.md` as a single complete document (English).
- The same final text printed to chat (no additions).
- Optional: saved chat transcript to `TASK_DIR/chats/02-execution-spec-chat-1.md`.

## Algorithm

1. Determine `TASK_DIR` and validate the working files exist.
2. Read `TASK_DIR/03-solution-hld.md` and extract the `=== RESULT FOR EXECUTION-SPEC ===` block.
3. Read `TASK_DIR/04-execution-spec.md` (template) and prepare to fill it completely.
4. If any section cannot be filled with facts from inputs:
   - ask clarifying questions without proposing solutions;
   - stop and end the message with:

```
=== WAITING FOR ANSWERS (EXECUTION-SPEC) ===
```

5. After answers (or if inputs are sufficient), follow the prompt in `references/exec-spec-prompt.md` strictly.
6. Hard requirement for the filled spec: in the template section `## 9. Testing` there must be either a list of acceptance test cases or a link to an artifact that contains them.
7. Hard requirement for the filled spec: explicitly state that the executor must work by TDD using those acceptance test cases.
8. Hard requirement for the filled spec: include a test definition of done that states “all acceptance test cases are implemented and pass”.
9. Conventions rule: do not duplicate test coding rules in the spec.
10. Conventions rule: provide links to the relevant conventions instead.
11. Default requirement: if the task impacts any public API (HTTP, RPC, events, DB contracts, or other externally consumed interfaces), explicitly require backward compatibility in `TASK_DIR/04-execution-spec.md` unless the inputs explicitly approve a breaking change.
12. If a required link or acceptance cases cannot be provided factually from inputs, ask for it as a clarifying question and stop with `=== WAITING FOR ANSWERS (EXECUTION-SPEC) ===`.
13. Write the final document to `TASK_DIR/04-execution-spec.md` in English and output the exact same text to chat.
14. Ask whether the current chat transcript may be saved.
15. If yes, save it to `TASK_DIR/chats/02-execution-spec-chat-1.md`.
16. If you cannot save the transcript automatically, do not fabricate it.
17. Ask the user for help or use `$chat-transcript-export`.
