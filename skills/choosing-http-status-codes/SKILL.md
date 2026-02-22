---
name: choosing-http-status-codes
description: "Choose HTTP response status codes for an HTTP/JSON endpoint using Ergonomic Approach conventions and output a contract-ready status-code matrix."
---

# Choosing HTTP status codes (HTTP/JSON API)

Primary reference: `../../conventions/http-json-api/status-codes.md`.

## When to use

- Designing a new HTTP/JSON endpoint contract (including OpenAPI).
- Reviewing an endpoint implementation for status-code consistency.
- Standardizing error mapping in controllers / exception handlers.

## Input

- Endpoint: method + path.
- Operation kind: query vs command; create/update/delete; sync vs async.
- Success response body: yes/no; whether a representation is returned.
- Expected failure modes:
  - request syntactically invalid (parse/type/format/mapping)
  - request semantically invalid
  - authn/authz
  - referenced resource id not found in DB
  - expected domain failures (business rules, data integrity, invalid transition, etc.)
  - expected dependency failures
  - backend outage/unavailability (if relevant)
  - unexpected server errors

## Output

1) A “Status codes” table: code → when → body shape.
2) Error body rules: Problem Details + required fields.
3) One to three example responses (`application/problem+json`) for the most relevant error categories for the endpoint.

## Algorithm

1. Determine the success code.
   - GET (query) → 200.
   - Create resource (POST) → 201.
     - Optional: set `Location` when applicable.
     - Recommended: return the created resource representation.
   - Async start → 202.
     - Return an operation id (or an operation-status resource) in the body.
   - Command with no body → 204.
   - Otherwise → 200.

2. Enumerate client and contract errors.
   - Invalid request (parse/type/format/mapping/query/path) → 400.
   - Unauthenticated → 401.
   - Unauthorized → 403.
   - Endpoint/resource not found (missing endpoint, or resource id absent in DB) → 404.
   - Method not allowed (endpoint exists but HTTP method is not supported) → 405.
   - Semantically invalid request → 422.
   - Rate limited (if applicable) → 429.

3. Enumerate expected domain failures.
   - Any expected domain failure where the request cannot be processed in the current state of the system → 409.
   - This typically requires checking current DB state or an external system.
   - Map all expected domain exceptions to 409 consistently.

4. Enumerate integration failures.
   - Expected dependency failure (timeouts, handled 5xx, compatibility breaks) → 502.

5. Enumerate backend outage/unavailability.
   - Full backend outage / unavailability → 503/504.

6. Enumerate unexpected failures.
   - Anything else unexpected → 500.

7. Validate minimalism.
   - Use only the convention set (400/401/403/404/405/409/422/500/502/503/504, plus 429 if used).
   - Introduce other codes only as an explicit local exception.

8. Produce the output artifacts.
   - Status table.
   - Problem Details envelope notes (media type, required fields, `status` consistency).
   - Examples.

## Output template

### Status codes

| Code | When | Body |
|---:|---|---|
| 200 | ... | dto / none |
| 201 | ... | dto |
| 202 | ... | operation-handle |
| 204 | ... | none |
| 400 | invalid request | problem+json |
| 401 | unauthenticated | problem+json? |
| 403 | unauthorized | problem+json? |
| 404 | endpoint/resource not found | problem+json |
| 405 | method not allowed | problem+json |
| 409 | expected domain failure | problem+json |
| 422 | semantically invalid request | problem+json |
| 429 | rate limited (if used) | problem+json |
| 500 | unexpected server error | problem+json |
| 502 | dependency unavailable | problem+json |
| 503 | backend unavailable | problem+json |
| 504 | backend timeout | problem+json |

### Problem Details rules

- Content-Type: application/problem+json.
- Fields:
  - type: URI/route-like identifier of problem type.
  - title: short code-like title.
  - status: must equal HTTP status code.
  - detail: human-readable detail (safe to expose).
  - instance: unique id of occurrence (or trace id).
  - timestamp: optional ISO-8601.

## Examples

Examples are illustrative.
Author new ones.
Do not copy from sources.

Example domain error (409):
- type: "/reservation-dates-in-past"
- title: "CONFLICT"
- status: 409
- detail: "Reservation dates are in the past: 2026-02-01"
- instance: "<uuid>"
- timestamp: "<iso-8601>"

Example semantic error (422):
- type: "/same-source-and-target-account"
- title: "UNPROCESSABLE_ENTITY"
- status: 422
- detail: "Source and target accounts must be different"
- instance: "<uuid>"
- timestamp: "<iso-8601>"

Example dependency error (502):
- type: "/external-system-unavailable"
- title: "BAD_GATEWAY"
- status: 502
- detail: "Billing system is temporarily unavailable"
- instance: "<uuid>"
- timestamp: "<iso-8601>"
