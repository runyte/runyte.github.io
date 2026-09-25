---
seoTitle: "Runyte Plugins — Extend Your Terminal Editor"
title: Plugins
description: Extend Runyte with plugins written in any programming language, with native commands, views, key bindings, and background work.
---

# Extend Runyte in any language.

A plugin is a program you enable. It runs as a separate process and talks to
Runyte in newline-delimited JSON over stdin/stdout. Python, JavaScript, Rust,
C, or anything else that can read and write lines.

Stable plugin support starts with Runyte 0.3.0.

{{< compact-table label="What plugins can provide" >}}
| Area | Plugins can add |
| --- | --- |
| **Commands** | Named commands in the palette; type `::` to browse them |
| **Keys** | Configurable bindings, shown in help and key hints |
| **Views** | Native lists, prompts, and menus that use Runyte's own keys |
| **Editing** | Atomic edits to captured selections, undone with one `u` |
| **Documents** | Remote files opened as ordinary editable buffers |
| **Background work** | Jobs, timers, and progress without blocking the editor |
{{< /compact-table >}}

## ru-time

[ru-time](https://github.com/runyte/ru-time) is the first official plugin: a
task list and time tracker in Python, using only the standard library.

{{< compact-table label="ru-time default shortcuts" >}}
| Task | Default shortcut or command |
| --- | --- |
| Open the task list | `Space = =` · `::time` |
| Add a task | `Space = a` · `::time-add` |
| Start or pause the task under the cursor | `Enter` |
| Edit the task's note | `Space = n` · `::time-note` |
| All actions for a task | `Tab` in the task list |
{{< /compact-table >}}

Task history persists per workspace, and interrupted timers can be recovered.
Notes open as normal Markdown buffers.

## Try one

Save [uppercase.py](https://github.com/runyte/runyte/blob/v0.3.2/docs/plugins/uppercase.py)
and [application.py](https://github.com/runyte/runyte/blob/v0.3.2/docs/plugins/application.py)
side by side, then add this to your configuration with absolute paths:

```yaml
plugins:
  - id: case
    enabled: true
    api: runyte-1
    runyte: ">=0.3.0, <0.4.0"
    executable: /absolute/path/to/python3
    args: [/absolute/path/to/uppercase.py]
    capabilities: [text, selections]
    bindings:
      uppercase: F12
```

Select some text and press `F12`, or run `::uppercase`.

{{< compact-table label="Plugin management commands" >}}
| Task | Command |
| --- | --- |
| Plugins, permissions, and diagnostics | `:plugins` |
| Stop a plugin | `:plugin-stop <id>` |
| Restart a plugin | `:plugin-restart <id>` |
{{< /compact-table >}}

## Trust

Plugins run as your user, with your permissions. Capabilities control what they
can do inside the editor, but they are not a sandbox. Enable only programs you
trust.

[Plugin guide](https://github.com/runyte/runyte/blob/v0.3.2/docs/plugins.md) ·
[Authoring guide](https://github.com/runyte/runyte/blob/v0.3.2/docs/plugins/authoring.md) ·
[Examples in Python, Rust, and C](https://github.com/runyte/runyte/blob/v0.3.2/docs/plugins/todo/README.md) ·
[File manager, SFTP, and media examples](https://github.com/runyte/runyte/blob/v0.3.2/docs/plugins/applications.md#local-file-manager)
