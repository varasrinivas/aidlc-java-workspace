# Test Results: US5161

## Run

- **Command:** `scripts\verify.cmd priorauth-web`, run from the workspace root on 2026-11-03.
- **Repo state:** `priorauth-web` on `f1220/us5161-restore-filter` at `9af272e`, with a clean working tree.
- **Exit code:** 0.

## Build Status

Success. There is nothing to compile or bundle, and the verify script ran `npm test --silent` (`node --test`).

## Test Results

| Total | Passed | Failed | Skipped | Cancelled |
|---|---|---|---|---|
| 38 | 38 | 0 | 0 | 0 |

The run was deduplicated: the stage-level `unit-test-instructions.md` has one repo-wide command, and it was run once.

| Test file | Tests | Change |
|---|---|---|
| `test/saved-filter-client.test.js` | 9 | New |
| `test/filter-session.test.js` | 15 | New |
| `test/queue-filters.test.js` | 5 (2 F1210 + 3 new) | Extended |
| `test/render.test.js` | 7 (2 F1210 + 5 new) | Extended |
| `test/api.test.js` | 2 | Unchanged |

**Baseline comparison:** 6 of 6 passed before the change at `65a999b`, and the same 6 still pass. There are no regressions.

## Failure Details

None.

## Coverage

NOT MEASURED. F1220 adds no coverage tooling, under the team's recorded exception owned by Meena Iyer. The express workflow's Testing Contract sets no coverage floor. No claim is made that a coverage floor is met.

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| TC-1 suite-green | Testing Contract, `scope_floor` | The existing suite stays green | 6 of 6 F1210 tests pass | Verify output above | Build and Test | Met |
| TC-2 test-per-requirement | Testing Contract, `strategy_volume` | One verifiable test per requirement | Every FR4.x, FR5.x and AC1.2.x owned here has a named test, except keyboard use (see the cross-unit file) | `cross-unit-traceability.md`, test names tagged US5161 | Build and Test | Met |
| TC-3 happy-path-per-component | Testing Contract, `strategy_volume` | At least one happy-path test per component | SavedFilterClient, FilterSession, QueueFilters and QueueRenderer each have one | Test files above | Build and Test | Met |
| TP-1 file-edge-cases | team.md Testing Posture | Each new or changed test file has the happy path plus two error or edge cases | All 4 new or changed files do | Test files above | Build and Test | Met |
| TP-2 verify-script-only | team.md and project.md | Tests run only through the verify script | Yes | Command above | Build and Test | Met |

There is no NFR Requirements or NFR Design stage in this workflow, so there are no further measurable targets.
