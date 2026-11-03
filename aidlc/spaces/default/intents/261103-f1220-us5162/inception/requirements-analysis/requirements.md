# Requirements: US5162 Clear my filters (F1220, unit U3 `us5162-clear-filters`)

This story's requirements come from the parent feature intent `261102-f1220-remember-filter`. The IDs FR6, FR5.3 and NFR10 are the parent's, and FR4.8 and FR4.9 are US5161's. They are quoted unchanged so traceability holds. Only FR4.10 is new: it carries the dropped-tenant wording fix that US5161's code review handed to this story (Q1). Nothing the parent approved is reopened here (Q2).

## Sources

| Tag | Source |
|---|---|
| Desc | Initial description: build US5162 of Rally F1220, and fix the dropped-tenant message wording handed over from US5161's code review (`project-description.json`) |
| Parent RA | `261102-f1220-remember-filter/inception/requirements-analysis/requirements.md`, FR6.1-FR6.3, FR5.3, NFR5, NFR10 (approved) |
| Story | `261102-f1220-remember-filter/inception/user-stories/stories.md`, US1.3, AC1.3.1-AC1.3.6, and US1.2's common screen behaviour (approved) |
| Unit | `261102-f1220-remember-filter/inception/units-generation/unit-of-work.md`, U3 (approved) |
| ADR-004 | `261102-f1220-remember-filter/inception/domain-design/decisions.md`: US1.3 changes only `FilterSession` and `QueueRenderer` (accepted) |
| Contract | `261102-f1220-remember-filter/inception/contract-design/contract-summary.md` and `examples/`, C1 (approved) |
| Bolt | `261102-f1220-remember-filter/inception/delivery-planning/bolt-plan.md`, B3 (approved) |
| US5161 | `261102-f1220-us5161/inception/requirements-analysis/requirements.md`, FR4.8 and FR4.9; `261102-f1220-us5161/construction/code-generation/code-summary.md` (the wording note) and the code review handover |
| codekb | `codekb/priorauth-web/`, focused scan of `feature/F1220` at `b9c8448` (this intent's Reverse Engineering) |
| Practices | `memory/team.md`, `memory/project.md` |
| Q<n> | `requirements-analysis-questions.md` in this folder, question n |

## Intent Analysis

- **Goal:** Rita the Reviewer clears the tenant and the over-limit switch with one control and sees the whole queue again, without unpicking each control. (Story US1.3)
- **Second goal:** the message shown when a saved tenant is dropped on open says only what is true, including when the over-limit switch stays on. (Desc; US5161 code review)
- **Type:** an enhancement in the brownfield repo `priorauth-web` only. No API change: Clear saves through the existing contract C1. (Unit U3; Contract C1)
- **Complexity:** Minimal depth, size S (Rally: 1). Most of Clear's behaviour already exists in US5161's `FilterSession.change`: it resets both filters, asks for the whole queue, saves one at a time and reports a failed save. The new parts are the button, its disabled state, its wiring and the message wording. (codekb; Unit U3)
- **Branch:** `f1220/us5162-clear-filters`, cut from `origin/feature/F1220` (US5161 has merged there, PR #82). The PR goes into `feature/F1220`. (Desc; Bolt B3; Practices)
- **Priority:** Should. B3 is the first thing cut if 2027.Q1 R1 is at risk. (Bolt B3)

## Functional Requirements

### FR6 Clear filters (parent, unchanged)

- **FR6.1** One "Clear filters" control sets the tenant to all tenants and the switch to off, shows the whole queue, and saves `{"tenant": null, "overLimit": false}`. (Parent RA; AC1.3.1)
  - Pass/fail: with TX-01 and the switch on, using Clear makes the picker show "All tenants", turns the switch off, asks the queue with no tenant and no over-limit filter, and sends `PUT /reviewers/{reviewerId}/filter` with `{"tenant": null, "overLimit": false}`.
- **FR6.2** "Clear filters" is disabled when no filter is set, meaning the tenant is all tenants and the switch is off. (Parent RA; AC1.3.2, AC1.3.3)
  - Pass/fail on the rendered HTML: with "All tenants" and the switch off, "Clear filters" is a native `<button>` with the `disabled` attribute. With a tenant set, or the switch on, or both, it has no `disabled` attribute.
- **FR6.3** A failed save after "Clear filters" behaves as FR5.2: the whole queue is still shown, and the message area says the filter wasn't saved. (Parent RA; AC1.3.4)

### Approved criteria this story also carries

- **FR5.3 Clear while a save is open (parent, unchanged).** Saves go one at a time, and a waiting save is replaced by a newer one. When Clear is used while a save of TX-01 is still open, the cleared filter is the one sent last and stored. (Parent RA; AC1.3.6)
- **Focus after Clear.** When Rita uses "Clear filters" from the keyboard, focus moves to the Tenant picker, because the button has just become disabled. This is checked by hand at the feature's Build and Test. (AC1.3.5; NFR10)

### FR4.8 and FR4.9 (US5161, unchanged except for the wording below)

- **FR4.8 Saved tenant no longer known.** When the tenant list loads and the saved tenant isn't in it, the screen drops the saved tenant, opens with "All tenants", keeps the saved over-limit switch and saves nothing until the reviewer changes a control. (US5161)
- **FR4.9 Which message shows.** The one message area (`role="status"`) shows the highest message still in force, in a fixed order. The "couldn't load" messages clear on the next successful load of the same call. (US5161)

### FR4.10 Dropped-tenant message (new, this story)

- **FR4.10** In the FR4.8 case, the message area shows its own message, "Your saved tenant is no longer available, so all tenants are shown." That sentence is true whether the switch is off or on. The failed-read message (FR4.5, AC1.2.4) stays "Your saved filter couldn't be loaded, so all requests are shown." and is used only when the saved filter can't be read. (Q1 A, Tara Joshi with Divya Pillai)
  - In the FR4.9 order, the new message takes the saved-filter message's place, fourth. The two can't be in force together, because a tenant is dropped only after a successful read. (FR4.9)
  - It follows the parent's rule for these messages. It stays until the page is reloaded and isn't removed by a filter change or by Clear, like the failed-read message. (Q2 A, a child story doesn't change the parent's rule; Meena Iyer agreed)
  - Pass/fail: with `GET /tenants` answering `["NM-02", "TX-01"]` and a saved filter of `{"tenant": "ZZ-99", "overLimit": true}`, the message area shows the dropped-tenant message, not the failed-read message. With the saved-filter read failing, it shows the failed-read message. The US5161 test at `test/filter-session.test.js:267-274` that expects the old wording for the dropped case changes with this requirement.

## Non-Functional Requirements

- **NFR5 Safe display (parent, unchanged):** every value rendered on the screen, including the Clear button and the new message, goes through the one shared `esc` helper. (Parent RA; Practices)
- **NFR10 Accessibility (parent, unchanged):**
  - "Clear filters" works by keyboard and has a visible text label.
  - Its disabled state uses the native `disabled` attribute, so it isn't shown by colour alone.
  - The dropped-tenant message is text in the `role="status"` area.
  - (Parent RA; AC1.3.2, AC1.3.5)
- **NFR11 Coverage (parent, unchanged):** each new branch gets a test. The disabled state is tested on the rendered string, and Clear's behaviour through `FilterSession` with an injected `fetchFn`. Each changed test file covers the happy path and at least two error or edge cases. Line coverage is NOT MEASURED in F1220. (Parent RA; Practices Testing Posture)
- **NFR8 Compatibility (parent, unchanged):** US5161's existing tests keep passing, except the one FR4.10 changes. A test baseline at `b9c8448` is recorded through `scripts\verify.cmd priorauth-web` before the first code change. (Parent RA; Practices)

## Constraints

- `priorauth-web` only. No API change and no new dependency. (Unit U3; Practices)
- Among the `src/` modules, only `FilterSession` (`src/filter-session.js`) and `QueueRenderer` (`src/render.js`) change, plus their tests. (ADR-004; Bolt B3)
- Screen logic lives in tested `src/` modules, and `index.html` only calls them. (Practices Testing Posture)
- Tests run only through the workspace verify script. (Practices)
- Plan approval is on, and the mob reviews the code plan against the team's security checklist before code is written. (Practices)

## Assumptions

- **A1 `index.html` wiring is allowed.** ADR-004 and Bolt B3 say US1.3 changes only `FilterSession` and `QueueRenderer`. The button still needs a click handler, and the focus move (AC1.3.5) needs a line in `index.html`, the page that only calls the `src/` modules. This reading takes ADR-004 to mean the tested `src/` modules, with the thin page wiring in `index.html` allowed. [assumption] If the team reads ADR-004 strictly, the tech lead changes the parent first.
- **A2 Clear without a reviewer link saves nothing.** When the page is opened without `?reviewer=`, Clear resets the filters and shows the whole queue but sends no save, the same as any other change (AC1.2.9). [assumption]
- **A3 Clear reuses the session's change path.** Clear goes through the same `FilterSession` save-ordering and queue-ordering logic as a picker change, so AC1.3.4 and AC1.3.6 hold without new ordering code. The code plan decides whether that is a named `clear()` on the session or a call to `change`. [assumption]

## Assumptions & Open Questions

- A1-A3 above are open until the gate confirms them.
- None of the parent's open questions affect this story.

## Out of Scope

- Removing the saved-filter or dropped-tenant message after a change or Clear (Q2 A). A change to that rule goes to the tech lead and the parent first.
- Other issues the scan noted (a stale count when the queue fails, the unused `fetchPending`, repeated fetch-and-throw code, stale README notes). They are mentioned, not fixed. (codekb; Practices)
- Any API change or screen view of the history (US5163).
