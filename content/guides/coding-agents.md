---
title: Use Claude Code and Codex inside Runyte
seoTitle: Use Claude Code and Codex in a Terminal Editor | Runyte
description: Run coding agents in Runyte terminal panes, edit their prompts with Ctrl+G, and return to the same workspace with your files and Git tools.
image: images/screenshots/coding-agents.webp
imageAlt: Claude Code and Codex in adjacent Runyte terminal panes.
---

# Use Claude Code and Codex inside Runyte

Runyte runs CLI coding agents in integrated terminal panes beside your files.
In a persistent workspace, an agent's external-editor request can open its
prompt as an ordinary Runyte buffer in the same pane. Save and close that buffer
to return to the agent.

## Start a persistent workspace

[Install Runyte](/installation/) and install the coding agent you want to use
separately. From your project directory, run:

```sh
runyte --persistent
```

Press `Ctrl-w v` to split the view vertically, then `Ctrl-w t` to open a shell
in the active pane. Set the editor variables in that shell before starting
the agent:

```sh
export EDITOR='runyte --wait'
export VISUAL='runyte --wait'
```

Start `claude` or `codex` in that shell. Existing agent processes keep the
environment they started with, so restart the agent after changing these
variables. For the same workflow every time, put the exports in your shell's
configuration.

{{< screenshot
  src="images/screenshots/coding-agents.webp"
  alt="Claude Code and Codex running in adjacent Runyte 0.2.0 terminal panes."
  caption="Two coding agents in one workspace."
  theme="frappe"
>}}

## Edit a prompt with Ctrl+G

1. Type a draft into the agent's prompt input.
2. Press `Ctrl+G`. Runyte opens the requested file in Normal mode, temporarily
   covering the originating terminal.
3. Press `i` to edit. You can use the editor's selections, search, and normal
   text-editing commands.
4. Press `Esc`, then enter `:wq`. Runyte writes the prompt and returns to the
   same terminal. Review the text in the agent before submitting it.

`Ctrl+G` is documented by both
[Codex CLI](https://learn.chatgpt.com/docs/cli-customization#prompt-editor) and
[Claude Code](https://code.claude.com/docs/en/interactive-mode#general-controls).

Saving with `:w` alone leaves the editor request open. In this prompt-editing
workflow, `:q!` cancels the request and discards unsaved changes; text saved
previously remains on disk.

## Move between code and terminals

`Ctrl-w h/j/k/l` moves between panes, including while typing in a terminal.
`Ctrl-w n` opens the Navigator for open buffers and running terminals.

Ordinary terminal keystrokes belong to the running program. Press `Ctrl-\`
to leave terminal input and enter Runyte's live Normal mode; `i` resumes input.
From editor modes, `Space f` opens the Finder, and `Tab` switches it between
names and contents across files, open buffers, and terminals.

For Git work, open the `Space g` menu from an editor buffer. You can inspect
changes and stage them while the agent remains in its terminal pane.

## Keep the workspace running

After completing any open prompt-editor request, use `:detach` from editor
command mode to leave the persistent workspace running. Run `runyte --persistent`
from the same project directory to return. Detaching during an external-editor
request cancels that request.

Persistent state lasts while its local host process runs; it does not survive
host termination or reboot. See [persistent terminal workspaces](/guides/persistent-workspaces/)
and the [external-editor reference](/docs/user-guide/#session-and-destination-navigation).
