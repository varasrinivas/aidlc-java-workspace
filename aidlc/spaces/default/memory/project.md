# Project-Level Rules

> Project-specific specialisation and corrections. Loaded after `org.md` and
> `team.md` as strict-additive guidance; contradictions with broader policy
> are rejected. Populated by practices-discovery and the self-learning loop.
>
> Use sparingly: most teams don't need a project layer. Reach for it
> only when this specific project needs stable, durable guidance beyond the
> team practice (for example, package-specific release checks or an additional
> regression suite for a legacy component).

## Way of Working

<!-- Project-specific specialisation. Example: -->
<!-- This monorepo requires package-scoped branch names and a package owner -->
<!-- review in addition to the team's normal merge policy. -->

## Walking Skeleton

<!-- Project-specific specialisation. Example: -->
<!-- The walking skeleton must exercise the legacy service adapter as well -->
<!-- as the new service boundary. -->

## Testing Posture

<!-- Project-specific specialisation. -->

## Guard Policy

<!-- Project-specific. Mode: strict, relaxed, or off. Strict here holds for every intent, whatever one person asks in chat; relaxed or off here applies to every intent whose policy came from its scope, unless the person sets another; changing this line changes it. A section under the retired Change Control heading, written by an earlier release, is still read. -->

## Deployment

<!-- Project-specific specialisation. -->

## Code Style

<!-- Project-specific specialisation. -->

## Tech Stack

<!-- Technology choices locked for this project. -->

## Decided

<!-- Decisions made in earlier stages that should not be re-asked. -->
<!-- Format: DECIDED: [decision] (Stage [slug], [date]) -->

## Scope Overrides

<!-- Custom scope rules for this project. -->

## Forbidden

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: NEVER [behavior] (affirmed [date]) -->
<!-- Example: NEVER throw exceptions across service layer boundaries (affirmed 2026-05-17) -->

- NEVER start a branch from another person's branch. (affirmed 2026-11-02)

- NEVER cut a story branch before the stories it depends on are merged into the feature branch, unless it needs only an agreed contract. (affirmed 2026-11-02)

- NEVER change another intent's folder. (affirmed 2026-11-02)

- NEVER edit `memory/` or `codekb/` by hand; they change only through gates. (affirmed 2026-11-02)

- NEVER push a code-repo branch or open a pull request from AI-DLC; the story owner does that. Committing and pushing the `aidlc/` record after every gate stays allowed. (affirmed 2026-11-02)

- NEVER cut validation at trust boundaries, error handling that prevents data loss, security, accessibility, or anything the request asked for. (affirmed 2026-11-02)

## Mandated

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: ALWAYS [behavior] (affirmed [date]) -->
<!-- Example: ALWAYS use Result<T,E> for fallible operations in service layer (affirmed 2026-05-17) -->

- ALWAYS run tests through the workspace verify script (`scripts/verify.sh`, or `scripts\verify.cmd` on Windows) and run it before saying a change is done. (affirmed 2026-11-02)

- ALWAYS name a new dependency in the unit's plan before adding it. (affirmed 2026-11-02)

- ALWAYS start a branch from its PR base, freshly pulled; for a story of a multi-story feature, the PR base is `origin/feature/F<id>`. (affirmed 2026-11-02)

- ALWAYS name branches `f<id>/us<id>-<word>` for a story of a multi-story Rally feature, `<intent label>/<unit slug>` for a single-intent feature, `fix/<intent label>` for a bug fix and `hotfix/<intent label>` (cut from the release tag) for a production fix, using the same name in every repo the work touches. (affirmed 2026-11-02)

- ALWAYS open one PR per repo for a change across repos, each PR naming the others. (affirmed 2026-11-02)

- ALWAYS start a bug fix with a failing test. (affirmed 2026-11-02)

- ALWAYS give new branching, parsing, money or security logic a test. (affirmed 2026-11-02)

- ALWAYS fix a bug once, at its root, after finding every caller, in every repo. (affirmed 2026-11-02)

- ALWAYS end each code summary with what was skipped or not checked, and any risk. (affirmed 2026-11-02)

- ALWAYS check the repo's existing tags and its build file before proposing a version or a tag. (affirmed 2026-11-02)

- ALWAYS fetch and rebase a story branch onto `origin/feature/F<id>` before opening its PR, keep both stories' changes on a conflict, and re-run the verify script before pushing with `--force-with-lease`. (affirmed 2026-11-02)

## Corrections

<!-- Project-specific corrections from human feedback. -->
<!-- Format: NEVER/ALWAYS [behavior] (learned [date]) -->
