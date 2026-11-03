# Test Results — F1220 US5163 (`priorauth-api`)

## Build Status

**Success.** `scripts\verify.cmd priorauth-api` exited 0 on 2026-11-03 (about 14 seconds).

- Code: `priorauth-api` branch `f1220/us5163-filter-history` at `3cf2206`, one commit on `origin/feature/F1220` (`2dbc68b`); working tree clean.
- After a fresh `git fetch`, the branch is 0 commits behind `origin/feature/F1220`, so no rebase was needed for this run.

## Commands Run

| Source | Command | Runs | Result |
|---|---|---|---|
| `construction/code-generation/unit-test-instructions.md` (the only test command; the Minimal strategy generates no other instruction files) | `scripts\verify.cmd priorauth-api` | once | exit 0 |

## Test Results

**118 tests: 118 passed, 0 failed, 0 errors, 0 skipped.** From `priorauth-api/target/surefire-reports/*.txt`:

| Test class | Tests | US5163 |
|---|---|---|
| `aging.AgeBadgeTest` | 1 | unchanged |
| `aging.BusinessDaysTest` | 4 | unchanged |
| `api.BrowserAccessPolicyTest` | 5 | unchanged |
| `api.DotReviewerIdTest` | 4 | changed (3 → 4) |
| `api.NewEndpointProtocolErrorTest` | 6 | changed (5 → 6) |
| `api.OverLimitFilterTest` | 1 | unchanged |
| `api.PendingRequestsControllerTest` | 3 | unchanged |
| `api.ReviewerFilterContractTest` | 7 | unchanged |
| `api.ReviewerFilterControllerTest` | 23 | unchanged |
| `api.ReviewerFilterHistoryTest` | 10 | new |
| `api.ReviewerIdsTest` | 9 | unchanged |
| `api.ReviewerLimitHttpTest` | 3 | unchanged |
| `api.SavedFilterBodyTest` | 15 | unchanged |
| `api.TenantFilterTest` | 3 | unchanged |
| `api.TenantsControllerTest` | 3 | unchanged |
| `store.RequestStoreTest` | 3 | unchanged |
| `store.ReviewerFilterStoreTest` | 15 | changed (6 → 15) |
| `store.TenantDirectoryTest` | 3 | unchanged |

- **Baseline (Code Generation Step 2, before any change, at `2dbc68b`):** 97 tests, all passing. All 97 still pass; the 6 existing `ReviewerFilterStoreTest` tests changed only in how they build the store.
- **`.`/`..`** (printed by `DotReviewerIdTest`): `PUT` and `GET` on `/reviewers/./filter` and `/reviewers/../filter` answer `400` with the fixed `invalid-reviewer-id` body, no id echo. The new history test asserts the same for `/filter/history`.

## Failure Details

None.

## Coverage

**NOT MEASURED.** No coverage tool is configured in `priorauth-api`, and F1220 adds none (team Testing Posture, the recorded exception owned by Meena Iyer). The express scope carries no coverage floor of its own; the feature's 80% target is the parent intent's to report as NOT MEASURED. Nothing here claims it is met.

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| TC-STRATEGY-1 | `code-generation-plan.md` `## Testing Contract`, `obligations.strategy_volume[0]` | One verifiable test per requirement | Every FR and NFR in `requirements.md` that needs code has a passing test tagged with its ID; NFR6 needed no code | `cross-unit-traceability.md`; `@Test` tag comments | Build and Test | Met |
| TC-STRATEGY-2 | same, `strategy_volume[1]` | At least one happy-path unit test per component | Store (`ReviewerFilterStoreTest` AC1.4.1), endpoint and response record (`ReviewerFilterHistoryTest` AC1.4.1), clock bean (exercised by every Spring test) | surefire reports | Build and Test | Met |
| TC-SCOPE-1 | same, `obligations.scope_floor[0]` | Existing suite stays green | All 97 baseline tests pass | verify exit 0; surefire reports | Build and Test | Met |
| TP-VERIFY | `team.md` Testing Posture | Tests run only through the verify script | Every run went through `scripts\verify.cmd priorauth-api` | Commands Run; `code-generation/code-summary.md` | Build and Test | Met |
| TP-BASELINE | `team.md` Testing Posture | Baseline recorded before the first code change | 97 of 97 passing at `2dbc68b` | `code-generation/code-summary.md` | Build and Test | Met |
| TP-FILES | `team.md` Testing Posture; NFR11 | Every new or changed test file covers the happy path and at least two error or edge cases | `ReviewerFilterStoreTest` 15, `ReviewerFilterHistoryTest` 10, `DotReviewerIdTest` 4, `NewEndpointProtocolErrorTest` 6, each with happy and error/edge cases | table above | Build and Test | Met |
| TP-TAGS | `team.md` Testing Posture | Tests carry the FR/AC they prove | Every new `@Test` carries an AC, FR or NFR tag | `@Test` comments in `priorauth-api/src/test/java` | Build and Test | Met |
| TP-INDEPENDENT | `team.md` Testing Posture Q7 B; NFR9 | Tests don't share saved filters or history | `ReviewerFilterHistoryTest` has its own context; new shared-context tests use their own ids; store tests use a fresh store | test sources | Build and Test | Met |
| TP-CLOCK | `team.md` Testing Posture Q7 C; NFR9 | Times a test checks come from a clock the test controls | Every asserted `at` comes from `MutableClock` | `ReviewerFilterStoreTest`, `ReviewerFilterHistoryTest` | Build and Test | Met |
| NFR7-BOUND | `requirements.md` NFR7 | History never exceeds the configured limit, keeping the newest | Limit 3: five saves keep exactly the 3 newest (store and HTTP) | `ReviewerFilterStoreTest`, `ReviewerFilterHistoryTest` AC1.4.6 | Build and Test | Met |
| NFR2-ATOMIC | `requirements.md` NFR2 | A save and its line together under concurrency | 50 concurrent saves: 50 lines, saved filter equals newest line | `ReviewerFilterStoreTest` AC1.4.7 | Build and Test | Met |
