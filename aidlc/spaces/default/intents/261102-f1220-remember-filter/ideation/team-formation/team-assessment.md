# Team Assessment — F1220 Remember my filter

Builds on the approved scope (`ideation/scope-definition/scope-document.md`) and backlog (`ideation/scope-definition/intent-backlog.md`). Answers cited as [Q<n>] are from `team-formation-questions.md` in this folder.

## Team

One team, priorauth, delivers the whole feature. Nobody outside the team is needed. [Q4] [Q6]

| Person | Role on F1220 | Availability | Location | Source |
|---|---|---|---|---|
| Dana Ortiz | Product owner | As needed for decisions and the feature demo | — | [Q7]; scope document |
| Meena Iyer | Tech lead; drives the feature's Inception decisions with the mob | — | IST, remote | [Q5] [Q7] |
| Kiran Rao | Owner of US5160 (save and read the last filter) | Full time until US5160 is merged | IST, remote | [Q1] [Q5] |
| Divya Pillai | Owner of US5161 (open the screen with my last filter) | Full time until US5161 is merged | IST, remote | [Q1] [Q5] |
| Tara Joshi | Owner of US5162 (clear my filters) | Full time until US5162 is merged | IST, remote | [Q1] [Q5] |
| Arjun Nair | Owner of US5163 (audit every filter change) | Full time until US5163 is merged | IST, remote | [Q1] [Q5] |
| Ravi Menon | Nurse manager; consulted on the filter history | As needed | — | [Q7] |

## Capacity Allocation Agreement

- **Story owners:** all four work on F1220 full time until their story is merged. [Q1]
- **Competing work:** none. F1220 is the team's only work for 2027.Q1 R1, so no one's time is split. [Q3]
- **Workload:** one story per owner. The Rally estimates in the backlog are 3 (US5160), 3 (US5161), 1 (US5162) and 2 (US5163). [Q1]; intent backlog
- **If the release is at risk:** the agreed lever is scope, not people. US5162 slips first. Scope document: Deadline and Trade-off

## RACI

R = responsible, A = accountable, C = consulted, I = informed.

| Activity | Dana Ortiz | Meena Iyer | Story owner | Mob (whole team) | Ravi Menon | Source |
|---|---|---|---|---|---|---|
| Scope and priority | A | C | C | — | I | [Q7] |
| Inception decisions for the feature (requirements to delivery plan) | C | A, R | C | R | C on the filter history | [Q4] [Q7] |
| Review of each story's code plan before code is written | — | A | R | R | — | [Q4] |
| Building a story and opening its pull request | — | C | A, R | — | — | [Q7] |
| Filter history (US5163) behaviour | C | C | A, R (Arjun Nair) | — | C | [Q7] |
| Release-notes line on history limits | I | A, R | — | — | I | scope document; intent statement |
| Feature acceptance after the demo | A, R | C | I | I | I | [Q7] |

## Risks to Delivery

| Risk | Likelihood | Impact | Mitigation | Source |
|---|---|---|---|---|
| Every owner holds exactly one story, so someone's absence stops that story | Low | Medium | Pairing (Kiran with Arjun, Divya with Tara) means a second person knows each part of the code | [Q1] [Q4] |
| The screen stories depend on the agreed contract before they can start | Low | Medium | Divya and Kiran agree it in Contract Design, before construction | scope document: Sequencing and Dependencies |

## Assumptions & Open Questions

None.
