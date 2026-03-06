# Kotlin Conventions

Follow the official Kotlin coding conventions: <https://kotlinlang.org/docs/coding-conventions.html>.

## Project emphasis

- Declare properties before functions in classes.
- Place `companion object` declarations at the end of the class.
- Prefer imports over fully qualified names.
- Use fully qualified names only to disambiguate name collisions.
- Prefer non-null parameters with default values over nullable parameters plus local `?:` defaulting when the default is trivial.
- Do not introduce `wireValue` (or similar) properties and custom parsing/conversion logic for enums unless a stable external contract requires it (for example when an external API uses `android`/`ios` but enum constants are `ANDROID`/`IOS`) or the codebase already follows that pattern.
- When a test needs to send an unknown enum value, pass it as a raw transport string via a test client escape hatch instead of extending the enum parsing logic.
- Prefer Kotlin-generic APIs over Java `Class` tokens when both are available.
- Prefer Kotlin extension functions over Java-style calls when both represent the same operation.
- If a class body contains one or more functions, insert a blank line after `{` and before `}`.
- Do not use deprecated APIs unless there is no practical alternative.
- If you must use a deprecated API, justify it and record a removal plan.
- If a private helper does not use class state, prefer a top-level `private` function over a private member method.
- If such a helper is naturally expressed as an extension on a receiver type and does not require access to the receiver's private or protected state, prefer a top-level `private fun Receiver.helper(...)` extension over a private member method.
- Keep the helper inside the class only when it must access private class state, when it forms part of the class's internal contract, or when co-locating it materially improves readability.
- Avoid overload sets of generic functions that collide on JVM type erasure, and prefer distinct names (or `@JvmName`) when Java interop is required.

## Rule: Prefer constructor parameters and immutable properties

Prefer initializing required state via constructor parameters.
Prefer `val` over `var` for stored state.
Avoid designing classes that require setter-based initialization or mutation of required state after construction unless it is impossible to implement the behavior otherwise.
