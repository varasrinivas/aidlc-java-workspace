# Discovered Rules

> Only hard constraints people have stated. Sources: the workspace's checked-in `CLAUDE.md` and the practices interview (Q12). Conventions and review practices, including the security checklist, are in `team-practices.md`, not here.

## Mandated

- ALWAYS run tests through the workspace verify script (`scripts/verify.sh`, or `scripts\verify.cmd` on Windows) and run it before saying a change is done.
- ALWAYS name a new dependency in the unit's plan before adding it.
- ALWAYS start a branch from its PR base, freshly pulled; for a story of a multi-story feature, the PR base is `origin/feature/F<id>`.
- ALWAYS name branches `f<id>/us<id>-<word>` for a story of a multi-story Rally feature, `<intent label>/<unit slug>` for a single-intent feature, `fix/<intent label>` for a bug fix and `hotfix/<intent label>` (cut from the release tag) for a production fix, using the same name in every repo the work touches.
- ALWAYS open one PR per repo for a change across repos, each PR naming the others.
- ALWAYS start a bug fix with a failing test.
- ALWAYS give new branching, parsing, money or security logic a test.
- ALWAYS fix a bug once, at its root, after finding every caller, in every repo.
- ALWAYS end each code summary with what was skipped or not checked, and any risk.
- ALWAYS check the repo's existing tags and its build file before proposing a version or a tag.
- ALWAYS fetch and rebase a story branch onto `origin/feature/F<id>` before opening its PR, keep both stories' changes on a conflict, and re-run the verify script before pushing with `--force-with-lease`.

## Forbidden

- NEVER start a branch from another person's branch.
- NEVER cut a story branch before the stories it depends on are merged into the feature branch, unless it needs only an agreed contract.
- NEVER change another intent's folder.
- NEVER edit `memory/` or `codekb/` by hand; they change only through gates.
- NEVER push a code-repo branch or open a pull request from AI-DLC; the story owner does that. Committing and pushing the `aidlc/` record after every gate stays allowed.
- NEVER cut validation at trust boundaries, error handling that prevents data loss, security, accessibility, or anything the request asked for.
