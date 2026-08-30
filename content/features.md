---
title: Features
description: The editor, file, terminal, Git, language, and persistent-session workflows integrated into Runyte.
---

# Features

Runyte brings the core software-development workflow into one terminal
workspace. These are not separate plugins with separate interaction models:
the editor, files, terminals, Git, and language tools share the same panes,
commands, workspace, and visual language.

{{< features-table >}}
<colgroup>
  <col class="features-table__area">
  <col class="features-table__built-in">
  <col class="features-table__environment">
</colgroup>
<thead>
  <tr>
    <th scope="col">Area</th>
    <th scope="col">Built in Runyte</th>
    <th scope="col">How it works as one environment</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><strong>Modal editor</strong></td>
    <td>Selection-first, multicursor, Vim and Helix bindings</td>
    <td class="features-table__shared" rowspan="6">
      <ul>
        <li>Same keybindings</li>
        <li>Shared clipboard</li>
        <li>Fuzzy-search anything</li>
        <li>Jump anywhere</li>
        <li>Switch between worktrees</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><strong>File management</strong></td>
    <td>Editable directory explorer</td>
  </tr>
  <tr>
    <td><strong>Terminal sessions</strong></td>
    <td>Multiplexing, scrollback</td>
  </tr>
  <tr>
    <td><strong>Git</strong></td>
    <td>Status, diffs, staging, commits, pull, push, branches, worktrees, blame, stashes</td>
  </tr>
  <tr>
    <td><strong>Language</strong></td>
    <td>Tree-sitter for 18 languages, asynchronous LSP</td>
  </tr>
  <tr>
    <td><strong>Sessions</strong></td>
    <td>Optional client–server mode, detachable clients</td>
  </tr>
</tbody>
{{< /features-table >}}

Run `:tutorial` for a guided tour, or open [Help](/help/) to learn how Runyte
exposes commands as you work.
