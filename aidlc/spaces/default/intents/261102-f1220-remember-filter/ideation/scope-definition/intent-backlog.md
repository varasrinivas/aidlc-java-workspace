# Intent Backlog — F1220 Remember my filter

Prioritized with MoSCoW, from the answers in `scope-definition-questions.md` [Q<n>]. Each item is a proto-Unit: one Rally story, one owner. Inception turns these into units of work. Estimates are the story points in the Rally snapshot for F1220. They are shown for reference and have not been re-estimated.

## Backlog

| Rank | Item | Story | Owner | MoSCoW | Rally estimate | Depends on | Value it delivers | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | Save and read a reviewer's last filter | US5160 | Kiran Rao | Must | 3 | — | The filter follows the reviewer to any browser | [Q1] [Q3] [Q4] |
| 2 | Open the screen with my last filter | US5161 | Divya Pillai | Must | 3 | Agreed contract (Contract Design) | Reviewers no longer re-pick their filter every morning | [Q1] [Q3] |
| 3 | Audit every filter change | US5163 | Arjun Nair | Must | 2 | US5160 | Nurse managers can explain a missed request | [Q1] [Q3] |
| 4 | Clear my filters | US5162 | Tara Joshi | Should | 1 | US5161 | The whole queue is back with one action | [Q1] [Q2] [Q3] |

US5160 and US5161 share rank 1–2 in time: US5161 can start as soon as the contract is agreed, so the two can be built in parallel. [Q3]

## Release Conditions (not stories)

| Item | Owner | When | Source |
|---|---|---|---|
| Release notes say the filter history is lost when the service restarts, and that anyone using the screen can read it | Meena Iyer | At release (2027.Q1 R1) | intent: Initial Scope Signal; [Q5] [Q6] |

## Won't Have (this time)

- A durable store for filters and history (intent: Initial Scope Signal)
- Sign-in, and limiting who may read the history (intent: Initial Scope Signal; [Q6])
- More than one saved filter, or more filter fields (intent: Initial Scope Signal)
- Exporting or retaining the history (intent: Initial Scope Signal)

## Slip Order

If 2027.Q1 R1 is at risk, US5162 slips first. The three musts ship together or the feature does not deliver its value. [Q1] [Q2] [Q5]

## Assumptions & Open Questions

None.
