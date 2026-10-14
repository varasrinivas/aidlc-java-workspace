# Reviewer Queue API: Product Specification

| | |
|---|---|
| Document | Reviewer Queue API: Product Specification |
| Version | 1.3 (approved) |
| Owners | Ravi Menon (Utilization Management), Meena Iyer (Engineering) |
| Library | Prior Auth Platform > Product > Specifications |
| Last modified | 12 Oct 2026 |

*Converted from Reviewer-Queue-API-Spec.docx with markitdown for AI-DLC; the Word file in SharePoint is the original.*

## 1. Purpose

The reviewer screen shows the prior-authorization requests that still need a decision. It reads one endpoint, `GET /requests/pending`, from priorauth-api. This document fixes what that endpoint returns and how callers narrow it. It does not cover the screen's layout, the nightly report, or how requests are stored.

## 2. Response

A JSON array, oldest request first. Every row carries `id`, `tenantId`, `service`, `status`, `receivedAt`, and, since version 1.1, `ageBusinessDays`, `overLimit` and `ageLabel`. Fields are never removed or renamed; new fields are added only at the end.

## 3. Narrowing the list

Callers narrow the list with query parameters. Parameters combine with AND. A parameter that is absent does not filter.

| Parameter | Values | Effect |
|---|---|---|
| `asOf` | ISO date, `YYYY-MM-DD` | The date the age is computed for. Default: today. |
| `tenant` | a tenant id, e.g. `TX-01` | Only that tenant's requests. |
| `status` | `PENDED`, `IN_REVIEW` | Only requests with that status. |
| `overLimit` | `true`, `false` | Only requests whose over-limit flag has that value, for the same `asOf`. |

## 4. Errors

A request the API cannot answer correctly gets `400 Bad Request` with a JSON body `{ "error": "<message>" }`. The message names the parameter and, where there is a fixed list, the allowed values.

- An `asOf` that is not a date, or is before a request's received date.
- A `status` outside the list in section 3.
- A `tenant` that is not configured in the platform. A mistyped tenant must not look like an empty queue: reviewers would conclude their work is done.

## 5. Non-functional requirements

- No new runtime dependencies for filtering; the list is small (hundreds of rows) and is filtered in memory.
- Response time for the pending list stays under 500 ms at the 95th percentile, as today.
- The response shape stays backward compatible (section 2): the screen's current release must keep working unchanged.

## 6. Glossary

| Term | Meaning |
|---|---|
| Tenant | A health plan the platform serves, identified by an id such as `TX-01`. |
| Pending | A request in status `PENDED` (waiting on the provider) or `IN_REVIEW` (waiting on a reviewer). |
| Over the limit | Older than the tenant's limit in business days (default 5), as defined in requirement FR2 of intent 261013-request-age-api. |
