# F1187 Reviewer queue filters

> Snapshot of a Rally feature and its user stories, written by `scripts/export-rally.py` (offline, from F1187.json).
> Rally is the source of truth: refresh this file before `/aidlc`, and cite the story IDs (US…) in requirements.

| Field | Value |
|---|---|
| Epic | E212 Reviewer screen v2 |
| State | Ready |
| Owner | Ravi Menon |
| Release | 2026.Q4 R2 |
| Last updated in Rally | 2026-10-14 |
| Stories | 3 |

## Feature description

Reviewers now see each request's age and over-limit flag (F1162, delivered in priorauth-api 1.1.0). The list is still one long queue across every health plan, so a reviewer who covers one plan, or who is clearing over-limit requests first, scrolls past rows they will not touch.

Let the screen ask the API for a narrower list: by tenant, by status, and only the over-limit rows. The screen change is a separate feature (F1190).

## User stories

### US5120 Filter the pending list by tenant

Schedule state: Defined · Estimate: 2 · Owner: Kiran Rao

As a reviewer who covers one health plan, I want the pending list for my tenant only, so that I don't scroll past other plans' requests.

**Note:** the sample export has only TX-01 today. Add a second tenant (NM-02) to the sample data so this story can be tested.

**Acceptance criteria**

- `GET /requests/pending?tenant=TX-01` returns only TX-01 rows, oldest first.
- Without `tenant`, every tenant is returned, as today.
- A tenant with no pending requests, or one we don't know, returns an empty list (200).

### US5121 Filter the pending list by status

Schedule state: Defined · Estimate: 1 · Owner: Kiran Rao

As a reviewer, I want to see only the requests waiting on me (`IN_REVIEW`) or only the ones waiting on the provider (`PENDED`), so that I work one kind at a time.

**Acceptance criteria**

- `?status=PENDED` and `?status=IN_REVIEW` return only rows with that status.
- Any other value, including a status that is not pending such as `APPROVED`, returns 400 with a message naming the allowed values.

### US5122 Show only the over-limit requests

Schedule state: Defined · Estimate: 2 · Owner: Kiran Rao

As a nurse manager, I want the list of requests that are over the business-day limit, so that the team clears them first.

**Acceptance criteria**

- `?overLimit=true` returns only rows whose `overLimit` is true; `?overLimit=false` returns the others.
- The flag is computed for the same `asOf` date as the rest of the response.
- Filters combine: `?tenant=TX-01&overLimit=true` returns rows that match both.
