# Intent Capture & Framing — Questions

## Sources

- [desc] Initial description: "Rally F1220 Remember my filter: four stories, four owners (US5160 Kiran, US5161 Divya, US5162 Tara, US5163 Arjun). See docs-in/rally/F1220/ and docs-in/specs/F1220/."
- [scope] Workflow-selected scope: `feature`.

The questions below are shaped by the Rally snapshot (`docs-in/rally/F1220/F1220-remember-my-filter.md`) and the draft API contract (`docs-in/specs/F1220/reviewer-filter-api-spec.md`). Nothing from those documents goes into the deliverables unless you confirm it in an answer here.

## Q1. What business problem is F1220 solving?

The Rally feature says reviewers set the tenant filter and the "over limit only" switch again every morning, and that the filter decides which requests a reviewer sees first.

A. Reviewers lose time re-picking the same filter every day; remembering it on the server (so it follows them to any browser) removes that chore
B. Option A, plus: nobody can tell afterwards why a reviewer did not see a request, because filter changes leave no record
C. Mainly the missing record of filter changes (option B's second half); the convenience is secondary
D. Not yet defined
X. Other (please specify)

[Answer]: B. Decided in the mob session (Dana Ortiz, Ravi Menon, Meena Iyer; Kiran, Arjun, Tara, Divya present).

## Q2. Who are the customers, and are they internal or external?

The stories name two roles: the reviewer (US5160, US5161, US5162) and the nurse manager (US5163).

A. Internal prior-authorization reviewers (primary) and their nurse managers (secondary, for the audit trail)
B. Internal reviewers only; the nurse manager is a stakeholder, not a user of this version
C. External users (for example, provider-side staff) as well as internal reviewers
D. Not yet defined
X. Other (please specify)

[Answer]: A. Reviewers first; nurse managers use the history (Ravi Menon).

## Q3. What does success look like, and how will you measure it? (select all that apply)

Each option is a measurable outcome; pick the ones that matter for this feature.

A. When a reviewer has a saved filter, the screen opens with it applied every time, on any browser (no manual re-pick)
B. Every successful filter save has exactly one audit line, and a refused save (unknown tenant) has none
C. A nurse manager can answer "why didn't this reviewer see request X?" from the filter history alone
D. A measured drop in time from opening the screen to starting the first review (a baseline would need to be taken first)
E. Not yet defined
X. Other (please specify)

[Answer]: A, B, C. Not D: we have no baseline and won't take one for this release (Dana Ortiz).

## Q4. What triggered this feature now?

The Rally snapshot places F1220 in epic E212 "Reviewer screen v2", release 2027.Q1 R1, right after F1210 shipped the filters.

A. Reviewer feedback after F1210: the filters help but resetting them daily is a chore
B. A nurse manager or audit need: a missed request could not be explained
C. Both A and B
D. It is the planned next step of the Reviewer screen v2 epic for the 2027.Q1 R1 release; no specific incident
E. Not identified
X. Other (please specify)

[Answer]: C. Reviewers asked for it in the F1210 demo; Ravi could not explain a missed request last month.

## Q5. Who are the key stakeholders, and what does each care about? (select all that apply)

The Rally snapshot names Dana Ortiz as the feature owner; the API draft names Meena Iyer as tech lead; the four story owners are Kiran Rao (US5160), Divya Pillai (US5161), Tara Joshi (US5162) and Arjun Nair (US5163).

A. Dana Ortiz, product owner: the feature lands in 2027.Q1 R1 and is accepted after the feature demo
B. Meena Iyer, tech lead: the API contract is agreed first so the four stories can be built in parallel
C. The four story owners: each delivers one story, in the order the feature sets (US5160 first; US5162 after US5161; US5163 after US5160)
D. Reviewers and nurse managers as end users (see Q2)
E. Not identified
X. Other (please specify, for example compliance or another team)

[Answer]: A, B, C, D.

## Q6. Who decides scope and priority, and who influences it?

A. Dana Ortiz (product owner) decides scope and priority; Meena Iyer (tech lead) decides how it is built and the order of stories; the story owners influence
B. Dana Ortiz and Meena Iyer decide together; the story owners influence
C. Someone else decides (please name them under Other)
D. Not yet defined
X. Other (please specify)

[Answer]: A.

## Q7. What communication or reporting is expected while this is built?

A. The team's usual Rally routine: each owner moves their story to In-Progress when work starts and to Completed when its PR merges into the feature branch, pastes the PR link and intent id into the story's Discussion; Dana accepts after the feature demo
B. Option A, plus a regular status update to the product owner (please give the cadence under Other)
C. No formal reporting beyond the pull requests
D. Not yet defined
X. Other (please specify)

[Answer]: A.

## Q8. What does this first version deliberately leave out? (select all that apply)

The workflow covers the whole feature (`feature`); this question is only about what the product itself will not do yet.

A. A real database: filters and their history are kept in memory behind one replaceable class
B. Sign-in: the reviewer is identified by a login name the screen passes along, with no authentication
C. More than one saved filter per reviewer, or filter fields beyond tenant and over-limit
D. Exporting the audit history or keeping it for a set retention period
E. None: nothing is deliberately left out
X. Other (please specify)

[Answer]: A, B, C, D.

## Q9. Is it acceptable that the filter history disappears when the API restarts?

With no database (Q8 option A), the saved filters and the audit lines live in the API's memory, so a restart or redeploy empties them. A nurse manager could then find no history for a period that matters.

A. Yes, acceptable for this version; durable storage is a later feature
B. Acceptable for saved filters, but the audit history must survive restarts
C. No: both must survive restarts in this version
D. Not yet decided; raise it with the product owner
X. Other (please specify)

[Answer]: A. Acceptable for this version: Ravi Menon agreed, provided the release notes say the history is lost on restart. Durable storage is a later feature (Dana Ortiz).

## Q10. What is Ravi Menon's role in F1220? (follow-up to Q1, Q2, Q4 and Q9)

Your answers name Ravi Menon several times: he took part in the decisions, he could not explain a missed request last month, and he set the release-notes condition in Q9. He is not in the Rally snapshot or in the stakeholder list in Q5, so the stakeholder map needs his role from you.

A. Nurse manager: he uses the filter history (US5163) and speaks for the nurse managers
B. Nurse manager, and he also decides scope alongside Dana Ortiz (this would change the Q6 answer)
C. Another role (please say which under Other)
D. Not identified
X. Other (please specify)

[Answer]: A. Nurse manager: he uses the filter history (US5163) and speaks for the nurse managers

## Consolidated Summary Confirmation

- Problem: reviewers re-pick the same filter every day, and nobody can tell afterwards why a reviewer did not see a request because filter changes leave no record (Q1)
- Customers: internal prior-authorization reviewers first; nurse managers use the filter history (Q2)
- Success: a saved filter is applied every time the screen opens, on any browser; every successful save has exactly one audit line and a refused save has none; a nurse manager can explain a missed request from the history alone. No time-saving metric: no baseline this release (Q3)
- Trigger: reviewers asked for it in the F1210 demo, and Ravi Menon could not explain a missed request last month (Q4)
- Stakeholders: Dana Ortiz (product owner), Meena Iyer (tech lead), the four story owners (Kiran Rao, Divya Pillai, Tara Joshi, Arjun Nair), reviewers and nurse managers as end users; Ravi Menon is a nurse manager who speaks for the nurse managers (Q5, Q10)
- Decisions: Dana Ortiz decides scope and priority; Meena Iyer decides how it is built and the story order; story owners influence (Q6)
- Communication: the usual Rally routine (In-Progress, Completed on merge to the feature branch, PR link and intent id in Discussion); Dana accepts after the feature demo (Q7)
- Left out of this version: a real database, sign-in, more than one saved filter or more filter fields, export or retention of the audit history (Q8)
- Restarts: losing saved filters and history on restart is acceptable for this version, provided the release notes say so; durable storage is a later feature (Q9)
- Release notes: Meena Iyer writes the line saying the history is lost on restart, decided with Dana Ortiz (Q11)

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct

## Assumption Confirmation

The stakeholder map carries one open item:

- Open question for Dana Ortiz (product owner): who may see a reviewer's filter history, and how is a nurse manager identified? This version has no sign-in, so nothing yet decides either.

A. Accept assumptions
B. Convert to follow-up questions

[Answer]: A. Accept assumptions

## Q11. Who writes the release-notes line saying the filter history is lost on restart? (follow-up to Q9)

Ravi Menon accepted losing the history on restart only if the release notes say so (Q9), but nobody was named to write that line.

A. Meena Iyer (tech lead)
B. Dana Ortiz (product owner)
C. The owner of the story that builds the history (Arjun Nair, US5163)
D. Not yet decided
X. Other (please specify)

[Answer]: A. Meena Iyer owns the release-notes line about the history being lost on restart; decided in the session with Dana Ortiz.
