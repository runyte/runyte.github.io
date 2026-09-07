---
title: Performance
description: Recorded editing-readiness, session-attachment, quit, and idle measurements for Runyte.
---

# Measured performance

Recorded benchmarks, with versions and dates. Lower timings are better.

## Ready to edit

Launch → insert one space → see the edit. The saved whole file is verified afterward.

**5 September 2026 · Runyte 0.1.10 · Neovim 0.12.4 · Helix 25.07.1**

{{< compact-table label="Readiness to edit, median milliseconds" >}}
| File | Lines | Neovim | Helix | Runyte |
| --- | ---: | ---: | ---: | ---: |
| Text | 500 | 22.5 | 29.7 | **15.1** |
| Text | 5,000 | 23.3 | 31.6 | **15.5** |
| Text | 50,000 | 25.3 | 31.1 | **23.0** |
| Lua | 500 | 41.0 | 34.7 | **21.2** |
| Lua | 5,000 | 32.0 | 53.1 | **32.7** |
| Lua | 50,000 | 32.2 | 295.7 | **157.5** |
{{< /compact-table >}}

Milliseconds, median of 10 warm-cache launches. AMD Ryzen AI 9 365, Linux,
120×40 terminal, isolated configuration. One edit near the file start;
background parsing may still differ between editors.

Neovim is much faster to the first visible edit on the large Lua file because
it can display the edit before syntax parsing finishes, while this Runyte build
waits for the initial parse; plain text skips syntax parsing, so timings are closer.

[Ranges, samples, and methodology](https://github.com/runyte/runyte/blob/main/context/reference/startup-performance.md#2026-09-05--readiness-loading-and-syntax)

## Persistent sessions

**6 September 2026 · development build based on `9750cd0` plus session navigation**

{{< compact-table label="Persistent session timing, median milliseconds" >}}
| Scenario | Cold start | Warm attach |
| --- | ---: | ---: |
| One session | 32.59 | **5.22** |
| Three sessions | 33.32 | **6.13** |
| Three sessions, strip hidden | 33.48 | **6.37** |
| Three sessions, another terminal producing output | 33.20 | **6.55** |
{{< /compact-table >}}

Milliseconds, median of 3 runs on Ryzen AI 9 365 / Linux. Time to visible output;
this measures a different event from editing readiness. No screen writes during
the settled 16-second idle windows.

[Session benchmark details](https://github.com/runyte/runyte/blob/main/context/reference/startup-performance.md#2026-09-06--persistent-session-navigation)

## Quit and idle

**31 August 2026 · Runyte 0.1.6 · Neovim 0.12.4 · Helix 25.07.1**

{{< compact-table label="Historical quit and idle measurements" >}}
| Measurement | Neovim | Helix | Runyte |
| --- | ---: | ---: | ---: |
| Quit, fixture medians | 2–6 ms | 4–22 ms | **4–28 ms** |
| Idle CPU, median | 0.00% | 0.00% | **0.00%** |
| Idle screen writes | 0 | 0 | **0** |
{{< /compact-table >}}

Quit: six text/Lua fixtures, 10 runs each. Idle: five 10-second windows;
Runyte's CPU range was 0.00–0.10%.

[Full quit and idle results](https://github.com/runyte/runyte/blob/main/context/reference/startup-performance.md#2026-08-31)

These recorded builds predate some 0.2.0 changes. Values are machine-specific;
the tables are not measurements of the current release.

[All benchmark harnesses](https://github.com/runyte/runyte/blob/main/benchmarks/README.md) ·
[Finder vs. fzf](https://github.com/runyte/runyte/blob/main/context/reference/fuzzy-matching.md)
