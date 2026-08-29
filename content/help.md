---
title: Help
description: A short guide to Runyte's modal editor, command discovery, workspaces, file explorer, terminals, and Git tools.
---

# Help

Runyte is a terminal workspace for software development, built around a modal
text editor. Normal mode is for selecting and navigating; Insert mode is for
typing. Select what you want to change first, then apply an action.
If that model is new to you, start with `:tutorial`—it opens a guided, hands-on
introduction inside the editor.

## Discover commands as you work

You do not need to memorize the interface before using it. Starting a command
family such as `Space`, `g`, `z`, `m`, or `Ctrl-w` opens a hint popup with the
available continuations and their descriptions. The `:` command palette is
searchable and uses the same command registry.

- `Space ?` opens contextual help for the current buffer type.
- `:help` opens the general Runyte manual.
- `:help <topic>` jumps to a topic such as `git`, `search`, `mouse`, or `lsp`.
- `:tutorial` opens the interactive introduction.

## Standalone and persistent workspaces

Runyte starts in **standalone mode** by default: the current process owns the
editor workspace. In optional **persistent mode**, a local host keeps unsaved
buffers, editor state, language servers, and terminal processes alive while
the TUI client is detached.

```sh
runyte --persistent
runyte --session-list
```

Integrated terminal panes act as a workspace-scoped terminal multiplexer. You
can split the interface, run shells or full-screen terminal applications, and
review terminal history without stopping the child process.

## Files and Git

Open a directory with `runyte .` to use the editable file explorer. Rename,
move, copy, create, and delete entries with normal editor commands, then review
an explicit filesystem plan before Runyte changes anything on disk.

The built-in Git interface covers status, diffs, staging, commits, branches,
history, blame, stashes, and worktrees. Worktrees pair especially well with
integrated terminals and coding agents: each task can have an isolated working
directory while staying inside the same interface.

For the complete reference, see the
[Runyte user guide](https://github.com/runyte/runyte/blob/main/docs/user-guide.md).
