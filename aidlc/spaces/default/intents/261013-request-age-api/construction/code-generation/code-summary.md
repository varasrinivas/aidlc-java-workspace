# Code summary: priorauth-api (3.5)

**Intent** 261013-request-age-api · **Scope** express · **Requirements** FR1–FR3, NFR1 · **Branch** request-age/u1-age-api · **Commit** b477c4e

**What changed.** New package `com.acmehealth.priorauth.aging`: `BusinessDays` (pure business-day arithmetic, received day = day 0,
weekends and tenant holidays excluded), `AgeBadge` (days, over-limit flag, label) and `HolidayCalendar` (one JSON file per tenant
under resources, the same TX-01 list the report uses). `GET /requests/pending` takes an optional `?asOf=YYYY-MM-DD` and every row
now carries `ageBusinessDays`, `overLimit` and `ageLabel`. The threshold comes from `priorauth.aging.threshold-days` (default 5).
An `asOf` before a request's received date answers 400. Version 1.0.2 → 1.1.0.

**What did not change.** The endpoint path, the existing fields, `RequestStore`, the model, the sample export, the dependencies.

**Verification.** `./scripts/verify.sh`: 10 tests, 7 new (one per requirement, the 5/6 boundary and the 400), 0 failures.

**Open.** Holiday data covers TX-01 2026 only; each later year and each other tenant needs its own file (without one, only
weekends are skipped). Pushing the branch and opening the PR are the team's.
