---
name: formalizing-task-requirements
description: 'Turn an informal development task statement into a formal task statement from the user’s point of view, including goal/outcome, context, assumptions, glossary, scenarios, constraints, in/out scope, and acceptance criteria as black-box test cases. Use when requirements are unclear (notes, chat, ticket text) and need to be made testable before solution design or implementation, and when preparing an artifact to hand off to the designer/developer roles.'
---

# Requirements Formalization

## Goal

- Produce a formal task statement from the user’s point of view.
- Make requirements testable via black-box acceptance criteria.

## Inputs

- An informal task statement provided in chat or via a file path.
- Optional: the target output path for the formalized statement.
- Optional: links to existing docs, screenshots, and constraints.

## Outputs

- A formal requirements document in Markdown.
- A list of remaining open questions (if any) that still block verification or scope closure after clarification.

## Role constraints

- Follow the analyst role rules in `../../agents/roles.md`.
- Never propose architecture or implementation details.
- Resolve ambiguity first by asking clarifying questions and recording the user’s decisions.
- If assumptions are unavoidable, label them explicitly and add them to the “Assumptions” section and the “Open questions” list.

## Workflow

1. Read the informal task statement.
2. Restate the task in 1–3 sentences and ask the user to confirm the restatement.
3. Clarify the user goal and a measurable expected outcome.
4. Run a clarification loop until the requirements are testable.
5. Identify actors and permissions, including who can do what.
6. Confirm boundaries by stating what is in scope and what is out of scope.
7. Define domain terms and add them to the glossary.
8. Describe usage scenarios, including a happy path and alternatives.
9. Capture business rules and constraints in domain language.
10. Produce acceptance criteria as black-box test cases using the minimal format from `../../agents/roles.md`.
11. Write the final document using `references/formal-task-statement-template.md`.
12. Run a final check that every acceptance criterion is verifiable and no implementation details are present.

## Clarification loop

- Prefer asking questions over writing “open questions” into the output.
- Ask the minimum number of questions that unblock: scope boundaries, acceptance criteria, and edge cases.
- Ask high-impact questions first, and incorporate answers immediately into the draft requirements.
- Repeat until you can write acceptance criteria that are verifiable as a black box.
- Leave “Open questions” only for items the user cannot answer now, and label them explicitly as blockers.

## Interop

- Use this document as input for solution design workflows.
- For the engineering-log workflow, see `../engineering-log-solution-design/SKILL.md`.

## engineering-log defaults (optional)

- If the user provides `TASK_DIR`, treat `TASK_DIR/01-problem-statement.md` as the default input.
- Write the formalized statement to `TASK_DIR/01-problem-statement-formal.md` by default.
- Overwrite `TASK_DIR/01-problem-statement.md` only if the user explicitly asks.

## File output rules

- If the user provided an output path, write the document there.
- If the user did not provide an output path, propose a default path and ask for confirmation before writing.
- Keep Markdown in one-sentence-per-line style.
