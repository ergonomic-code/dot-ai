# Regression: The operations checklist must keep conditional balanced form and operation-level CQS explicit

## Prompt fragment

- RU: "уточни operations checklist" / "верни balanced form" / "операция должна быть command или query".
- RU: "запрос может писать только скрытое состояние" / "команда не должна быть read API".
- EN: "clarify the operations checklist" / "restore balanced form" / "an operation must be a command or a query".
- EN: "a query may write only secret state" / "a command must not act as a read API".

## Expected behavior

- `checklists/operations.md` must say that balanced form is required when an operation uses more than one branch type among input, transformation, and output.
- `checklists/operations.md` must classify the operation itself, at its own abstraction level, as either a command or a query.
- The operations checklist must say that commands may return only acknowledgment and generated data, not a read projection of existing state.
- The operations checklist must say that queries do not change observable state.
- The operations checklist must allow writes only to secret state whose changes cannot affect the answer of repeated non-secret queries with the same explicit parameters.
- The operations checklist must keep links to both `concepts/balanced-system-form.md` and `concepts/command-query-separation.md`.

## Framework hook

- `checklists/operations.md`.
- `concepts/balanced-system-form.md`.
- `concepts/command-query-separation.md`.
