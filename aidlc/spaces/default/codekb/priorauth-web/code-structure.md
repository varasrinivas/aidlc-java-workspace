# Code Structure: priorauth-web

## Layout

```
priorauth-web/
  .gitignore                 node_modules/
  README.md                  run, serve and page parameters
  package.json               name, version 1.1.0, "type": "module", test script, engines
  index.html                 markup, CSS, inline module script (the only DOM code)
  src/
    api.js                   GET /requests/pending URL builder and fetch
    queue-filters.js         filtered queue URL and load (US5153, US5161)
    saved-filter-client.js   C1 saved filter and C2 tenants client (US5161)
    filter-session.js        page state, ordering and messages (US5161, US5162)
    render.js                HTML string rendering (US5161, US5162)
  test/
    <module>.test.js         one per src/ module
    contract-examples/       C1 and C2 JSON examples used by tests
```

## File Classification

| File | Category | Lines |
|---|---|---|
| `index.html` | Static/Asset + Controller (DOM wiring) | 60 |
| `src/filter-session.js` | Service/UseCase (state, orchestration) | 161 |
| `src/render.js` | Utility (view rendering) | 48 |
| `src/queue-filters.js` | Repository/DAO-like HTTP client | 22 |
| `src/saved-filter-client.js` | Repository/DAO-like HTTP client | 35 |
| `src/api.js` | Repository/DAO-like HTTP client | 14 |
| `package.json` | Configuration | 13 |
| `test/*.test.js` (5) | Test | - |
| `test/contract-examples/*.json` (4) | Test fixture | - |

## Dependency Adjacency List

- `index.html` -> `src/filter-session.js`, `src/render.js`
- `src/filter-session.js` -> `src/queue-filters.js`, `src/saved-filter-client.js`
- `src/queue-filters.js` -> `src/api.js`
- `src/api.js`, `src/saved-filter-client.js`, `src/render.js` -> none
- Circular references: none.

## Code Patterns

- ES modules with relative imports carrying `.js`; named exports only, no classes, no default exports.
- Factory with closures (`createFilterSession`) instead of a class.
- Every network function takes `fetchFn = fetch` as its last parameter.
- Non-2xx throws `Error("priorauth-api answered <status>")`.
- Line 1 of each `src/` file is a purpose comment naming story and contract; inline comments cite FR/AC/assumption ids.
- 2-space indent, double quotes, semicolons, template literals.
- Tests: `node:test` + `node:assert/strict`, behaviour-sentence names with story tags, a hand-driven fetch stub (`manualApi`) and no timers.

Per-module exports are listed in [component-inventory.md](component-inventory.md).
