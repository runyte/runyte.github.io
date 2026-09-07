---
title: Performance
description: Runyte, Neovim, and Helix editing-readiness benchmarks, plus Runyte session, quit, and idle results.
---

# Measured performance

AMD Ryzen AI 9 365 / Linux. Timings are medians in milliseconds; lower is better.

## Ready to edit

Time from launch to a visible edit, with warm caches and LSP disabled.
Initial syntax parsing may still be running.

**7 September 2026 · Runyte 0.2.0 development build (`c56eb96`) · Neovim 0.12.5 · Helix 25.07.1**

{{< compact-table label="Readiness to edit, median milliseconds" class="readiness-table" >}}
| File | Lines | Neovim | Helix | Runyte |
| --- | ---: | ---: | ---: | ---: |
| Text | 500 | 20.9 | 29.6 | **15.3** |
| Text | 5,000 | 20.8 | 30.5 | **16.6** |
| Text | 50,000 | 23.5 | 34.5 | **23.4** |
| Lua | 500 | 38.8 | 38.5 | **17.4** |
| Lua | 5,000 | 29.3 | 52.7 | **17.6** |
| Lua | 50,000 | 29.7 | 297.6 | **22.3** |
{{< /compact-table >}}

[Detailed results and methodology on GitHub](https://github.com/runyte/runyte/blob/c56eb96/context/reference/startup-performance.md#2026-09-07--document-readiness-before-initial-syntax)

## Persistent sessions

Runyte time to visible output.

**6 September 2026 · development build based on `9750cd0` plus session navigation**

{{< compact-table label="Persistent session timing, median milliseconds" >}}
| Scenario | Cold start | Warm attach |
| --- | ---: | ---: |
| One session | 32.59 | **5.22** |
| Three sessions | 33.32 | **6.13** |
| Three sessions, strip hidden | 33.48 | **6.37** |
| Three sessions, another terminal producing output | 33.20 | **6.55** |
{{< /compact-table >}}

[Session results and methodology on GitHub](https://github.com/runyte/runyte/blob/main/context/reference/startup-performance.md#2026-09-06--persistent-session-navigation)

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

[Quit and idle results and methodology on GitHub](https://github.com/runyte/runyte/blob/c56eb96/context/reference/startup-performance.md#quit-during-initial-parsing)

[All benchmark harnesses](https://github.com/runyte/runyte/blob/main/benchmarks/README.md) ·
[Finder vs. fzf](https://github.com/runyte/runyte/blob/main/context/reference/fuzzy-matching.md)
