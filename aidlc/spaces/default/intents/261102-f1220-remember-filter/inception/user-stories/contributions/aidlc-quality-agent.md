**Collaborator:** aidlc-quality-agent

## Contribution

I reviewed every acceptance criterion against four questions. Does it have a clear pass/fail? Can it be automated with the team's tools (JUnit 5 + AssertJ + MockMvc; `node --test` with an injected `fetchFn`, no browser or DOM tests)? Does each story have a happy path plus at least two error or edge cases? Can it be tested in isolation, with a clock the test controls? Most criteria pass. The points below are the ones that need a change before code plans are written against them.

### 1. Cross-cutting: how screen criteria are proven without DOM tests

The team rule (team.md Testing Posture, NFR9) is that screen logic lives in `src/` modules and `index.html` only calls them. For US1.2 and US1.3 to be testable, the stories should say the behaviour is proven through a DOM-free `src/` module (for example a filter-session/controller module). The test drives it with an injected `fetchFn` and asserts on two things:
- **the requests sent**: the URLs and bodies the stub `fetchFn` received (for example `GET /reviewers/rita.k/filter`, then `GET /requests/pending?tenant=TX-01&overLimit=true`, then `PUT /reviewers/rita.k/filter` with a given body)
- **the returned view state**: the selected tenant, the switch value, whether Clear is enabled, the rows to show, and the message text.

Proposed wording for the US1.2 and US1.3 headers: "Each criterion is proven by `node --test` against a `src/` module with a stubbed `fetchFn`; 'the screen shows X' means the module's returned view state or rendered markup string contains X."

### 2. Accessibility criteria need a named verification method (AC1.2.1, AC1.3.2, NFR10)

"Work by keyboard", "visible labels" and "skipped or announced as unavailable by keyboard and screen reader" cannot be automated with the team's tools. Split each into an automatable part and a manual part:
- **Automated (render string test):** the picker is a native `<select>` and the switch a native `<input type="checkbox">`, each with a `<label for>` that matches its `id`. "Clear filters" is a native `<button>` that carries the `disabled` attribute when no filter is set (AC1.3.2) and loses it after any filter is set (AC1.3.3). Failure messages are text in the rendered output, not a class or colour only.
- **Manual (recorded check):** a short keyboard and screen-reader checklist (Tab order, Space/arrow keys change the controls, the disabled button is skipped) that is run once at the feature's Build and Test or demo, with the result written into the Build and Test record.
- Make AC1.3.2 a single pass/fail. Replace "skipped **or** announced as unavailable" with "uses the native `disabled` attribute", which gives both behaviours.
- In traceability, mark NFR10 as `OK: US1.2, US1.3 (automated markup) + build-and-test (manual keyboard check)`, not plain OK.

### 3. AC1.2.7 and AC1.2.8 must be deterministic

"A stubbed API that answers slowly" invites real timers and flaky tests. Reword both criteria so the stub `fetchFn` returns promises that the test resolves by hand, with no `setTimeout` and no wall clock:
- **AC1.2.7:** with A's save held open, the test applies B and then C. When A resolves, **exactly** two saves were sent, in the order A then C ("at most two" is not a pass/fail when the test controls timing). The last body is C.
- **AC1.2.7, queue answers out of order:** state the out-of-order case explicitly. The queue answer for A resolves **after** the one for C, and the shown rows stay C's.
- **New edge for AC1.2.7:** A's save fails while C is waiting. C is still sent and stored, and the "not saved" message is cleared once C's save succeeds. Otherwise the case where an earlier save fails and a later one succeeds has no defined behaviour.
- **AC1.2.8:** the saved-filter read is held open, the user changes a control, then the read resolves. The controls and rows stay on the user's choice, and no extra queue request or save is made for the late value.

### 4. Gaps in US1.1 (API)

- **FR1.3 case sensitivity has no AC.** Add: "Given `rita.k` saved TX-01, when `GET /reviewers/Rita.K/filter` is sent, then it answers `{}`." This proves that ids are case-sensitive and that the two reviewers are distinct.
- **AC1.1.7 needs the accepted boundary as well as the refused one.** Add "an id of exactly 64 allowed characters is accepted". Add one encoded-character case such as `rita%20k`, and a traversal-like id such as `..`, which must give 400 or 404 and never reach another endpoint. Say what an empty id (`/reviewers//filter`) gives, or leave it to Contract Design. As written it is unspecified.
- **AC1.1.6 lists six refusal cases in one sentence.** Ask for one test per case, parameterised, each starting from a known saved filter so "unchanged" can be checked. Two cases are missing:
  - `"overLimit": null`: is it a wrong type? It should get 400.
  - an empty body.

  For the size limit, state the boundary in bytes ("more than 1,024 bytes"). The test pads a valid body with whitespace, so the over-size case is refused because of its size and not for any other reason.
- **AC1.1.9 needs a concrete oracle.** Send a sentinel such as `ZZ-99<x>` as the tenant and a sentinel reviewer id. Assert the error body does not contain the sentinel, has no `trace` or `exception` key, and does not contain `Exception` or `\tat `. Without a sentinel, "none of the raw values" cannot be checked.
- **FR1.5 is traced OK but only the sequential case is tested (AC1.1.2).** Add a testable form of "close together": "Given N saves for `rita.k` sent in parallel, when all complete, then the stored filter equals one of the N bodies and equals the newest history line, and the history has gained N lines (with US1.4)." This also gives NFR2 a first automated check. If the team prefers, mark FR1.5 `Partial: US1.1 (sequential) + nfr-design (concurrent)` instead.
- **AC1.1.3 "does not take a slot" is only observable with a limit.** Make it concrete: "With the limit set to 2, after `GET` of `new.one`'s filter and of its history, reviewers `a` and `b` can both still save." This also covers FR1.4's read-only rule for the history endpoint.
- **NFR3 "never used to build a file path or cache key / never passed to `HolidayCalendar.forTenant`"** cannot be proven by a behaviour test. It is a code-review item on the security checklist at 3.5. Trace NFR3 as `OK: US1.1 (size and validation ACs) + code-plan review (no path/key from caller input)`.

### 5. Gaps in US1.4 (history)

- **AC1.4.1 "to the second":** add a fixed clock reading `2027-01-12T09:15:30.789Z`, with the expected line at `09:15:30Z` (truncated, not rounded). Add a clock set to a non-UTC zone, which must still produce `Z`. This makes "UTC to the second" a pass/fail instead of an example that happens to have no fractional seconds.
- **AC1.4.4 same-time ordering:** state that the three saves run under one fixed clock instant, with distinguishable bodies (TX-01/true, NM-02/false, null/false), so the order is checked by content.
- **AC1.4.6 trimming:** five saves give only about six distinct bodies, so the test should use a clock it advances per save (for example +1 s). The assertion is then exact: lines 5, 4, 3, newest first.
- **The new endpoint has no safe-error criterion.** AC1.1.9 (NFR4) belongs to US1.1, but US1.4 adds `GET .../filter/history`. Add "AC1.4.8: an invalid reviewer id on the history endpoint answers 400 with a body that follows AC1.1.9", and add US1.4 to NFR4 in traceability.
- **AC1.4.7 "No screen view is added"** is checked in review of the US1.4 diff (it touches `priorauth-api` only), not by a test. Say so, so nobody writes a test for something that is not there.
- **TD-4 (`LocalDate.now()` with no `Clock`):** the US1.4 code plan must inject a `Clock` bean that tests override with `Clock.fixed` or a mutable test clock. This should appear in US1.4's INVEST note ("Testable ... with a controlled clock"), which already points the right way.

### 6. Test isolation for the API stories

- The ACs reuse `rita.k` across many criteria. With `@SpringBootTest` the context, and so the in-memory store, is cached and shared across test classes. State in the stories that example ids are illustrative and each test uses its own reviewer id or resets the store (team.md Q7 B, NFR9).
- **The limit criteria (AC1.1.8, AC1.1.3 rewritten, AC1.4.6) cannot run in the shared context.** "Reviewers `a` and `b` have saved" with a limit of 2 only holds if no other test has saved. Recommend proving the limits at the store level, with a new store instance built with limits 2 and 3 and no Spring. Add one MockMvc test, in its own context with `@TestPropertySource`, that proves the HTTP status and message mapping for the limit refusal.

### 7. Contract drift between the two repos

With the walking skeleton off and US1.1 and US1.2 built in parallel, the API is tested with MockMvc and the screen with a stub `fetchFn`. No automated test proves the two agree. Two recommendations:
- **Delivery Planning / Contract Design:** publish the contract's example request and response bodies once (saved filter, `{}`, the 400 error body, the limit error, the history list). Both repos' tests then use those exact JSON examples, copied verbatim with a comment naming the contract.
- **The feature's Build and Test:** add a short manual end-to-end check run locally against the real API: open with `?reviewer=`, change, reload, clear, and read the history. This also catches the cross-origin (NFR6) gap, which no `node --test` run can see.

### 8. Criteria that stay provisional until Contract Design

AC1.1.8 (the status code), AC1.1.9 (the error body shape), AC1.2.1 (where the tenant list comes from, OQ2, and the order of the options) and the `overLimitOnly`/`overLimit` naming (OQ3) cannot be finalised now. Mark them "provisional: finalised in Contract Design" so each story's 3.5 code plan restates the final pass/fail value. For AC1.2.1, also state the option order (as returned, or sorted), or the "exactly the tenants" test has no fixed expectation.

### 9. Other edge cases to add to US1.2 and US1.3

- **AC1.2.4:** add "the saved-filter read answers 200 with a body that isn't a valid filter (for example `{"tenant": 5}`)", treated as the same failure. Also add: the saved tenant is no longer in the known-tenant list. Either open unfiltered with the message, or keep it selected; Contract or Domain Design decides, but the AC should name one.
- **AC1.2.2 / AC1.2.9:** the reviewer id from the address is URL-encoded into the path. A test with `?reviewer=../requests/pending` asserts that the request goes to `/reviewers/..%2Frequests%2Fpending/filter` (or is not sent) and never to another endpoint. Also state that `?reviewer=` with an empty value behaves as AC1.2.9.
- **AC1.2.5:** add the switch-only change (`{"tenant": null, "overLimit": true}`), so both controls' change paths are tested.
- **AC1.2.10:** codekb TD-7 says `esc` does not escape `'` today, so this AC changes `render.js` and its existing test file. Under team.md that changed file then needs the happy path plus two edge cases. Note it in the story so the US1.2 plan names `test/render.test.js`.
- **US1.3:**
  - Add "Clear while a save is in flight follows AC1.2.7: the stored filter ends as `{"tenant": null, "overLimit": false}`".
  - Add "Clear with no reviewer in the address (A1) clears the controls and the queue and sends no save".
  - AC1.3.3 needs two cases, tenant only and switch only.

### 10. Traceability corrections

- **NFR8:** it is `Deferred: build-and-test`, yet AC1.1.10 already cites it. Use `OK: US1.1 (AC1.1.10), US1.2 (web 6/6 kept) + build-and-test`. Add to US1.2 an AC or a definition-of-done line saying the 6 existing web tests keep passing, because US1.2 changes `render.js` and possibly `queue-filters.js` (OQ3).
- **NFR9:** it is traced to US1.4 only. Test isolation applies to US1.1, and "logic in tested `src/` modules" applies to US1.2 and US1.3, so trace it to all four.
- **NFR11 deferral:** I agree it is deferred to build-and-test for the NOT MEASURED report. Each story's definition of done should still carry "every new branch tested; each new or changed test file has the happy path and at least two error or edge cases", because Build and Test cannot add tests after the fact.
- **NFR2 and NFR6 deferral:** I agree, on condition that NFR Design names the owning story and test for each. NFR6 can be tested with a MockMvc preflight from an allowed origin and from a disallowed one, owned by US1.1 (and US1.4 for the history path). NFR2 needs a store-level test with a history append that fails.

### Coverage per story (happy path + at least two error or edge cases)

| Story | Happy | Error / edge (current) | Verdict |
|---|---|---|---|
| US1.1 | AC1.1.1, AC1.1.2, AC1.1.5 | AC1.1.3-AC1.1.9 | Met; add the boundary and case-sensitivity cases (§4) |
| US1.2 | AC1.2.2, AC1.2.5 | AC1.2.3, AC1.2.4, AC1.2.6-AC1.2.10 | Met once AC1.2.7 and AC1.2.8 are deterministic (§3) |
| US1.3 | AC1.3.1 | AC1.3.2, AC1.3.4 | Just met; add the in-flight and no-reviewer edges (§9) |
| US1.4 | AC1.4.1, AC1.4.4 | AC1.4.3, AC1.4.5, AC1.4.6 | Met; add the safe-error AC for the new endpoint (§5) |

## Positions

- AGREE: One AI-DLC story per Rally story (Q2 A). It gives each owner one set of criteria to build and test against.
- AGREE: Deferring NFR1, NFR2, NFR6 and NFR11 out of the stories (Q3 A), provided NFR Design names the owning story and test for NFR2 and NFR6.
- AGREE: AC1.4.1 fixes the clock value and AC1.1.8 and AC1.4.6 use small configured limits. Both are the right shape for deterministic tests.
- AGREE: AC1.2.10 includes `'`. It forces the TD-7 escaping gap to be closed and tested.
- OBJECT: AC1.2.1 and AC1.3.2 (NFR10 keyboard and screen-reader parts) have no verification method the team's tools can run. Split them into an automated markup assertion and a recorded manual check, and make AC1.3.2 one pass/fail (the native `disabled` attribute).
- OBJECT: AC1.2.7 ("answers slowly", "at most two saves") is not a deterministic pass/fail. It should use promises the test resolves by hand, require exactly A then C, and state the out-of-order queue-answer case.
- OBJECT: FR1.5 is traced OK, but no AC tests concurrent saves. Add a parallel-save AC, or trace it as Partial with the rest deferred to nfr-design.
- OBJECT: FR1.3 case sensitivity of `reviewerId` has no acceptance criterion. Add the `Rita.K` vs `rita.k` case.
- OBJECT: The new history endpoint (US1.4) has no safe-error criterion, and NFR4 is traced to US1.1 only. Add AC1.4.8 and trace NFR4 to US1.4.
- OBJECT: The reviewer-limit criteria (AC1.1.8, AC1.1.3) cannot be tested reliably in the shared Spring context. The stories should state that the limits are proven against a fresh store instance (or their own context), and that example reviewer ids are illustrative.
