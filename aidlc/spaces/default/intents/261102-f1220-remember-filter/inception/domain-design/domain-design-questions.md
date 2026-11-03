# Domain Design — Questions

These questions decide the building blocks F1220 adds or changes in `priorauth-api` and `priorauth-web`. Inputs:

- `requirements.md` (approved)
- `stories.md` (approved)
- the code inventories in `codekb/`
- the team's code-style rules

Things that are already decided are not asked again. That includes the endpoints, the saved-filter shape, the limits, the four-field history line, `GET /tenants`, and the screen's message area.

## Q1. Do saved filters and their history live in one component or two?

FR1 and FR7 (US1.1 and US1.4) need a save and its history line to succeed or fail together (NFR2, AC1.4.7). The draft contract says "one in-memory store behind one class, replaceable later" (NFR1).

A. **One component**, a reviewer-filter store that owns both the saved filters and the history. A save and its history line happen in one place, under one lock, so they can't come apart. The whole store can later be swapped for a database as one piece. US1.4 extends the class US1.1 creates.
B. **Two components**, a filter store (US1.1) and a separate history log (US1.4). Each owner has their own class, but every save then has to write to both and roll back by hand if the second write fails.
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q2. Who owns the list of known tenants?

Known tenants are every `tenantId` in the request export (FR3.1). Two things use the list: save validation (FR1.2) and `GET /tenants` (AC1.1.11). The request store has no tenant method today.

A. A small new tenant-directory component that reads the request store once and answers "is this tenant known?" and "list the known tenants". The request store keeps its current job. Matching is exact and case-sensitive (A4).
B. Add a `knownTenants()` method to the existing request store
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q3. Which controllers serve the new endpoints?

The new endpoints are `PUT`/`GET /reviewers/{reviewerId}/filter`, `GET /reviewers/{reviewerId}/filter/history` and `GET /tenants`. The pending-requests controller stays unchanged (AC1.1.13).

A. A new reviewer-filter controller for the three `/reviewers/...` endpoints, plus a small tenants controller for `/tenants`. One shared error handler applies to the new endpoints only, giving the safe error body (NFR4) without changing the old endpoint's errors.
B. One new controller for all four endpoints
C. Add the endpoints to the existing pending-requests controller
D. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q4. How is the screen's new logic split into modules?

The team's rule is that screen logic lives in tested, DOM-free `src/` modules, and `index.html` only calls them. US1.2 and US1.3 add reading, saving, tenants, ordering of saves, ignoring a late read, and choosing messages.

A. Three modules:
   - a **saved-filter client** in a new `src/` module: it reads and saves the filter and reads the tenants
   - a **filter session**: the logic that orders saves, drops a superseded one, ignores a late read and decides which message shows
   - an extended **queue renderer**: the controls markup and the message area, all escaped through `esc`

   The existing queue-filters module keeps building the queue request. The F1210 option name `overLimitOnly` is mapped to `overLimit` in that one place.
B. One new module for everything
C. Not yet decided
X. Other (please specify)

[Answer]: A. Divya Pillai and Tara Joshi agreed on the module split, so US5162 changes only the filter session and the renderer.

## Consolidated Summary Confirmation

- One reviewer-filter store owns both saved filters and their history; a save and its history line happen together under one lock; replaceable as one piece; US1.4 extends the class US1.1 creates (Q1)
- A new tenant directory reads the request store once and answers "known?" and "list known tenants"; the request store is unchanged in purpose; exact, case-sensitive matching (Q2)
- A new reviewer-filter controller for the three `/reviewers/...` endpoints and a small tenants controller for `/tenants`; one shared error handler for the new endpoints only; the pending-requests controller is unchanged (Q3)
- Screen: a saved-filter client (read/save filter, read tenants), a filter session (save ordering, late-read handling, message choice), and the extended queue renderer (controls and message area, escaped); queue-filters keeps building the queue request and maps `overLimitOnly` to `overLimit` in one place; US5162 changes only the filter session and the renderer (Divya Pillai, Tara Joshi) (Q4)

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
