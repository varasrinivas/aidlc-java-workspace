# Initiative Brief — F1220 Remember my filter

One page that closes Ideation. It compiles the approved intent statement, stakeholder map, scope document, intent backlog and team assessment in `ideation/`. Answers cited as [Q<n>] are from `approval-handoff-questions.md` in this folder.

## Intent and Problem

Reviewers have to set the same queue filter again every day. Nobody can tell afterwards why a reviewer did not see a request, because changes to a reviewer's filter leave no record. F1220 keeps each reviewer's last filter so it follows them to any browser, restores it when the screen opens, and records every change so a nurse manager can explain a missed request. (Intent statement: Problem Statement, Target Customer.)

**Success measures** (intent statement: Success Metrics):

- When a reviewer has a saved filter, the screen opens with it applied every time, on any browser.
- Every successful save has exactly one history entry, and a refused save has none.
- For any period since the service last restarted, a nurse manager can explain a missed request from the history alone.

## Market Validation

Market research did not run. F1220 extends the reviewer screen F1210 shipped, for internal users, and the trigger came from those users directly: reviewers asked for it in the F1210 demo, and a nurse manager could not explain a missed request. [Q4]; intent statement: Initiative Trigger

## Feasibility and Risk Highlights

No feasibility study ran; the team agreed none is needed for this feature. [Q4]

| Risk | Mitigation | Status | Source |
|---|---|---|---|
| Saved filters and history are lost when the service restarts | Accepted; the release notes say so (Meena Iyer) | Acknowledged | [Q2]; scope document |
| Anyone using the screen can read a reviewer's history (no sign-in) | Accepted; the release notes say so; Ravi Menon agreed | Acknowledged | [Q1] [Q2]; scope document |
| One owner per story, so an absence stops that story | Pairing on each part of the product | Acknowledged | [Q2]; team assessment |
| The screen stories depend on the agreed contract | Agreed in Contract Design, before construction | Acknowledged | [Q2]; scope document |

## Scope Boundary

- **Must:**
  - US5160 save and read the last filter (Kiran Rao)
  - US5161 open the screen with it (Divya Pillai)
  - US5163 audit every change (Arjun Nair)
- **Should:** US5162 clear my filters (Tara Joshi). It is the first to slip if 2027.Q1 R1 is at risk.
- **Out:**
  - a durable store
  - sign-in, and limiting who reads the history
  - more saved filters or filter fields
  - export or retention of the history
- **Deadline:** the whole feature in 2027.Q1 R1.

(Scope document; intent backlog.)

## Concept Visuals

No new mockups. The mockup attached to US5153 in F1210 (`docs-in/rally/F1210/US5153/queue-filters-mockup.md`) and the current reviewer screen are the reference, per Divya Pillai. [Q4]

## Team Plan

- **Team:** one team (priorauth). The four story owners are full time until their story is merged, with no competing work and no outside help. [Q3]; team assessment
- **Ways of working:**
  - The whole team mobs on the feature's Inception decisions, with Meena Iyer typing, and on each story's code plan.
  - Kiran pairs with Arjun on the API, and Divya pairs with Tara on the screen.
  - (Mob composition.)
- **Next sessions:** mob elaboration I (requirements, stories) and II (design, units, contract, delivery plan) on the next two mornings, IST. [Q5]
- **Decisions:** Dana Ortiz owns scope and acceptance. Meena Iyer owns Inception and how it is built. (Stakeholder map; team assessment.)

## Go / No-Go

**Go: proceed to Inception**, decided by Dana Ortiz. All stakeholders, including Ravi Menon for the nurse managers, agree on the intent and scope, the risks are acknowledged, and the team's time is committed. [Q1] [Q2] [Q3] [Q6]

## Assumptions & Open Questions

None.
