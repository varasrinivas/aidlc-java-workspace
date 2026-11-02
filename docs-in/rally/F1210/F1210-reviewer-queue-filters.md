# F1210 Reviewer queue filters, end to end

> Snapshot of a Rally feature and its user stories, written by `scripts/export-rally.py` (offline, from F1210.json).
> Rally is the source of truth: refresh this file before `/aidlc`, and cite the story IDs (US…) in requirements.

| Field | Value |
|---|---|
| Epic | E212 Reviewer screen v2 |
| State | Ready |
| Owner | Dana Ortiz |
| Release | 2026.Q4 R3 |
| Last updated in Rally | 2026-11-02 |
| Stories | 4 |

## Feature description

Reviewers scroll one long queue across every health plan. Let them narrow it on the screen, by tenant and to the over-limit rows only. The API gets the filters, the reviewer screen gets the controls.

Four stories, four developers. **US5150** lays the shared plumbing that US5151 and US5152 build on; **US5153** builds the screen against the API contract agreed before Construction, so it does not wait for the merge.

## User stories

### US5150 Shared filter parameters on the pending list

Schedule state: Defined · Estimate: 2 · Owner: Kiran Rao

As a developer of the reviewer queue, I want one place where the pending list's filters are read and applied, so that each filter story adds a field, not a new code path.

**Order:** first. US5151 and US5152 start their code after this story is merged into the feature branch.

**Acceptance criteria**

- `GET /requests/pending` without filters returns exactly what it returns today.
- Filters are read into one `RequestFilter` and applied in one place, after aging.
- An unknown query parameter is ignored, as today.

### US5151 Filter the pending list by tenant

Schedule state: Defined · Estimate: 2 · Owner: Arjun Nair

As a reviewer who covers one health plan, I want the pending list for my tenant only, so that I don't scroll past other plans' requests.

**Order:** after US5150. Add a second tenant (NM-02) to the sample data so this story can be tested.

**Acceptance criteria**

- `GET /requests/pending?tenant=TX-01` returns only TX-01 rows, oldest first.
- Without `tenant`, every tenant is returned.

### US5152 Show only the over-limit requests

Schedule state: Defined · Estimate: 1 · Owner: Tara Joshi

As a nurse manager, I want only the requests over the business-day limit, so that the team clears them first.

**Order:** after US5150. Works together with US5151's tenant filter.

**Acceptance criteria**

- `?overLimit=true` returns only rows whose `overLimit` is true.
- `?tenant=TX-01&overLimit=true` applies both filters.

### US5153 Filter controls on the reviewer screen

Schedule state: Defined · Estimate: 3 · Owner: Divya Pillai

As a reviewer, I want a tenant picker and an "over limit only" switch above the queue, so that I can narrow it without typing a URL.

**Order:** builds against the API contract agreed in the feature's design; it can start at once and is tested against the API when US5151 and US5152 are merged.

**Acceptance criteria**

- The controls call `tenant` and `overLimit` on `GET /requests/pending`.
- The list and the count above it change together.
