# API
`GET /requests/pending` → 200, JSON array of `{ id, tenantId, service, status, receivedAt }`, oldest first, pending statuses only
(PENDED, IN_REVIEW). No parameters, no paging, no auth in this cut.
