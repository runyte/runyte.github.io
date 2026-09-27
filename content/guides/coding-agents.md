---
title: Use Claude Code and Codex inside Runyte
seoTitle: Use Claude Code and Codex in a Terminal Editor | Runyte
description: Run coding agents in Runyte terminal panes, edit their prompts with Ctrl+G, and return to the same workspace with your files and Git tools.
image: images/screenshots/coding-agents.webp
imageAlt: Claude Code and Codex in adjacent Runyte terminal panes.
---

# Use coding agents inside Runyte

Run Claude Code or Codex in terminal panes beside your files.
Use Runyte to edit their prompts and inspect their output.

## Set up

Install the agent separately. Set your editor in your shell configuration:

```sh
export EDITOR='runyte --wait'
export VISUAL='runyte --wait'
```

Restart an existing agent after changing these variables.

1. Run `runyte -a` in your project.
2. Press `Ctrl-w v` to split the view.
3. Press `Ctrl-w t` to open a terminal.
4. Start `claude` or `codex`.

{{< screenshot
  src="images/screenshots/coding-agents.webp"
  alt="Claude Code and Codex running in adjacent Runyte terminal panes."
  caption="Two coding agents in one workspace."
  theme="frappe"
>}}

## Edit a prompt with Ctrl-g

1. Draft a prompt in the agent.
2. Press `Ctrl-g` to open it in Runyte.
3. Press `i` and edit. Press `Esc` when done.
4. Run `:wq` to save and return to the agent.
5. Review the prompt, then submit it.

Saving with `:w` alone leaves the editor request open.
`:q!` cancels the request and discards unsaved changes.

## Move around

| Task | Keys |
| --- | --- |
| Move between panes | `Ctrl-w h/j/k/l` |
| Open Navigator, including from a terminal | `Ctrl-w n` |
| Leave terminal input | `Ctrl-\` |
| Resume terminal input | `i` |
| Find files or content from editor modes | `Space f`, then Tab to switch |
| Open Git actions from an editor buffer | `Space g` |

## Keep agents running

Use `:detach` after finishing any prompt-editor request.
Return with `runyte -a` in the same project.

Buffers and terminals stay alive while the local host runs.
They do not survive host termination or reboot.

[Persistent sessions](/guides/persistent-workspaces/) ·
[External-editor reference](/docs/user-guide/#session-and-destination-navigation)
