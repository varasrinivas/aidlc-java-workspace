# Requirements — F1220 US5160 Save and read my last filter (U1 `us5160-save-filter`)

This story's requirements are a subset of the parent feature's approved requirements. The IDs below are the parent's IDs, kept exactly, so tests and the code plan trace straight back to the feature. Where the parent's approved contract is stricter than a requirement's wording, the contract wins (parent `contract-summary.md`, gate feedback R-03).

## Sources

| Tag | Source |
|---|---|
| Req | Parent `inception/requirements-analysis/requirements.md` (approved) |
| Story | Parent `inception/user-stories/stories.md`, US1.1 (Rally US5160), AC1.1.1-AC1.1.13 (approved) |
| Unit | Parent `inception/units-generation/unit-of-work.md`, U1 (approved) |
| Contract | Parent `inception/contract-design/contract-summary.md`, C1, C2, C4, C5, C6, and `examples/` (approved) |
| ADR | Parent `inception/domain-design/decisions.md`, ADR-001, ADR-002, ADR-003, ADR-006 (approved) |
| Plan | Parent `inception/delivery-planning/bolt-plan.md`, B1 (approved) |
| Practices | `memory/team.md`, `memory/project.md` |
| codekb | `codekb/priorauth-api/` (current, reused) |

"Parent" means `aidlc/spaces/default/intents/261102-f1220-remember-filter/`.

## Intent Analysis

- **Goal:** the API keeps each reviewer's last queue filter and gives it back, so the screen (US5161) can restore it on any computer. It also gives the screen the known-tenant list and lets the browser call the API from the screen's named origin. (Story; Unit)
- **Type:** an enhancement to brownfield `priorauth-api` only. It adds new endpoints and leaves the existing queue endpoint unchanged. (Unit; codekb)
- **Complexity:** Large for one story (5 points, Plan B1): strict request bodies, reviewer-id rules, a reviewer limit, safe errors, `GET /tenants` and browser access.
- **Branch:** `f1220/us5160-save-filter`, cut from `origin/feature/F1220`; the PR goes into `feature/F1220`. (Plan; Practices)

## Functional Requirements

### FR1 Save a reviewer's filter

- **FR1.1** `PUT /reviewers/{reviewerId}/filter` with a valid body saves it as that reviewer's last filter, replacing any earlier one, and answers `204`. (Req; AC1.1.1, AC1.1.2)
- **FR1.2** The body has exactly two fields:
  - `tenant` is a known tenant id (FR3) or `null`.
  - `overLimit` is `true` or `false`.

  A missing field, an extra field, a wrong type (no type conversion, so `"true"` and `1` are refused), unreadable JSON, a missing or non-JSON content type, or a body over 1,024 bytes answers `400 invalid-body`. An unknown tenant answers `400 unknown-tenant`. In each case the saved filter is unchanged. A valid body of exactly 1,024 bytes is accepted, and `charset` parameters on the content type are accepted. (Req; AC1.1.4, AC1.1.6; Contract C1)
- **FR1.3** A `reviewerId` is 1-64 ASCII characters from `A-Z a-z 0-9 . - _` with at least one letter or digit, matched case-sensitively. Any other id answers `400 invalid-reviewer-id` on `PUT` and `GET`, and nothing is saved. The ids `.` and `..` answer `404` with the server's default body, which is a deliberate exception. (Req; AC1.1.7, AC1.1.8; Contract rules)
- **FR1.4** At most `priorauth`'s configured reviewer limit of distinct reviewers (default 10,000) have a saved filter. A save for a new reviewer beyond the limit answers `409 reviewer-limit`, and nothing is saved. Reviewers already kept can still save. A read never takes a reviewer slot. (Req; AC1.1.3, AC1.1.9; Contract)
- **FR1.5** When two saves for the same reviewer arrive close together, the last one completed wins. The history line for each save is US5163's work. (Req; ADR-001)
- **FR1.6** When a request has several faults, the first failing check in this fixed order decides the answer: reviewer id, then content type and body size, then body shape, then tenant known, then reviewer limit. (Contract, check order, `examples/case-multi-fault.json`)

### FR2 Read a reviewer's filter

- **FR2.1** `GET /reviewers/{reviewerId}/filter` answers `200` with the last saved filter in the FR1.2 shape. (Req; AC1.1.1)
- **FR2.2** For a reviewer who has never saved, it answers `200 {}` and stores nothing. (Req; AC1.1.3)
- **FR2.3** An invalid `reviewerId` answers `400 invalid-reviewer-id`. (Req; AC1.1.7)

### FR3 Known tenants

- **FR3.1** A tenant is known when it is the `tenantId` of any request in the request export, pending or not, matched exactly and case-sensitively. `GET /tenants` answers `200` with every known tenant once, sorted ascending by plain character code. (Req; AC1.1.5, AC1.1.11; Contract C2; ADR-002)
- **FR3.2** The sample export gets one NM-02 request, with `receivedAt` on or before 2026-10-13 so that no existing `asOf` case turns into a 400. With the sample data, `GET /tenants` answers `["NM-02", "TX-01"]`. The existing queue tests whose row counts change are updated. The code plan names each test file it changes. (Req; AC1.1.13; Unit)
- **FR3.3** `GET /requests/pending` keeps its behaviour: an unknown `tenant` still answers `200 []`, and its errors are unchanged. (Req; AC1.1.13; Contract C4; ADR-003)

### FR8 Browser access (this story's part of NFR6)

- **FR8.1** A browser call from a configured origin (`priorauth.cors.allowed-origins`, default `http://localhost:3000`, comma-separated exact origins) to `/reviewers/**`, `/tenants` and `/requests/pending` is allowed. That includes the `PUT` preflight, which allows `GET, PUT` and the `Content-Type` header, without credentials. A call from any other origin, or with `Origin: null`, gets no permission headers. `*` is never answered. (AC1.1.12; Contract C5; ADR-006; `examples/case-preflight.json`)

FR8 is a new ID in this record only. It restates the parent's NFR6 and Contract C5 as a testable behaviour of this story. It adds no new scope.

## Non-Functional Requirements

- **NFR1 Data lifetime:** saved filters live in memory in one `ReviewerFilterStore` class that a durable store can later replace. A restart empties them. (Req; ADR-001)
- **NFR3 Input limits:** every request value is validated and size-limited at the API boundary (FR1.2-FR1.4). No caller value reaches a file path or a cache key, and in particular never `HolidayCalendar`. (Req; Practices security checklist)
- **NFR4 Error responses:** every refused call on the new endpoints answers `{"error": "<code>", "message": "<fixed text>"}` with the contract's fixed message for the code. There is no stack trace and no `path` or `instance` field, and the body never contains the caller's tenant, reviewer id or body. For example, a save with tenant `<b>ZZ</b>` produces a response containing no `<b>`. The error handler applies only to the new controllers. (Req; AC1.1.10; Contract; ADR-003)
- **NFR6 Cross-origin calls:** named origins only, never `*` (FR8). (Req)
- **NFR7 Memory bound (this story's part):** the reviewer limit is configurable (default 10,000). It is proven with a fresh store using a small limit, plus one HTTP test in its own Spring context, never in the shared one. The history limit is US5163's. (Req; Story testing note; A3)
- **NFR8 Compatibility:** the existing queue tests keep passing apart from the FR3.2 updates. Kiran Rao records the API's test baseline through the verify script, with the repo named, before the first code change. (Req; Practices)
- **NFR9 Testability:** API tests do not share saved filters. Each test uses its own reviewer id, or the store is reset. (Req; Practices)
- **NFR11 Coverage:** each new branch has a test. Each new or changed test file covers the happy path and at least two error or edge cases. Line coverage is NOT MEASURED in F1220. (Req; Practices)

## Constraints

- `priorauth-api` only (Java 21, Spring Boot 4.1, Jackson 3 `tools.jackson.databind`), following the team's code style and package rules. New components are `ReviewerFilterController`, `ReviewerFilterStore`, `TenantDirectory`, `TenantsController`, `NewEndpointErrorHandler` and `BrowserAccessPolicy`. Only the sample data changes in existing code. (Unit; ADR-001-003, ADR-006; Practices)
- `ReviewerFilterStore` is built ready for US5163 to add the history line inside the same lock, without changing what `save` and `read` mean. (Contract C6; ADR-001)
- No new dependency unless the code plan names it first. (Practices)
- Tests run only through `scripts\verify.cmd priorauth-api` (`scripts/verify.sh priorauth-api`). They carry their FR/US tags. The contract examples for C1, C2 and C5 are copied into the API tests. (Practices; Plan B1)
- The code is committed on `f1220/us5160-save-filter` as the plan's last step. Pushing and opening the PR are Kiran Rao's. (Practices)

## Assumptions

- **A1** The configuration key for the reviewer limit follows the team's style, kebab-case under `priorauth.` with a default in `@Value`. The code plan names the exact key. Reason: team code style, and requirements A3.
- **A2** The NM-02 sample request is pending (`PENDED` or `IN_REVIEW`), so the queue tests see it and AC1.1.13's row-count updates are real. Reason: AC1.1.13 expects row counts to change.

## Out of Scope

- Filter history, its limit, the injected clock and `GET /reviewers/{reviewerId}/filter/history`: US5163.
- Any screen change: US5161 and US5162.
- Allowed origins beyond `http://localhost:3000` (parent OQ4).
- A durable store, sign-in and access control (parent Out of Scope; A2).
- The hard-coded 2026 holiday file name (codekb TD-3).

## Open Questions (for this story's code plan)

- **OQ-U1.1** How the store's single lock is built, and the memory ceiling at the default limits. The parent's contract hands this to U1's code plan (Contract Open Questions, Domain Design R-03). The mob reviews it at plan approval.
- **OQ-U1.2** The real `404` body for `.` and `..`. It is recorded at build time. If it echoes the id, Kiran Rao raises a contract change with Meena Iyer (Contract R-04; Plan B1).
