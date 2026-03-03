# Spring: Dependency Injection Conventions

This document defines conventions for wiring Spring beans and configuration values.

## Rule: Prefer constructor injection

Prefer constructor injection for Spring beans.
Prefer `val` constructor parameters for injected collaborators and configuration values.
Do not use field injection, setter injection, or mutable injected properties (for example `@Value` on a `var`) unless it is impossible to implement the component otherwise.

Example (preferred):

```kotlin
@Component
class SomeComponent(
    private val someService: SomeService,
    @Value("\${some.feature.enabled:false}")
    private val featureEnabled: Boolean,
)
```
