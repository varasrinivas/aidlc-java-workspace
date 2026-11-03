# Practices Discovery — Questions

These questions settle how the team builds, tests, merges and ships, for F1220 and after. They ask only what the evidence could not establish. The draft is `team-practices.md` in this folder, and the reviews from the quality engineer, developer and security engineer are in `contributions/`.

Your answers become the team's recorded practices (`memory/team.md`) when you approve this stage.

## Q1. Where do F1220's stories merge while the feature is being built?

Your workspace rules say a multi-story feature gets a `feature/F1220` branch in each repo. Story PRs go into it, and one PR goes from it to `main` after the feature's Build and Test. The framework default is short branches merged straight to `main` within 1-2 days. This also decides where AI-DLC starts and merges each story's work.

A. Keep the workspace rule: `feature/F1220` in each repo, cut from the current `main`; story PRs go into it, and one PR goes to `main` after Build and Test. AI-DLC uses `feature/F1220` as the base and merge target for story work. It lives until the 2027.Q1 R1 release.
B. Merge each story straight to `main` and drop the feature branch
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q2. How are pull requests merged?

Both repos' history shows merge commits ("Merge pull request #71"). The framework default is to squash each story into one commit.

A. Keep merge commits for every PR
B. Squash story PRs into the feature branch; use a merge commit for the feature branch into `main`
C. Squash every PR
D. Not yet decided
X. Other (please specify)

[Answer]: A. Merge commits, as for F1210 (Meena Iyer).

## Q3. Build a thin end-to-end slice first?

A walking skeleton is a minimal version that runs the whole way through, built first to prove the pieces connect before the real features go in. For F1220 that would be the saved-filter API (US5160) wired to the screen that restores it (US5161), proven with the verify script before US5162 and US5163.

A. Yes: build US5160 + US5161 end to end first, prove it, then the other two stories
B. No: the stories are built in parallel against the agreed contract and proven together at the feature's Build and Test
C. Not yet decided
X. Other (please specify)

[Answer]: B. Built in parallel against the agreed contract, proven together at the feature's Build and Test.

## Q4. When are tests written?

The history can't tell: each F1210 story landed as one commit with its code and tests together. Your rules already say a bug fix starts with a failing test.

A. Tests after: build each layer, then write and run its tests before the next layer (bug fixes still start with a failing test)
B. Test-first (TDD): a failing test before each piece of code
C. Acceptance first: write the story's Given/When/Then scenarios as tests first, then unit tests after each layer
D. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q5. How is the 80% line-coverage floor measured and enforced?

The feature workflow requires 80% line coverage. Neither repo measures coverage today. Measuring it means:

- The screen can use Node's built-in coverage, with no new dependency. Making a run fail below the floor needs Node 22 or later, but `package.json` allows Node 20.
- The API needs a new Maven plugin (JaCoCo), which must be named in a plan. Its check must also run through the verify script, which today runs `mvn -q test`.

A. 80% on the code each story adds or changes. The tooling goes in with the first story in each repo: JaCoCo in US5160's plan, bound so the verify script runs it, and Node coverage plus a Node 22 minimum in US5161's plan.
B. 80% on the whole repo, enforced the same way as option A
C. Measure and report coverage this feature, but don't fail the run on it yet
D. Not yet decided
X. Other (please specify)

[Answer]: X. No coverage tooling in F1220: the 80% floor stays a target, and a later feature adds JaCoCo and Node coverage with CI (Meena Iyer). Each story still tests every new branch.

## Q6. What stands in for "CI before merge"?

There is no CI service: the remotes are local repos. Your rules say tests run only through the verify script.

A. No CI service for now. The story owner runs the verify script with the repos named (`scripts\verify.cmd priorauth-api priorauth-web`) before every PR and pastes the result into the PR. Setting up real CI is a separate piece of work.
B. Set up a CI service as part of F1220 (please say who and where under Other)
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q7. Which testing practices does the team adopt? (select all that apply)

The reviews found these gaps. F1220 is the first code that needs each one.

A. Record each repo's test baseline through the verify script, with the repos named, before any code changes. With no repos named on a clean `main`, the script tests nothing and still passes.
B. Keep API tests independent of each other: each test uses its own reviewer id, or the store is reset between tests. Saved filters and history would otherwise leak between tests.
C. Times that tests check come from a clock the test controls, not the system clock.
D. Screen logic lives in `src/` modules with tests; `index.html` only calls them. Code inside `index.html` is neither tested nor counted.
E. None of these
X. Other (please specify)

[Answer]: A, B, C, D.

## Q8. Which environments exist, and how does a release go out?

The repos have no deployment configuration or environments. Releases have been version tags (`priorauth-api` v1.1.0, `priorauth-web` v1.0.0).

A. No deployed environments yet. A release is the PR to `main` plus a version tag; the demo runs locally from `main`, and Dana Ortiz accepts after it.
B. Deploy to a staging environment on every merge to `main`; production needs tech lead and product owner sign-off (please name the environments under Other)
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q9. Who sets the version and the tag for F1220, and when?

`priorauth-api` is still `1.1.0` in `pom.xml` after F1210. Your rules say to check a repo's existing tags and build file before proposing a version.

A. Meena Iyer bumps the version in each build file and tags each repo when the feature branch merges to `main` (a minor version for a new feature)
B. Each story owner bumps the version in their story's PR
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q10. How is code style kept?

Neither repo has a formatter or linter. The developer listed the conventions the code actually follows, per repo, in `contributions/aidlc-developer-agent.md`. Examples: API layer boundaries, Java records, constructor injection, 4-space indent; screen named exports, 2-space indent, double quotes; tests tagged with the FR/US they prove. The security engineer notes that a linter is also the only realistic way to get automated security checks here.

A. Convention and review: adopt the developer's list as the written standard, with no formatter or linter this feature
B. Add a formatter and/or linter, named in a plan, and fail the verify run on it
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q11. How are security checks done?

Neither repo has any security scanning. F1220 brings the first input from callers that the API keeps and the screen displays: reviewer ids, tenants and history. That raises three risks: hostile text shown on the page, unlimited memory use, and caller values reaching file paths.

A. The mob checks a short secure-coding list at each story's code-plan review, with no new tool:
  - validate and size-limit every request value
  - escape API data before showing it on the page
  - never build a file path or cache key from a caller's value
  - no stack traces or raw input in error responses
  - allow only named origins for browser calls (CORS)
B. Option A, plus add a dependency or code scanner, named in a plan
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q12. Which of these become recorded rules? (select all that apply)

Each is already written in your workspace instructions, or corrects a draft rule.

A. ALWAYS give new branching, parsing, money or security logic a test
B. ALWAYS fix a bug once, at its root, after finding every caller, in every repo
C. ALWAYS end each code summary with what was skipped or not checked, and any risk
D. Narrow the draft rule "NEVER push or open a pull request from AI-DLC" to code-repo branches and PRs. Pushing the `aidlc/` record after every gate stays allowed.
E. None of these
X. Other (please specify)

[Answer]: A, B, C, D.

## Q13. The coverage answer conflicts with the organisation's rule. Which way? (follow-up to Q5)

The two statements side by side:

- **Q5, your answer:** "No coverage tooling in F1220: the 80% floor stays a target, and a later feature adds JaCoCo and Node coverage with CI."
- **Organisation rule** (`memory/org.md`, Testing Posture): the `feature` workflow adds "an 80% line-coverage floor and CI execution before merge". Build and Test "verifies defined coverage floors … they may not be weakened to make a step pass".

Team practices may add to the organisation's rules but not contradict them. As answered, Build and Test would have no way to verify the floor.

A. Keep Q5 for F1220 as a recorded exception. Build and Test reports coverage as not measured, without claiming the floor is met, and the later feature that adds the tooling closes the gap. Meena Iyer owns that exception.
B. Add the coverage tooling in F1220 after all: JaCoCo in US5160's plan, Node coverage in US5161's plan (Q5 option A)
C. Change the organisation rule in `memory/org.md` first; whoever owns it does that outside this workflow
X. Other (please specify)

[Answer]: A.

## Q14. The branching answers conflict with the organisation's rule. Which way? (follow-up to Q1 and Q2)

The two statements side by side:

- **Q1 and Q2, your answers:** `feature/F1220` lives until the 2027.Q1 R1 release, with story PRs into it and AI-DLC working on top of it; PRs merge with merge commits.
- **Organisation rule** (`memory/org.md`, Way of Working): trunk-based development, branches that live 1-2 days and merge to `main`, AI-DLC work based on and merged to `main`, and each story squash-merged into one commit.

A. Keep Q1 and Q2 for this team and record them as the team's practice. If recording refuses them as a contradiction, the organisation rule in `memory/org.md` has to change first.
B. Change the organisation rule in `memory/org.md` first, to allow a per-feature branch and merge commits, then record the team practice
C. Follow the organisation rule: story branches merge straight to `main`, squashed
X. Other (please specify)

[Answer]: A.

## Consolidated Summary Confirmation

- Way of working: `feature/F1220` in each repo, cut from current `main`; story PRs into it, one PR to `main` after Build and Test; AI-DLC story work based on and merged to `feature/F1220`; it lives until 2027.Q1 R1. Merge commits for every PR, as for F1210. Recorded as the team's practice despite the organisation default (Q1, Q2, Q14)
- No thin end-to-end slice first: stories built in parallel against the agreed contract, proven together at the feature's Build and Test (Q3)
- Tests after each layer; a bug fix still starts with a failing test (Q4)
- Coverage: no coverage tooling in F1220; the 80% floor stays a target and Build and Test reports coverage as not measured, as a recorded exception owned by Meena Iyer; a later feature adds JaCoCo, Node coverage and CI; each story still tests every new branch (Q5, Q13)
- CI stand-in: the story owner runs the verify script with the repos named before every PR and pastes the result into the PR; real CI is separate work (Q6)
- Testing practices: record baselines with repos named before any change; API tests independent (own reviewer id or store reset); test-controlled clock; screen logic in `src/` modules, `index.html` only calls them (Q7)
- Release: no deployed environments; release = PR to `main` + version tag; demo runs locally from `main`, Dana Ortiz accepts after it (Q8)
- Versioning: Meena Iyer bumps the version in each build file and tags each repo when the feature branch merges to `main`, minor version for a feature (Q9)
- Code style: convention and review, using the developer's per-repo list as the written standard; no formatter or linter this feature (Q10)
- Security: the mob checks a short secure-coding list at each story's code-plan review (validate and size-limit inputs, escape API data on the page, no caller values in file paths or cache keys, no stack traces or raw input in errors, named origins only for CORS); no new tool (Q11)
- Recorded rules added: tests for new branching/parsing/money/security logic; fix a bug once at its root in every repo; end each code summary with what was skipped and any risk; "never push or open a PR" narrowed to code-repo branches and PRs (Q12)

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
