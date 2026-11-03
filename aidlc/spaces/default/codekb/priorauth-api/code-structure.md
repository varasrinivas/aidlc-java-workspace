# Code Structure: priorauth-api

Full rescan of `main` at `0e00544` (tag `v1.2.0`), 2026-11-03. 68 tracked files (25 main Java classes, 3 main resources, 20 test Java classes, 17 test fixtures, 3 root files); `target/` (build output) and `.git/` were not opened.

## Layout

```
priorauth-api/
  .gitignore                      target/, .idea/, *.iml, .vscode/
  README.md                       endpoints, config keys, run commands, AI-DLC intents
  pom.xml                         Spring Boot 4.1.1 parent, Java 21, version 1.2.0
  src/main/java/com/acmehealth/priorauth/
    PriorAuthApiApplication.java  entry point + UTC Clock bean
    aging/                        AgeBadge, BusinessDays, HolidayCalendar
    api/                          15 classes: 3 controllers, parsing/validation, responses, errors, CORS
    model/                        HistoryLine, PriorAuthRequest, SavedFilter
    store/                        RequestStore, ReviewerFilterStore, TenantDirectory
  src/main/resources/
    application.yml               port, threshold, CORS origins, reviewer and history limits
    data/requests.sample.json     5 requests (TX-01 x4, NM-02 x1)
    data/holidays-TX-01-2026.json 11 TX-01 holidays for 2026
  src/test/java/com/acmehealth/priorauth/
    MutableClock.java             test UTC clock (US5163 NFR9)
    aging/                        AgeBadgeTest, BusinessDaysTest
    api/                          13 test classes + ContractExamples helper
    store/                        RequestStoreTest, ReviewerFilterStoreTest, TenantDirectoryTest
  src/test/resources/contract/f1220/   17 contract fixtures (C1, C2, C3, cases, errors)
```

## File Classification (main source, 25 classes and 3 resources)

| Category | Files |
|---|---|
| Configuration | `PriorAuthApiApplication` (Clock bean), `api/BrowserAccessPolicy` (CORS), `application.yml` |
| Controller | `api/PendingRequestsController`, `api/ReviewerFilterController`, `api/TenantsController` |
| Middleware (error mapping) | `api/NewEndpointErrorHandler`, `api/NewEndpointProtocolErrorHandler`, `api/FilterRequestException`, `api/ErrorCode` |
| Model / DTO | `model/PriorAuthRequest`, `model/SavedFilter`, `model/HistoryLine`; `api/PendingRequestResponse`, `api/SavedFilterResponse`, `api/HistoryLineResponse`, `api/ErrorResponse`, `api/RequestFilter` (query) |
| Utility / validator | `api/SavedFilterBody`, `api/ReviewerIds`, `aging/BusinessDays` |
| Service | `aging/AgeBadge` (value object with factory), `aging/HolidayCalendar` |
| Repository | `store/RequestStore`, `store/TenantDirectory`, `store/ReviewerFilterStore` |
| Static data | `data/requests.sample.json`, `data/holidays-TX-01-2026.json` |

Per-component detail is in `component-inventory.md`.

## Code Patterns

- **Records for data**, with static factories: `of(...)` computes (`AgeBadge.of`), `from(...)` maps (`PendingRequestResponse.from`, `SavedFilterResponse.from`, `HistoryLineResponse.from`, `ErrorResponse.from`).
- **Final utility classes** with a private constructor for pure functions (`BusinessDays`, `SavedFilterBody`, `ReviewerIds`); package-private where only `api` uses them.
- **Constructor injection only**; configuration through `@Value("${priorauth.<kebab-key>:<default>}")`.
- **Error style**: domain throws `IllegalArgumentException` (caller error) or `IllegalStateException` (unrecoverable I/O); `api` maps them (`ResponseStatusException` 400 for the queue; `FilterRequestException(ErrorCode)` for the new endpoints).
- **Concurrency**: immutable collections for read-only data (`List.copyOf`, `Set.copyOf`, `toList()`); one `synchronized` lock in `ReviewerFilterStore`; `ConcurrentHashMap.computeIfAbsent` cache in `HolidayCalendar`.
- **Requirement tags**: class Javadoc and inline comments name the FR/US/AC/ADR; each `@Test` carries its tag.
- **Style**: 4-space indent, continuation 8, imports grouped app, third-party, `java.*`, static; no wildcard imports in main code.

## Test Structure

- Tests mirror the main package tree. Domain and store classes have plain JUnit tests (`<Class>Test`) with fresh instances; HTTP behaviour is tested with `@SpringBootTest` + MockMvc, and with a real server (`RANDOM_PORT`) where Tomcat behaviour matters (`DotReviewerIdTest`, `NewEndpointProtocolErrorTest`).
- Isolation: the shared Spring context holds one `ReviewerFilterStore`; each test class writes its own reviewer-id prefix (`rfc-`, `rfh-`, `rfs-`), and classes that need other limits start their own context through `properties` (`ReviewerLimitHttpTest`, `ReviewerFilterHistoryTest`).
- Contract fixtures under `contract/f1220/` are read by `ContractExamples` and replayed or compared as JSON trees.
- Counts and gaps are in `code-quality-assessment.md`.
