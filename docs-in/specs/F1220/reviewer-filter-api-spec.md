# F1220 Remember my filter: API contract (draft for 2.8 Contract Design)

Owner: Meena Iyer (tech lead). Input to the parent intent; the approved contract is the parent's
`inception/contract-design/contract-summary.md`, not this file.

## PUT /reviewers/{reviewerId}/filter

Body: `{"tenant": "TX-01" | null, "overLimit": true | false}`. Saves the reviewer's last filter; 204.
An unknown tenant: 400, nothing saved, nothing audited.

## GET /reviewers/{reviewerId}/filter

The last saved filter, or `{}` when there is none (200). The screen calls it on load (US5161).

## GET /reviewers/{reviewerId}/filter/history

The reviewer's audit lines, newest first: `[{"at": "<UTC ISO time>", "tenant": ..., "overLimit": ...}]` (US5163).

- No database yet: one in-memory store behind one class, replaceable later.
- `reviewerId` is the reviewer's login name; this product has no sign-in yet, so the screen passes it as `?reviewer=`.
