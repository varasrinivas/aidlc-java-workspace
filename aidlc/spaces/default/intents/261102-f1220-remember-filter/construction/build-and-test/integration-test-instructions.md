# Integration Test Instructions — F1220 Remember my filter

Test strategy: **Standard**, so the integration checks cover the key boundaries between stories:

- the screen (US5161, US5162) against the API (US5160, US5163) through contracts C1-C5;
- the save (US5160) against the history (US5163) inside one store.

## 1. Automated Boundary Tests (Run by the Verify Script)

`scripts\verify.cmd priorauth-api priorauth-web` already runs these. Both sides test against the same contract examples, so drift shows up as a failing test in one repo.

| Boundary | Where it is tested |
|---|---|
| C1/C2 shapes, API side | `ReviewerFilterContractTest` and `TenantsControllerTest` read `src/test/resources/contract/f1220/*.json`, which are byte-identical copies of the parent's `inception/contract-design/examples/` |
| C1/C2 shapes, screen side | `test/saved-filter-client.test.js` reads `test/contract-examples/*.json` (copies of the same files) |
| C3 history | `ReviewerFilterHistoryTest` reads `c3-get-history*.json` |
| Save and history in one lock (NFR2) | `ReviewerFilterStoreTest`: AC1.4.3 (a refused save writes no line) and AC1.4.7 (50 concurrent saves give 50 lines, and the saved filter equals the newest line) |
| Errors, CORS, 405 and 406 on a real server | `DotReviewerIdTest`, `NewEndpointProtocolErrorTest` (embedded Tomcat on a random port) |

**Contract-copy check.** Before the feature PR, confirm the copies still match the parent's examples. Compare `Get-FileHash` (or `sha256sum`) of each file in the three folders.

## 2. End-to-End API Checks Against the Running API

Start the API (`build-instructions.md`, "Run the Feature Locally"). Send every request with the header `Origin: http://localhost:3000`. Use a reviewer id no one else uses, for example `bt.rita`. Then run the checks in order:

| # | Request | Expected |
|---|---|---|
| E1 | `GET /tenants` | 200 `["NM-02","TX-01"]`, `Access-Control-Allow-Origin: http://localhost:3000` |
| E2 | `GET /reviewers/bt.rita/filter` | 200 `{}` |
| E3 | `OPTIONS /reviewers/bt.rita/filter` with `Access-Control-Request-Method: PUT` and `Access-Control-Request-Headers: content-type` | 200, allow-origin `http://localhost:3000`, allow-methods `GET,PUT` |
| E4 | The same preflight from `Origin: http://evil.example` | 403, no `Access-Control-Allow-Origin` |
| E5 | `PUT /reviewers/bt.rita/filter` with `{"tenant":"TX-01","overLimit":true}` | 204 |
| E6 | `GET /reviewers/bt.rita/filter` | 200 `{"tenant":"TX-01","overLimit":true}` |
| E7 | `GET /requests/pending?tenant=TX-01&overLimitOnly=true` | 200, only TX-01 rows, all `overLimit: true` |
| E8 | `PUT` with `{"tenant":"<script>","overLimit":false}` | 400 `unknown-tenant`, fixed message, input not echoed |
| E9 | `PUT` with `{"tenant":null,"overLimit":false}` (Clear) | 204 |
| E10 | `GET /reviewers/bt.rita/filter/history` | 200, two lines newest first: Clear, then TX-01. E8 wrote none |
| E11 | `PUT` with a body over 1 KB | 400 `invalid-body` |
| E12 | `GET /reviewers/rita%20k/filter` | 400 `invalid-reviewer-id`, id not echoed |
| E13 | `GET /requests/pending` | 200, 4 rows including `PA-10270` (NM-02) |
| E14 | `GET /tenants` from `Origin: http://evil.example` | 403, no `Access-Control-Allow-Origin` |

## 3. Manual Screen Checks (Browser, by a Person)

The team has no browser or DOM tests, so `index.html` wiring is checked by hand. Serve the page on port 3000 and open `http://localhost:3000/?reviewer=rita.k&api=http://localhost:8080`.

| # | Check | Proves |
|---|---|---|
| M1 | First open: the queue is unfiltered, and the Tenant picker lists All tenants, NM-02 and TX-01 | FR4.4, FR4.6 |
| M2 | Choose TX-01 and turn on "Over limit only". Reload. The page opens with both set, and no unfiltered queue flashes first | FR4.3, AC1.2.2 |
| M3 | Use only the keyboard: Tab reaches the picker, the switch and "Clear filters" in that order. Arrow keys or typing change the picker; Space toggles the switch; Enter or Space presses Clear | NFR10 |
| M4 | Every control has a visible text label. With no filter set, Clear is disabled; this is announced as disabled, not shown by colour alone | NFR10, AC1.3.2 |
| M5 | Press "Clear filters". Both controls reset, the whole queue shows, and focus moves to the Tenant picker | AC1.3.1, **AC1.3.5** |
| M6 | Stop the API and change a control. The "not saved" message shows in text, and the queue keeps the chosen filter or shows the queue message | FR5.2, AC1.2.12 |
| M7 | With the picker's list open, wait for an answer to arrive (change the switch first). The list must not close or flicker in a way that loses the choice | US5161 risk note |
| M8 | Open without `?reviewer=`. The controls still filter, nothing is saved, and the page says so | AC1.2.9 |

Record each result (pass or fail, browser and version, who ran it) in `test-results.md` under "Manual screen checks".

## Test Data

- The sample export in the API jar has 5 requests: 4 pending and 1 decided. TX-01 and NM-02 are the known tenants.
- Saved filters and history are in memory, so restarting the API resets them.
