# Developer Code Scan: priorauth-api

- Repo: `priorauth-api` (sibling of the workspace root), branch `main` at `0e00544` (tag `v1.2.0`, merge of PR #85 `feature/F1220`), working tree clean, no untracked files.
- Breadth: full rescan of the whole repo (`./`), run for intent `f1220-us5163` as an isolated single-stage 2.1 run.
- Date: 2026-11-03. Tests were not run (documentation only).

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `./` (every tracked file, 67 files from `git ls-files`, read in full)
  - `pom.xml`
  - `README.md`
  - `.gitignore`
  - `src/main/java/com/acmehealth/priorauth/` (27 classes: root, `aging/`, `api/`, `model/`, `store/`)
  - `src/main/resources/application.yml`
  - `src/main/resources/data/` (`requests.sample.json`, `holidays-TX-01-2026.json`)
  - `src/test/java/com/acmehealth/priorauth/` (20 classes: root `MutableClock`, `aging/`, `api/`, `store/`)
  - `src/test/resources/contract/f1220/` (17 contract fixtures)
- **Skimmed only**: none
- **Left out**:
  - `target/` (Maven build output, ignored by `.gitignore`; not opened)
  - `.git/` (repository metadata; not opened)

### Packages Found
- `com.acmehealth.priorauth` (root): entry point, Java, `PriorAuthApiApplication` boots Spring and publishes the UTC `Clock` bean (US5163 NFR9).
- `com.acmehealth.priorauth.api`: controllers, request parsing and validation, response records, error mapping, CORS configuration (15 classes).
- `com.acmehealth.priorauth.aging`: business-day ageing, over-limit badge, per-tenant holiday calendar (3 classes).
- `com.acmehealth.priorauth.model`: domain records `PriorAuthRequest`, `SavedFilter`, `HistoryLine` (3 classes).
- `com.acmehealth.priorauth.store`: read-only request export, derived tenant directory, in-memory reviewer filter and history store (3 classes).
- Imports checked by hand: `api -> aging, store, model`; `store -> model`; `aging` and `model` import no app package; no cycles; no Spring web types in `store`, `model` or `aging`.

### Build System
- **Type**: Maven, single module, Spring Boot parent `spring-boot-starter-parent` 4.1.1, artifact `com.acmehealth:priorauth-api:1.2.0`, `java.version` 21.
- **Config Files**: `pom.xml`, `src/main/resources/application.yml`.
- **Build Dependencies**: `spring-boot-starter-webmvc` (compile), `spring-boot-starter-webmvc-test` (test), `spring-boot-maven-plugin`. No version pinned in the POM; every version comes from the parent. No wrapper (`mvnw`) is committed.

### APIs Discovered
- REST (Spring MVC) in `api/`, 5 endpoints:
  - `GET /requests/pending` (`PendingRequestsController`)
  - `PUT /reviewers/{reviewerId}/filter`, `GET /reviewers/{reviewerId}/filter`, `GET /reviewers/{reviewerId}/filter/history` (`ReviewerFilterController`)
  - `GET /tenants` (`TenantsController`)
- CORS for the three path groups in `BrowserAccessPolicy`; 405/406 no-body handling for `/reviewers/**` and `/tenants` in `NewEndpointProtocolErrorHandler`.

### Frameworks & Libraries
- Spring Boot 4.1.1 (parent BOM), Spring MVC with embedded Tomcat (from the webmvc starter).
- Jackson 3 (`tools.jackson.databind`, `tools.jackson.core`), version from the BOM; no `com.fasterxml.jackson` import anywhere.
- Jakarta Servlet API (`jakarta.servlet.http.HttpServletRequest`), from the starter.
- Test: JUnit 5 (Jupiter, including `junit-jupiter-params`), AssertJ, Spring MockMvc, Spring Boot Test, JDK `java.net.http.HttpClient` for real-server tests.

### Test Coverage
- **Test Directories**: `src/test/java/com/acmehealth/priorauth/` (mirrors main: `aging/`, `api/`, `store/`, plus `MutableClock`), `src/test/resources/contract/f1220/`.
- **Test Frameworks**: JUnit 5, AssertJ, Spring MockMvc (`@SpringBootTest` + `@AutoConfigureMockMvc`), `RANDOM_PORT` real server for `DotReviewerIdTest` and `NewEndpointProtocolErrorTest`.
- **Test count**: 90 test methods in 18 test classes (81 `@Test`, 9 `@ParameterizedTest`), which expand to 118 executions (matches the earlier Build and Test record of 118/118 at `d1d11a5`; not rerun here).
- **Coverage Config**: absent (no JaCoCo or other plugin in `pom.xml`).

### Code Quality Indicators
- **Linting**: none (no Checkstyle, SpotBugs, PMD, Spotless or `.editorconfig`).
- **CI/CD**: none (no `.github/workflows/`, Jenkinsfile or other pipeline file in the repo).
- **Documentation**: `README.md` (endpoints, configuration keys, run commands, AI-DLC intents that changed the repo); every main class except `PriorAuthApiApplication`'s requirement tag has a one-line purpose Javadoc naming its FR/US; tests carry FR/AC tags on each `@Test`.

### Technical Debt Signals
- `aging/HolidayCalendar.java:35`: the holiday file name hard-codes the year (`"data/holidays-" + tenantId + "-2026.json"`), and only `holidays-TX-01-2026.json` exists. Any as-of date in 2027 (F1220 ships in 2027.Q1 R1) counts 2027 holidays as business days, and `NM-02` has no holidays at all. Safe-direction by the class's own rule (age is never lower), but ages become wrong after 2026-12-31.
- `aging/HolidayCalendar.java:42`: `root.get("holidays")` is not null-checked; a file without that key throws `NullPointerException` (a 500), not the documented `IllegalStateException`.
- `api/PendingRequestsController.java:36`: the default as-of day uses `LocalDate.now()` (system clock and zone), not the injected `Clock` bean that US5163 added; the default date cannot be pinned in a test.
- `api/RequestFilter.java:6-13`: the `tenant` query parameter of `GET /requests/pending` is neither validated nor size-limited (predates the team's security checklist); `overLimit=false` behaves the same as absent.
- `store/ReviewerFilterStore.java:31-32`: worst-case memory is `max-reviewers` x `max-history-lines` = 10,000 x 1,000 = 10 million `HistoryLine` objects in the heap with the defaults; bounded, but not sized against a heap limit.
- No authentication or authorization anywhere: any caller can read or write any reviewer's filter and history (known and accepted for F1220, stated in the release notes).
- `api/DotReviewerIdTest.java:53`: `System.out.println` diagnostic left in a test.
- No TODO, FIXME, HACK or `@SuppressWarnings` in the code.

## Handoff Summary
- **Intent-relevant finding**: US5163 (filter history) is implemented and released in `v1.2.0`. `ReviewerFilterStore.save` (`store/ReviewerFilterStore.java:55-64`) writes the filter and its `HistoryLine` inside one `synchronized` block, so a save and its line never come apart; `appendHistoryLine` (lines 82-89) adds newest-first to a per-reviewer `ArrayDeque`, cuts the time to the second from the injected `Clock`, and drops the oldest line past `priorauth.reviewer-filter.max-history-lines` (default 1000, at least 1). `GET /reviewers/{reviewerId}/filter/history` (`api/ReviewerFilterController.java:57-61`) validates the id with `ReviewerIds`, maps through `HistoryLineResponse` (ISO-8601 UTC `at`), and answers `[]` for a reviewer who never saved. A refused save (bad id, bad body, unknown tenant, reviewer limit) writes no line. Tests: `ReviewerFilterHistoryTest` (10), `ReviewerFilterStoreTest` (9 of 15 for US5163), `DotReviewerIdTest`, `NewEndpointProtocolErrorTest`.
- **Risks / follow-up**: history is lost on restart and readable by anyone (no auth); worst-case heap of 10 million lines with default limits; the hard-coded 2026 holiday file makes 2027 ages wrong for the release that ships this feature; `GET /requests/pending` still reads the system clock; no coverage, linting or CI. None of these were changed by this scan.
