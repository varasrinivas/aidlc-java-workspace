# Component inventory
- PendingRequestsController (@RestController): one GET mapping, delegates to RequestStore.
- PendingRequestResponse (record): maps PriorAuthRequest → JSON row.
- RequestStore (@Service): loads the sample export once at startup with the injected JsonMapper; all(), pending().
- PriorAuthRequest (record): id, tenantId, memberId, service, status, receivedAt (LocalDate); isPending().
