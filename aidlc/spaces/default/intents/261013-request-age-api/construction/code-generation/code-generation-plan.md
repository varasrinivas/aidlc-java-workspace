# Code Generation Plan — Request age on the pending list (priorauth-api)

Express scope, zero Units: one stage-level implementation for the whole change. Repo: priorauth-api.
Workspace rules (CLAUDE.md): one unit = one branch = one PR, branch pattern `request-age/<slug>`; tests through
`./scripts/verify.sh` (`scripts\verify.cmd`); a new pom.xml dependency must be declared here (there is none).

## Steps
- [ ] Step 1 — Branch and baseline. In `priorauth-api/`, create `request-age/u1-age-api` from `main`; run `./scripts/verify.sh`
  and record the baseline: 3 existing tests, all passing.
- [ ] Step 2 — Files, in this order:

| # | File | Action | Covers |
|---|---|---|---|
| 1 | src/main/java/com/acmehealth/priorauth/aging/BusinessDays.java | create: `isBusinessDay`, `between` (strictly after start, up to and including end) | FR1, FR1.1, FR1.2 |
| 2 | src/main/java/com/acmehealth/priorauth/aging/AgeBadge.java | create: record `businessDays`, `overLimit`, `thresholdDays`; `of(...)`, `label()` | FR2, FR3 |
| 3 | src/main/java/com/acmehealth/priorauth/aging/HolidayCalendar.java | create: `@Service`, loads `data/holidays-<tenant>-2026.json`, empty set when absent | FR1.2 |
| 4 | src/main/resources/data/holidays-TX-01-2026.json | create: the 11 TX-01 dates (follow-up 1) | FR1.2 |
| 5 | src/main/java/com/acmehealth/priorauth/api/PendingRequestResponse.java | change: add `ageBusinessDays`, `overLimit`, `ageLabel`; `from(request, badge)` | FR3 |
| 6 | src/main/java/com/acmehealth/priorauth/api/PendingRequestsController.java | change: `?asOf` (ISO date, default today; before a received date → 400), inject `HolidayCalendar` and the threshold | FR1, FR2, FR3 |
| 7 | src/main/resources/application.yml | change: `priorauth.aging.threshold-days: 5` | FR2 |
| 8 | src/test/java/com/acmehealth/priorauth/aging/BusinessDaysTest.java | create: day zero, weekend, holiday, as-of before received (4 tests) | FR1, FR1.1, FR1.2 |
| 9 | src/test/java/com/acmehealth/priorauth/aging/AgeBadgeTest.java | create: 5 not flagged, 6 flagged, labels (1 test) | FR2 |
| 10 | src/test/java/com/acmehealth/priorauth/api/PendingRequestsControllerTest.java | change: add two tests, `?asOf=2026-10-13` → PA-10231 7 / true, PA-10244 4 / false; `?asOf=2026-09-30` → 400 | FR1, FR3 |
| 11 | pom.xml | change: version 1.0.2 → 1.1.0, nothing else | NFR1 |
| 12 | README.md | change: usage line | — |

- [ ] Step 3 — Verify. Run `./scripts/verify.sh`. Expected: 10 tests (3 existing + 7 new), 0 failures.
- [ ] Step 4 — Commit on `request-age/u1-age-api`. Pushing and opening the PR are the team's.

Not touched: PriorAuthApiApplication, PriorAuthRequest, RequestStore, RequestStoreTest, the sample export, the endpoint path.

## Requirement → Step Traceability
FR1, FR1.1, FR1.2 → files 1, 3, 4, 6, 8, 10 · FR2 → files 2, 6, 7, 9 · FR3 → files 2, 5, 6, 10 · NFR1 → file 11
