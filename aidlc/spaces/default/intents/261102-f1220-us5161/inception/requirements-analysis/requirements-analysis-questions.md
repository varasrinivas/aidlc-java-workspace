# Requirements Analysis Questions: US5161 Open the screen with my last filter

The parent intent `261102-f1220-remember-filter` already approved the story (US1.2, AC1.2.1-AC1.2.12), the unit (U2 `us5161-restore-filter`), the contract (C1, C2, C4) and the Bolt plan (B2). None of that is asked again here. These three questions cover cases the approved criteria don't decide, all of which come up when the screen opens.

## Question 1
The screen asks for the tenant list (`GET /tenants`) when it opens, to fill the Tenant picker (AC1.2.1). No approved criterion says what happens when that call fails, for example when the API is unreachable or the call times out after 10 seconds. What should the screen do?

A. The picker offers only "All tenants", plus the saved tenant if there is one. The queue still loads with the saved filter, and no message is shown.
B. The same as A, and the message area says the tenant list couldn't be loaded.
C. The screen treats it as a queue failure (AC1.2.12): it shows "The queue couldn't be loaded" and loads no rows.
X. Other (please specify)

[Answer]: B. Divya Pillai, with Tara Joshi.

## Question 2
A reviewer's saved tenant may not be in the list `GET /tenants` returns. That happens when the tenant was in the export when it was saved but is gone now (the in-memory store keeps it until a restart). What should the screen do on open?

A. Keep the saved tenant: add it to the picker as an extra option, select it, and ask the queue for it. The queue answers `200 []` for an unknown tenant, so the reviewer sees "No requests match this filter".
B. Drop the saved tenant: open with "All tenants" and keep the saved over-limit switch. The message area says the saved filter couldn't be loaded. Nothing is saved until the reviewer changes a control.
C. Drop the whole saved filter and open unfiltered, as in AC1.2.4.
X. Other (please specify)

[Answer]: B.

## Question 3
The story allows one message area showing at most one message (US1.2 common behaviour). On open, two failures can happen together: the saved filter couldn't be read (AC1.2.4) and the queue couldn't be loaded (AC1.2.12). A failed save can also arrive while the "couldn't load" message is showing. Which message is shown?

A. A fixed priority: "The queue couldn't be loaded" first, then "Your filter wasn't saved", then "Your saved filter couldn't be loaded", then "won't be remembered". When the higher message clears, the next one still in force shows.
B. The newest message replaces the older one.
C. A fixed priority as in A, but a cleared message is not brought back.
X. Other (please specify)

[Answer]: A.

## Question 4 (follow-up to Questions 1 and 3)
Question 1 (B) adds a fifth message, "The tenant list couldn't be loaded", but the priority order from Question 3 (A) doesn't include it. Where does it rank? The other messages, highest first, are: "The queue couldn't be loaded", "Your filter wasn't saved", "Your saved filter couldn't be loaded", "Open this page from your reviewer link to have your filter remembered".

A. Second: after "The queue couldn't be loaded", before "Your filter wasn't saved".
B. Third: after "Your filter wasn't saved", before "Your saved filter couldn't be loaded".
C. Last: after "Open this page from your reviewer link to have your filter remembered".
X. Other (please specify)

[Answer]: B
