---
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
{{< /compact-table >}}

Helix-inspired selection-first editing with familiar Vim motions.

## 26 bundled languages

{{< language-list >}}
Bash, C, C#, C++, CMake, CSS, Go, HTML, INI, Java, JavaScript, JSON,
Kotlin, Lua, Make, Markdown, Protocol Buffers, Python, Rust, SQL, Swift,
TOML, TSX, TypeScript, YAML, Zig
{{< /language-list >}}

No grammar downloads. Syntax-aware indentation: `editor.smart_newline: true`.

Install language servers separately and allow them per workspace with `:lsp-trust`.

[See it in action →](/screenshots/)
