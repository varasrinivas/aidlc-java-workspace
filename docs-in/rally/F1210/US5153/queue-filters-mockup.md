# US5153 Filter controls: mockup (from the design review, 2 Nov 2026)

Attached to US5153 in Rally by Divya Pillai. Text version of the sketch, so AI-DLC can read it.

```
+---------------------------------------------------------------+
| Pending requests                                     12 shown |
| Tenant: [ All tenants  v ]    [x] Over limit only             |
+---------------------------------------------------------------+
| PA-10231  TX-01  MRI lumbar spine      7 bd  OVER 5           |
| PA-10270  NM-02  Knee arthroscopy      6 bd  OVER 5           |
| ...                                                           |
+---------------------------------------------------------------+
```

- The count ("12 shown") is the length of the list the API returned, never a separate call.
- The tenant list comes from the rows of the unfiltered list; "All tenants" sends no `tenant`.
- The switch sends `overLimit=true` when on and nothing when off.
- The last choice is kept in the browser for the next visit (out of scope: US5131, a later feature).
