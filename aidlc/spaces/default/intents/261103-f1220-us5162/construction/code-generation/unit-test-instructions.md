# Unit Test Instructions: US5162 Clear my filters

## Framework and Configuration

- **Framework:** the Node built-in runner (`node --test`) with `node:assert/strict`. No test configuration file and no dependency is added (team practice).
- **Discovery:** `npm test` runs `node --test`, which finds every `*.test.js` file under `priorauth-web/test/`.
- **Node:** `package.json` asks for version 20 or later.

## How to Run This Story's Tests

This intent changes one repo, `priorauth-web`, and has no other unit, so the repo's suite is exactly this story's scope. Team practice runs tests only through the workspace verify script, with the repo named. Run it from the workspace root:

```
scripts\verify.cmd priorauth-web
```

On macOS or Linux, use `scripts/verify.sh priorauth-web`. It runs `npm test --silent` in `priorauth-web` and exits non-zero on any failure.

- **Before the first change (plan Step 1):** this command is the baseline on `f1220/us5162-clear-filters` at `origin/feature/F1220`. The count goes in `code-summary.md`; reading the files gives 38.
- **After each test step (plan Steps 4 and 6) and at Step 9:** every test passes, the baseline tests included. The one exception is the US5161 FR4.8 test, which this story changes on purpose (FR4.10).

The test files this story touches:

- `test/filter-session.test.js` (changed: the FR4.8 test, plus the new Clear and FR4.10 tests)
- `test/render.test.js` (extended: the Clear button and `filterIsSet`)

Unchanged: `test/saved-filter-client.test.js`, `test/queue-filters.test.js` and `test/api.test.js`.

## Expected Coverage

- **Tests to write:** at least one for each requirement and criterion this story owns that can be automated: AC1.3.1, AC1.3.2, AC1.3.3, AC1.3.4, AC1.3.6, FR6.2 (`filterIsSet`), FR4.10 and A2. Each new branch has a test.
- **Manual check:** AC1.3.5 (focus moves to the Tenant picker after Clear) and keyboard use of the button are listed for the feature's Build and Test, because the team has no browser tests.
- **Every changed test file:** covers the happy path and at least two error or edge cases.
- **Expected total:** about 10 new or changed tests, plus the baseline.
- **Line coverage:** not measured in F1220. Build and Test reports it as NOT MEASURED (the team's recorded exception).

## Mocking and Stubbing

- Reuse `filter-session.test.js`'s `manualApi()` stub and `session()`/`opened()` helpers. Every call goes through an injected `fetchFn`, the test answers each call by hand, and there are no timers or sleeps.
- **AC1.3.6:** leave the first PUT (TX-01) unanswered, call `clear()`, then answer both PUTs in order and check the PUT bodies.
- **No DOM:** `index.html` isn't loaded in tests (team practice). Markup criteria are checked on the strings `src/render.js` returns.

## Test Data

- Use the existing contract examples in `test/contract-examples/` (`c1-get-filter-saved.json`, `c2-get-tenants.json`, and the rest). No example changes.
- **Independent tests:** each session test uses its own reviewer id, for example `t-clear`, `t-clear-fails`, `t-clear-open-save` and `t-dropped-off`.
- **Story tags:** test names are behaviour sentences that carry the story tag, for example `"Clear resets both filters, shows the whole queue and saves the cleared filter (US5162 AC1.3.1)"`.
