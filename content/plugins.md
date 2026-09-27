---
seoTitle: "Runyte Plugins — Extend Your Terminal Editor"
title: Plugins
description: Extend Runyte with plugins written in any language. Add commands, views, editing tools, and background work.
---

# Plugins

A plugin is a separate program you enable. It talks to Runyte in JSON over
stdin and stdout. Write one in any language.

Plugin commands start with `::`. The stable contract starts with Runyte 0.3.0.

## Official plugins

| Plugin | What it does |
| --- | --- |
| [ru-time](https://github.com/runyte/ru-time) | Task lists, time tracking, and task notes |
| [ru-dbviewer](https://github.com/runyte/ru-dbviewer) | Browse SQLite and PostgreSQL; run SQL from editor buffers |

Both are in development. See each repository for setup.

## What plugins can add

- Commands and keybindings, with discoverable hints.
- Native lists, prompts, menus, and documents.
- Undoable edits to selections.
- Remote files and background jobs.

## Write a plugin

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
