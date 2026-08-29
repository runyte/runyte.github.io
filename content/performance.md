---
title: Performance
description: Reproducible measurements of Runyte's startup latency and idle cost, with fair comparisons against Neovim and Helix.
wide: true
---

# Performance

Runyte is designed to present a responsive workspace without doing unnecessary
work in the background. The measurements below are snapshots from a repeatable
benchmark harness, recorded on August 29, 2026.

## Startup benchmark

The benchmark opens a generated 1.0 MB Lua document containing 30,000 lines.
All three editors parse the entire file with a single Tree-sitter Lua grammar,
so this row compares equivalent work. Each value is the median of five runs in
a 120×40 pseudo-terminal with an empty editor configuration.

| Editor | Version | First output | Settled frame |
| --- | --- | ---: | ---: |
| Neovim | 0.12.4 | 6 ms | 136 ms |
| Helix | 25.07.1 | 134 ms | 135 ms |
| **Runyte** | **0.1.3** | **94 ms** | **95 ms** |

Runyte reached a settled frame in 95 ms, about 30% sooner than Helix and
Neovim in this test. First output and readiness are deliberately reported
separately: Neovim starts writing earlier, while Runyte's first frame appears
almost fully settled.

## Idle behavior

Runyte uses filesystem events and a short debounce instead of periodically
polling Git repositories. With LSP disabled to isolate Git-related work, an
unchanged workspace produced no screen writes and launched no Git subprocesses
during either measurement window.

| Workspace | Window | Idle CPU | Screen writes | Git subprocesses |
| --- | ---: | ---: | ---: | ---: |
| One visible tracked file | 10 s | 0.40% | 0 | 0 |
| 100 open repository files, one visible | 5 s | 0.80% | 0 | 0 |

Each workspace performed one initial Git snapshot before the measurement
window. Hidden buffers did not add background Git work.

## Test environment and caveats

These results were recorded on Linux 7.1.9 with an AMD Ryzen AI 9 365, 20
threads, 27 GB of memory, and btrfs storage. Absolute timings are
machine-specific, and cross-editor comparisons are meaningful only when every
editor performs the same work. Differences below roughly 10% should not be
treated as significant for this result set.

The harness, fixture design, historical results, and detailed interpretation
are available in the repository:

- [Benchmark methodology](https://github.com/runyte/runyte/blob/main/benchmarks/README.md)
- [Full performance record](https://github.com/runyte/runyte/blob/main/context/reference/startup-performance.md)
