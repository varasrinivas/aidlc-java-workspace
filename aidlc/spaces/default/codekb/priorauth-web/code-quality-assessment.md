# Code Quality Assessment: priorauth-web

## Test Coverage

- 48 tests (counted by reading at `ddca232`, not executed in this scan): api 2, queue-filters 5, saved-filter-client 9, render 10, filter-session 22. One test file per `src/` module; tests carry US/FR/AC tags.
- Every `src/` module is tested; async ordering (late reads, quick changes, open save during Clear) is tested with a hand-driven fetch stub and no timers.
- Not tested: the `index.html` inline script (by team rule), any browser/DOM behaviour (focus after Clear, the button's live `disabled` state).
- Coverage tooling: absent. Coverage is NOT MEASURED (team-recorded exception for F1220, owned by Meena Iyer).
- Last recorded baseline in `team.md`: 6 of 6 at `65a999b` (pre-F1220); the current count is higher.

## Linting, Formatting, CI

- Linter / formatter: none; style is held by convention and review (`team.md` Code Style).
- CI: none in the repo. The workspace `scripts/verify.sh` (`scripts\verify.cmd`) runs `npm test --silent` and is the CI stand-in.

## Documentation

- `README.md`: short and useful (run, serve, page parameters, US5161/US5162 behaviour); its last two lines are stale (see below).
- Every `src/` file starts with a purpose comment naming story and contracts; inline comments cite FR/AC ids. No JSDoc, by convention.

## Quick Ratings

| Aspect | Rating | Note |
|---|---|---|
| Naming clarity | good | domain names (`loadQueueFor`, `filterIsSet`, `droppedTenant`) |
| Function size | good | all functions short; `filter-session.js` is the only larger module (161 lines) |
| Error handling | good | non-2xx and network errors surface as messages; off-contract answers rejected; nothing swallowed silently (failures become flags) |
| Test presence | good | every module, happy path plus edge cases |
| Duplication | fair | non-2xx handling three times, base trimming twice |
| Dead code | fair | `api.fetchPending` unused by the page |

## Technical Debt

1. `src/api.js` `fetchPending` is exported and tested but no longer used by the page.
2. The non-2xx check `priorauth-api answered <status>` is repeated in `api.js`, `queue-filters.js` and `saved-filter-client.js`; trailing-slash trimming in `api.js` and `saved-filter-client.js`.
3. `loadQueue` returns a `count` the page does not use (`countLabel(view.rows)` recomputes it).
4. `README.md` tail still says `main` / `v1.0.0` is the start of the guide with US5153 not built; `main` is now `v1.1.0` with US5153, US5161 and US5162.
5. Default API base `http://localhost:8080` is hard-coded in `index.html` (overridable).
6. No lint, coverage or CI.
7. No TODO/FIXME/HACK markers, no lint suppressions, no secrets found.

## Security Notes

- All rendered values go through `esc` (escapes `& < > " '`); tested with markup-bearing tenant ids.
- Reviewer id is `encodeURIComponent`-encoded into one path segment; tested.
- The reviewer id is a plain page parameter with no authentication: anyone with the link reads and writes that reviewer's filter (accepted and stated in release notes).
