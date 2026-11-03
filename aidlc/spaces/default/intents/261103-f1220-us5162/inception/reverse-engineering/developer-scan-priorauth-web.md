# Developer Code Scan: priorauth-web

Repo: `priorauth-web` at `ddca232bb3bbeaa76d57ab12a83648710ee64adb` (`main`, tag `v1.1.0`, clean working tree). Full rescan of `./`.

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `./` (every tracked file, 18 in total)
  - `index.html`
  - `package.json`, `README.md`, `.gitignore`
  - `src/api.js`, `src/queue-filters.js`, `src/saved-filter-client.js`, `src/filter-session.js`, `src/render.js`
  - `test/api.test.js`, `test/queue-filters.test.js`, `test/saved-filter-client.test.js`, `test/filter-session.test.js`, `test/render.test.js`
  - `test/contract-examples/` (4 JSON examples for contracts C1 and C2)
- **Skimmed only**: none (the repo is small enough to read in full)
- **Left out**:
  - `node_modules/` (gitignored; not present in the tracked tree, not opened)
  - `.git/`

### Packages Found
- `priorauth-web` 1.1.0 — single private package, browser page plus DOM-free ES modules — JavaScript (ES2022+, `"type": "module"`) — the reviewer screen: the pending prior-authorization queue read from `priorauth-api`, with tenant / over-limit filters that are remembered per reviewer (US5161) and can be cleared (US5162).

### Build System
- **Type**: npm (scripts only); no build step, no bundler, no transpiler.
- **Config Files**: `package.json` (`scripts.test = "node --test"`, `engines.node >= 20`), `.gitignore` (`node_modules/`).
- **Build Dependencies**: none. Zero `dependencies` and zero `devDependencies`. Serving is done ad hoc with `npx serve@14 . -l 3000` (README; pinned per Build and Test finding F-4).
- Internal module graph (no cycles):
  - `index.html` -> `src/filter-session.js`, `src/render.js`
  - `src/filter-session.js` -> `src/queue-filters.js`, `src/saved-filter-client.js`
  - `src/queue-filters.js` -> `src/api.js`
  - `src/saved-filter-client.js` -> (none)
  - `src/render.js` -> (none)
  - `src/api.js` -> (none)

### APIs Discovered
- HTTP client of `priorauth-api` — `src/api.js`, `src/queue-filters.js`, `src/saved-filter-client.js` — 4 endpoint/method pairs consumed:
  - `GET /requests/pending[?asOf=&tenant=&overLimit=true]` (queue; C4 per `filter-session.js` header)
  - `GET /reviewers/{reviewerId}/filter` (C1 read; `{}` or `{tenant: string|null, overLimit: boolean}`)
  - `PUT /reviewers/{reviewerId}/filter` body exactly `{"tenant", "overLimit"}` (C1 write; 204 expected)
  - `GET /tenants` (C2; array of tenant id strings)
- Page parameters (the screen's own input surface) — `index.html` — 2: `?api=` (default `http://localhost:8080`), `?reviewer=`.
- JS module exports (internal API) — `src/` — 16 named exports (see code-structure / api-documentation).
- No server endpoints exposed; the repo is static files only.

### Frameworks & Libraries
- Node.js — `>=20` (engines) — test runtime only; uses `node:test`, `node:assert/strict`, `node:fs`.
- Browser platform APIs — n/a — `fetch`, `URL`, `URLSearchParams`, `AbortSignal.timeout` (10 s per call), `encodeURIComponent`.
- `serve` — `@14` via `npx` (not a declared dependency) — local static server for the demo.
- No UI framework.

### Test Coverage
- **Test Directories**: `test/` (one `<module>.test.js` per `src/` module) and `test/contract-examples/`.
- **Test Frameworks**: Node built-in runner (`node --test`) with `node:assert/strict`; network stubbed by injected `fetchFn` (a hand-driven `manualApi()` stub in `filter-session.test.js`, no timers).
- **Test count (by reading, not run)**: 48 tests — api 2, queue-filters 5, saved-filter-client 9, render 10, filter-session 22. Tests carry US/FR/AC tags in their names.
- **Coverage Config**: absent (team recorded exception: coverage NOT MEASURED in F1220).
- `index.html` inline script is untested (by team rule, it holds only DOM wiring); no browser/DOM tests.

### Code Quality Indicators
- **Linting**: none (no ESLint/Prettier config; style held by convention per `team.md`).
- **CI/CD**: none (no `.github/workflows` or other pipeline file). The workspace `scripts/verify.sh` / `scripts\verify.cmd` is the CI stand-in.
- **Documentation**: `README.md` present and short (run, serve, page parameters). Every `src/` file has a line-1 purpose comment naming the story and contracts; inline comments cite FR/AC/assumption ids. No JSDoc (by convention).

### Technical Debt Signals
- `src/api.js` `fetchPending` is exported and tested but no longer called by the page (the queue goes through `queue-filters.js` `loadQueue`, which duplicates its non-2xx handling). Candidate dead code.
- Non-2xx handling (`priorauth-api answered <status>`) is written three times: `api.js`, `queue-filters.js`, `saved-filter-client.js` (`answered`). Base-URL trailing-slash trimming is written twice (`api.js` inline, `saved-filter-client.js` `trimBase`).
- `README.md` bottom lines are stale: they describe `main` / `v1.0.0` as "US5153 not built yet", but `main` is now `v1.1.0` with US5153, US5161 and US5162 merged.
- `index.html` hard-codes `http://localhost:8080` as the default API base (documented, overridable by `?api=`).
- `filter-session.js` is the largest module (161 lines) and holds all async ordering logic (single in-flight save, newest-queue-wins, late-read ignore, message priority); the logic is well covered by 22 tests but is the riskiest file to change.
- `loadQueue` returns `count` that the page ignores (`countLabel(view.rows)` recomputes it).
- No TODO/FIXME/HACK comments, no lint suppressions, no credentials.

## Handoff Summary
- **Intent-relevant finding**: US5162 is already implemented and merged on `main` (`835c32e`, merged in `64c1612`, released in `v1.1.0`): `filterIsSet` and the "Clear filters" button in `src/render.js:18-31`, `clear()` in `src/filter-session.js:157-158` (reuses `change`, so it saves `{"tenant":null,"overLimit":false}` through the single-flight save queue), the `droppedTenant` message and its priority slot in `src/filter-session.js:11,17,136-139`, and the click/focus wiring in `index.html:35,43,53-56`. Tests: `test/render.test.js:36-57`, `test/filter-session.test.js:267-367`.
- **Risks / follow-up**: Preserve the contract shapes in `test/contract-examples/` (C1, C2) and the message priority order in `filter-session.js:17`; any change to `change()` also changes Clear. Coverage is not measured and there is no lint or CI; the verify script is the only test gate. README's tail is stale. Tests were counted by reading, not executed in this scan.
