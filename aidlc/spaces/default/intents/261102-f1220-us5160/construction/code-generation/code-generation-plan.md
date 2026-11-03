# Code Generation Plan — F1220 US5160 Save and read my last filter (U1 `us5160-save-filter`)

## Summary

- Builds: PUT/GET `/reviewers/{reviewerId}/filter`, GET `/tenants`, named-origin browser access, and the NM-02 sample request, in `priorauth-api` only
- Touches: new `model/SavedFilter`, `store/ReviewerFilterStore`, `store/TenantDirectory`, and 9 `api/` classes; changes `requests.sample.json`, `application.yml`, `README.md` and 3 existing test files
- Tests: about 50 JUnit 5 / MockMvc tests in 10 new test classes plus 3 changed ones, including the contract examples for C1, C2 and C5; run only through `scripts\verify.cmd priorauth-api`
- Change requested at the gate (Step 12): 405 and 406 on `/reviewers/**` and `/tenants` answer with no body, so no default error body echoes the reviewer id; 4 real-server tests in one new class; the queue's errors are unchanged

## Scope and Inputs

- **Story:** US1.1 (Rally US5160), AC1.1.1-AC1.1.13. Requirements: `inception/requirements-analysis/requirements.md` of this intent (FR1-FR3, FR8, NFR1, NFR3, NFR4, NFR6-NFR9, NFR11).
- **Contract (wins over the story's provisional wording):** parent `inception/contract-design/contract-summary.md`, C1, C2, C4, C5 and C6, plus `examples/`.
- **Design decisions:** parent ADR-001 (one store, one lock), ADR-002 (tenant directory), ADR-003 (new controllers with a scoped error handler) and ADR-006 (named origins).
- **Repo and branch:** `priorauth-api` only. Branch `f1220/us5160-save-filter`, cut from `origin/feature/F1220` (today at `df871d9`, the same commit as `main`). The PR goes into `feature/F1220`.
- **No new dependency.** Everything uses what `spring-boot-starter-webmvc` and `spring-boot-starter-webmvc-test` already bring: Spring MVC CORS, Jackson 3 `JsonNode`, JUnit 5 with `@ParameterizedTest`, AssertJ, MockMvc, and the JDK `java.net.http.HttpClient`. `pom.xml` is not changed.
- **Not in this story:** history, the clock and `GET .../filter/history` (US5163); the screen (US5161, US5162).

## Design Decisions This Plan Settles

These are the two points the parent's contract left to this story's code plan (OQ-U1.1, OQ-U1.2), plus how its rules land in code.

1. **One lock in the store (OQ-U1.1, ADR-001, C6).**
   - `ReviewerFilterStore` holds a plain `HashMap<String, SavedFilter>`.
   - Every `save` and `read` runs inside `synchronized (lock)` on one `private final Object lock`.
   - US5163 adds its history line inside that same block, so a save and its line can never come apart.
   - One lock serialises all saves. That is acceptable at the expected volume (ADR-001).
2. **Memory ceiling at the default limit (OQ-U1.1).** At most 10,000 entries. Each entry is a key of at most 64 ASCII characters (about 200 bytes as a Java `String`), a map entry (about 50 bytes) and a two-field `SavedFilter` (about 24 bytes; the tenant string is the directory's own instance). That is under 3 MB in total. The history ceiling is US5163's to state.
3. **Store operations (C6):**
   - `save(reviewerId, SavedFilter) -> SaveResult.SAVED | SaveResult.REVIEWER_LIMIT`
   - `read(reviewerId) -> Optional<SavedFilter>`
   - A read never adds an entry.
   - A save for an id already kept always succeeds, whatever the limit.
   - The store uses no Spring web types.
4. **Check order (contract rules, FR1.6).** The controller runs the checks itself, in this order:
   1. reviewer id
   2. content type and body size
   3. body shape
   4. tenant known
   5. reviewer limit

   It takes the raw request body (`InputStream`) instead of `@RequestBody SavedFilter`, so Spring can never refuse a request early with its own status and body (415, or 400 with `path`). Spring would otherwise do that before the reviewer-id check runs.
5. **The size limit is enforced while reading (NFR3).** The body is read with `readNBytes(1025)`, so at most 1,025 bytes are ever held. More than 1,024 bytes answers `invalid-body`.
6. **The body shape is checked by hand on a `JsonNode` (AC1.1.6).**
   - It must be an object with exactly the field names `tenant` and `overLimit`.
   - `tenant` must be a JSON string or `null`.
   - `overLimit` must be a JSON boolean.

   The check doesn't depend on Jackson's coercion or unknown-property settings, which differ between versions and which Spring Boot loosens. Unreadable JSON, trailing content or an empty body answer `invalid-body`.
7. **Content type (contract rules).** The type is parsed with `MediaType.parseMediaType`, and only `application/json` passes, with any parameters such as `charset=UTF-8`. A missing, unparsable or different type answers `invalid-body`.
8. **Errors (NFR4, ADR-003).**
   - `NewEndpointErrorHandler` is a `@RestControllerAdvice(assignableTypes = {ReviewerFilterController.class, TenantsController.class})`, so `GET /requests/pending` keeps its own errors (AC1.1.13).
   - It maps `FilterRequestException(ErrorCode)` to the code's status and the body `{"error", "message"}`. The message is the contract's fixed text.
   - No caller value is ever put into an exception or a message.
9. **`.` and `..` (OQ-U1.2).**
   - The server normalises these paths before Spring sees them. MockMvc does not normalise, so this is proven against a real server (`webEnvironment = RANDOM_PORT`).
   - The real 404 body is recorded in `code-summary.md` and checked against the no-echo rule.
   - If the body contains the id, Kiran Rao raises a contract change with Meena Iyer before the PR. This plan does not work around it.
10. **Browser access (C5, ADR-006).**
    - `BrowserAccessPolicy` is a `WebMvcConfigurer` that registers CORS for `/reviewers/**`, `/tenants` and `/requests/pending`.
    - It allows the configured origins only, the methods `GET` and `PUT`, the header `Content-Type`, and no credentials.
    - The origins come from `priorauth.cors.allowed-origins`, a comma-separated list with the default `http://localhost:3000`, each trimmed.
    - Start-up fails with `IllegalStateException` if the list contains `*`, `null` or an empty entry, so `*` can never be answered.
11. **NM-02 sample request (FR3.2, AC1.1.13).** The new row is `PA-10270`, tenant `NM-02`, status `PENDED`, received `2026-10-12`.
    - Received on or before 2026-10-13, so no existing `asOf` case turns into a 400.
    - Sorts last, so the existing row positions (`$[0]`, `$[1]`) don't move.
    - Not over the limit on 2026-10-13: 1 business day, since NM-02 has no holiday file. So `OverLimitFilterTest` stays at 1 row and is not changed.
    - Its tenant id is never used to build a file path from a caller's value. `HolidayCalendar` only ever sees tenant ids from the export.
12. **Configuration keys (team code style):**
    - `priorauth.reviewer-filter.max-reviewers`, default `10000` in `@Value`, and also written in `application.yml` with a comment.
    - `priorauth.cors.allowed-origins`, default `http://localhost:3000`, written the same way.

## Security Checklist (for the mob's plan review)

| Checklist item | How this plan meets it |
|---|---|
| Every request value is validated and size-limited | The reviewer id is checked against `^(?=.*[A-Za-z0-9])[A-Za-z0-9._-]{1,64}$` on every PUT and GET. The body is limited to 1,024 bytes while it is read, its exact shape is checked, and the tenant must be in a fixed known set (Decisions 4-7). |
| API data is escaped before it is shown on the page | No page in this repo. The error bodies carry no caller value at all (Decision 8); escaping is US5161's. |
| No file path or cache key is built from a caller's value | Caller ids are only `HashMap` keys in `ReviewerFilterStore`. The tenant is checked against `TenantDirectory` and never passed to `HolidayCalendar` (NFR3). |
| Error responses carry no stack traces and no raw caller input | Fixed `{error, message}` bodies from the scoped handler, tested with a `<b>ZZ</b>` tenant and with the reviewer id (AC1.1.10). |
| Browser calls only from named origins, never `*` | Decision 10. Start-up refuses `*` and `null`, and this is tested. |

## Steps

Test-after, per the Testing Contract: build each layer, then write and run that layer's tests through the verify script before starting the next layer. Paths are relative to `priorauth-api/` unless they start with `scripts\`. Each step lists the story it traces to.

### Step 1: Branch from the freshly pulled feature branch (US5160; team Way of Working)

- [ ] Run `scripts\pull-all.ps1` from the workspace root.
- [ ] In `priorauth-api`: `git switch -c f1220/us5160-save-filter origin/feature/F1220`.
- [ ] Confirm the working tree is clean and `HEAD` equals `origin/feature/F1220`.

### Step 2: Verify the test runner and record the API baseline (NFR8)

- [ ] Run `scripts\verify.cmd priorauth-api` on the new branch before any change.
- [ ] Record the exit code and the test count and failures from `target/surefire-reports/*.txt` in `code-summary.md`. The expected result is 12 tests, all passing.
- [ ] If the baseline is not green, stop and report it. Do not change any code.

### Step 3: Data model — implement (FR1.2, C6)

- [ ] Add `src/main/java/com/acmehealth/priorauth/model/SavedFilter.java`: `record SavedFilter(String tenant, boolean overLimit)`. Its one-line Javadoc names US5160 / FR1.2, and `tenant == null` means all tenants.
- There is no separate model test. The record has no logic, and the store and body tests in Steps 5 and 7 exercise it.

### Step 4: Data access — implement (FR1.1, FR1.4, FR1.5, FR2, FR3.1, FR3.2; ADR-001, ADR-002; NFR1, NFR3, NFR7)

- [ ] `src/main/resources/data/requests.sample.json`: add `{ "id": "PA-10270", "tenantId": "NM-02", "memberId": "M-40418", "service": "MRI knee", "status": "PENDED", "receivedAt": "2026-10-12" }` as the last row, in the file's column-aligned style.
- [ ] Add `src/main/java/com/acmehealth/priorauth/store/TenantDirectory.java`, a `@Service` with constructor injection of `RequestStore`.
  - At construction it builds an immutable sorted list of the distinct `tenantId`s from `RequestStore.all()`, using natural `String` order (plain character code, case-sensitive), and an immutable `Set`.
  - `boolean isKnown(String tenantId)` is false for `null`.
  - `List<String> list()`.
- [ ] Add `src/main/java/com/acmehealth/priorauth/store/ReviewerFilterStore.java`, a `@Service` built as Decisions 1-3 describe.
  - Constructor `ReviewerFilterStore(@Value("${priorauth.reviewer-filter.max-reviewers:10000}") int maxReviewers)`. A limit below 1 throws `IllegalArgumentException` naming the value.
  - Nested `enum SaveResult { SAVED, REVIEWER_LIMIT }`.
  - Javadoc names US5160, FR1, FR2, NFR1, NFR7 and says US5163 adds the history line inside the same lock.
- [ ] `src/main/resources/application.yml`: add `priorauth.reviewer-filter.max-reviewers: 10000` with a one-line comment (FR1.4, A3).

### Step 5: Data access — write and run its tests (and the existing tests the new row changes)

- [ ] New `src/test/java/com/acmehealth/priorauth/store/ReviewerFilterStoreTest.java`, plain JUnit with a fresh `new ReviewerFilterStore(n)` per test:
  - `saveThenReadReturnsTheFilter` (AC1.1.1)
  - `laterSaveReplacesTheEarlierOne` (AC1.1.2, FR1.5)
  - `readOfANeverSavedReviewerIsEmptyAndTakesNoSlot`: limit 1; read `new.one`, then save another new reviewer, which is `SAVED` (AC1.1.3)
  - `newReviewerBeyondTheLimitIsRefusedAndNothingIsSaved`: limit 2; `a1` and `b1` saved, `c1` gets `REVIEWER_LIMIT` and reads empty, and `a1` still saves (AC1.1.9, NFR7)
  - `reviewerIdsAreCaseSensitive` (AC1.1.8)
  - `limitBelowOneIsRefused`
- [ ] New `src/test/java/com/acmehealth/priorauth/store/TenantDirectoryTest.java`, built over a real `RequestStore`:
  - `listsEachKnownTenantOnceInCharacterOrder`: `["NM-02", "TX-01"]` (AC1.1.11)
  - `knowsTenantsExactly`: `TX-01` and `NM-02` are known (AC1.1.5)
  - `refusesWrongCaseUnknownAndNull`: `tx-01`, `ZZ-99` and `null` are not known (AC1.1.5, A4)
- [ ] Change `src/test/java/com/acmehealth/priorauth/store/RequestStoreTest.java` (FR3.2):
  - Size 4 becomes 5.
  - `all().get(3)` stays `PA-10263`, and `all().get(4)` is `PA-10270`.
  - `pending()` now contains `PA-10231, PA-10244, PA-10263, PA-10270`.
  - Add `allKeepsDecidedRequests`, which checks that `PA-10250` (APPROVED) is in `all()` but not in `pending()`.
- [ ] Change `src/test/java/com/acmehealth/priorauth/api/PendingRequestsControllerTest.java` (FR3.2, AC1.1.13): `listsPendingRequestsOldestFirst` expects 4 rows, not 3. The other two tests are unchanged and keep the file at the happy path plus two edge cases.
- [ ] Change `src/test/java/com/acmehealth/priorauth/api/TenantFilterTest.java` (FR3.2, FR3.3, AC1.1.13):
  - NM-02 now returns 1 row (`PA-10270`); TX-01 stays at 3.
  - Add `unknownTenantStillAnswersAnEmptyList`: `?tenant=ZZ-99` answers `200 []`.
  - Add `tenantMatchIsCaseSensitive`: `?tenant=tx-01` answers `200 []`.
- [ ] Run `scripts\verify.cmd priorauth-api`. It must be green, with `OverLimitFilterTest` unchanged and passing.

### Step 6: Request rules — implement (FR1.2, FR1.3, FR2.3, NFR3, NFR4)

- [ ] Add `api/ErrorCode.java`, an enum of the 4 contract codes. Each code carries its HTTP status (`400` or `409`), its wire code (`invalid-reviewer-id`, `invalid-body`, `unknown-tenant`, `reviewer-limit`) and its fixed message, copied character for character from the contract.
- [ ] Add `api/FilterRequestException.java`, a `RuntimeException` that carries only an `ErrorCode`. Its message is the code, never caller input.
- [ ] Add `api/ReviewerIds.java`, a `final` utility class with a private constructor.
  - `static String requireValid(String id)` returns the id or throws `FilterRequestException(INVALID_REVIEWER_ID)`.
  - It uses the contract's ASCII pattern, precompiled.
- [ ] Add `api/SavedFilterBody.java`, a `final` utility class: `static SavedFilter parse(String contentType, InputStream body, JsonMapper mapper, TenantDirectory tenants)`.
  - It checks in order: content type, then size (`readNBytes(1025)`), then readable JSON and exact shape (Decision 6). Each of these throws `INVALID_BODY`.
  - Then the tenant is checked; an unknown tenant throws `UNKNOWN_TENANT`.
  - An `IOException` while reading the body becomes `INVALID_BODY`.
  - JSON errors are caught and replaced, never passed on, so their messages (which can quote input) never reach the response.

### Step 7: Request rules — write and run their tests

- [ ] New `src/test/java/com/acmehealth/priorauth/api/ReviewerIdsTest.java`:
  - `acceptsLettersDigitsDotDashUnderscoreUpTo64`: includes `rita.k`, a 64-character id and `a`
  - `refusesBadIds`, parameterized: `rita k`, `rené`, a 65-character id, `-_-`, an empty string, `a/b` (AC1.1.7)
- [ ] New `src/test/java/com/acmehealth/priorauth/api/SavedFilterBodyTest.java`:
  - `parsesTheTwoFields`, with a known tenant and with `null` (AC1.1.1, AC1.1.2)
  - `refusesMalformedBodies`, parameterized over the 7 bodies in AC1.1.6 plus an empty body and trailing content, each giving `INVALID_BODY`
  - `refusesBodiesOver1024Bytes`: 1,025 bytes is refused and exactly 1,024 bytes (a valid body padded with spaces) is accepted (AC1.1.6, NFR3)
  - `contentTypeMustBeJson`: `application/json; charset=UTF-8` is accepted; missing, `text/plain` and unparsable types are refused
  - `refusesUnknownOrWrongCaseTenant`: `ZZ-99` and `tx-01` give `UNKNOWN_TENANT` (AC1.1.4, AC1.1.5)
  - `checksShapeBeforeTenant`: `{"tenant": "ZZ-99"}` gives `INVALID_BODY`, not `UNKNOWN_TENANT` (FR1.6)
- [ ] Run `scripts\verify.cmd priorauth-api`. It must be green.

### Step 8: API endpoints — implement (FR1, FR2, FR3.1, FR8, NFR4, NFR6; ADR-003, ADR-006)

- [ ] Add `api/ErrorResponse.java`: `record ErrorResponse(String error, String message)` with `static ErrorResponse from(ErrorCode)`.
- [ ] Add `api/SavedFilterResponse.java`: `record SavedFilterResponse(String tenant, boolean overLimit)` with `static SavedFilterResponse from(SavedFilter)`. A `null` tenant is written as `"tenant": null`, which is Spring Boot's default inclusion.
- [ ] Add `api/ReviewerFilterController.java`, a `@RestController` with constructor injection of `ReviewerFilterStore`, `TenantDirectory` and `JsonMapper`.
  - `@PutMapping("/reviewers/{reviewerId}/filter")` takes `@PathVariable String reviewerId`, `@RequestHeader(value = "Content-Type", required = false) String contentType` and `InputStream body`. It runs Decision 4's order and answers `204` on `SAVED`. `REVIEWER_LIMIT` throws `FilterRequestException(REVIEWER_LIMIT)`.
  - `@GetMapping("/reviewers/{reviewerId}/filter")` validates the id, then answers `SavedFilterResponse`, or `Map.of()` (`{}`) when nothing is saved.
- [ ] Add `api/TenantsController.java`, a `@RestController`: `@GetMapping("/tenants")` returns `tenantDirectory.list()`.
- [ ] Add `api/NewEndpointErrorHandler.java` (Decision 8): `@ExceptionHandler(FilterRequestException.class)` returns a `ResponseEntity<ErrorResponse>` with the code's status and `application/json`.
- [ ] Add `api/BrowserAccessPolicy.java`, a `@Configuration` implementing `WebMvcConfigurer` (Decision 10). The origin check is a package-visible static method, so it can be tested without a context.
- [ ] `application.yml`: add `priorauth.cors.allowed-origins: http://localhost:3000` with a one-line comment (named origins only, never `*`; parent OQ4 decides others).
- [ ] Every new main class gets a one-line purpose Javadoc naming US5160 and its FR or contract item. There are no wildcard imports, and Jackson imports are `tools.jackson.databind`.

### Step 9: API endpoints — write and run their tests (contract examples included)

- [ ] Copy these parent contract examples unchanged into `src/test/resources/contract/f1220/`:
  - `c1-put-filter-request.json`, `c1-get-filter-saved.json`, `c1-get-filter-nothing-saved.json`
  - `c2-get-tenants.json`
  - `error-invalid-reviewer-id.json`, `error-invalid-body.json`, `error-unknown-tenant.json`, `error-reviewer-limit.json`
  - `case-put-204.json`, `case-invalid-reviewer-id.json`, `case-invalid-body.json`, `case-unknown-tenant.json`, `case-reviewer-limit.json`, `case-multi-fault.json`, `case-preflight.json`

  The C3 history examples are US5163's.
- [ ] Add a test helper, `src/test/java/com/acmehealth/priorauth/api/ContractExamples.java`, which reads a file from `contract/f1220/` as a string or a `JsonNode`.
- [ ] New `api/ReviewerFilterControllerTest.java`, shared `@SpringBootTest` context. Each test uses its own reviewer id (prefix `rfc-<test>`), never the ids in the contract files (NFR9):
  - `saveAnswers204AndReadReturnsIt` (AC1.1.1)
  - `laterSaveReplaces` (AC1.1.2)
  - `neverSavedReadsAsEmptyObject` (AC1.1.3)
  - `unknownTenantIsRefusedAndTheSavedFilterIsKept` (AC1.1.4)
  - `knownTenantsAcceptedAndWrongCaseRefused` (AC1.1.5)
  - `malformedBodiesAreRefusedAndTheSavedFilterIsKept`, parameterized over AC1.1.6's 8 cases plus a missing content type and `text/plain`
  - `exactly1024ByteBodyIsAccepted` (AC1.1.6)
  - `invalidReviewerIdsAreRefusedOnPutAndGet`, parameterized, using `rita%20k`, `ren%C3%A9`, 65 characters and `-_-` (AC1.1.7)
  - `sixtyFourCharacterIdIsAccepted` (AC1.1.7)
  - `reviewerIdsAreCaseSensitive` (AC1.1.8)
  - `errorBodiesNeverEchoCallerInput`: tenant `<b>ZZ</b>` and a bad id. The body equals the fixed `{error, message}`, contains no `<b>`, no id, no `trace`, no `path` and no `instance` (AC1.1.10)
- [ ] New `api/ReviewerFilterContractTest.java`, shared context. It replays each C1 case file exactly (request method, path, headers and body, then status and body with strict JSON comparison): `case-put-204`, `case-invalid-reviewer-id`, `case-invalid-body`, `case-unknown-tenant` and `case-multi-fault`. It also checks that `c1-put-filter-request` saved for an own reviewer id reads back as `c1-get-filter-saved`, that a never-saved own id reads as `c1-get-filter-nothing-saved`, and that each `error-*.json` equals the body the matching case returns. This is the only class that writes the contract files' reviewer ids, and it asserts no state that another test writes.
- [ ] New `api/TenantsControllerTest.java`, shared context:
  - `listsTheKnownTenantsAsInTheContractExample`: equals `c2-get-tenants.json`, `["NM-02", "TX-01"]` (AC1.1.11)
  - `listsEachTenantOnceThoughItHasManyRequests` (FR3.1)
  - `pendingQueueStillAnswersEmptyForAnUnknownTenant`: `GET /requests/pending?tenant=ZZ-99` answers `200 []` (AC1.1.13)
- [ ] New `api/BrowserAccessPolicyTest.java`, shared context, plus static checks:
  - `preflightFromTheNamedOriginIsAllowed`: replays `case-preflight.json` (allowed origin, `GET,PUT`, `Content-Type`)
  - `otherOriginsGetNoPermission`: `http://evil.example` and `Origin: null` get no `Access-Control-Allow-Origin` (AC1.1.12)
  - `queueAndTenantsAreReachableFromTheNamedOrigin`: a GET of `/requests/pending` and `/tenants` with `Origin: http://localhost:3000` carries that origin back, never `*` (AC1.1.12, C4)
  - `wildcardNullAndBlankOriginsAreRefusedAtStartUp`: the static origin check throws for `*`, `null` and `""`
- [ ] New `api/ReviewerLimitHttpTest.java`, in its own context with `@SpringBootTest(properties = "priorauth.reviewer-filter.max-reviewers=2")`:
  - `newReviewerBeyondTheLimitGets409`: replays `case-reviewer-limit.json` after `a1` and `b1` save (AC1.1.9)
  - `keptReviewerCanStillSave`: `a1` saves again and gets 204 (AC1.1.9)
  - `refusedReviewerHasNothingSaved`: `c1` reads `{}` (AC1.1.9)
- [ ] New `api/DotReviewerIdTest.java`, in its own context with `@SpringBootTest(webEnvironment = RANDOM_PORT)` and `java.net.http.HttpClient` (Decision 9):
  - `singleDotIdAnswers404OnPutAndGet` (AC1.1.7)
  - `doubleDotIdAnswers404OnPutAndGet` (AC1.1.7)
  - `nothingIsSavedForDotIds`: the injected store reads `.` and `..` as empty, and the 404 body does not contain the submitted path segment
  - The test prints the real 404 body once, for `code-summary.md`.
- [ ] Run `scripts\verify.cmd priorauth-api`. It must be green.

### Step 10: Documentation and traceability (US5160)

- [ ] `README.md`: add 4 lines naming:
  - `PUT` and `GET /reviewers/{reviewerId}/filter`
  - `GET /tenants`
  - the two configuration keys
  - the in-memory, lost-on-restart store

  Plus one line `Changed by AI-DLC intent f1220-us5160`, in the file's existing style.
- [ ] Record in `code-summary.md`: the baseline from Step 2, the final verify output, the real 404 body for `.` and `..`, and every existing test file changed (`RequestStoreTest`, `PendingRequestsControllerTest`, `TenantFilterTest`).

### Step 11: Final verification and commit (team Way of Working)

- [ ] Run `scripts\verify.cmd priorauth-api` once more on the finished branch. It must be green, and the output goes into `code-summary.md` for the PR.
- [ ] `git -C priorauth-api add` only the files this plan names, then commit on `f1220/us5160-save-filter` with the message `US5160 save and read my last filter (intent f1220-us5160)`, matching the F1210 commit style.
- [ ] Do not push and do not open the PR. Kiran Rao does that after fetching and rebasing onto `origin/feature/F1220` and re-running the verify script.

### Step 12: Requested change — no default error body for 405 and 406 on the new endpoints (NFR4, AC1.1.10; Kiran Rao at the Code Generation gate)

Kiran Rao's request at the gate: "map the 405 and 406 errors on the new endpoints so no Spring default error body (with its path field carrying the reviewer id) is returned from them."

**The behaviour to build:**
- A call to `/reviewers/{reviewerId}/filter` or `/tenants` with a method that path does not support answers `405`. Examples: `DELETE` or `POST /reviewers/rita.k/filter`, `POST /tenants`. The `Allow` header lists the supported methods, as now.
- A call to those paths whose `Accept` header excludes JSON (for example `Accept: text/plain`) answers `406`.
- In both cases the answer has **no body**: no `path`, no `trace`, no reviewer id, no caller input.
- **Why no body:** the contract's error codes are fixed at four (C1-C3 `Error` enum). A new code is an additive change that only Meena Iyer can make, after she updates the examples. An empty body with the right status stays inside the contract and echoes nothing.

**Limits on the change:**
- `GET /requests/pending` keeps its existing error behaviour, including Spring Boot's default body (C4, AC1.1.13, ADR-003). The queue endpoint is not touched.
- No new dependency. Choose the smallest mechanism that meets these limits, and record which one and why in `code-summary.md`.
  - A controller-scoped `@RestControllerAdvice(assignableTypes = ...)` does not see a `405`, because Spring raises it before a controller is chosen.
  - So the mechanism must decide by request path, limited to `/reviewers/**` and `/tenants`.
  - Possible mechanisms: a narrowly path-checked global handler for these two exception types that lets every other path fall through unchanged, or a servlet filter on those two path patterns.
- Code lives in `api` (HTTP concerns stay in `api`). Every new or changed main class keeps its one-line purpose Javadoc naming US5160 / NFR4.

**Tasks:**
- [x] Implement the behaviour above in `priorauth-api/src/main/java/com/acmehealth/priorauth/api/`, changing `NewEndpointErrorHandler.java` or adding one class.
- [x] New `priorauth-api/src/test/java/com/acmehealth/priorauth/api/NewEndpointProtocolErrorTest.java`, on a real server (`@SpringBootTest(webEnvironment = RANDOM_PORT)` with `java.net.http.HttpClient`, as in `DotReviewerIdTest`). Spring Boot's default error body is only rendered on a real server, not in MockMvc.
  - `wrongMethodOnFilterAnswers405WithNoBody`: `DELETE` and `POST` `/reviewers/rfc-405/filter`. Status `405`, `Allow` header present, empty body that does not contain `rfc-405` or `path` (NFR4, AC1.1.10).
  - `wrongMethodOnTenantsAnswers405WithNoBody`: `POST /tenants`. Status `405`, empty body.
  - `nonJsonAcceptAnswers406WithNoBody`: `GET /reviewers/rfc-406/filter` and `GET /tenants` with `Accept: text/plain`. Status `406`, empty body that does not contain `rfc-406`.
  - `queueKeepsItsOwnErrorBody`: `DELETE /requests/pending` still answers `405` with Spring Boot's default JSON body, including its `path` field (C4, AC1.1.13: unchanged).
- [x] Run `scripts\verify.cmd priorauth-api`. It must be green, and every earlier test must still pass.
- [x] Update `code-summary.md`: the mechanism chosen and why, the new test class, the final verify result, and remove this item from "Skipped, Not Checked, and Risks".
- [x] Commit on `f1220/us5160-save-filter` as a second commit, `US5160 no default error body for 405 and 406 on the new endpoints (intent f1220-us5160)`, adding only the files this step changed. Do not amend `cb1aee7`, do not push and do not open a PR.

## Story-to-Step Traceability

| Requirement / AC | Steps |
|---|---|
| FR1.1, FR2.1 / AC1.1.1, AC1.1.2 | 3, 4, 5, 8, 9 |
| FR2.2, FR1.4 / AC1.1.3 | 4, 5, 8, 9 |
| FR1.2, FR3.1 / AC1.1.4, AC1.1.5 | 4, 6, 7, 8, 9 |
| FR1.2, NFR3 / AC1.1.6 | 6, 7, 8, 9 |
| FR1.3, FR2.3 / AC1.1.7, AC1.1.8 | 6, 7, 8, 9 |
| FR1.4, NFR7 / AC1.1.9 | 4, 5, 8, 9 |
| NFR4 / AC1.1.10 | 6, 8, 9, 12 |
| FR3.1 / AC1.1.11 | 4, 5, 8, 9 |
| FR8, NFR6 / AC1.1.12 | 8, 9 |
| FR3.2, FR3.3, NFR8 / AC1.1.13 | 2, 4, 5, 9 |
| FR1.6 check order | 6, 7, 8, 9 |
| FR1.5 last save wins | 4, 5 |
| NFR1 in-memory, replaceable store | 4 |

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

Layers that don't apply to this story: "Frontend behavior" (the screen is US5161 and US5162). "Project structure" and "Environment/build configuration" need no new build work: the module, `pom.xml` and the runner exist, and the two configuration keys are added in Steps 4 and 8.
