# External Dependency Map — F1220 Remember my filter

A **Bolt** is one build pass over a piece of the work that ends in something that runs (`bolt-plan.md`).

No party outside the priorauth team can block a Bolt (`delivery-planning-questions.md` Q4). The repos, the contract, the test tooling and the release are all held inside the team. There are no deployed environments, external APIs or approval queues.

The only outside touch points are Rally and acceptance, and neither blocks a build:

| Item | Owner | Lead time | Bolt it touches | If it slips |
|---|---|---|---|---|
| Rally story status (In-Progress, then Completed, plus the PR link and intent id) | Each story owner | Minutes | B1-B4 | Nothing is blocked; the owner updates Rally when they can |
| Feature acceptance after the demo | Dana Ortiz | One demo session | After all Bolts merge | The release waits for acceptance |
| Nurse-manager input on the history at the demo | Ravi Menon | One demo session | After B4 | Acceptance can proceed; his feedback goes to a later feature |

**Things inside the team that do gate Bolts** are listed here so nothing is missed:

- The approved contract (done) gates B1 and B2.
- `feature/F1220` in both repos, which Meena Iyer creates, gates B1 and B2.
- B1's merge gates B4.
- B2's merge gates B3.
