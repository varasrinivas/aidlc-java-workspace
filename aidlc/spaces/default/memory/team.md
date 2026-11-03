# Team-Level Rules

> This team's affirmed practices and corrections. Loaded after `org.md` as
> strict-additive guidance; contradictions with broader policy are rejected.
> Populated by the practices-discovery affirmation gate. Edit at the gate,
> not directly.

## Way of Working

This is our team's practice in place of the organisation default (trunk-based development with 1-2 day branches merged straight to `main`, squash-merged). We chose it on purpose and recorded the conflict with `memory/org.md` (interview Q1, Q2, Q14, answer A each).

- We keep two code repos, `priorauth-api` and `priorauth-web`, each with its own git, origin and pull requests. The PR base of both is `main`.
- One Rally story = one AI-DLC unit = one intent = one branch = one PR, driven only by the story's Rally owner. A change across both repos is one PR per repo, each naming the other.
- For a multi-story Rally feature, the tech lead creates `feature/F<id>` in every code repo the feature changes, cut from that repo's current `main`. For F1220 that is `feature/F1220` in `priorauth-api` and `priorauth-web`, cut from current `main` (not from the stray `f1210-answer-python` tag). The feature branch lives until the feature's release (F1220: 2027.Q1 R1).
- Story branches are named `f<id>/us<id>-<word>` and cut from `origin/feature/F<id>`. Story PRs go into the feature branch. One PR goes from the feature branch to `main` after the parent intent's Build and Test.
- AI-DLC Construction worktrees for a story of a multi-story feature use `feature/F<id>` as both the base branch and the merge target; for F1220 the base is `feature/F1220` and the merge target is `feature/F1220`. Nothing from a story merges straight to `main`.
- We merge every PR with a merge commit, as we did for F1210: story PRs into the feature branch, the feature branch into `main`, and AI-DLC worktree merges (`--strategy merge`). We do not squash.
- Other branch names: `<intent label>/<unit slug>` for a single-intent feature, `fix/<intent label>` for a bug fix, `hotfix/<intent label>` cut from the release tag for a production fix. The same name is used in every repo the work touches.
- Every branch starts from its PR base, freshly pulled (`scripts/pull-all.sh`, `scripts\pull-all.ps1` on Windows), never from another person's branch.
- A story branch is not cut before the stories it depends on are merged into the feature branch (the parent's Delivery Planning lists them). A story that needs only an agreed contract can start at once.
- Before a PR the story owner runs `git fetch`, rebases the story branch onto `origin/feature/F<id>`, keeps both stories' changes on a conflict, runs the verify script and pushes with `git push --force-with-lease`.
- The code is committed on the unit's branch as the plan's last step. Pushing code branches and opening PRs is done by people, not by AI-DLC. The AI-DLC record (`aidlc/`) is committed and pushed to the workspace's `main` after every gate: only the intent's own folder, `git pull --rebase`, then push; on an `intents.json` conflict, keep every row from both sides.
- The parent feature intent's gates 2.3 to 2.9 are decided as a mob (the whole team, one person typing), with the deciders' names and any dissent written down. Each story's code plan (3.5) is reviewed by the mob before code is written; plan approval is on in every child intent.

## Walking Skeleton

We don't run a walking-skeleton ceremony: the stance is off. We do not build a thin end-to-end slice first. A feature's stories are built in parallel, each in its own child intent, against the contract the parent intent agreed, and they are proven together at the feature's Build and Test with the verify script (interview Q3, answer B). For F1220 that means US5160, US5161, US5162 and US5163 do not wait on a first US5160 + US5161 slice; the dependency order in the parent's Delivery Planning still applies.

## Testing Posture

- **Methodology**: test-after
- **Methodology evidence**: Affirmed by the team in the interview (Q4, answer A). The git history could not show a cadence (each F1210 story landed as one commit with its code and tests together); the team chose tests after each layer, keeping the workspace rule that a bug fix starts with a failing test.
- **Ordering**: We build each testable layer of a story, then write and run that layer's tests before starting the next layer; a bug fix instead starts with a failing test that reproduces the bug.
- Tests run only through the workspace verify script, `scripts/verify.sh` (`scripts\verify.cmd` on Windows), never ad hoc. It runs `mvn -q test` for `priorauth-api` and `npm test --silent` (`node --test`) for `priorauth-web`.
- CI stand-in (Q6, answer A): there is no CI service; the remotes are local repos. Before every PR the story owner runs the verify script with the repos named (`scripts\verify.cmd priorauth-api priorauth-web`, or `scripts/verify.sh priorauth-api priorauth-web`) on the rebased branch and pastes the result into the PR. Setting up real CI is separate work.
- Before any code change we record each repo's test baseline through the verify script with the repos named. A no-argument run on a clean `main` tests nothing and still exits 0, so it never counts as a baseline (Q7 A).
- API tests stay independent of each other: each test uses its own `reviewerId`, or the store is reset between tests, so saved filters and history never leak between tests or depend on execution order (Q7 B).
- Any time a test checks comes from a clock the test controls (an injected `Clock`), never the system clock (Q7 C).
- Screen logic lives in `src/` modules that have tests; `index.html` only calls them. Code written inside `index.html` is neither tested nor counted (Q7 D).
- New branching, parsing, money or security logic gets a test, and each story tests every new branch it adds. Every new or changed test file covers the happy path and at least two error or edge cases. Existing F1210 test files are not back-filled unless a story changes them or a plan names it.
- Tests carry the FR/US they prove, in the test name or a comment on the `@Test`, as the existing tests do.
- Coverage (Q5, answer X; Q13, answer A): F1220 adds no coverage tooling. The 80% line-coverage floor of the `feature` scope stays the target, but it is not measured in F1220. Build and Test reports coverage as NOT MEASURED and never claims the floor is met. This is a recorded exception to the organisation's coverage and CI-before-merge rule, owned by Meena Iyer, until a later feature adds JaCoCo (`priorauth-api`), Node test coverage (`priorauth-web`) and CI.
- Tools: JUnit 5, AssertJ and Spring MockMvc in `priorauth-api`; the Node built-in runner (`node --test`) with `node:assert/strict` and an injected `fetchFn` in `priorauth-web`. There are no browser or DOM tests.
- Baselines to preserve: `priorauth-web` 6 of 6 passing at `65a999b`. `priorauth-api` has 12 tests; its baseline is not yet recorded; Kiran Rao takes it through the verify script with the repos named before the first code change.

## Guard Policy

<!-- Affirmed by the team. Mode: strict, relaxed, or off. Strict here holds for every intent, whatever one person asks in chat; relaxed or off here applies to every intent whose policy came from its scope, unless project.md or the person sets another; changing this line changes it. A section under the retired Change Control heading, written by an earlier release, is still read. -->

## Deployment

- We have no deployed environments for `priorauth-api` or `priorauth-web` (Q8, answer A). Nothing deploys on merge; there is no staging or production environment and no deploy pipeline.
- A release is the PR from the feature branch to `main` plus a version tag in each repo the feature changed. The demo runs locally from `main`, and the product owner, Dana Ortiz, accepts the feature after the demo.
- Meena Iyer bumps the version in each repo's build file (`pom.xml`, `package.json`) and tags each repo when the feature branch merges to `main`; a feature gets a minor version (Q9, answer A). Before proposing a version or a tag we check the repo's existing tags and its build file (today `priorauth-api` `v1.1.0` with `pom.xml` at `1.1.0`, `priorauth-web` `v1.0.0`).
- F1220 ships in release 2027.Q1 R1. Its release notes say the filter history is lost on restart and that anyone using the screen can read it; Meena Iyer writes that line.

## Code Style

We keep style by convention and review, with no formatter or linter in F1220 (Q10, answer A). The conventions below are the written standard that reviewers and Code Generation check new code against.

**Both repos**
- We make the smallest complete change: prefer what already exists (this codebase, the platform libraries, an installed dependency) over new code, and add no features, options or abstractions nobody asked for.
- We touch only the repos and files the approved plan names, match the surrounding style, and mention unrelated problems instead of fixing them.
- A new dependency is named in the plan before it is added.
- Code and tests are tagged with the FR/US they implement: in the class Javadoc or file header where a requirement introduced the code, on the line a story changed, and on the test that proves it.

**`priorauth-api` (Java 21, Spring Boot, Jackson 3)**
- One module, root package `com.acmehealth.priorauth`; packages `api` (controller, query and response records), `model` (domain records), `store` (data access), and feature packages such as `aging`. Tests mirror the main package tree.
- Dependencies point one way: `api -> aging, store, model`; `store -> model`. HTTP concerns (status codes, `ResponseStatusException`, request binding) stay in `api`; domain and store code never import Spring web classes.
- Responses are separate records in `api` (`PendingRequestResponse.from(...)`); domain records are never returned directly.
- Names follow the domain: `<Thing>Controller`, `<Thing>Response`, `<Thing>Store`; records for data; static factories `of(...)` (computes) and `from(...)` (maps). Configuration keys are kebab-case under `priorauth.` with a default in `@Value`.
- Test classes are `<ClassUnderTest>Test` for domain code and a controller or per-behaviour class for HTTP; test methods are behaviour sentences in camelCase.
- Errors: domain code throws `IllegalArgumentException` with a message naming the bad values for caller errors and `IllegalStateException` wrapping the cause for unrecoverable I/O; the controller maps a caller error to HTTP 400, never 500. Missing optional data gets an explicit, documented safe default.
- 4-space indent, continuation lines 8; imports grouped app, third-party, `java.*`, then static; no wildcard imports in main code.
- Records for data, `final` utility classes with a private constructor for pure functions, constructor injection only in main code, immutable collections. Methods stay short.
- Jackson 3 packages (`tools.jackson.databind`) only, never `com.fasterxml.jackson`.
- Every main class has a one-line purpose Javadoc; it names the FR/US where a requirement introduced the class (not every class has one, for example `PriorAuthApiApplication`).
- `pom.xml` takes versions from the Spring Boot parent and puts a one-line comment above each dependency and plugin saying why it is there.

**`priorauth-web` (JavaScript ES modules, no dependencies)**
- `index.html` holds markup, CSS and a thin inline module script, the only DOM-touching code. Everything in `src/` is DOM-free and tested: URL builders, network calls with an injected `fetchFn = fetch` as the last parameter, and string rendering.
- One test file per `src/` module (`test/<module>.test.js`); no build step; relative imports with the `.js` extension.
- Kebab-case file names; camelCase function names in domain language; named exports only, no default exports, no classes. Optional query parameters are omitted when unset.
- A non-2xx answer throws a plain `Error` whose message names the service and the status.
- Every rendered value goes through the one shared escape helper (`esc`).
- 2-space indent, double quotes, semicolons, template literals, arrow functions for small callbacks, default parameters for options.
- Line 1 of every `src/` file is a one-line purpose comment, naming the story and contract where a story introduced it; no JSDoc. Tests use `node:test` and `node:assert/strict`, with behaviour-sentence names carrying the story tag.

**Security checklist at each code-plan review (Q11, answer A)**

The mob checks each story's code plan (3.5) against this list, with no new tool:
- Every request value is validated and size-limited.
- API data is escaped before it is shown on the page.
- No file path or cache key is ever built from a caller's value.
- Error responses carry no stack traces and no raw caller input.
- Browser calls are allowed only from named origins (CORS), never `*`.
## Forbidden

<!-- Team-specific forbidden patterns -->

## Mandated

<!-- Team-specific mandates -->

## Corrections

<!-- Self-learning loop appends here. -->
