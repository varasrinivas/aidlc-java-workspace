# Security Test Instructions — F1220 Remember my filter

The team's security checklist (applied at each story's code-plan review) and NFR3-NFR6 are the security requirements. There is no SAST or DAST tool in F1220, and the team chose not to add one (Practices Q11 A). The checks below are tests and requests run against the API on a local machine.

## Checklist Item to Check

| Checklist item / NFR | Automated proof (verify script) | Live check (`integration-test-instructions.md` §2) |
|---|---|---|
| Every request value validated and size-limited (NFR3) | `ReviewerIdsTest`, `SavedFilterBodyTest` (shape, types, 1 KB limit, trailing tokens), `ReviewerFilterControllerTest` (check order) | E8, E11, E12 |
| API data escaped before display (NFR5) | `render.test.js` AC1.2.10: tenant ids with `& < > " '` render as text | M1 by eye |
| No file path or cache key from a caller's value (NFR3) | `TenantDirectory` reads tenants from the export only; the reviewer id is a map key in memory, never a path. `HolidayCalendar.forTenant` is not called with request input (code reading) | — |
| Errors carry no stack trace and no raw caller input (NFR4) | `ReviewerFilterContractTest` error examples; `NewEndpointProtocolErrorTest` (405 and 406 with no body); `DotReviewerIdTest`; `ReviewerFilterHistoryTest` AC1.4.8 | E8, E12 |
| Browser calls only from named origins, never `*` (NFR6) | `BrowserAccessPolicyTest` (start-up refuses `*`, `null`, empty entries; preflight answers) | E3, E4, E14 |

## Known Exposures (Accepted, Not Fixed in F1220)

- **No authentication.** Anyone who can reach the API can read or overwrite any reviewer's filter and history. This is accepted for F1220, and Meena Iyer's release-notes line says anyone using the screen can read it.
- **Unmapped paths under `/reviewers/`** (for example `/reviewers/rita.k/other`) get Spring Boot's default 404 body, whose `path` field echoes the id. This was accepted at US5160's gate and put on the backlog.
- **Duplicate JSON keys** are accepted, and the last value wins (US5160 risk note). Every value is still validated, so there is no bypass.
