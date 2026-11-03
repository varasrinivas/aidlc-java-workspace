# Build Instructions: US5161 (priorauth-web)

## Dependencies

None. `priorauth-web` has no dependencies and no build step: plain ES modules and `index.html`. US5161 added no dependency. You only need Node >= 20 (`package.json` `engines`); this machine has v24.19.0.

## Environment Setup

- Check out `priorauth-web` on `f1220/us5161-restore-filter` (commit `9af272e`). It was cut from `origin/feature/F1220` at `65a999b`.
- No environment variables or config files are needed.
- The tests need no server.

## Build

There is nothing to compile or bundle. The "build" is the test run through the workspace verify script, run from the workspace root:

```
scripts\verify.cmd priorauth-web
```

On macOS or Linux, use `scripts/verify.sh priorauth-web`. Exit code 0 means every test passed.

## Running the Screen Locally (Manual Checks Only)

```
cd priorauth-web
npx serve .
```

Then open `http://localhost:3000/?reviewer=rita.k&api=http://localhost:8080`. `npx serve` is the README's own development tool, not a project dependency. The page needs `priorauth-api` running with US5160's endpoints and its CORS setting, so this works only after US5160 merges into `feature/F1220`.

## Troubleshooting

- **`verify: no repo is off its PR base; nothing to test`:** you ran the script without naming the repo on a clean base branch. Name the repo: `scripts\verify.cmd priorauth-web`.
- **The page shows "The queue couldn't be loaded":**
  - the API isn't running at `?api=`, or
  - the API doesn't allow `http://localhost:3000` (C5), or
  - the page was opened as `file://`, which isn't supported.
