# Unit test instructions (3.5)

Run from the workspace root: `./scripts/verify.sh` (Windows: `scripts\verify.cmd`), which runs `mvn -q test` inside priorauth-api.
Maven downloads the Spring Boot test libraries on the first run (about a minute); later runs take about 10 seconds.
Expected: 10 tests, 0 failures. The controller test starts the whole application in-process (`@SpringBootTest`) and calls
`GET /requests/pending?asOf=2026-10-13` through MockMvc, so no port is opened and nothing has to be running.
