# Requirements — F1220 Remember my filter

## Sources

| Tag | Source |
|---|---|
| Intent | `ideation/intent-capture/intent-statement.md` (approved) |
| Scope | `ideation/scope-definition/scope-document.md` (approved) |
| Rally | `docs-in/rally/F1220/F1220-remember-my-filter.md`: stories US5160-US5163 and their acceptance criteria |
| Spec | `docs-in/specs/F1220/reviewer-filter-api-spec.md`: Meena Iyer's draft API contract, an input to Contract Design |
| RQ<n> | `inception/requirements-analysis/requirements-analysis-questions.md`, question n (confirmed) |
| Practices | `memory/team.md` and `memory/project.md` (affirmed in Practices Discovery) |
| codekb | `codekb/priorauth-api/`, `codekb/priorauth-web/` (approved Reverse Engineering) |
| Corners | `corner-checklist.md` sweep at Standard depth (stated as requirements the team can correct at the gate) |

## Intent Analysis

- **Goal:** reviewers stop re-picking their queue filter every day, on any browser. Nurse managers can explain why a reviewer did not see a request, from a history of filter changes. (Intent)
- **Type:** an enhancement to an existing product. It is brownfield, across two repos: `priorauth-api` gets a new resource, and `priorauth-web` gets new screen behaviour. (codekb)
- **Complexity:** Standard. The work is small, with three new endpoints and one screen. It still needs input validation, memory limits, failure handling and a history that is never written for a refused save.
- **Must-have stories:** US5160, US5161 and US5163. US5162 is a should-have and slips first. Due in 2027.Q1 R1. (Scope)

## Functional Requirements

### FR1 Save a reviewer's filter (US5160)

- **FR1.1** `PUT /reviewers/{reviewerId}/filter` with a valid body saves it as that reviewer's last filter, replacing any earlier one, and answers 204. (Rally US5160; Spec)
- **FR1.2** The body always has both fields:
  - `tenant` is a known tenant id (FR3) or `null`, which means all tenants.
  - `overLimit` is `true` or `false`, where `false` means all requests.
  - A missing field, an extra field, a wrong type, an unknown tenant or an unreadable body gets 400. The saved filter stays as it was, and no history line is written. (Rally US5160; RQ4)
- **FR1.3** A `reviewerId` must be 1 to 64 characters from letters, digits, `.`, `-` and `_`, and it is case-sensitive. Any other id gets 400, and nothing is saved or written. (RQ2; Practices security checklist)
- **FR1.4** The API keeps saved filters for at most 10,000 distinct reviewers. A save for a new reviewer beyond that limit is refused with a 4xx error that names the limit, and nothing is saved or written. Contract Design fixes the exact code. Reviewers already kept can still save. Read-only calls (FR2, FR7.3) never take a reviewer slot: reading a reviewer who has never saved stores nothing. (RQ6; gate feedback R-02)
- **FR1.5** When two saves for the same reviewer arrive close together, the last one completed wins. Each completed save writes its own history line. (Corners: concurrency)

### FR2 Read a reviewer's filter (US5160)

- **FR2.1** `GET /reviewers/{reviewerId}/filter` answers 200 with the last saved filter, in the same shape as FR1.2. (Rally US5160; Spec)
- **FR2.2** For a reviewer who has never saved, it answers 200 with `{}`. (Rally US5160; RQ4)
- **FR2.3** An invalid `reviewerId` (FR1.3) gets 400. (RQ2)

### FR3 Known tenants (US5160)

- **FR3.1** A tenant is known when it appears as the `tenantId` of any request in the request export, whether pending or not. The comparison is exact and case-sensitive, as F1210's `tenant` filter is. (RQ3; codekb)
- **FR3.2** US5160 adds an NM-02 request to the sample export, so the product has two known tenants (TX-01 and NM-02). Existing tests that count rows are updated in the same story. Kiran Rao owns this. (RQ3)
- **FR3.3** `GET /requests/pending` keeps its current behaviour: an unknown `tenant` still answers `200 []`. Only the new save refuses unknown tenants. (codekb; Spec)

### FR4 Open the screen with the reviewer's last filter (US5161)

- **FR4.1** The screen takes the reviewer from its `?reviewer=` page parameter, as the spec sets it. (Spec)
- **FR4.2** US5161 adds a tenant picker and an "over limit only" switch to the page. Both were in F1210's tested code but never added to the page, and the restore and clear behaviour needs them. The team confirmed at the Requirements Analysis gate that this UI is in scope and that US5161 owns it. (codekb TD-1; Rally US5161; gate feedback R-05)
- **FR4.3** On open, the screen reads the reviewer's saved filter. It then asks the queue with that filter, and the controls show it. (Rally US5161)
- **FR4.4** With no saved filter (`{}`), or a saved filter of `{"tenant": null, "overLimit": false}`, the screen opens unfiltered, as it does today. (Rally US5161; RQ4)
- **FR4.5** If the saved filter cannot be read, the screen opens unfiltered and shows a short message that the saved filter couldn't be loaded. Failures include the API being unreachable, an error answer, or a 400 for an invalid reviewer id. The queue still loads. (RQ7)
- **FR4.6** The picker offers exactly the tenants the API accepts as known (FR3), plus "All tenants". How the screen gets that list is decided in Domain and Contract Design. (RQ3; Open questions)

### FR5 Save the filter when a control changes (US5161)

- **FR5.1** When the reviewer changes the tenant picker or the switch, the screen asks the queue with the new filter and saves it (FR1). (Rally US5161)
- **FR5.2** If the save fails, the queue keeps showing the filter the reviewer just chose, and a short message says it wasn't saved. (RQ8)
- **FR5.3** If the reviewer changes controls quickly, only the latest queue answer is shown. The screen also sends saves one at a time: while a save is in flight, any newer choice waits, and a waiting save is replaced by an even newer one. So the last filter chosen is always the last save sent and the one stored. Test (pass/fail): with a stubbed API that answers slowly, three quick changes A, B, C send at most two saves (A, then C, with B dropped), and the stored filter is C. (Corners: older response arrives last; gate feedback R-01)

### FR6 Clear filters (US5162)

- **FR6.1** One "Clear filters" control sets the tenant to all tenants and the switch to off, shows the whole queue, and saves `{"tenant": null, "overLimit": false}`. (Rally US5162; RQ4)
- **FR6.2** "Clear filters" is disabled when no filter is set, meaning the tenant is all tenants and the switch is off. (Rally US5162)
- **FR6.3** A failed save after "Clear filters" behaves as FR5.2. (RQ8)

### FR7 History of filter changes (US5163)

- **FR7.1** Every successful save writes exactly one history line with:
  - the time, in UTC to the second
  - the reviewer id
  - the tenant, or `null`
  - `overLimit`

  This includes "Clear filters" and a save that repeats the current filter. (Rally US5163; RQ5)
- **FR7.2** A refused save writes no line. Refusals include an unknown tenant, an invalid body, an invalid reviewer id and the reviewer limit. (Rally US5163; FR1.2-FR1.4)
- **FR7.3** `GET /reviewers/{reviewerId}/filter/history` answers 200 with that reviewer's lines, newest first. Lines with the same time keep the order they were saved in, newest first. Each line has the shape `{"at": "<UTC ISO time>", "tenant": ..., "overLimit": ...}`. (Rally US5163; Spec; Corners: ordering)
- **FR7.4** A reviewer with no saves gets `[]`, and an invalid `reviewerId` gets 400. (RQ2; Corners: empty)
- **FR7.5** The API keeps at most the newest 1,000 lines per reviewer and drops older ones when a new line is written. (RQ6)
- **FR7.6** The history is read through the API only. There is no history view on the screen in F1220. (RQ9)

## Non-Functional Requirements

- **NFR1 Data lifetime:**
  - Saved filters and history are kept in memory, behind one class that a later feature can replace with a durable store.
  - A restart or redeploy empties both. This is accepted for this version. (Rally US5160; Intent; Scope)
- **NFR2 Atomic save:** a save and its history line succeed or fail together. There is never a saved filter without its line, and never a line without its saved filter. (FR7.1-FR7.2; Corners: multi-step write)
- **NFR3 Input limits:**
  - Every request value is validated and size-limited at the API boundary, as FR1.2-FR1.4 describe.
  - A request body larger than 1 KB is refused with 400.
  - No caller-supplied value is used to build a file path or a cache key. In particular, it is never passed to `HolidayCalendar.forTenant`. (Practices security checklist; codekb)
- **NFR4 Error responses:** errors from the new endpoints carry a short message and no stack trace, and never echo raw caller input. The body shape is set in Contract Design. (Practices security checklist; codekb TD-5)
- **NFR5 Safe display:** every value from the API shown on the screen is escaped for HTML. That covers tenant ids, labels and messages, and includes `&`, `<`, `>`, `"` and `'`. (Practices security checklist; codekb TD-7)
- **NFR6 Cross-origin calls:**
  - The API allows browser calls to the new endpoints only from named origins, never `*`.
  - The allowed origins are configured and include the screen's local development origin.
  - (Practices security checklist; codekb)
- **NFR7 Memory bound:**
  - With the default limits, the API stores at most 10,000 saved filters and at most 10,000 × 1,000 = 10,000,000 history lines.
  - Proof (pass/fail): a test with small configured limits (A3), for example 2 reviewers and 3 lines, shows two things. A third new reviewer's save is refused, and a reviewer's history never holds more than 3 lines, keeping the newest.
  - (RQ6; gate feedback R-03)
- **NFR8 Compatibility:**
  - `GET /requests/pending` and its existing tests keep passing, except for the row counts FR3.2 updates.
  - The screen's 6 existing tests keep passing.
  - The API's baseline is recorded by Kiran Rao before the first code change. (Practices; codekb)
- **NFR9 Testability:**
  - History times come from an injected clock that tests control.
  - API tests do not share saved filters or history, using their own reviewer id or a store reset.
  - Screen logic lives in tested `src/` modules, and `index.html` only calls them. (Practices Testing Posture)
- **NFR10 Accessibility:**
  - The tenant picker, the switch and "Clear filters" work by keyboard and have visible labels.
  - The disabled state of "Clear filters" and the failure messages are shown in text, not by colour alone.
  - (Corners: screens; Practices NEVER cut accessibility)
- **NFR11 Coverage:**
  - Each story tests every new branch it adds. Each new or changed test file covers the happy path and at least two error or edge cases.
  - Line coverage is not measured in F1220. Build and Test reports it as NOT MEASURED, under the team's recorded exception. (Practices Testing Posture)

## Constraints

- Two repos and two PRs per cross-repo change: `priorauth-api` (Java 21, Spring Boot, Maven) and `priorauth-web` (JavaScript ES modules, no dependencies). Stories merge into `feature/F1220`. (Practices)
- No new dependency unless a unit's plan names it first. No coverage tooling, linter or CI is added in F1220. (Practices)
- Tests run only through the workspace verify script, with the repos named before each PR. (Practices)
- No sign-in in this product. The reviewer id is an untrusted value supplied by the screen. (Spec; Scope)
- Due in release 2027.Q1 R1. US5162 slips first if the date is at risk. (Scope)

## Assumptions

- **A1** If the screen is opened without `?reviewer=`, it opens unfiltered, as today. The controls still filter the queue, but nothing is saved or read, and a short note says the filter won't be remembered. Reason: the spec names `?reviewer=` as the only identity, and nothing should be saved under an empty id. The team can correct this at the gate.
- **A2** Anyone using the screen can read any reviewer's history and save a filter in any reviewer's name. Dana Ortiz accepted this for this version (RQ1; Scope). Meena Iyer's release-notes line covers four limits (gate feedback R-04):
  - anyone can read and write any reviewer's filter and history
  - the history is lost on restart
  - only the newest 1,000 history lines per reviewer are kept
  - a history line shows the reviewer id it was saved under, not who actually saved it
- **A3** The reviewer limit (FR1.4) and the history limit (FR7.5) can be configured, with the defaults 10,000 and 1,000. Reason: matching the existing `priorauth.` configuration style costs nothing and lets tests use small limits.
- **A4** Tenant ids are opaque strings matched exactly, so `tx-01` is not `TX-01`. Reason: F1210's `tenant` filter already behaves this way (codekb).

## Out of Scope

- A durable store, sign-in, and limiting who may read or write a reviewer's filter or history. (Scope; RQ1)
- More than one saved filter per reviewer, or filter fields beyond tenant and over-limit. (Scope)
- Exporting the history or keeping it for a set retention period. (Scope)
- A history view on the screen. (RQ9)
- Coverage tooling, a linter and CI. (Practices)
- The hard-coded 2026 holiday file name in `HolidayCalendar`, which needs its own bug. (codekb TD-3)

## Open Questions (for later stages)

- **OQ1 (Domain and Contract Design):**
  - The exact status code for a save refused by the reviewer limit (FR1.4).
  - The error body shape for 400 responses (NFR4).
- **OQ2 (Domain and Contract Design):** how the screen gets the list of known tenants for the picker (FR4.6): a new endpoint, the queue's own rows, or a fixed list.
- **OQ3 (Contract Design):** whether the screen's `overLimitOnly` option is renamed to the contract's `overLimit` or mapped to it in one place.
- **OQ4 (NFR Design):** the list of allowed browser origins (NFR6) and where it is configured.
