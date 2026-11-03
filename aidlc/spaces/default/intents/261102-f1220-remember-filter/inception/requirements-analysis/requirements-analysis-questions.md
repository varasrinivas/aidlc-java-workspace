# Requirements Analysis — Questions

These questions build on:

- the approved intent and scope (`ideation/`)
- the Rally stories in `docs-in/rally/F1220/F1220-remember-my-filter.md`
- Meena Iyer's draft API contract in `docs-in/specs/F1220/reviewer-filter-api-spec.md`
- the code scans (`codekb/`)
- the team practices just affirmed

Everything those already settle becomes a requirement without a question. These are the points they leave open.

## Q1. Who may change a reviewer's saved filter?

The draft contract identifies a reviewer by login name, passed by the screen as `?reviewer=`, because there is no sign-in. Scope already accepts that anyone using the screen can read any reviewer's history. The same is true of writing: anyone could also save a filter in another reviewer's name. That would change what that reviewer sees and write a history line that looks like theirs. Nothing short of sign-in prevents it.

A. Accept it for this version as part of the same no-sign-in limit, and add writing to Meena Iyer's release-notes line
B. Not acceptable: sign-in has to come into F1220 (this reopens the approved scope with Dana Ortiz)
C. Not yet decided
X. Other (please specify)

[Answer]: A. Dana Ortiz accepted it in the session; Meena Iyer adds writing to the release-notes line.

## Q2. What counts as a valid reviewer id?

The reviewer id is the login name and is untrusted input. The team's security checklist asks for every request value to be validated and size-limited.

A. 1 to 64 characters, letters, digits, dot, hyphen and underscore only, case-sensitive. Anything else gets 400 and nothing is saved.
B. Any non-blank text up to 64 characters
C. Not yet defined
X. Other (please specify)

[Answer]: A.

## Q3. Which tenants are "known"?

US5160 refuses a tenant "the export doesn't know" with 400. The API has no tenant list: the only source is the tenant ids in the bundled request export, which today holds only `TX-01`. The NM-02 row F1210 asked for was never added.

A. Every tenant that appears in the request export (all requests, pending or not); US5160 adds an NM-02 request to the sample export so there are two
B. A list of tenants set in the API's configuration
C. Not yet decided
X. Other (please specify)

[Answer]: A. Kiran Rao adds the NM-02 request in US5160.

## Q4. What exactly does a saved filter look like?

The draft contract sends `{"tenant": "TX-01" | null, "overLimit": true | false}`. Two points are open: whether `overLimit: false` means "show everything" (as the queue treats it today), and what "Clear filters" saves.

A. Both fields always present on a save: `tenant` is a known tenant or `null` (all tenants), and `overLimit` is `true` or `false`, where `false` means all requests. "Clear filters" saves `{"tenant": null, "overLimit": false}`. Reading back with nothing ever saved returns `{}`, and the screen treats `{}` the same as a cleared filter.
B. Both fields optional, and a missing field means "not set". "Clear filters" saves `{}`.
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q5. Does every save write a history line, even when nothing changed?

US5163 says "every saved filter writes one audit line".

A. Yes: every successful save writes exactly one line, including "Clear filters" and a save that repeats the current filter
B. Only a save that changes the filter writes a line
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q6. Should there be limits on how much the API keeps?

Anyone can save without signing in, and everything is kept in memory. A caller could keep adding reviewers or history lines until the API runs out of memory.

A. Yes: keep at most the newest 1,000 history lines per reviewer (older ones dropped), and at most 10,000 reviewers. A save that would exceed the reviewer cap is refused with a clear error.
B. Yes, with different numbers (please give them under Other)
C. No limits this version: a restart clears everything anyway
D. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q7. What does the screen do when it can't load the saved filter on open?

Today a failed call leaves an empty table with no message.

A. Open unfiltered, as today, and show a short message that the saved filter couldn't be loaded
B. Open unfiltered and show nothing
C. Show an error and no queue until the reviewer reloads
D. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q8. What does the screen do when saving a changed filter fails?

A. Keep showing the queue with the filter the reviewer just chose, and show a short message that it wasn't saved
B. Put the control back to its previous value and show a message
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q9. How do nurse managers read the history in this version?

US5163 adds the history to the API (`GET /reviewers/{reviewerId}/filter/history`). No story adds a history view to the screen.

A. API only: a nurse manager reads it from the API directly. No history view on the screen in F1220.
B. Add a simple history view to the reviewer screen (new scope, which Dana Ortiz would have to approve)
C. Not yet decided
X. Other (please specify)

[Answer]: A. Ravi Menon agreed: the API is enough for this version.

## Consolidated Summary Confirmation

- Anyone using the screen may also save a filter in another reviewer's name; accepted for this version by Dana Ortiz, and Meena Iyer adds writing to the release-notes line (Q1)
- A reviewer id is 1-64 characters of letters, digits, dot, hyphen and underscore, case-sensitive; anything else gets 400 and nothing is saved (Q2)
- Known tenants are every tenant in the request export (all requests, pending or not); Kiran Rao adds an NM-02 request to the sample export in US5160 (Q3)
- A save always carries both fields: `tenant` is a known tenant or `null` (all tenants), `overLimit` is `true` or `false` (`false` = all requests); "Clear filters" saves `{"tenant": null, "overLimit": false}`; reading with nothing saved returns `{}`, which the screen treats as cleared (Q4)
- Every successful save writes exactly one history line, including "Clear filters" and a repeat of the current filter (Q5)
- The API keeps at most the newest 1,000 history lines per reviewer (older dropped) and at most 10,000 reviewers; a save that would exceed the reviewer cap is refused with a clear error (Q6)
- If the saved filter can't be loaded on open, the screen opens unfiltered and shows a short message (Q7)
- If saving a changed filter fails, the queue keeps the reviewer's new filter and a short message says it wasn't saved (Q8)
- Nurse managers read the history from the API only; no history view on the screen in F1220, agreed by Ravi Menon (Q9)

Does this all look correct before I generate the requirements artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
