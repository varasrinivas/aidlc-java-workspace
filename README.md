# acme-workspace: one Rally feature, four developers (Java edition)

The starting workspace of the AI-DLC course's guide **One Rally feature, four developers**:
https://learnings.varasrinivas.com/ai-dlc-execution/aidlc-rally-team-of-four.html

Rally feature F1210 has four linked stories, each owned by a different developer: US5150 (shared filter code),
US5151 and US5152 (two filters on top of it) in `priorauth-api`, US5153 (the screen) in `priorauth-web`.
This branch has the team's files with the two repos, the Rally export and the team rules for many developers.

| Repo | Start from | Answer key |
|---|---|---|
| this workspace, branch `rally-team` | the branch | tag `rally-team-answer`: the record with the parent and four child intents |
| [`aidlc-priorauth-api`](https://github.com/varasrinivas/aidlc-priorauth-api) | tag `v1.1.0` (cut `feature/F1210` from it) | tag `f1210-answer` |
| [`aidlc-priorauth-web`](https://github.com/varasrinivas/aidlc-priorauth-web) | `main` (`v1.0.0`) | tag `f1210-answer` |

## Start

1. Fork the three repos (the workspace with all branches: untick "copy the main branch only").
2. The tech lead, once:
   ```
   git clone -b rally-team https://github.com/<you>/aidlc-java-workspace.git acme-workspace
   cd acme-workspace
   ./scripts/use-forks.sh <you>          # Windows: .\scripts\use-forks.ps1 <you>
   aidlc config --harness claude
   aidlc system workspace-sync
   git add -A && git commit -m "acme-workspace: our forks and the AI-DLC harness" && git push
   ```
3. Each developer clones the workspace fork, sets `git config user.name`, runs `aidlc system workspace-sync`.
   Alone? Make five clones in five folders (meena, kiran, arjun, tara, divya), one per person.
4. Follow the guide from its step 7. The feature branch comes from the tag:
   `git -C priorauth-api switch -c feature/F1210 v1.1.0`.

Tests, in every repo: `./scripts/verify.sh priorauth-api priorauth-web` (Windows: `scripts\verify.cmd ...`).
