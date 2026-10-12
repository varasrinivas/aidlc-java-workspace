# java-workspace

Run AI-DLC from this folder. One code repo, `priorauth-api/`, a Spring Boot 4.1 REST API on Java 21, built with Maven.

| Repo          | Owns                                   | Verify with      | Branch pattern       |
|---------------|----------------------------------------|------------------|----------------------|
| priorauth-api | the API the reviewer screen reads      | `mvn -q test`    | request-age/<slug>   |

Rules: the record in `aidlc/` is the source of truth for requirements and decisions; commit it after every gate.
One unit = one branch = one PR. Tests through `./scripts/verify.sh` (`scripts\verify.cmd` on Windows), never ad hoc.
Never add a dependency to pom.xml inside a unit without saying so in the plan.
