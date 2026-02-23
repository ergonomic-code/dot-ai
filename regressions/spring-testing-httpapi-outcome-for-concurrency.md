# Regression: Keep concurrent HTTP scenario tests ergonomic via `*ForOutcome` and shared concurrency helpers

## Prompt fragment

- RU: "рефакторинг конкурентного теста" / "убери технический шум из кейса" / "вынеси concurrent helper".
- EN: "refactor a concurrent test" / "remove technical noise from the test case" / "extract a concurrency helper".

## Expected behavior

- If an external scenario test cannot know whether a given HTTP call will succeed or return an expected error (usually due to concurrency), the agent must implement an outcome-returning `*HttpApi` method (`*ForOutcome`).
- The outcome method must return expected errors as values and must fail fast on unexpected HTTP responses or contract violations.
- The set of expected errors must be centralized and reusable rather than re-encoded in each test case.
- If the outcome method validates the same response body against multiple schemas (for example, “success” vs “error”), it must preserve diagnostics for all failed validations (as `cause` or `suppressed` exceptions).
- The test case must not inline latches, futures, or executor boilerplate and must use shared test platform helpers for concurrent execution.
- The test case assertions must focus on scenario logic and observable outcomes rather than repeating HTTP parsing and validation details.

## Framework hook

- `ergo/tech/spring/testing.md` (`*HttpApi` design and schema verification rules).
- `skills/refactoring-http-tests-to-httpapi/SKILL.md` (Outcome-based negative cases).
- `checklists/testing.md` (Coupling smells for concurrency and repeated HTTP noise).
