# Security Test Instructions: US5161

## Status

There is no SAST or DAST tool in F1220 (team Code Style and Testing Posture). The screen's security rules are proven by unit tests that run through the verify script, against the team's five-point security checklist, which the mob applied at the code-plan review.

## What Is Tested

| Checklist point | Test |
|---|---|
| API data is escaped before it is shown (NFR5, AC1.2.10) | `test/render.test.js`: a tenant `<b>'x"&` renders escaped in the options and the rows, with `'` as `&#39;` |
| Request values are validated and size-limited | `test/saved-filter-client.test.js`: a reviewer id with `/`, `?` or a space stays one encoded path segment, and a save body has exactly `tenant` and `overLimit`. `test/filter-session.test.js`: a saved-filter or tenant-list answer outside the contract is treated as a failure. |
| No file path or cache key from a caller's value | Not applicable: the screen builds neither. |
| Error responses carry no stack traces or raw input | The screen shows only its fixed `MESSAGES` texts through `textContent`. API error bodies are never parsed or shown (`test/filter-session.test.js` failure cases). |
| CORS named origins only | Owned by US5160 (C5) in `priorauth-api`, not this repo |

## How to Run

```
scripts\verify.cmd priorauth-web
```

Run it from the workspace root. These tests are part of the same suite.

## Not Covered

- Validation of the reviewer id's content. The API owns it (C1 returns `400 invalid-reviewer-id`). The screen only encodes the id and shows the saved-filter message on any failure.
- A browser-level XSS check. There are no DOM tests; escaping is checked on the rendered strings only.
