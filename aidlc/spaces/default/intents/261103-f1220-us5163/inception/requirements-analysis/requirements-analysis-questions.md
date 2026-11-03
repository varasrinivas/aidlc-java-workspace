# Requirements Analysis Questions — US5163 Filter history

The parent intent (261102-f1220-remember-filter) already approved the requirements for this story and they are not asked again here: FR7.1-FR7.6, FR1.5, NFR2, NFR4, NFR7 and NFR9 in its `requirements.md`; AC1.4.1-AC1.4.9 in `stories.md`; and the C3 and C6 contracts in `contract-summary.md`, including the 2026-11-03 change that makes `.` and `..` answer `400 invalid-reviewer-id`. The scan of `feature/F1220` (2dbc68b) left only the implementation points below open. They are written as assumptions so you can confirm them in one step.

## Question 1: Assumptions for building the history on top of US5160

Context: these points are not set by the parent's documents. They decide how the history fits the code US5160 merged.

- **A1 History limit setting.** The history limit (FR7.5, A3) is a new key under the existing `priorauth.reviewer-filter` block of `application.yml`: `max-history-lines: 1000`. It has a comment naming FR7.5 and a default in `@Value`, like `max-reviewers`.
- **A2 Where the endpoint lives.** `GET /reviewers/{reviewerId}/filter/history` goes in `ReviewerFilterController`, as C3 names it. The existing error handling therefore covers it with no change: `NewEndpointErrorHandler` is scoped to that controller, and `NewEndpointProtocolErrorHandler` covers `/reviewers/**`. Any other method on the history path answers 405 with no body, and a request whose `Accept` excludes JSON answers 406 with no body, as on the other new paths.
- **A3 Clock.** A `java.time.Clock` bean (UTC system clock) is added and injected into `ReviewerFilterStore`, so tests control history times (NFR9, team rule Q7 C). It is a JDK type, so no dependency is added.
- **A4 Contract examples.** `c3-get-history.json` and `c3-get-history-empty.json` are copied from the parent's `contract-design/examples/` into `src/test/resources/contract/f1220/`, and the tests read them.
- **A5 Invalid ids.** `.`, `..` and every other invalid reviewer id answer `400 invalid-reviewer-id` with the fixed body on the history call too (contract change of 2026-11-03).
- **A6 Memory.** No cap beyond the parent's NFR7 is added. At the defaults, that is up to 10,000 × 1,000 lines in memory, which the parent accepted.
- **A7 Test isolation.** Each history test uses its own reviewer ids, because the Spring tests share one store (team rule Q7 B).

A. Accept assumptions
B. Convert to follow-up questions
X. Other (please specify)

[Answer]: A. Accept assumptions
**Mode:** guided (Arjun Nair, 2026-11-03)
