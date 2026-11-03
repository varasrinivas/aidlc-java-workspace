# Cross-Unit Traceability — F1220 US5160

## Verdict

**FAIL on the strict check, with no untested requirement.**

- **The check:** every `FR` and `NFR` in `inception/requirements-analysis/requirements.md` must appear with status `OK` in `construction/code-generation/traceability.json`, with a target file that exists. This intent has no User Stories stage, so no AC list is enumerated from `stories.md`. The ACs still appear, because `traceability.json` covers them.
- **Result:** 8 of the 21 requirement IDs are listed in `traceability.json` (FR1.6, FR8.1, NFR1, NFR3, NFR4, NFR6, NFR7, NFR8), and every listed target file exists. The other 13 IDs are not listed there.
- **Why it isn't a testing gap:** `traceability.json` maps most requirements through the acceptance criteria that prove them (AC1.1.1-AC1.1.13, all `OK`) rather than by FR ID. Each of the 11 unlisted FRs has a passing test tagged with its own ID in the test source, and the two unlisted NFRs are team practices with evidence in `test-results.md`; the table below names them.
- **Fix:** add the 13 IDs as direct entries to `construction/code-generation/traceability.json`, using the test files below as targets. It is a record-only change; no code or test changes. I have not made it, because that file belongs to the approved Code Generation stage.

## Coverage per ID

| ID | In `traceability.json` | Proven by (tagged, passing test) | Target file exists |
|---|---|---|---|
| FR1.1 | No (via AC1.1.1, AC1.1.2) | `ReviewerFilterControllerTest` (`@Test // AC1.1.1, FR1.1, FR2.1`) | Yes |
| FR1.2 | No (via AC1.1.4, AC1.1.6) | `ReviewerFilterControllerTest` (`AC1.1.6, FR1.2`), `SavedFilterBodyTest` (`FR1.2`) | Yes |
| FR1.3 | No (via AC1.1.7, AC1.1.8) | `ReviewerFilterControllerTest` (`AC1.1.7, FR1.3, FR2.3`; `AC1.1.8, FR1.3`) | Yes |
| FR1.4 | No (via AC1.1.3, AC1.1.9) | `ReviewerFilterStoreTest` (`AC1.1.3, FR1.4`), `ReviewerLimitHttpTest` (`AC1.1.9, FR1.4`) | Yes |
| FR1.5 | No (via AC1.1.2) | `ReviewerFilterStoreTest` and `ReviewerFilterControllerTest` (`AC1.1.2, FR1.5`) | Yes |
| FR1.6 | Yes, `OK` | `ReviewerFilterContractTest` | Yes |
| FR2.1 | No (via AC1.1.1) | `ReviewerFilterControllerTest` (`AC1.1.1, FR1.1, FR2.1`) | Yes |
| FR2.2 | No (via AC1.1.3) | `ReviewerFilterControllerTest` (`AC1.1.3, FR2.2`), `ReviewerFilterContractTest` (`FR2.2`) | Yes |
| FR2.3 | No (via AC1.1.7) | `ReviewerFilterControllerTest` (`FR2.3`), `ReviewerFilterContractTest` (`FR2.3`) | Yes |
| FR3.1 | No (via AC1.1.5, AC1.1.11) | `TenantsControllerTest` (`FR3.1`), `RequestStoreTest` (`FR3.1`) | Yes |
| FR3.2 | No (via AC1.1.13) | `RequestStoreTest`, `PendingRequestsControllerTest`, `TenantFilterTest` (`US5160 FR3.2`) | Yes |
| FR3.3 | No (via AC1.1.13) | `TenantFilterTest` (`US5160 FR3.3`), `TenantsControllerTest` (`AC1.1.13, FR3.3`) | Yes |
| FR8.1 | Yes, `OK` | `BrowserAccessPolicy.java`; tested in `BrowserAccessPolicyTest` (`NFR6, FR8`) | Yes |
| NFR1 | Yes, `OK` | `ReviewerFilterStore.java` (in-memory, one class) | Yes |
| NFR3 | Yes, `OK` | `SavedFilterBody.java`; tested in `SavedFilterBodyTest`, `ReviewerFilterControllerTest` (`NFR3`) | Yes |
| NFR4 | Yes, `OK` | `NewEndpointErrorHandler.java`; tested in `ReviewerFilterControllerTest` (`AC1.1.10, NFR4`), `NewEndpointProtocolErrorTest` (`NFR4`) | Yes |
| NFR6 | Yes, `OK` | `BrowserAccessPolicyTest` | Yes |
| NFR7 | Yes, `OK` | `ReviewerFilterStoreTest` (`AC1.1.9, NFR7`) | Yes |
| NFR8 | Yes, `OK` | `PendingRequestsControllerTest`; baseline 12/12 in `code-summary.md` | Yes |
| NFR9 | No | Practice-level: own reviewer ids per test, own context for limits (`test-results.md`, TP-INDEPENDENT) | n/a |
| NFR11 | No | Practice-level: every new branch tested, every new/changed file has happy + 2 edge cases; coverage NOT MEASURED (`test-results.md`, TP-FILES) | n/a |

Acceptance criteria in `traceability.json`: AC1.1.1-AC1.1.13, all `OK`, and every target file exists.

## Uncovered Elements (strict check)

- **13 IDs not listed in `traceability.json`:** FR1.1, FR1.2, FR1.3, FR1.4, FR1.5, FR2.1, FR2.2, FR2.3, FR3.1, FR3.2, FR3.3, NFR9 and NFR11.
- **Untested:** none. Every FR has a passing test tagged with its own ID. NFR9 and NFR11 are practices, evidenced in `test-results.md`.
