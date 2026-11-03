# Requirements: US5161 Open the screen with my last filter (F1220, unit U2 `us5161-restore-filter`)

This story's requirements come from the parent feature intent `261102-f1220-remember-filter`. The IDs FR4, FR5, NFR5 and NFR10 and the assumption A1 are the parent's, quoted unchanged so traceability holds. Only FR4.7, FR4.8 and FR4.9 are new. They come from this stage's questions Q1-Q4 and close cases the parent's criteria leave open. Nothing the parent approved is reopened here.

## Sources

| Tag | Source |
|---|---|
| Parent RA | `261102-f1220-remember-filter/inception/requirements-analysis/requirements.md` (approved) |
| Story | `261102-f1220-remember-filter/inception/user-stories/stories.md`, US1.2, AC1.2.1-AC1.2.12 (approved) |
| Unit | `261102-f1220-remember-filter/inception/units-generation/unit-of-work.md`, U2 (approved) |
| Contract | `261102-f1220-remember-filter/inception/contract-design/contract-summary.md` and `examples/`, C1, C2, C4 (approved) |
| Bolt | `261102-f1220-remember-filter/inception/delivery-planning/bolt-plan.md`, B2 (approved) |
| codekb | `codekb/priorauth-web/` (reused, unchanged since the parent's Reverse Engineering) |
| Practices | `memory/team.md`, `memory/project.md` |
| Q<n> | `requirements-analysis-questions.md` in this folder, question n |

## Intent Analysis

- **Goal:** Rita the Reviewer opens the queue with the filter she used last, on any browser, and her changes are remembered. (Story US1.2)
- **Type:** an enhancement in the brownfield repo `priorauth-web` only. The API side is US5160 (U1), and this story builds against the agreed contract, not against U1's merged code. (Unit U2)
- **Complexity:** Minimal depth with L size. The tenant picker and the "over limit only" switch F1210 never added to the page come first (FR4.2). The ordering rules for saves and late reads are the risky part. (Unit U2; Bolt B2)
- **Branch:** `f1220/us5161-restore-filter`, cut from `origin/feature/F1220`. The PR goes into `feature/F1220`. (Project description; Practices)

## Functional Requirements

### FR4 Open the screen with the reviewer's last filter (parent, unchanged)

- **FR4.1** The screen takes the reviewer from its `?reviewer=` page parameter. (Parent RA)
- **FR4.2** US5161 adds a tenant picker and an "over limit only" switch to the page. (Parent RA; AC1.2.1)
- **FR4.3** On open, the screen reads the reviewer's saved filter. It then asks the queue with that filter, and the controls show it. A loading text is shown until the saved filter is read, and the unfiltered queue is never shown first. (Parent RA; AC1.2.2)
- **FR4.4** With no saved filter (`{}`), or `{"tenant": null, "overLimit": false}`, the screen opens unfiltered. (Parent RA; AC1.2.3)
- **FR4.5** If the saved filter can't be read, the screen opens unfiltered and says the saved filter couldn't be loaded. The queue still loads. (Parent RA; AC1.2.4)
- **FR4.6** The picker offers exactly the tenants `GET /tenants` (C2) returns, plus "All tenants". (Parent RA; AC1.2.1; Contract C2)

### FR4 additions from this story (new)

- **FR4.7 Tenant list can't be loaded.** When `GET /tenants` fails (a timeout, a network error or a non-2xx answer), the picker offers only "All tenants", plus the saved tenant if there is one. The queue still loads with the saved filter, and the message area says the tenant list couldn't be loaded. (Q1 B, decided by Divya Pillai with Tara Joshi)
  - Pass/fail: with a stubbed `GET /tenants` that fails and a saved filter of `{"tenant": "TX-01", "overLimit": true}`, the rendered picker holds exactly "All tenants" and TX-01, TX-01 is selected, the queue is asked for TX-01 over-limit requests, and the message is the tenant-list message.
- **FR4.8 Saved tenant no longer known.** When the tenant list loads, and the saved tenant isn't in it, the screen drops the saved tenant. It opens with "All tenants" and keeps the saved over-limit switch. The message area says the saved filter couldn't be loaded. Nothing is saved until the reviewer changes a control. (Q2 B)
  - Pass/fail: with `GET /tenants` answering `["NM-02", "TX-01"]` and a saved filter of `{"tenant": "ZZ-99", "overLimit": true}`, "All tenants" is selected, the switch is on, the queue is asked for over-limit requests with no tenant, the saved-filter message shows, and no `PUT` is sent.
  - When the tenant list itself failed, FR4.7 applies instead: there is no list to check against, so the saved tenant is kept.
- **FR4.9 Which message shows.** The one message area (`role="status"`) shows the highest message still in force, in this fixed order, highest first (Q3 A; Q4 B):
  1. "The queue couldn't be loaded" (AC1.2.12)
  2. "Your filter wasn't saved" (AC1.2.6)
  3. "The tenant list couldn't be loaded" (FR4.7)
  4. "Your saved filter couldn't be loaded" (AC1.2.4, FR4.8)
  5. "Open this page from your reviewer link to have your filter remembered" (AC1.2.9)

  When a higher message clears, the next one still in force shows. Each message clears as the story says: "wasn't saved" on the next successful save, and the "couldn't load" messages on the next successful load of the same call. (Story US1.2 common behaviour)
  - Pass/fail: with the saved-filter read and the queue both failing on open, the area shows the queue message. After the next change loads the queue, it shows the saved-filter message.
  - "No requests match this filter" is shown in the table, not the message area, so it is outside this order. (AC1.2.11)

### FR5 Save the filter when a control changes (parent, unchanged)

- **FR5.1** A change to the picker or the switch asks the queue with the new filter and saves it. (Parent RA; AC1.2.5)
- **FR5.2** If the save fails, the queue keeps the reviewer's new filter and the message area says it wasn't saved. A later successful save clears it. (Parent RA; AC1.2.6)
- **FR5.3** Only the latest queue answer is shown. Saves go one at a time, and a waiting save is replaced by a newer one. Three quick changes A, B, C send exactly A then C, and the stored filter is C. (Parent RA; AC1.2.7)

### Other approved criteria this story carries

- **R-06 / AC1.2.8** A change made before the saved-filter read answers wins: it is applied and saved, and the read's later answer is ignored. Divya Pillai covers it in the code plan, with a test. (Story; Bolt B2)
- **A1 / AC1.2.9** Without `?reviewer=`, the screen shows the whole queue and the controls still filter it. Nothing is read or saved, and the message area says the filter won't be remembered. (Parent RA A1)
- **AC1.2.11** An empty queue answer shows "No requests match this filter" and a count of 0.
- **AC1.2.12** A failed `GET /requests/pending` shows the queue message, and the empty-result text is not shown. The controls stay usable, and the next change tries again.

## Non-Functional Requirements (parent, unchanged)

- **NFR5 Safe display:** every API value shown on the screen goes through the shared `esc` helper, including `&`, `<`, `>`, `"` and `'` (`'` renders as `&#39;`). That covers tenant ids in the picker, including a saved tenant kept by FR4.7. (Parent RA; AC1.2.10)
- **NFR10 Accessibility:** the picker and the switch are native controls with visible labels (`<label for>`), they work by keyboard, and failures are shown in text in a `role="status"` area. Keyboard use is checked by hand at the feature's Build and Test. (Parent RA; AC1.2.1)
- **NFR8 / NFR11 Compatibility and tests:**
  - The screen's 6 existing tests keep passing (baseline: 6 of 6 at `65a999b`).
  - Each new branch has a test, and each new or changed test file covers the happy path and two edge cases.
  - Coverage is reported as NOT MEASURED.
  - (Parent RA; Practices)

## Constraints

- **Repo:** only `priorauth-web` changes. The new modules are `FilterSession` and `SavedFilterClient`. The changed ones are `index.html` (a thin caller), `QueueFilters` (the one `overLimitOnly` to `overLimit` mapping) and `QueueRenderer`. (Unit U2)
- **Screen logic:** all of it lives in DOM-free `src/` modules with an injected `fetchFn`. `index.html` only calls them. (Practices)
- **Calls:** every call from the screen gives up after 10 seconds. A timeout, a network error or a non-2xx answer is a failure, and there are no automatic retries. Save bodies carry exactly `tenant` and `overLimit`. (Contract C1, C2, C4)
- **Contract examples:** the examples for C1, C2 and C4 are copied into the screen tests. (Unit U2; Bolt B2)
- **Dependencies:** none are added. Any new one is named in the code plan first. (Practices)
- **Tests:** they run through `scripts\verify.cmd priorauth-web` (Windows) or `scripts/verify.sh priorauth-web`. (Practices)

## Assumptions

- **A5** After `GET /tenants` fails, the reviewer's next change asks for the tenant list again, along with the queue. A success then fills the picker and clears the tenant-list message. Reason: the contract says "The reviewer's next change or a reload tries again" for every call, and FR4.9 clears a "couldn't load" message on the next successful load. Correct it at the gate if the list should be read only on open.
- **A6** The tenant-list message text is "The tenant list couldn't be loaded." It follows the story's statement-of-fact style, and the wording can change in code review like the others.

## Out of Scope

- "Clear filters" (US5162, U3), the history (US5163, U4), and every API change (US5160, U1).
- Automatic retries, and browser or DOM tests.

## Open Questions

None for this story. The full demo needs U1 merged into `feature/F1220`. Until then the screen is proven against the contract examples with stubbed calls. (Bolt B2)
