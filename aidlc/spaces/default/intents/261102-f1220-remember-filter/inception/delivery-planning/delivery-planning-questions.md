# Delivery Planning — Questions

This plan sets the order in which F1220's four units are built. A **Bolt** is one build pass over a piece of the work that ends in something that runs.

Already decided, so not asked again:

- **Order between stories:** dependency-first (Scope Q4).
- **No thin end-to-end slice first:** the team doesn't run a walking-skeleton build. A walking skeleton is a minimal version that runs the whole way through, built first.
- **Release:** 2027.Q1 R1, with US5162 slipping first if the date is at risk (Scope Q2, Q5).
- **Dependency map:**
  - U1 (US5160) and U2 (US5161) start from the approved contract.
  - U4 (US5163) needs U1 merged.
  - U3 (US5162) needs U2 merged.
- **Four people, full time, in two pairs:** Kiran Rao with Arjun Nair on the API, and Divya Pillai with Tara Joshi on the screen (Team Formation).

## Q1. How big is one Bolt?

A. One Bolt per unit, so four Bolts. Each is one story, one branch and one PR (team practice).
B. Bundle units: one Bolt per repo (U1+U4, U2+U3)
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q2. Should the order be scored with a formal model?

A formal model such as WSJF scores each item by value and urgency against its size.

A. No formal model. The order follows the dependency map and the scope's priorities, which leave only one real choice: what to protect if time runs short. US5162 is cut first.
B. Score the four Bolts with WSJF (please give the weights under Other)
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q3. Can Bolts be built at the same time?

A. Yes, in two waves:
   - **Wave 1:** U1 and U2 in parallel, once the contract is approved.
   - **Wave 2:** U4 starts as soon as U1 merges, and U3 as soon as U2 merges, so the two may overlap.
B. One after another: U1, U4, U2, U3
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q4. Is anything outside the team going to hold us up?

A. No. The work, the contract, the repos and the release are all inside the team. The only outside party is Rally: owners update their stories, and Dana Ortiz accepts after the demo.
B. Yes (please name who, what, how long, and which Bolt it blocks under Other)
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q5. What worries you most, so we tackle it early? (select all that apply)

A. **U1's size.** It grew well past its Rally estimate of 3, adding the tenant list, browser access and strict request checks. It also sits ahead of U4.
B. **U2's ordering logic:** saves sent one at a time, late reads ignored, and the right message shown. It also sits ahead of U3, the story cut first.
C. **The two repos drifting from the contract**, since each is tested only against stubs until the feature's Build and Test
D. Nothing in particular
X. Other (please specify)

[Answer]: A, B, C.

## Q6. What is Kiran Rao's new estimate for US5160 (U1)?

User Stories asked for this re-estimate. If U1 no longer fits 2027.Q1 R1, the agreed fallback is to split off the tenant list and browser access as their own Rally story, still ahead of U2's screen work.

A. It still fits as one story (please give the new estimate under Other, for example "5 points")
B. Split it now: the tenant list and browser access become a separate Rally story (Dana Ortiz agrees the split)
C. Not yet decided
X. Other (please specify)

[Answer]: A. 5 points, still one story (Kiran Rao); Dana Ortiz agreed.

## Q7. How does this parent workflow continue once Inception ends?

Your rules say each story is built in its own child intent, which its owner creates against this plan and the approved contract. The child intent runs that story's design, code plan (reviewed by the mob) and code. This parent workflow still lists every Construction and Operation stage, from Functional Design to Feedback.

A. **The parent waits for the children.** It skips the per-unit design stages and Code Generation, because each child intent does that work, along with the Operation stages, because there are no environments. It comes back for **Build and Test** across both repos once all four story PRs have merged into `feature/F1220`. The one PR from `feature/F1220` to `main` follows that.
B. The parent also runs the per-unit design stages (Functional Design, NFR Requirements, NFR Design) before the children start coding
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Consolidated Summary Confirmation

- Four Bolts, one per unit (one story, one branch, one PR) (Q1)
- No formal scoring model; order follows the dependency map and scope priorities; US5162 is cut first if needed (Q2)
- Two waves: U1 and U2 in parallel once the contract is approved; U4 as soon as U1 merges and U3 as soon as U2 merges (Q3)
- No outside dependencies; Rally updates by owners and Dana Ortiz's acceptance after the demo only (Q4)
- Worries to tackle early: U1's size, U2's ordering logic, and the repos drifting from the contract (Q5)
- U1 re-estimated by Kiran Rao at 5 points, still one story; Dana Ortiz agreed (Q6)
- The parent skips the per-unit design stages, Code Generation and the Operation stages; each story's child intent does the build; the parent returns for Build and Test across both repos once all four story PRs merge into `feature/F1220`, then the one PR to `main` (Q7)

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
