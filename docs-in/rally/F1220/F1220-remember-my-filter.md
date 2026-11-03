# F1220 Remember my filter

> Snapshot of a Rally feature and its user stories, written by `scripts/export-rally.py` (offline, from F1220.json).
> Rally is the source of truth: refresh this file before `/aidlc`, and cite the story IDs (US…) in requirements.

| Field | Value |
|---|---|
| Epic | E212 Reviewer screen v2 |
| State | Ready |
| Owner | Dana Ortiz |
| Release | 2027.Q1 R1 |
| Last updated in Rally | 2026-11-03 |
| Stories | 4 |

## Feature description

F1210 gave reviewers a tenant filter and an "over limit only" switch. Every morning they set them again. Remember each reviewer's last filter on the server, so it follows them to any browser, restore it when the screen opens, give them one control to clear it, and keep an audit line of every change, because the filter decides which requests a reviewer sees first.

Four stories, four developers. **US5160** is the API the others use; **US5163** extends it; **US5161** builds the screen against the agreed contract; **US5162** changes the same screen after US5161.

## User stories

### US5160 Save and read a reviewer's last filter

Schedule state: Defined · Estimate: 3 · Owner: Kiran Rao

As a reviewer, I want the API to keep my last filter, so that the screen can give it back to me on any computer.

**Order:** first. US5161 and US5163 depend on it. No database in this product yet: keep the filters in memory, behind one class the next feature can replace.

**Acceptance criteria**

- `PUT /reviewers/{reviewerId}/filter` with `{"tenant": "TX-01", "overLimit": true}` saves it and answers 204.
- `GET /reviewers/{reviewerId}/filter` returns the last saved filter, or `{}` when there is none (200).
- A tenant the export doesn't know is refused with 400; the saved filter stays as it was.

### US5161 Open the screen with my last filter

Schedule state: Defined · Estimate: 3 · Owner: Divya Pillai

As a reviewer, I want the queue to open with the filter I used last, so that I don't pick it every morning.

**Order:** builds against the contract agreed in the feature's design; it can start at once. US5162 changes the same screen after it.

**Acceptance criteria**

- On load the screen reads the saved filter and asks the queue with it; the controls show it.
- Changing a control saves the new filter.
- With no saved filter the screen opens unfiltered, as today.

### US5162 Clear my filters

Schedule state: Defined · Estimate: 1 · Owner: Tara Joshi

As a reviewer, I want one control that clears the tenant and the over-limit switch, so that I see the whole queue again without unpicking each control.

**Order:** after US5161: the same screen code.

**Acceptance criteria**

- "Clear filters" resets both controls, shows the whole queue and saves the empty filter.
- It is disabled when no filter is set.

### US5163 Audit every filter change

Schedule state: Defined · Estimate: 2 · Owner: Arjun Nair

As a nurse manager, I want a record of who changed their filter to what and when, so that I can tell why a reviewer didn't see a request.

**Order:** after US5160: it records what US5160 saves.

**Acceptance criteria**

- Every saved filter writes one audit line: time (UTC), reviewer, tenant, overLimit.
- `GET /reviewers/{reviewerId}/filter/history` returns that reviewer's lines, newest first.
- A refused save (unknown tenant) writes no line.
