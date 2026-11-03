# Performance Test Instructions: US5161

## Status

This intent writes no performance tests:

- The test strategy is Minimal.
- No performance target applies to this story. The requirements set none for the screen, and this express workflow has no NFR Requirements or NFR Design stage.
- There are no deployed environments (team Deployment practice).

## Timing Behaviour That Is Tested

The one timing rule in this story comes from the contract: every call from the screen gives up after 10 seconds, with no retries. It is checked as a unit test: every call the session makes carries an `AbortSignal` (`test/filter-session.test.js`). No test waits 10 seconds.

## How to Run

Not applicable. If a later feature sets a screen performance target, add instructions here.
