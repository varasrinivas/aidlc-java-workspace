# Unit Test Instructions — F1220 US5163 (U4 `us5163-filter-history`, `priorauth-api`)

## Framework and Configuration

- JUnit 5, AssertJ and Spring MockMvc, all from the existing `spring-boot-starter-webmvc-test` (test scope). There is no new dependency and no new test configuration file.
- HTTP tests use `@SpringBootTest` with `@AutoConfigureMockMvc`. `DotReviewerIdTest` and `NewEndpointProtocolErrorTest` keep their real server (`webEnvironment = RANDOM_PORT`) and the JDK `HttpClient`.
- Contract examples live in `priorauth-api/src/test/resources/contract/f1220/`. The two C3 files are copied unchanged from the parent's `inception/contract-design/examples/`, and tests read them through the existing `ContractExamples` helper.

## How to Run This Story's Tests

From the workspace root, and only through the workspace verify script (team rule: tests never run ad hoc):

```
scripts\verify.cmd priorauth-api
```

(`scripts/verify.sh priorauth-api` on a POSIX shell.)

**Scope:** this story is the only unit of its intent and changes only `priorauth-api`. Naming the repo limits the run to this story's repo, and `priorauth-web` is not run. The verify script runs the repo's whole suite. That is deliberate: the team runs tests only through the verify script, and US5160's tests must stay green while the store changes underneath them. No narrower filter is allowed. US5160 used the same rule.

The script is already runnable before the first code change. Plan Step 2 runs it on the new branch to record the baseline, which includes all of US5160's tests.

**Reading the result:** the script's exit code is the pass/fail signal. Per-class counts are in `priorauth-api/target/surefire-reports/*.txt`.

## Test Scope (Minimal strategy plus the team's floors)

| Test class | Kind | Proves |
|---|---|---|
| `store/ReviewerFilterStoreTest` (changed) | unit, fresh store and `MutableClock` per test | AC1.4.1-AC1.4.7, FR7.5 limit check; US5160's 6 existing tests unchanged except their construction |
| `api/ReviewerFilterHistoryTest` (new) | MockMvc, own context (history limit 3, test clock) | AC1.4.1-AC1.4.6, AC1.4.8, AC1.4.9, contract C3 examples |
| `api/DotReviewerIdTest` (changed) | real server | A5: `.` and `..` on the history call answer 400 |
| `api/NewEndpointProtocolErrorTest` (changed) | real server | A2, NFR4: 405 and 406 on the history path have no body |

- Every new or changed test file has the happy path plus at least two error or edge cases. Every new branch has a test:
  - a save that writes a line, and a refused save that writes none
  - a history that is under the limit, and one at the limit
  - an empty history and a non-empty one
  - a valid id and an invalid one
  - a history limit that is valid, and one that is invalid
- Each test names the FR or AC it proves, in its name or in a comment on the `@Test`, as the existing tests do.
- No other existing test class changes, and all of them must keep passing (NFR8).

## Coverage Target

Line coverage is NOT MEASURED in F1220, under the team's recorded exception owned by Meena Iyer. No coverage tool is added. The 80% floor stays the target, and nothing here claims it is met.

## Mocking and Stubbing

- Nothing is mocked. The store is small, in-memory and deterministic, so tests use real instances.
- **Time:** the only stand-in is `MutableClock` (test sources), a `java.time.Clock` in UTC whose instant each test sets. The system clock is never read in a test (team rule Q7 C).
  - Unit tests pass it straight to `new ReviewerFilterStore(maxReviewers, maxHistoryLines, clock)`.
  - `ReviewerFilterHistoryTest` provides it as a `@Primary` `Clock` bean in a nested `@TestConfiguration` and sets its time before each save.
  - Shared-context classes keep the real `Clock.systemUTC()` bean. None of them checks a history time.

## Test Data

- **Independence (team rule Q7 B):**
  - `ReviewerFilterHistoryTest` has its own Spring context, so its store is its own.
  - Inside it, every test writes only its own reviewer ids, prefixed per test (for example `rfh-ac141`).
  - Only the C3 example test uses `rita.k`, the id in the example file.
  - In the shared-context classes, the new tests use their own ids (`rfc-405-history`, `rfc-406-history`).
- **Times:** the AC1.4.1 time is `2027-01-12T09:15:30.900Z`, expected as `2027-01-12T09:15:30Z`. The C3 example times are `09:15:30Z` and `09:20:05Z`. Same-second tests set the same second twice.
- **Limits:**
  - Unit level: a fresh store per test, with a history limit of 3 for AC1.4.6 and 1000 otherwise.
  - HTTP level: `ReviewerFilterHistoryTest`'s own context sets `max-history-lines=3` and `max-reviewers=50`.
  - Limits are never changed in the shared context.
- **Concurrency (AC1.4.7):** 50 tasks on a fixed thread pool, released together by a `CountDownLatch`, each saving a filter under `rfs-concurrent`. The store's history limit is 1000, so no line is dropped. The test waits with a timeout and fails if a task throws.
