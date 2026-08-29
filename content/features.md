---
title: Features
description: The editor, file, terminal, Git, language, and persistent-session workflows integrated into Runyte.
---

# Features

Runyte brings the core software-development workflow into one terminal
workspace. These are not separate plugins with separate interaction models:
the editor, files, terminals, Git, and language tools share the same panes,
commands, workspace, and visual language.

| Area | Built into Runyte | How it works as one environment |
| --- | --- | --- |
| **Modal editor** | Selection-first editing, multiple selections, counts, named registers, macros, transactional undo, jumplists, structural text objects, folds, and Unicode-aware wrapping. | The same selection and command model extends into explorers, generated views, and terminal review. |
| **File management** | An editable directory explorer, project finder, fuzzy file and content search, buffer picker, and filesystem operations with trash support. | Rename, move, copy, create, and delete with normal editor commands, then review one explicit plan before disk changes. |
| **Terminal sessions** | Workspace-scoped terminal multiplexing for shells, full-screen TUIs, development tools, and coding agents, with scrollback and review mode. | Terminals live in ordinary splits beside files. Review uses editor motions, search, selection, and copy while the child process keeps running. |
| **Git workflows** | Status, gutter marks, diffs, staging, commits, pull and push, branches, worktrees, history, blame, and stashes. | Git data opens as native Runyte views rather than shell output. Worktrees and terminals create isolated workspaces for parallel tasks. |
| **Language tooling** | Statically linked Tree-sitter highlighting for 18 languages plus asynchronous LSP diagnostics, completion, navigation, symbols, rename, actions, and formatting. | Syntax and language servers belong to the workspace and remain responsive while editing, searching, using Git, or running terminals. |
| **Workspace sessions** | Standalone operation by default and optional persistent sessions with detachable clients. | Persistent mode keeps unsaved buffers, selections, registers, Git state, language servers, and terminal processes alive together while the TUI is detached. |

Run `:tutorial` for a guided tour, or open [Help](/help/) to learn how Runyte
exposes commands as you work.
