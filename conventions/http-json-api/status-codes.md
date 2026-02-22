# HTTP/JSON API: Status codes

Goal: a fixed, minimal, and predictable set of HTTP status codes for an HTTP/JSON API.

Machine-readable rules: `status-codes.rules.yaml`.
Workflow skill: `../../skills/choosing-http-status-codes/SKILL.md`.

Canonical source:
- https://ergowiki.azhidkov.pro/docs/patterns/http-json-api/status-code-choosing/

Related:
- https://ergowiki.azhidkov.pro/docs/patterns/http-json-api/error-response-body-format/
- https://ergowiki.azhidkov.pro/docs/patterns/operations-impl/error-handling/
- https://www.rfc-editor.org/info/rfc9457 (Problem Details)

## 1. General rules

1) The same class of situations must map to the same status code across the entire API.
2) Error responses use Problem Details (`application/problem+json`) and may include `timestamp`.
3) In Problem Details, the `status` field must equal the HTTP status code.

## 2. How to choose an error status code

Classify the failure first.
Use the code associated with the category.

- Request is invalid (parse/type/format/mapping/query/path) → 400.
- Not authenticated → 401.
- Authenticated but not authorized → 403.
- Endpoint is missing, or the request references a resource id that does not exist in DB → 404.
- Endpoint exists but does not support the HTTP method → 405.
- Request cannot be processed in the current state of the system (requires checking current DB state or an external system) → 409.
- Request is syntactically correct but semantically invalid → 422.
- Rate limited (if implemented) → 429.
- Expected dependency failure (including dependency timeouts, handled 5xx, compatibility break) → 502.
- Full backend outage / unavailability → 503/504.
- Anything else unexpected → 500.

Note: reserve 504 for infrastructure-level/backend timeouts.
Use 502 for expected dependency timeouts.

If you need a contract-ready status code matrix for a specific endpoint, use `../../skills/choosing-http-status-codes/SKILL.md`.

## 3. Successful responses (2xx)

Use only the following codes:

- 200 OK
  - Successful GET.
  - Successful PUT/PATCH/POST command when the response returns a result representation (DTO).

- 201 Created
  - Resource creation (typically POST to a collection).
  - Recommended:
    - return the created resource representation in the body
    - set `Location` to the resource URL (when applicable)

- 202 Accepted
  - An asynchronous operation has been accepted for processing.
  - The body returns an operation id (or an operation-status resource).

- 204 No Content
  - Successful command with no useful response body (often: DELETE, sometimes PUT/PATCH).

## 4. Client errors (4xx)

- 400 Bad Request
  - The request is syntactically invalid.
  - Includes invalid JSON, wrong types, invalid formats, and mapping/parsing errors (including query/path parameters).

- 401 Unauthorized
  - Request is not authenticated.

- 403 Forbidden
  - Authenticated but not authorized.

- 404 Not Found
  - Endpoint is missing (contract violation), or the request references a resource id that does not exist in DB.
  - If the missing resource id was loaded from DB during request processing, treat it as a backend bug → 500.

- 405 Method Not Allowed
  - Endpoint exists but does not support the HTTP method (contract violation).

- 409 Conflict
  - The request cannot be processed in the current state of the system.
  - This is an expected domain failure that requires checking current DB state or an external system.
  - Does not include missing resources referenced by id (use 404).
  - Does not include semantically invalid requests (use 422).
  - Common cases:
    - uniqueness violation (“already exists”)
    - invalid state transition / version conflict / broken invariants
    - other predictable business-rule refusals that depend on current state
  - Return Problem Details with `status: 409` and a domain-specific `type`.

- 422 Unprocessable Entity
  - The request is syntactically correct but semantically invalid (for example, two fields contradict each other).
  - Prefer 422 when the error can be detected without reading current DB state or calling external systems.

- 429 Too Many Requests
  - Rate limiting / throttling (if implemented).

## 5. Dependency/server errors (5xx)

- 500 Internal Server Error
  - Backend programming errors, internal infrastructure failures, and other unexpected server-side failures.

- 502 Bad Gateway
  - Expected failures of external systems/dependencies (including dependency timeouts, handled 5xx, compatibility breaks, etc.).

- 503 Service Unavailable
  - Full backend outage / unavailability (usually emitted by infrastructure).

- 504 Gateway Timeout
  - Full backend outage / unavailability due to timeouts (usually emitted by infrastructure).

## 6. Mini-matrix “situation → code”

Success:
- GET → 200
- POST create → 201
- async start → 202
- command without body → 204

Errors:
- invalid input → 400
- unauthenticated → 401
- unauthorized → 403
- endpoint/resource not found → 404
- method not allowed → 405
- expected domain failure → 409
- semantically invalid request → 422
- rate limited → 429
- unexpected server error → 500
- dependency unavailable → 502
- backend unavailable → 503/504

## 7. Quality control (review rules)

- For each endpoint, the set of possible responses (2xx + 4xx/5xx) is fixed in the contract / OpenAPI.
- No “success” responses (200/201) when an error actually occurred (do not mask errors).
- 404 is used for missing endpoints (contract violations) and missing resources referenced by id.
- 422 is used for semantically invalid requests.
- 409 is used for expected domain failures that require checking current DB state or external systems.
- Avoid introducing additional 4xx/5xx codes beyond this convention unless an explicit local exception exists.
- All expected dependency failures map to 502 (when this is an expected category of failure).
- 503/504 are reserved for full backend outage/unavailability (usually emitted by infrastructure).
