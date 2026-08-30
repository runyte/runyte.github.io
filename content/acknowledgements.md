---
title: Acknowledgements
description: The projects Runyte is built on, from Helix and Tree-sitter to Ratatui, Crossterm, and Ropey.
---

# Acknowledgements

Runyte is a small project standing on a lot of other people's work. These are
the projects it depends on most directly.

## Helix

Runyte's selection-first editing model and much of its keymap language come
from [Helix](https://helix-editor.com/), though common motions also have
Vim-style aliases. The
[keymap register](https://github.com/runyte/runyte/blob/main/context/reference/helix-keymap-v1.md)
records where the two deliberately differ, most of all in search and macros.

Syntax highlighting is built on
[tree-house](https://github.com/helix-editor/tree-house), the Helix project's
tree-sitter highlighter and bindings. It provides the highlighter, injected
syntax layers, tree cursors, and query iteration behind every highlighted
buffer, and it is licensed under the MPL-2.0, as Runyte is.

## Tree-sitter and the grammar authors

The language layer rests on [Tree-sitter](https://tree-sitter.github.io/) and
on the 26 grammar crates Runyte statically links, together with the query
material they ship. Their authors, revisions, and licenses are listed in
[third-party notices](https://github.com/runyte/runyte/blob/main/THIRD_PARTY_NOTICES.md).

## Ratatui, Crossterm, and Ropey

The interface is drawn with [Ratatui](https://ratatui.rs/) over
[Crossterm](https://github.com/crossterm-rs/crossterm), which also carries key
and mouse input and the terminal lifecycle. Every buffer is a
[Ropey](https://github.com/cessen/ropey) rope, so every edit is a transaction
over one.

## Theme palettes

Runyte's built-in themes adapt palettes from GitHub's Primer, Base16 Default
Dark, Gruvbox, Everforest, Catppuccin, Nightfox, and Zenbones. Each palette is
credited with its author, upstream revision, and license in
[third-party notices](https://github.com/runyte/runyte/blob/main/THIRD_PARTY_NOTICES.md),
and the license texts travel with the repository.

## Design influences

The editable directory explorer follows the design
[Oil.nvim](https://github.com/stevearc/oil.nvim) established: a directory as an
ordinary buffer you edit and then apply. The `g w` jump labels take their
visual and narrowing model from
[hop.nvim](https://github.com/smoka7/hop.nvim), and the shell-directory handoff
on exit works the way [Yazi](https://yazi-rs.github.io/) does it. Vim shaped
the motion aliases, and tmux and Zellij shaped what a terminal session is
expected to do.

See
[third-party notices](https://github.com/runyte/runyte/blob/main/THIRD_PARTY_NOTICES.md)
for the full list of acknowledgements and the licenses they carry.
