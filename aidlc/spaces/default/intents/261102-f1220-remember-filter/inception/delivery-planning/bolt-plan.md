# Bolt Plan — F1220 Remember my filter

A **Bolt** is one build pass over a piece of the work that ends in something that runs. F1220 has four Bolts, one per unit (`delivery-planning-questions.md` Q1). Each Bolt is one Rally story, one branch and one PR, built in that story's own child intent by its owner (Q7).

**Walking skeleton: none.** The team doesn't build a thin end-to-end slice first (team practice). A walking skeleton is a minimal version that runs the whole way through, built first to prove the pieces connect. The stories are proven together at this parent's Build and Test.

## Waves

| Wave | Bolts | Starts when |
|---|---|---|
| 1 | B1 (U1) and B2 (U2), in parallel | Contract Design is approved (done) and `feature/F1220` exists in both repos |
| 2 | B4 (U4) | B1's PR has merged into `feature/F1220` |
| 2 | B3 (U3) | B2's PR has merged into `feature/F1220` |

B3 and B4 may overlap. Neither waits for the other (Q3).

## B1 — U1 `us5160-save-filter` (US5160, Kiran Rao, priorauth-api, 5 points)

- **Branch:** `f1220/us5160-save-filter`, cut from `origin/feature/F1220`.
- **Definition of Done:**
  - AC1.1.1-AC1.1.13 pass through the verify script, with the repos named.
  - The API baseline was recorded before the first change.
  - The contract examples for C1, C2 and C5 are copied into the API tests and pass.
  - The real 404 body for `.` and `..` is recorded and checked against the no-echo rule.
  - The mob reviewed the code plan against the security checklist.
  - The PR into `feature/F1220` names its sibling stories, and its verify output is pasted in.
- **Confidence hypothesis:** shipping B1 shows that strict checks on request bodies and ids, plus the reviewer limit, can be enforced at the API boundary without changing the existing queue endpoint. AC1.1.13 and the existing queue tests prove it.
- **Expected demo:** with the API running locally, call `PUT` and then `GET /reviewers/rita.k/filter` and `GET /tenants`, and see the fixed error body for an unknown tenant.

## B2 — U2 `us5161-restore-filter` (US5161, Divya Pillai, priorauth-web, Rally 3)

- **Branch:** `f1220/us5161-restore-filter`, cut from `origin/feature/F1220`.
- **Definition of Done:**
  - AC1.2.1-AC1.2.12 pass through the verify script. Keyboard use is listed for the manual check at Build and Test.
  - The screen's 6 existing tests still pass.
  - The contract examples for C1, C2 and C4 are copied into the screen tests and pass.
  - R-06 (a change before the first read wins) is in the code plan and has a test.
  - The mob reviewed the code plan.
  - The PR into `feature/F1220` names its sibling stories.
- **Confidence hypothesis:** shipping B2 shows that the ordering rules work as specified, tested with stubbed answers the test resolves by hand. Those rules are: saves go one at a time, a superseded save is dropped, and a late read is ignored. The test is AC1.2.7 and AC1.2.8.
- **Expected demo:** serve the screen with `npx serve .` at `http://localhost:3000/?reviewer=rita.k&api=http://localhost:8080`. Change the filter, reload, and see it restored. The full demo needs B1 merged.

## B3 — U3 `us5162-clear-filters` (US5162, Tara Joshi, priorauth-web, Rally 1, Should-have)

- **Branch:** `f1220/us5162-clear-filters`, cut from `origin/feature/F1220` after B2 merges.
- **Definition of Done:**
  - AC1.3.1-AC1.3.6 pass through the verify script. Focus after Clear is listed for the manual check.
  - Only `FilterSession` and `QueueRenderer` are changed (ADR-004).
  - The mob reviewed the code plan.
  - The PR into `feature/F1220` names its sibling stories.
- **Confidence hypothesis:** shipping B3 shows that a second owner can extend U2's session and renderer without touching U2's other modules.
- **Expected demo:** set TX-01 and over-limit only, use Clear filters, and see the whole queue with Clear disabled. After a reload the filter is still cleared.
- **Slip rule:** B3 is the first thing cut if 2027.Q1 R1 is at risk. Because it waits for B2, a late B2 delays B3 directly (Units Generation R-03).

## B4 — U4 `us5163-filter-history` (US5163, Arjun Nair, priorauth-api, Rally 2)

- **Branch:** `f1220/us5163-filter-history`, cut from `origin/feature/F1220` after B1 merges.
- **Definition of Done:**
  - AC1.4.1-AC1.4.9 pass through the verify script.
  - The C3 examples are copied into the API tests and pass.
  - The test of saves made at the same moment (AC1.4.7) passes reliably.
  - The mob reviewed the code plan.
  - The PR into `feature/F1220` names its sibling stories.
- **Confidence hypothesis:** shipping B4 shows that a save and its history line never come apart, even under saves made at the same moment (NFR2).
- **Expected demo:** save three filters for `rita.k`, including Clear, then call `GET /reviewers/rita.k/filter/history` and see three four-field lines, newest first.

## After the Four Bolts (This Parent Workflow)

1. **Build and Test** across both repos on `feature/F1220`, once all four story PRs have merged:
   - The verify script, with the repos named.
   - Coverage reported as NOT MEASURED, under the team's recorded exception.
   - The manual checks: keyboard and focus, and the end-to-end path of screen with `?reviewer=`, change, reload, and read history.
2. One PR from `feature/F1220` to `main` in each repo.
3. Meena Iyer bumps the versions (minor) and tags each repo. She also writes the release-notes line, which covers:
   - history lost on restart
   - anyone can read and write
   - only the newest 1,000 lines are kept
   - each line shows the reviewer id it was saved under
   - the history call, with an example
4. Feature demo, then Dana Ortiz accepts.

This parent workflow skips the per-unit design stages, Code Generation and the Operation stages, because each child intent does that work and there are no environments (Q7).
