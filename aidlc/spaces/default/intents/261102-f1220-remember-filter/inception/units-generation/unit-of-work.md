# Units of Work — F1220 Remember my filter

There are four units, one per Rally story: one unit is one intent, one branch and one PR (team practice; `units-generation-questions.md` Q2). They group the components in `inception/domain-design/components.md` and follow its ADRs.

| Unit ID | Directory | Rally | Story | Owner | Repo | Kind | Branch | Complexity |
|---|---|---|---|---|---|---|---|---|
| U1 | u1-us5160-save-filter | US5160 | US1.1 | Kiran Rao | priorauth-api | service | `f1220/us5160-save-filter` | L |
| U2 | u2-us5161-restore-filter | US5161 | US1.2 | Divya Pillai | priorauth-web | ui | `f1220/us5161-restore-filter` | L |
| U3 | u3-us5162-clear-filters | US5162 | US1.3 | Tara Joshi | priorauth-web | ui | `f1220/us5162-clear-filters` | S |
| U4 | u4-us5163-filter-history | US5163 | US1.4 | Arjun Nair | priorauth-api | service | `f1220/us5163-filter-history` | M |

The construction directory is the Unit ID followed by the unit name. The unit name is used as given in Q2.

---

## U1 `us5160-save-filter` (Rally US5160)

- **Description:** the API keeps each reviewer's last filter and gives it back. It also provides the known-tenant list for the picker and opens browser access to the API for the screen.
- **Boundaries:** `priorauth-api` only. No screen change.
- **Components it builds or changes:**
  - **New:**
    - `ReviewerFilterController`, with PUT/GET `/reviewers/{reviewerId}/filter`
    - `ReviewerFilterStore`, saved filters only, built to take history in U4 (ADR-001)
    - `TenantDirectory`
    - `TenantsController`
    - `NewEndpointErrorHandler`
    - `BrowserAccessPolicy`
  - **Changed:** `RequestStore` sample data gets the NM-02 request (FR3.2).
- **Responsibilities:**
  - FR1, FR2 and FR3.
  - AC1.1.1-AC1.1.13: strict bodies, reviewer-id rules, the reviewer limit, safe errors, `GET /tenants`, named-origin browser access, and the queue endpoint left unchanged.
- **Deployment model:** shared. It is part of the single `priorauth-api` service, released by the feature PR to `main` plus a tag. There are no deployed environments (team practice).
- **Complexity:** L. It took on `GET /tenants`, browser access and strict bodies beyond the Rally estimate of 3. Kiran Rao re-estimates it at Delivery Planning, and the fallback split is in `stories.md`.
- **Implementation notes and constraints:**
  - Kiran Rao records the API test baseline through the verify script, with the repos named, before the first code change.
  - The NM-02 row's `receivedAt` is on or before 2026-10-13. The code plan names every existing test file it changes.
  - A caller's value never reaches `HolidayCalendar`, a file path or a cache key.
  - Spring's lenient JSON settings are switched off for the new request bodies.
  - The store's lock and limits are built here, ready for U4's history (ADR-001).
  - The contract examples for the filter and tenants calls are copied into this repo's tests (Q1).
  - Any new dependency is named in the plan first.

## U2 `us5161-restore-filter` (Rally US5161)

- **Description:** the reviewer screen gets its tenant picker and "over limit only" switch. It opens with the reviewer's last filter and saves changes.
- **Boundaries:** `priorauth-web` only. It builds against the agreed contract, not against U1's merged code.
- **Components it builds or changes:**
  - **New:** `FilterSession`, `SavedFilterClient`.
  - **Changed:**
    - `ReviewerPage` (`index.html`), kept as a thin caller.
    - `QueueFilters` (the one `overLimitOnly` to `overLimit` mapping).
    - `QueueRenderer` (controls, message area, empty result, and `esc` for `'`).
- **Responsibilities:**
  - FR4 and FR5.
  - AC1.2.1-AC1.2.12: no flash on open, failure messages, quick changes, late reads, no reviewer, safe display, empty result, queue failure.
- **Deployment model:** shared. It is part of the static `priorauth-web` screen, released by the feature PR to `main` plus a tag.
- **Complexity:** L. The F1210 controls must be added to the page first.
- **Implementation notes and constraints:**
  - The ordering, late-read and message logic lives in DOM-free `src/` modules with tests (team practice).
  - Divya Pillai covers R-06 (a change before the first read wins) in this unit's code plan.
  - The contract examples for the calls the screen makes are copied into this repo's tests (Q1).
  - Keyboard use is checked by hand at the feature's Build and Test.
  - The screen's 6 existing tests keep passing.

## U3 `us5162-clear-filters` (Rally US5162)

- **Description:** one "Clear filters" control resets both filters, shows the whole queue and saves the cleared filter.
- **Boundaries:** `priorauth-web` only. It changes only `FilterSession` and `QueueRenderer` (ADR-004, agreed by Divya Pillai and Tara Joshi).
- **Responsibilities:** FR6, plus AC1.3.1-AC1.3.6 (the disabled state, focus after Clear, and Clear while a save is open).
- **Deployment model:** shared. It is part of the `priorauth-web` screen.
- **Complexity:** S (Rally: 1). It is a Should-have and the first to slip if 2027.Q1 R1 is at risk.
- **Implementation notes and constraints:** its branch is cut from `origin/feature/F1220` after U2 merges (team practice). It follows U2's save-ordering rule (AC1.3.6).

## U4 `us5163-filter-history` (Rally US5163)

- **Description:** every saved filter writes one history line, and nurse managers read a reviewer's history newest first.
- **Boundaries:** `priorauth-api` only. It extends U1's `ReviewerFilterStore` and `ReviewerFilterController` (ADR-001).
- **Responsibilities:**
  - FR7, plus FR1.5 and NFR2 (an atomic save with its line).
  - AC1.4.1-AC1.4.9: four-field lines, UTC cut to the second, refused saves leave no line, newest first, limits, parallel saves, safe errors.
- **Deployment model:** shared. It is part of the `priorauth-api` service.
- **Complexity:** M (Rally: 2, plus the parallel-save test).
- **Implementation notes and constraints:**
  - Its branch is cut after U1 merges into `feature/F1220`.
  - Line times come from an injected `Clock` (ADR-005).
  - The contract example for the history call is copied into this repo's tests (Q1).
  - The release-notes line naming the history call is Meena Iyer's.
