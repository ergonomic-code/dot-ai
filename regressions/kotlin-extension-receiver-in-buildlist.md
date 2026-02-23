# Regression: Avoid implicit receiver confusion in Kotlin builders inside extension functions

## Prompt fragment

- RU: "вынеси helper в extension" / "задедуплицируй через generic extension" / "вынеси в platform как extension".
- EN: "extract helper to an extension" / "deduplicate via a generic extension" / "move it to platform as an extension".

## Expected behavior

- If an extension function uses a lambda with receiver (for example `buildList {}`, `with {}`, `apply {}`), the agent must capture the extension receiver into a local variable before entering the lambda and use it inside the builder.
- The agent must not call methods like `first()` or `isEmpty()` on the builder receiver when the intent is to call them on the original receiver.
- If a refactor introduces overloaded generic functions, the agent must avoid JVM type-erasure collisions by using distinct names (or `@JvmName` when Java interop is required).

## Framework hook

- `conventions/kotlin.md` (JVM type erasure guidance).
