---
title: Performance
description: Startup performance measurements for Runyte, Neovim, and Helix across text and Lua files of three sizes.
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

{{< benchmark-table >}}
<colgroup>
  <col class="benchmark-table__fixture">
  <col class="benchmark-table__loc">
  <col class="benchmark-table__size">
  <col span="6" class="benchmark-table__result">
</colgroup>
<thead>
  <tr>
    <th rowspan="2" scope="col">Fixture</th>
    <th rowspan="2" scope="col">LOC</th>
    <th rowspan="2" scope="col">Size</th>
    <th colspan="2" scope="colgroup">Neovim</th>
    <th colspan="2" scope="colgroup">Helix</th>
    <th colspan="2" scope="colgroup">Runyte</th>
  </tr>
  <tr class="benchmark-table__metrics">
    <th scope="col">First</th>
    <th scope="col">Ready</th>
    <th scope="col">First</th>
    <th scope="col">Ready</th>
    <th scope="col">First</th>
    <th scope="col">Ready</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><code>short.txt</code></td><td>0.5k</td><td>17 kB</td>
    <td>{{< result rank="middle" >}}6{{< /result >}}</td><td>{{< result rank="slowest" >}}18{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}17{{< /result >}}</td><td>{{< result rank="slowest" >}}18{{< /result >}}</td>
    <td>{{< result rank="fastest" >}}5{{< /result >}}</td><td>{{< result rank="fastest" >}}6{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>medium.txt</code></td><td>5k</td><td>171 kB</td>
    <td>{{< result rank="fastest" >}}6{{< /result >}}</td><td>{{< result rank="middle" >}}17{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}19{{< /result >}}</td><td>{{< result rank="slowest" >}}20{{< /result >}}</td>
    <td>{{< result rank="fastest" >}}6{{< /result >}}</td><td>{{< result rank="fastest" >}}7{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>long.txt</code></td><td>50k</td><td>1.7 MB</td>
    <td>{{< result rank="fastest" >}}6{{< /result >}}</td><td>{{< result rank="middle" >}}22{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}22{{< /result >}}</td><td>{{< result rank="slowest" >}}23{{< /result >}}</td>
    <td>{{< result rank="middle" >}}16{{< /result >}}</td><td>{{< result rank="fastest" >}}17{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>short.lua</code></td><td>0.5k</td><td>17 kB</td>
    <td>{{< result rank="fastest" >}}6{{< /result >}}</td><td>{{< result rank="slowest" >}}30{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}22{{< /result >}}</td><td>{{< result rank="middle" >}}23{{< /result >}}</td>
    <td>{{< result rank="middle" >}}10{{< /result >}}</td><td>{{< result rank="fastest" >}}12{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>medium.lua</code></td><td>5k</td><td>171 kB</td>
    <td>{{< result rank="fastest" >}}6{{< /result >}}</td><td>{{< result rank="middle" >}}46{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}48{{< /result >}}</td><td>{{< result rank="slowest" >}}50{{< /result >}}</td>
    <td>{{< result rank="middle" >}}28{{< /result >}}</td><td>{{< result rank="fastest" >}}29{{< /result >}}</td>
  </tr>
  <tr>
    <td><code>long.lua</code></td><td>50k</td><td>1.7 MB</td>
    <td>{{< result rank="fastest" >}}6{{< /result >}}</td><td>{{< result rank="middle" >}}175{{< /result >}}</td>
    <td>{{< result rank="slowest" >}}214{{< /result >}}</td><td>{{< result rank="slowest" >}}215{{< /result >}}</td>
    <td>{{< result rank="middle" >}}150{{< /result >}}</td><td>{{< result rank="fastest" >}}152{{< /result >}}</td>
  </tr>
</tbody>
{{< /benchmark-table >}}
