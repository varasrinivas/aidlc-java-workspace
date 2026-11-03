# API Documentation: priorauth-api

Full rescan of `main` at `0e00544` (tag `v1.2.0`), 2026-11-03. Base URL `http://localhost:8080` (`server.port`). All bodies are JSON. No authentication, no rate limiting, no versioning in the path.

## Endpoint Summary

| Method | Path | Success | Errors | Controller | Contract |
|---|---|---|---|---|---|
| GET | `/requests/pending` | 200 array | 400 (Spring Boot default body) | `PendingRequestsController` | C4 (unchanged queue) |
| PUT | `/reviewers/{reviewerId}/filter` | 204, no body | 400, 409 (fixed body) | `ReviewerFilterController` | C1 |
| GET | `/reviewers/{reviewerId}/filter` | 200 object or `{}` | 400 (fixed body) | `ReviewerFilterController` | C1 |
| GET | `/reviewers/{reviewerId}/filter/history` | 200 array or `[]` | 400 (fixed body) | `ReviewerFilterController` | C3 (US5163) |
| GET | `/tenants` | 200 array | none of its own | `TenantsController` | C2 |

## GET /requests/pending

- **Query**: `asOf` (optional, ISO date `YYYY-MM-DD`; default the server's `LocalDate.now()`), `tenant` (optional, exact case-sensitive match; unknown tenant gives `[]`), `overLimit` (optional; `true` keeps only over-limit rows, `false` or absent keeps all).
- **Response**: array, oldest first (`receivedAt`, then `id`), of
  `{"id", "tenantId", "service", "status", "receivedAt", "ageBusinessDays", "overLimit", "ageLabel"}`; `memberId` is never returned. Example row: `{"id": "PA-10231", "tenantId": "TX-01", "service": "MRI lumbar spine", "status": "PENDED", "receivedAt": "2026-10-01", "ageBusinessDays": 7, "overLimit": true, "ageLabel": "7 bd OVER 5"}` for `asOf=2026-10-13`.
- **Errors**: `asOf` before any pending request's received date -> 400 via `ResponseStatusException`, rendered as Spring Boot's default error body. A malformed `asOf` or `overLimit` value is rejected by Spring binding with its default 400 (not covered by a test). A wrong method answers Spring's default 405 body with its `path` (kept on purpose, AC1.1.13).

## PUT /reviewers/{reviewerId}/filter

- **Path**: `reviewerId` must match `^(?=.*[A-Za-z0-9])[A-Za-z0-9._-]{1,64}$` (case-sensitive; `.` and `..` refused).
- **Headers**: `Content-Type: application/json` (parameters such as `charset` allowed).
- **Body**: exactly `{"tenant": <known tenant string or null>, "overLimit": <true|false>}`, at most 1,024 bytes, one JSON value, no extra or missing fields, no coercion.
- **Check order** (first failure wins, FR1.6): reviewer id -> content type -> size -> JSON syntax -> shape -> known tenant -> reviewer limit.
- **Success**: 204, no body; replaces any earlier filter and adds one history line.
- **Errors**: see Error Contract.

## GET /reviewers/{reviewerId}/filter

- **Success**: 200 `{"tenant": "TX-01", "overLimit": true}` (`tenant` may be `null`, meaning all tenants), or `{}` when the reviewer never saved. A read never stores anything.
- **Errors**: 400 `invalid-reviewer-id`.

## GET /reviewers/{reviewerId}/filter/history (US5163, C3)

- **Success**: 200 array, newest first, of `{"at", "reviewer", "tenant", "overLimit"}`; `at` is ISO-8601 UTC cut to the second (`2027-01-12T09:15:30Z`); lines saved in the same second keep save order, newest first; at most `priorauth.reviewer-filter.max-history-lines` lines; `[]` when the reviewer never saved. A read never stores anything.
- **Example** (`c3-get-history.json`):
  `[{"at": "2027-01-12T09:20:05Z", "reviewer": "rita.k", "tenant": null, "overLimit": false}, {"at": "2027-01-12T09:15:30Z", "reviewer": "rita.k", "tenant": "TX-01", "overLimit": true}]`
- **Errors**: 400 `invalid-reviewer-id`; PUT/POST answer 405 with `Allow: GET` and no body; a non-JSON `Accept` answers 406 with no body.

## GET /tenants

- **Success**: 200 `["NM-02", "TX-01"]`: every `tenantId` in the export (pending or decided), once each, ascending by character code.

## Error Contract (new endpoints)

Body `{"error": <code>, "message": <fixed text>}`, `Content-Type: application/json`, never containing caller input, stack trace, path or instance (NFR4). Mapped by `NewEndpointErrorHandler` from `FilterRequestException(ErrorCode)`.

| Code | Status | Message |
|---|---|---|
| `invalid-reviewer-id` | 400 | Reviewer id must be 1-64 letters, digits, '.', '-' or '_' and contain a letter or digit. |
| `invalid-body` | 400 | Filter must be JSON with exactly "tenant" (a known tenant or null) and "overLimit" (true or false). |
| `unknown-tenant` | 400 | Tenant is not a known tenant. |
| `reviewer-limit` | 409 | The store already holds the maximum number of reviewers. |

405 and 406 on `/reviewers/**` and `/tenants` carry the status and headers (`Allow` on 405) with no body (`NewEndpointProtocolErrorHandler`).

## Browser Access (CORS, C5)

Paths `/reviewers/**`, `/tenants`, `/requests/pending`; origins from `priorauth.cors.allowed-origins` (comma-separated, default `http://localhost:3000`; `*`, `null` or an empty entry stops start-up); methods GET, PUT; header `Content-Type`; no credentials. An allowed preflight answers 200 with `Access-Control-Allow-Origin` echoing the origin; any other origin gets no allow header (403 on preflight).

## Configuration Keys

| Key | Default | Effect |
|---|---|---|
| `priorauth.aging.threshold-days` | 5 | Over-limit threshold |
| `priorauth.cors.allowed-origins` | `http://localhost:3000` | Allowed browser origins |
| `priorauth.reviewer-filter.max-reviewers` | 10000 | Distinct reviewers kept (at least 1) |
| `priorauth.reviewer-filter.max-history-lines` | 1000 | History lines kept per reviewer (at least 1) |

## Contract Fixtures

`src/test/resources/contract/f1220/` (17 files, copied from the F1220 parent record): C1 `c1-get-filter-nothing-saved.json`, `c1-get-filter-saved.json`, `c1-put-filter-request.json`; C2 `c2-get-tenants.json`; C3 `c3-get-history.json`, `c3-get-history-empty.json`; request/response cases `case-invalid-body`, `case-invalid-reviewer-id`, `case-multi-fault`, `case-preflight`, `case-put-204`, `case-reviewer-limit`, `case-unknown-tenant`; error bodies `error-invalid-body`, `error-invalid-reviewer-id`, `error-reviewer-limit`, `error-unknown-tenant`. No OpenAPI document exists.

## Internal APIs

Public methods other code relies on: `ReviewerFilterStore.save(id, filter) -> SaveResult {SAVED, REVIEWER_LIMIT}`, `read(id) -> Optional<SavedFilter>`, `history(id) -> List<HistoryLine>`; `TenantDirectory.isKnown(id)`, `list()`; `RequestStore.all()`, `pending()`; `HolidayCalendar.forTenant(id)`; `AgeBadge.of(...)`, `BusinessDays.between(...)`. Signatures are in `component-inventory.md`.
