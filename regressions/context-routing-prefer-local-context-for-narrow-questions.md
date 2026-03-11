# Regression: Narrow questions must prefer local context before broad repository context

## Prompt fragment

- RU: "что делает этот метод?".
- RU: "почему падает этот тест?".
- RU: "посмотри этот файл" / "объясни этот символ" / "что значит эта ошибка?".
- EN: "what does this method do?".
- EN: "why does this test fail?".
- EN: "look at this file" / "explain this symbol" / "what does this error mean?".

## Expected behavior

- For a narrow question, the agent should prefer the smallest context that can answer correctly.
- If the prompt references a concrete file, symbol, test, or error, the agent should read that target before broad repository-wide context documents.
- After mandatory startup materials, the agent should expand context lazily through nearby code such as referenced types, helper functions, direct call sites, and adjacent tests.
- The agent should not open `APPLICATION-CONTEXT.md` or `SYSTEM-CONTEXT.md` by default for a single-file or single-symbol question.
- The agent may open broad context documents only when local code is insufficient, module or repository boundaries are unclear, or the task is architectural or cross-repo.

## Framework hook

- `bootstrap/AGENTS.md` (Context loading).
