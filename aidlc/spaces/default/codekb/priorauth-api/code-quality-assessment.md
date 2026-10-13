# Code quality
Small, typed, records everywhere, constructor injection, no statics except the pending-status set. The controller is thin; the
store sorts once at load. Tests: unit (store) and one full-context MockMvc test. Nothing to refactor before this change.
Note for the change: date arithmetic belongs in its own package, not in the controller.
