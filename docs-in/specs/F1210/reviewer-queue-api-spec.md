# F1210 Reviewer queue filters: API contract (draft for 2.8 Contract Design)

Owner: Meena Iyer (tech lead). Input to the parent intent; the approved contract is the parent's
`inception/contract-design/contract-summary.md`, not this file.

## GET /requests/pending

| Query parameter | Type | Default | Story |
|---|---|---|---|
| `asOf` | ISO date | today | existing (FR1) |
| `tenant` | string, e.g. `TX-01` | none: every tenant | US5151 |
| `overLimit` | `true` / absent | absent: every row | US5152 |

- Filters combine with AND, are applied after aging, and keep the list oldest first.
- An unknown parameter is ignored. An unknown tenant returns an empty list (200).
- One `RequestFilter` reads the parameters; every filter story adds one field to it (US5150).

## Response

Unchanged: the same rows as today (`id`, `tenantId`, `service`, `status`, `receivedAt`,
`ageBusinessDays`, `overLimit`, `ageLabel`). The screen counts the rows itself (US5153).
