---
title: Performance
description: Startup, quit, and idle measurements for Runyte, Neovim, and Helix across text and Lua files of three sizes.
---

# Performance

The benchmark opens generated documents at 500, 5,000, and 50,000 lines. Each
size is written twice with byte-identical content: the `.txt` file carries no
language for any editor, while the `.lua` file gives all three the same single
Tree-sitter Lua grammar.

Startup, quit, and idle cost are measured separately, because they answer
different questions and no editor leads all three. Startup and quit are
medians of 10 runs in a 120×40 pseudo-terminal with isolated configuration,
cache, and state directories. Idle is the median and range of five independent
ten-second windows, each using a fresh process. See the
[full benchmark methodology](https://github.com/runyte/runyte/blob/main/benchmarks/README.md)
for details.

Measured on 31 August 2026 with Neovim 0.12.4, Helix 25.07.1, and Runyte 0.1.6
on an AMD Ryzen AI 9 365 running Linux 7.1.9. Absolute values are
machine-specific and are not comparable against results taken on other
hardware. In each row the fastest value is highlighted in green, the
intermediate value in yellow, and the slowest in red. Ties are highlighted
equally.

## Startup

Startup is the time in milliseconds from immediately before the process
launches until a token from the first document line appears in the raw
terminal stream. It is one shared output event, not proof that the whole
screen has been presented, that input is accepted, or that highlighting and
background work have finished. An editor may emit that token before or after
it parses the document, so an earlier value means the document text reached
the terminal sooner — not that the editor completed more work.

{{< benchmark-table variant="fixtures" >}}
<colgroup>
  <col class="benchmark-table__fixture">
  <col class="benchmark-table__loc">
  <col class="benchmark-table__size">
  <col span="3" class="benchmark-table__result">
</colgroup>
<thead>
  <tr>
    <th scope="col">Fixture</th>
    <th scope="col">LOC</th>
    <th scope="col">Size</th>
    <th scope="col">Neovim</th>
    <th scope="col">Helix</th>
    <th scope="col">Runyte</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><code>short.txt</code></td><td>0.5k</td><td>17 kB</td>
    <td>{{< result rank="slowest" >}}19{{< /result >}}</td>
    <td>{{< result rank="middle" >}}17{{< /result >}}</td>
    <td>{{< result rank="fastest" >}}6{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>medium.txt</code></td><td>5k</td><td>171 kB</td>
    <td>{{< result rank="slowest" >}}21{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}21{{< /result >}}</td>
    <td>{{< result rank="fastest" >}}8{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>long.txt</code></td><td>50k</td><td>1.7 MB</td>
    <td>{{< result rank="slowest" >}}23{{< /result >}}</td>
    <td>{{< result rank="middle" >}}21{{< /result >}}</td>
    <td>{{< result rank="fastest" >}}15{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>short.lua</code></td><td>0.5k</td><td>17 kB</td>
    <td>{{< result rank="slowest" >}}33{{< /result >}}</td>
    <td>{{< result rank="middle" >}}27{{< /result >}}</td>
    <td>{{< result rank="fastest" >}}14{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>medium.lua</code></td><td>5k</td><td>171 kB</td>
    <td>{{< result rank="fastest" >}}27{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}48{{< /result >}}</td>
    <td>{{< result rank="middle" >}}28{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>long.lua</code></td><td>50k</td><td>1.7 MB</td>
    <td>{{< result rank="fastest" >}}28{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}215{{< /result >}}</td>
    <td>{{< result rank="middle" >}}176{{< /result >}}</td>
  </tr>
</tbody>
{{< /benchmark-table >}}

Runyte emits document content first on every fixture without a language and on
the smallest Lua file. On `medium.lua` the millisecond separating Neovim and
Runyte is within ordinary run variation. On `long.lua` Neovim emits document
text at 28 ms against Runyte's 176 ms: Runyte draws a stable
`Opening workspace…` presentation and then replaces it with a single complete
highlighted frame, so no document text is exposed in an unhighlighted or
reflowing intermediate state. That is a difference in output order, not
evidence that Neovim finished parsing 1.7 MB of Lua at 28 ms.

## Quit

Quit is the time in milliseconds from the final force-quit keystroke until the
process exits. Every editor receives the same `Esc` `:` `q` `!` `Enter`
sequence against the same unchanged document, so no editor-specific save or
persistence workflow is included.

{{< benchmark-table variant="fixtures" >}}
<colgroup>
  <col class="benchmark-table__fixture">
  <col class="benchmark-table__loc">
  <col class="benchmark-table__size">
  <col span="3" class="benchmark-table__result">
</colgroup>
<thead>
  <tr>
    <th scope="col">Fixture</th>
    <th scope="col">LOC</th>
    <th scope="col">Size</th>
    <th scope="col">Neovim</th>
    <th scope="col">Helix</th>
    <th scope="col">Runyte</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><code>short.txt</code></td><td>0.5k</td><td>17 kB</td>
    <td>{{< result rank="fastest" >}}2{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}4{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}4{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>medium.txt</code></td><td>5k</td><td>171 kB</td>
    <td>{{< result rank="fastest" >}}3{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}4{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}4{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>long.txt</code></td><td>50k</td><td>1.7 MB</td>
    <td>{{< result rank="fastest" >}}3{{< /result >}}</td>
    <td>{{< result rank="middle" >}}4{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}5{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>short.lua</code></td><td>0.5k</td><td>17 kB</td>
    <td>{{< result rank="fastest" >}}2{{< /result >}}</td>
    <td>{{< result rank="middle" >}}4{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}5{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>medium.lua</code></td><td>5k</td><td>171 kB</td>
    <td>{{< result rank="fastest" >}}2{{< /result >}}</td>
    <td>{{< result rank="middle" >}}7{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}8{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>long.lua</code></td><td>50k</td><td>1.7 MB</td>
    <td>{{< result rank="fastest" >}}6{{< /result >}}</td>
    <td>{{< result rank="middle" >}}22{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}28{{< /result >}}</td>
  </tr>
</tbody>
{{< /benchmark-table >}}

Neovim exits first in every row. The category is reported as measured rather
than dropped where Runyte does not lead.

## Idle

With `medium.lua` open in a Git repository and no input, CPU is sampled over
ten seconds across the editor and every process it spawned, alongside the
number of times it writes to the screen. Each cell is the median across the
five windows, with the observed range in parentheses.

{{< benchmark-table variant="idle" >}}
<colgroup>
  <col class="benchmark-table__editor">
  <col span="2" class="benchmark-table__idle">
</colgroup>
<thead>
  <tr>
    <th scope="col">Editor</th>
    <th scope="col">Idle CPU</th>
    <th scope="col">Screen writes</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Neovim</td><td>0.00 % (0.00–0.00)</td><td>0 (0–0)</td>
  </tr>
  <tr>
    <td>Helix</td><td>0.00 % (0.00–0.00)</td><td>0 (0–0)</td>
  </tr>
  <tr>
    <td>Runyte</td><td>0.00 % (0.00–0.10)</td><td>0 (0–0)</td>
  </tr>
</tbody>
{{< /benchmark-table >}}

All three editors are event-driven at rest. One of Runyte's five windows
rounded to 0.10 %; the work that remains scheduled is bounded and named — a
one-second maintenance wake and a two-second metadata reconciliation covering
filesystem events the operating system fails to deliver.
