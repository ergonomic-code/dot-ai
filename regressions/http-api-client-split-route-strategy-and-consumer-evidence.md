# Regression: API client splits must lock route strategy and contract evidence before coding

## Prompt fragment

- RU: "нам надо растащить АПИ получения новостей для админки и МП".
- RU: "Давай ещё варианты, что делать с путями".
- RU: "Оставь в АПИ только необходимые параметры".
- RU: "`languageTag` / `platform` / `appVersion` а вот это для МП оставь".

## Expected behavior

- Before implementing an API split or surface move, the agent must explicitly decide and record the route strategy, including prefix vs suffix, versioning, client split, compatibility paths, and any local rule about class-level prefixes.
- The agent must shape client-specific request parameters and response fields from explicit consumer evidence or direct user instruction, not from intuition.
- When an endpoint changes surface or client audience, the agent must update the corresponding controllers, OpenAPI, tests, and authorization rules in the same change set.

## Framework hook

- `checklists/api-design.md` (Contracts and surface strategy).
- `checklists/testing.md` (tests updated together with the surface split).
- `conventions/contracts.md` (client-shaped contracts from actual consumers).
- `ergo/tech/http-json-api/README.md` (surface strategy before coding).
