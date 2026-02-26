# Checklist: Code hygiene

Primary reference is `../conventions/code-hygiene.md`.

## DRY pass (new or changed code)

- No repeated blocks of logic were introduced in production code.
- No copy-pasted test infrastructure was introduced across test classes.
- Overloads and convenience helpers delegate to a single canonical implementation.
- String constants and schema payloads are not duplicated across call sites if a low-risk extraction exists.

## “Done” gate (before reporting task completion)

- You scanned the diff of the change set and removed obvious duplication.
- If you introduced a new helper / abstraction, you searched the repository for an existing equivalent (by key names and domain terms) and reused it instead.
- If duplication is kept intentionally, you recorded the reason close to the code change (for example as a commit message or PR description note).
