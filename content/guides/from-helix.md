---
title: Move from Helix to Runyte
seoTitle: Moving from Helix to Runyte — Editing and Key Differences
description: Learn what carries over from Helix to Runyte and what changes in search, macros, selections, integrated terminals, and persistent workspaces.
---

# Moving from Helix to Runyte

Runyte is a modal terminal editor inspired by Helix's selection-first model.
It combines editing with integrated terminals, Git tools, project search, and
optional persistent workspaces. Familiar motions and selection commands carry
over, but Runyte deliberately changes several bindings and behaviors.

## Start with familiar editing

Use `h/j/k/l` to move, `w/b/e` for word motions, and `v` to enter Select mode.
`d` deletes a selection, `c` changes it, and `i` enters Insert mode. Press `Esc`
to return to Normal mode. Commands apply to multiple selections.

Run `:tutorial` for an interactive introduction. `Space ?` opens contextual
help; starting a command prefix displays its next keys.

## Search selects all matches

Runyte's `s` searches for a case-insensitive literal, while `/` accepts a regular
expression. Both select every match in the search region. If a selection spans
two or more characters, the search stays within the selected regions; otherwise
it searches the buffer.

For example, with a single caret in a buffer, press `s`, type `old_name`, and
press Enter. Every occurrence is selected. Press `c`, type `new_name`, then
press `Esc` to replace them together. Runyte's `s` treats punctuation literally,
so `foo(` can be searched without escaping it.

Press `n` or `N` after a search to reduce the selection to the next or previous
match. `*` selects occurrences of the current word or selection as a
case-sensitive literal.

| Task | Runyte default |
| --- | --- |
| Literal search | `s` |
| Regular-expression search | `/` |
| Literal search across the workspace | `Space / s` |
| Regex search across the workspace | `Space / /` |
| Find files, buffers, or terminals | `Space f`; `Tab` switches names and contents |
| Render a Markdown buffer as a page | `?` |

`?` is not reverse search in Runyte. In a Markdown buffer it switches between
source and a formatted page.

## Macros live under Space m

`q` and `Q` are unbound in ordinary editable buffers. Use `Space m m` to start
recording the default macro, repeat those keys to stop, and use `Space m r`
to replay. `Space m l` lists recorded macros. Named recordings and replay use
`Space m M` and `Space m R`, followed by a register.

## Check selection and paste behavior

Yanking with `y` collapses each selection to a caret on the last copied
character. `p` at a caret pastes after it; with text still selected, `p`
replaces that selection. `P` pastes before the selection without replacing it.

Split selections into carets at line ends with `Space s e`, or at line starts
with `Space s b`. These produce carets rather than one selected range per line.
Selection filtering uses `Space s k` to keep regex matches and `Space s r`
to remove them.

## Add terminals and persistent projects

`Ctrl-w t` opens a terminal in the active pane. `Ctrl-w h/j/k/l` moves between
panes even while typing into a terminal; `Ctrl-\` leaves terminal input and
`i` resumes it. `Space n` opens the Navigator from editor modes, and `Ctrl-w n`
also works in Terminal Insert.

Start with `runyte --persistent` to keep your workspace running after `:detach`.
See [persistent terminal workspaces](/guides/persistent-workspaces/) and
[using coding agents](/guides/coding-agents/) for complete examples.

The [user guide](/docs/user-guide/#key-bindings) documents the current defaults.
The [detailed Helix keymap comparison](https://github.com/runyte/runyte/blob/main/context/reference/helix-keymap-v1.md)
records implemented commands, deviations, and unsupported behavior.
