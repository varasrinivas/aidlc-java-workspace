# Personas — F1220 Remember my filter

Two personas, confirmed in `user-stories-questions.md` Q1. Both are internal users. (intent-statement.md: Target Customer)

## P1 Rita the Reviewer (primary)

| Field | Value |
|---|---|
| Role | Prior-authorization reviewer. Works the pending-requests queue on the reviewer screen. |
| Goals | Start the day on the requests that matter to her (her tenant, over-limit first) without setting the filter again. Get the same view on any computer. Get back to the whole queue in one step. |
| Pain points | Sets the tenant and the "over limit only" switch again every morning (intent: Problem Statement). Has to undo each control on its own to see everything. |
| Context | Opens the screen with her login name in the address (`?reviewer=`), because there is no sign-in. Uses the keyboard as much as the mouse. |
| Tech comfort | Medium |
| Frequency | Daily, several times a day |
| Stories | US1.1 (through the screen), US1.2, US1.3 |

## P2 Nina the Nurse Manager (secondary)

| Field | Value |
|---|---|
| Role | Nurse manager responsible for a group of reviewers. Ravi Menon holds this role and speaks for the nurse managers (intent Q10). |
| Goals | When a request is missed, find out what filter the reviewer had at the time, from a record she can trust in this version. |
| Pain points | Last month a missed request could not be explained, because filter changes left no record (intent: Initiative Trigger). |
| Context | Reads a reviewer's filter history from the API directly. There is no history view on the screen in this version (requirements RQ9). Times in the history are UTC. The history records saved filters only, not what was on the reviewer's screen at the time: an unsaved choice after a failed save leaves no line. Each change of control saves, so a reviewer stepping through the tenant picker with the keyboard can add several lines. She knows three more limits (requirements A2): the history is lost on restart, only the newest 1,000 lines are kept, and each line shows the reviewer id a change was saved under rather than who saved it. |
| Tech comfort | Medium |
| Frequency | Occasional, when a missed request is investigated |
| Stories | US1.4 |

## Relationships and Priority

- Rita is the primary persona. Three of the four stories serve her directly, and the must-have value of F1220 is her daily convenience. (scope-document.md)
- Nina depends on Rita's saves: every history line she reads is written when Rita, or someone using Rita's id, saves a filter. (requirements FR7.1, A2)
- If the two conflict, Nina's need for a complete and truthful record outweighs Rita's convenience. A save that cannot be recorded is refused, not saved silently. (requirements NFR2, FR7.2)
