# Requirements Analysis — Questions

Context: the request (Ravi Menon, 13 Oct) asks the pending list from `GET /requests/pending` to carry "the same business-day age and the over-5 flag" as the nightly report, where weekends and the org's holidays don't count. The nightly report's code is not in this workspace, so its exact rule can't be read off. These questions pin it down so the API matches the report.

## Question 1
How should the business-day age be counted? It depends on whether the day the request arrived counts. For example, a request received on Thursday 8 Oct 2026, viewed on Tuesday 13 Oct 2026 (Monday 12 Oct is a weekday):

A. Count business days after the received date, up to and including today (received day does not count). A request received today has age 0.
B. Count business days including both the received date and today. A request received today has age 1.
C. Count business days after the received date, up to but not including today (whole business days elapsed before today).
X. Other (please specify)

[Answer]: A — the received day is day 0, same as the report. (Ravi Menon, 09:47) **Mode:** chat

## Question 2
When should the "over-5" flag be true?

A. When the age is strictly greater than 5 business days (6 or more)
B. When the age is 5 business days or more
X. Other (please specify)

[Answer]: A — over means more than 5; the threshold is 5, from configuration. (Ravi Menon, 09:47) **Mode:** chat

## Question 3
Where should the list of org holidays come from? Nothing in the API knows about holidays today, and the nightly report's holiday list lives elsewhere.

A. A list of dates in the API's configuration (`application.yml`), which the team updates each year
B. A list of dates in a data file bundled with the API (like the existing sample data), updated each year
C. Read from the same source the nightly report uses (please name it), so the two can never disagree
D. Hard-code the 2026 US federal holidays for now
X. Other (please specify)

[Answer]: B — the same TX-01 list the report uses, as a JSON file in the API resources for now. (Meena Iyer, 09:47) **Mode:** chat

## Question 4
Which time zone decides what "today" is? This matters near midnight, and the received date has no time or zone attached.

A. The org's local time zone (please name it)
B. UTC
C. Whatever time zone the server runs in
X. Other (please specify)

[Answer]: C — the server's zone; callers can pass asOf. The API returns a flag and never refuses or alerts. (Ravi Menon, Meena Iyer, 09:47) **Mode:** chat

## Follow-up 1
You chose the TX-01 holiday list the nightly report uses (Question 3), but its dates aren't anywhere in this workspace, so I can't copy them. This matters right away: Monday 12 Oct 2026 falls inside the sample data's date range, and whether it is a TX-01 holiday changes the ages.

A. I'll paste the TX-01 holiday dates here
B. I'll point you to a file in the workspace that holds them
C. Ship the file with no dates for now (weekends only) and add the dates later
X. Other (please specify)

[Answer]: A — the 2026 TX-01 holidays are 2026-01-01, 2026-01-19, 2026-02-16, 2026-05-25, 2026-07-03, 2026-09-07, 2026-10-12, 2026-11-11, 2026-11-26, 2026-11-27, 2026-12-25. (Meena Iyer, 09:49) **Mode:** chat

## Follow-up 2
TX-01 is a tenant id, and every sample request belongs to TX-01. What should happen for a request from any other tenant?

A. Use the TX-01 list for every tenant for now (one org-wide holiday list)
B. Key the holiday file by tenant. Only TX-01 has dates; other tenants count weekends only
X. Other (please specify)

[Answer]: B — one file per tenant; a shared calendar service is a separate intent. (Meena Iyer, 09:49) **Mode:** chat
