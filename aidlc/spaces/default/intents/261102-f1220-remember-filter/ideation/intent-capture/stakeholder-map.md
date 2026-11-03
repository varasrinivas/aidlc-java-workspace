# Stakeholder Map — F1220 Remember my filter

## Key Stakeholders and Their Interests

| Stakeholder | Role | What they care about | Source |
|---|---|---|---|
| Dana Ortiz | Product owner | F1220 lands in release 2027.Q1 R1 and is accepted after the feature demo | [Q5] |
| Meena Iyer | Tech lead | The API contract is agreed first, so the four stories can be built in parallel; owns the release-notes line that the history is lost on restart | [Q5] [Q11] |
| Kiran Rao | Story owner, US5160 | Delivers US5160, which comes first in the feature's order | [desc] [Q5] |
| Divya Pillai | Story owner, US5161 | Delivers US5161 in the order the feature sets | [desc] [Q5] |
| Tara Joshi | Story owner, US5162 | Delivers US5162, after US5161 | [desc] [Q5] |
| Arjun Nair | Story owner, US5163 | Delivers US5163, after US5160 | [desc] [Q5] |
| Prior-authorization reviewers | End users (primary) | Their last filter comes back without re-picking it | [Q2] [Q5] |
| Nurse managers | End users (secondary) | The filter history explains why a reviewer did not see a request | [Q2] [Q5] |
| Ravi Menon | Nurse manager; speaks for the nurse managers | Being able to explain a missed request; the release notes must say the history is lost on restart | [Q4] [Q9] [Q10] |

## Decision-Makers vs. Influencers

| Person or group | Decides or influences | Over what | Source |
|---|---|---|---|
| Dana Ortiz | Decides | Scope and priority | [Q6] |
| Meena Iyer | Decides | How it is built, and the order of the stories | [Q6] |
| Story owners (Kiran Rao, Divya Pillai, Tara Joshi, Arjun Nair) | Influence | Scope, priority and build decisions | [Q6] |

## Communication Requirements

| What | Who | When | Source |
|---|---|---|---|
| Move the story to In-Progress | Each story owner | When work on the story starts | [Q7] |
| Move the story to Completed; paste the PR link and the intent id into the story's Discussion | Each story owner | When the story's PR merges into the feature branch | [Q7] |
| Acceptance of the feature | Dana Ortiz | After the feature demo | [Q7] |
| Say in the release notes that the filter history is lost on restart | Meena Iyer (decided with Dana Ortiz) | At release | [Q9] [Q11] |

## Assumptions & Open Questions

- [assumption] Open question for Dana Ortiz (product owner): who may see a reviewer's filter history, and how is a nurse manager identified? This version has no sign-in, so nothing yet decides either. Nurse managers, including Ravi Menon, use that history.
