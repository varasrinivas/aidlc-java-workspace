# java-workspace

Run AI-DLC from this folder. One code repo, `priorauth-api/`, a Spring Boot 4.1 REST API on Java 21, built with Maven.

| Repo          | Owns                                   | Verify with      | Branch pattern       |
|---------------|----------------------------------------|------------------|----------------------|
| priorauth-api | the API the reviewer screen reads      | `mvn -q test`    | request-age/<slug>   |

Rules: the record in `aidlc/` is the source of truth for requirements and decisions; commit it after every gate.
One unit = one branch = one PR. Tests through `./scripts/verify.sh` (`scripts\verify.cmd` on Windows), never ad hoc.
Never add a dependency to pom.xml inside a unit without saying so in the plan.

## Inputs from Rally and SharePoint
Features come from Rally as snapshots in docs-in/rally/ (scripts/export-rally.py); Rally is the source of truth for stories.
Cite the story ID (US5120…) next to every requirement, plan row and test; never invent a story.
Product specs come from SharePoint, converted to Markdown and onboarded under aidlc/spaces/default/knowledge/.
When a spec and a story disagree, ask at the gate; never pick one silently.
Refresh both snapshots before /aidlc, and commit them with the record.
