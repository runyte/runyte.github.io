---
title: Performance
description: Recorded editing-readiness, session-attachment, quit, and idle measurements for Runyte.
---

# Measured performance

Recorded benchmarks, with versions and dates. Lower timings are better.

## Ready to edit

Launch → insert one space → see the edit. The saved whole file is verified afterward.

**7 September 2026 · Runyte 0.2.0 development build (`c56eb96`) · Neovim 0.12.5 · Helix 25.07.1**

{{< compact-table label="Readiness to edit, median milliseconds" >}}
| File | Lines | Neovim | Helix | Runyte |
| --- | ---: | ---: | ---: | ---: |
| Text | 500 | 20.9 | 29.6 | **15.3** |
| Text | 5,000 | 20.8 | 30.5 | **16.6** |
| Text | 50,000 | 23.5 | 34.5 | **23.4** |
| Lua | 500 | 38.8 | 38.5 | **17.4** |
| Lua | 5,000 | 29.3 | 52.7 | **17.6** |
| Lua | 50,000 | 29.7 | 297.6 | **22.3** |
{{< /compact-table >}}

Milliseconds, median of 10 warm-cache launches after one discarded warm-up.
AMD Ryzen AI 9 365, Linux, 120×40 terminal, isolated configuration with LSP
disabled. Editor order rotates; every readiness sample passes whole-file save
verification. One edit near the file start; syntax parsing may still be running.

Runyte now displays the loaded document and accepts edits while initial syntax
parsing runs in the background. Highlighting appears when a tree matching the
current text is ready. Reading, ordinary editing, undo/redo, and saving work
throughout; syntax commands under `Space x`, plus `mm` for matching brackets,
remain temporarily dimmed until a current tree is available.

For the 50,000-line Lua file, this reduced Runyte's readiness median from
**160.9 ms to 22.3 ms**, about seven times sooner. Neovim measured 29.7 ms in
the final comparison. Runyte's initial syntax parse still completes around
156.9 ms in separate instrumented launches: editing becomes available earlier
while parsing takes a similar time. Large plain-text readiness remains close
to the previous result (24.4 ms before, 23.4 ms after). These are measurements
of one fixture matrix on one machine, not universal editor rankings.

[Ranges, samples, before/after results, and methodology](https://github.com/runyte/runyte/blob/c56eb96/context/reference/startup-performance.md#2026-09-07--document-readiness-before-initial-syntax)

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

**7 September 2026 · Runyte 0.2.0 development build (`c56eb96`)**

{{< compact-table label="Runyte quit and idle measurements" >}}
| Measurement | Runyte |
| --- | ---: |
| Quit during initial parsing, 50,000-line Lua | **2.7 ms** |
| Quit after settling, 50,000-line text | **4 ms** |
| Quit after settling, 50,000-line Lua | **22 ms** |
| Idle CPU, median | **0.00%** |
| Idle screen writes | **0** |
{{< /compact-table >}}

Quit values are medians of 10 runs. Early quit sends `:q` immediately after
the first document frame and measures through successful process exit; it
takes 2.5–4.7 ms. A separate instrumented build confirmed that none of its ten
initial parses completed before exit. Settled Lua quit also measured 22 ms
before the change.

Idle: three independent 10-second windows with a Lua document open in a Git
repository. CPU ranged from 0.00–0.10% of one logical CPU; every window had zero
screen writes.

[Quit and idle details](https://github.com/runyte/runyte/blob/c56eb96/context/reference/startup-performance.md#quit-during-initial-parsing) ·
[Historical comparison with Neovim and Helix](https://github.com/runyte/runyte/blob/c56eb96/context/reference/startup-performance.md#2026-08-31)

Each table identifies the build and date measured. Values are machine-specific;
the latest readiness and quit results describe the development build above,
not a newly published release. Persistent-session results retain their earlier
build and measure time to visible output.

[All benchmark harnesses](https://github.com/runyte/runyte/blob/main/benchmarks/README.md) ·
[Finder vs. fzf](https://github.com/runyte/runyte/blob/main/context/reference/fuzzy-matching.md)
