# Test Results — F1220 US5160 (`priorauth-api`)

## Build Status

**Success.** `scripts\verify.cmd priorauth-api` exited 0 on 2026-11-03.

- Code: `priorauth-api` branch `f1220/us5160-save-filter` at `4b63a4e` (two commits on `origin/feature/F1220`: `cb1aee7`, `4b63a4e`); working tree clean.
- The branch is 0 commits behind `origin/feature/F1220` after a fresh `git fetch`, so no rebase was needed for this run.
- The command compiles main and test code and runs the whole suite (`mvn -q test`), about 14 seconds.

## Commands Run

| Source | Command | Runs | Result |
|---|---|---|---|
| `construction/code-generation/unit-test-instructions.md` (the only test command; Minimal strategy generates no other instruction files) | `scripts\verify.cmd priorauth-api` | once | exit 0 |

## Test Results

**97 tests: 97 passed, 0 failed, 0 errors, 0 skipped.** From `priorauth-api/target/surefire-reports/*.txt`:

| Test class | Tests | New / changed / existing |
|---|---|---|
| `aging.AgeBadgeTest` | 1 | existing |
| `aging.BusinessDaysTest` | 4 | existing |
| `api.BrowserAccessPolicyTest` | 5 | new |
| `api.DotReviewerIdTest` | 3 | new |
| `api.NewEndpointProtocolErrorTest` | 5 | new (Code Generation Step 12) |
| `api.OverLimitFilterTest` | 1 | existing, unchanged |
| `api.PendingRequestsControllerTest` | 3 | changed (row count 3 → 4) |
| `api.ReviewerFilterContractTest` | 7 | new |
| `api.ReviewerFilterControllerTest` | 23 | new |
| `api.ReviewerIdsTest` | 9 | new |
| `api.ReviewerLimitHttpTest` | 3 | new |
| `api.SavedFilterBodyTest` | 15 | new |
| `api.TenantFilterTest` | 3 | changed (NM-02 count, 2 edge tests added) |
| `api.TenantsControllerTest` | 3 | new |
| `store.RequestStoreTest` | 3 | changed (5 rows, 1 edge test added) |
| `store.ReviewerFilterStoreTest` | 6 | new |
| `store.TenantDirectoryTest` | 3 | new |

- **Baseline (before any change, at `df871d9`):** 12 tests, all passing (recorded in `code-generation/code-summary.md`). All 12 still exist; the 3 changed files were updated only for the new NM-02 row, as the approved plan named.
- **Observed `.`/`..` answer** (printed by `DotReviewerIdTest`): `PUT` and `GET` `/reviewers/./filter` and `/reviewers/../filter` answer `400 application/json {"error":"invalid-reviewer-id","message":"Reviewer id must be 1-64 letters, digits, '.', '-' or '_' and contain a letter or digit."}`. No id echo. Accepted at the Code Generation gate as a contract change by Meena Iyer.

## Failure Details

None.

## Coverage

**NOT MEASURED.** No coverage tool is configured in `priorauth-api`, and F1220 adds none (team Testing Posture, the recorded exception owned by Meena Iyer). This story's express scope carries no coverage floor of its own. The feature's 80% target is the parent intent's to report, at its Build and Test, as NOT MEASURED. Nothing here claims it is met.

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| TC-STRATEGY-1 | `code-generation-plan.md` `## Testing Contract`, `obligations.strategy_volume[0]` | One verifiable test per requirement | Every FR, NFR and AC of `requirements.md` has at least one test tagged with its ID | `cross-unit-traceability.md`; `@Test` tag comments in `priorauth-api/src/test/java` | Build and Test | Met |
| TC-STRATEGY-2 | same, `strategy_volume[1]` | At least one happy-path unit test per component | Each of the 14 new main classes is exercised by a passing happy-path test (store, directory, body parser, id rules, both controllers, error handlers, CORS policy) | `ReviewerFilterStoreTest`, `TenantDirectoryTest`, `SavedFilterBodyTest`, `ReviewerIdsTest`, `ReviewerFilterControllerTest`, `TenantsControllerTest`, `BrowserAccessPolicyTest`, `NewEndpointProtocolErrorTest` | Build and Test | Met |
| TC-SCOPE-1 | same, `obligations.scope_floor[0]` | Existing test suite stays green | All 12 baseline tests pass; `OverLimitFilterTest` unchanged and passing | verify exit 0; surefire reports | Build and Test | Met |
| TP-VERIFY | `team.md` Testing Posture | Tests run only through the verify script | Every run went through `scripts\verify.cmd priorauth-api` | this file, Commands Run | Build and Test | Met |
| TP-BASELINE | `team.md` Testing Posture; NFR8 | API baseline recorded before the first code change | 12 of 12 passing at `df871d9` | `code-generation/code-summary.md`, Test Summary | Build and Test | Met |
| TP-FILES | `team.md` Testing Posture; NFR11 | Every new or changed test file covers the happy path and at least two error or edge cases | All 15 new or changed test files have 3 or more tests with happy and error/edge cases | table above | Build and Test | Met |
| TP-TAGS | `team.md` Testing Posture | Tests carry the FR/US they prove | Every `@Test` / `@ParameterizedTest` in the new and changed files has an FR, AC, US or contract tag | `@Test` comments in `priorauth-api/src/test/java` | Build and Test | Met |
| TP-INDEPENDENT | `team.md` Testing Posture; NFR9 | API tests don't share saved filters | Shared-context tests use their own `rfc-*` ids; only `ReviewerFilterContractTest` uses the contract files' ids; limit tests use fresh stores or their own context | test sources; `code-generation/code-summary.md` | Build and Test | Met |
