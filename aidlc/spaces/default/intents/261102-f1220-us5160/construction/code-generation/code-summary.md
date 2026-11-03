# Code Summary — F1220 US5160 Save and read my last filter (U1 `us5160-save-filter`)

Repo `priorauth-api` only, branch `f1220/us5160-save-filter`, cut from `origin/feature/F1220` at `df871d9`. Committed as `cb1aee7` ("US5160 save and read my last filter (intent f1220-us5160)"). The change Kiran Rao asked for at the gate (plan Step 12) is a second commit, `4b63a4e` ("US5160 no default error body for 405 and 406 on the new endpoints (intent f1220-us5160)"). Not pushed, and no PR opened. No new dependency; `pom.xml` unchanged. Paths below are relative to `priorauth-api/`.

## Files Created and Modified

**Created, main code (13)**

| File | Purpose |
|---|---|
| `src/main/java/com/acmehealth/priorauth/model/SavedFilter.java` | The saved filter record (FR1.2) |
| `src/main/java/com/acmehealth/priorauth/store/ReviewerFilterStore.java` | In-memory store, one lock, reviewer limit (FR1, FR2, NFR1, NFR7; C6) |
| `src/main/java/com/acmehealth/priorauth/store/TenantDirectory.java` | Known tenants from the export (FR3.1; ADR-002) |
| `src/main/java/com/acmehealth/priorauth/api/ErrorCode.java` | The four contract codes, status and fixed message (NFR4) |
| `src/main/java/com/acmehealth/priorauth/api/FilterRequestException.java` | Refusal carrying only an `ErrorCode` |
| `src/main/java/com/acmehealth/priorauth/api/ReviewerIds.java` | Reviewer-id rule (FR1.3, FR2.3) |
| `src/main/java/com/acmehealth/priorauth/api/SavedFilterBody.java` | Save-body rules in the contract's check order (FR1.2, FR1.6, NFR3) |
| `src/main/java/com/acmehealth/priorauth/api/ErrorResponse.java` | `{error, message}` body |
| `src/main/java/com/acmehealth/priorauth/api/SavedFilterResponse.java` | GET response record |
| `src/main/java/com/acmehealth/priorauth/api/ReviewerFilterController.java` | PUT/GET `/reviewers/{reviewerId}/filter` (C1) |
| `src/main/java/com/acmehealth/priorauth/api/TenantsController.java` | GET `/tenants` (C2) |
| `src/main/java/com/acmehealth/priorauth/api/NewEndpointErrorHandler.java` | Scoped error handler (ADR-003) |
| `src/main/java/com/acmehealth/priorauth/api/BrowserAccessPolicy.java` | Named-origin CORS (C5, FR8; ADR-006) |

**Created, tests (11 classes plus 15 contract examples)**

- `src/test/java/com/acmehealth/priorauth/store/ReviewerFilterStoreTest.java`, `TenantDirectoryTest.java`
- `src/test/java/com/acmehealth/priorauth/api/ReviewerIdsTest.java`, `SavedFilterBodyTest.java`, `ContractExamples.java` (helper), `ReviewerFilterControllerTest.java`, `ReviewerFilterContractTest.java`, `TenantsControllerTest.java`, `BrowserAccessPolicyTest.java`, `ReviewerLimitHttpTest.java`, `DotReviewerIdTest.java`
- `src/test/resources/contract/f1220/`: the 15 files the plan names, byte-identical to the parent's `inception/contract-design/examples/` (checked with `Get-FileHash`).

**Modified**

- `src/main/resources/data/requests.sample.json`: new last row `PA-10270`, `NM-02`, `PENDED`, `2026-10-12` (FR3.2).
- `src/main/resources/application.yml`: `priorauth.cors.allowed-origins` and `priorauth.reviewer-filter.max-reviewers`, each with a one-line comment.
- `README.md`: four lines on the new endpoints, the two keys and the in-memory store, plus `Changed by AI-DLC intent f1220-us5160`.
- Existing test files changed (FR3.2, AC1.1.13):
  - `src/test/java/com/acmehealth/priorauth/store/RequestStoreTest.java`: size 5, `get(4)` is `PA-10270`, pending has 4 ids, new `allKeepsDecidedRequests`.
  - `src/test/java/com/acmehealth/priorauth/api/PendingRequestsControllerTest.java`: `listsPendingRequestsOldestFirst` expects 4 rows.
  - `src/test/java/com/acmehealth/priorauth/api/TenantFilterTest.java`: NM-02 returns 1 row (`PA-10270`); new `unknownTenantStillAnswersAnEmptyList` and `tenantMatchIsCaseSensitive`.
- `OverLimitFilterTest` is not changed and passes.

**Created in Step 12 (commit `4b63a4e`, 2 files, no other file changed)**

| File | Purpose |
|---|---|
| `src/main/java/com/acmehealth/priorauth/api/NewEndpointProtocolErrorHandler.java` | 405 and 406 on `/reviewers/**` and `/tenants` answer with no body (NFR4, AC1.1.10) |
| `src/test/java/com/acmehealth/priorauth/api/NewEndpointProtocolErrorTest.java` | Real-server tests: 405 and 406 with no body on the new endpoints, the queue's default error body unchanged, preflights unchanged |

## Key Implementation Decisions

- **One lock (OQ-U1.1).** `ReviewerFilterStore` keeps a plain `HashMap` and runs every `save` and `read` in `synchronized (lock)` on one `private final Object`. US5163 adds its history line inside the same block. The limit check (`!containsKey && size >= max`) is in the same block, so a kept reviewer always saves and a read never adds an entry.
- **Memory ceiling at the default limit (OQ-U1.1)**, as the plan states: at most 10,000 entries of about 274 bytes each, under 3 MB.
- **Check order (FR1.6).** The controller takes the raw `InputStream` and the `Content-Type` header, so Spring never answers first. Order: reviewer id, then content type, then size (`readNBytes(1025)`), then readable JSON with exact shape, then known tenant, then the reviewer limit.
- **Shape is checked by hand on a `JsonNode`.** The object must have exactly 2 properties, `tenant` and `overLimit`. `tenant` must be a JSON string or `null`, and `overLimit` must be a JSON boolean. The reader turns on `FAIL_ON_TRAILING_TOKENS`. An empty body, unreadable JSON, a JSON array or trailing content answers `invalid-body`.
- **No caller value in an error.** `JacksonException` and `InvalidMediaTypeException` are caught and replaced, because their messages can quote input. `FilterRequestException`'s message is the code only. The handler writes the fixed `{error, message}` body as `application/json`. It is scoped to `ReviewerFilterController` and `TenantsController`.
- **CORS.** Registered for `/reviewers/**`, `/tenants` and `/requests/pending`. It allows `GET` and `PUT`, the `Content-Type` header, and no credentials. The origins are the trimmed comma-separated `priorauth.cors.allowed-origins`. Start-up throws `IllegalStateException` for an empty entry, `null` (any case) or any entry containing `*`.
- **405 and 406 on the new endpoints (Step 12): a global, path-checked `@RestControllerAdvice`.**
  - `NewEndpointProtocolErrorHandler` handles `HttpRequestMethodNotSupportedException` (405) and `HttpMediaTypeNotAcceptableException` (406).
  - For `/reviewers/**` and `/tenants` it answers the exception's own status and headers (the `Allow` header on a 405) with no body. So no `path`, `trace`, reviewer id or caller input is returned, and the contract's four error codes stay unchanged.
  - For any other path it rethrows the same exception. Spring treats a rethrown original exception as "not handled" and passes it to `DefaultHandlerExceptionResolver`, which logs no warning for it. So `GET /requests/pending` and every other path keep Spring Boot's default error handling (C4, AC1.1.13).
  - The path is matched with `PathPattern` against the same parsed request path Spring MVC routes by, so the decision agrees with the controllers' mappings.
  - **Why this mechanism:** the scoped `NewEndpointErrorHandler` (`assignableTypes`) cannot see a 405, because Spring raises it before a controller is chosen. A global advice with a path check is one small class with no new dependency and no response wrapping. A servlet filter would have had to intercept `sendError` and wrap the response, which is more code and touches every request. `NewEndpointErrorHandler` itself is not changed.
- **Package-private request rules.** `ErrorCode`, `FilterRequestException`, `ReviewerIds` and `SavedFilterBody` are package-private in `api`. Controllers, records and the handler are public, as the existing controller is.

## Test Summary

### Baseline (Step 2, before any code change)

- Branch `f1220/us5160-save-filter` at `df871d9` (equal to `origin/feature/F1220` and `main`).
- Command: `scripts\verify.cmd priorauth-api` from the workspace root. Exit code `0`.
- Surefire (`priorauth-api/target/surefire-reports/*.txt`): 12 tests, 0 failures, 0 errors, 0 skipped.

| Class | Tests | Failures |
|---|---|---|
| `aging.AgeBadgeTest` | 1 | 0 |
| `aging.BusinessDaysTest` | 4 | 0 |
| `api.OverLimitFilterTest` | 1 | 0 |
| `api.PendingRequestsControllerTest` | 3 | 0 |
| `api.TenantFilterTest` | 1 | 0 |
| `store.RequestStoreTest` | 2 | 0 |

### Per-layer runs (test-after, layer by layer)

| After step | Command | Exit | Tests |
|---|---|---|---|
| 5 (data access) | `scripts\verify.cmd priorauth-api` | 0 | 24, 0 failures |
| 7 (request rules) | `scripts\verify.cmd priorauth-api` | 0 | 48, 0 failures |
| 9 (API), first run | `scripts\verify.cmd priorauth-api` | 1 | 92, 2 failures in `DotReviewerIdTest` (expected 404, got 400; see below) |
| 9 (API), after the deviation below | `scripts\verify.cmd priorauth-api` | 0 | 92, 0 failures |
| 11 (finished first commit `cb1aee7`) | `scripts\verify.cmd priorauth-api` | 0 | 92, 0 failures |
| 12 (requested change, commit `4b63a4e`) | `scripts\verify.cmd priorauth-api` | 0 | 97, 0 failures |

### Final verify output (after Step 12, finished branch at `4b63a4e`)

```
verify: priorauth-api: mvn -q test
EXIT=0
TOTAL tests=97 failures=0 errors=0 skipped=0   (sum of target/surefire-reports/*.txt)
```

In the run's log, `DefaultHandlerExceptionResolver` resolved only the queue's `DELETE /requests/pending` (405). The new endpoints' 405s were answered by `NewEndpointProtocolErrorHandler`.

| Class | Tests | Failures |
|---|---|---|
| `aging.AgeBadgeTest` | 1 | 0 |
| `aging.BusinessDaysTest` | 4 | 0 |
| `api.BrowserAccessPolicyTest` (new) | 5 | 0 |
| `api.DotReviewerIdTest` (new) | 3 | 0 |
| `api.NewEndpointProtocolErrorTest` (new, Step 12) | 5 | 0 |
| `api.OverLimitFilterTest` (unchanged) | 1 | 0 |
| `api.PendingRequestsControllerTest` (changed) | 3 | 0 |
| `api.ReviewerFilterContractTest` (new) | 7 | 0 |
| `api.ReviewerFilterControllerTest` (new) | 23 | 0 |
| `api.ReviewerIdsTest` (new) | 9 | 0 |
| `api.ReviewerLimitHttpTest` (new) | 3 | 0 |
| `api.SavedFilterBodyTest` (new) | 15 | 0 |
| `api.TenantFilterTest` (changed) | 3 | 0 |
| `api.TenantsControllerTest` (new) | 3 | 0 |
| `store.RequestStoreTest` (changed) | 3 | 0 |
| `store.ReviewerFilterStoreTest` (new) | 6 | 0 |
| `store.TenantDirectoryTest` (new) | 3 | 0 |

Parameterized cases count once per invocation. Coverage: NOT MEASURED in F1220, under the team's recorded exception owned by Meena Iyer. No coverage tool was added.

## The 404 Body for . and ..

**There is no 404.** On Spring Boot 4.1.1 with embedded Tomcat, a real request to `/reviewers/./filter` or `/reviewers/../filter`, sent literally by `java.net.http.HttpClient`, reaches `ReviewerFilterController` with `reviewerId` `.` or `..`. Spring MVC matches on the raw request URI, which Tomcat does not normalise. The reviewer-id rule then refuses it. `DotReviewerIdTest` printed the real answers verbatim:

```
OQ-U1.2 PUT /reviewers/./filter -> 400 application/json {"error":"invalid-reviewer-id","message":"Reviewer id must be 1-64 letters, digits, '.', '-' or '_' and contain a letter or digit."}
OQ-U1.2 GET /reviewers/./filter -> 400 application/json {"error":"invalid-reviewer-id","message":"Reviewer id must be 1-64 letters, digits, '.', '-' or '_' and contain a letter or digit."}
OQ-U1.2 PUT /reviewers/../filter -> 400 application/json {"error":"invalid-reviewer-id","message":"Reviewer id must be 1-64 letters, digits, '.', '-' or '_' and contain a letter or digit."}
OQ-U1.2 GET /reviewers/../filter -> 400 application/json {"error":"invalid-reviewer-id","message":"Reviewer id must be 1-64 letters, digits, '.', '-' or '_' and contain a letter or digit."}
```

- **Does it echo the id?** No. The body is the contract's fixed `invalid-reviewer-id` body. It has no `path`, no trace and no caller value.
- **Is anything saved?** No. The store reads `.` and `..` as empty after the calls.
- **Does it match the contract?** No. The contract (Rules, reviewer id, "Deliberate exception"; C1 `404` responses; AC1.1.7; FR1.3) says these ids answer `404` with the server's default body, because the server reroutes them. That premise does not hold on this stack. The real answer is the general rule's `400 invalid-reviewer-id`.
- **Action for Kiran Rao:** before the PR, raise this with Meena Iyer as a contract change: drop the `.`/`..` 404 exception, because they follow the 400 rule. This is a changed status code, so it is a breaking change under the contract's ownership rules. Consumers are not affected in practice, since the screen treats any non-2xx as a failure. The code does not work around it.

## Deviations from the Plan

1. **`DotReviewerIdTest` asserts the observed 400, not 404.** The plan's tests `singleDotIdAnswers404OnPutAndGet` and `doubleDotIdAnswers404OnPutAndGet` failed (expected 404, got 400). They are renamed `singleDotIdIsRefusedOnPutAndGet` and `doubleDotIdIsRefusedOnPutAndGet`. They now assert `400` with the exact `error-invalid-reviewer-id.json` body. `nothingIsSavedForDotIds` is kept as planned: nothing is saved, and the answer does not carry `/./` or `/../`. Production code is unchanged. Forcing a 404 would have meant inventing the server rerouting the contract assumed, so the plan's rule "this plan does not work around it" applies. This needs the contract owner's decision (see the section above).
2. **The origin check refuses any entry that contains `*`**, not only an entry equal to `*`. It also refuses `null` in any case. This is a little stricter than Decision 10 and keeps its intent: never `*`.
3. **Extra test cases beyond the plan's lists**, none of which loosen anything:
   - `ReviewerIdsTest`: a newline-terminated id and `null`.
   - `SavedFilterBodyTest`: a JSON array body and an empty content-type string.
   - `BrowserAccessPolicyTest`: a valid two-origin list.
   - `ReviewerFilterContractTest`: the error-example equality is checked inside each case test (5 cases plus 2 example tests, 7 in all), rather than as a separate test.
4. **The preflight's `Access-Control-Allow-Methods` is `GET,PUT`**, as `case-preflight.json` expects. The contract's C5 YAML lists `OPTIONS` too. Spring answers preflight `OPTIONS` itself, so `OPTIONS` is not in the allowed-methods setting, and the example is what the test checks.
5. **Step 12 has 5 real-server tests, not 4.** The extra test, `preflightsAreUnchanged`, checks three things on a real server:
   - A preflight from the named origin to `/reviewers/{id}/filter` still answers `200` with that origin.
   - A preflight from the named origin asking for `DELETE` still answers `403` with no `Access-Control-Allow-Origin`.
   - A preflight from `http://evil.example` still answers `403` with no `Access-Control-Allow-Origin`.

   This was added because the brief asked to check that preflights are unaffected. Spring answers preflights before any exception is raised, so the new handler never sees them. No planned test was dropped or loosened.
6. **The 405 tests assert that `Allow` contains the supported methods** (`GET` and `PUT` for the filter, `GET` for `/tenants`) instead of an exact header value, because Spring may also list `HEAD` and `OPTIONS`.

## Gate Decisions (Code Generation approval, 2026-11-03)

Approved by Kiran Rao after the mob's code review with Meena Iyer and Arjun Nair.

- **`.` and `..` answer 400 `invalid-reviewer-id`.** Meena Iyer accepts this as a contract change and updates the parent's contract (`261102-f1220-remember-filter`, Contract Design). The code and `DotReviewerIdTest` stay as they are. The risk below is settled by this decision.
- **The 404 echo on unknown sub-paths under `/reviewers/` is accepted for F1220.** It goes to the backlog and is not fixed in this story.

## Skipped, Not Checked, and Risks

- **Contract mismatch for `.`/`..`** (above). The PR should not merge into `feature/F1220` until Meena Iyer settles it. If she keeps the 404, a small controller change is needed and `DotReviewerIdTest` changes with it.
- **Unmapped paths under `/reviewers/` still get Spring Boot's default 404 body.** A path such as `/reviewers/rita.k/other` matches no controller, so Spring Boot answers `404` with its default body, whose `path` field holds the id. Step 12 covered only 405 and 406 on the new endpoints, so this is not changed and not tested. It is mentioned per NFR4, for Kiran Rao to decide on.
- **406 may already have had no body before Step 12.** For an `Accept: text/plain` request, Spring Boot's own error controller may itself answer 406 with no body. The 406 tests prove the behaviour now; whether the change was needed for 406 was not checked by reverting.
- **Duplicate JSON keys** (`{"tenant": "TX-01", "tenant": null, "overLimit": true}`) are accepted, and the last value wins. Duplicate detection was not in the plan and is not turned on.
- **Body charset.** A `charset` parameter is accepted, but the bytes are always decoded by Jackson's own detection (UTF-8/16/32). A `charset=ISO-8859-1` body with non-ASCII bytes would be read as UTF-8. No tenant id contains non-ASCII, so this cannot make an unknown tenant pass.
- **One lock serialises all saves and reads** (ADR-001, accepted). Not load-tested.
- **Not checked:** concurrent saves (US5163 owns AC1.4.7), a real browser against `priorauth-web` (US5161), and `priorauth-web` itself (not run; not touched).
- **Coverage is NOT MEASURED** (team exception), so the 80% target is not claimed.
- **Line endings.** The repo has `core.autocrlf` behaviour: new files were written with LF and git warns it will convert them to CRLF. The diff of the changed files is clean (42 insertions, 9 deletions across 6 files).
