# Website demo

`../../static/videos/runyte-demo.mp4` was recorded by Codex from real Runyte
0.2.2 (editor source `54366eb`) on 9 September 2026. It uses ocean-dark,
200 columns × 50 rows, and JetBrainsMono Nerd Font Medium with bold/italic
variants. The silent H.264/yuv420p video is 2400×1300 pixels at 15 fps:
900 frames, exactly 60 seconds.

The workflow starts on About, opens a terminal in a right vertical split,
and launches Codex. Ctrl-g opens the external prompt editor in the existing
Runyte persistent session. A meaningful focus-planner prompt supplies a wide
four-column task table, shown rendered and then soft-wrapped. `:wbc` saves the
prompt and returns to Codex; Enter submits it. In this Runyte version, `:wc`
means window-close; `:wbc` is the write-and-close-buffer command.

After the real answer arrives, Ctrl-\ and `gw` capture terminal review and
jump to `focus`. The word is copied into the left explorer to create `focus.rs`.
The complete answer is selected in terminal review and pasted into the file.
The prepared Cargo manifest registers that file as its binary target.
The script checks that the pasted answer compiles, formats it through Runyte,
and visibly changes a numeric `15` to `"15"`. The diagnostics list shows
the resulting real rust-analyzer/rustc type mismatch.

The final twelve seconds demonstrate Finder: `Space f` finds `focus.rs` by
name, then `Tab` switches to content mode. Searching `fn focus` finds the
function in both the file and retained Codex output. The scene selects each
source to show its preview, then Enter opens the terminal match in review.

`website_demo.py` prepares an empty temporary Git workspace, owns a persistent
host, and drives real keys through the editor repository's `runyte-demo-videos`
skill. It derives jump labels and the answer selection from the current screen.
It verifies actual file creation and compilation of the copied answer. No editor
API supplies text or selections. Generated Rust is compiled but not executed.

`prompt.md` is the prompt input. Runyte, Codex, rust-analyzer, Cargo, FFmpeg
with libx264, and FFprobe must be installed. Codex needs a working file-based
login and network access. The script copies the existing login into a private,
short-lived Codex home, then removes it with the other temporary settings.
The prompt asks for source only, without tools or file edits. Each scene-owned
persistent host is stopped explicitly during cleanup.

`edit_demo.py` removes startup and response waits and keeps a brief transition
into the answer. It budgets exactly three seconds for typing the prompt, twelve
seconds for Finder, and forty-five seconds for the rest of the workflow. Each
section is retimed separately, so filling the minute cannot stretch the prompt
typing again. Reading pauses are recorded live. `runyte-demo.edit.json` records
the cuts, section budgets, and source/output frame boundaries with each segment's
time scale. The raw recording, diagnostic screenshots, and private
recording metadata remain temporary verification artifacts.

To make a new take, build Runyte and install the skill's Python requirements:

```sh
python3 -m venv /tmp/runyte-video-venv
/tmp/runyte-video-venv/bin/pip install -r /path/to/runyte/skills/runyte-demo-videos/scripts/requirements.txt
/tmp/runyte-video-venv/bin/python website_demo.py \
  --skills-root /path/to/runyte/skills \
  --binary /path/to/runyte/target/release/runyte \
  --font-dir /path/to/jetbrains-mono-nerd-fonts \
  --workspace /tmp/focus-planner-new-take \
  --output /tmp/runyte-website-raw.mp4
/tmp/runyte-video-venv/bin/python edit_demo.py \
  /tmp/runyte-website-raw.mp4 /tmp/runyte-website-demo.mp4
```

Use an empty workspace and a new output name. The font directory must contain
the four JetBrainsMono font files named by the script. Inspect the rendered
table, label narrowing, copied filename, entire answer selection, and diagnostic
at full size. Check both Finder previews and the opened terminal match.
Generate the poster from the rendered, wrapped table checkpoint.

The editor README uses a GitHub video attachment to render a native player:
https://github.com/user-attachments/assets/cc77a90c-25e5-4b15-a1c9-f5da7f3f12fb

That attachment is a copy of the final MP4, separate from the website asset.
When replacing the demo, upload the new final MP4 to GitHub and update the
standalone attachment URL near the beginning of the editor README as well.
