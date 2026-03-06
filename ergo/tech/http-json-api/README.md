# Tech: HTTP/JSON API

This directory contains technology-specific conventions for HTTP/JSON APIs.

## Surface strategy before coding

When an API family is being split or moved, decide the surface strategy before implementation.
Record the chosen path scheme, client split, compatibility paths, and auth boundary in the spec, plan, or task notes.
Keep that decision aligned across controllers, security rules, OpenAPI, and test clients.

## Index

- [`status-codes.md`](status-codes.md) — Status code choosing rules (minimal fixed set).
- [`status-codes.rules.yaml`](status-codes.rules.yaml) — Machine-readable status code mapping rules.

## Related skills

- [`../../../skills/choosing-http-status-codes/SKILL.md`](../../../skills/choosing-http-status-codes/SKILL.md) — Workflow for producing an endpoint-specific status-code matrix.
