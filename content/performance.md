---
seoTitle: "Runyte Performance — Terminal Editor Benchmarks"
title: Performance
description: Runyte, Neovim, and Helix editing-readiness benchmarks, plus Runyte session, quit, and idle results.
---

# Measured performance

AMD Ryzen AI 9 365 / Linux. Timings are medians in milliseconds; lower is better.

## Ready to edit

These measurements compare editing readiness with isolated configurations and
LSP disabled. They do not compare equivalent feature setups: Runyte includes
integrated terminals, Git workflows, and persistent sessions, while other editors
provide different combinations of built-in features and plugins. Results do not
predict performance with your configuration.

Time from launch to a visible edit, with warm caches and LSP disabled.
Initial syntax parsing may still be running. Ten measured launches per cell
follow one warm-up; every sample passes whole-file save verification.

**30 September 2026 · Runyte v0.3.5 (`b937570`) · Neovim 0.12.5 · Helix 25.07.1**

{{< compact-table label="Readiness to edit, median milliseconds" class="readiness-table" >}}
| File | Lines | Neovim | Helix | Runyte |
| --- | ---: | ---: | ---: | ---: |
| Text | 500 | 20.9 | 32.2 | **18.8** |
| Text | 5,000 | 20.9 | 32.7 | **20.4** |
| Text | 50,000 | **22.6** | 33.0 | 26.9 |
| Text | 500,000 | **38.6** | 45.9 | 88.0 |
| Lua | 500 | 42.3 | 39.1 | **20.6** |
| Lua | 5,000 | 31.7 | 63.7 | **21.7** |
| Lua | 50,000 | 31.3 | 349.0 | **27.9** |
| Lua | 500,000 | **45.7** | 548.8 | 102.5 |
{{< /compact-table >}}

[Detailed results and methodology on GitHub](https://github.com/runyte/runyte/blob/main/context/reference/startup-performance.md#2026-09-30--runyte-035)

## Persistent sessions

Runyte time to visible output, median of three samples per scenario.

**30 September 2026 · Runyte v0.3.5 (`b937570`)**

{{< compact-table label="Persistent session timing, median milliseconds" >}}
| Scenario | Cold start | Warm attach |
| --- | ---: | ---: |
| One session | 34.23 | **6.12** |
| Three sessions | 33.26 | **6.80** |
| Three sessions, strip hidden | 34.04 | **6.27** |
| Three sessions, another terminal producing output | 33.43 | **6.70** |
{{< /compact-table >}}

[Session results and methodology on GitHub](https://github.com/runyte/runyte/blob/main/context/reference/startup-performance.md#2026-09-30--runyte-035)

## Quit and idle

Quit medians use ten launches. Idle uses five ten-second windows with a
5,000-line Lua file open in a Git repository.

**30 September 2026 · Runyte v0.3.5 (`b937570`)**

{{< compact-table label="Runyte quit and idle measurements" >}}
| Measurement | Runyte |
| --- | ---: |
| Quit immediately after first document frame, 50,000-line Lua | **4.9 ms** |
| Quit after settling, 50,000-line text | **4 ms** |
| Quit after settling, 50,000-line Lua | **22 ms** |
| Idle CPU, median | **0.00%** |
| Idle screen writes | **0** |
{{< /compact-table >}}

[Quit and idle results and methodology on GitHub](https://github.com/runyte/runyte/blob/main/context/reference/startup-performance.md#2026-09-30--runyte-035)

[All benchmark harnesses](https://github.com/runyte/runyte/blob/main/benchmarks/README.md) ·
[Finder vs. fzf](https://github.com/runyte/runyte/blob/main/context/reference/fuzzy-matching.md)
