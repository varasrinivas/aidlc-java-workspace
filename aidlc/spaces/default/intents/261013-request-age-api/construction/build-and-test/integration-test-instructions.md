# Integration Test Instructions

## Applicability
The active test strategy is **Minimal**, which generates no separate integration test suite. There is one service, and the only boundary is the HTTP endpoint.

## What already exercises the boundary
`PendingRequestsControllerTest` starts the full Spring context with the real holiday file and request data and calls `GET /requests/pending?asOf=2026-10-13` through MockMvc (`eachRowCarriesItsAgeAndFlag`); `listsPendingRequestsOldestFirst` checks the existing contract is unchanged.

## How to run
From the workspace root: `mvn -q -f priorauth-api/pom.xml test -Dtest=PendingRequestsControllerTest`

## Test data
`data/requests.sample.json` and `data/holidays-TX-01-2026.json` are on the classpath and read-only; no setup or cleanup.
