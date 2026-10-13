# Developer Code Scan: priorauth-api

Repo: `priorauth-api/` · HEAD `d9aa178afefad32cd7599dd60267038b3d01fe2b` (branch `main`) · Scan date 2026-10-13 · Breadth: full (first scan, no existing store)

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `./` (the whole repository; every tracked, hand-written file was read in full)
  - `pom.xml`
  - `README.md`
  - `.gitignore`
  - `src/main/java/com/acmehealth/priorauth/PriorAuthApiApplication.java`
  - `src/main/java/com/acmehealth/priorauth/api/PendingRequestsController.java`
  - `src/main/java/com/acmehealth/priorauth/api/PendingRequestResponse.java`
  - `src/main/java/com/acmehealth/priorauth/model/PriorAuthRequest.java`
  - `src/main/java/com/acmehealth/priorauth/store/RequestStore.java`
  - `src/main/resources/application.yml`
  - `src/main/resources/data/requests.sample.json`
  - `src/test/java/com/acmehealth/priorauth/api/PendingRequestsControllerTest.java`
  - `src/test/java/com/acmehealth/priorauth/store/RequestStoreTest.java`
- **Skimmed only**: none
- **Left out**:
  - `.git/` (version-control metadata; only `HEAD` and `refs/heads/main` were read to record the commit hash)
  - `target/`, `.idea/`, `*.iml`, `.vscode/` (ignored by `.gitignore`; none present on disk)

### Packages Found
- `com.acmehealth.priorauth` — application entry point — Java 21 — `@SpringBootApplication` bootstrap
- `com.acmehealth.priorauth.api` — controller + response DTO — Java 21 — HTTP surface for the reviewer screen (`GET /requests/pending`)
- `com.acmehealth.priorauth.model` — domain model — Java 21 — `PriorAuthRequest` record and the "pending" rule
- `com.acmehealth.priorauth.store` — data access — Java 21 — loads the nightly export from the classpath, sorts oldest first, filters pending

Single Maven module; no sub-modules.

### Build System
- **Type**: Maven (no Maven wrapper `mvnw` in the repo; relies on a system `mvn`)
- **Config Files**: `pom.xml`, `src/main/resources/application.yml`
- **Build Dependencies**: single module; `spring-boot-starter-parent` 4.1.1 manages all versions. Workspace verification goes through `scripts/verify.sh` / `scripts\verify.cmd`, which run `mvn -q test` inside `priorauth-api/`.

### APIs Discovered
- REST (Spring MVC) — `api/PendingRequestsController.java` — 1 endpoint: `GET /requests/pending` → JSON array of `PendingRequestResponse {id, tenantId, service, status, receivedAt}` (`receivedAt` is an ISO `LocalDate`), oldest first. No parameters, no paging, no authentication, no error envelope.

### Frameworks & Libraries
- Java — 21 (`java.version` property) — language/runtime
- Spring Boot — 4.1.1 (parent POM) — application framework
- `spring-boot-starter-webmvc` — managed by Boot 4.1.1 — Spring MVC, embedded Tomcat, JSON (Jackson 3, package `tools.jackson.*`)
- `spring-boot-starter-webmvc-test` (test scope) — managed — JUnit 5 (Jupiter), AssertJ, MockMvc, Spring Boot Test
- `spring-boot-maven-plugin` — managed — runnable jar and `spring-boot:run`

### Test Coverage
- **Test Directories**: `src/test/java/com/acmehealth/priorauth/api/`, `src/test/java/com/acmehealth/priorauth/store/`
- **Test Frameworks**: JUnit 5, AssertJ, Spring MockMvc (`@SpringBootTest` + `@AutoConfigureMockMvc`)
- **Coverage Config**: absent (no JaCoCo or other coverage plugin)
- 3 tests total: `PendingRequestsControllerTest.listsPendingRequestsOldestFirst` (full-context endpoint test), `RequestStoreTest.loadsTheSampleOldestFirst`, `RequestStoreTest.pendingExcludesDecidedRequests` (plain unit tests). All read the real classpath sample `data/requests.sample.json`.
- Test command: `mvn -q test` (workspace rule: run through `scripts/verify.sh`, or `scripts\verify.cmd` on Windows). The suite was not executed during this scan.

### Code Quality Indicators
- **Linting**: none (no Checkstyle, SpotBugs, PMD, Spotless or formatter plugin; no `.editorconfig`)
- **CI/CD**: none in the repo (no `.github/`, Jenkinsfile or other pipeline files)
- **Documentation**: short `README.md` (purpose, `mvn test`, `mvn spring-boot:run`); every class has a one-line Javadoc that explains its purpose. Naming is clear and every method is under 10 lines.

### Technical Debt Signals
- Data source is a classpath JSON sample ("nightly export packed into the jar"); `RequestStore` Javadoc says production reads the queue database. The data is fixed at startup and not refreshed (`store/RequestStore.java:13-30`).
- No business-day, holiday or age logic, and no holiday configuration, anywhere in the repo. The nightly report that already computes AGE is not in this repo (`docs-in/request.md` only says "same rule as the report").
- The code has no time source (`Clock`/`LocalDate.now()`), so "today" is not yet injectable for deterministic tests.
- Status values are magic strings (`Set.of("PENDED", "IN_REVIEW")`, `model/PriorAuthRequest.java:15`); there is no enum.
- `tenantId` is carried, but nothing is tenant-scoped (no filter by tenant) even though the POM describes the API as "pending requests per tenant".
- No auth, no input validation surface (the endpoint has no inputs), and no error handling beyond startup `IOException` propagation (fail-fast at boot, which is acceptable).
- No coverage tooling, so the express/feature coverage floors cannot be measured without adding a plugin. Any such addition must be declared in the plan per workspace rule.
- No TODO/FIXME/HACK comments; no `@SuppressWarnings`; no hard-coded secrets.

## Handoff Summary
- **Intent-relevant finding**: The pending list is built in `store/RequestStore.java:38-40` (`pending()` filters `PriorAuthRequest::isPending` over a list sorted by `receivedAt`, then `id`) and mapped per row in `api/PendingRequestResponse.java:15-18` (`from(PriorAuthRequest)`), returned by `api/PendingRequestsController.java:19-22`. That record (`id, tenantId, service, status, receivedAt`) is where a business-day `age` and an `over 5 business days` flag would be added. `receivedAt` is a `LocalDate` (`model/PriorAuthRequest.java:13`). No business-day or holiday logic, and no holiday list or config, exists in this repo.
- **Risks / follow-up**: (1) The rule must match the nightly report's ("weekends and our holidays do not count"), but that report's source and the org holiday list are outside this repo. Requirements must pin down the exact counting convention (whether the received day counts, how `> 5` versus `>= 5` is decided) and where holidays come from (config in `application.yml`, a classpath file, or a shared source). (2) Age depends on "today", so a `java.time.Clock` bean or an equivalent is needed for deterministic tests; the existing controller test asserts on sample data dated 2026-10-01..09. (3) Adding fields to `PendingRequestResponse` is additive to the JSON contract; the existing tests must remain green. (4) Adding any dependency (for example a holiday library or JaCoCo) must be declared in the plan (workspace rule).
