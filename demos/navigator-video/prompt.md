Add task completion to the store.

| Item | Where | Behaviour |
| --- | --- | --- |
| `Store::complete(title)` | `src/store.rs` | Marks the first open task with that title as done |
| Test | `src/store.rs` | A completed task no longer appears in `pending()` |

Run `cargo test` when you are done.
Reply in one line naming the file you changed.
