# Developer Code Scan: priorauth-web

Full rescan of `priorauth-web` on `main` at `ddca232` (F1220 merged, version 1.1.0), 2026-11-03. Run in the conductor's session (lead-only pipeline) after the developer hand-off was refused by the Code Generation dispatch check.

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `./` (whole repo: every tracked file was read or inventoried)
  - `package.json`, `README.md`, `.gitignore`
  - `index.html`
  - `src/` (all 5 modules read in full: `api.js`, `filter-session.js`, `queue-filters.js`, `render.js`, `saved-filter-client.js`)
  - `test/` (5 test files inventoried with test counts; `saved-filter-client.test.js` read in part)
  - `test/contract-examples/` (4 contract example files, by name and role)
- **Skimmed only**:
  - Bodies of `api.test.js`, `filter-session.test.js`, `queue-filters.test.js`, `render.test.js` (names, counts and story tags; assertions not read line by line)
- **Left out**:
  - `node_modules/` (gitignored; the repo has no dependencies)

### Packages Found
- `priorauth-web` - static web page + ES modules - JavaScript - the reviewer screen: pending prior-auth queue with tenant and over-limit filters, remembered per reviewer

### Build System
- **Type**: none (no bundler, no build step); `npm test` runs `node --test`; served as static files (`npx serve@14 . -l 3000`)
- **Config Files**: `package.json` (`type: module`, `engines.node >=20`, version 1.1.0)
- **Build Dependencies**: module graph `index.html -> filter-session.js, render.js`; `filter-session.js -> queue-filters.js, saved-filter-client.js`; `queue-filters.js -> api.js`. No cycles.

### APIs Discovered
- REST client - `src/api.js`, `src/queue-filters.js` - `GET /requests/pending[?asOf&tenant&overLimit]`
- REST client - `src/saved-filter-client.js` - `GET` / `PUT /reviewers/{reviewerId}/filter` (C1), `GET /tenants` (C2)
- Page parameters - `index.html` - `?api=` (base URL, default `http://localhost:8080`), `?reviewer=` (reviewer id)
- The history endpoint `GET /reviewers/{reviewerId}/filter/history` (C3) is not called by the screen.

### Frameworks & Libraries
- None at runtime (browser built-ins: `fetch`, `AbortSignal.timeout`, `URL`, `URLSearchParams`)
- Node.js >= 20 - test runner `node:test`, `node:assert/strict`
- `serve@14` via `npx` - local static server, documented in README only (not a declared dependency)

### Test Coverage
- **Test Directories**: `test/`, `test/contract-examples/`
- **Test Frameworks**: Node built-in runner with `node:assert/strict`; network injected through `fetchFn`
- **Test volume**: 5 test files, 48 tests; last recorded verify run (Build and Test, `64c1612`) 48/48 passing
- **Coverage Config**: absent; recorded as NOT MEASURED. No browser or DOM tests; `index.html` logic is untested by design (kept thin).

### Code Quality Indicators
- **Linting**: none (no ESLint/Prettier); style by convention and review
- **CI/CD**: none in the repo; tests run through the workspace `scripts\verify.cmd`
- **Documentation**: `README.md` covers running, page parameters and behaviour; every `src/` file opens with a one-line purpose comment naming its story

### Technical Debt Signals
- `src/api.js` `fetchPending` is no longer used by the page (the queue goes through `queue-filters.js`); still tested.
- `README.md` branch notes ("`main` / `v1.0.0`: the start of the guide (US5153 not built yet)") are out of date now that `main` is 1.1.0 with F1210 and F1220.
- `index.html` keeps the previous count when the queue load fails (`if (view.rows)` guard), so the header count can be stale while the message says the queue couldn't load.
- `src/filter-session.js` validates C1/C2 answers but `queue-filters.js` does not validate the pending-list rows' shape.
- No authentication: `?reviewer=` is whatever the URL says (release-notes item).

## Handoff Summary
- **Intent-relevant finding**: F1220 is fully present on `main`: `createFilterSession` restores the saved filter before the first queue request (`src/filter-session.js:118-144`), saves each change with one save in flight and the newest waiting choice winning (`:99-116`), drops a saved tenant no longer known and says so (`:135-139`), and Clear reuses the change path (`:158`); the button is disabled when no filter is set (`src/render.js:19-33`).
- **Risks / follow-up**: no DOM tests, so focus and keyboard behaviour (Build and Test findings M6/M7) stay manual; stale README branch notes; unused `fetchPending`.
