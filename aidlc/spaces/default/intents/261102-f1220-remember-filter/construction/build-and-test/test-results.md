# Test Results — F1220 Remember my filter (feature build, 2026-11-03)

Standalone Build and Test run over `feature/F1220`, with all four story PRs merged: `priorauth-api` at `d1d11a5`, `priorauth-web` at `64c1612`. Local heads equal `origin/feature/F1220` in both repos.

## Build

**Success.** `mvn -q test` compiled `priorauth-api` with no errors. `priorauth-web` has no build step.

## Automated Tests: `scripts\verify.cmd priorauth-api priorauth-web`

Exit code **0**. One run, from the workspace root.

| Repo | Total | Passed | Failed | Skipped | Source of the count |
|---|---|---|---|---|---|
| `priorauth-api` | 118 | 118 | 0 | 0 (errors 0) | Sum of `target/surefire-reports/*.txt`, 18 classes |
| `priorauth-web` | 48 | 48 | 0 | 0 | `node --test` summary: `tests 48, pass 48, fail 0` |

The story intents' unit-test instructions all name this same script, each with only its own repo. Running it once with both repos covers every one of them, so no test is counted twice.

**Per class, `priorauth-api`:**

| Class | Tests |
|---|---|
| `aging.AgeBadgeTest` | 1 |
| `aging.BusinessDaysTest` | 4 |
| `api.BrowserAccessPolicyTest` | 5 |
| `api.DotReviewerIdTest` | 4 |
| `api.NewEndpointProtocolErrorTest` | 6 |
| `api.OverLimitFilterTest` | 1 |
| `api.PendingRequestsControllerTest` | 3 |
| `api.ReviewerFilterContractTest` | 7 |
| `api.ReviewerFilterControllerTest` | 23 |
| `api.ReviewerFilterHistoryTest` | 10 |
| `api.ReviewerIdsTest` | 9 |
| `api.ReviewerLimitHttpTest` | 3 |
| `api.SavedFilterBodyTest` | 15 |
| `api.TenantFilterTest` | 3 |
| `api.TenantsControllerTest` | 3 |
| `store.RequestStoreTest` | 3 |
| `store.ReviewerFilterStoreTest` | 15 |
| `store.TenantDirectoryTest` | 3 |

**How the counts add up across stories:**

- API: 12 before F1220, 97 after US5160, 118 after US5163.
- Web: 6 before F1220 (at `65a999b`), 38 after US5161, 48 after US5162.
- The merged feature branch gives exactly the last story's numbers in each repo, so nothing was lost in the merges.

`DotReviewerIdTest` printed the live answers for `.` and `..`: `400 application/json {"error":"invalid-reviewer-id",...}` on PUT and GET. That matches the contract change of 2026-11-03.

## End-to-End API Checks (Running API, `Origin: http://localhost:3000`)

The API ran with `mvn spring-boot:run` on port 8080. Every check was sent from PowerShell with the screen's origin. The full table of checks is in `integration-test-instructions.md` §2.

| # | Result | Observed |
|---|---|---|
| E1 | Pass | 200 `["NM-02","TX-01"]`, ACAO `http://localhost:3000` |
| E2 | Pass | 200 `{}` |
| E3 | Pass | 200, ACAO `http://localhost:3000`, methods `GET,PUT` |
| E4 | Pass | 403, no ACAO |
| E5 | Pass | 204 |
| E6 | Pass | 200 `{"tenant":"TX-01","overLimit":true}` |
| E7 | Pass | 200, 3 rows, all TX-01 and over limit |
| E8 | Pass | 400 `{"error":"unknown-tenant","message":"Tenant is not a known tenant."}`, no echo of `<script>` |
| E9 | Pass | 204 |
| E10 | Pass | 200, 2 lines newest first (Clear, then TX-01), both `2026-11-03T02:16:31Z`. The refused E8 wrote no line |
| E11 | Pass | 400 `invalid-body`, fixed message |
| E12 | Pass | 400 `invalid-reviewer-id`, id not echoed |
| E13 | Pass | 200, 4 rows including `PA-10270` NM-02 (FR3.2, FR3.3) |
| E14 | Pass | 403, no ACAO |

The screen was served with `npx serve@14 . -l 3000` and answered 200 on `/`. The README's plain `npx serve .` started an old cached `serve` on port 5000 instead. See finding F-4 in the summary.

## Manual Screen Checks (M1-M8)

**Run on 2026-11-03 by Divya Pillai and Tara Joshi, in Chrome, using the keyboard.** They tested `feature/F1220` (API `d1d11a5`, screen `64c1612`), with the screen served by `npx serve@14 . -l 3000`. The checks are defined in `integration-test-instructions.md` §3.

The browser tool's attempt earlier in this run was refused for permission. The checks below were done by people, and this record keeps their results.

| # | Check | Result | Notes |
|---|---|---|---|
| M1 | First open unfiltered; picker lists All tenants, NM-02 and TX-01 | Pass | |
| M2 | The saved filter is restored on reload, with no unfiltered flash | Pass | |
| M3 | Keyboard only: Tab order, picker, switch, Clear | Pass | NFR10 keyboard |
| M4 | Visible labels; disabled state and messages shown in text | Pass | |
| M5 | Clear resets both, shows the whole queue, and focus moves to the Tenant picker | Pass | **AC1.3.5** |
| M6 | API stopped, then a control is changed | **Partial** | The message shown is "The queue couldn't be loaded. Try again in a moment.", which is right by the message priority rule (FR4.9). Two faults: **F-7**, the switch reads off again after the reviewer turned it on; and **F-8**, the heading still says "4 requests" over an empty table |
| M7 | The open picker list while an answer arrives | **Partial** | The picker element and its focus survive an answer, but every option element is rebuilt, so an open list can close (**F-6**) |
| M8 | Without `?reviewer=`: the controls filter, nothing is saved, and the page says so | Pass | |

**Six passed and two partly passed.** F-6, F-7 and F-8 are screen behaviour faults in `priorauth-web` (US5161 code). They break no API contract and lose no data.

## Coverage

**NOT MEASURED.** F1220 adds no coverage tooling, under the team's recorded exception owned by Meena Iyer. The 80% line-coverage floor is not claimed.

## Failure Handling (Single-Stage Run: Diagnosis and Options Only)

**Failure predicate:** every command passed, but three applicable targets are **Unverified** (`build-and-test-summary.md`, Target Verification Matrix). So this run does not count as a successful Build and Test. This is a standalone run, so nothing jumps back to another stage. The diagnosis and options are below, for the team to decide.

**Rung 1 (in-stage fix).** The keyboard and focus checks are inside this stage's remit, but they need a browser. Attempt 1, the browser tool, was refused for permission. No second attempt was made, because the fix needs a person or a permission grant.

**Rung 2 (classified, with impact estimates).** None of the three gaps is a defect in the generated code. Two are missing evidence (a manual check not yet run). One is a target that is deliberately not measured under a recorded exception.

| Gap | Fix | Estimated impact |
|---|---|---|
| T-NFR10-KEYBOARD, T-AC1.3.5-FOCUS (manual) | A. A person runs M1-M8 in a browser and records the results here. | About 20 minutes for one person. No code change, no cost, no risk. |
| | B. Allow the browser tool for this project, and AI-DLC re-runs this stage and does M1-M8 with Playwright. | About 10 minutes. No code change. The evidence is a scripted browser, not a screen-reader user. |
| T-NFR11-COV80 (coverage floor) | C. Keep the recorded exception. It stays Unverified and is listed in the release notes and the feature PR. | No effort. The risk is the one the team already accepted, owned by Meena Iyer. |
| | D. Measure coverage now: `node --test --experimental-test-coverage` in `priorauth-web` (no new dependency), and the JaCoCo Maven plugin in `priorauth-api` (a new build plugin, which has to be named in a plan first). | About 2-3 hours, plus a plan and a review. It goes against the team's "no coverage tooling in F1220" decision, so the team would have to change that first. The result might show the floor is not met. |

Giving up on a target is the team's decision to make, not AI-DLC's.

### Outcome, 2026-11-03

- **Option A was taken.** Divya Pillai and Tara Joshi ran M1-M8 (above).
  - T-NFR10-KEYBOARD and T-AC1.3.5-FOCUS are now **Met**.
  - M6 and M7 found three screen faults (F-6, F-7, F-8). Each has its own target in the matrix, verdict **Not Met**.
- **Option C was taken.** T-NFR11-COV80 stays **Unverified** under the recorded exception.
- The decision record is in `build-and-test-summary.md`, "Team Decisions, 2026-11-03".

**The failure predicate still holds.** Three targets are Not Met and one is Unverified, so this is not a successful Build and Test by the stage's own rule. Dana Ortiz, Meena Iyer and the team decided to accept these gaps for 2027.Q1 R1. This record does not turn any of them into Met.
