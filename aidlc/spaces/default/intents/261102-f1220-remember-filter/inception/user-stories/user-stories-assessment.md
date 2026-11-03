# User Stories Assessment — F1220 Remember my filter

## Decision

**Execute.**

## Rationale

- F1220 is user-facing. Reviewers see their filter restored on the screen and can clear it, and nurse managers read a reviewer's filter history. (requirements.md: Intent Analysis, FR4-FR7)
- There are two personas with different goals: the reviewer, who wants convenience, and the nurse manager, who wants to explain a missed request. (requirements.md; intent-statement.md)
- The work crosses teams and repos. Four Rally stories, each with its own owner, are split across `priorauth-api` and `priorauth-web` and built in parallel against one contract. Stories with clear acceptance criteria are what each owner's child intent builds and tests against. (team-practices.md; scope-document.md)
- The business rules carry real risk: refused saves must write no history, limits apply, and failures must not lose the reviewer's choice. Given/When/Then criteria make each one testable. (requirements.md FR1, FR5, FR7; inception rules)

## Factors Considered

| Factor | Finding |
|---|---|
| Project type | Brownfield enhancement across two repos |
| User-facing scope | Reviewer screen (restore, save, clear) and nurse-manager history (API) |
| Complexity signals | Input validation, limits, atomic save plus history, ordering of quick changes, failure handling on the screen |
| Coordination | 4 owners, 2 repos, parallel build against one contract |

## Where Stories Add the Most Value

- Turning FR1-FR7 into acceptance criteria each story owner can test directly.
- Making the screen's failure and ordering behaviour (FR4.5, FR5.2, FR5.3, R-06) explicit for US5161 and US5162.
- Keeping the refused-save rules (FR1.2-FR1.4, FR7.2) the same across US5160 and US5163, which share the save path.
