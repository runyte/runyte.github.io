---
seoTitle: "Modal Editing, Terminals, Git and Project Search | Runyte"
title: Features
description: Selection-first editing, files, terminals, Git, language tools, and persistent sessions in one interface.
---

# One workspace. Familiar tools.

Shared panes, theme, commands, and clipboard.

{{< compact-table label="Runyte features" >}}
| Area | Built in |
| --- | --- |
| **Editor** | Multiple selections, macros, undo, structural selection |
| **Files** | Editable explorer with reviewed filesystem changes |
| **Search** | Finder for files and content; Navigator for open buffers and terminals |
| **Terminals** | Splits, scrollback, modal review, persistent processes |
| **Git** | Status, diffs, staging, commits, pull/push, branches, worktrees, blame, stashes |
| **Languages** | Bundled Tree-sitter highlighting and asynchronous LSP |
| **Sessions** | Clickable session strip, keyboard switching, detachable clients |
| **Interface** | Key hints, themes, settings, notifications, rendered Markdown |
| **Plugins** | [Any language](/plugins/): native commands, views, keys, background work |
{{< /compact-table >}}

Helix-inspired selection-first editing with familiar Vim motions.

## 32 bundled languages

{{< language-list >}}
Bash, C, C#, C++, CMake, CSS, Dockerfile, Elixir, Go, HCL/Terraform, HTML, INI,
Java, JavaScript, JSON, Kotlin, Lua, Make, Markdown, PHP, Protocol Buffers,
Python, Ruby, Rust, SQL, Swift, TOML, TSX, TypeScript, XML, YAML, Zig
{{< /language-list >}}

No grammar downloads. Enter indents by syntax and continues Markdown lists;
set `editor.smart_newline: false` to keep only the current indentation.
Indent with spaces or tabs: `editor.indent`.

Install language servers separately and allow them per workspace with `:lsp-trust`.

[See it in action →](/screenshots/)
