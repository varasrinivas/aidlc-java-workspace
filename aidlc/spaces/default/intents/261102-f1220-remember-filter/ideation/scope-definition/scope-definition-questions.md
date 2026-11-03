# Scope Definition — Questions

These questions build on the approved intent statement (`ideation/intent-capture/intent-statement.md`). The four stories and their order come from the Rally snapshot for F1220 (`docs-in/rally/F1220/F1220-remember-my-filter.md`). Nothing from it becomes scope unless you confirm it here.

The four stories, for reference:

- US5160 Save and read a reviewer's last filter (Kiran Rao, estimate 3)
- US5161 Open the screen with my last filter (Divya Pillai, estimate 3)
- US5162 Clear my filters (Tara Joshi, estimate 1)
- US5163 Audit every filter change (Arjun Nair, estimate 2)

## Q1. Which stories must ship for F1220 to deliver its value? (select all that apply)

The intent names two problems: re-picking the filter every day, and not being able to explain a missed request. Anything not selected here becomes "should" or "could" for this release.

A. US5160 Save and read a reviewer's last filter
B. US5161 Open the screen with my last filter
C. US5162 Clear my filters
D. US5163 Audit every filter change
E. Not yet defined
X. Other (please specify)

[Answer]: A, B, D. US5162 is a should (Dana Ortiz).

## Q2. If time runs short, which story would you let slip to a later release first?

This tells Delivery Planning what to protect and what to drop if the release date is at risk.

A. US5162 Clear my filters (the smallest story; reviewers can still unpick each control by hand)
B. US5163 Audit every filter change (the nurse-manager need waits)
C. None: all four ship together or the feature does not ship
D. Not yet defined
X. Other (please specify)

[Answer]: A.

## Q3. Is the order between the stories in the Rally snapshot the one to plan by?

The snapshot says: US5160 first; US5163 after US5160 (it records what US5160 saves); US5161 builds against the agreed API contract and can start at once; US5162 after US5161 (the same screen).

A. Yes, exactly that order
B. Mostly, but US5161 should wait until US5160 is merged rather than start against the contract alone
C. A different order (please describe under Other)
D. Not yet defined
X. Other (please specify)

[Answer]: A. US5161 builds against the contract from the start; Divya and Kiran agree the contract in Contract Design.

## Q4. What should guide the sequence when more than one order is possible?

A. Dependency-first: agree the contract and build the saved-filter story before anything that relies on it
B. Value-first: get the restored filter on the reviewers' screen as early as possible
C. Risk-first: build the audit history early, because a missed request it cannot explain is what triggered this
D. Not yet defined
X. Other (please specify)

[Answer]: A.

## Q5. Are there hard deadlines tied to specific stories?

The Rally snapshot places F1220 in release 2027.Q1 R1.

A. One deadline for the whole feature: 2027.Q1 R1, with no earlier milestone for any story
B. 2027.Q1 R1 overall, but one story is needed earlier (please name it and the date under Other)
C. No hard deadline
D. Not yet defined
X. Other (please specify)

[Answer]: A.

## Q6. Is "who may see a reviewer's filter history" in or out of this version's scope?

The intent leaves this open for Dana Ortiz: with no sign-in, anyone who knows a reviewer's login name could read that reviewer's history. Scope needs a position before requirements are written.

A. Out of scope for this version: the history is readable by anyone using the screen, and this is accepted as a known limit of having no sign-in
B. Out of scope, but say it in the release notes alongside the restart limit
C. In scope: limit who may read the history in this version (this would need some way to identify a nurse manager, which the boundary currently leaves out)
D. Not yet decided; Dana Ortiz settles it before Requirements Analysis
X. Other (please specify)

[Answer]: B. Dana Ortiz decided in the session; Meena Iyer adds it to the release-notes line.

## Consolidated Summary Confirmation

- Must have: US5160 (save and read the last filter), US5161 (open the screen with it), US5163 (audit every change). Should have: US5162 (clear my filters), per Dana Ortiz (Q1)
- If time runs short, US5162 slips first (Q2)
- Order as in Rally: US5160 first; US5163 after US5160; US5161 builds against the agreed contract from the start, with Divya and Kiran agreeing it in Contract Design; US5162 after US5161 (Q3)
- Sequencing is dependency-first: agree the contract and build the saved-filter story before what relies on it (Q4)
- One deadline: the whole feature in 2027.Q1 R1, no earlier milestone (Q5)
- Who may see a reviewer's filter history is out of scope for this version; the release notes say so alongside the restart limit, and Meena Iyer adds it to her release-notes line (Dana Ortiz decided) (Q6)

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
