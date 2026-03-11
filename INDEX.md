# Framework Index

This repository provides roles, conventions, concepts, and skills for development according to the Ergonomic Approach (EA).
Use this page as an entry point and as a discoverability index.

## Start here

- Before non-trivial coding, refactoring, or review, perform task triage.
- Use [`checklists/README.md`](checklists/README.md) to select the mandatory checklist packs for the current activity and artifact.
- Select those packs from the concrete target or failing command first, not from every plausible concern in the ticket text.
- Read the smallest mandatory pack set justified by that visible evidence before proceeding with the main task.
- Load another mandatory pack only when local inspection shows that an additional concern is actually in play.
- If the task also matches a reusable workflow, open the matching skill from [`skills/README.md`](skills/README.md) after reading the mandatory checklist packs.
- Read [`conventions/ea-principles.md`](conventions/ea-principles.md) to understand the top-level principles and review criteria.
- Use [`checklists/README.md`](checklists/README.md) for lightweight review checklists derived from the principles.
- Read [`agents/roles.md`](agents/roles.md) to understand the agent roles and collaboration rules.
- Read [`conventions/markdown.md`](conventions/markdown.md) and follow it when editing framework documents.

## Task triage

Select context on two axes.

1. Activity lens:
   what kind of work is happening now.
   Examples:
   fixing failing tests,
   changing data shape,
   editing an API contract,
   refactoring an operation,
   changing an integration,
   or reviewing architecture.
2. Artifact lens:
   what kind of artifact is being touched.
   Examples:
   tests,
   records and DTOs,
   HTTP contracts,
   repositories and integrations,
   operation code,
   or class and dependency structure.

The mandatory read set is the union of the packs selected by both lenses.
Select those lenses from the concrete target under edit whenever one is available.
Do not speculate extra lenses until local evidence shows they matter.
Only after reading that set should the agent proceed with implementation, review, or a narrower reusable skill.

## Concepts

- See [`concepts/README.md`](concepts/README.md) for the concepts index.

## Conventions

- See [`conventions/README.md`](conventions/README.md) for conventions and formatting rules.

## Checklists

- See [`checklists/README.md`](checklists/README.md) for review checklists aligned with EA principles.

## Skills

- See [`skills/README.md`](skills/README.md) for the skills index.

## Processes

- See [`processes/README.md`](processes/README.md) for multi-step internal workflows.

## Integration templates

- Use [`bootstrap/AGENTS.md`](bootstrap/AGENTS.md) as a starter `AGENTS.md` for a target project.
- Use [`bootstrap/APPLICATION-CONTEXT.md`](bootstrap/APPLICATION-CONTEXT.md) and [`bootstrap/SYSTEM-CONTEXT.md`](bootstrap/SYSTEM-CONTEXT.md) as starter context templates.
- See [`bootstrap/README.md`](bootstrap/README.md) for the full templates index.

## Core vs tech

- `ergo/core/` contains technology-agnostic rules.
- `ergo/tech/` contains technology-specific conventions.
- See [`ergo/README.md`](ergo/README.md) for a file-level index.
