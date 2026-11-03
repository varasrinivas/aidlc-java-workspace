# Unit Test Instructions: US5161 Open the screen with my last filter

## Framework and Configuration

- **Framework:** the Node built-in runner (`node --test`) with `node:assert/strict`. No test configuration file and no dependency is added (team practice).
- **Discovery:** `npm test` runs `node --test`, which finds every `*.test.js` file under `priorauth-web/test/`.
- **Node:** `package.json` asks for >=20; this machine has v24.19.0.

## How to Run This Story's Tests

This intent changes one repo, `priorauth-web`, and has no other unit, so the repo's suite is exactly this story's scope. Team practice runs tests only through the workspace verify script, with the repo named:

```
scripts\verify.cmd priorauth-web
```

On macOS or Linux, use `scripts/verify.sh priorauth-web`. Run it from the workspace root. It runs `npm test --silent` in `priorauth-web` and exits non-zero on any failure.

- **Before the first change:** this command is the baseline. Expected: 6 of 6 passing at `65a999b`.
- **After each test step (Steps 4, 6, 8, 10) and at Step 13:** every test passes, the 6 baseline tests included.

The test files are:

- `test/saved-filter-client.test.js` (new)
- `test/filter-session.test.js` (new)
- `test/queue-filters.test.js` (extended)
- `test/render.test.js` (extended)
- `test/api.test.js` (unchanged)

## Expected Coverage

- **Tests to write:** one or more for every requirement and acceptance criterion this story owns: AC1.2.1-AC1.2.12, FR4.7, FR4.8, FR4.9, A5 and R-06. Each new branch has a test.
- **Every new or changed test file:** covers the happy path and at least two error or edge cases.
- **Expected total:** about 28 new tests plus the 6 existing ones.
- **Line coverage:** not measured in F1220. Build and Test reports it as NOT MEASURED (the team's recorded exception).

## Mocking and Stubbing

- **No real network:** every call goes through an injected `fetchFn`, matching the existing tests.
- **Simple stubs:** return `{ ok, status, json: async () => body }`. A network failure is a stub that rejects.
- **Ordering tests (AC1.2.7, AC1.2.8, FR4.9):** use a stub that records each `(url, init)` and returns a promise the test resolves by hand. The test controls exactly when each answer arrives. No timers or sleeps.
- **Timeout:** tests check that each call's `init.signal` is an `AbortSignal`. They never wait 10 seconds.
- **No DOM:** `index.html` isn't loaded in tests (team practice). Markup criteria are checked on the strings `src/render.js` returns.

## Test Data

- **Contract examples** are copied byte for byte into `test/contract-examples/` from `261102-f1220-remember-filter/inception/contract-design/examples/`:
  - `c1-get-filter-saved.json`
  - `c1-get-filter-nothing-saved.json`
  - `c1-put-filter-request.json`
  - `c2-get-tenants.json`

  Tests read them with `node:fs`. When an example changes in the parent, its copy and the tests change with it.
- **Independent tests:** each session test creates its own session with its own reviewer id (for example `t-restore`, `t-quick`), so no state is shared.
- **Story tags:** test names are behaviour sentences that carry the story tag, for example `"a change before the saved filter arrives wins (US5161 AC1.2.8)"`.
