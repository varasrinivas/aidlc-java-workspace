# Build Instructions — F1220 Remember my filter (feature build)

This is a standalone Build and Test run over the whole feature: the merged `feature/F1220` branch in both repos, after the four story PRs.

| Repo | Branch | Head | Story PRs merged |
|---|---|---|---|
| `priorauth-api` | `feature/F1220` | `d1d11a5` | #81 US5160 (`cb1aee7`, `4b63a4e`), #83 US5163 (`3cf2206`) |
| `priorauth-web` | `feature/F1220` | `64c1612` | #82 US5161 (`9af272e`), #84 US5162 (`835c32e`) |

What each story built is recorded in its own intent:
- `intents/261102-f1220-us5160/construction/code-generation/`
- `intents/261102-f1220-us5161/construction/code-generation/`
- `intents/261103-f1220-us5162/construction/code-generation/`
- `intents/261103-f1220-us5163/construction/code-generation/`

## Prerequisites

- Java 21 and Maven, for `priorauth-api` (Spring Boot 4.1.1 comes from the parent POM).
- Node.js 22 or later, for `priorauth-web`. The repo has no dependencies; `node --test` is built in.
- No database, no cloud account, no secrets. The request export is packed into the API jar.

## Get the Feature Branch

```
scripts\pull-all.ps1                       # or scripts/pull-all.sh
git -C priorauth-api switch feature/F1220
git -C priorauth-web switch feature/F1220
```

Check that each local head matches `origin/feature/F1220` (`git -C <repo> status -sb`).

## Build and Unit Tests: One Command

Tests run only through the workspace verify script, with both repos named:

```
scripts\verify.cmd priorauth-api priorauth-web     # Windows
scripts/verify.sh priorauth-api priorauth-web      # macOS/Linux
```

- It runs `mvn -q test` in `priorauth-api`, which compiles the code, and `npm test --silent` (`node --test`) in `priorauth-web`, which needs no build step.
- Exit code 0 means both repos passed.
- For the API's test count, add up `priorauth-api/target/surefire-reports/*.txt`.
- A run with no arguments on a clean `main` tests nothing and still exits 0, so it never counts as a result.

## Run the Feature Locally (for the integration and manual checks)

Run each in its own terminal:

```
cd priorauth-api && mvn spring-boot:run              # http://localhost:8080
cd priorauth-web && npx serve@14 . -l 3000           # http://localhost:3000
```

Then open `http://localhost:3000/?reviewer=rita.k&api=http://localhost:8080`.

**Pin `serve`.** The README says `npx serve .`. On this machine npx picked up an old cached `serve`, which ignored the port and listened on 5000. The API allows browser calls only from `http://localhost:3000` (`priorauth.cors.allowed-origins`), so on port 5000 every API call from the page is refused. Use `npx serve@14 . -l 3000`, or check the port the server prints.

## Configuration

These are in `priorauth-api/src/main/resources/application.yml`. All have defaults, so none is required.

| Key | Default | Purpose |
|---|---|---|
| `priorauth.cors.allowed-origins` | `http://localhost:3000` | Comma-separated named origins; `*` is refused at start-up |
| `priorauth.reviewer-filter.max-reviewers` | `10000` | Most reviewers with a saved filter (FR1.4) |
| `priorauth.reviewer-filter.max-history-lines` | `1000` | Newest history lines kept per reviewer (FR7.5) |

## Build Verification

- `verify:` prints one line per repo, and the script exits 0.
- `priorauth-api`: 18 test classes, 118 tests, 0 failures.
- `priorauth-web`: 48 tests, 48 passing.
- With the API running, `GET http://localhost:8080/tenants` answers `["NM-02","TX-01"]`.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| The page shows "couldn't be loaded" for everything, and the browser console shows CORS errors | The page isn't served from `http://localhost:3000` | Serve on port 3000, or add the origin to `priorauth.cors.allowed-origins` |
| The API won't start: `IllegalStateException` about allowed origins | An empty entry, `null`, or `*` in the origins list | Name each origin |
| `Mockito is currently self-attaching` and dynamic-agent warnings | A JDK warning that predates F1220 | None needed; the tests still pass |
| Git warns "LF will be replaced by CRLF" | `core.autocrlf` on Windows | No effect on the build |
