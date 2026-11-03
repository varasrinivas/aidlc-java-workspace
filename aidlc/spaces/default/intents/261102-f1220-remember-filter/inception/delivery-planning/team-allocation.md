# Team Allocation — F1220 Remember my filter

One team, priorauth, builds all four Bolts. A **Bolt** is one build pass over a piece of the work that ends in something that runs. Each Bolt has one owner who drives that story's own child intent and PR. The owner pairs with the other person working in the same repo (Team Formation, `mob-composition.md`).

The **mob** is the whole team working one problem together on one call, with one person typing. It reviews every code plan before code is written.

| Bolt | Unit | Rally | Owner | Pair | Repo | Wave |
|---|---|---|---|---|---|---|
| B1 | U1 `us5160-save-filter` | US5160 | Kiran Rao | Arjun Nair | priorauth-api | 1 |
| B2 | U2 `us5161-restore-filter` | US5161 | Divya Pillai | Tara Joshi | priorauth-web | 1 |
| B3 | U3 `us5162-clear-filters` | US5162 | Tara Joshi | Divya Pillai | priorauth-web | 2 (after B2) |
| B4 | U4 `us5163-filter-history` | US5163 | Arjun Nair | Kiran Rao | priorauth-api | 2 (after B1) |

## Who Does What

- **Story owners:**
  - Create their story's child intent. It uses `express` scope and names only their repo, and its arguments point at this plan and `inception/units-generation/unit-of-work.md`.
  - Move the Rally story to In-Progress when it starts and to Completed when the PR merges.
  - Paste the PR link and the intent id into the story's Discussion.
- **The mob (whole team, Meena Iyer typing):** reviews each story's code plan before code is written. Plan approval is on in every child intent.
- **Meena Iyer (tech lead):**
  - Creates `feature/F1220` in both repos from the current `main`.
  - Owns the contract.
  - Runs this parent's Build and Test and the feature PRs to `main`.
  - Bumps the versions, tags each repo, and writes the release notes.
- **Dana Ortiz (product owner):** accepts the feature after the demo, and decides if US5162 has to slip.
- **Ravi Menon (nurse manager):** consulted on the history at the demo.
- **Pairs while waiting:** while B1 and B2 run, Arjun Nair pairs with Kiran Rao on the API and Tara Joshi pairs with Divya Pillai on the screen. That puts both second-wave owners inside the code they will extend.

This is one team, so there is no multi-team program board. This parent workflow itself is run solo from Meena Iyer's session. Each story's build happens in its owner's child intent, not here.
