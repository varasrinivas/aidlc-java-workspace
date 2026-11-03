# Technology Stack: priorauth-web

| Layer | Technology | Version | Source |
|---|---|---|---|
| Language | JavaScript (ES modules; uses `??=`, `Array.prototype.findLast`, `.at()`) | ES2023-level | `src/`, `test/` |
| Runtime (tests) | Node.js | `>=20` (`engines`) | `package.json` |
| Runtime (page) | Modern browser: `fetch`, `URL`, `URLSearchParams`, `AbortSignal.timeout` | evergreen | `index.html`, `src/filter-session.js` |
| Package manager | npm (scripts only) | - | `package.json` |
| Build | none (no bundler, no transpiler) | - | README |
| Test runner | Node built-in `node --test` | Node 20+ | `package.json` |
| Assertions | `node:assert/strict` | Node built-in | `test/` |
| Local static server | `serve` via `npx serve@14` | 14 (not a declared dependency) | README |
| UI framework | none (string templates + DOM properties) | - | `src/render.js`, `index.html` |
| Backend | `priorauth-api` (Java 21, Spring Boot, separate repo) | `v1.2.0` per workspace history | workspace |

No formatter, linter, coverage tool or CI is configured; see [code-quality-assessment.md](code-quality-assessment.md).
