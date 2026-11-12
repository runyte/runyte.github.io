# Desktop release demo

`static/videos/runyte-demo.mp4` is 55.2 seconds, 2560 × 1380, 30 fps,
H.264/yuv420p, silent, and ends with a 1.5-second fade to black. The homepage
hero, the demo overlay, and the editor README all use it.

It joins two captures of the real native window on the `dark` theme. Both work
in a private clone of the Runyte repository at `51349bb2`, the revision the
previous overview showed. The editor take plays uncut:

| Time | Scene |
| --- | --- |
| 0–5.7 s | `overlay_rectangles` in `src/ui.rs`: select the function, then rename all 18 uses of `area` with multiple cursors |
| 5.7–18.7 s | `Space E` opens the workspace explorer; `/RustB` and Enter open the Rust Book PDF. `43gg` and two `Ctrl-f` reach page 45, three `+` zoom into Listing 2-1, `z f` fits again |
| 18.7–24 s | Leave full-screen for six panes, the PDF among them. Shift-Alt-drag extends one pane down and another up; Alt-drag swaps two columns |
| 24–31 s | The Navigator lists files and terminals, including those covered above, and brings back a hidden terminal |
| 31–36 s | `Space f` finds `src/diff.rs` by name and opens it |

The agent take follows with a cut. Codex and Claude Code sit side by side over
`[agent channel]`. Claude gets one prompt; after that the agents wake each
other by typing into each other's terminals:

| Time | Event |
| --- | --- |
| 38.3 s | Claude asks Codex in the channel whether `aligned_groups` in `src/diff.rs` stays fast on a 5000-line file |
| 41.3 s | Claude's wake-up line arrives at Codex's prompt, and Codex starts |
| 45.3 s | Codex answers in the channel: common ends are trimmed and `MAX_REGION_CELLS` caps the work |
| 48.8 s | Codex's wake-up line arrives at Claude's prompt, queued behind its current turn |
| 51.6 s | Claude checks the answer against `src/diff.rs` and confirms it in the channel |

Each message and wake-up line plays at normal speed. The typed prompt runs four
times faster, and the agents' work between beats is shortened. `edit_demo.py`
records every segment and its speed.

Terminals are covered but never shrunk on camera, because a live shell loses its
visible output when its pane gets shorter. The editor take turns
`editor.soft_wrap` off so the narrow panes look as they did in 0.4.3; the agent
take keeps it on so channel messages wrap.

Recorded from Runyte 0.4.5 (`28a6e0d6`) on Linux with the native embedded font at
22 logical pixels. The display is an isolated Xvfb server with lavapipe. The
configuration, cache, runtime storage, shell home, and workspace belong to the
recording.

`static/videos/features/desktop.mp4` is the 9.3-second pane section of the
previous 23-second overview, recorded from Runyte 0.4.3 (`fad66590`). The
scripts and record that produced it are in this directory's history.

## Agent channel

Both agents are real and unscripted. Files are read-only to them: Claude may use
Read, Grep, and Runyte's channel and terminal tools; Codex runs in a read-only
sandbox. Each needs Write in the workspace to type into the other's terminal.
Write cannot be a default grant, so the recorder grants it through
`:mcp claude` and `:mcp codex` before filming, for that throwaway workspace only.
Codex runs with the maintainer's personal `runyte-mcp` skill disabled, because
its summary otherwise printed that skill's home-directory path on screen.

## MCP server clip

`static/videos/features/agents.mp4` is a real exchange between Claude Code and
Codex through Runyte's MCP server and `:agent-channel`, on a one-file throwaway
project, in `frappe`. The agents are read-only and limited to the channel tools.
It was recorded with an earlier `--scene agents`, which this directory's history
keeps; `edit_agents.py` shortened its waits.

## Reproduce and review

`record_native.py` drives physical X11 input through libXtst and records the real
window with FFmpeg. Use `DISPLAY` for a dedicated 2560 × 1440 X server and
`VK_DRIVER_FILES` for a working Vulkan ICD. Do not point the recorder at a personal
desktop display. Record the two takes into separate output directories, removing
the workspace between them, then join them:

```sh
python3 record_native.py --output MAIN --workspace /tmp/runyte-demo \
  --binary path/to/runyte-desktop --source file:///path/to/runyte --pdf RustBook.pdf
python3 record_native.py --scene agents --output AGENTS --workspace /tmp/runyte-demo \
  --binary path/to/runyte-desktop --source file:///path/to/runyte
python3 edit_demo.py --native MAIN/raw.mp4 --agents AGENTS/raw.mp4 --output EDITED
```

The workspace path appears in pane titles, so keep it short. The PDF is supplied
by the maintainer and is not redistributed here; it stays untracked in the
recording workspace. The agents answer differently on every take, so find the
channel messages and wake-up lines in the new capture and adjust the segments in
`edit_demo.py` before encoding.

`--scene pdf-shot --pdf PDF --size 1920x1508 --theme everforest-dark-medium
--font-size 20` takes the homepage PDF screenshot. Only its cover is shown.

`edit_demo.py` also writes the poster. The homepage shows the first frame as a
still before the video plays, so replace them together. `reviewed-take.json`
records the checkpoints and hashes. The editor README embeds a GitHub attachment
of the same file.
