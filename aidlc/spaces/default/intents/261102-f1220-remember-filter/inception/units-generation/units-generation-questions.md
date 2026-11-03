# Units Generation — Questions

Much of the decomposition is already set by the team's rules and the earlier stages, so it is not asked again:

- **One Rally story = one unit = one branch = one PR** (team practice). That gives four units: US5160, US5161, US5162 and US5163.
- **Kind of each unit:**
  - US5160 and US5163 are API work (`service`, `priorauth-api`).
  - US5161 and US5162 are screen work (`ui`, `priorauth-web`).
- **Dependencies:**
  - US5163 needs US5160 merged, because it changes US5160's store (ADR-001).
  - US5162 needs US5161, because it changes the same screen modules (ADR-004).
  - US5160 and US5161 depend only on the agreed contract, so they can be built in parallel.
- **Deployment:** there are no deployed environments. Each repo is released by its PR to `main` and a tag.

Two points are open.

## Q1. Who builds the shared contract examples, and is that a unit of its own?

User Stories ("Cross-Repo Check") asked for example JSON for each call, used by both repos' tests, so the API and the screen are checked against the same shapes. Contract Design will write the examples, but someone has to put them into the repos.

A. No separate unit. Contract Design keeps the examples in the parent record. US5160 copies the ones for its endpoints into `priorauth-api`'s tests, and US5161 copies them into `priorauth-web`'s tests. Each story's code plan names the files.
B. A small separate unit (kind `spec`) that adds the examples to both repos before US5160 and US5161 start. That is a fifth piece of work outside the one-story-one-unit rule.
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Q2. What are the units called?

Unit names become the construction folder names. Story branches are `f1220/us<id>-<word>` (team practice), using the same word in each repo the story touches.

A. Unit names and branch words:

   | Unit | Name | Branch |
   |---|---|---|
   | U1 | `us5160-save-filter` | `f1220/us5160-save-filter` |
   | U2 | `us5161-restore-filter` | `f1220/us5161-restore-filter` |
   | U3 | `us5162-clear-filters` | `f1220/us5162-clear-filters` |
   | U4 | `us5163-filter-history` | `f1220/us5163-filter-history` |

B. Different words (please give them under Other)
C. Not yet decided
X. Other (please specify)

[Answer]: A.

## Consolidated Summary Confirmation

- Four units, one per Rally story: U1 `us5160-save-filter` (service, priorauth-api), U2 `us5161-restore-filter` (ui, priorauth-web), U3 `us5162-clear-filters` (ui, priorauth-web), U4 `us5163-filter-history` (service, priorauth-api); branches `f1220/<unit name>` (Q2)
- Dependencies: U4 on U1; U3 on U2; U1 and U2 on the agreed contract only, with no edge between them
- No separate contract unit: Contract Design keeps the example JSON in the parent record; each story copies the examples for the calls it builds or calls into its own repo's tests, named in its code plan (U1 the filter and tenants calls, U4 the history call, U2 the calls the screen makes) (Q1)
- Deployment: no environments; each repo released by its PR to `main` plus a tag

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
