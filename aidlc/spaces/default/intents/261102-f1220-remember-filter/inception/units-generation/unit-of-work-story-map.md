# Unit-to-Story Map — F1220 Remember my filter

Keyed by the stories in `inception/user-stories/stories.md`.

| Story | Rally | Unit ID | Directory | Acceptance criteria |
|---|---|---|---|---|
| US1.1 | US5160 | U1 | u1-us5160-save-filter | AC1.1.1-AC1.1.13 |
| US1.2 | US5161 | U2 | u2-us5161-restore-filter | AC1.2.1-AC1.2.12 |
| US1.3 | US5162 | U3 | u3-us5162-clear-filters | AC1.3.1-AC1.3.6 |
| US1.4 | US5163 | U4 | u4-us5163-filter-history | AC1.4.1-AC1.4.9 |

## Rows That Span Units

| Concern | Units | How it is split |
|---|---|---|
| Saving a filter (FR1) | U1, U4 | U1 builds the save; U4 adds the history line to the same atomic save (ADR-001) |
| Save ordering (FR5.3) | U2, U3 | U2 builds the rule in `FilterSession`; U3's Clear follows it (AC1.3.6) |
| Safe errors (NFR4) | U1, U4 | U1 builds `NewEndpointErrorHandler`; U4's history endpoint uses it (AC1.4.8) |
| Contract examples | U1, U2, U4 | Each copies the examples for its own calls into its repo's tests (Q1) |
| Accessibility checks by hand (NFR10) | U2, U3 | Done once at the feature's Build and Test |

## Implementation Order Within Each Unit

Each unit follows the team's test-after posture: build a layer, then write and run its tests before moving to the next.

- **U1:**
  1. Record the API baseline.
  2. Add the NM-02 sample row and update the affected tests.
  3. `TenantDirectory`.
  4. `ReviewerFilterStore`.
  5. `ReviewerFilterController`, strict bodies and `NewEndpointErrorHandler`.
  6. `TenantsController`.
  7. `BrowserAccessPolicy`.
- **U2:**
  1. `QueueRenderer` controls, message area and `esc`.
  2. `SavedFilterClient`.
  3. The `QueueFilters` mapping.
  4. `FilterSession`: restore, save ordering, late read, messages.
  5. Wire `index.html`.
- **U3:**
  1. `FilterSession` Clear and its disabled state.
  2. The `QueueRenderer` button.
  3. Wire `index.html`.
- **U4:**
  1. The history line and limit in `ReviewerFilterStore`, with the injected `Clock`.
  2. The atomic save with its line.
  3. The history endpoint in `ReviewerFilterController`.

## Coverage Check

- Every story (US1.1-US1.4) is assigned to exactly one unit.
- Every unit (U1-U4) has at least one story.
