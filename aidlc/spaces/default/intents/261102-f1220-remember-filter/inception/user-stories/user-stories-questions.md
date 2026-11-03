# User Stories — Plan and Questions

## Story Plan

- **Input:** the approved `inception/requirements-analysis/requirements.md`, with requirements FR1-FR7 and NFR1-NFR11.
- **Format:** "As a [persona], I want [goal], so that [benefit]", checked against INVEST. Each story has Given/When/Then acceptance criteria with IDs `AC<group>.<seq>.<n>`.
- **Priority:** MoSCoW, taken from the approved scope (not asked again):
  - US5160, US5161 and US5163 are Must.
  - US5162 is Should, and slips first.
  The MVP line is drawn in Delivery Planning.
- **Personas:** drawn from the approved intent and stakeholder map. Q1 confirms them.
- **Mob:** I draft the stories. Then the designer (screen experience), developer (can it be built, and is it the right size) and quality engineer (can each criterion be tested) each review the draft separately, and I fold their points in.

## Q1. Which personas should the stories be written for?

The intent names reviewers (primary) and nurse managers (secondary, through the history).

A. Two personas: the prior-authorization reviewer and the nurse manager (Ravi Menon's role)
B. Option A, plus a third persona for the team that runs the API (who cares about limits and restarts)
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q2. How do AI-DLC stories map to the four Rally stories?

Your rule is one Rally story = one unit = one branch = one PR, so each Rally story stays one piece of build work. Inside that, the stories can be finer. US5161 now covers the new controls, restore on open, save on change, and two failure cases.

A. One AI-DLC story per Rally story (US1.1 = US5160, US1.2 = US5161, US1.3 = US5162, US1.4 = US5163), each carrying its Rally id, with acceptance criteria covering every requirement
B. Group the stories by Rally story, but split the larger ones into several smaller AI-DLC stories under the same Rally id. For example, US5161 becomes "add the controls", "restore on open" and "save on change". Each Rally story is still one unit and one PR.
C. Not yet decided
X. Other (please specify)

[Answer]: A. One AI-DLC story per Rally story, so each owner reads one story (Meena Iyer).

## Q3. Where do the non-functional requirements go?

NFR1-NFR11 cover limits, safe display, error bodies, cross-origin calls, atomic saves and accessibility. Some of these are visible to a user, and some are not.

A. Put the user-visible ones into the stories as acceptance criteria: escaping, failure messages, keyboard use, limit errors and history trimming. Leave the rest (memory bound, atomic save, browser-call origins, data lifetime, coverage) to NFR Requirements and Design, with the traceability file marking each one Deferred to the stage that owns it.
B. Write separate technical stories for the non-functional requirements as well
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q4. Where does the tenant picker get its list? (raised by the mob)

The picker must offer exactly the tenants the API accepts as known: every tenant in the request export (requirements FR3.1, FR4.6). The developer found that only a new API call can give the screen that list. The F1210 mockup instead builds the list from the pending rows on screen. That would drop a restored tenant that has no pending requests, and Rita would then see a filter the picker can't show.

A. A new read-only call, `GET /tenants`, that answers the known tenants. US1.1 (Kiran Rao) builds it, and Contract Design fixes its shape.
B. Build the list from the pending rows, as in the F1210 mockup. A restored tenant with no pending rows is added to the list anyway, so the picker can show it.
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q5. What does Rita see when the queue itself can't be loaded? (raised by the mob)

Today, when `GET /requests/pending` fails, the table just stays empty with no message. Restoring a filter makes a silently empty table more likely to be mistaken for "nothing pending", which is the missed-request problem F1220 exists to fix. No requirement covers this yet, so adding one is new scope.

A. Add it to US1.2: when the queue can't be loaded, the screen says so in text, distinct from "No requests match this filter", and the controls still work
B. Leave it as it is today: out of scope for F1220
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q6. Reviewer ids made only of dots (raised by the mob)

FR1.3 allows letters, digits, `.`, `-` and `_`. The developer found that the web server reroutes the ids `.` and `..` before the API code sees them, so they would get 404 instead of the required 400.

A. Narrow FR1.3: a reviewer id must also contain at least one letter or digit, so `.` and `..` are invalid. The API still answers 404 for those two because the server reroutes them first, and the story says so.
B. Keep FR1.3 as written, and let the acceptance criterion accept 404 for `.` and `..`
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Consolidated Summary Confirmation

- Two personas: the prior-authorization reviewer and the nurse manager (Ravi Menon's role) (Q1)
- One AI-DLC story per Rally story, each carrying its Rally id: US1.1 = US5160, US1.2 = US5161, US1.3 = US5162, US1.4 = US5163; acceptance criteria cover every requirement, so each owner reads one story (Meena Iyer) (Q2)
- User-visible NFRs become acceptance criteria (escaping, failure messages, keyboard use, limit errors, history trimming); the rest (memory bound, atomic save, browser-call origins, data lifetime, coverage) are marked Deferred to NFR Requirements and Design (Q3)
- Priorities as approved in scope: US5160, US5161, US5163 Must; US5162 Should
- Tenant picker list comes from a new read-only `GET /tenants` call, built in US1.1 (Kiran Rao); shape fixed in Contract Design (Q4)
- New in US1.2: when the queue itself can't be loaded, the screen says so in text, distinct from "No requests match this filter", and the controls still work (Q5)
- FR1.3 narrowed: a reviewer id must also contain at least one letter or digit; `.` and `..` get 404 because the server reroutes them first (Q6)
- Folded in from the mob: browser-call origins (CORS) built in US1.1 for the new endpoints and `/requests/pending`; testable accessibility checks (markup automated, keyboard manual at Build and Test); deterministic quick-change test (saves exactly A then C); new criteria for parallel saves, case-sensitive ids, safe errors on history, empty-result message, one announced message area cleared on the next successful save, no flash of the whole queue on open, focus to the Tenant picker after Clear; limits tested on a fresh store; concrete bad bodies and a 1,024-byte boundary; NM-02 test impact named in US1.1

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
