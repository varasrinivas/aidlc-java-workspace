**Collaborator:** aidlc-devsecops-agent

## Contribution

Security engineer review of the lead draft, covering lint and format rules, SAST and DAST, secret and dependency scanning, supply-chain controls, and input validation at trust boundaries as a team practice. Evidence read: both repos' `pom.xml`, `package.json` and `.gitignore`, the workspace `.gitignore`, `scripts/verify.sh`, `priorauth-api/src/main/resources/application.yml`, `PendingRequestsController.java`, `HolidayCalendar.java`, `priorauth-web/src/render.js` and `index.html`, the codekb files (`dependencies.md`, `technology-stack.md`, `code-quality-assessment.md`, `api-documentation.md`) for both repos, `scope-document.md`, and the workspace `CLAUDE.md`.

### 1. What the evidence establishes (security tooling baseline)

I confirm the lead's "none found" for CI, lint and coverage, and add the security-specific facts the draft does not record:

| Control | `priorauth-api` | `priorauth-web` | Evidence |
|---|---|---|---|
| SAST (SpotBugs/FindSecBugs, Semgrep, CodeQL, Sonar, ESLint security plugins) | none | none | `pom.xml` has only `spring-boot-maven-plugin`; `package.json` has only `"test": "node --test"` |
| DAST | none; no environment to run it against | n/a (static files) | no deploy config, local bare remotes (`repos.json`) |
| Secret scanning (pre-commit or CI) | none | none | no `.pre-commit-config.yaml`, `.gitleaks.toml` or hook config; no hosted platform, so no GitHub secret scanning either |
| Dependency vulnerability scanning | none | not needed today: zero dependencies, no lockfile | codekb `dependencies.md` for both repos |
| Dependency version control | every version comes from one place, the Spring Boot parent BOM `4.1.1`; no explicit versions | no `dependencies` or `devDependencies` | `pom.xml:8-13`; `package.json` |
| Build tool pinning | Maven not pinned (no wrapper); Java pinned at 21 | Node `>=20` (floor only); npm not pinned | codekb `technology-stack.md` |
| Secrets in code or config | none found | none found | codekb `code-quality-assessment.md` (both); `application.yml` holds only port and threshold |
| `.gitignore` coverage of secret-bearing files | `target/`, IDE files only; no `.env`, `*.pem`, `*.key`, `application-local.*` | `node_modules/` only | both `.gitignore` files |
| Input validation at the HTTP boundary | type binding only (`@DateTimeFormat` on `asOf`; `RequestFilter` by model-attribute binding); no Bean Validation starter on the classpath | n/a | `PendingRequestsController.java:33-35`; codekb `api-documentation.md` |
| Output encoding | n/a (JSON via Jackson) | one helper, `esc`, escapes `& < > "` but not `'`; rows go into `innerHTML`; untested | `render.js:3`, `index.html:26`; codekb web TD-7 |
| CORS | no CORS configuration found anywhere in `src/` (grep for `cors`, `CrossOrigin`, `allowedOrigins`: no match), although the web README says the API must allow the page's origin | browser calls the API cross-origin | `priorauth-web/README.md:14` |
| Error detail | Spring Boot defaults (`server.error.include-message` and `include-stacktrace` not overridden) | non-2xx throws, not shown to the user | `application.yml` |

Net: the team's real supply-chain and secure-coding controls today are (a) a very small dependency surface (one compile starter in the API, zero packages in the web repo), (b) one version source (the Boot BOM), (c) the workspace rule "name a new dependency in the plan", and (d) review. No automated security check runs anywhere, and there is no hosted platform on which one could run. That is a fact the team should affirm or change on purpose, not inherit by silence.

### 2. Why this matters more for F1220 than for F1210

F1210 only read server-owned data from a classpath file. F1220 adds the first write endpoints (`PUT /reviewers/{reviewerId}/filter`) and the first data that flows from one user's browser, through the API, into another user's screen (the history: who, when, what). That changes the trust picture in four ways the practices should anticipate:

1. **Stored XSS becomes possible.** `reviewerId` and `tenant` will be caller-chosen strings that the history view renders. Today `esc` is the only barrier, it does not escape `'`, and it has no test with hostile input (web TD-7, rated Medium in codekb). With user-supplied values reaching `innerHTML`, I rate it High for F1220.
2. **Unbounded in-memory growth from unauthenticated input.** The store is in memory and there is no sign-in, so any caller can create unlimited reviewers and unlimited history entries until the JVM runs out of heap. A durable store is out of scope, but size limits are not.
3. **The accepted risk covers reading, not writing.** `scope-document.md` accepts that "anyone using the screen can read" a reviewer's history. It does not record that anyone can also overwrite another reviewer's saved filter, or write history entries in another reviewer's name, which is what an untrusted `reviewerId` allows (codekb web `api-documentation.md`, Security and Identity). That is a requirements question, not a practice, but it should not be lost: I recommend the lead flag it for Requirements Analysis so the team either accepts it explicitly (and Meena's release-notes line covers it) or narrows it.
4. **Log and audit integrity.** If the history or application logs record `reviewerId` or `tenant` verbatim, CR/LF in those values can forge log lines. The audit trail is the feature's whole value for nurse managers.

A reuse hazard to note for the code plans: `HolidayCalendar.forTenant(tenantId)` builds a classpath path from its argument (`"data/holidays-" + tenantId + "-2026.json"`) and caches every key it sees in an unbounded `ConcurrentHashMap` (`HolidayCalendar.java:31,35`). It is safe today only because the argument comes from the server's own data. F1220 code must not pass a caller-supplied tenant to it (for example to check that a tenant exists, TD-1).

### 3. Proposed additions to the practices (for the interview, not facts yet)

I suggest these as candidate lines. Items marked **rule** are worded for `discovered-rules.md` if the team affirms them; the others belong in `team-practices.md`. None adds a dependency unless it says so, and every one that does is offered as an option with its cost.

**Input validation at trust boundaries (Code Style or a new security line under Way of Working)**

- **rule** ALWAYS validate every value that enters the API from a request (path variable, query parameter, body field) for type, length, character set and allowed values before it is stored, used to build a path or key, logged, or echoed back; reject anything else with a 400 that does not repeat the raw input.
- **rule** ALWAYS bind request bodies to a dedicated record that holds only the fields the endpoint accepts; never bind into a domain or store object.
- **rule** ALWAYS put an upper bound on anything an unauthenticated caller can make the API keep in memory (number of entries per key, length of each value); the bound is stated in the unit's plan and has a test.
- **rule** NEVER use a caller-supplied value to build a file path, classpath resource name or cache key without first checking it against an allowlist.
- Without the `spring-boot-starter-validation` starter (not on the classpath; adding it is a new dependency to name in a plan), validation is written by hand, for example in the request record's compact constructor, and tested. The team picks one way for F1220 and uses it in every new endpoint.

**Output encoding (web)**

- **rule** ALWAYS escape every API-supplied value before it reaches `innerHTML`, through the one shared helper, or set it with `textContent`; NEVER insert API data into HTML unescaped.
- The shared escape helper covers `& < > " '` and has a test with hostile input (`<script>`, `"`, `'`, `&`). Fixing `esc` belongs in whichever F1220 story first renders a caller-supplied value (the history view, US5163, or the restored filter, US5161), named in that story's plan, not as an unrelated fix.

**Secrets**

- Already covered by `memory/phases/construction.md` ("never hardcode credentials ... use environment variables"); I would not duplicate it as a team rule.
- Option for the interview: extend both repos' `.gitignore` with `.env`, `*.pem`, `*.key`, `application-local.*`. No dependency; a one-line change, but only inside a plan that names it.
- Option for the interview: a secret scanner (Gitleaks) as a developer-machine pre-commit hook. It is a tool on each laptop, not a project dependency, but it is still a new tool the team must agree to. With no hosted platform there is no server-side backstop.

**Dependencies and supply chain**

- **rule** (extends the existing "name a new dependency in the plan") ALWAYS state, when a plan adds a dependency or plugin, why it is needed, its version source (the Boot BOM where it manages it; otherwise an exact pinned version) and its licence; and for `priorauth-web`, commit the lockfile it creates and install with `npm ci`.
- Keep `priorauth-web` dependency-free unless a plan justifies a package. Zero dependencies is the strongest supply-chain control this team has; it should be stated as a practice, not left as an accident.
- Keep every API dependency version under the Spring Boot parent BOM; NEVER override a BOM-managed version in `pom.xml` without a reason in the plan (an override silently stops Boot upgrades from patching it).
- Dependency vulnerability check: with no CI, the practical options are (a) a manual check of the Boot parent version against Spring's security advisories before each release tag (no tooling; owner named), or (b) the OWASP Dependency-Check Maven plugin run on demand (a new plugin; needs NVD data access and is slow, so not suitable for `verify.sh`). I recommend (a) for F1220 and an owner, with (b) left to a later decision when CI exists.
- Maven is unpinned (no wrapper). Adding the Maven wrapper is a supply-chain improvement (reproducible builds) but adds checked-in scripts and a download; offer it, do not assume it.

**Lint, format and SAST**

- The lead frames T6 as a style question only. Any linter choice is also the team's only realistic SAST: SpotBugs with the FindSecBugs plugin for the API, ESLint with `eslint-plugin-no-unsanitized` (flags `innerHTML` sinks) for the web repo. Each is a new build plugin or dev dependency to be named in a plan, and in `priorauth-web` it would end the zero-dependency state and need a lockfile.
- My recommendation for F1220: no new SAST tool in this feature; instead, the mob's 3.5 plan review checks each new endpoint and each new rendering against a short secure-coding checklist (validation and bounds, body record, no caller value in paths or keys, escaped output, no raw input in errors or logs, CORS allowlist). This costs no dependency and fits the team's existing mob gate. Record it as an accepted gap with an owner who revisits SAST when CI exists.

**DAST**

- Not feasible today: no environment exists to scan (T4). Record "no DAST until a shared environment exists" explicitly, so the Operation stages do not assume one.

**CORS (affects US5160/US5161)**

- The new `PUT` with a JSON body triggers a browser preflight; the cross-origin call will not work without CORS configuration, which does not exist in the code. When it is added: an explicit origin allowlist from configuration, methods limited to those the screen uses (`GET`, `PUT`), and no `*`. CORS is not an access control here (there is no auth, any non-browser client can call the API), but a wildcard would let any web page a reviewer visits silently rewrite their saved filter through their browser.

**Errors and logging**

- **rule** NEVER return stack traces or raw caller input in error bodies, and NEVER log `memberId` (patient-linked) or a full request body; log caller-supplied strings only after stripping CR/LF. Keep Spring Boot's defaults for `server.error.include-stacktrace` and `include-message`, and say so in the plan if a new 400 shape (TD-5) changes them.

### 4. Suggested interview questions (security, only what evidence cannot settle)

Add as one question to the lead's list, so the interview stays short:

12. **Security tooling and checks**: With no CI and no hosted platform, which of these does the team adopt for F1220? (A) Validation, bounds and output-encoding rules above, checked by the mob at each 3.5 plan review, with no new tool. (B) A plus `.gitignore` hardening in both repos and a Gitleaks pre-commit hook on each laptop. (C) B plus a security linter (SpotBugs and FindSecBugs; ESLint with `no-unsanitized`) named in a plan. (D) Defer all security tooling until CI exists, with a named owner. X. Other (please specify). Also: who checks the Spring Boot version against security advisories before the release tag?

And one item to hand forward to Requirements Analysis, not to answer here: the scope accepts that anyone can read a reviewer's history; does it also accept that anyone can overwrite a reviewer's saved filter and write history in their name?

### 5. Rating summary

| Finding | Severity for F1220 | Where it is settled |
|---|---|---|
| Caller-supplied values rendered in the history view; `esc` misses `'` and is untested | High | practice now; fix in the first story that renders them |
| Unbounded in-memory growth from unauthenticated writes | High | practice now (bounds rule); limits in Requirements/NFR |
| Write and impersonation not covered by the accepted risk | High | Requirements Analysis |
| No validation framework; hand validation not yet a stated practice | Medium | practice now |
| No SAST, secret or dependency scanning, no CI | Medium | interview Q12 |
| CORS absent; wildcard risk when added | Medium | Contract Design / US5160 plan |
| Log forging via `reviewerId` / `tenant` | Medium | practice now (logging rule) |
| `HolidayCalendar.forTenant` unsafe with caller input | Low (latent) | 3.5 plan review |
| `.gitignore` lacks secret-file patterns | Low | interview Q12 option B |
| Maven unpinned (no wrapper) | Low | optional, later |

## Positions

- AGREE: Discovered rule "NEVER cut validation at trust boundaries, error handling that prevents data loss, security, accessibility, or anything the request asked for" is correctly taken from the workspace `CLAUDE.md`; I propose sharper companion rules in section 3 because F1220 is the first feature with write endpoints.
- AGREE: Discovered rule "ALWAYS name a new dependency in the unit's plan" is the team's main supply-chain control; I propose extending it with version source, licence and lockfile (section 3).
- AGREE: The lead's finding that no linter, CI, coverage or pipeline exists in either repo, and that the remotes are local bare repositories, is accurate; I add that no SAST, secret scanning or dependency scanning exists either, and that no hosted backstop can exist without a platform change.
- AGREE: Keeping hand-written conventions in `team-practices.md` and only written rules in `discovered-rules.md` is the right split; my proposed rules are candidates for the interview, not discovered facts.
- AGREE: Not duplicating "never hardcode credentials" as a team rule; `memory/phases/construction.md` already carries it.
- OBJECT: Tension T6 and open question 11 treat a linter purely as a style choice; for this team a linter is also the only realistic SAST, so the question should name the security option (SpotBugs and FindSecBugs; ESLint `no-unsanitized`) and its dependency cost.
- OBJECT: The evidence and the open questions have no security row; add a security-tooling tension and question 12 (section 4) so the absence of SAST, secret and dependency scanning is affirmed or changed on purpose rather than inherited by silence.
- OBJECT: The draft records codekb web TD-7 nowhere; with caller-supplied `reviewerId` and `tenant` rendered in the history, output encoding should be a stated practice (section 3), and the read-only accepted risk should be handed forward to Requirements Analysis with the write and impersonation question.
