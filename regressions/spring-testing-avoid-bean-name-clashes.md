# Regression: Avoid bean name clashes in Spring test fixtures

## Prompt fragment

- RU: "org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type '...*TestApi' available".
- EN: "`NoSuchBeanDefinitionException` and a missing `*TestApi` bean after a test refactor".

## Expected behavior

- When combining `@ComponentScan` with explicit `@Bean` methods in test fixtures, the agent must check for bean name collisions.
- The agent must remember that the default bean name for `FooBar` is `fooBar`, and avoid `@Bean` methods with the same name as scanned components.
- If a platform helper and a fixture facade would collide by name, the agent must rename the `@Bean` method or set an explicit bean name (for example via `@Bean(name = ["..."])`).
- After changing test fixture wiring, the agent must run a minimal test task that loads the relevant Spring context to catch wiring errors early.

## Framework hook

- `ergo/tech/spring/testing.md` (Test fixture wiring and bean naming collisions).
- `checklists/testing.md` (Coupling and fixture architecture).
