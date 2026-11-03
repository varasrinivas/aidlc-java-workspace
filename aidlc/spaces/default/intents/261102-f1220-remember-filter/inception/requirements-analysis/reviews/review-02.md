## Review

**Verdict:** READY
**Reviewer:** aidlc-product-lead-agent
**Date:** 2026-11-02T16:14:47Z
**Iteration:** 1

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Major | aidlc/spaces/default/intents/261102-f1220-remember-filter/inception/requirements-analysis/requirements.md > FR5.3 with FR1.5 | FR5.3 promises that "the last filter chosen is the one saved" when a reviewer changes controls quickly. FR1.5 says the last save to complete wins, so two overlapping saves can finish in the wrong order. The screen cannot guarantee the first promise as written, and a test cannot prove it without a rule for ordering the saves. | Say how the screen guarantees it, for example by sending a save only after the previous one finishes, or by dropping superseded saves. Or weaken the promise to "the last save to complete is stored". Add a pass/fail test case either way. | Resolved (reviewer) |
| R-02 | Minor | requirements.md > FR1.4, OQ1 | Which status code the reviewer-limit refusal gets is deferred to Contract Design, so the requirement has no pass/fail status check. The requirement also does not say whether GET filter and GET history for a never-saved reviewer take one of the 10,000 slots. | State that read-only calls never take a slot, and that the refusal is a 4xx or 5xx whose exact code is fixed in Contract Design. | Resolved (reviewer) |
| R-03 | Minor | requirements.md > NFR7 | "A fixed upper bound" is not measurable. The bound is 10,000 reviewers times 1,000 lines, which is up to 10 million lines. No memory figure is given. | Give the worst-case line count, or a measurable memory target. State whether a test at a small configured limit (A3) is the proof. | Resolved (reviewer) |
| R-04 | Minor | requirements.md > FR7.5, A2 | The intent promises an audit line for "every change", but FR7.5 drops lines beyond the newest 1,000 per reviewer. The release-notes line in A2 covers only the loss on restart and open read/write access. The history also cannot show who made a change, because anyone can save under any reviewer's id. | Add the 1,000-line trim and the "history shows the reviewer id, not who actually saved" caveat to the release-notes item Meena Iyer writes. | Resolved (reviewer) |
| R-05 | Minor | requirements.md > FR4.2 | FR4.2 adds a tenant picker and an over-limit switch to the page. Scope and Rally describe only restoring and clearing filters, so this is new UI. Its origin (codekb TD-1) is documented, but no confirmed answer approves it. | Confirm at the gate that adding the picker and switch to the page is in scope. Name US5161 as the owner of that UI. | Resolved (reviewer) |
| R-06 | Minor | aidlc/spaces/default/intents/261102-f1220-remember-filter/inception/requirements-analysis/requirements.md > FR4.3 with FR5.1 | The artifact does not say what happens if the reviewer changes a control before the initial saved-filter read (FR4.3) has answered. The late read could overwrite the reviewer's fresh choice, which is the same stale-answer problem FR5.3 closes for saves. | Add one sentence: a reviewer's change made before the initial read finishes wins, and the late read result is ignored. Add a matching test case. | New |

> R-01 Reviewer note: FR5.3 now says saves are sent one at a time, with a waiting save replaced by a newer one. It adds a pass/fail test: three quick changes A, B, C send at most two saves (A, then C) and the stored filter is C. This agrees with FR1.5.

> R-02 Reviewer note: FR1.4 says read-only calls never take a reviewer slot and the refusal is a 4xx that names the limit. Contract Design fixes the exact code (OQ1).

> R-03 Reviewer note: NFR7 gives the worst case of 10,000 filters and 10,000,000 history lines. It names a small-limit test (2 reviewers, 3 lines) as the pass/fail proof.

> R-04 Reviewer note: A2 lists four release-notes caveats. They include the 1,000-line trim and that a history line shows the reviewer id, not who saved.

> R-05 Reviewer note: FR4.2 records the picker and switch as in scope and names US5161 as owner.

### Summary

All five prior findings are addressed. The ordering promise now has a testable rule, and the limits and caveats are measurable and complete. One small corner remains (the initial read racing a first control change). It does not block engineering from starting.
