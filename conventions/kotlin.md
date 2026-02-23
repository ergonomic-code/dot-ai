# Kotlin Conventions

Follow the official Kotlin coding conventions: <https://kotlinlang.org/docs/coding-conventions.html>.

## Project emphasis

- Declare properties before functions in classes.
- Place `companion object` declarations at the end of the class.
- Prefer imports over fully qualified names.
- Use fully qualified names only to disambiguate name collisions.
- If a class body contains one or more functions, insert a blank line after `{` and before `}`.
- Do not use deprecated APIs unless there is no practical alternative.
- If you must use a deprecated API, justify it and record a removal plan.
- If a private helper does not use class state, prefer a top-level private function over a private member method.
