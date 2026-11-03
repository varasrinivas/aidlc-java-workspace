# Build Instructions — F1220 US5163 (`priorauth-api`)

## Prerequisites

- JDK 21 and Maven on `PATH` (the run below used Java 21.0.10 and Spring Boot 4.1.1 from the `pom.xml` parent).
- No new dependency: `pom.xml` is unchanged by US5163. Maven resolves everything from the local repository or Maven Central on first build.
- No environment variables, services or files are needed. The store is in memory.

## Environment Setup

- Settings (all optional; defaults in `application.yml` and `@Value`):
  - `priorauth.reviewer-filter.max-reviewers` (default 10000)
  - `priorauth.reviewer-filter.max-history-lines` (default 1000, new in US5163)
  - `priorauth.cors.allowed-origins` (default `http://localhost:3000`)
- Time comes from the `clock` bean, `Clock.systemUTC()`. Nothing to configure.

## Build and Test Command

From the workspace root, only through the workspace verify script:

```
scripts\verify.cmd priorauth-api
```

(`scripts/verify.sh priorauth-api` on a POSIX shell.) It runs `mvn -q test` in `priorauth-api`, which compiles main and test code and runs the whole suite (about 14 seconds).

## Build Verification

- The script exits 0 on success and non-zero on any compile or test failure.
- Per-class counts: `priorauth-api/target/surefire-reports/*.txt`. Expected after US5163: 118 tests in 18 classes, none failing.
- To run the API locally for the demo: `mvn spring-boot:run` in `priorauth-api`, then `GET http://localhost:8080/reviewers/{reviewerId}/filter/history`.

## Before the PR (story owner)

1. `git -C priorauth-api fetch origin`, then rebase `f1220/us5163-filter-history` onto `origin/feature/F1220`; keep both stories' changes on a conflict.
2. Run `scripts\verify.cmd priorauth-api` on the rebased branch and paste the result into the PR.
3. `git push -u origin f1220/us5163-filter-history --force-with-lease` (the branch's upstream is currently `origin/feature/F1220`, so name the remote branch), then open the PR into `feature/F1220`.

## Troubleshooting

- **Mockito "self-attaching" / dynamic agent warnings:** expected and harmless; they predate US5163.
- **`NoUniqueBeanDefinitionException` for `Clock`** in a new test: give a test clock a different bean name and mark it `@Primary`, as `ReviewerFilterHistoryTest` does.
- **`IllegalArgumentException ... max-history-lines must be at least 1`:** a setting below 1 was configured; use 1 or more.
