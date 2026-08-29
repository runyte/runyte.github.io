---
title: Performance
description: Startup performance measurements for Runyte, Neovim, and Helix across text and Lua files of three sizes.
wide: true
---

# Performance

Startup time in milliseconds, shown as **first output / settled frame**. Each
value is the median of 10 runs in a 120×40 pseudo-terminal with an empty editor
configuration. The fastest value in each fixture and measurement category is
highlighted in green; ties are highlighted equally.

| Fixture | Size | Neovim first / ready | Helix first / ready | Runyte first / ready |
| --- | --- | ---: | ---: | ---: |
| `short.txt` | 17 kB | 6 / 18 ms | 17 / 18 ms | **5** / **6** ms |
| `medium.txt` | 171 kB | **6** / 17 ms | 19 / 20 ms | **6** / **7** ms |
| `long.txt` | 1.7 MB | **6** / 22 ms | 22 / 23 ms | 16 / **17** ms |
| `short.lua` | 17 kB | **6** / 30 ms | 22 / 23 ms | 10 / **12** ms |
| `medium.lua` | 171 kB | **6** / 46 ms | 48 / 50 ms | 28 / **29** ms |
| `long.lua` | 1.7 MB | **6** / 175 ms | 214 / 215 ms | 150 / **152** ms |
