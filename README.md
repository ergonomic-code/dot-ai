# Ergocode AI Agent Framework

A reusable AI agent layer that defines roles, rules, concepts, processes, and conventions for development according to the [Ergonomic Approach (EA)](https://ergowiki.azhidkov.pro/docs/about-ea/).

## How to integrate into a project

Recommended integration structure:

```
<project-root>/
├── .ai/
│   ├── ergo/          # git submodule → this repository pinned to a commit
│   └── project-local/ # project-specific extensions and overrides  
└── ...
```

## Repository navigation

- [INDEX.md](INDEX.md) — start here (entry point and artifact index).
- agents/ — agent roles and collaboration model.
- skills/ — executable skills and procedures.
- concepts/ — formalized concepts (operational definitions and specifications).
- conventions/ — shared conventions and formatting rules.
- conventions/ea-principles.md — EA principles as top-level review criteria.
- checklists/ — review checklists aligned with EA principles.
- bootstrap/ — initial project bootstrap templates to activate the framework.
