# Component Inventory: priorauth-web

Each component is one file. Headings are the component names used in the Scope of Analysis block.

### index.html

- **Responsibility**: page markup, CSS, and the inline module script: reads `?api=` / `?reviewer=`, writes the controls once, wires `change` events and the Clear button (then focuses the Tenant picker, AC1.3.5), and applies each published view to the DOM (controls, Clear `disabled`, message, rows, count).
- **Depends on**: `src/filter-session.js`, `src/render.js`.
- **Tests**: none by rule (DOM wiring only).

### src/filter-session.js

- **Responsibility**: FilterSession (ADR-004). Holds the view state, the message flags and priority, the 10 s timeout wrapper, contract validation of C1/C2 answers, newest-queue-wins, single-flight save, late-read ignore, the dropped-tenant rule (US5162 FR4.10) and `clear()` (US5162 FR6.1).
- **Exports**: `MESSAGES`, `createFilterSession`.
- **Depends on**: `src/queue-filters.js`, `src/saved-filter-client.js`.
- **Tests**: `test/filter-session.test.js` (22).

### src/render.js

- **Responsibility**: QueueRenderer. HTML strings for rows, count, controls (incl. the "Clear filters" button), tenant options and queue states; the shared `esc` helper; `filterIsSet` (US5162 FR6.2).
- **Exports**: `countLabel`, `renderRows`, `filterIsSet`, `renderControls`, `renderTenantOptions`, `renderQueue`.
- **Depends on**: none.
- **Tests**: `test/render.test.js` (10).

### src/queue-filters.js

- **Responsibility**: filtered queue URL and load (US5153); `loadQueueFor` maps the saved filter's `overLimit` to `overLimitOnly` (US5161).
- **Exports**: `filteredUrl`, `loadQueue`, `loadQueueFor`.
- **Depends on**: `src/api.js` (`pendingUrl`).
- **Tests**: `test/queue-filters.test.js` (5).

### src/saved-filter-client.js

- **Responsibility**: C1 saved filter read/write and C2 tenant list (US5161); reviewer id encoded as one path segment.
- **Exports**: `filterUrl`, `tenantsUrl`, `readFilter`, `saveFilter`, `readTenants`.
- **Depends on**: none.
- **Tests**: `test/saved-filter-client.test.js` (9).

### src/api.js

- **Responsibility**: base queue URL (`pendingUrl`, with `asOf`) and the original one-call fetch (`fetchPending`, now unused by the page).
- **Exports**: `pendingUrl`, `fetchPending`.
- **Depends on**: none.
- **Tests**: `test/api.test.js` (2).

### test/contract-examples

- **Responsibility**: JSON examples of contracts C1 (saved, nothing saved, PUT body) and C2 (tenants), read by the session and client tests.
- **Depends on**: none.

### package.json

- **Responsibility**: package identity (`priorauth-web` 1.1.0, private, ES modules), `npm test` = `node --test`, `engines.node >= 20`. No dependencies.
