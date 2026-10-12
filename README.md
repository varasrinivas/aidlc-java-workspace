# aidlc-java-workspace

The AI-DLC workspace for the course **AWS AI-DLC, Step by Step**
([agenticai.varasrinivas.com/courses/ai-dlc-execution](https://agenticai.varasrinivas.com/courses/ai-dlc-execution/)).
AI-DLC runs from this folder; the code lives in its own repo,
[aidlc-priorauth-api](https://github.com/varasrinivas/aidlc-priorauth-api), which `repos.json` pulls in.

| Branch | Start here to | State |
|---|---|---|
| `main` | run the hello-world feature (request age), step by step | the team's files only: `CLAUDE.md`, `repos.json`, `scripts/` |
| `rally-feature` | run the next feature from a Rally feature and a SharePoint spec | the hello-world run finished, plus the Rally export and the spec onboarded |

## Start the Rally feature

```
git clone -b rally-feature https://github.com/varasrinivas/aidlc-java-workspace.git java-workspace
cd java-workspace
aidlc config --harness claude
aidlc system workspace-sync
git -C priorauth-api switch -c request-filters v1.1.0
claude
```

Then follow the guide: [AI-DLC from a Rally feature](https://agenticai.varasrinivas.com/courses/ai-dlc-execution/aidlc-hello-world-java/aidlc-rally-sharepoint.html).

Needs JDK 21, Maven 3.9, AI-DLC Workflows 2.11 (`aidlc`) and Claude Code. The people, the Rally IDs and the
SharePoint library are part of the course's story; the code, the tests and the `aidlc` output are real.
