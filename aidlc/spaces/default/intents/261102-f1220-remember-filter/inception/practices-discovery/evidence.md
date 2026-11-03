# Practices Discovery Evidence

> Lead: aidlc-pipeline-deploy-agent. Draft 2026-11-02T15:49:38Z, integrated 2026-11-02T16:03:32Z, workspace commit `5f5844d`. Brownfield, scope `feature`, Standard depth, active space `default`. `memory/team.md` and `memory/project.md` were empty templates, so there was no affirmed baseline; `memory/org.md` was read as the default practice only. Three support reviews ran blind to each other, then the team answered a 14-question interview and confirmed its summary ("Looks correct"). The human answers decide every practice here; the reviews shaped wording and detail.

## Sources

### Lead (aidlc-pipeline-deploy-agent)

| Source | What it gave us |
|---|---|
| `CLAUDE.md` (workspace root, checked in) | Branch naming, one story = one intent = one branch = one PR, `feature/F<id>` with story PRs into it, mob decisions, plan approval on in children, verify script as the only test path, "name a new dependency in the plan", "a bug fix starts with a failing test", "check tags and build file before a version", pushing and PRs done by people, record pushed after every gate. Source of every rule in `discovered-rules.md` except the three added from Q12. |
| `README.md` (workspace) | F1210 precedent: `feature/F1210` cut from tag `v1.1.0` in `priorauth-api`; tests through `scripts/verify.sh priorauth-api priorauth-web`. |
| `scripts/verify.sh`, `scripts/verify.cmd`, `scripts/pull-all.sh` | Verify runs `mvn -q test` / `npm test --silent` only (no coverage, lint or build step); pull-all fast-forwards a clean PR base, otherwise only fetches. |
| `repos.json` | Remotes are local bare repositories; no hosted platform, CI or environment protection. |
| `.claude/scopes/aidlc-feature.md`, `aidlc-state.md` | `feature` scope has `skeleton: on`; Brownfield, Standard depth and test strategy, unit-major, serial. |
| Git history of `priorauth-api` and `priorauth-web` (read-only) | Only `main` exists; F1210 story PRs #71-#74 merged with merge commits; each story is one commit holding code and tests; tags `v1.0.2`, `v1.1.0` (API) and `v1.0.0` (web); `pom.xml` still `1.1.0`; a stray `f1210-answer-python` tag off `main` in the web repo. |
| CI, deployment and tooling search in both repos | No `.github/`, pipeline file, `Dockerfile`, `.editorconfig`, formatter, linter, Maven wrapper or lockfile. |
| `priorauth-api/target/surefire-reports/` (local, not committed) | 12 tests, 0 failures, run 2026-11-02; supporting evidence only, not a recorded baseline. |
| Ideation record (`scope-document.md`, `decision-log.md`, `mob-composition.md`, `stakeholder-map.md`, `intent-capture-questions.md`) | Release 2027.Q1 R1; Dana Ortiz accepts after the demo; Meena Iyer writes the release-notes line on history limits. |

### Reverse-engineering knowledge bases (upstream artifacts)

| Upstream artifact | Used for |
|---|---|
| `codekb/priorauth-api/technology-stack.md`, `codekb/priorauth-web/technology-stack.md` | Test tools, no coverage/lint/CI/container, versions and tags. |
| `codekb/priorauth-api/code-quality-assessment.md`, `codekb/priorauth-web/code-quality-assessment.md` | 12 API tests without a recorded baseline; web 6/6 at `65a999b`; TD-6 coverage gaps; web TD-7 (`esc` misses `'`, untested); style by convention. |
| `codekb/priorauth-api/dependencies.md`, `codekb/priorauth-web/dependencies.md` | JaCoCo would be a new plugin; web repo has zero dependencies. |
| `codekb/priorauth-api/code-structure.md`, `codekb/priorauth-web/code-structure.md` | Tests mirror packages / one test file per module; FR/US tags on tests. |
| `codekb/priorauth-api/architecture.md`, `codekb/priorauth-web/architecture.md` | No persistence (state lost on restart); a single Spring Boot jar and a static page: what a release and a demo can be. |
| `codekb/priorauth-api/business-overview.md`, `codekb/priorauth-web/business-overview.md` | Scanned for delivery facts; nothing on environments or release practice. |

### Quality engineer (aidlc-quality-agent, `contributions/aidlc-quality-agent.md`)

Inspected the verify scripts (`.sh`, `.cmd`, `.ps1`), `pom.xml` and all six API test classes, `package.json` and the three web test files, both code-quality and technology-stack codekb files, `CLAUDE.md`, `memory/org.md`, `memory/phases/construction.md`, and the local Node version (`v24.19.0` against `engines.node >=20`). Found: the verify script compares with `origin/HEAD`, so a no-argument run on clean `main` tests nothing and exits 0 (became Q7 A); enforcing a Node coverage threshold needs Node 22 and JaCoCo's `check` does not run under `mvn -q test` (shaped Q5); `index.html` code is invisible to tests (Q7 D); new mutable state would leak between `@SpringBootTest` classes (Q7 B); `LocalDate.now()` with no injectable `Clock` (Q7 C); fixture coupling to `data/requests.sample.json`; several existing test files fall short of the happy-path-plus-two rule, so the rule applies to new and changed test files; no contract check between web stubs and the API.

### Developer (aidlc-developer-agent, `contributions/aidlc-developer-agent.md`)

Read every main and test source file in both repos, `application.yml`, `pom.xml`, `index.html`, `package.json`, the code-structure and code-quality codekb files and `CLAUDE.md`; ran nothing. Produced the per-repo conventions list (layer boundaries, naming, error handling, style, comments, traceability tags) adopted as the written standard in Q10. Corrected the draft: not every API class names an FR/US in its Javadoc (`PriorAuthApiApplication`, `PendingRequestResponse`, `RequestStore` do not), so the convention is a purpose Javadoc on every class with requirement tags where a requirement introduced it. Flagged the over-broad "never push" rule (narrowed by Q12 D), two unrecorded `CLAUDE.md` rules (added by Q12 B, C), and the joined `memory/` / `codekb/` rule (now split). Noted open design items: duplicated fetch-and-throw code (web TD-2), no shared API error body (TD-5), no injectable `Clock` (TD-4), no user-visible error on the page (TD-9).

### Security engineer (aidlc-devsecops-agent, `contributions/aidlc-devsecops-agent.md`)

Read both `pom.xml`, `package.json` and `.gitignore` files, the workspace `.gitignore`, `scripts/verify.sh`, `application.yml`, `PendingRequestsController.java`, `HolidayCalendar.java`, `render.js`, `index.html`, the dependencies, technology-stack, code-quality and api-documentation codekb files, `scope-document.md` and `CLAUDE.md`. Found no SAST, DAST, secret scanning, dependency scanning or CI; no Bean Validation on the classpath; no CORS configuration; `.gitignore` without secret-file patterns; Maven unpinned. Rated High for F1220: caller-supplied values rendered through an incomplete `esc`, unbounded in-memory growth from unauthenticated writes, and writes/impersonation not covered by the accepted read risk. These shaped Q11 (secure-coding checklist at plan review, no new tool).

## Interview decisions

| Q | Topic | Decision |
|---|---|---|
| Q1 | Where stories merge | A: `feature/F1220` per repo cut from current `main`; story PRs into it; one PR to `main` after Build and Test; AI-DLC worktree base and merge target `feature/F1220`; lives until 2027.Q1 R1 |
| Q2 | PR merge style | A: merge commits for every PR, as for F1210 (Meena Iyer) |
| Q3 | Thin end-to-end slice first | B: no; stories built in parallel against the agreed contract, proven together at the feature's Build and Test |
| Q4 | When tests are written | A: tests after each layer; bug fixes start with a failing test |
| Q5 | Coverage floor | X: no coverage tooling in F1220; 80% stays a target; a later feature adds JaCoCo, Node coverage and CI (Meena Iyer); each story still tests every new branch |
| Q6 | CI stand-in | A: owner runs `scripts\verify.cmd priorauth-api priorauth-web` before every PR and pastes the result into the PR; real CI is separate work |
| Q7 | Testing practices | A, B, C, D: baseline with repos named; independent API tests; test-controlled clock; screen logic in `src/` modules |
| Q8 | Environments and release | A: no deployed environments; release = PR to `main` + version tag; local demo from `main`; Dana Ortiz accepts |
| Q9 | Version and tag | A: Meena Iyer bumps build files and tags each repo at the merge to `main`; minor version for a feature |
| Q10 | Code style | A: convention and review, developer's list as the written standard; no formatter or linter |
| Q11 | Security checks | A: mob secure-coding checklist at each code-plan review; no new tool |
| Q12 | Recorded rules | A, B, C, D: three new ALWAYS rules; "never push / open a PR" narrowed to code-repo branches and PRs |
| Q13 | Coverage vs organisation rule | A: recorded exception (see below) |
| Q14 | Branching vs organisation rule | A: recorded as the team's practice (see below) |

### Recorded conflicts with `memory/org.md`

1. **Coverage and CI (Testing Posture).** `org.md` gives the `feature` scope an 80% line-coverage floor and CI execution before merge, and says Build and Test may not weaken defined floors. The team keeps no coverage tooling and no CI in F1220 (Q5, Q13 A). Recorded as an exception owned by Meena Iyer: Build and Test reports coverage as NOT MEASURED and never claims the floor is met; the later feature that adds JaCoCo, Node coverage and CI closes the gap. The floor is not lowered, only unmeasured.
2. **Branching and merge style (Way of Working).** `org.md` says trunk-based, 1-2 day branches to `main`, Construction worktrees based on and merged to `main`, squash-merge. The team keeps a per-feature integration branch living until the release, worktrees based on and merged to `feature/F<id>`, and merge commits (Q1, Q2, Q14 A). The team chose to record this as its own practice; if promotion refuses it as a contradiction, `memory/org.md` must change first (Q14 A).

## Assumptions & Open Questions

- **API baseline not yet recorded.** `priorauth-api` has 12 tests (local Surefire shows 12/12) but no recorded baseline. It must be taken with `scripts\verify.cmd priorauth-api priorauth-web` before the first code change; who runs it is not yet named.
- **Deployment default may also be read as a conflict.** `org.md` `## Deployment` assumes deploy-on-merge to staging and a gated production. The team has no environments (Q8 A), so there is nothing to deploy to; this was not raised as a third conflict. If promotion's admission check refuses `## Deployment`, the same path as Q14 applies. Rollback and smoke checks for the Operation stages are undefined because nothing is deployed; the local demo is the only post-release check.
- **Accepted risk, for Requirements Analysis.** The scope accepts that anyone using the screen can read a reviewer's history. It does not say whether anyone may also overwrite another reviewer's saved filter or write history in their name, which an untrusted `reviewerId` allows. Hand this to Requirements Analysis to accept explicitly or narrow.
- **For design (Application Design / Contract Design and the story plans):**
  - CORS: none is configured today, and the new `PUT` with a JSON body needs a preflight; add a named-origin allowlist (`GET`, `PUT` only), never `*`.
  - Holiday-calendar trap: `HolidayCalendar.forTenant(tenantId)` builds a classpath path and an unbounded cache key from its argument; F1220 code must not pass a caller-supplied tenant to it.
  - `esc` does not escape `'` and has no hostile-input test; the first story that renders a caller-supplied value should fix and test it in its plan.
  - Size limits on what unauthenticated callers can make the in-memory store keep belong in the NFRs.
  - First instances of a shared API error body, an injectable `Clock` and a user-visible page error: one choice should be named in design so both stories follow it.
  - Fixture coupling: new API tests should build their own data rather than edit `data/requests.sample.json`, or the plan names the existing tests it changes.
- **Not decided here:** whether Construction continues automatically or stops at each checkpoint (asked at Construction entry, since the skeleton stance is off); a contract check between web stubs and API responses; `.gitignore` secret patterns, a secret scanner, SAST and a dependency-advisory owner (deferred with CI).
