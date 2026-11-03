# Build Instructions: US5162 Clear my filters

## Prerequisites

- Node 20 or later (`priorauth-web/package.json` `engines`). The verify run used the Node on this machine.
- `priorauth-web` on branch `f1220/us5162-clear-filters` (`835c32e`, cut from `origin/feature/F1220` `b9c8448`).

## Dependencies and Environment

- There are no dependencies to install: `priorauth-web` has no `dependencies` or `devDependencies`, and this story adds none.
- There are no environment variables. The page takes `?api=` (default `http://localhost:8080`) and `?reviewer=` from its address.

## Build

- There is no build step. The screen is plain ES modules served as files (`index.html` imports `./src/*.js`).
- Build verification is the test run through the verify script from the workspace root:

```
scripts\verify.cmd priorauth-web
```

`scripts/verify.sh priorauth-web` does the same on macOS or Linux.

## Running the Screen Locally (for the manual checks)

- Serve the `priorauth-web` folder over http, for example `npx serve priorauth-web` or any static server. Open `index.html?reviewer=<id>`.
- Point it at a running `priorauth-api`, whose CORS allows the page's origin. Until US5160 is in `feature/F1220`, the saved-filter calls fail and the page shows the saved-filter message. That is expected.

## Troubleshooting

- **`verify` reports nothing tested:** a run with no arguments on a clean branch tests nothing. Always name the repo.
- **A module fails to load in the browser:** the page must be served over http, not opened as `file://`.
