**Collaborator:** aidlc-developer-agent

## Contribution

Developer review of `stories.md` (Round 1). I checked whether each story can be built as one PR in its repo, whether the dependencies are right, and what the stories leave out that the code will need. I read the current source of `priorauth-api` (`df871d9`) and `priorauth-web` (`65a999b`), not only the codekb.

### 1. Sizing and the one-PR rule

- **US1.1 (priorauth-api, Rally 3)** fits in one PR. It has more hidden work than the story shows (points 3 to 6). Most of that is in the error body and the strict body parsing, not in the store.
- **US1.2 (priorauth-web, Rally 3)** is the biggest and riskiest story. It needs a new page layout, error display, and one new DOM-free `src/` module holding the open/restore/save sequence (AC1.2.2 to AC1.2.9). The team rule that screen logic lives in tested `src/` modules decides where that code goes: AC1.2.7 and AC1.2.8 can only be tested if they live in one pure module, driven with an injected `fetchFn` and promises the test controls. `index.html` only wires DOM events to it. I agree with keeping it as one story (Q2 A). The code plan (3.5) should still show this module as its own layer, tested before the page wiring, so the mob can see the concurrency logic separately.
- **US1.3 (priorauth-web, Rally 1)** and **US1.4 (priorauth-api, Rally 2)** each fit in one PR.

### 2. Dependencies

- **US1.2 on the contract only: agreed.** All its tests stub `fetchFn`, so Divya can build and test it before US1.1 merges. Add one line: the end-to-end check (the screen against a real API) needs US1.1 merged **and** CORS in place (point 4). Until then the only end-to-end proof is the feature's Build and Test.
- **US1.4 on US1.1 is a code dependency, not only a behaviour one.** NFR2 (atomic save plus history line) means US1.4 adds its history write inside US1.1's save method, in the same store class and the same critical section. Under the Forbidden rule, US1.4's branch cannot be cut until US1.1 is merged into `feature/F1220`. Its INVEST line should say so ("changes US1.1's store; branch cut after US1.1 merges"), so nobody tries to start it on the contract alone. Ask US1.1's code plan to keep one save entry point, with no second write path, so that US1.4 can make the save and the history line atomic without restructuring the store.
- **US1.3 on US1.2: agreed.** It is sequential, after the largest story, so it is on the critical path. That fits its Should priority (it slips first). AC1.3.1 and AC1.3.4 must go through US1.2's save sequencing (FR5.3), not a second save call. Proposed **AC1.3.5:** "Given a save is still in flight, when Rita uses Clear filters, then the stored filter ends as `{"tenant": null, "overLimit": false}`" (FR5.3 applied to FR6.1).

### 3. Hidden work in US1.1: the NM-02 sample row (FR3.2, AC1.1.5, AC1.1.10)

The story calls this "updating row counts". In the code it is larger:

- `RequestStoreTest`: `hasSize(4)`, `get(3)` and the `containsExactly(...)` pending list all change.
- `PendingRequestsControllerTest.listsPendingRequestsOldestFirst`: `$.length()` 3 changes, and so does `$[0]`/`$[1]` if the new row is older than PA-10231 or PA-10244.
- `TenantFilterTest.keepsOnlyTheTenantAskedFor`: today it asserts that `NM-02` returns **0** rows. Adding the row flips this assertion on purpose.
- **Constraint on the new row:** two tests call `?asOf=2026-10-13`, and `BusinessDays.between` throws when the as-of date is before the received date. So a **pending** NM-02 row received after 2026-10-13 would turn `eachRowCarriesItsAgeAndFlag` and `OverLimitFilterTest` into 400s. One received before 2026-10-01 would also change the `asOf=2026-09-30` test. AC1.1.5 should state the row: pending, NM-02, received between 2026-10-02 and 2026-10-13 (for example 2026-10-08, which gives 3 business days at 10-13, not over the limit, because NM-02 has no holiday file).
- **Back-fill rule:** team Testing Posture says every *changed* test file covers the happy path and at least two error or edge cases. Changing `TenantFilterTest` (1 test) and `RequestStoreTest` therefore brings in back-fill work. The natural edge case for `TenantFilterTest` is AC1.1.10's `ZZ-99 -> 200 []`, which replaces the old "NM-02 -> 0" check. AC1.1.10 should name the changed test files, so the API baseline (NFR8, Kiran) can be compared test by test, not only by count.

### 4. Hidden work no story owns: CORS (NFR6)

- `priorauth-api` has **no CORS configuration at all** (codekb api-documentation.md; there is no `CorsConfiguration`, `@CrossOrigin` or `WebMvcConfigurer` in the source).
- The screen's `PUT` with `Content-Type: application/json` triggers a browser preflight (`OPTIONS`), so without CORS the save can never work in a browser.
- The existing `GET /requests/pending` is cross-origin from `npx serve` too. NFR6 says "the new endpoints", but the restored-filter flow also calls `/requests/pending`. The allowed-origin mapping has to cover it, or the screen loads nothing after restore.
- The traceability file marks NFR6 `Deferred -> nfr-design`. Design can choose the origins (OQ4), but the code has to land in a unit, and only an API story can carry it. **Proposal:** US1.1 owns the CORS code, with one AC: "Given the configured origin `http://localhost:3000`, a preflight for `PUT /reviewers/rita.k/filter` from that origin is allowed, and one from `http://evil.example` is not; no response carries `Access-Control-Allow-Origin: *`" (NFR6). Set the traceability target to `US1.1, nfr-design`.

### 5. Hidden work in US1.1: error bodies (AC1.1.8, AC1.1.9)

AC1.1.9 is right. Spring Boot's defaults break it, though, so the story should know this is real work and not a free Contract Design choice:

- The default `/error` JSON includes a `path` field holding the raw request URI. A refused `GET /reviewers/<script>/filter` would echo the caller's reviewer id, which breaks AC1.1.9.
- By default it **omits** the exception message (`server.error.include-message` is `never`), so the AC1.1.8 "message names the limit" fails unless the new endpoints write their own body.
- Turning `include-message` on globally is **not** a safe shortcut. The existing `/requests/pending` 400 message is `"as-of date <caller value> is before ..."`, which echoes caller input.
- So US1.1 needs its own error handling, scoped to the new controller: an `@ExceptionHandler` or `ProblemDetail` in `api`. Note that Spring's `ProblemDetail` fills `instance` with the request path by default, so that field must be suppressed too.
- AC1.1.9 should add an example: "a refused `GET /reviewers/rita%20k/filter` answers a body that does not contain `rita`".

### 6. Hidden work in US1.1: strict body parsing (AC1.1.6)

Spring Boot's default Jackson setup accepts several bodies that AC1.1.6 says must be refused:

- unknown properties are ignored (`FAIL_ON_UNKNOWN_PROPERTIES` is disabled by Boot)
- `"overLimit": "true"` is coerced to a boolean
- `"tenant": 5` is coerced to `"5"`
- with a plain record, a missing `tenant` cannot be told apart from `"tenant": null`

Binding the body straight to a record therefore passes the happy path and fails AC1.1.6. The implementation has to read the body as a tree (or raw bytes) and check field presence and JSON types explicitly. That is cheap, but the code plan must name it. Ask AC1.1.6 to list the concrete cases, so the tests catch coercion:

- `{"tenant":"TX-01"}` (missing field)
- `{"tenant":"TX-01","overLimit":true,"x":1}` (extra field)
- `{"tenant":"TX-01","overLimit":"true"}` (string where a boolean is expected)
- `{"tenant":5,"overLimit":false}` (number where a string is expected)

Two more points on AC1.1.6:

- **"1 KB" is ambiguous.** State "more than 1,024 bytes" and give the boundary: a valid body padded with spaces to 1,024 bytes is accepted, and 1,025 bytes is refused. Spring has no default body-size limit for this, so the check is code we write. It must not rely only on `Content-Length`, which can be absent with chunked requests.
- **Content type.** A save without `Content-Type: application/json` gets **415** from Spring, not 400. Either accept 415 in AC1.1.6 or ask for 400 explicitly. I suggest accepting Spring's 415 (smallest change) and saying so.

### 7. Smaller points on US1.1

- **AC1.1.7:** `.` and `..` match the FR1.3 character set, but Tomcat normalises `/reviewers/../filter` to another route before our code runs, so it answers 404, not 400. Either reject ids made only of dots in FR1.3 at Contract Design, or let AC1.1.7 allow "400 or 404, and nothing saved" for them. Otherwise the AC cannot be met for those inputs.
- **AC1.1.8:** the limit check and the insert must be one atomic step. Otherwise two new reviewers saving at the same moment both get in at limit minus one. A limit of 2 means its own Spring context (a separate test class with `properties=`) or a store-level unit test plus one HTTP test for the status and message. Both are fine; it is a code-plan choice, not an AC change.
- **Known tenants (FR3.1):** derive them from `RequestStore.all()` (all requests, not only pending), never through `HolidayCalendar.forTenant` (NFR3).

### 8. US1.2: AC1.2.1 and the tenant list (OQ2)

AC1.2.1 says the picker offers "exactly the tenants the API accepts as known". Of the three OQ2 options:

- **The queue's own rows** cannot meet "exactly". They hold only *pending* rows, and once a tenant filter is applied, only that tenant's rows, while FR3.1 counts non-pending requests too.
- **A fixed list in the screen** drifts from the export.
- **A new endpoint** (for example `GET /tenants`) is API work that no story carries today.

So AC1.2.1 as written effectively chooses the endpoint, and that work has no owner. **Proposal:** OQ2 is decided at Contract Design before US1.2's code plan. If it is an endpoint, it goes into **US1.1** (Kiran owns FR3), with its own AC ("`GET /tenants` answers 200 with `["NM-02", "TX-01"]`, sorted"). US1.2 builds against that contract. If the team prefers no new endpoint, relax AC1.2.1 to the option chosen.

### 9. US1.2: other implementation notes

- **AC1.2.10:** the shared `esc` in `render.js` today escapes `& < > "` but **not `'`**, and it is not exported. US1.2 must export it, add `'`, and use it for the picker's `<option>` text and `value` attribute. That changes `render.js` and `render.test.js`, which brings in the back-fill rule for that test file. Also, "tenant id or label": there is no label field in the API. Say "tenant ids, row values and messages".
- **OQ3 (`overLimitOnly` vs `overLimit`):** whichever way it goes, it touches `queue-filters.js` and `queue-filters.test.js` (2 of the 6 baseline tests). The story should expect those tests to change, as AC1.1.10 does for the API.
- **AC1.2.9:** also cover `?reviewer=` present but empty. Treat it like no reviewer, so nothing is saved under an empty id (A1).
- **AC1.2.4 / AC1.2.6:** the current page does not catch a failed `fetchPending` (a top-level `await`, so the table stays empty). The stories do not ask to fix a failing *queue* load. I am mentioning it, not proposing it.

### 10. US1.3: AC1.3.2

The enabled rule (tenant is "All" and the switch is off) should be a pure function in a `src/` module, so it is tested by `node --test` (AC1.2/AC1.3 testable logic). The "skipped or announced by keyboard and screen reader" clause cannot be tested with the team's tools, because there are no DOM or browser tests. A native `disabled` button meets it without extra code. The story should say this part is checked by hand at the code-plan review or the demo, so nobody writes a test that cannot exist.

### 11. US1.4: notes

- **AC1.4.1:** times are "to the second", but `Instant` from a real clock carries fractions of a second, and Jackson 3 writes them. Make the AC's clock read `2027-01-12T09:15:30.789Z` and expect `"2027-01-12T09:15:30Z"`, so the truncation is proven, not only the formatting.
- **Clock:** there is no `Clock` bean today. US1.4 adds one (UTC system clock), and tests replace it. The existing controller's `LocalDate.now()` stays as it is (surgical).
- **FR7.1 vs FR7.3:** FR7.1 stores the reviewer id on each line, while FR7.3's response shape leaves it out. AC1.4.1 follows FR7.3 (the reviewer is in the path), which I agree with. Contract Design should say explicitly that the id is stored but not returned.
- **Making NFR2 and FR1.5 testable:** today NFR2 is Deferred, and FR1.5 has no AC that runs concurrently (AC1.1.2 is sequential). Proposed **AC1.4.8:** "Given 20 saves for `rita.k` sent at the same time from different threads, then her history has 20 lines, and the stored filter equals the newest line" (FR1.5, NFR2). This is the only observable check that the save and the history line cannot come apart. It is deterministic in what it asserts, even though the thread order is not.

## Positions

- AGREE: One AI-DLC story per Rally story (Q2 A): each one fits a single PR in its own repo.
- AGREE: US1.2 depends on the agreed contract only: every US1.2 test stubs `fetchFn`, so it can be built and tested before US1.1 merges.
- AGREE: US1.4 follows US1.1, but the reason should be stated as a code dependency (the same store class and save path, NFR2), so its branch is cut only after US1.1 merges.
- AGREE: AC1.2.7 and AC1.2.8 can be built, provided the sequencing lives in one DOM-free `src/` module that is tested with controlled promises.
- OBJECT: NFR6 (CORS) is marked Deferred with no story owning the code: without it no `PUT` works from the browser. It must land in US1.1, cover `/requests/pending` too, and have an AC.
- OBJECT: AC1.2.1 ("exactly the tenants the API accepts") can in practice only be met by a new API endpoint, and no story carries it. Resolve OQ2 before US1.2's plan and put any endpoint in US1.1.
- OBJECT: AC1.1.5 and AC1.1.10 understate the NM-02 change. The new row's status and date range must be stated, or the existing `asOf=2026-10-13` tests turn into 400s, and the changed test files must be named (back-fill rule).
- OBJECT: AC1.1.6 as written can be "met" by a record binding that silently coerces types and ignores extra fields. List the concrete cases and define 1 KB as 1,024 bytes with a boundary, so the tests catch it.
- OBJECT: AC1.1.7 cannot be met for the ids `.` and `..`, which FR1.3 allows but Tomcat re-routes before our code runs. Either narrow FR1.3 at Contract Design or let the AC accept 404 for them.
