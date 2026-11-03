# Code Generation Plan: US5161 Open the screen with my last filter

## Summary

- Builds: the Tenant picker and "Over limit only" switch on the reviewer screen, restored from and saved to the reviewer's saved filter (US5161, FR4, FR5)
- Touches: priorauth-web `src/filter-session.js` and `src/saved-filter-client.js` (new), `src/queue-filters.js`, `src/render.js`, `index.html`, `README.md`, and `test/`
- Tests: about 28 Node unit tests across 4 test files (2 new, 2 extended), plus the 6 existing tests kept green

## Context

- **Repo:** `priorauth-web` only. Branch `f1220/us5161-restore-filter`, cut from `origin/feature/F1220` (today `65a999b`, the same commit as `main`). The PR goes into `feature/F1220` and names the sibling stories US5160, US5162 and US5163. Divya Pillai pushes the branch and opens the PR, not AI-DLC.
- **Inputs:**
  - `inception/requirements-analysis/requirements.md` in this intent (FR4.1-FR4.9, FR5.1-FR5.3, NFR5, NFR8, NFR10, NFR11, A5, A6)
  - the parent's story US1.2 (AC1.2.1-AC1.2.12)
  - unit U2
  - contract C1, C2 and C4
  - ADR-004 and the `components.md` entries for ReviewerPage, FilterSession, SavedFilterClient, QueueFilters and QueueRenderer
- **New dependencies:** none. Everything uses the browser and Node built-ins: `fetch`, `AbortSignal.timeout`, `URL`, `node:test`, `node:assert/strict` and `node:fs`. Node here is v24.19.0, and `package.json` asks for >=20.
- **Unchanged:** `src/api.js` (ApiClient), `package.json`, and the existing tests in `test/api.test.js`, `test/queue-filters.test.js` and `test/render.test.js`. The two existing test files are only appended to.

## Design (ADR-004 split)

- **`src/saved-filter-client.js` (new, SavedFilterClient):** a DOM-free client for C1 and C2, with `fetchFn = fetch` as the last parameter.
  - `filterUrl(base, reviewer)` builds `{base}/reviewers/{encodeURIComponent(reviewer)}/filter`, with a trailing `/` on `base` removed. `tenantsUrl(base)` builds `{base}/tenants`.
  - `readFilter(base, reviewer, fetchFn)` sends a GET and returns the parsed body.
  - `saveFilter(base, reviewer, { tenant, overLimit }, fetchFn)` sends a PUT with `Content-Type: application/json` and a body of exactly `{"tenant", "overLimit"}`. It never sends extra fields.
  - `readTenants(base, fetchFn)` sends a GET and returns the parsed array.
  - A non-2xx answer throws `Error("priorauth-api answered <status>")`, the existing house message.
- **`src/filter-session.js` (new, FilterSession):** a DOM-free factory, `createFilterSession({ base, reviewer, fetchFn = fetch, onChange })`, returning `{ open, change, view }`. It has no classes. The view is `{ loading, tenants, tenant, overLimit, rows, message }`, and `onChange(view)` fires after every state change.
  - **Timeout:** the session wraps `fetchFn` once, so every call it makes carries `signal: AbortSignal.timeout(10000)` (contract: give up after 10 seconds). A timeout, a network error or a non-2xx answer is a failure. There are no retries.
  - **`open()` with a reviewer:** the view is `loading: true` and no rows. It reads the saved filter and the tenant list together. Then:
    - It normalizes the read: `{}` becomes `{tenant: null, overLimit: false}`. A body that isn't one of the two contract shapes is treated as a failure, because it is a trust boundary.
    - Read failure: unfiltered, with the saved-filter message (FR4.5).
    - Tenant list failure: the tenants list is empty, the saved tenant is kept, and the tenant-list message shows (FR4.7).
    - Saved tenant not in a loaded list: the tenant is dropped, `overLimit` is kept, and the saved-filter message shows. Nothing is saved (FR4.8).
    - Only then is the queue asked for, so the unfiltered queue never shows first (FR4.3).
  - **`open()` without a reviewer:** it reads the tenants and the unfiltered queue. The filter is never read or saved, and the won't-be-remembered message shows (A1).
  - **`change({ tenant, overLimit })`:** the change is applied at once and wins over a read that hasn't answered yet, so the late read is ignored (R-06, AC1.2.8). It asks the queue, and only the newest queue answer is shown (a sequence number). It saves when there is a reviewer. If the tenant list had failed, it asks for the list again (A5).
  - **Save ordering (FR5.3):** one save is in flight at a time, and the newest waiting choice replaces any older waiting one. So changes A, B and C send A, then C.
  - **Message (FR4.9):** the session keeps one flag per message and shows the highest flag set, in this order:
    1. queue couldn't be loaded
    2. wasn't saved
    3. tenant list couldn't be loaded
    4. saved filter couldn't be loaded
    5. won't be remembered

    A successful save clears "wasn't saved". A successful queue load clears the queue flag. A successful tenant-list read clears its flag. The texts are exported as `MESSAGES`, in the story's statement-of-fact wording, with A6 for the tenant list.
- **`src/queue-filters.js` (changed, QueueFilters):** adds `loadQueueFor(base, { tenant, overLimit }, fetchFn)`. It is the one place the contract's `overLimit` maps to the F1210 option `overLimitOnly` (OQ3). A null tenant or `false` leaves the parameter out. `filteredUrl` and `loadQueue` are unchanged.
- **`src/render.js` (changed, QueueRenderer):**
  - `esc` also escapes `'` as `&#39;` (NFR5).
  - New `renderControls()` returns the controls block:
    - `<label for="tenant">Tenant</label>` and a native `<select id="tenant">`
    - a native checkbox labelled "Over limit only"
    - the single `<p id="message" role="status">` message area
    - `data-testid` on the interactive elements
  - New `renderTenantOptions(tenants, selected)`: "All tenants" (value `""`) plus every tenant, escaped. It also includes `selected` when it isn't in the list (FR4.7).
  - New `renderQueue({ loading, rows })`:
    - the loading text while loading
    - nothing when the rows are unknown (the queue failed)
    - "No requests match this filter" for `[]`
    - otherwise `renderRows`
- **`index.html` (changed, ReviewerPage, thin):** it reads `?reviewer=` and `?api=`, writes `renderControls()` once, and creates the session.
  - On a control change it calls `session.change(...)`.
  - In `onChange` it sets the options, `select.value`, `checkbox.checked`, the message `textContent`, the rows and the count. It writes the count only when the rows are known.
  - The controls are written once and then updated through DOM properties, so keyboard focus isn't lost on each update (NFR10).
  - There is no filter logic in the page.

## Steps

Ordering follows the Testing Contract (test-after: build each testable layer, then write and run its tests before the next layer). The data-model, repository and API layers don't exist in this static screen and are omitted.

- [x] **Step 1: Branch and baseline** (FR4, FR5; Practices). Run `scripts\pull-all.ps1`, then in `priorauth-web` create `f1220/us5161-restore-filter` from `origin/feature/F1220`. Record the baseline with `scripts\verify.cmd priorauth-web`; the expected result is 6 of 6 passing at `65a999b`. Stop and report if it isn't green.
- [x] **Step 2: Verify the test runner** and record the exact command in `unit-test-instructions.md`: `scripts\verify.cmd priorauth-web`, which runs `node --test` over `test/`. Copy `c1-get-filter-saved.json`, `c1-get-filter-nothing-saved.json`, `c1-put-filter-request.json` and `c2-get-tenants.json` from the parent's `contract-design/examples/` into `priorauth-web/test/contract-examples/`. They are test data, not code (U2 note, Bolt B2 DoD).
- [x] **Step 3: SavedFilterClient: implement** `src/saved-filter-client.js`, with a line-1 purpose comment naming US5161 and C1/C2. (AC1.2.1, AC1.2.2, AC1.2.5)
- [x] **Step 4: SavedFilterClient: write and run its tests** in `test/saved-filter-client.test.js`:
  - the read URL and body from the C1 saved and nothing-saved examples
  - the PUT method, content type and body equal to `c1-put-filter-request.json`, with exactly two fields
  - tenants from `c2-get-tenants.json`
  - a non-2xx answer rejecting with the service and status
  - a reviewer id with `/`, `?` or space encoded into a single path segment

  Run `scripts\verify.cmd priorauth-web`.
- [x] **Step 5: QueueFilters: implement** `loadQueueFor` in `src/queue-filters.js`, tagging the changed lines US5161/OQ3. (FR4.3, FR5.1)
- [x] **Step 6: QueueFilters: write and run its tests** by appending to `test/queue-filters.test.js`:
  - `overLimit: true` with a tenant gives `tenant=TX-01&overLimit=true`
  - `overLimit: false` and tenant `null` give the bare queue URL
  - a non-2xx answer rejects

  Run the verify script.
- [x] **Step 7: FilterSession: implement** `src/filter-session.js` as designed above. (FR4.1, FR4.3-FR4.9, FR5.1-FR5.3, A1, A5, R-06)
- [x] **Step 8: FilterSession: write and run its tests** in `test/filter-session.test.js`, using a stub `fetchFn` whose answers the test resolves by hand, and the contract examples. Each test uses its own reviewer id:
  - restore with loading and no unfiltered queue call first (AC1.2.2)
  - `{}` and `{null,false}` open unfiltered (AC1.2.3)
  - read fails by 500, network error or 400 → unfiltered with the saved-filter message (AC1.2.4)
  - a malformed read body → the same as a failure
  - a change applies and saves `{"tenant":"NM-02","overLimit":false}` (AC1.2.5)
  - save fails → the filter is kept with the not-saved message, and a later successful save clears it (AC1.2.6)
  - A, B, C send exactly two PUTs, A then C, and a late queue answer for A is ignored (AC1.2.7)
  - a change before the read answers wins, and the late read is ignored (AC1.2.8)
  - no reviewer: no filter GET or PUT, the won't-be-remembered message, and the controls still filter (AC1.2.9)
  - queue fails → the queue message, and the next change asks again (AC1.2.12)
  - tenants fail → the saved tenant is kept with the tenant-list message, and the next change retries and clears it (FR4.7, A5)
  - an unknown saved tenant is dropped, `overLimit` is kept, the message shows, and no PUT is sent (FR4.8)
  - read and queue both fail → the queue message, then the saved-filter message after a successful queue load (FR4.9)
  - every call carries an abort signal (the contract's 10 s timeout)

  Run the verify script.
- [x] **Step 9: QueueRenderer: implement** the `esc` change and `renderControls`, `renderTenantOptions` and `renderQueue` in `src/render.js`, tagging the changed lines US5161. (AC1.2.1, AC1.2.10, AC1.2.11, AC1.2.12, NFR5, NFR10)
- [x] **Step 10: QueueRenderer: write and run its tests** by appending to `test/render.test.js`:
  - the controls markup has `<label for="tenant">`, a native select, a checkbox labelled "Over limit only", a single `role="status"` element and `data-testid` attributes (AC1.2.1)
  - the options are "All tenants" plus exactly the given tenants, with `selected` on the current one, and a kept saved tenant not in the list is still offered (FR4.7)
  - a tenant `<b>'x"&` renders escaped, `'` as `&#39;`, in the options and the rows (AC1.2.10)
  - an empty queue gives "No requests match this filter", unknown rows give no such text, and loading gives the loading text (AC1.2.11, AC1.2.12, AC1.2.2)

  Run the verify script.
- [x] **Step 11: ReviewerPage: wire** `index.html` as designed above, adding a few lines of CSS for the controls. It holds no logic of its own and isn't tested, by team practice. Keyboard use is listed for the manual check at the feature's Build and Test.
- [x] **Step 12: Documentation:** add the `?reviewer=` page parameter and the serve URL `http://localhost:3000/?reviewer=rita.k&api=http://localhost:8080` to `README.md`. Fill in `code-summary.md` and `traceability.json` in this intent's record.
- [x] **Step 13: Final verify and commit:** run `scripts\verify.cmd priorauth-web`. Every test must pass, the 6 baseline tests included. Then commit on `f1220/us5161-restore-filter` with the message `US5161 open the screen with my last filter (intent f1220-us5161)`. Don't push and don't open the PR.

## Story-to-Step Traceability

| Requirement / AC | Steps |
|---|---|
| AC1.2.1 controls (FR4.2, FR4.6, NFR10) | 3-4, 9-11 |
| AC1.2.2 restore without flash (FR4.1, FR4.3) | 3-4, 7-8, 9-10 |
| AC1.2.3 nothing saved (FR4.4) | 7-8 |
| AC1.2.4 read fails (FR4.5) | 7-8 |
| AC1.2.5 change applied and saved (FR5.1) | 3-8 |
| AC1.2.6 save fails (FR5.2) | 7-8 |
| AC1.2.7 quick changes (FR5.3) | 7-8 |
| AC1.2.8 / R-06 change before read wins | 7-8 |
| AC1.2.9 / A1 no reviewer | 7-8, 11 |
| AC1.2.10 safe display (NFR5) | 9-10 |
| AC1.2.11 no matching requests | 9-10 |
| AC1.2.12 queue can't load | 7-10 |
| FR4.7 tenant list fails, A5 retry | 7-8, 9-10 |
| FR4.8 unknown saved tenant | 7-8 |
| FR4.9 message priority, A6 wording | 7-8 |
| NFR8 6 existing tests green | 1, 13 |

## Security checklist (for the mob's plan review)

- **Request values validated and size-limited:**
  - The reviewer id is sent percent-encoded as one path segment, so it can't change the path. The API validates it (C1).
  - The save body is built from the two controls only, and the tenant comes from the picker's options.
  - A read answer that isn't a contract shape is rejected.
- **API data escaped:** every tenant id, row value and option goes through `esc`, which now also escapes `'`. Messages are fixed texts set through `textContent`.
- **No file path or cache key from a caller's value:** none is built.
- **Error responses:** none are produced by the screen. API error bodies are never parsed or shown. The screen shows only its fixed messages.
- **CORS:** owned by U1 (C5). The screen calls only the `?api=` base.

## Risks and Notes

- **The saved-filter message stays until a reload.** The saved filter is read only on open, so FR4.9 clears its message only on a reload, even after a later successful save. A higher message still covers it while in force. Raise it at plan review if a successful save should clear it too.
- **The end-to-end run needs U1.** Until U1 merges into `feature/F1220`, the API has no `/reviewers` or `/tenants` endpoints and the browser can't call it (CORS). The screen is proven against stubs and the contract examples only (Bolt B2).
- **The test command is repo-wide.** `scripts\verify.cmd priorauth-web` runs every test file in the repo, because team practice runs tests only through the verify script. This intent has a single repo and no other unit, so nothing runs twice.

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "We build each testable layer of a story, then write and run that layer's tests before starting the next layer; a bug fix instead starts with a failing test that reproduces the bug.",
  "scope": "express",
  "test_strategy": "minimal",
  "project_type": "brownfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "team",
      "text": "- **Methodology**: test-after\n- **Methodology evidence**: Affirmed by the team in the interview (Q4, answer A). The git history could not show a cadence (each F1210 story landed as one commit with its code and tests together); the team chose tests after each layer, keeping the workspace rule that a bug fix starts with a failing test.\n- **Ordering**: We build each testable layer of a story, then write and run that layer's tests before starting the next layer; a bug fix instead starts with a failing test that reproduces the bug.\n- Tests run only through the workspace verify script, `scripts/verify.sh` (`scripts\\verify.cmd` on Windows), never ad hoc. It runs `mvn -q test` for `priorauth-api` and `npm test --silent` (`node --test`) for `priorauth-web`.\n- CI stand-in (Q6, answer A): there is no CI service; the remotes are local repos. Before every PR the story owner runs the verify script with the repos named (`scripts\\verify.cmd priorauth-api priorauth-web`, or `scripts/verify.sh priorauth-api priorauth-web`) on the rebased branch and pastes the result into the PR. Setting up real CI is separate work.\n- Before any code change we record each repo's test baseline through the verify script with the repos named. A no-argument run on a clean `main` tests nothing and still exits 0, so it never counts as a baseline (Q7 A).\n- API tests stay independent of each other: each test uses its own `reviewerId`, or the store is reset between tests, so saved filters and history never leak between tests or depend on execution order (Q7 B).\n- Any time a test checks comes from a clock the test controls (an injected `Clock`), never the system clock (Q7 C).\n- Screen logic lives in `src/` modules that have tests; `index.html` only calls them. Code written inside `index.html` is neither tested nor counted (Q7 D).\n- New branching, parsing, money or security logic gets a test, and each story tests every new branch it adds. Every new or changed test file covers the happy path and at least two error or edge cases. Existing F1210 test files are not back-filled unless a story changes them or a plan names it.\n- Tests carry the FR/US they prove, in the test name or a comment on the `@Test`, as the existing tests do.\n- Coverage (Q5, answer X; Q13, answer A): F1220 adds no coverage tooling. The 80% line-coverage floor of the `feature` scope stays the target, but it is not measured in F1220. Build and Test reports coverage as NOT MEASURED and never claims the floor is met. This is a recorded exception to the organisation's coverage and CI-before-merge rule, owned by Meena Iyer, until a later feature adds JaCoCo (`priorauth-api`), Node test coverage (`priorauth-web`) and CI.\n- Tools: JUnit 5, AssertJ and Spring MockMvc in `priorauth-api`; the Node built-in runner (`node --test`) with `node:assert/strict` and an injected `fetchFn` in `priorauth-web`. There are no browser or DOM tests.\n- Baselines to preserve: `priorauth-web` 6 of 6 passing at `65a999b`. `priorauth-api` has 12 tests; its baseline is not yet recorded; Kiran Rao takes it through the verify script with the repos named before the first code change."
    }
  ],
  "obligations": {
    "strategy": "minimal",
    "strategy_volume": [
      "One verifiable test per requirement at the narrowest effective level.",
      "At least one happy-path unit test per component.",
      "Unit tests are the default; a bugfix/security scope floor may require an integration or E2E regression when that is the narrowest level that reproduces the defect."
    ],
    "scope_floor": [
      "Keep the existing test suite green.",
      "This scope adds no extra new-test floor beyond the selected test strategy."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Verify the existing test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Verify the existing test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:3ea1c5de97d92b72d157e8986e8f028cd43fe070f151b748e1d7c3c0a11cdd41",
  "contract_sha256": "sha256:1a77f4180a609a7f4d75b1d214b3fb66fe0d8211649c167a97a0163da56ad1f8"
}
```
