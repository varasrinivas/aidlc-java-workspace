# API Documentation: priorauth-web

`priorauth-web` exposes no server endpoints. It is an HTTP **client** of `priorauth-api`, takes two page parameters, and offers internal JS module APIs.

## Page Parameters (index.html)

| Parameter | Default | Meaning |
|---|---|---|
| `?api=` | `http://localhost:8080` | Base URL of `priorauth-api`; a trailing `/` is trimmed. |
| `?reviewer=` | none | Reviewer id (US5161). With it, the saved filter is read on open and saved on each change / Clear. Without it, nothing is read or saved and the not-remembered message shows. |

## priorauth-api Endpoints Consumed

All calls go through the page's `fetch`, from the browser, with a 10 s `AbortSignal.timeout` and no retries (set in `filter-session.js`). Any non-2xx answer becomes `Error("priorauth-api answered <status>")`. No auth headers are sent.

| Contract | Method and path | Request | Expected answer | Client function |
|---|---|---|---|---|
| C4 (queue; F1210 base) | `GET /requests/pending` with optional `asOf=<date>`, `tenant=<id>`, `overLimit=true` | query only; unset options are omitted | JSON array of rows `{id, tenantId, service, status, ageLabel, overLimit}` | `api.pendingUrl`, `queue-filters.filteredUrl`, `loadQueue`, `loadQueueFor`; `api.fetchPending` (unused by the page) |
| C1 read | `GET /reviewers/{reviewerId}/filter` | `reviewerId` is `encodeURIComponent`-encoded (one path segment) | `{}` when nothing is saved, else `{"tenant": string or null, "overLimit": boolean}`; unknown fields ignored; anything else is treated as a failed read | `saved-filter-client.readFilter` (validated by `filter-session.savedFilterFrom`) |
| C1 write | `PUT /reviewers/{reviewerId}/filter` | `Content-Type: application/json`, body exactly `{"tenant": ..., "overLimit": ...}` (no other field) | 2xx (204 in tests) | `saved-filter-client.saveFilter` |
| C2 | `GET /tenants` | none | JSON array of tenant id strings, e.g. `["NM-02", "TX-01"]`; anything else is a failed list | `saved-filter-client.readTenants` (validated by `filter-session.tenantListFrom`) |

Contract examples kept in `test/contract-examples/`: `c1-get-filter-saved.json`, `c1-get-filter-nothing-saved.json`, `c1-put-filter-request.json`, `c2-get-tenants.json`.

Mapping note (US5161/OQ3): the contract's `overLimit` becomes the F1210 option `overLimitOnly` only in `queue-filters.loadQueueFor`. A cleared filter (US5162) is sent as `{"tenant":null,"overLimit":false}` and asks the bare `GET /requests/pending`.

## Internal Module API

### `createFilterSession({ base, reviewer, fetchFn = fetch, onChange })` (`src/filter-session.js`)

Returns:
- `open()`: load saved filter (if reviewer) and tenants, then the queue.
- `change({ tenant, overLimit })`: apply a filter; `""`/falsy tenant means all tenants; asks queue, retries a failed tenant list, saves when a reviewer is known. Returns a promise for all work.
- `clear()`: `change({ tenant: null, overLimit: false })` (US5162 FR6.1).
- `view()`: a copy of the current view.

`onChange(view)` receives `{ loading, tenants, tenant, overLimit, rows, message }`. Also exported: `MESSAGES` (the six message texts).

### Rendering (`src/render.js`)

`countLabel(rows)`, `renderRows(rows)`, `filterIsSet({tenant, overLimit})`, `renderControls(view?)`, `renderTenantOptions(tenants, selected)`, `renderQueue({loading, rows})`. All return strings; all rendered values pass through the private `esc`.

DOM ids and test ids produced by `renderControls`: `#tenant` (`queue-filters-tenant-select`), `#over-limit` (`queue-filters-over-limit-checkbox`), `#clear-filters` (`queue-filters-clear-button`), `#message` with `role="status"` (`queue-message`), wrapper `queue-filters`.
