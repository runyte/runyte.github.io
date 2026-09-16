---
title: Persistent terminal workspaces
seoTitle: Persistent Terminal Workspaces with Runyte
description: Keep files, unsaved buffers, language servers, and terminal processes open while you detach from Runyte or switch projects on Linux and macOS.
image: images/screenshots/session-strip.webp
imageAlt: Runyte with a strip of running persistent sessions above the editor.
---

# Persistent terminal workspaces with Runyte

A Runyte workspace belongs to one project directory. In persistent mode, a
local host keeps its buffers, panes, language servers, and terminal processes
alive while you detach or visit another project. The terminal interface
attaches to that host when you return.

## Open a project

From your project directory, start Runyte in persistent mode:

```sh
runyte --persistent
```

Open files with `Space f` and a terminal with `Ctrl-w t`. A terminal session is
one shell or other child process; a persistent session retains the whole
workspace, which can contain several terminal sessions.

## Detach and return

From an editor buffer, run `:detach`. If you are typing in a terminal, first
press `Ctrl-\` to enter Runyte's Normal mode, then type `:detach` and press Enter.
The interface returns to your outer shell while the host continues running.

From the same project directory, run:

```sh
runyte --persistent
```

Your panes, unsaved buffers, and running terminals remain in the host. Save
important edits to disk as usual.

## Switch projects

`Space Space` opens the persistent-session manager. Select a workspace and
press Enter to attach; Runyte starts its host if necessary. Within the manager,
`Ctrl-o` opens a directory chooser for another project.

You can also switch from an integrated terminal:

```sh
cd ../other-project
runyte -a
```

This switches the outer Runyte interface to the new workspace. Returning to the
original workspace brings you back to its existing terminal.

| Action | Default keys |
| --- | --- |
| Open the persistent-session manager | `Space Space` |
| Previous or next running persistent session | `Shift-Left` / `Shift-Right` |
| Return to the previous persistent session | `Ctrl-w a` |
| Visit a numbered running persistent session | `Space 1`–`9` |
| Open buffers and terminals in this workspace | `Space n` |

{{< screenshot
  src="images/screenshots/session-strip.webp"
  alt="Runyte 0.2.0 with its running persistent sessions displayed above the editor."
  caption="Switch between running projects from the session strip."
  theme="ocean-dark"
>}}

## List or stop persistent sessions

From an outer shell:

```sh
runyte --session-list
runyte --session-stop PROJECT
```

Replace `PROJECT` with a session name, an unambiguous ID prefix, or a project
directory. A normal stop refuses while the host has protected work such as
unsaved files, live terminal children, or active plugin jobs. Finish that work
and exit the terminal programs before stopping the host.

Inside the editor, `:quit` closes the active pane and, from the last pane,
stops a clean persistent session. Use `:detach` when you want it to keep running.

## What persists

Persistent mode retains editor state and live processes for the lifetime of
the host. It supports one interactive terminal interface per workspace at a
time, and is local to your machine. It does not provide recovery of unsaved
text or live processes after host termination, logout, reboot, or machine failure.

See the [complete persistent-session reference](/docs/user-guide/#workspaces-and-modes)
and [coding-agent workflow](/guides/coding-agents/).
