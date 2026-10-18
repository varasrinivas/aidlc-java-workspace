# java-workspace

Run AI-DLC from this folder. One code repo, `priorauth-api/`, a Spring Boot 4.1 REST API on Java 21, built with Maven.
AI-DLC's own instructions live in `.claude/` and what it learns in `aidlc/spaces/default/memory/`; don't repeat them here.

| Repo          | Owns                                   | Verify with      | Branch pattern       | PR base |
|---------------|----------------------------------------|------------------|----------------------|---------|
| priorauth-api | the API the reviewer screen reads      | `mvn -q test`    | request-age/<slug>   | main    |

## How we run AI-DLC here

Rules: the record in `aidlc/` is the source of truth for requirements and decisions; commit it after every gate.
One unit = one branch = one PR. Tests through `./scripts/verify.sh` (`scripts\verify.cmd` on Windows), never ad hoc.
Never add a dependency to pom.xml inside a unit without saying so in the plan.

- Commit the code on the unit's branch as the plan's last step; pushing and opening the PR are ours.
- Record the same script as the verification command. The engine runs it under cmd.exe on Windows, so record `scripts\verify.cmd` there.
- If you change a verify script, prove it exits non-zero on a failing test before relying on it.
- Before proposing a version or a tag, check the existing tags and the version in pom.xml.
- Requests and bug reports go in `docs-in/`; name the file in the `/aidlc` request.

## How to change code

1. Ask, don't assume. If something is unclear, put it in the stage's questions; state the assumptions you make.
2. Smallest complete change. Prefer what already exists (this codebase, the JDK, an installed dependency) over new code; no features, options or abstractions nobody asked for. Deleting beats adding.
3. Surgical. Touch only what the approved plan names and match the surrounding style. Mention unrelated problems, don't fix them. Fix a bug once, at its root, after finding every caller.
4. Prove it. A bug fix starts with a failing test; new branching, parsing, money or security logic gets a test; run the verify script before saying done.
5. Never cut validation at trust boundaries, error handling that prevents data loss, security, accessibility, or anything the request asked for.
6. End each code summary with what you skipped or did not check, and any risk.
