# Coding conventions: Operations

## Intention

This document defines coding conventions for Operations in the Ergocode AI Framework.
The goal is to make each operation a stable, testable, and reviewable unit of behavior with explicit effects.

## Scope

These conventions apply to application Operations.
An Operation is a component invoked by a Port.

## Definition

An Operation is a component that:

- represents one application scenario;
- coordinates effects over one or more Resources;
- exposes a single public entrypoint method.

Operations are the primary place for application-level orchestration.

Domain Operations are internal helpers created and used inside an Operation.
Domain Operations must not be DI-managed components.

## Core rules

### Rule: Each Operation is a single public entrypoint

Operation classes expose only one public method.

Verification.

- The public API of an Operation is one method.
- All other methods are private and exist only to structure the implementation.
- A Port can call an Operation without needing to choose between multiple behaviors.

## Consequences for code structure

### What belongs in an Operation

- Orchestration of multiple Resource calls required by a scenario.
- Transaction boundaries and consistency strategy at application level.
- Mapping between domain-level results and application-level outcomes.
- Creation and use of Domain Operations as internal reusable helpers.

### What must not be in an Operation

- Transport concerns (HTTP status codes, headers, request parsing).
- Shared mutable runtime state unrelated to the scenario.
- Multiple unrelated scenarios behind multiple public methods.

## Refactoring triggers

Refactor an Operation if at least one holds.

- The Operation exposes more than one public method.
- Callers need to choose between multiple “modes” of the same operation.
- The Operation is used as a general-purpose service by many ports.

## Default fix

Split the class into multiple Operations, one per scenario.
Keep a single public method per Operation.
Move shared logic into private helpers or into Domain Operations.
