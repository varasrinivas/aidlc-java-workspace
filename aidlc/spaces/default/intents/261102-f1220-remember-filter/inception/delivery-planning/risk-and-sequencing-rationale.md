# Risk and Sequencing Rationale — F1220 Remember my filter

A **Bolt** is one build pass over a piece of the work that ends in something that runs. There are four, one per unit (`bolt-plan.md`).

## Heuristic

The order is **dependency-first**, chosen in Scope Definition (Q4). There is no formal scoring model such as WSJF, which ranks work by value and urgency against size (Q2).

The dependency map from Units Generation leaves only one ordering choice: which Bolts may run together. The team chose two parallel waves (Q3). That puts the two riskiest Bolts, B1 and B2, first and in parallel.

The order follows the dependency map exactly:

- B1 and B2 depend only on the approved contract.
- B4 follows B1.
- B3 follows B2.

There is no walking-skeleton ceremony (team practice).

## Why This Order

| Bolt | Why here |
|---|---|
| B1 (U1) | The largest and riskiest API work: 5 points (Kiran Rao's re-estimate, agreed with Dana Ortiz), strict request checks, the reviewer limit, the tenant list and browser access. B4 builds on it, so it goes first. |
| B2 (U2) | The riskiest screen logic (save ordering and late reads), and the first time the F1210 controls appear on the page. B3 builds on it. It runs alongside B1 because they share only the contract. |
| B4 (U4) | Extends B1's store and controller (ADR-001), so it starts when B1 merges. A Must-have. |
| B3 (U3) | Extends B2's session and renderer (ADR-004). A Should-have, and the first to slip (Scope Q2). |

## Risks Tackled Early (Q5)

| Risk | Likelihood | Impact | How the plan addresses it |
|---|---|---|---|
| U1 is too big for the release | Medium | High: it delays B4, a Must-have | U1 is in the first wave. It was re-estimated at 5 points and kept as one story. The fallback split (tenant list and browser access as their own story) stays available if B1 runs long. Dana Ortiz decides. |
| U2's ordering logic is wrong or flaky | Medium | High: lost or wrong saves | U2 is in the first wave. AC1.2.7 and AC1.2.8 use stubbed answers the test resolves by hand, not real timers, and the logic lives in a DOM-free module (ADR-004). |
| The repos drift from the contract | Medium | Medium: found late at Build and Test | Each Bolt copies the shared contract examples into its tests. Only Meena Iyer changes the contract, in this parent record first. Build and Test includes a manual end-to-end check. |
| A late B2 delays B3 | Medium | Low: B3 is the Should-have cut first | Accepted (Units Generation R-03). If time runs short, B3 slips and the feature ships with B1, B2 and B4. |
| B3 or B4 cut before the dependency merges | Low | Medium: rework | Team rule: never cut a story branch before the stories it depends on have merged. |

## What a Slip Looks Like

If 2027.Q1 R1 is at risk:

1. B3 (US5162) is cut and moves to a later release. Dana Ortiz decides.
2. If B1 still runs long, the agreed split moves the tenant list and browser access into a separate story that still comes before B2's full demo.

The three Must-haves (B1, B2, B4) ship together or the feature doesn't deliver its value (Scope Q1).
