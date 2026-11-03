# Unit Test Instructions — F1220 US5160 (U1 `us5160-save-filter`, `priorauth-api`)

## Framework and Configuration

- JUnit 5 (including `@ParameterizedTest`), AssertJ and Spring MockMvc. All come from the existing `spring-boot-starter-webmvc-test` (test scope). There is no new dependency and no new test configuration file.
- HTTP tests use `@SpringBootTest` with `@AutoConfigureMockMvc`, as the existing `PendingRequestsControllerTest` does.
- The one exception is `DotReviewerIdTest`, which uses `webEnvironment = RANDOM_PORT` and the JDK's `java.net.http.HttpClient`. The server's path normalisation for `.` and `..` only happens on a real server.
- Contract examples live in `priorauth-api/src/test/resources/contract/f1220/`. They are copied unchanged from the parent's `inception/contract-design/examples/` and read through the `ContractExamples` test helper.

## How to Run This Story's Tests

From the workspace root, and only through the workspace verify script (team rule: tests never run ad hoc):

```
scripts\verify.cmd priorauth-api
```

(`scripts/verify.sh priorauth-api` on a POSIX shell.)

**Scope:** this story is the only unit of its intent and changes only `priorauth-api`. Naming the repo limits the run to this story's repo, and `priorauth-web` is not run. The verify script runs the repo's whole suite. That is deliberate: the team runs tests only through the verify script, and the existing queue tests must stay green with the new sample row (NFR8). No narrower filter is allowed.

The script is already runnable before the first code change. Step 2 of the plan runs it to record the baseline, which is expected to be 12 tests passing.

**Reading the result:** the script's exit code is the pass/fail signal. Per-class counts are in `priorauth-api/target/surefire-reports/*.txt`.

## Test Scope (Minimal strategy plus the team's floors)

| Test class | Kind | Proves |
|---|---|---|
| `store/ReviewerFilterStoreTest` (new) | unit, fresh store per test | AC1.1.1-1.1.3, AC1.1.8, AC1.1.9, FR1.5, NFR7 |
| `store/TenantDirectoryTest` (new) | unit | AC1.1.5, AC1.1.11, A4 |
| `store/RequestStoreTest` (changed) | unit | FR3.2 |
| `api/ReviewerIdsTest` (new) | unit | AC1.1.7 |
| `api/SavedFilterBodyTest` (new) | unit | AC1.1.4-1.1.6, FR1.6, NFR3 |
| `api/ReviewerFilterControllerTest` (new) | MockMvc, shared context | AC1.1.1-1.1.8, AC1.1.10 |
| `api/ReviewerFilterContractTest` (new) | MockMvc, shared context | contract C1 cases and bodies |
| `api/TenantsControllerTest` (new) | MockMvc, shared context | AC1.1.11, AC1.1.13, contract C2 |
| `api/BrowserAccessPolicyTest` (new) | MockMvc plus a static check | AC1.1.12, contract C5 |
| `api/ReviewerLimitHttpTest` (new) | MockMvc, own context, limit 2 | AC1.1.9 |
| `api/DotReviewerIdTest` (new) | real server, own context | AC1.1.7 (`.` and `..`) |
| `api/NewEndpointProtocolErrorTest` (new, plan Step 12) | real server, own context | NFR4, AC1.1.10: 405/406 on the new endpoints have no body; queue errors unchanged (AC1.1.13) |
| `api/PendingRequestsControllerTest` (changed) | MockMvc | FR3.2, AC1.1.13 |
| `api/TenantFilterTest` (changed) | MockMvc | FR3.2, FR3.3, AC1.1.13 |

- Every new or changed test file has the happy path plus at least two error or edge cases. Every new branch (each check in the fixed order, each refusal) has a test.
- Each test names the FR or AC it proves, in its name or in a comment on the `@Test`, as the existing tests do.
- `OverLimitFilterTest` is not changed and must keep passing.

## Coverage Target

Line coverage is NOT MEASURED in F1220, under the team's recorded exception owned by Meena Iyer. No coverage tool is added. The 80% floor stays the target, and nothing here claims it is met.

## Mocking and Stubbing

- Nothing is mocked. The store and directory are small, in-memory and deterministic, so tests use real instances.
  - Unit tests construct `new ReviewerFilterStore(n)` directly with a small limit.
  - `TenantDirectoryTest` uses a real `RequestStore` over the packed sample.
- No test needs a clock in this story. The history and its injected `Clock` are US5163's.

## Test Data

- **The packed sample export** (`requests.sample.json`) now has 5 requests across 2 tenants. The new row is `PA-10270`, tenant `NM-02`, `PENDED`, received `2026-10-12`.
- **Independence (team rule):**
  - In shared Spring contexts every test writes only its own reviewer ids, prefixed per test (for example `rfc-ac111`).
  - Only `ReviewerFilterContractTest` writes the reviewer ids that appear in the contract files (`rita.k`), and it asserts no state that another test writes.
- **Limit tests:**
  - Unit level: a fresh store instance per test.
  - HTTP level: `ReviewerLimitHttpTest` has its own context (`priorauth.reviewer-filter.max-reviewers=2`). Limits are never changed in the shared context.
- **Byte-exact bodies:** the 1,024-byte and 1,025-byte bodies are built in the test by padding a valid body with spaces and checking its UTF-8 length.
