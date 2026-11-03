# Contract Summary — F1220 Remember my filter

This is the approved contract for F1220. It replaces the draft in `docs-in/specs/F1220/reviewer-filter-api-spec.md`.

- **Owner:** Meena Iyer (tech lead). Kiran Rao (U1) and Divya Pillai (U2) signed off the examples with her (`contract-design-questions.md` Q4).
- **Examples:** one JSON file per call and per error, in `inception/contract-design/examples/`. Units copy them into their own repo's tests (Units Generation Q1).
- **Start rule:** U1 and U2 start only after this contract is approved.

## Contracts

| # | Provider Unit | Consumer | Mechanism | Owner |
|---|---|---|---|---|
| C1 | U1 `us5160-save-filter` (`ReviewerFilterController`) | U2 `us5161-restore-filter`, U3 `us5162-clear-filters` (`SavedFilterClient`) | Sync REST: `PUT` / `GET /reviewers/{reviewerId}/filter` | Meena Iyer |
| C2 | U1 `us5160-save-filter` (`TenantsController`) | U2 `us5161-restore-filter` (`SavedFilterClient`) | Sync REST: `GET /tenants` | Meena Iyer |
| C3 | U4 `us5163-filter-history` (`ReviewerFilterController`) | External: nurse manager (direct API call) | Sync REST: `GET /reviewers/{reviewerId}/filter/history` | Meena Iyer |
| C4 | Existing `PendingRequestsController` (unchanged) | U2 `us5161-restore-filter` (`ApiClient` via `QueueFilters`) | Sync REST: `GET /requests/pending` (unchanged, now reachable from the browser) | Meena Iyer |
| C5 | U1 `us5160-save-filter` (`BrowserAccessPolicy`) | Browser running `priorauth-web` | CORS on C1, C2, C3 and C4 | Meena Iyer |
| C6 | U1 `us5160-save-filter` (`ReviewerFilterStore`) | U4 `us5163-filter-history` (extends it) | Shared code in `priorauth-api` (Java), not a wire contract | Meena Iyer |

## Rules That Apply to Every Call (C1-C3)

- **Base URL:** the API's base URL, `http://localhost:8080` by default, passed to the screen as `?api=`. There is no version in the path (Q5).
- **Reviewer id** (`{reviewerId}` in the path):
  - Must be 1-64 ASCII characters from `A-Z a-z 0-9 . - _`, with at least one letter or digit. Case-sensitive.
  - Anything else answers `400 invalid-reviewer-id`.
  - **The ids `.` and `..`:** they reach the API on Spring Boot 4.1 and answer `400 invalid-reviewer-id` with the fixed body, like any other invalid id. Nothing is saved for them (AC1.1.7; changed after US5160's code review, see below).
- **Content type:** `PUT` bodies are `application/json`.
  - Parameters such as `charset=UTF-8` are accepted.
  - A missing or different content type answers `400 invalid-body`.
  - Responses are `application/json`, except the bodiless `204`.
- **Check order:** when a request has several faults, the first failing check in this fixed order decides the answer (gate feedback R-02):
  1. reviewer id: `400 invalid-reviewer-id`
  2. content type and body size: `400 invalid-body`
  3. body shape (exactly the two fields, right types, readable JSON): `400 invalid-body`
  4. tenant known: `400 unknown-tenant`
  5. reviewer limit: `409 reviewer-limit`

  For example, an invalid reviewer id with a bad body answers `invalid-reviewer-id` (`examples/case-multi-fault.json`).
- **Body size:** a `PUT` body over 1,024 bytes answers `400 invalid-body`. Exactly 1,024 bytes is accepted.
- **Errors** (Q2): every refused call on C1-C3 answers with this body:

  ```json
  {"error": "<code>", "message": "<fixed text for the code>"}
  ```

  | Code | Status | Message (fixed) |
  |---|---|---|
  | `invalid-reviewer-id` | 400 | `Reviewer id must be 1-64 letters, digits, '.', '-' or '_' and contain a letter or digit.` |
  | `invalid-body` | 400 | `Filter must be JSON with exactly "tenant" (a known tenant or null) and "overLimit" (true or false).` |
  | `unknown-tenant` | 400 | `Tenant is not a known tenant.` |
  | `reviewer-limit` | 409 | `The store already holds the maximum number of reviewers.` |

  - The message never contains the caller's tenant, reviewer id, or body.
  - There is no stack trace, no `path`, and no `instance` field (NFR4).
  - `GET /requests/pending` (C4) keeps its existing error behaviour.
  - **This contract overrides the provisional wording** of AC1.1.9, AC1.1.10 and AC1.4.8 in `inception/user-stories/stories.md` (gate feedback R-03):
    - AC1.1.9's "a 4xx error whose message names the limit" means `409` with the `reviewer-limit` body above.
    - AC1.1.10 and AC1.4.8's "a short message" means the fixed `{error, message}` body for the matching code.
    - Units test against this contract and its examples.
  - **`.` and `..`** follow these rules like any other invalid id: `400 invalid-reviewer-id` with the fixed body (changed 2026-11-03, see Changes after approval).
- **Unknown response fields:** consumers ignore fields they don't know.
- **Screen behaviour on failure** (Q6):
  - Every call from the screen gives up after 10 seconds.
  - A timeout, network error, or non-2xx answer is a failure and shows the matching message (FR4.5, FR5.2, AC1.2.12).
  - There are no automatic retries. The reviewer's next change or a reload tries again.

---

## C1 Save and Read a Reviewer's Filter (U1 → U2, U3)

```yaml
openapi: 3.0.3
info:
  title: F1220 saved filter
  version: f1220
paths:
  /reviewers/{reviewerId}/filter:
    parameters:
      - name: reviewerId
        in: path
        required: true
        schema:
          type: string
          pattern: '^(?=.*[A-Za-z0-9])[A-Za-z0-9._-]{1,64}$'
    put:
      summary: Save the reviewer's last filter (replaces it) and write one history line (US1.1, US1.4)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SavedFilter'
      responses:
        '204':
          description: Saved, and one history line written in the same step
        '400':
          description: invalid-reviewer-id, invalid-body or unknown-tenant; nothing saved, no line written
          content:
            application/json:
              schema: {$ref: '#/components/schemas/Error'}
        '409':
          description: reviewer-limit; a new reviewer would pass the limit; nothing saved, no line written
          content:
            application/json:
              schema: {$ref: '#/components/schemas/Error'}
    get:
      summary: Read the reviewer's last filter; never creates a reviewer entry (US1.1)
      responses:
        '200':
          description: The last saved filter, or {} when the reviewer has never saved
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: '#/components/schemas/SavedFilter'
                  - $ref: '#/components/schemas/NothingSaved'
        '400':
          description: invalid-reviewer-id
          content:
            application/json:
              schema: {$ref: '#/components/schemas/Error'}
components:
  schemas:
    SavedFilter:
      type: object
      additionalProperties: false
      required: [tenant, overLimit]
      properties:
        tenant:
          type: string
          nullable: true
          description: A known tenant id (exact, case-sensitive) or null for all tenants
        overLimit:
          type: boolean
          description: true = only over-limit requests; false = all requests
    NothingSaved:
      type: object
      additionalProperties: false
      maxProperties: 0
    Error:
      type: object
      additionalProperties: false
      required: [error, message]
      properties:
        error:
          type: string
          enum: [invalid-reviewer-id, invalid-body, unknown-tenant, reviewer-limit]
        message:
          type: string
```

- **Clear filters** (US1.3) saves `{"tenant": null, "overLimit": false}`. The screen treats `{}` the same way.
- The screen sends exactly the two fields. It never sends extra fields, because the API refuses them.
- **Examples:**
  - `examples/c1-put-filter-request.json`
  - `examples/c1-get-filter-saved.json`
  - `examples/c1-get-filter-nothing-saved.json`
  - `examples/error-invalid-reviewer-id.json`
  - `examples/error-invalid-body.json`
  - `examples/error-unknown-tenant.json`
  - `examples/error-reviewer-limit.json`

## C2 Known Tenants (U1 → U2)

```yaml
openapi: 3.0.3
info:
  title: F1220 known tenants
  version: f1220
paths:
  /tenants:
    get:
      summary: The known tenants, for the screen's picker (US1.1, US1.2)
      responses:
        '200':
          description: Every tenantId in the request export, ascending, no duplicates
          content:
            application/json:
              schema:
                type: array
                uniqueItems: true
                items:
                  type: string
```

- The order is ascending by plain character code, which is case-sensitive.
- With the sample export the answer is `["NM-02", "TX-01"]` (Q3).
- **Example:** `examples/c2-get-tenants.json`

## C3 Filter History (U4 → nurse manager)

```yaml
openapi: 3.0.3
info:
  title: F1220 filter history
  version: f1220
paths:
  /reviewers/{reviewerId}/filter/history:
    parameters:
      - name: reviewerId
        in: path
        required: true
        schema:
          type: string
          pattern: '^(?=.*[A-Za-z0-9])[A-Za-z0-9._-]{1,64}$'
    get:
      summary: The reviewer's filter history, newest first (US1.4); never creates a reviewer entry
      responses:
        '200':
          description: Up to the newest 1,000 lines (configurable); [] when the reviewer has never saved
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/HistoryLine'
        '400':
          description: invalid-reviewer-id
          content:
            application/json:
              schema: {$ref: '#/components/schemas/Error'}
components:
  schemas:
    Error:
      description: The same shared Error schema as C1 (gate feedback R-05)
      type: object
      additionalProperties: false
      required: [error, message]
      properties:
        error:
          type: string
          enum: [invalid-reviewer-id, invalid-body, unknown-tenant, reviewer-limit]
        message:
          type: string
    HistoryLine:
      type: object
      additionalProperties: false
      required: [at, reviewer, tenant, overLimit]
      properties:
        at:
          type: string
          description: UTC instant cut (not rounded) to the second, ISO-8601 with Z, e.g. 2027-01-12T09:15:30Z
        reviewer:
          type: string
          description: The reviewer id the save was made under (the path id); a claim, not proof of who saved
        tenant:
          type: string
          nullable: true
        overLimit:
          type: boolean
```

- Lines with the same `at` keep save order, newest first.
- This four-field shape is the contract. It settles FR7.3's example in favour of FR7.1, as Meena Iyer agreed (R-07).
- **Examples:**
  - `examples/c3-get-history.json`
  - `examples/c3-get-history-empty.json`

## C4 Pending Queue (Existing, Unchanged)

`GET /requests/pending?tenant=<id>&overLimit=true` keeps its F1210 behaviour:

- **Tenant:** an unknown tenant answers `200 []` (FR3.3).
- **Over limit:** off is sent by leaving `overLimit` out. `QueueFilters` maps the screen's `overLimitOnly` to `overLimit` in one place (OQ3).
- **Browser access:** the only change is that U1's browser-access setting (C5) now lets the screen reach it from a browser.

## C5 Browser Access (CORS)

```yaml
cors:
  applies_to: ['/reviewers/**', '/tenants', '/requests/pending']
  allowed_origins: ['${priorauth.cors.allowed-origins:http://localhost:3000}']   # comma-separated, named origins only, never '*'
  allowed_methods: [GET, PUT, OPTIONS]
  allowed_headers: [Content-Type]
  allow_credentials: false
```

- **Default origin:** `priorauth.cors.allowed-origins` defaults to `http://localhost:3000`. That is how the screen is served in development: `priorauth-web`'s README runs `npx serve .`, which serves on port 3000. `npx serve` is the README's own development tool, not a project dependency.
- **The setting is a comma-separated list** of exact origins, each with scheme, host and port. More origins can be added, but `*` is never allowed.
- **Pages opened as `file://`** send `Origin: null` and are not supported. `null` is never an allowed origin.
- **Other origins:** a call from an origin not on the list gets no CORS permission headers.
- **Preflight:** a `PUT` preflight from the allowed origin answers with permission for `GET, PUT` and the `Content-Type` header (`examples/case-preflight.json`).
- **Production list:** the list for anything beyond local development stays with NFR Design (OQ4).
- (Gate feedback R-01.)

## C6 Store Shared Between U1 and U4 (Shared Code)

```yaml
shared-schema:
  owner: U1 us5160-save-filter
  extended_by: U4 us5163-filter-history
  class: ReviewerFilterStore (package com.acmehealth.priorauth.store)
  operations:
    save(reviewerId, SavedFilter) -> saved | reviewerLimit   # U1; U4 adds the history line inside the same lock
    read(reviewerId) -> SavedFilter | nothing                # U1
    history(reviewerId) -> List<HistoryLine>, newest first   # U4
  rules:
    - reads never create a reviewer entry
    - a save and its history line happen together or not at all (NFR2)
    - no Spring web types in the store
```

U4 does not change the meaning of `save` or `read`. It only adds the history line and the `history` operation.

## Contract Ownership Rules

- **Owner:** Meena Iyer owns every contract above. Story intents never change this file. A change is raised with Meena, who updates the parent record first (team practice; Q4).
- **Additive changes** are allowed without agreement, after Meena updates the examples. That means a new field in a response, or a new error code. Consumers ignore unknown fields.
- **Breaking changes** need Meena to agree them with the owners of every affected unit before anyone codes against them. Examples include:
  - a new or renamed field in a save body (the API refuses unknown fields)
  - a removed or renamed field anywhere
  - a changed status code or error code
  - a changed meaning
- **Request, status and response cases** (gate feedback R-06): besides the body examples, `examples/` holds one `case-*.json` file per error code, plus a successful save and a preflight. Each case pairs a request with its status and response:
  - `case-put-204.json`
  - `case-invalid-reviewer-id.json`
  - `case-invalid-body.json`
  - `case-unknown-tenant.json`
  - `case-reviewer-limit.json`
  - `case-multi-fault.json`
  - `case-preflight.json`
- **Examples are the test source:** a unit copies the examples it builds or calls into its repo's tests and names them in its code plan. When an example changes, those tests change with it.
- **Start rule:** U1 and U2 start only after this contract is approved. U3 and U4 start after U2 and U1 merge.

## Open Questions

| Contract | Question | Blocks |
|---|---|---|
| C5 | Allowed browser origins beyond `http://localhost:3000` (OQ4) | Nothing in development. It must be set before anyone runs the screen from another origin; NFR Design decides. |
| C1 | How the store's single lock is built, and the memory ceiling at the limits (Domain Design R-03) | U1 code plan (NFR Design input) |

## Changes after approval

| Date | Change | Decided by | Why |
|---|---|---|---|
| 2026-11-03 | `.` and `..` answer `400 invalid-reviewer-id`, not `404` | Meena Iyer, at US5160's mob code review (with Kiran Rao, Arjun Nair) | Built and tested in US5160 (`DotReviewerIdTest`): the server does not reroute them, the 400 body is the fixed one and echoes nothing. Applies to every `/reviewers/{reviewerId}/...` call, including US5163's history. |
