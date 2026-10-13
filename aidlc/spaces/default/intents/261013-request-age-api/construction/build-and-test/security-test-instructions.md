# Security Test Instructions

## Applicability
No separate security test suite is generated. The test strategy is Minimal, and the change adds no authentication, secrets, persistence or outbound calls.

## Security-relevant checks
| Concern | Evidence |
|---|---|
| Input at the boundary: `asOf` | Spring's ISO date binding; an as-of date before a received date is rejected (`BusinessDaysTest.asOfBeforeReceivedIsAnError`) |
| No new personal data exposed | `PendingRequestResponse` still has no `memberId` |
| No new dependency (supply chain) | `pom.xml` changes its version only (NFR1) |
| No secrets | Config holds only the threshold |

## Not covered
- No SAST or dependency scan is configured in the repo, and none was run.
- The endpoint has no authentication, unchanged by this work and out of scope.
