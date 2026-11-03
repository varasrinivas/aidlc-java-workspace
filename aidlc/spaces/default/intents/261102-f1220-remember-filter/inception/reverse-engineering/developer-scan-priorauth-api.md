# Developer Code Scan: priorauth-api

Full rescan of `priorauth-api` on `main` at `0e00544` (F1220 merged, version 1.2.0), 2026-11-03. Run in the conductor's session (lead-only pipeline) after the developer hand-off was refused by the Code Generation dispatch check.

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `./` (whole repo: every tracked file was read or inventoried)
  - `pom.xml`, `README.md`, `.gitignore`
  - `src/main/java/com/acmehealth/priorauth/` (all 26 main classes: root, `aging/`, `api/`, `model/`, `store/`)
  - `src/main/resources/application.yml`
  - `src/main/resources/data/` (`holidays-TX-01-2026.json`, `requests.sample.json`)
  - `src/test/java/com/acmehealth/priorauth/` (test helpers `MutableClock`, `ContractExamples` read in full; `ReviewerFilterContractTest` read in part; every test class inventoried with its test count)
  - `src/test/resources/contract/f1220/` (17 contract example files, inventoried by name and purpose)
- **Skimmed only**:
  - Bodies of the 17 test classes other than the helpers and `ReviewerFilterContractTest` (names, counts and FR/US tags read; assertions not read line by line)
  - Contents of the 17 contract example JSON files (names and roles, not every field)
- **Left out**:
  - `target/` (Maven build output, gitignored; not present in the tracked tree)
  - `.idea/`, `*.iml`, `.vscode/` (IDE files, gitignored)

### Packages Found
- `com.acmehealth.priorauth` - Spring Boot entry point - Java - `PriorAuthApiApplication` plus the UTC `Clock` bean (US5163 NFR9)
- `com.acmehealth.priorauth.aging` - domain - Java - business-day age and over-limit badge (`AgeBadge`, `BusinessDays`, `HolidayCalendar`)
- `com.acmehealth.priorauth.api` - HTTP layer - Java - 3 controllers, request/response records, contract validation (`ReviewerIds`, `SavedFilterBody`), error codes and two `@RestControllerAdvice` handlers, CORS policy
- `com.acmehealth.priorauth.model` - domain records - Java - `PriorAuthRequest`, `SavedFilter`, `HistoryLine`
- `com.acmehealth.priorauth.store` - data access - Java - `RequestStore` (packaged export), `TenantDirectory`, `ReviewerFilterStore` (in memory)

### Build System
- **Type**: Maven, single module, `spring-boot-starter-parent` 4.1.1, Java 21, artifact `com.acmehealth:priorauth-api:1.2.0`
- **Config Files**: `pom.xml`, `src/main/resources/application.yml`
- **Build Dependencies**: `api -> aging, store, model`; `store -> model`; `aging` depends on no app package. No cycles.

### APIs Discovered
- REST - `PendingRequestsController` - 1 endpoint: `GET /requests/pending[?asOf&tenant&overLimit]`
- REST - `ReviewerFilterController` - 3 endpoints: `PUT` / `GET /reviewers/{reviewerId}/filter`, `GET /reviewers/{reviewerId}/filter/history`
- REST - `TenantsController` - 1 endpoint: `GET /tenants`
- CORS - `BrowserAccessPolicy` - named origins for the three path groups, methods GET and PUT, header `Content-Type`

### Frameworks & Libraries
- Spring Boot - 4.1.1 (parent) - application framework, embedded Tomcat
- spring-boot-starter-webmvc - managed by parent - Spring MVC, JSON (Jackson 3, `tools.jackson.*`)
- spring-boot-starter-webmvc-test (test scope) - managed by parent - JUnit 5, AssertJ, MockMvc
- spring-boot-maven-plugin - managed by parent - `mvn spring-boot:run`, runnable jar

### Test Coverage
- **Test Directories**: `src/test/java/com/acmehealth/priorauth/{,aging,api,store}`, `src/test/resources/contract/f1220/`
- **Test Frameworks**: JUnit 5, AssertJ, Spring MockMvc (`@SpringBootTest` + `@AutoConfigureMockMvc` for HTTP tests)
- **Test volume**: 18 test classes, 91 `@Test`/`@ParameterizedTest` methods; the last recorded verify run (Build and Test, `d1d11a5`) executed 118 tests, all passing
- **Coverage Config**: absent (no JaCoCo); the team records coverage as NOT MEASURED

### Code Quality Indicators
- **Linting**: none (no Checkstyle, SpotBugs, PMD, Spotless); style by convention and review
- **CI/CD**: none in the repo; tests run through the workspace `scripts\verify.cmd`
- **Documentation**: `README.md` documents every endpoint, the three settings and the in-memory limitation; every main class carries a purpose Javadoc naming its FR/US

### Technical Debt Signals
- `aging/HolidayCalendar.java`: holiday file name is fixed to year 2026 (`data/holidays-<tenant>-2026.json`); from 2027-01-01 every age ignores holidays unless a 2027 file is added. F1220 ships in 2027.Q1.
- `aging/HolidayCalendar.java`: only `TX-01` has a holiday file; `NM-02` silently has none (documented safe default).
- `api/PendingRequestsController.java:36`: default as-of date uses `LocalDate.now()` (system zone), not the `Clock` bean that history uses.
- `store/ReviewerFilterStore.java`: saved filters and history are in memory only; lost on restart, and no authentication means anyone can read or write any reviewer's filter (release-notes item).
- `store/RequestStore.java`: reads the packaged sample export (5 requests, tenants `TX-01` x4, `NM-02` x1), not the queue database.
- `api/RequestFilter.java`: `GET /requests/pending` accepts any `tenant` value without validation (returns an empty list for an unknown one), unlike the new endpoints.
- `pom.xml` `<description>` still says only "pending requests per tenant" and omits the F1220 endpoints; minor.

## Handoff Summary
- **Intent-relevant finding**: F1220 is fully present on `main`: `ReviewerFilterController` (C1, C3), `TenantsController` (C2), `ReviewerFilterStore` with saved filter and history written under one lock (`store/ReviewerFilterStore.java:55-64`), contract validation in a fixed order (`api/SavedFilterBody.java:27-35`), fixed error bodies scoped to the new endpoints (`api/NewEndpointErrorHandler.java:12`), and named-origin CORS (`api/BrowserAccessPolicy.java:18-35`).
- **Risks / follow-up**: the 2026-only holiday file (`HolidayCalendar.java:35`) affects ages from 2027; in-memory store and no authentication (already a release-notes item); `LocalDate.now()` vs the injected `Clock` for the pending list's default date.
