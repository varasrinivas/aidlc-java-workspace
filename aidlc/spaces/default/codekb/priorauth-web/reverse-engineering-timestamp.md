# Reverse Engineering Timestamp

## Run Record

- Date: 2026-11-03
- Commit: ddca232bb3bbeaa76d57ab12a83648710ee64adb
- Branch: main (tag `v1.1.0`, clean working tree)
- Kind of run: full rescan of `priorauth-web`; replaces the previous store wholesale.
- Intent: f1220-us5162 (record `261103-f1220-us5162`)
- Left out unopened: `node_modules/` (gitignored), `.git/`.

## Scope of Analysis

```yaml
scope_version: 1
kind: full
intent: f1220-us5162
fingerprint: 9bbe1171d4a30b9d1584afe78e7352de6a03c9b7
analyzed:
  paths:
    - ./
  components:
    - index.html
    - src/filter-session.js
    - src/render.js
    - src/queue-filters.js
    - src/saved-filter-client.js
    - src/api.js
    - test/contract-examples
    - package.json
shallow:
  paths: []
```
