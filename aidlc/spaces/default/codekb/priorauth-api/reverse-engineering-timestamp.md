# Reverse Engineering Timestamp

## Run Record

- Date: 2026-11-03
- Commit: 0e00544 (`main`, tag `v1.2.0`, merge of PR #85 `feature/F1220`; working tree clean)
- Repo: priorauth-api
- Intent: 261103-f1220-us5163 (isolated single-stage 2.1 run)
- Breadth: full rescan of the whole repo; every tracked file (68) read. This replaces the earlier STALE store wholesale.
- Left out unopened: `target/` (build output, git-ignored) and `.git/`. The test suite was not run.

## Scope of Analysis

```yaml
scope_version: 1
kind: full
intent: f1220-us5163
fingerprint: eee5e2c9e7450c43ded6fb191ae51ffc4e1dd859
analyzed:
  paths:
    - ./
  components:
    - PriorAuthApiApplication
    - PendingRequestsController
    - RequestFilter
    - PendingRequestResponse
    - ReviewerFilterController
    - TenantsController
    - SavedFilterBody
    - SavedFilterResponse
    - HistoryLineResponse
    - ReviewerIds
    - ErrorCode
    - ErrorResponse
    - FilterRequestException
    - NewEndpointErrorHandler
    - NewEndpointProtocolErrorHandler
    - BrowserAccessPolicy
    - BusinessDays
    - AgeBadge
    - HolidayCalendar
    - PriorAuthRequest
    - SavedFilter
    - HistoryLine
    - RequestStore
    - TenantDirectory
    - ReviewerFilterStore
shallow:
  paths: []
```
