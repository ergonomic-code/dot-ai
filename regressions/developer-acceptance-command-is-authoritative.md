# Regression: A user-provided verification command is the authoritative done gate

## Prompt fragment

- RU: "прогони полную верификацию проекта" / "`./gradlew -DrunTestSlow=true clean build koverVerify`".
- EN: "run the full verification" / "`<exact verification command>`".

## Expected behavior

- If the user, task artifact, or project docs provide an exact verification or acceptance command, the agent must treat that exact command as the authoritative done gate.
- The agent may use smaller or faster checks while iterating, but must not declare success, weaken the target, or invent unrelated fixes based on a different verification scenario.
- If the named command changes the test population or coverage profile (for example by including slow tests), the agent must prefer it over a faster approximation.

## Framework hook

- `agents/roles.md` (Role: developer, verification rules).
