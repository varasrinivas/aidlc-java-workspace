# Component Inventory: priorauth-api

Twenty-five main-source components in one Maven module, from a full rescan of `main` at `0e00544` (tag `v1.2.0`), 2026-11-03. Each `###` heading is the component name used in the Scope of Analysis block. Test counts are executions (parameterized cases expanded).

## Summary

| Component | Package | Kind | Spring bean | Introduced by |
|---|---|---|---|---|
| PriorAuthApiApplication | root | Entry point, Clock bean | `@SpringBootApplication` | v1.0.x; Clock US5163 |
| PendingRequestsController | `api` | REST controller | `@RestController` | v1.0.x, ageing 261013, filters F1210 |
| RequestFilter | `api` | Query record | no | F1210 US5150-US5152 |
| PendingRequestResponse | `api` | Response record | no | 261013-request-age-api |
| ReviewerFilterController | `api` | REST controller | `@RestController` | F1220 US5160 (C1), US5163 (C3) |
| TenantsController | `api` | REST controller | `@RestController` | F1220 US5160 (C2) |
| SavedFilterBody | `api` | Body parser and validator | no | F1220 US5160 |
| SavedFilterResponse | `api` | Response record | no | F1220 US5160 |
| HistoryLineResponse | `api` | Response record | no | F1220 US5163 |
| ReviewerIds | `api` | Validator | no | F1220 US5160 |
| ErrorCode | `api` | Enum | no | F1220 US5160 |
| ErrorResponse | `api` | Error record | no | F1220 US5160 |
| FilterRequestException | `api` | Exception | no | F1220 US5160 |
| NewEndpointErrorHandler | `api` | Scoped advice | `@RestControllerAdvice` | F1220 US5160 |
| NewEndpointProtocolErrorHandler | `api` | Global path-matched advice | `@RestControllerAdvice` | F1220 US5160 |
| BrowserAccessPolicy | `api` | CORS configuration | `@Configuration` | F1220 US5160 |
| BusinessDays | `aging` | Static utility | no | 261013-request-age-api |
| AgeBadge | `aging` | Value record | no | 261013-request-age-api |
| HolidayCalendar | `aging` | Cached loader | `@Service` | 261013-request-age-api |
| PriorAuthRequest | `model` | Domain record | no | v1.0.x |
| SavedFilter | `model` | Domain record | no | F1220 US5160 |
| HistoryLine | `model` | Domain record | no | F1220 US5163 |
| RequestStore | `store` | Read-only repository | `@Service` | v1.0.x |
| TenantDirectory | `store` | Derived directory | `@Service` | F1220 US5160 |
| ReviewerFilterStore | `store` | In-memory repository with lock | `@Service` | F1220 US5160, US5163 |

## Components

### PriorAuthApiApplication
- **Responsibility**: Boots Spring (scan root `com.acmehealth.priorauth`); publishes `Clock clock()` = `Clock.systemUTC()` (US5163 NFR9).
- **Depends on**: Spring Boot.
- **Tests**: loaded by every `@SpringBootTest`; `ReviewerFilterHistoryTest` overrides the clock with a `@Primary` `MutableClock`.

### PendingRequestsController
- **Responsibility**: `GET /requests/pending`; binds `asOf` and `RequestFilter`, ages each pending request, filters, maps `IllegalArgumentException` to 400.
- **Depends on**: RequestStore, HolidayCalendar, AgeBadge, RequestFilter, PendingRequestResponse; `priorauth.aging.threshold-days`.
- **Tests**: `PendingRequestsControllerTest` (3), `TenantFilterTest` (3), `OverLimitFilterTest` (1), part of `TenantsControllerTest`, `BrowserAccessPolicyTest`, `NewEndpointProtocolErrorTest`.

### RequestFilter
- **Responsibility**: `record RequestFilter(String tenant, Boolean overLimit)`; `matches()` ANDs the active filters.
- **Depends on**: PendingRequestResponse.

### PendingRequestResponse
- **Responsibility**: One pending-list row; `from(PriorAuthRequest, AgeBadge)`; omits `memberId`.
- **Depends on**: PriorAuthRequest, AgeBadge.

### ReviewerFilterController
- **Responsibility**: `PUT` and `GET /reviewers/{reviewerId}/filter`, `GET /reviewers/{reviewerId}/filter/history`. Reads the PUT body as a raw `InputStream` so the contract's check order decides every refusal; turns `SaveResult.REVIEWER_LIMIT` into `FilterRequestException(REVIEWER_LIMIT)`.
- **Depends on**: ReviewerFilterStore, TenantDirectory, `JsonMapper`, ReviewerIds, SavedFilterBody, SavedFilterResponse, HistoryLineResponse, FilterRequestException, ErrorCode.
- **Tests**: `ReviewerFilterControllerTest` (23), `ReviewerFilterContractTest` (7), `ReviewerLimitHttpTest` (3), `ReviewerFilterHistoryTest` (10), `DotReviewerIdTest` (4), part of `NewEndpointProtocolErrorTest`.

### TenantsController
- **Responsibility**: `GET /tenants` -> `TenantDirectory.list()`.
- **Depends on**: TenantDirectory.
- **Tests**: `TenantsControllerTest` (3).

### SavedFilterBody
- **Responsibility**: `static SavedFilter parse(contentType, InputStream, JsonMapper, TenantDirectory)`: JSON content type -> at most `MAX_BYTES = 1024` (`readNBytes(1025)`) -> non-empty single JSON value (`FAIL_ON_TRAILING_TOKENS`) -> exactly `tenant` (string or null) and `overLimit` (boolean) -> known tenant. Drops Jackson and media-type exception messages, which can quote caller input.
- **Depends on**: SavedFilter, TenantDirectory, Jackson 3, Spring `MediaType`, FilterRequestException, ErrorCode.
- **Tests**: `SavedFilterBodyTest` (15).

### SavedFilterResponse
- **Responsibility**: `{tenant, overLimit}` wire record; `from(SavedFilter)`.
- **Depends on**: SavedFilter.

### HistoryLineResponse
- **Responsibility**: `{at, reviewer, tenant, overLimit}` wire record; `from(HistoryLine)` renders `at` with `Instant.toString()` (ISO-8601 UTC, seconds always shown because the store truncates to the second).
- **Depends on**: HistoryLine.

### ReviewerIds
- **Responsibility**: `static String requireValid(String)` against `^(?=.*[A-Za-z0-9])[A-Za-z0-9._-]{1,64}$`; throws `INVALID_REVIEWER_ID` (also for `null`).
- **Depends on**: FilterRequestException, ErrorCode.
- **Tests**: `ReviewerIdsTest` (9).

### ErrorCode
- **Responsibility**: `INVALID_REVIEWER_ID` (400), `INVALID_BODY` (400), `UNKNOWN_TENANT` (400), `REVIEWER_LIMIT` (409), each with a fixed message (listed in `api-documentation.md`).
- **Depends on**: Spring `HttpStatus`.

### ErrorResponse
- **Responsibility**: `{error, message}` wire record; `from(ErrorCode)`.
- **Depends on**: ErrorCode.

### FilterRequestException
- **Responsibility**: Unchecked exception carrying only an `ErrorCode`; its message is the code string.
- **Depends on**: ErrorCode.

### NewEndpointErrorHandler
- **Responsibility**: `@RestControllerAdvice(assignableTypes = {ReviewerFilterController, TenantsController})`; `FilterRequestException` -> code status + JSON `ErrorResponse`.
- **Depends on**: FilterRequestException, ErrorCode, ErrorResponse.
- **Tests**: through the controller and contract tests.

### NewEndpointProtocolErrorHandler
- **Responsibility**: Global advice for `HttpRequestMethodNotSupportedException` (405) and `HttpMediaTypeNotAcceptableException` (406); on `/reviewers/**` or `/tenants` (matched on the parsed `RequestPath`) answers status and headers with no body, otherwise rethrows so Spring's default handling stays.
- **Depends on**: Spring MVC `PathPatternParser`, `ServletRequestPathUtils`, Jakarta `HttpServletRequest`.
- **Tests**: `NewEndpointProtocolErrorTest` (6, real server).

### BrowserAccessPolicy
- **Responsibility**: `WebMvcConfigurer` CORS mapping (paths, origins, methods, headers in `api-documentation.md`); `static List<String> namedOrigins(String)` refuses `*`, `null`, empty entries with `IllegalStateException` at start-up.
- **Depends on**: Spring MVC `CorsRegistry`; `priorauth.cors.allowed-origins`.
- **Tests**: `BrowserAccessPolicyTest` (5), `NewEndpointProtocolErrorTest.preflightsAreUnchanged`.

### BusinessDays
- **Responsibility**: `isBusinessDay(day, holidays)`, `between(start, end, holidays)` counting `(start, end]`; throws `IllegalArgumentException` when `end` is before `start`.
- **Depends on**: JDK only.
- **Tests**: `BusinessDaysTest` (4).

### AgeBadge
- **Responsibility**: `record AgeBadge(int businessDays, boolean overLimit, int thresholdDays)`; `of(...)` computes; `label()` gives `"7 bd OVER 5"` or `"4 bd"`.
- **Depends on**: BusinessDays.
- **Tests**: `AgeBadgeTest` (1).

### HolidayCalendar
- **Responsibility**: `forTenant(tenantId)` -> holiday set from `classpath:data/holidays-<tenant>-2026.json`, cached in a `ConcurrentHashMap`; missing file means no holidays; unreadable file throws `IllegalStateException`. The tenant id comes from the export, not from a caller.
- **Depends on**: Jackson 3 `JsonMapper`, Spring `ClassPathResource`.
- **Tests**: indirectly through `PendingRequestsControllerTest` (12 Oct TX-01 holiday); no direct unit test.

### PriorAuthRequest
- **Responsibility**: `record PriorAuthRequest(id, tenantId, memberId, service, status, LocalDate receivedAt)`; `isPending()` for `PENDED` or `IN_REVIEW`.
- **Depends on**: JDK only.

### SavedFilter
- **Responsibility**: `record SavedFilter(String tenant, boolean overLimit)`; `null` tenant = all tenants.
- **Depends on**: JDK only.

### HistoryLine
- **Responsibility**: `record HistoryLine(Instant at, String reviewer, String tenant, boolean overLimit)`; one line per successful save (US5163 FR7.1).
- **Depends on**: JDK only.

### RequestStore
- **Responsibility**: Loads `classpath:data/requests.sample.json` once in the constructor, sorted by `receivedAt` then `id`; `all()` and `pending()`. A load failure stops start-up.
- **Depends on**: PriorAuthRequest, Jackson 3 `JsonMapper`, Spring `ClassPathResource`.
- **Tests**: `RequestStoreTest` (3).

### TenantDirectory
- **Responsibility**: Distinct `tenantId`s of `RequestStore.all()`, sorted; `isKnown(id)` (exact, case-sensitive, `null` never known), `list()`.
- **Depends on**: RequestStore, PriorAuthRequest.
- **Tests**: `TenantDirectoryTest` (3).

### ReviewerFilterStore
- **Responsibility**: `save(id, filter) -> SaveResult` (refuses a new reviewer at `maxReviewers`; otherwise replaces the filter and prepends a `HistoryLine` stamped `clock.instant().truncatedTo(SECONDS)`, dropping the oldest past `maxHistoryLines`), `read(id) -> Optional<SavedFilter>`, `history(id) -> List<HistoryLine>` (immutable copy, newest first). Every operation runs under one `synchronized` lock; reads never add entries.
- **Depends on**: SavedFilter, HistoryLine, `java.time.Clock`; `priorauth.reviewer-filter.max-reviewers` (default 10000), `priorauth.reviewer-filter.max-history-lines` (default 1000), each at least 1 or `IllegalArgumentException` at start-up.
- **State**: two `HashMap`s (filters; per-reviewer `ArrayDeque<HistoryLine>`), process lifetime, one singleton shared by every request.
- **Tests**: `ReviewerFilterStoreTest` (15, fresh store and `MutableClock` per test, including a 50-thread concurrent save test), plus the HTTP tests above.

## Non-code Components

| Item | Role |
|---|---|
| `application.yml` | Port 8080, app name, threshold 5, CORS `http://localhost:3000`, max reviewers 10000, max history lines 1000 |
| `data/requests.sample.json` | 5 requests: TX-01 x4 (3 pending, 1 `APPROVED`), NM-02 x1 (pending) |
| `data/holidays-TX-01-2026.json` | 11 TX-01 holidays for 2026 |
| `src/test/resources/contract/f1220/` | 17 contract fixtures (listed in `api-documentation.md`) |
| Test support | `MutableClock` (test UTC clock), `ContractExamples` (fixture reader) |
