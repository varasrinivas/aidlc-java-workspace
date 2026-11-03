# Contract Design — Questions

Much of the contract is already settled, so it is not asked again:

- **The calls themselves:**
  - `PUT` and `GET /reviewers/{reviewerId}/filter`
  - `GET /reviewers/{reviewerId}/filter/history`
  - `GET /tenants`
  - the unchanged `GET /requests/pending`
- **The save body:** `{"tenant": "<id>" | null, "overLimit": true | false}`, with both fields always present. With nothing saved, a read returns `{}`.
- **The history line:** four fields, `{"at", "reviewer", "tenant", "overLimit"}`. This settles FR7.3's wording in favour of FR7.1, as Meena Iyer agreed at the User Stories gate (R-07).
- **Rules carried over:**
  - the reviewer-id rules
  - the 1,024-byte body limit
  - named browser origins
  - `?reviewer=` as the screen's identity
  - no sign-in

These are the points still open. Each question shows a recommended option.

## Q1. What status code refuses a save that would pass the reviewer limit?

AC1.1.9 needs an exact code. The request itself is valid; the store is full for new reviewers.

A. `409 Conflict`: the request is valid but conflicts with the store's current state
B. `422 Unprocessable Content`
C. `429 Too Many Requests`. This usually means rate limiting, which is misleading here.
D. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q2. What does an error body look like on the new calls?

NFR4 says a short message, no stack trace, and never the caller's input. The screen needs to tell the cases apart.

A. A small fixed shape, `{"error": "<code>", "message": "<short text>"}`, with stable codes: `invalid-reviewer-id`, `invalid-body`, `unknown-tenant`, `reviewer-limit`. The message is fixed text per code and never contains caller input.
B. Spring's standard problem-details shape (`type`, `title`, `status`, `detail`), with its default `instance` path removed because it would echo the reviewer id
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q3. What does `GET /tenants` return?

A. A plain JSON array of tenant ids in ascending order, for example `["NM-02", "TX-01"]`
B. An object, `{"tenants": ["NM-02", "TX-01"]}`, which leaves room to add fields later
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q4. Who owns the contract, and how can it change once U1 and U2 have started?

Your rules say the tech lead owns the parent intent and story intents never change it. Units Generation's reviewer asked for this to be stated (R-02).

A. Meena Iyer owns it. The source is this stage's `contract-summary.md`, with one example JSON file per call under `inception/contract-design/examples/`. Changes are handled like this:
   - **Adding** a field to a response is allowed, because consumers ignore unknown fields.
   - **Adding** a field to the save body is a breaking change, because the API refuses unknown fields.
   - **Any breaking change** is agreed by Meena with the owners of the units affected, then made in the parent record first, with the examples updated.
   - U1 and U2 start only after this contract is approved.
B. Same, but each provider unit's owner (Kiran Rao for the API calls) owns their own call's spec
C. Not yet decided
X. Other (please specify)

[Answer]: A. Kiran Rao and Divya Pillai signed the examples off with Meena Iyer in the session.

## Q5. Is the API versioned?

A. No version in the path for F1220. Both repos release together from `feature/F1220`, and only this team's screen calls the API. Versioning comes when a second consumer appears.
B. Put the new calls under `/v1/`
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q6. How does the screen handle a slow or failed call?

The requirements define what the reviewer sees on failure (FR4.5, FR5.2, AC1.2.12). They don't say how long the screen waits, or whether it retries.

A. No automatic retries. Each call from the screen gives up after 10 seconds and is treated as a failure, showing the matching message. The reviewer's next change or a reload tries again.
B. Retry a failed read once before showing the message, with no retry for saves
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Consolidated Summary Confirmation

- A save refused by the reviewer limit answers `409 Conflict` (Q1)
- Errors on the new calls are `{"error": "<code>", "message": "<short text>"}` with codes `invalid-reviewer-id`, `invalid-body`, `unknown-tenant`, `reviewer-limit`; fixed message per code, never caller input (Q2)
- `GET /tenants` returns a plain array of tenant ids, ascending, e.g. `["NM-02", "TX-01"]` (Q3)
- Meena Iyer owns the contract: `contract-summary.md` plus one example JSON per call under `inception/contract-design/examples/`; response fields may be added, save-body fields may not without a breaking-change agreement made in the parent first; U1 and U2 start only after approval; Kiran Rao and Divya Pillai signed the examples off with Meena (Q4)
- No version in the path for F1220 (Q5)
- The screen does not retry; each call gives up after 10 seconds and is treated as a failure with the matching message (Q6)

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
