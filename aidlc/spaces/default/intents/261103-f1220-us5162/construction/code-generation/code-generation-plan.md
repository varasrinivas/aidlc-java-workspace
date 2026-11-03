# Code Generation Plan: US5162 Clear my filters (F1220, unit U3 `us5162-clear-filters`)

## Summary

- Builds: a "Clear filters" button that is disabled when no filter is set, wired to `FilterSession.clear()`, plus its own message for a dropped saved tenant (FR4.10)
- Touches: `priorauth-web/src/filter-session.js`, `src/render.js`, `index.html`, `test/filter-session.test.js`, `test/render.test.js`
- Tests: about 10 new or changed unit tests (`node --test`) through `scripts\verify.cmd priorauth-web`, plus the existing suite kept green

## Context

- **Requirements:** `inception/requirements-analysis/requirements.md` in this intent: FR6.1-FR6.3, FR5.3 (AC1.3.6), the focus check (AC1.3.5), FR4.10, NFR5, NFR8, NFR10, NFR11, and assumptions A1-A3.
- **Parent artifacts:** story US1.3, AC1.3.1-AC1.3.6 (`261102-f1220-remember-filter/inception/user-stories/stories.md`), unit U3, ADR-004, and bolt B3. Contract C1 already accepts `{"tenant": null, "overLimit": false}`, so there is no API change.
- **Code base:** `priorauth-web` at `origin/feature/F1220` `b9c8448`, which includes US5161 (codekb `codekb/priorauth-web/`).
- **Repo and branch:** `priorauth-web` only, on branch `f1220/us5162-clear-filters` cut from `origin/feature/F1220`.
- **Dependencies:** none are added.

## Design

- **`src/filter-session.js` (FilterSession, ADR-004):**
  - Add `clear()`, which runs the existing `change({ tenant: null, overLimit: false })`. Clear therefore reuses US5161's queue ordering, its one-save-at-a-time rule and its failed-save message, with no new ordering code (A3, AC1.3.4, AC1.3.6). Without a reviewer it saves nothing, like any change (A2).
  - Add `MESSAGES.droppedTenant`: "Your saved tenant is no longer available, so all tenants are shown." (FR4.10, Q1 A).
  - In `PRIORITY`, put `droppedTenant` directly after `savedFilter`. The two are never in force together.
  - The FR4.8 branch flags `droppedTenant` instead of `savedFilter`. The failed-read branch keeps `savedFilter`.
  - Neither message is cleared by a change or Clear (Q2 A, the parent's rule).
- **`src/render.js` (QueueRenderer, ADR-004):**
  - Add `filterIsSet({ tenant, overLimit })`. It is true when a tenant is chosen or the switch is on (FR6.2).
  - `renderControls(view = { tenant: null, overLimit: false })` adds, inside the controls, `<button type="button" id="clear-filters" data-testid="queue-filters-clear-button">Clear filters</button>`. The button carries the `disabled` attribute when `filterIsSet(view)` is false (AC1.3.2, AC1.3.3, NFR10). It is a native button with a visible text label, so the disabled state is not shown by colour alone.
  - Calling it with no argument returns today's markup plus the disabled button, so the page's single call keeps working.
- **`index.html` (thin wiring only, A1):**
  - Import `filterIsSet`.
  - In `onChange`, set `clear.disabled = !filterIsSet(view)` through the DOM property, as the other controls are updated.
  - A click on the button calls `session.clear()` and then moves focus to `#tenant` (AC1.3.5). The page has no logic of its own beyond these calls.

## Steps

### Step 1: Branch and baseline (Way of Working)

- [x] Run `scripts\pull-all.ps1` so `origin/feature/F1220` is fresh.
- [x] In `priorauth-web`, create `f1220/us5162-clear-filters` from `origin/feature/F1220`. Its tip should be `b9c8448` or later, with US5161 merged.
- [x] Record the test baseline with `scripts\verify.cmd priorauth-web` before any change. The count is recorded in `code-summary.md`; the scan counted 38 tests.

### Step 2: Verify the test runner

- [x] Confirm that `scripts\verify.cmd priorauth-web` runs `npm test --silent` (`node --test`) and exits 0 on the baseline. No configuration change is needed. The command goes in `unit-test-instructions.md`.

### Step 3: Business logic: FilterSession, implement (US1.3 FR6.1, FR6.3, AC1.3.6; FR4.10)

- [x] Add `MESSAGES.droppedTenant`, put it into `PRIORITY` after `savedFilter`, and flag it in the FR4.8 branch at `open()`. Tag the lines `US5162 FR4.10`.
- [x] Add `clear()` to the returned session object, delegating to `change({ tenant: null, overLimit: false })`. Tag it `US5162 FR6.1`.
- [x] Update line 1's purpose comment to name US5162's additions.

### Step 4: Business logic: FilterSession, write and run its tests (test-after)

- [x] In `test/filter-session.test.js`:
  - Change the FR4.8 test (lines 267-274) to expect `MESSAGES.droppedTenant`. It keeps its other assertions.
  - Add the new tests:
    - **AC1.3.1:** from TX-01 with the switch on, `clear()` shows "All tenants" with the switch off, asks `/requests/pending`, and sends PUT `{"tenant":null,"overLimit":false}`.
    - **AC1.3.4:** the clear's save fails, so the whole queue still shows and the message is `notSaved`.
    - **AC1.3.6:** a save of TX-01 is still open when `clear()` runs. The PUTs are exactly TX-01 then the cleared filter, and the last one sent is the cleared filter.
    - **A2:** without a reviewer, `clear()` resets the view and sends no PUT.
    - **FR4.10:** a dropped tenant with the switch off also shows `droppedTenant`.
    - **FR4.10, Q2 A:** after a dropped tenant, `clear()` keeps `droppedTenant` once its save succeeds.
    - **FR4.10:** the two messages' texts differ, and `droppedTenant` doesn't claim that all requests are shown.
- [x] Run `scripts\verify.cmd priorauth-web`. Every test passes.

### Step 5: Frontend behaviour: QueueRenderer, implement (US1.3 FR6.2, NFR10)

- [x] Add `filterIsSet` and the Clear button in `renderControls(view)` as the Design describes, through the existing markup style. The button's label is fixed text, so no API value is rendered into it. Tag it `US5162 FR6.2, AC1.3.2, AC1.3.3, NFR10`.
- [x] Update line 2's purpose comment to name US5162's additions.

### Step 6: Frontend behaviour: QueueRenderer, write and run its tests (test-after)

- [x] In `test/render.test.js`, add:
  - **AC1.3.2:** `renderControls()` and `renderControls({ tenant: null, overLimit: false })` contain a native `<button type="button" id="clear-filters" ... disabled>Clear filters</button>`, inside the controls.
  - **AC1.3.3:** with `{ tenant: "TX-01", overLimit: false }`, `{ tenant: null, overLimit: true }`, and both set, the button has no `disabled` attribute.
  - **FR6.2:** `filterIsSet` is false for `{null, false}` and for `{"", false}` (the picker's "All tenants" value), and true otherwise.
- [x] Keep the US5161 controls test passing with the button added.
- [x] Run `scripts\verify.cmd priorauth-web`. Every test passes.

### Step 7: Page wiring (A1, AC1.3.5)

- [x] In `index.html`, import `filterIsSet`. Look up `#clear-filters`. In `onChange`, set `clear.disabled = !filterIsSet(view)`. On click, call `session.clear()` and then `select.focus()`. Tag it `US5162`.
- [x] No logic beyond these calls goes into the page. The focus move is listed for the manual check at the feature's Build and Test (AC1.3.5).

### Step 8: Documentation and traceability

- [x] Add the Clear button to `priorauth-web/README.md`'s description of the screen, only if it already lists the controls. Its stale branch notes are left alone (out of scope).
- [x] Write `code-summary.md` and `traceability.json` for AC1.3.1-AC1.3.6, FR6.1-FR6.3, FR4.10 and NFR10.

### Step 9: Final verification and commit

- [x] Run `scripts\verify.cmd priorauth-web`. Every test passes: the baseline count, plus the new tests, with the one changed FR4.8 test.
- [x] Commit on `f1220/us5162-clear-filters` with the message `US5162 clear my filters, and the dropped-tenant message (intent f1220-us5162)`. Do not push or open a PR; Tara Joshi does that.

## Story-to-Step Traceability

| Requirement / criterion | Steps | Test |
|---|---|---|
| FR6.1, AC1.3.1 Clear everything | 3, 7 | filter-session (AC1.3.1) |
| FR6.2, AC1.3.2 Disabled when nothing is set | 5, 7 | render (AC1.3.2), render (FR6.2 `filterIsSet`) |
| FR6.2, AC1.3.3 Enabled again | 5, 7 | render (AC1.3.3) |
| FR6.3, AC1.3.4 Clear but save fails | 3 | filter-session (AC1.3.4) |
| AC1.3.5 Focus after clearing | 7 | manual check at the feature's Build and Test |
| FR5.3, AC1.3.6 Clear while a save is open | 3 | filter-session (AC1.3.6) |
| FR4.10 Dropped-tenant message | 3 | filter-session (FR4.8 changed, FR4.10 switch off, Q2 A) |
| NFR5 Safe display | 5 | no API value is rendered into the button; existing escape tests stay green |
| NFR10 Accessibility | 5, 7 | render (AC1.3.2), manual keyboard check |
| A2 No reviewer, no save | 3 | filter-session (A2) |

## Security Checklist (team practice, for the mob's plan review)

- **Request values are validated and size-limited:** no new request value. Clear sends the fixed body `{"tenant":null,"overLimit":false}` through the existing contract C1 client.
- **API data is escaped before display:** the button's label and the new message are fixed text. The message is set with `textContent`, as today. Tenant values still go through `esc`.
- **No file path or cache key built from a caller's value:** not affected.
- **No stack traces or raw input in error responses:** not affected (no API change).
- **CORS only from named origins:** not affected.

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "We build each testable layer of a story, then write and run that layer's tests before starting the next layer; a bug fix instead starts with a failing test that reproduces the bug.",
  "scope": "express",
  "test_strategy": "minimal",
  "project_type": "brownfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "team",
      "text": "- **Methodology**: test-after\n- **Methodology evidence**: Affirmed by the team in the interview (Q4, answer A). The git history could not show a cadence (each F1210 story landed as one commit with its code and tests together); the team chose tests after each layer, keeping the workspace rule that a bug fix starts with a failing test.\n- **Ordering**: We build each testable layer of a story, then write and run that layer's tests before starting the next layer; a bug fix instead starts with a failing test that reproduces the bug.\n- Tests run only through the workspace verify script, `scripts/verify.sh` (`scripts\\verify.cmd` on Windows), never ad hoc. It runs `mvn -q test` for `priorauth-api` and `npm test --silent` (`node --test`) for `priorauth-web`.\n- CI stand-in (Q6, answer A): there is no CI service; the remotes are local repos. Before every PR the story owner runs the verify script with the repos named (`scripts\\verify.cmd priorauth-api priorauth-web`, or `scripts/verify.sh priorauth-api priorauth-web`) on the rebased branch and pastes the result into the PR. Setting up real CI is separate work.\n- Before any code change we record each repo's test baseline through the verify script with the repos named. A no-argument run on a clean `main` tests nothing and still exits 0, so it never counts as a baseline (Q7 A).\n- API tests stay independent of each other: each test uses its own `reviewerId`, or the store is reset between tests, so saved filters and history never leak between tests or depend on execution order (Q7 B).\n- Any time a test checks comes from a clock the test controls (an injected `Clock`), never the system clock (Q7 C).\n- Screen logic lives in `src/` modules that have tests; `index.html` only calls them. Code written inside `index.html` is neither tested nor counted (Q7 D).\n- New branching, parsing, money or security logic gets a test, and each story tests every new branch it adds. Every new or changed test file covers the happy path and at least two error or edge cases. Existing F1210 test files are not back-filled unless a story changes them or a plan names it.\n- Tests carry the FR/US they prove, in the test name or a comment on the `@Test`, as the existing tests do.\n- Coverage (Q5, answer X; Q13, answer A): F1220 adds no coverage tooling. The 80% line-coverage floor of the `feature` scope stays the target, but it is not measured in F1220. Build and Test reports coverage as NOT MEASURED and never claims the floor is met. This is a recorded exception to the organisation's coverage and CI-before-merge rule, owned by Meena Iyer, until a later feature adds JaCoCo (`priorauth-api`), Node test coverage (`priorauth-web`) and CI.\n- Tools: JUnit 5, AssertJ and Spring MockMvc in `priorauth-api`; the Node built-in runner (`node --test`) with `node:assert/strict` and an injected `fetchFn` in `priorauth-web`. There are no browser or DOM tests.\n- Baselines to preserve: `priorauth-web` 6 of 6 passing at `65a999b`. `priorauth-api` has 12 tests; its baseline is not yet recorded; Kiran Rao takes it through the verify script with the repos named before the first code change."
    }
  ],
  "obligations": {
    "strategy": "minimal",
    "strategy_volume": [
      "One verifiable test per requirement at the narrowest effective level.",
      "At least one happy-path unit test per component.",
      "Unit tests are the default; a bugfix/security scope floor may require an integration or E2E regression when that is the narrowest level that reproduces the defect."
    ],
    "scope_floor": [
      "Keep the existing test suite green.",
      "This scope adds no extra new-test floor beyond the selected test strategy."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Verify the existing test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Verify the existing test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:3ea1c5de97d92b72d157e8986e8f028cd43fe070f151b748e1d7c3c0a11cdd41",
  "contract_sha256": "sha256:1a77f4180a609a7f4d75b1d214b3fb66fe0d8211649c167a97a0163da56ad1f8"
}
```

Layers that don't apply to this story: data model and database, repository and data access (C1's client is unchanged), API and endpoint (no API change), and environment and build configuration.
