# Performance Test Instructions

## Applicability
No performance tests are generated. The test strategy is Minimal, and the requirements set no measurable performance target.

## Known risk (not tested)
The age is counted one day at a time from `receivedAt` to `asOf`. With realistic ages (days to weeks) the cost is trivial. Nothing in the requirements limits `asOf`, so a far-future `asOf` makes each row cost more. If a limit is wanted, raise it as a follow-up requirement.

## How to run if needed later
There is no load-test tooling in the repo. Performance Validation (4.6) is not in the express plan.
