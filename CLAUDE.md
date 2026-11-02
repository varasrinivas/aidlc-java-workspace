# acme-workspace

Run AI-DLC from this folder. It holds the two code repos of the course's four-developer guide (your forks of the sample repos), each cloned beside the record by
`aidlc system workspace-sync` from `repos.json`, each with its own git, origin and pull requests.
AI-DLC's own instructions live in `.claude/` and what it learns in `aidlc/spaces/default/memory/`; don't repeat them here.

| Repo                  | Owns                                              | Stack              | Team         | PR base |
|-----------------------|---------------------------------------------------|--------------------|--------------|---------|
| priorauth-api         | the API the reviewer screen reads                 | Python 3.12, uv    | priorauth    | main    |
| priorauth-web         | the reviewer screen                               | JavaScript, Node   | priorauth    | main    |

## How we run AI-DLC here

Rules: the record in `aidlc/` is the source of truth for requirements and decisions; commit it after every gate.
One unit = one branch = one PR. Tests through `./scripts/verify.sh` (`scripts\verify.cmd` on Windows), never ad hoc.
Never add a dependency inside a unit without saying so in the plan.

- Each person works in their own clone of this workspace. One piece of work = one intent; start it with `--repos` naming only the repos it changes.
- Branch names, the same in every repo the work touches: `<intent label>/<unit slug>` for a feature (`request-filters/u1-filter-api`), `fix/<intent label>` for a bug fix, `hotfix/<intent label>` from the release tag for a production fix.
- Start every branch from the repo's PR base, freshly pulled (`scripts/pull-all.sh`, `scripts\pull-all.ps1` on Windows). Never start one from another person's branch.
- Commit the code on the unit's branch as the plan's last step; pushing and opening the PR are ours. A change across repos is one PR per repo, each naming the others.
- The record goes to this workspace's main: commit only your intent's folder, `git pull --rebase`, then push. If `intents.json` conflicts, keep every row from both sides.
- Never change another intent's folder, and never edit `memory/` or `codekb/` by hand: they change through gates.
- Record `scripts/verify.sh` as the verification command (the engine runs it under cmd.exe on Windows, so record `scripts\verify.cmd` there). With no arguments it tests every repo whose branch is not its PR base.
- Before proposing a version or a tag, check the repo's existing tags and its build file.
- Requests and bug reports go in `docs-in/`; name the file in the `/aidlc` request.

## How to change code

1. Ask, don't assume. If something is unclear, put it in the stage's questions; state the assumptions you make.
2. Smallest complete change. Prefer what already exists (this codebase, the platform libraries, an installed dependency) over new code; no features, options or abstractions nobody asked for. Deleting beats adding.
3. Surgical. Touch only the repos and files the approved plan names and match the surrounding style. Mention unrelated problems, don't fix them. Fix a bug once, at its root, after finding every caller, in every repo.
4. Prove it. A bug fix starts with a failing test; new branching, parsing, money or security logic gets a test; run the verify script before saying done.
5. Never cut validation at trust boundaries, error handling that prevents data loss, security, accessibility, or anything the request asked for.
6. End each code summary with what you skipped or did not check, and any risk.

## Many developers on one Rally feature

- One Rally story = one AI-DLC unit = one intent = one branch = one PR, driven only by the story's Rally owner.
- The feature has a parent intent (`feature` scope, label `f<id>-<word>`), driven only by the tech lead. It holds the stories, the units, the API contracts and the order between stories. Children never change it: raise a change with the tech lead, who updates the parent first.
- Inputs live in one folder per feature: `docs-in/rally/F<id>/` holds the Rally snapshot (`F<id>.json` and its export), refreshed and committed by the tech lead only; `docs-in/rally/F<id>/US<id>/` holds a story's attachments, written by the story's owner only; specs go in `docs-in/specs/F<id>/`. Never write into another story's intent folder or attachments.
- The parent's gates from 2.3 to 2.9 are answered as a mob: the whole team in one session, one person typing. Write the room's decision with the names of who decided ("Approve - Dana Ortiz, Meena Iyer; the team agreed"), and the dissent if there was any.
- Each story's code plan (3.5) is reviewed by the mob before code is written: plan approval on in every child (`aidlc engine config set guard.plan-approval on`).
- Each story gets a child intent: `aidlc engine intent create --scope express --label f<id>-us<id> --repos <only the story's repos>`, with `--arguments` naming the story and the parent's `unit-of-work.md`. Don't re-ask what the parent approved.
- Branches: the tech lead creates `feature/F<id>` in every code repo the feature changes. Story branches are `f<id>/us<id>-<word>`, cut from `origin/feature/F<id>`; their PRs go into the feature branch. One PR from the feature branch to `main` after the parent's Build and Test.
- Don't cut a story branch before the stories it depends on are merged into the feature branch (the parent's Delivery Planning lists them). A story that needs only an agreed contract can start at once.
- Before you create an intent or a branch: pull. After every gate: commit `aidlc/` and push. If `intents.json` conflicts, keep every row from both sides.
- Before a PR: `git fetch` and rebase the story branch onto `origin/feature/F<id>`. On a conflict keep both stories' changes, run `scripts/verify.sh` (`scripts\verify.cmd`), then `git push --force-with-lease`.
- Rally: the owner moves the story to In-Progress when the child intent is created and to Completed when its PR is merged into the feature branch, and pastes the PR link and the intent id into the story's Discussion. The product owner accepts after the feature demo.
