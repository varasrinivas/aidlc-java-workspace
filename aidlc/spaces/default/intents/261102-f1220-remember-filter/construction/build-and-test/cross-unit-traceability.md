# Cross-Unit Traceability — F1220 Remember my filter

## Verdict: PASS, with record gaps (updated 2026-11-03)

AC1.3.5 had no proof when this file was first written. It is now covered by manual check M5 (Divya Pillai and Tara Joshi, Chrome, keyboard; see `test-results.md`). The first verdict, FAIL with 1 uncovered ID, is kept below as written. F-2 and F-3 are gaps in the record only.

## First Verdict: FAIL (1 uncovered ID; record gaps)

- **Declared:** 87 IDs.
  - From `inception/requirements-analysis/requirements.md`: FR1-FR7, their 29 sub-requirements, and NFR1-NFR11.
  - From `inception/user-stories/stories.md`: AC1.1.1-AC1.1.13, AC1.2.1-AC1.2.12, AC1.3.1-AC1.3.6 and AC1.4.1-AC1.4.9.
- **Covered:** 86 of 87 have a test or a tagged main file on `feature/F1220`. Every file named below exists.
  - 60 are covered with status `OK` in a story's `code-generation/traceability.json`.
  - 19 are found only by their FR/AC tag in the repos (finding F-2).
  - 7 are the group headings FR1-FR7, covered through all their sub-requirements.
- **Uncovered:** **AC1.3.5** (focus moves to the Tenant picker after Clear). It is wired in `priorauth-web/index.html`, which the team doesn't test. It needs manual check M5.
- **Sources read:**
  - the four story intents' `construction/code-generation/traceability.json`;
  - for IDs missing there, a search of `priorauth-api/src` and `priorauth-web/{src,test,index.html}` for the ID tag.
  - The parent has no `construction/*/code-generation/` of its own: the stories were built in their child intents (Delivery Planning Q7).

Legend for the "How" column:
- **T** means `OK` in the story's `traceability.json`.
- **Tag** means the ID is tagged in the repo, but missing from `traceability.json`.

## Functional Requirements

| ID | Story | How | Target file (test or main) |
|---|---|---|---|
| FR1 | US5160, US5163 | via FR1.1-FR1.5 | — |
| FR1.1 | US5160 | Tag | `priorauth-api/.../api/ReviewerFilterControllerTest.java` |
| FR1.2 | US5160 | Tag | `priorauth-api/.../api/SavedFilterBody.java`, `SavedFilterBodyTest.java` |
| FR1.3 | US5160 | Tag | `priorauth-api/.../api/ReviewerIds.java`, `ReviewerIdsTest.java` |
| FR1.4 | US5160 | Tag | `priorauth-api/.../api/ReviewerLimitHttpTest.java`, `store/ReviewerFilterStoreTest.java` |
| FR1.5 | US5163 | T | `priorauth-api/.../store/ReviewerFilterStoreTest.java` |
| FR2 | US5160 | via FR2.1-FR2.3 | — |
| FR2.1 | US5160 | Tag | `priorauth-api/.../api/ReviewerFilterControllerTest.java` |
| FR2.2 | US5160 | Tag | `priorauth-api/.../api/ReviewerFilterContractTest.java` |
| FR2.3 | US5160 | Tag | `priorauth-api/.../api/ReviewerFilterControllerTest.java` |
| FR3 | US5160 | via FR3.1-FR3.3 | — |
| FR3.1 | US5160 | Tag | `priorauth-api/.../store/TenantDirectory.java`, `TenantDirectoryTest.java` |
| FR3.2 | US5160 | Tag | `priorauth-api/.../store/RequestStoreTest.java`, `api/TenantFilterTest.java` |
| FR3.3 | US5160 | Tag | `priorauth-api/.../api/TenantFilterTest.java` |
| FR4 | US5161 | via FR4.1-FR4.6 | — |
| FR4.1 | US5161 | T | `priorauth-web/index.html` |
| FR4.2 | US5161 | T | `priorauth-web/src/render.js` |
| FR4.3 | US5161 | T | `priorauth-web/src/filter-session.js` |
| FR4.4 | US5161 | T | `priorauth-web/src/filter-session.js` |
| FR4.5 | US5161 | T | `priorauth-web/src/filter-session.js` |
| FR4.6 | US5161 | T | `priorauth-web/src/saved-filter-client.js` |
| FR5 | US5161 | via FR5.1-FR5.3 | — |
| FR5.1 | US5161 | T | `priorauth-web/src/filter-session.js` |
| FR5.2 | US5161 | T | `priorauth-web/src/filter-session.js` |
| FR5.3 | US5161 | T | `priorauth-web/src/filter-session.js` |
| FR6 | US5162 | via FR6.1-FR6.3 | — |
| FR6.1 | US5162 | T | `priorauth-web/src/filter-session.js` |
| FR6.2 | US5162 | T | `priorauth-web/src/render.js` |
| FR6.3 | US5162 | T | `priorauth-web/test/filter-session.test.js` |
| FR7 | US5163 | via FR7.1-FR7.6 | — |
| FR7.1 | US5163 | T | `priorauth-api/.../store/ReviewerFilterStore.java` |
| FR7.2 | US5163 | T | `priorauth-api/.../api/ReviewerFilterHistoryTest.java` |
| FR7.3 | US5163 | T | `priorauth-api/.../api/ReviewerFilterController.java` |
| FR7.4 | US5163 | T | `priorauth-api/.../store/ReviewerFilterStore.java` |
| FR7.5 | US5163 | T | `priorauth-api/.../store/ReviewerFilterStore.java` |
| FR7.6 | US5163 | T | `priorauth-api/.../api/ReviewerFilterController.java` |

## Non-Functional Requirements

| ID | Story | How | Target file |
|---|---|---|---|
| NFR1 | US5160 | T | `priorauth-api/.../store/ReviewerFilterStore.java` |
| NFR2 | US5163 | T | `priorauth-api/.../store/ReviewerFilterStore.java` |
| NFR3 | US5160 | T | `priorauth-api/.../api/SavedFilterBody.java` |
| NFR4 | US5160, US5163 | T | `api/NewEndpointErrorHandler.java`, `api/NewEndpointProtocolErrorTest.java` |
| NFR5 | US5161 | T | `priorauth-web/src/render.js` |
| NFR6 | US5160 | T | `priorauth-api/.../api/BrowserAccessPolicyTest.java` |
| NFR7 | US5160, US5163 | T | `store/ReviewerFilterStoreTest.java`, `application.yml` |
| NFR8 | US5160, US5161 | T | `api/PendingRequestsControllerTest.java`, `priorauth-web/test/api.test.js` |
| NFR9 | US5163 | T | `priorauth-api/src/test/.../MutableClock.java` |
| NFR10 | US5162 | T (labels and disabled state only; keyboard use is manual M3) | `priorauth-web/test/render.test.js` |
| NFR11 | US5161, US5163 | T (branch tests; line coverage NOT MEASURED) | `filter-session.test.js`, `ReviewerFilterStoreTest.java` |

## Acceptance Criteria

| IDs | Story | How | Target file |
|---|---|---|---|
| AC1.1.1-AC1.1.13 (13) | US5160 | T | `ReviewerFilterControllerTest`, `ReviewerFilterStoreTest`, `ReviewerLimitHttpTest`, `TenantsControllerTest`, `BrowserAccessPolicyTest`, `TenantFilterTest` |
| AC1.2.1-AC1.2.12 (12) | US5161 | T | `priorauth-web/src/{render,filter-session,saved-filter-client}.js` |
| AC1.3.1-AC1.3.4, AC1.3.6 (5) | US5162 | T | `priorauth-web/test/{filter-session,render}.test.js` |
| **AC1.3.5** | US5162 | Manual: M5 passed on 2026-11-03 (no automated test; the wiring is in `priorauth-web/index.html`) | `test-results.md`, "Manual Screen Checks" |
| AC1.4.1-AC1.4.9 (9) | US5163 | Tag | `ReviewerFilterHistoryTest.java` (all 9 except AC1.4.7), `ReviewerFilterStoreTest.java` (AC1.4.1-AC1.4.7) |

## Uncovered and Gaps (to Surface at the Gate)

1. **AC1.3.5:** closed by M5, which passed on 2026-11-03. It still has no automated test, because the team has no DOM tests.
2. **F-2, record gaps:** 19 IDs are tested but missing from the stories' `traceability.json`:
   - FR1.1-FR1.4, FR2.1-FR2.3 and FR3.1-FR3.3 (US5160);
   - AC1.4.1-AC1.4.9 (US5163).

   Each story owner can add them in their own intent. The parent must not edit another intent's folder.
3. **F-3:** these IDs are used by stories but not declared in `requirements.md`: `FR1.6`, `FR4.7`, `FR4.8`, `FR4.9`, `FR4.10` and `FR8.1`. All of them are covered.
