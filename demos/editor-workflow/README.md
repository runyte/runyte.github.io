# Twenty-second editing workflow

A silent recording of real Runyte: modal editing, search, Explorer, the directory
tree, shell terminals, and Navigator. No coding assistants are launched or
mentioned onscreen. The [20-second video in the matrix theme](runyte-editor-demo.mp4) is
saved alongside this recipe. Raw takes and recording sidecars stay outside the
repository.

A [40-second version](LONG-DEMO.md) preserves this entire clip and adds a
gruvbox continuation with fuzzy finding, Markdown rendering, session management,
and four panes.

| Approximate time | Visible action |
| --- | --- |
| 0–4s | Search `pending` with `s`, select all six matches, change them to `ready`, then save with Ctrl-s. |
| 4–7s | Space e opens the integrated Explorer; k and Enter open `config.py`. Space d d reveals it in the directory tree; j and Enter open `tasks.py`. |
| 7–9.5s | Space f searches names for `release`; Down previews `docs/release.md`; Tab switches to content search. |
| 9.5–12s | Ctrl-w t starts a shell; `python3 src/tasks.py` prints the real result. Name the terminal `checks`. |
| 12–20s | Navigator switches to the edited file, the `history` shell, and the `checks` shell. End on the full destination list and terminal preview. |

Before recording, setup opens `README.md` and `src/tasks.py`, starts a separate
shell named `history`, and runs `git log --oneline -3`. Both shell processes remain
alive during the Navigator sequence. Space n opens Navigator from Normal mode;
Ctrl-w n opens it from a terminal. The fixture has no external dependencies.

## Reproduce

Requires Linux, Git, Python 3.10+ with Pillow/pyte/wcwidth, FFmpeg with libx264,
FFprobe, and a Runyte binary supporting the directory tree (recorded with 0.3.4).
The editor checkout must contain the adjacent `runyte-demo-videos` and
`runyte-screenshots` skills. Install the recorder's requirements into a temporary
virtual environment if needed:

```sh
python3 -m venv /tmp/runyte-video-venv
/tmp/runyte-video-venv/bin/pip install -r \
  ../runyte-dev/skills/runyte-demo-videos/scripts/requirements.txt
/tmp/runyte-video-venv/bin/python demos/editor-workflow/record_demo.py \
  --skills-root ../runyte-dev/skills \
  --binary ../runyte-dev/target/release/runyte \
  --font-dir "$HOME/.local/share/fonts" \
  --output-dir /tmp/runyte-editor-review
```

Choose a new, empty output directory for each take. The script rejects media
output inside this repository; copy an approved final MP4 here after review.
Font files must be named
`JetBrainsMonoNerdFont-Medium.ttf`, `JetBrainsMonoNerdFontMono-Bold.ttf`,
`JetBrainsMonoNerdFont-MediumItalic.ttf`, and
`JetBrainsMonoNerdFontMono-BoldItalic.ttf`.

- `recipe.json` contains the exact setup and recorded keys, typing, pauses, and checkpoints.
- `fixture/` contains the complete starting project, copied into a disposable Git workspace.
- `record_demo.py` prepares the fixture, records it, verifies the saved edit and Python result, and exports the final media.
- `reviewed-take.json` identifies the reviewed take by binary, recipe, and video hashes, with actual checkpoint timings. The binary's source revision was not independently verified.

The scene uses standalone Runyte with isolated configuration/runtime storage,
LSP disabled, matrix, and a plain `/bin/sh` prompt. It neither attaches to
personal editor sessions nor loads interactive shell configuration. Temporary
workspace paths appear in the pane titles. All processes and fixtures belong to
the recorder and are cleaned up when recording ends.

## Output and review

The final file is `runyte-editor-demo.mp4`: **20.000 seconds**, 300 frames at
15 fps, 2400 × 1300 pixels, H.264/yuv420p, no audio. The underlying terminal is
200 × 50 cells with JetBrainsMono Nerd Font Medium and bold/italic variants.
Interaction speed is unchanged; only the final still is padded or trimmed. If
the last action exceeds 19 seconds, the script fails rather than cutting it.

The output directory also contains the raw MP4, the recorder's metadata and
contact sheet, checkpoint text and PNGs, and `provenance.json`. Checkpoint PNGs
are extracted from the final MP4 inside the preceding reading pause, avoiding
the next action at a boundary. These artifacts remain outside Git.

The script checks all fourteen visible milestones, destination pane types,
the exact saved replacement, real Python output, and final media properties.
Review the checkpoint images and the full video for readability and pacing
before deciding whether to publish it. The recipe does not upload media,
replace `static/videos/runyte-demo.mp4`, or change the site's video configuration.
