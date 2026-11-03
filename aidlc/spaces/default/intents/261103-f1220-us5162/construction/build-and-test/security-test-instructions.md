# Security Test Instructions: US5162 Clear my filters

## Scope

There is no SAST or DAST tool in F1220 (team practice). The team's security checklist was applied at the mob's code-plan review. For this story, each point is checked as follows.

| Checklist point | US5162 | Evidence |
|---|---|---|
| Every request value is validated and size-limited | No new request value. Clear sends the fixed body `{"tenant":null,"overLimit":false}` | `src/filter-session.js` `clear()`; `test/filter-session.test.js` (AC1.3.1) |
| API data is escaped before it is shown | The button label and the new message are fixed text. Messages are set with `textContent`, and tenant values still go through `esc` | `src/render.js`; `test/render.test.js` (US5161 AC1.2.10 escape test still passes) |
| No file path or cache key built from a caller's value | Not affected | — |
| Error responses carry no stack traces or raw input | Not affected (no API change) | — |
| CORS only from named origins | Not affected | — |

## How to Run

`scripts\verify.cmd priorauth-web` runs the tests named above.
