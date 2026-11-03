# Business Overview: priorauth-api

Full rescan of `main` at `0e00544` (tag `v1.2.0`), 2026-11-03.

## Purpose

`priorauth-api` is the HTTP API the prior-authorization reviewer screen (`priorauth-web`) reads. A health-plan reviewer works a queue of prior-authorization requests (a member's request for a service such as an MRI); the API tells them which requests still need action, how long each has waited in business days, and whether it is over the tenant's limit. Since F1220 ("Remember my filter", release 2027.Q1 R1) it also remembers each reviewer's last queue filter and keeps a history of every filter they saved.

A tenant is a health-plan line of business (`TX-01`, `NM-02` in the sample data). There is no database in this cut: the request queue is a nightly export packed into the jar, and saved filters live in memory only.

## Key Functionality

| Capability | Endpoint | Introduced by |
|---|---|---|
| Pending queue, oldest first, with age in business days, over-limit flag and label | `GET /requests/pending[?asOf&tenant&overLimit]` | v1.0.x, ageing 261013-request-age-api, filters F1210 (US5150-US5152) |
| Save a reviewer's last filter (tenant or all, over-limit switch) | `PUT /reviewers/{reviewerId}/filter` | F1220 US5160 |
| Read it back (`{}` when none) | `GET /reviewers/{reviewerId}/filter` | F1220 US5160 |
| Known tenants for the screen's picker | `GET /tenants` | F1220 US5160 |
| History of every saved filter, newest first | `GET /reviewers/{reviewerId}/filter/history` | F1220 US5163 |

Endpoint details are in `api-documentation.md`.

## Business Rules

- **Age** counts business days strictly after the received date up to and including the as-of date; weekends and the tenant's holidays do not count (FR1, assumption A-01). An as-of date before a received date is the caller's error (400).
- **Over limit** means strictly more business days than `priorauth.aging.threshold-days` (default 5) (FR2).
- **Pending** means status `PENDED` or `IN_REVIEW`; other statuses (for example `APPROVED`) are decided.
- **Known tenant**: any `tenantId` in the export, pending or decided, matched exactly and case-sensitively (FR3.1).
- **Reviewer id**: 1-64 ASCII letters, digits, `.`, `-`, `_`, with at least one letter or digit; case-sensitive (FR1.3). `.` and `..` are refused with 400 (contract change 2026-11-03).
- **Saved filter**: one per reviewer; a later save replaces it; at most `max-reviewers` (default 10,000) distinct reviewers; a new one beyond that is refused with 409 (FR1.4, NFR7).
- **History** (US5163): every successful save, including a repeat or a clear, adds one line `{at, reviewer, tenant, overLimit}`, time in UTC cut to the second; refused saves add none; newest first; at most `max-history-lines` (default 1,000) per reviewer, oldest dropped (FR7).
- **Errors** on the new endpoints carry a fixed code and message and never echo caller input (NFR4).

## Users and Stakeholders

- Reviewers, through `priorauth-web` (allowed browser origin `http://localhost:3000` by default).
- Product owner Dana Ortiz accepts features after the local demo; there is no deployed environment (see `technology-stack.md`).

## Known Business Limits

- Saved filters and history are lost on restart, and anyone who can reach the API can read or change any reviewer's filter and history (no authentication). Both are stated in the F1220 release notes.
- Only TX-01 2026 holidays are packaged; see `code-quality-assessment.md` (TD-1).
