**Collaborator:** aidlc-quality-agent

## Contribution

Blind review of the lead draft from the testing and quality-gate angle. Sources inspected: the four lead artifacts; `scripts/verify.sh`, `scripts/verify.cmd`, `scripts/verify.ps1`; `priorauth-api/pom.xml` and its six test classes under `src/test/java/`; `priorauth-web/package.json` and its three files under `test/`; `codekb/priorauth-api/code-quality-assessment.md`, `codekb/priorauth-web/code-quality-assessment.md`, both `technology-stack.md`; the workspace `CLAUDE.md`; `memory/org.md` and `memory/phases/construction.md`. Local Node is `v24.19.0` (`node --version`); `package.json` declares `engines.node >=20`.

### 1. What the evidence confirms (the lead's draft is right)

- The verify script is the single test path and it runs unit tests only: `mvn -q test` and `npm test --silent` (`node --test`). There is no coverage, lint, build or packaging step in it, in either repo, or in any CI file.
- Tools: JUnit 5 + AssertJ + MockMvc (`spring-boot-starter-webmvc-test`, test scope) in the API; `node:test` + `node:assert/strict` with an injected `fetchFn` in the web repo. No browser/DOM tests, no contract tests, no performance or security tests.
- Test shape in the API: 3 plain unit classes (`aging/`, `store/`) and 3 `@SpringBootTest` + MockMvc classes (`api/`), so roughly half unit, half in-process integration. Tests mirror the main packages, use behaviour-sentence names, and carry the FR/US they prove in a comment (`@Test // US5151: ...`) or in the test title (`"... (US5153)"`). This traceability habit is worth affirming as a team practice; it is what lets Build and Test map tests to acceptance criteria.
- No coverage is measured anywhere, so the `feature` scope's 80% line floor and CI-before-merge (org `## Testing Posture`) cannot be demonstrated today (codekb TD-6 in both repos).

### 2. Corrections and precision the lead should integrate

1. **The verify script's "PR base" is `origin/HEAD`, not the feature branch.** `verify.sh`/`verify.ps1` compare the current branch with `refs/remotes/origin/HEAD` (i.e. `main`). On a story branch `f1220/us<id>-<word>` or on `feature/F1220` the repo is tested, which is correct. But on a clean `main` the script prints "nothing to test" and exits 0. **The pre-change baseline (lead's open question 7) must therefore be run with the repos named explicitly**: `scripts\verify.cmd priorauth-api priorauth-web` (`scripts/verify.sh priorauth-api priorauth-web`). A no-argument run on `main` would record a false "pass".
2. **Measuring coverage in `priorauth-web` is dependency-free, enforcing it is not version-free.** `node --test --experimental-test-coverage` exists from Node 20, but the threshold flags that make a run fail below a floor (`--test-coverage-lines`, `--test-coverage-branches`) and the exclusion flags (`--test-coverage-include` / `--test-coverage-exclude`, needed so `test/*.test.js` do not count toward their own coverage) arrive only in Node 22.x. With `engines.node >=20` a developer on Node 20 can measure but not gate. The team must choose: raise `engines.node` (a change a plan must name), or accept a reported-but-not-enforced figure in the web repo.
3. **JaCoCo and the verify script do not line up by default.** The JaCoCo `report` and `check` goals bind to Maven's `verify` phase; the verify script runs `mvn -q test`, so a floor configured the usual way would never run through the only sanctioned test path. Either the plan binds `check` to the `test` phase in `pom.xml`, or the workspace verify script changes to `mvn -q verify` (which also repackages the Boot jar; slower, and a change to a script every repo and person uses). This is a decision, not a detail.
4. **Coverage in the web repo cannot see `index.html`.** Node coverage counts only the ES modules the tests import. The inline module script in `index.html` (page bootstrap, wiring, the place F1210's filters were never connected, codekb web TD-1) is invisible to both tests and coverage. F1220's US5161 "restore my filter on open" and "clear" behaviour would be untested and uncounted if written inline. Proposed practice for the interview: **page logic lives in `src/` modules with injected `fetchFn`/storage, and `index.html` stays a thin call into them.**
5. **New mutable state breaks test independence in the API unless the team picks a pattern.** Every `@SpringBootTest` class shares one cached Spring context, and the store is a singleton in memory. Today the store is read-only, so this is harmless. F1220 adds saved filters and history that tests will write; writes from one test class would leak into another and make results depend on execution order. Candidate practices: each test uses its own `reviewerId` (cheapest, no annotation), or the store exposes a test reset, or `@DirtiesContext` (slow). The team should pick one before Construction.
6. **Fixture coupling.** API tests assert absolute row counts from `data/requests.sample.json` (`TenantFilterTest` expects 3 and 0; `OverLimitFilterTest` expects one id on 13 Oct). Codekb TD-2 notes that adding the missing tenant `NM-02` shifts counts in three classes. Any F1220 data change will ripple through existing tests; either the plan names those test updates, or new tests build their own data rather than editing the shared sample.
7. **Time.** `LocalDate.now()` with no injectable `Clock` (API TD-4). F1220's audit/history timestamps in UTC can only be asserted deterministically through an injected `Clock`. Recommend affirming "time comes from an injected `Clock` in code under test" as a coding practice.

### 3. Existing suite vs. the phase rule

`memory/phases/construction.md` requires each test file to cover the happy path and at least two error or edge cases. Several existing files do not: `TenantFilterTest` and `OverLimitFilterTest` have one test each; `queue-filters.test.js` never exercises `loadQueue`'s non-2xx path; `render.test.js` never exercises `esc` with `& < > "` (web TD-7, an XSS-relevant gap). The interview should confirm the rule applies to **new and changed test files only**, so F1220 stories are not drawn into back-filling F1210 tests unless a plan names it. (If a story touches one of these files, it is a changed file and the rule applies.)

### 4. Cross-repo contract

The web tests stub the API with hand-written JSON (`fetchFn` returning `[{ id: "PA-10231" }]`); nothing checks that the stub matches what the API actually returns. F1220 adds new endpoints whose contract the parent intent owns, and US5161 may start against the agreed contract before US5160 lands. Without a new dependency (no Pact), a lightweight practice is: the parent's API contract carries one example request/response per endpoint; the API's MockMvc test asserts the response against that example's fields, and the web test uses the same example as its stub. The interview should decide whether that is wanted.

### 5. Suggested testing-posture questions (only what evidence cannot settle)

Phrased for the interview in plain words; the lead may merge them with its own Q4-Q7.

- **Cadence.** "When you build a story, which comes first: the tests (test-first), the acceptance scenarios in Given/When/Then that then become tests, or the code with tests written right after each layer?" Evidence is neutral: code and tests always land in one commit. If the answer mixes cadences (scenarios first, unit tests after), record `custom` with the ordering spelled out.
- **Coverage floor.** "The feature scope expects 80% of lines covered. Measured per whole repo, or only on code the story changed? Line only, or line and branch?" Recommend measuring each repo's current coverage during the baseline run first: if a repo is already below 80% overall, a whole-repo floor would block the first F1220 story for reasons outside its scope.
- **Tooling owner and placement.** "Who adds JaCoCo to `priorauth-api` and the coverage flags to `priorauth-web`, in which story or a separate first unit, and does the verify script change?" (both are named-in-plan changes; see §2.2-2.3).
- **CI stand-in.** "There is no CI service (remotes are local bare repos). Is a verify-script run on the rebased branch, with its output pasted in the PR, the accepted 'CI before merge'?"
- **Test isolation** (§2.5) and **page logic in modules** (§2.4).
- **Phase rule scope** (§3).
- **UI acceptance.** "With no browser tests, is the feature demo to Dana Ortiz the acceptance check for the screen, plus a written manual check list for restore and clear?" (adding a browser test tool is a new dependency.)

### 6. Quality gates as the evidence supports them today

| Gate | What exists | Gap |
|---|---|---|
| Before code change | Nothing recorded for the API; web 6/6 at `65a999b` | Record API baseline (expected 12/12) with explicit repo names; add coverage % once tooling exists |
| Before PR | Verify script, run by the owner after rebase (`CLAUDE.md`) | No coverage, no lint, no record that it ran |
| Before feature-to-`main` | Parent's Build and Test | Coverage floor and CI need a decided mechanism or the floor cannot be met (Build and Test may not weaken it) |
| Release | Feature demo, product-owner acceptance | No smoke check; restart empties saved filters (documented in release notes) |

## Positions

- AGREE: Testing Posture draft keeps `test-after` only as the framework default and marks it "draft: confirm"; the history genuinely cannot show cadence.
- AGREE: The verify script as the single test path, run before saying done, belongs in `discovered-rules.md` as a Mandated rule.
- AGREE: Tension T3 (coverage floor and CI) must be settled before Construction, since Build and Test may not weaken a defined floor.
- OBJECT: team-practices line 28 should add that a baseline or any run on a clean `main` must name the repos explicitly; with no arguments the script exits 0 having tested nothing.
- OBJECT: team-practices line 32 says the web repo can meet the floor with no new dependency; it can measure, but enforcing a threshold and excluding test files needs Node 22.x while `engines.node` is `>=20`, so the draft should say so.
- OBJECT: team-practices line 32 omits that JaCoCo's `check` goal does not run under `mvn -q test` by default; the coverage question should include whether the verify script or the pom binding changes.
- OBJECT: `discovered-rules.md` leaves out a written hard constraint from the workspace `CLAUDE.md` ("new branching, parsing, money or security logic gets a test"); it is a stated rule, not an inference, so it belongs under `## Mandated`.
- AGREE: The API surefire reports are correctly treated as supporting evidence only, not a recorded baseline.
