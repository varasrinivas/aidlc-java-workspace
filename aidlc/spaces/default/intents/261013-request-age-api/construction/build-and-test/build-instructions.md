# Build instructions (3.6)

- Build and test: `mvn -q test` in priorauth-api (Java 21, Maven 3.9). Same command as ./scripts/verify.sh.
- Run locally: `mvn spring-boot:run`, then `curl "http://localhost:8080/requests/pending?asOf=2026-10-13"`.
- Package: `mvn -q package` produces `target/priorauth-api-1.1.0.jar`. The workspace has no pipeline or deployment config: shipping the jar is the team's.
- No new configuration is required: `priorauth.aging.threshold-days` defaults to 5.
