**Collaborator:** aidlc-developer-agent

## Contribution

Scope of this review: naming, layer boundaries, error handling, file organization and code style as they are actually practised in `priorauth-api` and `priorauth-web`. I read every main and test source file in both repos (9 Java main classes, 6 Java test classes, `application.yml`, `pom.xml`; `index.html`, `src/*.js`, `test/*.test.js`, `package.json`), plus the codekb `code-structure.md`, `code-quality-assessment.md` for both repos, the lead draft and the workspace `CLAUDE.md`. I ran nothing and changed nothing.

### 1. Why the observed conventions should be written down in `team.md`

`memory/org.md` `## Code Style` says agents defer to the project's formatter and linter config, and only suggest style where the linter does not already cover it. Neither repo has any such config (confirmed: no `.editorconfig`, Checkstyle, Spotless, PMD, ESLint or Prettier; `pom.xml` has only `spring-boot-maven-plugin`; `package.json` has only `"test": "node --test"`). So unless the interview adds a tool, the written `## Code Style` section in `team.md` is the only style reference Code Generation will have. I recommend the lead turns the two indented bullets in the draft into a fuller, per-repo convention list (items 2 to 5 below), marked as observed practice that the team confirms, not as tool-enforced rules.

### 2. `priorauth-api` (Java 21, Spring Boot 4.1.1, Jackson 3)

**File organization and layer boundaries**
- One Maven module, root package `com.acmehealth.priorauth`. Packages are a mix of layer and feature: `api` (HTTP controller, query record, response record), `model` (domain record), `store` (read-only data access, `@Service`), and `aging` (a feature package holding domain logic: `BusinessDays`, `AgeBadge`, `HolidayCalendar`). Tests mirror the main package tree under `src/test/java`.
- Dependency direction is one-way: `api -> aging, store, model`; `store -> model`; `aging` depends on nothing else in the app. Domain and store classes never import `org.springframework.web` or `org.springframework.http`. HTTP concerns (status codes, `ResponseStatusException`, `@RequestParam`) stay in `api`.
- The response shape is a separate record in `api` (`PendingRequestResponse.from(request, age)`); the domain record `PriorAuthRequest` is never returned directly (so `memberId` is not exposed). This is a real boundary the team keeps.
- Package-private seams are used deliberately: `RequestFilter.matches()` is visible only within `api`.
- Static data lives in `src/main/resources/data/` as JSON, loaded from the classpath.

**Naming**
- Domain language throughout (`pending`, `AgeBadge`, `thresholdDays`, `overLimit`, `receivedAt`). Classes: `<Thing>Controller`, `<Thing>Response`, `<Thing>Store`, `<Thing>Calendar`; records for data.
- Static factories are named `of(...)` (computes, e.g. `AgeBadge.of`) and `from(...)` (maps, e.g. `PendingRequestResponse.from`).
- Configuration keys are kebab-case under the `priorauth.` prefix (`priorauth.aging.threshold-days`) with a default in the `@Value` expression.
- Test classes: for domain code, `<ClassUnderTest>Test`; for HTTP behaviour, either `<Controller>Test` or one class per story behaviour (`TenantFilterTest`, `OverLimitFilterTest`). Test method names are behaviour sentences in camelCase (`asOfBeforeReceivedIsABadRequest`).

**Error handling**
- Domain code signals caller errors with `IllegalArgumentException` (with a message naming the bad values) and unrecoverable I/O with `IllegalStateException` wrapping the cause. No checked exceptions leak out of domain methods; `RequestStore`'s constructor throws `IOException` so a missing or bad export fails the application at start-up (fail fast).
- The controller maps `IllegalArgumentException` to HTTP 400 locally with `ResponseStatusException(HttpStatus.BAD_REQUEST, e.getMessage(), e)`, keeping the cause. There is no `@ControllerAdvice` and no agreed error body (codekb TD-5). Missing optional data has an explicit, documented safe default (a tenant with no holiday file has no holidays).
- A tested convention: a caller error answers 400, not 500 (`asOfBeforeReceivedIsABadRequest`).

**Code style**
- 4-space indent, continuation lines indented 8; imports grouped as app, third-party, then `java.*`, then static imports; no wildcard imports in main code.
- Records for data, `final` utility class with a private constructor for pure functions, constructor injection only (no field injection in main code; tests use `@Autowired` fields), immutable collections (`Stream.toList()`, `Set.copyOf`) and `ConcurrentHashMap.computeIfAbsent` for caches.
- Methods are short (all under 20 lines). Expression-style streams are preferred to loops except in arithmetic (`BusinessDays.between`).
- Jackson 3 packages (`tools.jackson.databind`), not `com.fasterxml.jackson`. Code Generation must not mix the two.
- Comments: a one-line class Javadoc on every main class saying what it is for, usually with the FR/US/intent that introduced it; trailing `// US5151`-style comments on the line a story added; tests carry the same `// FR1.2`, `// US5151` tags on `@Test`. Correction to the draft: not every class names an FR/US (`PriorAuthApiApplication`, `PendingRequestResponse`, `RequestStore` do not), so the convention is "every class has a one-line purpose Javadoc; requirement tags where a requirement introduced it".
- `pom.xml` lists no versions under the Spring Boot parent and puts a one-line comment above each dependency and plugin saying why it is there. A new dependency would follow that pattern (and must be named in a plan, per `CLAUDE.md`).

### 3. `priorauth-web` (JavaScript ES modules, Node >= 20, no dependencies)

**File organization and layer boundaries**
- `index.html` holds markup, inline CSS and an inline `<script type="module">` that is the only DOM-touching code. Everything in `src/` is DOM-free and therefore testable under `node --test`: pure URL builders (`pendingUrl`, `filteredUrl`), network calls with an injected `fetchFn = fetch` as the last parameter (`fetchPending`, `loadQueue`), and pure string rendering (`countLabel`, `renderRows`).
- One test file per `src/` module: `test/<module>.test.js`. No build step, no bundler; imports use relative paths with the `.js` extension.

**Naming**
- File names kebab-case (`queue-filters.js`); functions camelCase verbs or nouns in domain language (`fetchPending`, `loadQueue`, `countLabel`, `renderRows`). Named exports only; no default exports, no classes.
- Screen-side option names may differ from wire names (`overLimitOnly` on screen vs `overLimit=true` on the wire; codekb TD-3). Optional query parameters are omitted when unset, never sent as `false` or empty.

**Error handling**
- A non-2xx answer throws a plain `Error` whose message names the service and status (`priorauth-api answered 503`). No custom error types.
- The page never catches: a failed fetch leaves an empty table and an unhandled rejection (codekb TD-9). This is the existing gap, not a convention to copy.
- Output escaping is done in one private helper (`esc`) applied to every rendered cell; it does not escape `'` and is untested (codekb TD-7). Any new rendered field must go through it.

**Code style**
- 2-space indent, double quotes (single quotes only to wrap a string containing double quotes), semicolons, template literals, arrow functions for small callbacks, default parameters for options (`{ asOf } = {}`).
- Line 1 of every `src/` file is a one-line purpose comment; story-introduced files name the story and the contract (`// US5153 ... Built against the contract ...`). No JSDoc.
- Tests use `node:test` `test()` and `node:assert/strict`; test names are behaviour sentences, with the story tag in the name where a story introduced it (`"the controls become the API's filters (US5153)"`). Network stubs are inline objects `{ ok, status, json }`.

### 4. Cross-repo conventions

- The requirement / story ID is the traceability thread in both repos: in class Javadoc or file-header comments, on the changed line, and on the test that proves it. I suggest the team affirms this explicitly ("tag code and tests with the FR/US they implement"), because it is consistent across both repos and both prior intents and Code Generation will otherwise not do it reliably.
- Duplication already flagged by reverse engineering is relevant to F1220: the fetch-and-throw block exists twice in the web repo (`api.js:10-14`, `queue-filters.js:12-17`, TD-2), and three MockMvc test classes repeat the same set-up in the API. The workspace rule "prefer what already exists" and "no abstractions nobody asked for" pull in opposite directions here; a new client call in F1220 would be the third copy. This is a design decision for the story plans, not a practice to settle now, but the lead may want to note it as an open item.
- No conventions exist yet for: a shared HTTP error body in the API (TD-5), an injectable `Clock` (TD-4, `LocalDate.now()` in the controller), or user-visible error messages on the page (TD-9). F1220 adds new 400 answers, UTC timestamps and a second page-load call, so it will create the first instance of each. Code Style should not invent them; I recommend the interview or Application Design names who decides them, so Code Generation follows one choice in both stories.

### 5. Suggested interview question for Code Style (to add to the lead's question 11)

Beyond "tool or convention", ask whether the team confirms the observed conventions above as the written standard for new code (a yes/no with "edit" as an option), because without a linter that list is what reviewers and Code Generation will check against.

### 6. Discovered rules: wording and gaps

- The draft's `NEVER push or open a pull request from AI-DLC` is broader than the source. `CLAUDE.md` says pushing and opening the PR for code are the people's ("Commit the code on the unit's branch as the plan's last step; pushing and opening the PR are ours"), but it also says the record goes to the workspace's `main` with `git pull --rebase` then push, and "After every gate: commit `aidlc/` and push". As worded, the rule would forbid the record push the team does after every gate. Suggested wording: `NEVER push a code repo branch or open a pull request from AI-DLC; the story owner does that.`
- Two further hard constraints are stated in `CLAUDE.md` and are not in the draft. The lead may add them if the interview confirms them as hard rules: `ALWAYS fix a bug at its root, once, after finding every caller in every repo.` and `ALWAYS end a code summary with what was skipped or not checked, and any risk.`
- `NEVER change another intent's folder, and never edit memory/ or codekb/ by hand.` joins two rules in one line with a lower-case second `never`. Splitting it into two `NEVER` lines would keep each rule checkable on its own.

## Positions

- AGREE: Code Style, "no formatter or linter is configured; style is consistent by hand" - confirmed by reading every source file and both build manifests.
- AGREE: The per-repo style bullets (4-space Java, records, constructor injection, short methods; 2-space JS, double quotes, semicolons, named exports, purpose comment on line 1) - all observed, with the one correction below.
- OBJECT: "class-level Javadoc naming the FR/US" for `priorauth-api` - three main classes have a purpose Javadoc without an FR/US; the convention is a purpose Javadoc on every class, with requirement tags where a requirement introduced the code.
- OBJECT: Code Style is too thin for a repo pair with no linter - it should carry the observed layer boundaries, naming, error-handling and traceability conventions (sections 2 to 4 above), since `team.md` is the only style reference Code Generation will have.
- OBJECT: `NEVER push or open a pull request from AI-DLC` - contradicts the workspace's own "after every gate: commit `aidlc/` and push"; scope it to code repo branches and PRs.
- AGREE: Code Style's open question about adding a formatter or linter as a planned new dependency, and whether CI fails on it - matches `CLAUDE.md` "never add a dependency inside a unit without saying so in the plan".
- AGREE: Every other line in `discovered-rules.md` traces to `CLAUDE.md` as stated.
- AGREE: Way of Working, Walking Skeleton, Testing Posture and Deployment drafts - outside my focus; I found nothing in the code that contradicts them.
