# Coding conventions: Ports

## Intention

This document defines coding conventions for Ports in the Ergocode AI Framework.
The goal is to keep entrypoints predictable, testable, and free of business logic.

## Scope

These conventions apply to all entrypoints.
Examples include HTTP controllers, message queue listeners, event handlers, and scheduler jobs.

## Definition

A Port is a component that:

- receives an external signal;
- translates it into an application call;
- returns or emits a response.

Ports are not responsible for business decision making.

## Core rules

### Rule: Ports remain thin

Each Port method contains exactly one call to an Operation or a Resource.

Verification.

- A reader can point to a single line that triggers the business action.
- The Port method can be summarized as “decode input -> call -> encode output”.

### Rule: Branching in Ports is limited

Port branching is limited to response presentation choice or secondary routing.

Allowed branching.

- Selecting an HTTP status code or response representation based on an Operation result type.
- Selecting an Operation or Resource based on a discriminator in the request (secondary routing).

Disallowed branching.

- Branching that encodes business rules.
- Branching that performs workflow orchestration.

## Consequences for code structure

### What belongs in a Port

- Request parsing and validation that is purely syntactic.
- Authentication and authorization checks that are infrastructural.
- Mapping between transport types and domain/application types.
- Mapping between application results and transport responses.

### What must not be in a Port

- Business rules and domain invariants.
- Multi-step workflows.
- Calling multiple Resources directly to complete a scenario.

## Refactoring triggers

Refactor a Port if at least one holds.

- The Port method calls more than one Operation/Resource.
- The Port method contains non-trivial loops or computations.
- The Port method contains branching that is not presentation or secondary routing.
- The Port method cannot be made “one call” without loss of behavior.

## Default fix

Extract the behavior into an Operation.
Leave in the Port only input decoding, a single call, and output encoding.
