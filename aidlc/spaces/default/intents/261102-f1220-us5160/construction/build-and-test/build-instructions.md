# Build Instructions — F1220 US5160 (`priorauth-api`)

## Prerequisites

- Java 21 (the run on 2026-11-03 used OpenJDK 21.0.10) and Maven on the `PATH`.
- Network access to Maven Central the first time, so Maven can download the Spring Boot 4.1.1 parent and its dependencies. Later builds use `~/.m2`.
- A checkout of this workspace with `priorauth-api/` beside the record, on branch `f1220/us5160-save-filter`.
- There is no new dependency in this story; `pom.xml` is unchanged.

## Environment and Configuration

No environment variables, local services or database are needed. The data is packed into the jar.

Two new settings in `priorauth-api/src/main/resources/application.yml`. Each also has its default in `@Value`, so it can be left unset:

| Key | Default | What it does |
|---|---|---|
| `priorauth.reviewer-filter.max-reviewers` | `10000` | Most distinct reviewers with a saved filter (FR1.4). |
| `priorauth.cors.allowed-origins` | `http://localhost:3000` | Comma-separated exact browser origins allowed to call the API (FR8.1). Start-up fails on `*`, `null` or an empty entry. |

## Build and Verify

From the workspace root, only through the workspace verify script (team rule). The script runs `mvn -q test`, which compiles the main and test code and runs every test:

```
scripts\verify.cmd priorauth-api
```

(`scripts/verify.sh priorauth-api` on a POSIX shell.)

- **Success:** exit code 0. The script prints `verify: priorauth-api FAILED` and exits 1 on any compile or test failure.
- **Per-class counts:** `priorauth-api/target/surefire-reports/*.txt`.
- **Run the API locally for a demo:** `mvn spring-boot:run` in `priorauth-api/` (the README's existing command), then for example:
  - `curl -X PUT -H "Content-Type: application/json" -d "{\"tenant\":\"TX-01\",\"overLimit\":true}" http://localhost:8080/reviewers/rita.k/filter`
  - `curl http://localhost:8080/reviewers/rita.k/filter`
  - `curl http://localhost:8080/tenants`

## Before the PR (team Way of Working)

1. `git -C priorauth-api fetch`, then rebase `f1220/us5160-save-filter` onto `origin/feature/F1220`, keeping both stories' changes on a conflict.
2. Run `scripts\verify.cmd priorauth-api` on the rebased branch and paste its result into the PR.
3. `git push --force-with-lease`, then open the PR into `feature/F1220`, naming the sibling stories (US5161, US5162, US5163). Kiran Rao does this, not AI-DLC.

## Troubleshooting

- **Port 8080 in use** for `mvn spring-boot:run`: stop the other process or run with `--server.port=<port>`. The tests use MockMvc or a random port, so they are not affected.
- **Start-up fails with `IllegalStateException` about allowed origins:** `priorauth.cors.allowed-origins` contains `*`, `null` or an empty entry. Use exact origins only.
- **Java agent warnings** (Mockito / Byte Buddy self-attaching) in the test output are harmless and do not fail the build.
