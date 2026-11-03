# Integration Test Instructions: US5161

## Status

This intent writes no integration tests. Its test strategy is Minimal, which means unit tests only. The team also has no browser or DOM tests (team Testing Posture).

The screen's boundary with the API is covered by unit tests that use the agreed contract examples. `test/contract-examples/` holds byte-identical copies of the parent's C1 and C2 examples, and `test/saved-filter-client.test.js` and `test/filter-session.test.js` build their stub answers and check their requests against them.

## Where the Real Integration Check Happens

The parent intent `261102-f1220-remember-filter` owns the cross-repo check, at its Build and Test on `feature/F1220`, after all four story PRs merge (Bolt plan, "After the Four Bolts"). It is a manual end-to-end run:

1. Start `priorauth-api` from `feature/F1220`.
2. Serve `priorauth-web` with `npx serve .`.
3. Open `http://localhost:3000/?reviewer=rita.k&api=http://localhost:8080`.
4. Change the filter, reload, and see it restored.
5. Read `GET /reviewers/rita.k/filter/history`.

The same run covers keyboard use of the Tenant picker and the switch (AC1.2.1, NFR10).

## Test Data

The contract examples are the shared test source. When Meena Iyer changes an example in the parent record, its copy in `priorauth-web/test/contract-examples/` and the tests that read it change with it.
