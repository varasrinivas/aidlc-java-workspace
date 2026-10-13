# Test results (3.6) · Tue 13 Oct, 10:52

## Build status
| Repo | Command | Pass | Fail | Skipped |
|---|---|---|---|---|
| priorauth-api | mvn -q test | 10 | 0 | 0 |

## Target Verification Matrix (finalised)
| Requirement | Test | Result |
|---|---|---|
| FR1 | BusinessDaysTest.receivedTodayHasAgeZero, BusinessDaysTest.asOfBeforeReceivedIsAnError, PendingRequestsControllerTest.asOfBeforeReceivedIsABadRequest (→ 400) | pass |
| FR1.1 | BusinessDaysTest.weekendIsNotCounted | pass |
| FR1.2 | BusinessDaysTest.tenantHolidayIsNotCounted | pass |
| FR2 | AgeBadgeTest.flagOnlyWhenOverTheThreshold (5 → not flagged, 6 → flagged) | pass |
| FR3 | PendingRequestsControllerTest.eachRowCarriesItsAgeAndFlag | pass |
| NFR1 | pom.xml diff: only `<version>` changed | pass (inspection) |
Existing tests: 3, still passing.

## Manual check
`mvn spring-boot:run`, then `curl "http://localhost:8080/requests/pending?asOf=2026-10-13"`: PA-10231 returns
`"ageBusinessDays": 7, "overLimit": true, "ageLabel": "7 bd OVER 5"` (received 1 Oct; 12 Oct is a TX-01 holiday).

## Loop-Back Log
(none)
