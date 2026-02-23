# Regression: Keep API tests focused on observable behavior (avoid internal storage asserts)

## Prompt fragment

- RU: "добавь регрессионный API-тест" / "проверь, что команда сохранилась в БД" / "проверь сохранённую команду".
- EN: "add an API regression test" / "assert the command is saved in the DB" / "verify stored command payload".

## Expected behavior

- In external scenario (HTTP/API) tests, the agent must prefer asserting the HTTP contract plus observable effects (published messages, outgoing calls, follow-up queries).
- The agent must not couple API tests to internal persistence or command-storage details when the same scenario can be verified via observable behavior.
- If persistence is the only observable effect, the agent must prefer verifying it via a public query API or via a dedicated internal scenario test rather than via an HTTP scenario test.

## Framework hook

- `checklists/testing.md` (Coupling rules for observable behavior vs internal details).
- `concepts/testing-testcode-architecture.md` (External vs internal scenario test boundaries).
- `ergo/tech/spring/testing.md` (HTTP in tests and keeping test cases ergonomic).
