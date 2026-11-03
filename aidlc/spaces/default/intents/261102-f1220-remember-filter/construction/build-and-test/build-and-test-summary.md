# Build and Test Summary — F1220 Remember my filter

**Standalone run on 2026-11-03** over `feature/F1220`, with all four story PRs merged (#81, #82, #83, #84): `priorauth-api` `d1d11a5`, `priorauth-web` `64c1612`. Test strategy: Standard.

## Overall Status

| Item | Status |
|---|---|
| Build | Success |
| Automated tests (verify script, both repos) | 166 of 166 passing: API 118, web 48. Exit 0 |
| End-to-end API checks with the screen's origin | 14 of 14 pass (E1-E14) |
| Manual screen checks (M1-M8) | Run by Divya Pillai and Tara Joshi in Chrome, using the keyboard: 6 pass; M6 and M7 partly pass (F-6, F-7, F-8) |
| Coverage | NOT MEASURED (team exception, kept) |
| Cross-story traceability | Every FR and AC is covered. AC1.3.5 is covered by manual check M5. The stories' `traceability.json` files are incomplete (F-2) |
| **Result** | **Not a full pass by the stage's rule.** 3 targets are Not Met (F-6, F-7, F-8) and 1 is Unverified (coverage). The team accepted all four for release 2027.Q1 R1 (see "Team Decisions") |

## Prerequisites

Java 21 with Maven, and Node.js 22 or later. No dependencies were added by F1220 in either repo. See `build-instructions.md`.

## Test Types Generated

| File | Why |
|---|---|
| `build-instructions.md` | Always |
| `integration-test-instructions.md` | Standard strategy: the contract boundaries, end-to-end API checks E1-E14, manual screen checks M1-M8 |
| `performance-test-instructions.md` | NFR7 memory bounds and the screen's timeout and ordering. No latency target exists |
| `security-test-instructions.md` | NFR3-NFR6 and the team's security checklist |

Unit tests are the stories' own, run here once through the verify script.

## Coverage Expectations per Story

| Story (unit) | Repo | Tests after the story | Line coverage |
|---|---|---|---|
| US5160 (U1) | api | 97 (+85) | NOT MEASURED |
| US5161 (U2) | web | 38 (+32) | NOT MEASURED |
| US5162 (U3) | web | 48 (+10) | NOT MEASURED |
| US5163 (U4) | api | 118 (+21) | NOT MEASURED |

The floor is the `feature` scope's 80% of lines. It is not measured in F1220 (the team's recorded exception, owner Meena Iyer).

## Target Verification Matrix

There was no NFR Requirements or NFR Design stage; the parent skipped them (Delivery Planning Q7). So the targets come from `requirements.md` (FR and NFR), the contract, and the four stories' code-generation plans.

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| T-BUILD | team Testing Posture | Verify script exits 0 for both repos | Exit 0; 118/118 and 48/48 | `test-results.md` | build-and-test | Met |
| T-NFR8-API | requirements NFR8 | `GET /requests/pending` and its tests pass, with only the FR3.2 counts changed | `PendingRequestsControllerTest` 3/3, `OverLimitFilterTest` 1/1, `TenantFilterTest` 3/3; E13 returns 4 rows | verify run, E13 | build-and-test | Met |
| T-NFR8-WEB | requirements NFR8 | The 6 tests from before F1220 still pass | All 6 F1210 tests among the 48 pass (the US5162 FR4.8 test changed on purpose and passes) | verify run | build-and-test | Met |
| T-NFR3-1KB | requirements NFR3 | A body over 1 KB gets 400 | 400 `invalid-body` | `SavedFilterBodyTest`; E11 | build-and-test | Met |
| T-FR1.4-LIMIT | requirements FR1.4, NFR7 | A new reviewer beyond the limit is refused (409 `reviewer-limit`); default 10,000; reads take no slot | Refused at a small limit; default `10000` in `application.yml` | `ReviewerLimitHttpTest`, `ReviewerFilterStoreTest` | build-and-test | Met |
| T-FR7.5-HIST | requirements FR7.5, NFR7 | At most 1,000 lines per reviewer, keeping the newest; default 1,000 | Holds at limit 3; default `1000` | `ReviewerFilterStoreTest` AC1.4.6, `ReviewerFilterHistoryTest` | build-and-test | Met |
| T-NFR2-ATOMIC | requirements NFR2 | A save and its line succeed or fail together | Refused saves write no line; 50 concurrent saves give 50 lines | AC1.4.3, AC1.4.7; E8 then E10 | build-and-test | Met |
| T-NFR4-ERR | requirements NFR4, contract | Fixed `{error, message}`, no trace, no echo; 405 and 406 with no body | As expected | contract and protocol-error tests; E8, E11, E12 | build-and-test | Met |
| T-NFR5-ESC | requirements NFR5 | `& < > " '` escaped in everything shown | Escaped | `render.test.js` AC1.2.10 | build-and-test | Met |
| T-NFR6-CORS | requirements NFR6, contract C5 | Only named origins, never `*`; `http://localhost:3000` allowed | Allowed for localhost:3000; 403 for evil.example; `*` refused at start-up | `BrowserAccessPolicyTest`; E1, E3, E4, E14 | build-and-test | Met |
| T-NFR9 | requirements NFR9 | Injected clock; tests isolated; logic in `src/` | `MutableClock`; per-test reviewer ids; `index.html` thin | US5163 and US5161 code summaries | build-and-test | Met |
| T-FR5.3-ORDER | requirements FR5.3 | Changes A, B, C send at most 2 saves (A then C); C stored and shown | As expected | `filter-session.test.js` AC1.2.7 | build-and-test | Met |
| T-C-TIMEOUT | contract (screen: 10 s, no retries) | Every screen call gives up after 10 s | Every call carries an `AbortSignal`; `TIMEOUT_MS = 10000` | `filter-session.test.js` (signal present); code reading | build-and-test | Met |
| T-NFR10-LABELS | requirements NFR10 | Visible labels; disabled state and failures in text | Labelled native select and checkbox; native button with text and `disabled`; messages in text | `render.test.js` AC1.2.1, AC1.3.2 | build-and-test | Met |
| T-NFR11-BRANCH | requirements NFR11 | Each story tests every new branch; each changed test file covers the happy path and at least 2 edge cases | Stated and reviewed in each story's code summary and mob code review | four code summaries | code-generation (stories) | Met |
| T-NFR10-KEYBOARD | requirements NFR10 | Picker, switch and Clear work by keyboard | All three work by keyboard in Chrome | M3 pass (Divya Pillai, Tara Joshi) | build-and-test (manual) | Met |
| T-AC1.3.5-FOCUS | stories AC1.3.5 | After Clear, focus moves to the Tenant picker | Focus moves to the picker | M5 pass | build-and-test (manual) | Met |
| T-FR5.2-CONTROLS (F-7) | requirements FR5.2; stories AC1.2.12 | After a failed call, the controls keep the filter the reviewer just chose | With the API stopped, the switch reads off again after the reviewer turned it on | M6 partial | build-and-test (manual) | Not Met (accepted: backlog and release notes) |
| T-M6-COUNT (F-8) | integration-test-instructions M6 | When the queue fails, the page shows no count for rows it doesn't have | The heading still says "4 requests" over an empty table. This matches US5161's design: AC1.2.12 leaves the count as it was | M6 partial | build-and-test (manual) | Not Met (accepted: backlog and release notes) |
| T-M7-PICKER (F-6) | integration-test-instructions M7; US5161 risk note | An open picker list survives an arriving answer | The picker and its focus survive, but every option element is rebuilt, so an open list can close | M7 partial | build-and-test (manual) | Not Met (accepted: backlog and release notes) |
| T-NFR11-COV80 | org Testing Posture (`feature` scope), requirements NFR11 | 80% line coverage | NOT MEASURED | team exception, owner Meena Iyer; kept on 2026-11-03 | build-and-test | Unverified (exception kept) |

## Readiness

- **Build-ready:** yes.
- **Test-ready:** yes. The automated suites, the end-to-end API checks and the manual screen checks M1-M8 have all run.
- **Deployment-ready:** not applicable; there is no deployed environment.
- **Release-ready, on the team's decisions below:** the feature PR to `main` can go ahead once the release PR pins `serve` (F-4). The version tags follow the merge. F-6, F-7, F-8 and the coverage exception ship as accepted known issues.

## Team Decisions, 2026-11-03

Decided by Dana Ortiz, Meena Iyer and the team. No dissent was recorded.

| Item | Decision | Owner / where |
|---|---|---|
| Manual checks | M1-M8 run by Divya Pillai and Tara Joshi in Chrome with the keyboard; results recorded in `test-results.md` | Done |
| F-6 (an open picker list can close when an answer arrives) | A follow-up story on the backlog, and a known issue in the 2027.Q1 R1 release notes | Backlog; release notes (Meena Iyer) |
| F-7 (after a failed call the switch reads off again) | A follow-up story on the backlog, and a known issue in the release notes | Backlog; release notes |
| F-8 (stale "4 requests" heading over an empty table when the queue fails) | A follow-up story on the backlog, and a known issue in the release notes | Backlog; release notes |
| 80% line coverage (T-NFR11-COV80) | The recorded exception stays; it is not measured in F1220 | Meena Iyer |
| F-1 (leftover 404 for `.` and `..`) | Fixed in the record: `eba5ee3` and `d0d882f` | Done (checked below) |
| F-4 (`npx serve .` starts the wrong `serve`) | Pin `npx serve@14` in `priorauth-web/README.md` in the release PR | Release PR |

F-6, F-7 and F-8 go into one follow-up story, which needs a Rally story id. All three are in US5161's code (`priorauth-web/src/filter-session.js`, `src/render.js`, `index.html`). F-8 is what AC1.2.12 asked for ("the count is left as it was"), so the follow-up story changes that acceptance criterion as well as the code.

## Findings

- **F-1: fixed.** `d0d882f` finished the contract change. A search of `contract-summary.md` and `stories.md` now finds "404" only in the change-log row that records the change.
- **F-2: The stories' `traceability.json` files are incomplete.**
  - US5160's lists its ACs but not FR1.1-FR1.4, FR2.x or FR3.x.
  - US5163's lists FR7.x but none of AC1.4.1-AC1.4.9.
  - The parent's `FR1`-`FR7` group headings have no entries.

  That is 19 IDs in all, and every one of them is tagged on a test or a main class in the repos (`cross-unit-traceability.md`), so this is a gap in the record, not in the tests.
- **F-3: Story records use IDs the parent's requirements don't declare.** These are `FR1.6`, `FR4.7`-`FR4.10` and `FR8.1`, added in Contract Design and the stories. `FR8.1` is the parent's NFR6. Harmless, but `requirements.md` is not the full list.
- **F-4: The README's `npx serve .` can start the wrong `serve`.** On this machine it started an old cached version on port 5000, which the API's origin list refuses. Decided: `priorauth-web/README.md` pins `npx serve@14` in the release PR. It is not changed yet.
- **F-5: The team practices note "`priorauth-api` has 12 tests" is out of date.** It is now 118. Memory changes only at a gate, so this is for the next learnings ritual.
- **F-6, F-7, F-8:** found by the manual checks M6 and M7. See the matrix and the decisions above.
- **Backlog, already accepted:**
  - the 404 body echoes the id on unmapped `/reviewers/...` paths (US5160 gate);
  - duplicate JSON keys are accepted, and the last value wins.

## Known Limitations

- Saved filters and history are lost on restart, and the API has no authentication. Both are accepted and named in the 2027.Q1 R1 release notes (Meena Iyer).
- Known issues for the release notes: F-6, F-7 and F-8 (above).
- History memory in the worst case is about 640 MB at the default limits. It is not measured, and there is no load test.
