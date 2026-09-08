# Build a small Rust focus planner

Write a dependency-free Rust command-line program.

| Task | Minutes | Priority | Scheduling constraint |
| --- | --- | --- | --- |
| Fix keyboard navigation | 15 | 3 | A small usability improvement that fits into a short working session. |
| Review a pull request | 25 | 5 | Unblock a teammate before starting lower-priority maintenance work. |
| Refactor the parser | 60 | 4 | Requires a longer uninterrupted session; never recommend it when the budget is too small. |

Read available minutes from the first CLI argument, defaulting to 25.
Recommend the highest-priority task that fits; break ties by shorter duration.
Handle invalid input and the case where no task fits.
Name the selection function `focus`. Keep the program under 35 lines.
Return only complete Rust source, without Markdown fences or explanation.
Do not use tools or edit files.
