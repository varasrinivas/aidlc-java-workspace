# Business Overview: priorauth-web

Snapshot: `priorauth-web` `v1.1.0` (`ddca232`), full rescan on 2026-11-03.

## Purpose

`priorauth-web` is the **reviewer screen** of Acme Health's prior-authorization service. A reviewer opens one page and sees the queue of pending prior-authorization requests, oldest first, read from `priorauth-api`. Requests past their age limit are highlighted.

## Users

- **Reviewer**: works the pending queue. Identified only by the `?reviewer=<id>` page parameter (no sign-in on the page).

## Key Functionality (by Rally story)

| Story | Feature | What the reviewer gets |
|---|---|---|
| (v1.0.0) | Pending queue | One row per pending request (id, tenant, service, status, age), over-limit rows in red, a count above the table. |
| US5153 (F1210) | Filter controls | A Tenant picker ("All tenants" or one tenant) and an "Over limit only" switch that narrow the queue on the API side. |
| US5161 (F1220) | Remember my filter | With `?reviewer=`, the page opens with that reviewer's last saved filter and saves every change. Without it, the controls still filter but nothing is remembered and the page says so. |
| US5162 (F1220) | Clear my filters | A "Clear filters" button resets both controls to "All tenants" / switch off, reloads the whole queue, saves the cleared filter, and is disabled when no filter is set. A saved tenant that no longer exists is dropped with its own message ("Your saved tenant is no longer available, so all tenants are shown."). |

## Business Rules Visible in Code

- The unfiltered queue never flashes before a saved filter is applied (FR4.3).
- A reviewer's own change always beats a late saved-filter read (AC1.2.8).
- Saves are sent one at a time; only the newest waiting choice is sent next (FR5.3).
- A failed save keeps the filter on the page and says it was not saved (FR5.2).
- One message area shows the highest-priority message in force (FR4.9); the priority order is recorded in [architecture.md](architecture.md).
- Every API call gives up after 10 seconds, with no retries (contracts C1, C2, C4).

## Business Constraints and Known Limits

- Filter history lives only in `priorauth-api` memory; release notes for 2027.Q1 R1 state it is lost on restart and readable by anyone using the screen (team.md, Deployment).
- No deployed environment; the demo runs locally from `main`.

See [api-documentation.md](api-documentation.md) for the contracts and [component-inventory.md](component-inventory.md) for where each rule lives.
