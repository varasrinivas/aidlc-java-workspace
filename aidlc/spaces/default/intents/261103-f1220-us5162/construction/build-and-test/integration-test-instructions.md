# Integration Test Instructions: US5162 Clear my filters

## Scope

No integration tests are written for this story (Minimal test strategy). US5162 changes only `priorauth-web` and calls the API only through US5161's existing contract C1 client. The Clear save sends the C1 request body `{"tenant":null,"overLimit":false}`, which `saved-filter-client.test.js` already checks ("saveFilter sends a null tenant for all tenants").

## Where Integration Is Checked

The parent feature's Build and Test (`261102-f1220-remember-filter`) owns the one manual end-to-end check across both repos. For this story it adds:

1. Open the screen with `?reviewer=<id>`, set TX-01 and "Over limit only", and use "Clear filters". The whole queue shows, and the button becomes disabled.
2. Reload. The filter is still cleared.
3. `GET /reviewers/<id>/filter/history` shows the clear as its own line (US5163).

## How to Run

None to run in this story. The unit suite runs with `scripts\verify.cmd priorauth-web`.

## Coverage Target

Not applicable at this level. Line coverage is NOT MEASURED in F1220.
