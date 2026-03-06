# Regression: Do not model omitted request input with Kotlin default args on `@ModelAttribute`

## Prompt fragment

- RU: "Kotlin-дефолты для `@ModelAttribute` фактически не работают".

## Expected behavior

- The agent must not rely on a Kotlin default argument on a controller `@ModelAttribute` parameter to model omitted request input.
- The agent must verify omission and default semantics through an MVC-level request test.
- The agent must choose a framework-supported defaulting mechanism instead of a controller-method default argument when Spring MVC binding is involved.

## Framework hook

- `ergo/tech/spring/testing.md` (Spring MVC binding pitfall).
