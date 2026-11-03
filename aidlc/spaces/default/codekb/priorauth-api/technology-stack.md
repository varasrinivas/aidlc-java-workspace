# Technology Stack: priorauth-api

Full rescan of `main` at `0e00544` (tag `v1.2.0`), 2026-11-03. Versions are as declared in `pom.xml`; transitive versions come from the Spring Boot 4.1.1 BOM and were not resolved (no `mvn dependency:tree` run).

## Languages and Runtime

| Item | Version | Evidence |
|---|---|---|
| Java | 21 | `pom.xml` `java.version` |
| JSON (data and contract fixtures) | n/a | `src/main/resources/data/`, `src/test/resources/contract/f1220/` |
| YAML (configuration) | n/a | `application.yml` |

## Frameworks and Libraries

| Name | Version | Purpose |
|---|---|---|
| Spring Boot (`spring-boot-starter-parent`) | 4.1.1 | Parent POM and dependency BOM |
| `spring-boot-starter-webmvc` | from BOM | Spring MVC, embedded Tomcat, JSON |
| Jackson 3 (`tools.jackson.databind`, `tools.jackson.core`) | from BOM | JSON read/write; `JsonMapper` bean injected |
| Jakarta Servlet API | from BOM | `HttpServletRequest` in `NewEndpointProtocolErrorHandler` |
| `spring-boot-starter-webmvc-test` (test) | from BOM | JUnit 5 (incl. params), AssertJ, MockMvc, Spring Boot Test |
| JDK `java.net.http.HttpClient` (test) | JDK 21 | Real-server tests |

## Build and Tooling

| Tool | Detail |
|---|---|
| Maven | Single module; no wrapper committed; `spring-boot-maven-plugin` for `spring-boot:run` and the runnable jar |
| Run | `mvn spring-boot:run` (port 8080) |
| Test | `mvn -q test`, run only through the workspace verify script (`scripts\verify.cmd` / `scripts/verify.sh`) |
| Formatter / linter | none |
| Coverage | none |
| CI | none (local remotes; the verify script is the CI stand-in) |

## Infrastructure and Deployment

No container file, IaC, or deployment configuration in the repo. No deployed environments: a release is the feature-branch PR to `main` plus a version tag (`v1.0.2`, `v1.1.0`, `v1.2.0`; also the non-release tag `f1210-answer`; `pom.xml` is at `1.2.0`, matching the latest tag), demoed locally.

## Storage

None external. The request export and holidays are classpath JSON; filters and history are in process memory.
