# Kotlin Conventions

Follow the official Kotlin coding conventions: <https://kotlinlang.org/docs/coding-conventions.html>.

## Project emphasis

- Declare properties before functions in classes.
- Place `companion object` declarations at the end of the class.
- Prefer imports over fully qualified names.
- Use fully qualified names only to disambiguate name collisions.
- Prefer Kotlin-generic APIs over Java `Class` tokens when both are available.
- Prefer Kotlin extension functions over Java-style calls when both represent the same operation.
- If a class body contains one or more functions, insert a blank line after `{` and before `}`.
- Do not use deprecated APIs unless there is no practical alternative.
- If you must use a deprecated API, justify it and record a removal plan.
- If a private helper does not use class state, prefer a top-level private function over a private member method.
- Avoid overload sets of generic functions that collide on JVM type erasure, and prefer distinct names (or `@JvmName`) when Java interop is required.
