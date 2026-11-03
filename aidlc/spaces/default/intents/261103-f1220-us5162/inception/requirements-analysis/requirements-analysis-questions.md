# Requirements Analysis Questions: US5162 Clear my filters (F1220)

The parent feature (261102-f1220-remember-filter) already approved the story (US1.3, AC1.3.1-AC1.3.6), its requirements (FR6.1-FR6.3, NFR10), the contract and the plan, so none of that is asked again. Only two points are open. Both come from the wording fix handed over from US5161's code review and from the code scan of `feature/F1220`.

## Question 1: Wording when a saved tenant is dropped

When the screen opens, a saved tenant that is no longer in the tenant list is dropped. The over-limit switch is kept, and nothing is saved (FR4.8). Today the screen then shows the same message as a failed read: "Your saved filter couldn't be loaded, so all requests are shown." (`src/filter-session.js:10`). With the switch on, that isn't true, because only over-limit requests are shown. US5161's code review handed this wording to US5162. How should the dropped-tenant case read?

A. Give the dropped tenant its own message that is true in both switch states: "Your saved tenant is no longer available, so all tenants are shown." The failed-read message stays as it is. (Recommended)
B. Give the dropped tenant its own message that changes with the switch: "...so all tenants are shown." when the switch is off, and "...so over-limit requests for all tenants are shown." when it is on. This needs two texts.
C. Keep one message for both cases, reworded so it makes no claim about what is shown: "Your saved filter couldn't be fully restored."
X. Other (please specify)

[Answer]: A. Tara Joshi, with Divya Pillai.

## Question 2: Does the saved-filter message stay after Clear?

The parent's rule (US1.2) is that the "couldn't load" messages stay until the next successful load. The saved filter is read only on open, so today the message stays on screen after Rita changes a filter or uses "Clear filters", even though her own new choice is then on screen and saved. A test, `test/filter-session.test.js:285-289`, checks that it stays. What should US5162 do?

A. Keep the parent's rule: the message stays until the page is reloaded. US5162 changes only its wording. (Recommended: a child story doesn't change what the parent approved.)
B. A successful "Clear filters" or filter change removes it, because the reviewer has replaced the saved filter herself. This changes the parent's approved rule, so the tech lead updates the parent first.
C. Only "Clear filters" removes it. This also changes the parent's rule and needs the tech lead first.
X. Other (please specify)

[Answer]: A. A child story doesn't change the parent's rule (Meena Iyer agreed).
