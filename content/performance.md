---
title: Performance
description: Startup performance measurements for Runyte, Neovim, and Helix across text and Lua files of three sizes.
wide: true
---

# Performance

The benchmark opens generated documents at 500, 5,000, and 50,000 lines. Each
size is written twice with byte-identical content: the `.txt` file measures
reading and drawing without language processing, while the `.lua` file makes
all three editors parse the same document with a single Tree-sitter Lua grammar.

Startup time is shown in milliseconds as **first output / settled frame**. The
first value records the first byte written to the terminal; the second records
when drawing goes quiet. Each result is the median of 10 runs in a 120×40
pseudo-terminal with an empty editor configuration. See the
[full benchmark methodology](https://github.com/runyte/runyte/blob/main/benchmarks/README.md)
for details.

The fastest value in each fixture and measurement category is highlighted in
green, the intermediate value in yellow, and the slowest in red. Ties are
highlighted equally.

| Fixture | LOC | Size | Neovim first / ready | Helix first / ready | Runyte first / ready |
| --- | ---: | --- | ---: | ---: | ---: |
| `short.txt` | 500 | 17 kB | {{< result rank="middle" >}}6{{< /result >}} / {{< result rank="slowest" >}}18{{< /result >}} ms | {{< result rank="slowest" >}}17{{< /result >}} / {{< result rank="slowest" >}}18{{< /result >}} ms | {{< result rank="fastest" >}}5{{< /result >}} / {{< result rank="fastest" >}}6{{< /result >}} ms |
| `medium.txt` | 5,000 | 171 kB | {{< result rank="fastest" >}}6{{< /result >}} / {{< result rank="middle" >}}17{{< /result >}} ms | {{< result rank="slowest" >}}19{{< /result >}} / {{< result rank="slowest" >}}20{{< /result >}} ms | {{< result rank="fastest" >}}6{{< /result >}} / {{< result rank="fastest" >}}7{{< /result >}} ms |
| `long.txt` | 50,000 | 1.7 MB | {{< result rank="fastest" >}}6{{< /result >}} / {{< result rank="middle" >}}22{{< /result >}} ms | {{< result rank="slowest" >}}22{{< /result >}} / {{< result rank="slowest" >}}23{{< /result >}} ms | {{< result rank="middle" >}}16{{< /result >}} / {{< result rank="fastest" >}}17{{< /result >}} ms |
| `short.lua` | 500 | 17 kB | {{< result rank="fastest" >}}6{{< /result >}} / {{< result rank="slowest" >}}30{{< /result >}} ms | {{< result rank="slowest" >}}22{{< /result >}} / {{< result rank="middle" >}}23{{< /result >}} ms | {{< result rank="middle" >}}10{{< /result >}} / {{< result rank="fastest" >}}12{{< /result >}} ms |
| `medium.lua` | 5,000 | 171 kB | {{< result rank="fastest" >}}6{{< /result >}} / {{< result rank="middle" >}}46{{< /result >}} ms | {{< result rank="slowest" >}}48{{< /result >}} / {{< result rank="slowest" >}}50{{< /result >}} ms | {{< result rank="middle" >}}28{{< /result >}} / {{< result rank="fastest" >}}29{{< /result >}} ms |
| `long.lua` | 50,000 | 1.7 MB | {{< result rank="fastest" >}}6{{< /result >}} / {{< result rank="middle" >}}175{{< /result >}} ms | {{< result rank="slowest" >}}214{{< /result >}} / {{< result rank="slowest" >}}215{{< /result >}} ms | {{< result rank="middle" >}}150{{< /result >}} / {{< result rank="fastest" >}}152{{< /result >}} ms |
