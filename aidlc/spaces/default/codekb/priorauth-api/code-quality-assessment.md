# Code Quality Assessment: priorauth-api

Full rescan of `main` at `0e00544` (tag `v1.2.0`), 2026-11-03. The test suite was not run in this scan; counts are from reading the code.

## Quick Assessment

| Aspect | Rating | Evidence |
|---|---|---|
| Naming clarity | good | Domain names (`AgeBadge`, `TenantDirectory`, `ReviewerFilterStore`); test methods are behaviour sentences |
| Function size | good | Every main method is under 30 lines; the longest (`PendingRequestsController.pending`, `SavedFilterBody.toFilter`) are about 12-15 |
| Error handling | good (new endpoints), fair (queue, holidays) | Fixed, input-free error bodies on the new endpoints; see TD-2, TD-5 |
| Test presence | good | Every main class with logic has direct or HTTP tests; `HolidayCalendar` only indirectly |
| Duplication | fair | Request helpers (`save`, `assertError`) repeated across HTTP test classes; acceptable for test readability |
| Dead code | good | No unused classes, commented-out blocks, TODO/FIXME/HACK or `@SuppressWarnings` |

## Tests

- 18 test classes, 90 test methods (81 `@Test`, 9 `@ParameterizedTest`), 118 executions. The last recorded run was 118/118 at `d1d11a5` (F1220 Build and Test); not rerun here.
- Frameworks: JUnit 5, AssertJ, MockMvc; two real-server classes (`RANDOM_PORT`) for Tomcat path handling and default error bodies.
- Strengths: contract fixtures replayed byte-for-byte as JSON trees; a test clock (`MutableClock`) for every checked time; a 50-thread concurrency test for the save-and-history atomicity; per-class reviewer-id prefixes and separate contexts for non-default limits keep tests order-independent.
- Gaps: no direct `HolidayCalendar` test (missing file, unreadable file); no test for malformed `asOf` / `overLimit` query values on `GET /requests/pending`; `RequestFilter` is tested only through HTTP.

## Coverage, Linting, CI

- **Coverage**: no tool configured (no JaCoCo). Reported as NOT MEASURED; the 80% floor is a recorded team exception owned by Meena Iyer.
- **Linting / formatting**: none; style is kept by convention and review (team `Code Style`).
- **CI/CD**: none in the repo; the workspace verify script run before each PR is the stand-in.
- **Documentation**: `README.md` is current for all five endpoints and the four configuration keys; class Javadoc names FR/US/ADR; no OpenAPI document.

## Technical Debt

| ID | Location | Signal | Impact |
|---|---|---|---|
| TD-1 | `aging/HolidayCalendar.java:35`; `data/` | Holiday file name hard-codes `-2026`; only TX-01 has a file | From 2027-01-01 (F1220 ships 2027.Q1) holidays are ignored, so ages and over-limit flags can be too high; NM-02 never has holidays |
| TD-2 | `aging/HolidayCalendar.java:42` | `root.get("holidays")` not null-checked | A malformed holiday file gives a `NullPointerException` (500), not the documented `IllegalStateException` |
| TD-3 | `api/PendingRequestsController.java:36` | Default as-of uses `LocalDate.now()` (system clock and default zone), not the `Clock` bean | Default date is untestable and depends on the server's time zone |
| TD-4 | `store/ReviewerFilterStore.java:29-32` | Defaults allow 10,000 reviewers x 1,000 lines = 10 million `HistoryLine`s | Bounded, but not sized against a heap limit; a flood of saves from many ids can exhaust memory |
| TD-5 | `api/RequestFilter.java:6` | `tenant` query value on the queue is not validated or size-limited | Predates the team's security checklist; harmless today (exact-match compare only) |
| TD-6 | whole API | No authentication or authorization | Anyone who can reach the API can read or overwrite any reviewer's filter and history; accepted for F1220 and stated in the release notes |
| TD-7 | `store/ReviewerFilterStore.java` | In-memory only, single instance | Filters and history lost on restart; cannot scale out |
| TD-8 | `api/DotReviewerIdTest.java:53` | `System.out.println` diagnostic in a test | Noise in test output only |
| TD-9 | `pom.xml` | No Maven wrapper, coverage, linter or CI | Build depends on a locally installed Maven; quality gates are manual |

## Security Checklist (team, at code-plan review)

| Check | State |
|---|---|
| Every request value validated and size-limited | New endpoints yes (id regex, 1,024-byte body, exact shape); queue query values no (TD-5) |
| No file path or cache key built from a caller's value | Yes: `HolidayCalendar` builds its path from export tenant ids only; the store is keyed by validated reviewer ids |
| Error responses carry no stack traces or raw caller input | New endpoints yes (fixed bodies, 405/406 bodiless); the queue keeps Spring Boot's default body, which includes the path |
| CORS named origins only, never `*` | Yes, enforced at start-up |
| Escaping before display | n/a in this repo (done in `priorauth-web`) |
