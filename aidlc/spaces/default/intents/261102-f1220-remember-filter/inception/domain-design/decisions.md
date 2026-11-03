# Architecture Decisions — F1220 Domain Design

Answers cited as Q<n> are from `domain-design-questions.md` (confirmed). The team decided each one in the mob session.

## ADR-001: One store owns saved filters and their history

- **Status:** Accepted (Q1)
- **Context:**
  - A save and its history line must succeed or fail together (NFR2, AC1.4.7).
  - A refused save writes no line (FR7.2).
  - The draft contract wants one in-memory store behind one replaceable class (NFR1).
  - The work is split across two owners: US1.1 creates the save path and US1.4 adds history to it.
- **Decision:** a single `ReviewerFilterStore` owns both `SavedFilter` and `FilterHistoryLine`. A save replaces the filter and appends the line under one lock. US1.4 extends the class US1.1 creates.
- **Consequences:**
  - Positive: atomicity is local and simple to test, and a durable store can later replace one class.
  - Positive: limits are enforced in one place.
  - Negative: the US1.1 and US1.4 owners change the same class, so US1.4's branch is cut only after US1.1 merges.
  - Negative: one lock serialises all saves, which is acceptable at the expected volume. NFR Design checks this.
- **Alternatives Rejected:**
  - **Separate filter store and history log:** each owner gets their own class, but every save writes to two places with hand-made rollback, which is the failure AC1.4.7 guards against.
  - **Event-based history (the store publishes, a log subscribes):** loose coupling, but a save could succeed while its line is lost. That breaks NFR2.
- **Security and compliance:**
  - The store keeps caller-supplied ids only as map keys, never as file paths.
  - The limits bound memory use from unauthenticated callers (NFR7).
  - Data is lost on restart, which is accepted and stated in the release notes (A2).

## ADR-002: A tenant directory owns the known-tenant list

- **Status:** Accepted (Q2)
- **Context:**
  - Known tenants are the tenant ids in the request export (FR3.1).
  - Save validation and `GET /tenants` both need the list.
  - `RequestStore` has no tenant method.
  - `HolidayCalendar` builds a file path from a tenant id, so caller values must never reach it.
- **Decision:** a new `TenantDirectory` reads `RequestStore` once at start-up and answers "known?" (exact, case-sensitive) and "list" (stable order).
- **Consequences:**
  - Positive: one clear owner, no caller value near file paths, and RequestStore stays single-purpose.
  - Negative: one more small class.
  - Negative: the list reflects the export as loaded at start-up. That matches RequestStore, which also loads once.
- **Alternatives Rejected:**
  - **`knownTenants()` on RequestStore:** fewer classes, but it mixes "load requests" with "answer tenant questions" and widens a class other code depends on.
  - **A configured tenant list:** rejected in Requirements Analysis (RQ3). It could drift from the export.
- **Security and compliance:** validating against a fixed set at the boundary keeps unknown tenant values out of storage and history.

## ADR-003: New controllers for the new endpoints, with a scoped error handler

- **Status:** Accepted (Q3)
- **Context:**
  - Four new endpoints need strict validation and safe error bodies (NFR3, NFR4).
  - The queue endpoint must keep its behaviour, including `200 []` for an unknown tenant and its current errors (AC1.1.13).
- **Decision:**
  - `ReviewerFilterController` serves the three `/reviewers/...` endpoints, and `TenantsController` serves `/tenants`.
  - `NewEndpointErrorHandler` applies only to those two controllers.
- **Consequences:**
  - Positive: the old endpoint can't change by accident, the new error contract is uniform, and each controller is small.
  - Negative: two error styles exist in the API until a later change aligns them. They are documented in Contract Design.
- **Alternatives Rejected:**
  - **One controller for all four endpoints:** fewer files, but it mixes the tenant list with reviewer resources.
  - **Extending `PendingRequestsController`:** reuses existing wiring, but risks changing the queue's errors and behaviour.
  - **A global error handler:** simpler, but it would change the queue endpoint's error bodies.
- **Security and compliance:**
  - Reviewer-id validation and the 1,024-byte body limit happen in the controller, before anything is stored.
  - Error bodies never echo caller input.

## ADR-004: The screen logic is split into a client, a session and the renderer

- **Status:** Accepted (Q4; Divya Pillai and Tara Joshi agreed)
- **Context:**
  - Screen logic must be DOM-free and tested; `index.html` only calls it (team practice).
  - US1.2 adds reading, saving, tenants, save ordering, late-read handling and messages.
  - US1.3 adds Clear.
  - Two owners change the screen in sequence.
- **Decision:**
  - `SavedFilterClient` handles the REST calls.
  - `FilterSession` handles ordering, late answers, messages and Clear.
  - `QueueRenderer` is extended for the controls and the message area, all through `esc`.
  - `QueueFilters` keeps the queue request and maps `overLimitOnly` to `overLimit` in one place.
  - US1.3 changes only `FilterSession` and `QueueRenderer`.
- **Consequences:**
  - Positive: the riskiest logic is isolated and fully testable, and the two owners' changes are confined to known files.
  - Negative: more modules than today. The flow of one change crosses three of them.
- **Alternatives Rejected:**
  - **One new module for everything:** simpler to find, but mixes networking with ordering logic and makes US1.3's change touch US1.2's whole file.
  - **Logic in `index.html`:** quick, but untestable and against the team rule.
- **Security and compliance:** all rendering goes through the one `esc` helper, which also escapes `'` (NFR5).

## ADR-005: History lines carry the reviewer id and take their time from an injected clock

- **Status:** Accepted (FR7.1, A2, R-01, R-07; Q1 places it in the store)
- **Context:**
  - Nina needs who, what and when.
  - The requirements say a line holds the reviewer id (FR7.1). FR7.3's example omits it, and Meena Iyer settles that wording in Contract Design (R-07).
  - Tests must control time (NFR9).
- **Decision:**
  - Each `FilterHistoryLine` has `at` (UTC, cut to the second), `reviewer`, `tenant` and `overLimit`, plus an internal `sequence` that keeps the order of saves within the same second.
  - `at` comes from an injected `java.time.Clock`.
- **Consequences:**
  - Positive: lines are self-describing and tests are deterministic.
  - Negative: `reviewer` repeats the path id, and it is a claim, not proof of who saved (A2).
- **Alternatives Rejected:**
  - **Omitting `reviewer`, since the path names it:** a smaller body, but it contradicts FR7.1 and the release-notes wording.
  - **The system clock:** simpler, but untestable (team practice).
- **Security and compliance:** the reviewer id is validated before it is stored. The line records the claimed id only, as the release notes state.

## ADR-006: Browser access to the API is limited to named origins

- **Status:** Accepted (NFR6, AC1.1.12; built in US1.1)
- **Context:**
  - The screen calls the API from the browser, and the new `PUT` needs a preflight.
  - The API has no cross-origin settings today.
  - The team's security checklist forbids `*`.
- **Decision:**
  - `BrowserAccessPolicy` allows the configured named origins for the new endpoints and `GET /requests/pending`.
  - The default is the screen's local development origin. NFR Design fixes the origin list (OQ4).
- **Consequences:**
  - Positive: the screen works from the browser without opening the API to every site.
  - Negative: every new screen origin needs a configuration change.
- **Alternatives Rejected:**
  - **Allow `*`:** simplest, but forbidden by the team's checklist.
  - **Serve the screen from the API's origin:** no cross-origin setup is needed, but it changes how both repos are run and deployed. That is out of scope.
- **Security and compliance:** limiting origins reduces cross-site requests. It does not replace sign-in, which is accepted as out of scope (A2).
