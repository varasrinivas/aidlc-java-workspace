# Requirements — US5163 Filter history (F1220 U4 `us5163-filter-history`)

This story's requirements were approved in the parent intent, 261102-f1220-remember-filter. This file restates the subset US5163 builds, keeping the parent's IDs exactly, and adds the implementation assumptions confirmed for this story. It adds no new requirement. Where this file and the parent's documents disagree, the parent's documents win; changes go through Meena Iyer.

- **Rally:** US5163, owner Arjun Nair. **Repo:** `priorauth-api` only. **Branch:** `f1220/us5163-filter-history`, cut from `origin/feature/F1220` (2dbc68b, which holds US5160).
- **Depth:** Minimal. **Test strategy:** Minimal.

## Intent Analysis

- **Goal:** Nina, the nurse manager, can tell why a reviewer did not see a request. She reads a history of every filter the reviewer saved, newest first, through the API. (Parent intent; story US1.4)
- **Type:** an enhancement to US5160's code. It extends `ReviewerFilterStore`'s save so that every save also writes a history line, and adds one read endpoint.
- **Scope:** one component (`priorauth-api`): store, controller, configuration and tests. No screen change.

## Functional Requirements

From the parent's `requirements.md` (FR7, FR1.5), with the C3 contract settling the line shape:

- **FR7.1** Every successful save (`PUT /reviewers/{reviewerId}/filter`) writes exactly one history line, including "Clear filters" and a save that repeats the current filter. The line has four fields, `at`, `reviewer`, `tenant` and `overLimit` (C3 `HistoryLine`):
  - `at`: the UTC instant cut (not rounded) to the second, ISO-8601 with `Z`, for example `2027-01-12T09:15:30Z`
  - `reviewer`: the reviewer id in the path
  - `tenant`: the saved tenant, or `null`
  - `overLimit`: the saved switch
- **FR7.2** A refused save writes no line. Refusals include an invalid reviewer id, an invalid body, an unknown tenant and the reviewer limit.
- **FR7.3** `GET /reviewers/{reviewerId}/filter/history` answers 200 with that reviewer's lines, newest first. Lines with the same `at` keep save order, newest first. The C3 four-field shape replaces FR7.3's three-field example (R-07).
- **FR7.4** A reviewer with no saves gets `[]`, and the read stores nothing and takes no reviewer slot. An invalid reviewer id gets `400 invalid-reviewer-id`, and so do `.` and `..` (contract change 2026-11-03).
- **FR7.5** At most the newest N lines are kept per reviewer, where N is the history limit (default 1,000). The oldest line is dropped when a new line would pass N.
- **FR7.6** The history is read through the API only. No screen view is added.
- **FR1.5** When saves for one reviewer arrive close together, the last save to complete wins, and each completed save writes its own line.

Acceptance criteria AC1.4.1-AC1.4.9 in the parent's `user-stories/stories.md` are the pass/fail tests for these requirements.

## Non-Functional Requirements

- **NFR2 Atomic save:** a save and its history line succeed or fail together, inside the store's single lock (C6). There is never a saved filter without its line, and never a line without its save. AC1.4.7 proves it.
- **NFR4 Error responses:** a refused history call answers with the fixed `{error, message}` body for its code. There is no stack trace, no `path` or `instance`, and no caller input in the body (AC1.4.8, AC1.1.10).
- **NFR6 Cross-origin calls:** the history path falls under the existing CORS rule for `/reviewers/**` (C5). This story makes no change.
- **NFR7 Memory bound:** at the defaults, at most 10,000 reviewers × 1,000 lines. A test with small configured limits (for example 3 lines) shows a reviewer's history never holds more than the limit and keeps the newest lines (AC1.4.6).
- **NFR9 Testability:** history times come from an injected clock the tests control. History tests use their own reviewer ids.
- **NFR11 Coverage:** each new branch has a test. Each new or changed test file covers the happy path and at least two error or edge cases. Line coverage is NOT MEASURED in F1220 (team exception).

## Constraints

- Java 21, Spring Boot, Jackson 3 (`tools.jackson.databind`), and the team's `priorauth-api` code style (`team.md` Code Style).
- `ReviewerFilterStore` keeps the meaning of `save` and `read`. US5163 only adds the history line and the `history` operation (C6). The store imports no Spring web types.
- The C3 contract is owned by Meena Iyer. This story does not change it.
- Tests run only through `scripts\verify.cmd priorauth-api` (Windows) or `scripts/verify.sh priorauth-api`. The baseline is recorded on the story branch before the first code change.
- No new dependency is added.

## Assumptions

Confirmed by Arjun Nair, 2026-11-03 (`requirements-analysis-questions.md` Q1, answer A):

- **A1 History limit setting.** `priorauth.reviewer-filter.max-history-lines: 1000` is added to `application.yml` beside `max-reviewers`, with a comment naming FR7.5 and a default in `@Value`. This is the configurable limit of the parent's A3.
- **A2 Endpoint location.** The history endpoint goes in `ReviewerFilterController` (C3). `NewEndpointErrorHandler` (scoped to that controller) and `NewEndpointProtocolErrorHandler` (covering `/reviewers/**`) cover it unchanged. Other methods answer 405 and a non-JSON `Accept` answers 406, both with no body.
- **A3 Clock.** A UTC `java.time.Clock` bean is added and injected into `ReviewerFilterStore`. Tests supply their own clock.
- **A4 Contract examples.** `c3-get-history.json` and `c3-get-history-empty.json` are copied from the parent's `contract-design/examples/` into `src/test/resources/contract/f1220/`, and the tests read them.
- **A5 Invalid ids.** Every invalid reviewer id, including `.` and `..`, answers `400 invalid-reviewer-id` with the fixed body on the history call.
- **A6 Memory.** No cap beyond NFR7 is added.
- **A7 Test isolation.** Each history test uses its own reviewer ids, because the Spring tests share one store.

## Out of Scope

- A history view on the screen (FR7.6), and any `priorauth-web` change.
- A durable store, sign-in, and limiting who may read a reviewer's history (parent A2, Scope).
- Exporting the history or keeping it for a set retention period.
- Changing the C3 contract or the behaviour of the existing PUT and GET filter calls.
- The release-notes line, which Meena Iyer writes.

## Open Questions

None. The `.`/`..` question (OQ-U1.2) was closed by the contract change of 2026-11-03.

## Sources

- Initial description: `project-description.json` (Build US5163 of Rally F1220 ...)
- Parent: `aidlc/spaces/default/intents/261102-f1220-remember-filter/inception/requirements-analysis/requirements.md` (FR7, FR1.5, NFR2, NFR4, NFR6, NFR7, NFR9, NFR11, A2, A3)
- Parent: `.../inception/user-stories/stories.md` (US1.4, AC1.4.1-AC1.4.9)
- Parent: `.../inception/contract-design/contract-summary.md` (C3, C5, C6, Changes after approval)
- Parent: `.../inception/units-generation/unit-of-work.md` (U4) and `.../delivery-planning/bolt-plan.md` (B4)
- Code knowledge base: `aidlc/spaces/default/codekb/priorauth-api/` (scan of `feature/F1220` 2dbc68b)
- `requirements-analysis-questions.md` Q1 (A1-A7)
