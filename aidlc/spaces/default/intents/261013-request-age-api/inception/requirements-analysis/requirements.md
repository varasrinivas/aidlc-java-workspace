# Requirements: request age on the pending list (intent 261013-request-age-api, express, Minimal depth)

## Intent analysis
The reviewer screen reads `GET /requests/pending` from priorauth-api and must show how long each request has waited,
in business days, and which ones are over the tenant's limit, with the same rule the nightly report already uses.
Source: docs-in/request.md (Ravi Menon). The endpoint, its path and its existing fields do not change.

## Functional requirements
- FR1  Each pending row carries its age in business days as of a date. The request may pass `?asOf=YYYY-MM-DD`; without it, today in the server's time zone (Question 4).
  The received day is day 0 (A-01, confirmed: Question 1). An as-of date before the received date is a caller error.
- FR1.1  Saturday and Sunday are not business days.
- FR1.2  The tenant's holidays are not business days. Source: one JSON file per tenant under `src/main/resources/data/`,
  the same list the nightly report uses (Question 3, follow-ups 1 and 2). A tenant without a file has no holidays.
- FR2  A row is over the limit when its age is strictly greater than the threshold (Question 2). Threshold: 5, from configuration
  (`priorauth.aging.threshold-days`), so an environment or tenant can override it without a code change.
- FR3  The new values travel in the existing response: `ageBusinessDays` (integer), `overLimit` (boolean) and
  `ageLabel` (text such as "7 bd OVER 5") on every row. No new endpoint, no new call for the screen.

## Non-functional requirements
- NFR1  No new dependencies: pom.xml changes only its version. (Constraint from codekb/technology-stack.md.)

## Assumptions
- A-01  The received day counts as day 0. Confirmed by Ravi Menon, 09:47.
- A-02  Only the API changes in this intent; the screen shows the new fields in its own change later (out of scope).

## Out of scope
- Changing the screen; changing the report; alerting when something is over the limit (answer to Question 4: that is observability, not the API).
