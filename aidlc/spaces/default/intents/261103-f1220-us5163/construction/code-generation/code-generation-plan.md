# Code Generation Plan — F1220 US5163 Filter history (U4 `us5163-filter-history`)

## Summary

- Builds: one history line per successful save, written inside the store's existing lock, and `GET /reviewers/{reviewerId}/filter/history` (newest first, capped per reviewer), in `priorauth-api` only
- Touches: new `model/HistoryLine` and `api/HistoryLineResponse`; changes `store/ReviewerFilterStore`, `api/ReviewerFilterController`, `PriorAuthApiApplication` (a `Clock` bean), `application.yml` and `README.md`; changes 3 test classes and adds 2 test files plus 2 contract examples
- Tests: about 25 JUnit 5 / MockMvc tests: about 9 new store unit tests, about 11 in a new HTTP class with its own context and test clock, and 3 added to existing real-server tests; run only through `scripts\verify.cmd priorauth-api`

## Scope and Inputs

- **Story:** US1.4 (Rally US5163), AC1.4.1-AC1.4.9, in the parent's `inception/user-stories/stories.md`.
- **Requirements:** this intent's `inception/requirements-analysis/requirements.md`: FR7.1-FR7.6, FR1.5, NFR2, NFR4, NFR6, NFR7, NFR9, NFR11 and assumptions A1-A7.
- **Contract (wins over the story's wording):** the parent's `inception/contract-design/contract-summary.md`, C3 and C6, plus the `.`/`..` change of 2026-11-03 and `examples/c3-get-history*.json`.
- **Code it builds on:** US5160 on `origin/feature/F1220` at 2dbc68b (`ReviewerFilterStore`, `ReviewerFilterController`, `ReviewerIds`, `NewEndpointErrorHandler`, `NewEndpointProtocolErrorHandler`, `BrowserAccessPolicy`). The code knowledge base is in `aidlc/spaces/default/codekb/priorauth-api/`.
- **Repo and branch:** `priorauth-api` only. The branch is `f1220/us5163-filter-history`, cut from a freshly fetched `origin/feature/F1220`. US5160, which this story depends on, is already merged there. The PR goes into `feature/F1220`.
- **No new dependency.** `java.time.Clock`, `java.util.ArrayDeque` and `java.util.concurrent` come from the JDK. Tests use JUnit 5, AssertJ, MockMvc and the JDK `HttpClient`, all of which are already present. `pom.xml` is not changed.
- **Not in this story:** any screen change (FR7.6), a durable store, sign-in, and the release-notes line (Meena Iyer).

## Design Decisions This Plan Settles

1. **The line is written inside the existing lock (NFR2, C6, ADR-001).**
   - `ReviewerFilterStore.save` already runs inside `synchronized (lock)`. After `filters.put(...)`, the same block appends the history line.
   - A save refused for the reviewer limit returns before `put` and writes no line.
   - Requests refused for an invalid id, an invalid body or an unknown tenant never reach the store, because the controller checks them first. So no line is written for them either (FR7.2).
   - `put` and the append cannot fail part-way in normal operation, because both are in-memory operations on plain collections. There is no separate commit step that could leave a save without its line.
2. **Store shape.**
   - `Map<String, ArrayDeque<HistoryLine>> history`, keyed by reviewer id.
   - The newest line goes first (`addFirst`). When the deque passes the limit, the oldest line is removed (`removeLast`) (FR7.5).
   - A same-second save is added in front of the earlier one, so lines with the same `at` keep save order, newest first (FR7.3).
   - `history(reviewerId)` returns `List.copyOf(deque)`, or `List.of()` when the reviewer has none. It uses `get`, never `computeIfAbsent`, so a read adds no entry and takes no slot (FR7.4, FR1.4).
   - The deque is created on the first successful save. The map therefore holds at most `maxReviewers` keys, the same set as `filters`.
3. **Time (FR7.1, NFR9, A3).**
   - The store takes a `java.time.Clock` in its constructor. `at = clock.instant().truncatedTo(ChronoUnit.SECONDS)`, which cuts the time and does not round it.
   - `PriorAuthApiApplication` gets one `@Bean Clock clock()` that returns `Clock.systemUTC()`. This is the smallest place to put it, and it adds no new configuration class.
   - Tests use their own clock: a small test-only `MutableClock`, whose time each test sets.
4. **History limit setting (A1).**
   - The store's constructor gains `@Value("${priorauth.reviewer-filter.max-history-lines:1000}") int maxHistoryLines`, next to `max-reviewers`.
   - A value below 1 is refused with `IllegalArgumentException`, and the message names the value. This matches `max-reviewers`.
   - The key and its default go into `application.yml` with a comment naming US5163 FR7.5.
5. **Domain and response records (team Code Style).**
   - `model/HistoryLine(Instant at, String reviewer, String tenant, boolean overLimit)`, a domain record.
   - `api/HistoryLineResponse(String at, String reviewer, String tenant, boolean overLimit)`, with `static from(HistoryLine)`. `at` is `Instant.toString()` of the truncated instant, for example `2027-01-12T09:15:30Z` (C3).
   - The controller returns `List<HistoryLineResponse>` and never returns the domain record.
   - A `null` tenant is written as `null`, as `SavedFilterResponse` already does.
6. **The endpoint (C3, A2, A5).**
   - `@GetMapping("/reviewers/{reviewerId}/filter/history")` in `ReviewerFilterController`. It calls `ReviewerIds.requireValid` first, then `store.history(id)`, then maps each line.
   - An invalid id, including `.` and `..`, answers `400 invalid-reviewer-id` through the existing `NewEndpointErrorHandler`.
   - Other methods answer 405, and an `Accept` that excludes JSON answers 406. `NewEndpointProtocolErrorHandler` covers `/reviewers/**`, so both answers have no body.
   - CORS already covers `/reviewers/**` (C5). No error-handling or CORS code changes.
7. **Memory ceiling at the defaults (NFR7, which the parent left for this story to state).**
   - At most 10,000 reviewers × 1,000 lines = 10,000,000 lines.
   - Each line costs about 64 bytes: the `HistoryLine` object (about 32 bytes), its `Instant` (about 24 bytes) and one deque slot (8 bytes).
   - The reviewer and tenant strings are shared, not copied. The line reuses the id string already used as the map key, and the tenant string is the directory's own instance.
   - That is about 640 MB in the worst case. The parent's NFR7 accepted the line count, and A6 (accepted) adds no further cap. The byte figure is raised here for the mob, as a risk for running with the defaults: see Risks.
8. **Security checklist (team Code Style, Q11).**
   - The only request value is the reviewer id, checked by `ReviewerIds.requireValid` (1-64 characters, a fixed character set).
   - The response is JSON data, and escaping it is the screen's job. No screen change is in this story.
   - No file path or cache key is built from the id. It is used only as a map key.
   - Errors use the fixed `{error, message}` bodies, with no stack trace and no caller input.
   - CORS allows named origins only, unchanged from US5160.

## Steps

Each step names the requirement it implements. The developer ticks each box when the step is done. Methodology: test-after, layer by layer (Testing Contract below).

- [x] **Step 1: Story branch (project structure).** Run `scripts\pull-all.ps1`, then `git -C priorauth-api fetch origin` and `git -C priorauth-api switch -c f1220/us5163-filter-history origin/feature/F1220`. Confirm `HEAD` is `origin/feature/F1220`, and that US5160 (`cb1aee7`, `4b63a4e`) is in its history. (Team Way of Working)
- [x] **Step 2: Test runner and baseline.** Run `scripts\verify.cmd priorauth-api` on the new branch before any change, and record in `code-summary.md` the exit code and the total test count from `priorauth-api/target/surefire-reports/*.txt`. A non-zero exit stops the build: report it, and change nothing. (Team Testing Posture Q7 A; NFR8)
- [x] **Step 3: Data model, implement.** Add `src/main/java/com/acmehealth/priorauth/model/HistoryLine.java`, a record with a one-line purpose Javadoc naming US5163 FR7.1. It has no logic, so it gets no test of its own; Step 7 tests it through the store. (FR7.1)
- [x] **Step 4: Store, implement.** Change `src/main/java/com/acmehealth/priorauth/store/ReviewerFilterStore.java` as Decisions 1-4 describe:
  - The constructor becomes `(int maxReviewers, int maxHistoryLines, Clock clock)`, and both limits are checked.
  - `save` appends the line inside the lock after `put`.
  - New method `history(String reviewerId)`.
  - The class Javadoc names US5163 FR7, NFR2 and NFR7.
  - `save` and `read` keep their meaning and signatures (C6).

  (FR7.1-FR7.5, FR1.5, NFR2, NFR7)
- [x] **Step 5: Clock bean.** Add `@Bean Clock clock()`, returning `Clock.systemUTC()`, to `src/main/java/com/acmehealth/priorauth/PriorAuthApiApplication.java`, with a one-line comment naming US5163 NFR9. (NFR9, A3)
- [x] **Step 6: Configuration.** Add `max-history-lines: 1000` under `priorauth.reviewer-filter` in `src/main/resources/application.yml`, with a comment: `# US5163 FR7.5: newest history lines kept per reviewer (in memory); older ones are dropped`. (FR7.5, A1)
- [x] **Step 7: Store, write and run its tests.**
  - Add `src/test/java/com/acmehealth/priorauth/MutableClock.java`, a test-only `Clock` whose instant a test sets. It is UTC and has no system time.
  - Change `src/test/java/com/acmehealth/priorauth/store/ReviewerFilterStoreTest.java`. The existing 6 tests construct the store through a helper `store(maxReviewers)`, which passes a history limit of 1000 and a `MutableClock`; their assertions stay unchanged.
  - Add these tests:
    - AC1.4.1: the clock at `2027-01-12T09:15:30.900Z` gives the exact line `2027-01-12T09:15:30Z` with `rita.k`, `TX-01` and `true` (cut, not rounded).
    - AC1.4.2: a repeated save and a clear each add a line (3 lines in total).
    - AC1.4.3: a save refused for the reviewer limit adds no line, and the history reads as before.
    - AC1.4.4: three saves, two in the same second, come back newest first, and the same-second pair keeps save order.
    - AC1.4.5: a never-saved reviewer reads `[]`, and with `maxReviewers = 1` another reviewer can still save afterwards, so the read took no slot.
    - AC1.4.6: with a limit of 3, five saves leave exactly the 3 newest lines.
    - AC1.4.7: 50 threads save at once (a `CountDownLatch` start gate). The history has exactly 50 lines, and `read` equals the newest line's tenant and switch.
    - A history limit below 1 is refused, and the message names the value.
    - The history is case-sensitive by reviewer id.
  - Run `scripts\verify.cmd priorauth-api`. All tests pass.

  (AC1.4.1-AC1.4.7, NFR9)
- [x] **Step 8: API, implement.**
  - Add `src/main/java/com/acmehealth/priorauth/api/HistoryLineResponse.java`, a record with `static from(HistoryLine)` and a Javadoc naming US5163 / C3.
  - Add the `GET /reviewers/{reviewerId}/filter/history` method to `src/main/java/com/acmehealth/priorauth/api/ReviewerFilterController.java`, with a comment naming US5163 FR7.3 and FR7.4.
  - Add US5163 / C3 to the class Javadoc.

  (FR7.3, FR7.4, FR7.6, A2)
- [x] **Step 9: API, write and run its tests.**
  - Copy `c3-get-history.json` and `c3-get-history-empty.json` unchanged from the parent's `inception/contract-design/examples/` into `src/test/resources/contract/f1220/`. (A4)
  - Add `src/test/java/com/acmehealth/priorauth/api/ReviewerFilterHistoryTest.java`.
    - Setup: `@SpringBootTest(properties = {"priorauth.reviewer-filter.max-history-lines=3", "priorauth.reviewer-filter.max-reviewers=50"})` with `@AutoConfigureMockMvc` and a nested `@TestConfiguration` that provides a `@Primary` `MutableClock` bean. That gives the class its own context and its own store, so no other test class sees its data (NFR9, team rule Q7 B).
    - Tests:
      - AC1.4.1: the exact JSON line over HTTP.
      - AC1.4.2: a repeat and a clear add lines.
      - AC1.4.3: an invalid body, an unknown tenant and an invalid reviewer id each answer their error and leave the history unchanged.
      - AC1.4.4: newest first over HTTP.
      - AC1.4.5: `[]` for a never-saved id, and `400` with the fixed `invalid-reviewer-id` body for a malformed id.
      - AC1.4.6: a limit of 3 over HTTP.
      - AC1.4.8: the error body equals `error-invalid-reviewer-id.json` exactly and does not contain the submitted id.
      - AC1.4.9: the history is served at `/reviewers/{id}/filter/history`.
      - C3 example: `rita.k` saves `TX-01`/`true` at `09:15:30.9Z` and then clears at `09:20:05Z`. The history equals `c3-get-history.json`. A never-saved id equals `c3-get-history-empty.json`.
    - Each test uses its own reviewer ids. `rita.k` is used only by the C3 example test.
  - Change `src/test/java/com/acmehealth/priorauth/api/DotReviewerIdTest.java`:
    - Add a test that `GET /reviewers/./filter/history` and `GET /reviewers/../filter/history` answer `400` with the fixed body (A5).
    - Update the class Javadoc's last sentence. The answer is now the contract's (contract change 2026-11-03), not a difference from it.
  - Change `src/test/java/com/acmehealth/priorauth/api/NewEndpointProtocolErrorTest.java`. Add a test that `PUT` and `POST` on `/reviewers/rfc-405-history/filter/history` answer 405 with no body, and `/reviewers/rfc-406-history/filter/history` with a non-JSON `Accept` answers 406 with no body. (A2, NFR4)
  - Run `scripts\verify.cmd priorauth-api`. All tests pass.

  (AC1.4.1-AC1.4.6, AC1.4.8, AC1.4.9, NFR4)
- [x] **Step 10: Documentation.**
  - In `priorauth-api/README.md`, add one line after the filter line describing the history call: `GET /reviewers/{reviewerId}/filter/history` gives that reviewer's saved filters, newest first, as `{"at", "reviewer", "tenant", "overLimit"}`. Add `priorauth.reviewer-filter.max-history-lines` (default 1000) to the settings line.
  - Add a line saying this was changed by AI-DLC intent `f1220-us5163`, next to the US5160 line.

  (FR7.6; Code Style)
- [x] **Step 11: Final verify.** Run `scripts\verify.cmd priorauth-api` on the branch. Record the exit code and the total test count against the Step 2 baseline in `code-summary.md`. (Project Mandated: verify before done)
- [x] **Step 12: Commit.** Commit every changed file on `f1220/us5163-filter-history` in `priorauth-api` as one commit: `US5163 audit every filter change: history line per save and GET .../filter/history (intent f1220-us5163)`. Do not push and do not open a PR; Arjun Nair does that. (Team Way of Working)

## Files

| File | Change | Step |
|---|---|---|
| `src/main/java/com/acmehealth/priorauth/model/HistoryLine.java` | new | 3 |
| `src/main/java/com/acmehealth/priorauth/store/ReviewerFilterStore.java` | changed | 4 |
| `src/main/java/com/acmehealth/priorauth/PriorAuthApiApplication.java` | changed (Clock bean) | 5 |
| `src/main/resources/application.yml` | changed (one key) | 6 |
| `src/test/java/com/acmehealth/priorauth/MutableClock.java` | new (test helper) | 7 |
| `src/test/java/com/acmehealth/priorauth/store/ReviewerFilterStoreTest.java` | changed | 7 |
| `src/main/java/com/acmehealth/priorauth/api/HistoryLineResponse.java` | new | 8 |
| `src/main/java/com/acmehealth/priorauth/api/ReviewerFilterController.java` | changed | 8 |
| `src/test/resources/contract/f1220/c3-get-history.json`, `c3-get-history-empty.json` | new (copied) | 9 |
| `src/test/java/com/acmehealth/priorauth/api/ReviewerFilterHistoryTest.java` | new | 9 |
| `src/test/java/com/acmehealth/priorauth/api/DotReviewerIdTest.java` | changed | 9 |
| `src/test/java/com/acmehealth/priorauth/api/NewEndpointProtocolErrorTest.java` | changed | 9 |
| `README.md` | changed | 10 |

No other file changes. `NewEndpointErrorHandler`, `NewEndpointProtocolErrorHandler`, `BrowserAccessPolicy`, `ReviewerIds` and `pom.xml` stay as they are.

## Story-to-Step Traceability

| ID | Steps |
|---|---|
| FR7.1 / AC1.4.1, AC1.4.2 | 3, 4, 5, 7, 9 |
| FR7.2 / AC1.4.3 | 4, 7, 9 |
| FR7.3 / AC1.4.4 | 4, 7, 8, 9 |
| FR7.4 / AC1.4.5 | 4, 7, 8, 9 |
| FR7.5 / AC1.4.6, NFR7 | 4, 6, 7, 9 |
| FR1.5, NFR2 / AC1.4.7 | 4, 7 |
| NFR4 / AC1.4.8 | 8, 9 |
| FR7.6 / AC1.4.9 | 8, 9, 10 |
| NFR9 | 5, 7, 9 |

## Risks

- **Memory at the defaults:** about 640 MB worst case for history (Decision 7). The parent accepted the 10,000,000-line bound, but the byte figure is new. If the mob wants a lower default for `max-history-lines`, that is a change to the parent's FR7.5 / C3 ("up to the newest 1,000 lines"), and it goes to Meena Iyer.
- **One lock for all saves (ADR-001):** a history append makes each save slightly longer under the lock. It is still a constant-time operation.
- **Existing store tests change:** only their constructor calls change, through one helper. Their assertions stay unchanged.

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

Layers that don't apply: the frontend layer (this is an API-only story, FR7.6). There is no database: the store is in memory, so the data-access layer is the store (Steps 4 and 7). The business logic lives in the store and the controller's checks, so it has no separate layer.
