# Intent Statement — F1220 Remember my filter

This intent is the parent of Rally feature F1220, delivered as four stories with four owners: US5160 (Kiran), US5161 (Divya), US5162 (Tara) and US5163 (Arjun). [desc]

## Problem Statement

Reviewers have to set the same queue filter again every day, a chore they asked to have removed. No measurement of the time it takes has been made. [Q1] [Q3] [Q4]

Nobody can tell afterwards why a reviewer did not see a request, because changes to a reviewer's filter leave no record. [Q1]

## Target Customer

| Customer | Internal or external | How they benefit | Source |
|---|---|---|---|
| Prior-authorization reviewers (primary) | Internal | Their last filter comes back on its own, so they stop re-picking it | [Q1] [Q2] |
| Nurse managers (secondary) | Internal | They use the filter history to explain why a reviewer did not see a request | [Q2] [Q10] |

## Success Metrics

| Outcome | How it is measured | Source |
|---|---|---|
| A reviewer's saved filter comes back on its own | When a reviewer has a saved filter, the screen opens with it applied every time, on any browser, with no manual re-pick | [Q3] |
| Every filter change is recorded, and only real changes | Each successful filter save has exactly one audit line; a refused save (unknown tenant) has none | [Q3] |
| Missed requests can be explained | For any period since the API last restarted, a nurse manager can answer "why didn't this reviewer see request X?" from the filter history alone. History from before a restart is not kept in this version (see Initial Scope Signal) | [Q3] [Q9] |

A time-saving metric (time from opening the screen to the first review) is not used for this release: there is no baseline and none will be taken. [Q3]

## Initiative Trigger

Reviewers asked for their filter to be remembered during the F1210 demo. [Q4]

Last month a nurse manager, Ravi Menon, could not explain why a reviewer missed a request. [Q4] [Q10]

## Initial Scope Signal

**Workflow-selected:** this work runs as a `feature`, the full set of lifecycle stages for the whole of F1220. [scope]

**Product boundary confirmed by the team:** this first version deliberately leaves out:

- a real database: saved filters and their history are kept in memory behind one replaceable class [Q8]
- sign-in: the reviewer is identified by a login name the screen passes along, with no authentication [Q8]
- more than one saved filter per reviewer, and filter fields beyond tenant and over-limit [Q8]
- exporting the audit history or keeping it for a set retention period [Q8]

Because nothing is stored durably, saved filters and the filter history are lost whenever the API restarts. The team accepts this for this version on one condition: the release notes must say the history is lost on restart. Durable storage is a later feature. [Q9]

Meena Iyer writes that release-notes line, as decided with Dana Ortiz. [Q11]

## Assumptions & Open Questions

None.
