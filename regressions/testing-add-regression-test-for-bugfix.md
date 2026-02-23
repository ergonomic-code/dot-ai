# Regression: Add a test for every regression bug fix

## Prompt fragment

- RU: "мы любые баги регрессии покрываем тестами" / "нужен ещё тест на эту правку" / "покрой это тестом".
- EN: "we cover regressions with tests" / "add a regression test for this fix" / "cover this bug with a test".

## Expected behavior

- When a regression bug is fixed, the agent must add or extend a test that reproduces the bug scenario.
- The regression test must fail without the fix and pass with the fix.
- Prefer the cheapest stable test level that makes the bug observable (unit test for pure logic, scenario test for end-to-end behavior).
- If the fix changes an integration contract, add a contract-level regression test that asserts the corrected request/response and protects against rollback.

## Framework hook

- `conventions/ea-principles.md` (EA.T1 — Cover 100% of observable behavior and contracts).
- `checklists/testing.md` (Coverage).
