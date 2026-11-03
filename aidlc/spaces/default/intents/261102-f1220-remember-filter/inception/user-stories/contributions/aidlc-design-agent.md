**Collaborator:** aidlc-design-agent

## Contribution

Lens: what Rita and Nina actually see and do, whether every screen state is covered, accessibility (NFR10), message wording, and consistency with the F1210 mockup (`docs-in/rally/F1210/US5153/queue-filters-mockup.md`, read as customer data). Points are numbered so the lead can fold them in one by one. Each new criterion I propose names its origin, because the inception rules say no requirement may enter without one. Where a point goes beyond the approved requirements, I say so and leave the decision to the gate.

### D1. Screen states for US1.2: what the draft leaves undefined

The draft covers the happy path (AC1.2.2, AC1.2.5), failed reads and saves (AC1.2.4, AC1.2.6), races (AC1.2.7, AC1.2.8) and the missing reviewer (AC1.2.9). Four states that Rita will actually meet are not defined:

**D1.1 Loading on open (refines AC1.2.2; origin FR4.3).** AC1.2.2 says the screen asks the queue with the saved filter. It does not rule out loading the whole queue first and swapping it out when the saved filter arrives. Rita would then see unfiltered rows for a moment and could open one before the swap. Proposed addition to AC1.2.2: "...and the screen does not show the unfiltered queue before the saved filter is applied. Until the saved filter answers, the table area shows a loading text (for example "Loading your requests…") and the controls can already be used (AC1.2.8)." The controls stay usable, so a slow or hanging read never traps her. AC1.2.8 already makes her change win.

**D1.2 Empty filtered result (new AC1.2.11; origin FR4.3, FR5.1, NFR10).** Today an empty answer leaves a blank table with no text. Once F1220 lands, a restored filter is the most likely reason for an empty queue, for example TX-01 plus over-limit with nothing pending. A blank table that nobody explains, under a filter Rita did not set today, is the same "why didn't she see the request" situation that prompted this feature. Proposed AC1.2.11: "Given the queue answers with no rows for the active filter, then the table area says in text that no pending requests match this filter, and the count shows 0. When a filter is set, 'Clear filters' is next to that text." The Clear filters part applies only once US1.3 merges. Tie it to US1.3 with a cross-reference, not a dependency, so US1.2 stays independently testable.

**D1.3 Stale rows while a change loads (refines AC1.2.5 and AC1.2.7; origin FR5.1, FR5.3).** Between a change and its queue answer, the table still holds rows for the previous filter. Proposed addition to AC1.2.5: "...while the new queue answer is pending, the table is marked as updating (in text, and with `aria-busy` on the table region), so the old rows are not presented as the new filter's result." This is low cost and stops Rita from acting on a row that is about to disappear.

**D1.4 The queue call itself fails (open question; not in the approved requirements).** FR4.5 and AC1.2.4 assume "the queue still loads". Nothing says what Rita sees when `GET /requests/pending` fails. Today she gets an empty table and a console error (codekb architecture: "Improvement Opportunities"). With D1.2 in place, a failed queue call must not show the "no requests match" text, because that would tell her that nothing is pending when the truth is unknown. I am not adding a criterion, because that would be a new requirement. I ask the lead to raise it at the gate. The two options are a text message such as "Requests couldn't be loaded. Reload to try again." (origin: codekb improvement item plus NFR10) or an explicit out-of-scope line. At minimum, the empty-state text in D1.2 must appear only after a successful empty answer.

### D2. Messages: one region, announced, with a defined lifetime (AC1.2.4, AC1.2.6, AC1.2.9, AC1.3.4)

The draft says "a short text message" four times but never says where the message appears, how a screen-reader user learns of it, or when it goes away.

**D2.1 One status region, announced without moving focus (origin NFR10).** Proposed shared criterion, added to US1.2 and referenced by AC1.3.4: "Failure and notice messages appear in one message area above the table, in text. Screen readers announce them (a polite live region, `role="status"`) without moving keyboard focus. A new message replaces the previous one; messages never stack."

**D2.2 Lifetime (refines AC1.2.4 and AC1.2.6).** If a "wasn't saved" message stays on screen after Rita's next change saves, it is false and teaches her to ignore the area. Proposed: "A 'couldn't be loaded' or 'wasn't saved' message is removed when a later save succeeds." The AC1.2.9 note about a missing reviewer is permanent for that page visit, because nothing can fix it without reloading.

**D2.3 Success is silent (confirms the draft).** A successful save shows nothing: no toast and no "Saved" flash. Rita changes the filter many times a day, and confirmation noise would hide the failure messages that matter. I suggest the lead add one sentence saying so, so that Code Generation does not add a toast.

**D2.4 Wording.** Messages are fixed text written into the region with `textContent`. They never include the reviewer id or any other value from the address or the API, which keeps NFR5 and NFR4 simple. Proposed copy, to be fixed before US1.2's code plan because US1.3 reuses it:

| Case | Proposed text | Why this wording |
|---|---|---|
| AC1.2.4 read failed (unreachable or error) | "Your saved filter couldn't be loaded. Showing all requests." | Says what happened and what she now sees. |
| AC1.2.4 read answered 400 for the reviewer id | "The reviewer name in the address isn't valid, so your filter can't be saved or restored." | Retrying won't help here, unlike a network failure. Without this, every later change also shows "wasn't saved", which would be confusing. This is wording only; behaviour stays as FR4.5 says. |
| AC1.2.6, AC1.3.4 save failed | "Your filter change wasn't saved. It works on this screen now but won't be restored next time." | Honest about the consequence. "Wasn't saved" alone doesn't tell her what she loses. |
| AC1.2.9 no reviewer (absent or empty `?reviewer=`) | "Your filter won't be remembered because no reviewer is named in the address." | Names the cause. Rita knows the `?reviewer=` convention (persona context). |
| D1.2 empty result | "No pending requests match this filter." | Puts the empty table down to the filter, not to the queue. |

The quality engineer may want the criteria to match these strings exactly. If so, the lead should put the table into US1.2 as the source for AC1.2.4, AC1.2.6, AC1.2.9 and AC1.2.11.

**D2.5 Empty reviewer parameter (refines AC1.2.9; origin A1).** `?reviewer=` with an empty value should behave as if the parameter were absent: no read, no save, and the note is shown. Without this, an empty id gets a 400 on read and on every save.

### D3. Controls: match the F1210 mockup and make NFR10 testable (AC1.2.1)

**D3.1 Labels and control types match the mockup.** The mockup shows `Tenant: [ All tenants v ]` and `[x] Over limit only`. AC1.2.1 calls the second control a "switch". I recommend the criterion name a native select labelled "Tenant" and a native checkbox labelled "Over limit only", each with an associated `<label>`. A "switch" invites a custom toggle widget, which needs `role="switch"` and its own keyboard handling, a risk the native checkbox avoids. The mockup already shows a checkbox. Proposed wording for AC1.2.1: "...a tenant select labelled 'Tenant', offering 'All tenants' first and then the known tenants, and a checkbox labelled 'Over limit only'. Both are native form controls with visible labels, reachable with Tab in visual order, and keep a visible focus outline."

**D3.2 Group the controls.** Put the select, the checkbox and (from US1.3) "Clear filters" in one group with an accessible name, for example a `fieldset` with the legend "Filter requests". The group sits under the "Pending requests" heading, as in the mockup. Screen-reader users then hear one filter area, and US1.3 has a defined place for its button: after the checkbox, on the same row.

**D3.3 The count follows the filter (refines AC1.2.2, AC1.2.5, AC1.3.1; origin: the mockup and the existing `loadQueue` contract of `{ rows, count }`).** The mockup says the count is the length of the returned list. The criteria should say "the table and the count show the filtered list". A broken count is the first thing Rita would notice. I recommend the count element also be a polite live region, so a screen-reader user hears the result of a change ("3 requests") without searching for it (NFR10). The existing `countLabel` text ("N requests") stays. The mockup's "12 shown" was a sketch, and F1220 should not change copy that nobody asked to change.

**D3.4 Keyboard select and history noise (note for US1.4 and for Nina).** In Chromium on Windows, pressing the arrow keys on a closed select fires `change` for each option passed. Each press then re-queries and saves, and each completed save writes a history line (FR7.1). AC1.2.7 drops only the saves queued behind one in flight. With two tenants this is minor and acceptable. Nina should still know that a history line can be a tenant a keyboard user passed through, not one they chose to work under. I suggest one sentence in the persona context (see D5.2). I do not propose a design change.

**D3.5 The mockup's tenant source conflicts with FR4.6.** The mockup says "The tenant list comes from the rows of the unfiltered list". FR3.1 defines known tenants as any request in the export, pending or not, and FR4.6 says the picker offers exactly those. Taking the list from pending rows breaks restore. A restored tenant with no pending requests would be missing from the picker, so the control could not show what is applied, and AC1.2.2 would fail. Taking it from the unfiltered rows also costs an extra unfiltered call on open, which conflicts with D1.1. AC1.2.1 already leaves the source to Domain and Contract Design (OQ2), which is correct. I ask the lead to note the conflict next to OQ2 so that design does not adopt the mockup's rule by default. A second sentence in the mockup is also out of date: "the last choice is kept in the browser … US5131". F1220 restores from the API only. The stories should say nothing is stored in the browser, so nobody adds `localStorage` as a fallback.

### D4. US1.3 Clear filters

**D4.1 AC1.3.2 is an either/or and cannot be tested ("skipped or announced as unavailable").** Pick one. Recommended: a native `<button disabled>`. Browsers then leave it out of the Tab order, screen readers report it as unavailable when reading the page, and its disabled look is not colour alone. Proposed AC1.3.2: "...then 'Clear filters' is a disabled native button: it is not in the Tab order, and assistive technology reports it as unavailable."

**D4.2 Focus after clearing (new AC1.3.5; origin NFR10).** With D4.1, activating "Clear filters" disables the button that has keyboard focus. Browsers then drop focus to the page body, and a keyboard or screen-reader user loses their place. That is an accessibility defect the current criteria would let through. Proposed AC1.3.5: "When Rita activates 'Clear filters' by keyboard, focus moves to the Tenant select, and the count announcement (D3.3) reports the full queue."

**D4.3 Enabled state follows restore, not only Rita's own changes (refines AC1.3.3).** AC1.3.3 says "when Rita sets any filter". A restored filter (AC1.2.2) must also enable the button, and a failed read (AC1.2.4) leaves it disabled. Proposed addition: "...or when a saved filter with a tenant or the switch on is restored on open."

**D4.4 Clearing counts as a change (new AC1.3.6; origin FR5.3, R-06).** For US1.3 to be testable on its own, it needs its own criterion for the race rules it inherits: "Clear filters" counts as a change for AC1.2.7 (the latest choice is the last save sent and the only queue answer shown) and for AC1.2.8 (clearing before the saved filter arrives wins).

**D4.5 AC1.3.4 wording.** The message comes from the D2.4 table, in the D2.1 region. After a failed save, the button is still disabled, because the screen now shows no filter.

### D5. Persona fidelity

**D5.1 US1.1 actor.** "Rita … wants the API to keep my last queue filter" puts words in Rita's mouth that she would never say. She has never seen the API. I suggest "**As** Rita the Reviewer, **I want** my last queue filter kept for me, **so that** the screen can restore it on any computer." The criteria stay API-level, which is right for an API-only story. Wording only.

**D5.2 Nina's trust boundary (personas.md, P2 Context).** The persona lists four limits from A2. One more matters most for her goal, "what filter the reviewer had at the time": the history records *saved* filters, not what was on the screen. A filter used with no reviewer in the address (AC1.2.9), or one whose save failed (AC1.2.6), is on Rita's screen but not in Nina's history. Proposed addition to the P2 Context: "Knows the history shows saved filters only: a filter used without a reviewer in the address, or one whose save failed, does not appear." I suggest Meena Iyer's release-notes line (A2) carry the same sentence.

**D5.3 Nina reads raw JSON.** With medium tech comfort and no screen view (FR7.6), Nina will open the history URL in a browser tab or ask a developer. That is acceptable for this version, and it means AC1.4.7 should say the history can be read by opening the URL directly. The times are UTC (AC1.4.1). The persona should say she converts them to local time when matching a missed request.

**D5.4 Reviewer id in the history line (for the lead and the quality engineer).** FR7.1 lists "the reviewer id" as a field of each line. The FR7.3 shape and AC1.4.1 leave it out, because the reviewer is already in the URL. Either way works for Nina, but the requirement and the criterion should agree. Raise it with Contract Design rather than leave the mismatch.

### D6. Summary of proposed edits by AC

| AC | Change |
|---|---|
| AC1.2.1 | Native select "Tenant" and native checkbox "Over limit only", labelled, grouped, with visible focus (D3.1, D3.2); note the mockup/FR4.6 conflict next to OQ2 (D3.5) |
| AC1.2.2 | No unfiltered flash; loading text; the count follows the filter (D1.1, D3.3) |
| AC1.2.4 | Message area, wording, cleared after a later successful save; separate wording for an invalid id (D2) |
| AC1.2.5 | Table marked as updating while the answer is pending; the count follows the filter (D1.3, D3.3) |
| AC1.2.6 | Message wording and lifetime (D2.2, D2.4) |
| AC1.2.9 | An empty `?reviewer=` counts as absent; the note stays for the visit (D2.5) |
| AC1.2.11 (new) | Empty filtered result text (D1.2) |
| Open question | What happens when the queue call fails (D1.4) |
| AC1.3.2 | Native disabled button; remove the either/or (D4.1) |
| AC1.3.3 | A restore also enables the button (D4.3) |
| AC1.3.5 (new) | Focus moves to the Tenant select after clearing (D4.2) |
| AC1.3.6 (new) | Clear counts as a change for AC1.2.7 and AC1.2.8 (D4.4) |
| US1.1 story line | Rita-centred wording (D5.1) |
| personas.md P2 | Saved filters only; UTC; keyboard passes (D3.4, D5.2, D5.3) |

## Positions

- AGREE: One AI-DLC story per Rally story (Q2). Each owner reads one story, and the screen work splits along the US5161/US5162 line without leaving a state unowned.
- AGREE: AC1.2.8 (a change before the saved filter arrives wins) is the right call for Rita. Her action always beats a background answer, which also keeps the controls usable during a slow read.
- AGREE: AC1.2.9 (no reviewer means an unfiltered, working screen plus a note). The screen degrades instead of failing, and the note names the cause. The only refinement is that an empty parameter counts as absent (D2.5).
- AGREE: AC1.2.10 and NFR5 for picker and table values. Messages should avoid the issue by being fixed text (D2.4).
- AGREE: No history view on the screen (AC1.4.7, FR7.6), provided Nina's persona states what the history does and does not show (D5.2).
- OBJECT: AC1.3.2 is an either/or ("skipped or announced") that cannot be tested, and with a disabled button nothing says where focus goes after clearing. Fix it with a native disabled button (D4.1) and add focus to the Tenant select (AC1.3.5, D4.2).
- OBJECT: US1.2 has no empty-result state. A restored filter that matches nothing shows a blank, unexplained table, which is the missed-request situation behind F1220. Add AC1.2.11 (D1.2), and make it distinguishable from a failed queue call (D1.4).
- OBJECT: The failure messages in AC1.2.4, AC1.2.6, AC1.2.9 and AC1.3.4 have no location, no screen-reader announcement and no lifetime. A "wasn't saved" message that outlives a later successful save is false. Add the shared status region and the clear-on-success rule (D2.1, D2.2).
- OBJECT: AC1.2.2 does not stop the screen from showing the unfiltered queue before the saved filter applies, which would let Rita act on the wrong rows. Add the no-flash and loading-text clause (D1.1).
