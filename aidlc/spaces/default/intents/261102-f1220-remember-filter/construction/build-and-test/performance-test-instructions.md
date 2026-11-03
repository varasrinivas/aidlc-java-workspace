# Performance Test Instructions — F1220 Remember my filter

The requirements set no latency or throughput target for F1220. The only measurable performance-type requirement is the memory bound (NFR7), stated as limits rather than bytes. There is no deployed environment and no load-test stage in the plan (team Deployment practice). So this file covers bounded-resource checks only.

## What Is Checked, and How

| Target | Check | Command |
|---|---|---|
| NFR7 / FR1.4: at most 10,000 reviewers kept; a new reviewer beyond the limit is refused | `ReviewerFilterStoreTest` and `ReviewerLimitHttpTest` with small configured limits (2 reviewers); `application.yml` default `10000` | verify script |
| NFR7 / FR7.5: at most 1,000 history lines per reviewer, keeping the newest | `ReviewerFilterStoreTest` AC1.4.6 and `ReviewerFilterHistoryTest` with limit 3; `application.yml` default `1000` | verify script |
| NFR2 under concurrency: the save and its history line together | `ReviewerFilterStoreTest` AC1.4.7: 50 concurrent saves | verify script |
| Screen: the 10 s give-up on every call (contract C1, C2, C4) | `filter-session.test.js` asserts every call carries an `AbortSignal`. `src/filter-session.js` sets `TIMEOUT_MS = 10000` (checked by reading the code; no test waits 10 s) | verify script, plus code reading |
| Screen: only the newest queue answer shows, and saves go one at a time (FR5.3) | `filter-session.test.js` AC1.2.7, with stubbed slow answers the test resolves by hand | verify script |

## Not Covered (No Target, No Environment)

- **Memory in bytes.** The worst case at default limits is about 640 MB of history (10,000 × 1,000 lines), estimated in US5163's code summary. Saved filters alone are under 3 MB. Neither is measured. Before any shared deployment, a heap check with `-Xmx` and a filled store is the right test; it belongs to the feature that adds a deployed environment.
- **Lock contention.** One lock serialises all saves and reads (ADR-001, accepted). There is no HTTP load test.
