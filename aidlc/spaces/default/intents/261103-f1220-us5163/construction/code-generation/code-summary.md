# Code Summary — F1220 US5163 Filter history (U4 `us5163-filter-history`)

## Result

- **Repo and branch:** `priorauth-api`, `f1220/us5163-filter-history`, cut from `origin/feature/F1220` at `2dbc68b`. The branch contains US5160 (`cb1aee7`, `4b63a4e`).
- **Commit:** `3cf2206` (`US5163 audit every filter change: history line per save and GET .../filter/history (intent f1220-us5163)`), 14 files. Not pushed, and no PR opened.
- **Verify:** every run went through `scripts\verify.cmd priorauth-api`.

| Run | Exit | Tests | Test classes |
|---|---|---|---|
| Baseline (plan Step 2, before any change) | 0 | 97 passing | 17 |
| Final (plan Step 11) | 0 | 118 passing, 0 failing | 18 |

The team's practices file still says "`priorauth-api` has 12 tests". That figure predates F1220; the recorded baseline for this story is 97.

## Files

| File | Change |
|---|---|
| `priorauth-api/src/main/java/com/acmehealth/priorauth/model/HistoryLine.java` | new: domain record `(Instant at, String reviewer, String tenant, boolean overLimit)` |
| `priorauth-api/src/main/java/com/acmehealth/priorauth/store/ReviewerFilterStore.java` | changed: history deque per reviewer, written inside the existing lock, `history(id)`, history limit, `Clock` |
| `priorauth-api/src/main/java/com/acmehealth/priorauth/PriorAuthApiApplication.java` | changed: `@Bean Clock clock()` = `Clock.systemUTC()` |
| `priorauth-api/src/main/resources/application.yml` | changed: `priorauth.reviewer-filter.max-history-lines: 1000` |
| `priorauth-api/src/main/java/com/acmehealth/priorauth/api/HistoryLineResponse.java` | new: C3 response record with `from(HistoryLine)` |
| `priorauth-api/src/main/java/com/acmehealth/priorauth/api/ReviewerFilterController.java` | changed: `GET /reviewers/{reviewerId}/filter/history` |
| `priorauth-api/README.md` | changed: history call, setting, intent line |
| `priorauth-api/src/test/java/com/acmehealth/priorauth/MutableClock.java` | new: test-only UTC clock |
| `priorauth-api/src/test/java/com/acmehealth/priorauth/store/ReviewerFilterStoreTest.java` | changed: 6 → 15 tests |
| `priorauth-api/src/test/java/com/acmehealth/priorauth/api/ReviewerFilterHistoryTest.java` | new: 10 tests, own context |
| `priorauth-api/src/test/java/com/acmehealth/priorauth/api/DotReviewerIdTest.java` | changed: 3 → 4 tests; Javadoc updated for the contract change |
| `priorauth-api/src/test/java/com/acmehealth/priorauth/api/NewEndpointProtocolErrorTest.java` | changed: 5 → 6 tests |
| `priorauth-api/src/test/resources/contract/f1220/c3-get-history.json`, `c3-get-history-empty.json` | new: copied unchanged from the parent's examples (SHA-256 matches) |

`pom.xml`, `NewEndpointErrorHandler`, `NewEndpointProtocolErrorHandler`, `BrowserAccessPolicy` and `ReviewerIds` are unchanged. No dependency was added.

## Key Implementation Decisions

- **Same lock as the save (NFR2, C6).** The history line is appended inside the store's existing `synchronized (lock)` block, right after `filters.put`. A save refused for the reviewer limit returns before both, so it writes no line. Saves refused for an invalid id, body or tenant never reach the store.
- **Newest first and the limit (FR7.3, FR7.5).** Each reviewer has an `ArrayDeque`: a new line goes in with `addFirst`, and `removeLast` drops the oldest line once the limit is passed. Same-second saves therefore stay in save order, newest first.
- **Reads create nothing (FR7.4).** `history(id)` uses `get` and returns a copy, or `List.of()`. The deque is created only on a successful save, so a read takes no reviewer slot.
- **Time (FR7.1, NFR9).** The time is `clock.instant().truncatedTo(SECONDS)`, which cuts and does not round, and the API writes it as `Instant.toString()`, for example `2027-01-12T09:15:30Z`. In production the clock is the bean `clock` (`Clock.systemUTC()`). `ReviewerFilterHistoryTest` adds a differently named `@Primary` `MutableClock` bean, because Spring Boot refuses a second bean with the same name.
- **Limits.** Both limits refuse a value below 1, with a message that names the setting and the value.
- **Endpoint (C3).** It checks the id with `ReviewerIds.requireValid` and maps the lines to `List<HistoryLineResponse>`; the domain record is never returned. The existing error handlers cover the new path unchanged, and tests confirm 400 with the fixed body (including `.`/`..`) and 405 and 406 with no body.

## Test Coverage

- **Store** (`ReviewerFilterStoreTest`, 9 new tests):
  - AC1.4.1: exact line, time cut to the second
  - AC1.4.2: a repeat and a clear count
  - AC1.4.3: a reviewer-limit refusal writes no line
  - AC1.4.4: newest first, and same-second lines keep save order
  - AC1.4.5: empty, and takes no slot
  - AC1.4.6: limit 3
  - AC1.4.7: 50 concurrent saves give 50 lines, and the saved filter equals the newest line
  - a history limit below 1 is refused
  - ids are case-sensitive
- **HTTP** (`ReviewerFilterHistoryTest`, 10 tests, own context with history limit 3 and a test clock):
  - AC1.4.1, AC1.4.2, AC1.4.4, AC1.4.6
  - AC1.4.3: invalid body, unknown tenant and invalid id leave the history unchanged
  - AC1.4.5: `[]`, and 400 for three malformed ids
  - AC1.4.8: fixed error body that does not echo the id
  - AC1.4.9: the URL
  - the C3 examples, `c3-get-history.json` and `c3-get-history-empty.json`
- **Real server** (2 tests):
  - `.` and `..` on the history call answer 400, and the store holds no history for them (A5)
  - 405 (with `Allow` containing `GET`) and 406 on the history path have no body (A2, NFR4)
- **Coverage:** line coverage is NOT MEASURED in F1220, under the team's recorded exception owned by Meena Iyer.

## Deviations from the Plan

- There are 21 new tests where the plan said "about 25": 9 store, 10 HTTP (plan: about 11) and 2 real-server (plan: 3, because the 405 and 406 checks share one test). Every acceptance criterion and check the plan lists has a test.
- The store test helper gained a two-argument form, `store(maxReviewers, maxHistoryLines)`, for the limit tests. The 6 existing tests' assertions are unchanged.
- Some new tests assert a little more than the plan lists:
  - AC1.4.5 also checks that no saved filter was created.
  - DotReviewerIdTest also checks that no history exists for `.` and `..`.
  - The 405 test also checks the `Allow` header.
- `MutableClock.withZone` throws `UnsupportedOperationException`, because it is UTC only.

## Skipped, Not Checked, and Risks

- **Memory:** about 640 MB of history in the worst case at the default limits (10,000 reviewers × 1,000 lines). This is not measured and has no cap beyond the line limits (plan Decision 7, Risks).
- **Concurrency** is proven at the store level only (50 threads). There is no HTTP concurrency or load test.
- **Line endings:** Git warned that LF becomes CRLF in the working copy (autocrlf). The stored line endings were not compared with the existing files.
- **Push:** the branch's upstream is `origin/feature/F1220`, because it was created from it. Push with `git push -u origin f1220/us5163-filter-history`, not a bare `git push`.
- **Not fixed, outside the plan:**
  - The README line "Saved filters live in memory only" does not say that the history is also lost on restart. Meena Iyer's release-notes line covers it for users.
  - A Mockito "self-attaching" JDK warning appears in test runs. It predates this story.
- **Not run:** the `priorauth-web` tests. This story doesn't change that repo.
- **Before the PR (Arjun Nair):** run `git fetch`, rebase onto `origin/feature/F1220`, run `scripts\verify.cmd priorauth-api`, then push and open the PR into `feature/F1220`.
