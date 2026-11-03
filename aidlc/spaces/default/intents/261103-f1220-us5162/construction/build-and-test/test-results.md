# Test Results: US5162 Clear my filters

## Build

Success. There is no build step (plain ES modules, no dependencies).

## Test Run

- **Command:** `scripts\verify.cmd priorauth-web`, from the workspace root. It is the only distinct command in `code-generation/unit-test-instructions.md` and was run once.
- **Code:** `priorauth-web` `f1220/us5162-clear-filters` at `835c32e`, with a clean tree.
- **Exit code:** 0

| Total | Passed | Failed | Skipped | Cancelled |
|---|---|---|---|---|
| 48 | 48 | 0 | 0 | 0 |

- **Baseline:** 38 of 38 at `b9c8448`, recorded before the first change (code-summary.md).
- **This story's tests:** 10 new tests pass:
  - 7 in `test/filter-session.test.js`: AC1.3.1, AC1.3.4, AC1.3.6, A2, and three FR4.10 tests.
  - 3 in `test/render.test.js`: AC1.3.2, AC1.3.3, FR6.2.
- **Changed on purpose:** the one US5161 FR4.8 test, which now expects the dropped-tenant message (FR4.10). It passes.
- **Unchanged files:** every test in `api.test.js`, `queue-filters.test.js` and `saved-filter-client.test.js` passes.

## Failures

None.

## Coverage

NOT MEASURED. F1220 adds no coverage tooling, under the team's recorded exception owned by Meena Iyer. The 80% floor is not claimed.

## Per-File Edge Cases (team practice)

- `test/filter-session.test.js`:
  - Happy path: AC1.3.1.
  - Edge and error cases: a failed save (AC1.3.4), a save still open (AC1.3.6), no reviewer (A2), the switch off and the message kept after Clear (FR4.10).
- `test/render.test.js`:
  - Happy path: AC1.3.3.
  - Edge cases: no argument, `{null, false}` and `{"", false}` (AC1.3.2, FR6.2).

## Manual Checks Carried to the Feature's Build and Test

- **AC1.3.5:** after "Clear filters" from the keyboard, focus moves to the Tenant picker.
- **NFR10:** the button works by keyboard, and its disabled state is announced.
- **The `index.html` wiring:** the button's live disabled state and the click.
