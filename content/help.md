---
title: Help
description: The essential Runyte shortcuts for editing, search, terminals, and persistent sessions.
---

# Find your way

Start with `:tutorial`. Press `Space` to discover commands as you work.

{{< compact-table label="Essential default shortcuts" >}}
| Task | Default shortcut |
| --- | --- |
| Find files or content | `Space f` · `Tab` switches mode |
| Navigate open buffers and terminals | `Space n` |
| Explore files | `Space e` |
| Open a terminal | `Ctrl-w t` |
| Move between panes | `Ctrl-w h/j/k/l` |
| Search this buffer | `s` literal · `/` regex |
| Start typing / return to Normal | `i` / `Esc` |
| Save | `Ctrl-s` |
| Contextual help | `Space ?` |
| Command palette / manual | `:` / `:help` |
{{< /compact-table >}}

## Switch projects. Keep your place.

Start with `runyte --persistent`. Buffers and terminals stay alive after detaching.

{{< session-navigation >}}

{{< compact-table label="Persistent session shortcuts" >}}
| Task | Default shortcut or command |
| --- | --- |
| Previous / next running session | `Shift ←` / `Shift →` |
| Jump to numbered session | `Space 1`–`9` |
| Return to previous session | `Ctrl-w a` |
| Session manager | `Space Space` |
| Detach and leave it running | `:detach` |
| Switch from an integrated terminal | `cd ../project` then `runyte -a` |
{{< /compact-table >}}

One interactive client per session. State lasts while its host runs, including
while detached; it does not survive host termination or reboot.

## Language tools

Language servers require workspace permission. Change it with `:lsp-trust`.
Editing and highlighting work without them.

[Full manual](https://github.com/runyte/runyte/blob/main/docs/user-guide.md) ·
[LSP setup](https://github.com/runyte/runyte/blob/main/docs/lsp/README.md) ·
[macOS Option-key help](https://github.com/runyte/runyte/blob/main/docs/faq.md)
