---
seoTitle: "Runyte Plugins — Extend Your Terminal Editor"
title: Plugins
description: Extend Runyte with plugins written in any language. Add commands, views, editing tools, and background work.
---

# Plugins

Plugins in Runyte are separate programs that run alongside Runyte and share
its panes and keybindings.
They do not modify how Runyte works, but rather extend its functionality.

Plugins can be written in any programming language, because they communicate
with Runyte in JSON over stdin and stdout.

The plugin ecosystem is still nascent. We have several
[example plugins](https://github.com/runyte/runyte/tree/main/docs/plugins) in the
GitHub repo and two official plugins in development:

- [`ru-time`](https://github.com/runyte/ru-time) for task lists and time tracking
- [`ru-dbviewer`](https://github.com/runyte/ru-dbviewer) for browsing SQLite and PostgreSQL databases

## What plugins can add

- Commands and keybindings, with discoverable hints.
- Native lists, prompts, menus, and documents.
- Undoable edits to selections.
- Remote files and background jobs.

## Write a plugin

Plugin commands start with `::`. The stable contract starts with Runyte 0.3.0.

Start with the [installation and protocol guide](https://github.com/runyte/runyte/blob/main/docs/plugins.md)
or the [application authoring guide](https://github.com/runyte/runyte/blob/main/docs/plugins/authoring.md).

Examples include text transforms, task lists, file managers, and database tools.
[Browse the examples](https://github.com/runyte/runyte/tree/main/docs/plugins).

## Manage plugins

| Command | Action |
| --- | --- |
| `:plugins` | Inspect plugins, permissions, and diagnostics |
| `:plugin-stop <id>` | Stop a plugin |
| `:plugin-restart <id>` | Restart it |

Plugins run with your user permissions. Their capabilities control editor
access, but do not sandbox the program. Enable programs you trust.
