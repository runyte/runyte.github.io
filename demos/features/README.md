# Feature videos

Nine real Runyte recordings for `/features/`. The original eight were recorded on
27 September 2026; directory tree on 29 September 2026.

| Clip | Seconds | Theme | Action |
| --- | ---: | --- | --- |
| Modal editing | 16.2 | gruvbox | Replace six matches, undo, redo, save |
| Key hints | 16.1 | ocean-dark | Space hints, Git hints, contextual help |
| Markdown | 14.3 | nordbones-dark-soft | Render a table and return to source |
| Finder | 13.8 | everforest-dark-medium | Find names, search contents, preview matches |
| Navigator | 18.1 | matrix | Switch between files and a terminal |
| Directory tree | 10.0 | ocean-dark | Reveal the active file, open a neighbor, hide and restore the tree |
| File management | 16.4 | gruvbox | Move, create, delete, review and apply |
| Git | 14.4 | rosebones-dark | Compare changes and stage a file |
| Session management | 22.1 | terafox / ember-dark | Manage sessions and switch with Shift Left / Right |

## Capture

- Runyte 0.3.3 for the original eight; 0.3.4 for directory tree. Binary hashes are in `recordings.json`. The original seven clips and directory tree have an unverified build source revision; session management was built from `457dbd2dddec88b22956782a90d8cd4479e9e7ca`.
- 200 × 50 terminal cells. 2400 × 1300 pixels. 15 fps. H.264, CRF 18, yuv420p.
- JetBrainsMono Nerd Font Medium, with bold and italic variants.
- Actual PTY output, rendered by the editor repository's `runyte-demo-videos` skill.
- Original timing, including short reading pauses. No speed changes or audio.
  Directory tree adjusts only the final still to exactly 10 seconds (150 frames).
- Posters are frames extracted from the final MP4s. Times and checksums are in `recordings.json`.

## Repeat

Requires Python with Pillow, pyte, and wcwidth; ffmpeg; Git; the editor binary;
and the recording skill from the editor repository.

```sh
python3 demos/features/record_features.py modal-editing \
  --skills-root ../runyte-dev/skills \
  --binary ../runyte-dev/target/release/runyte \
  --font-dir /path/to/jetbrains-mono-fonts \
  --output-dir /tmp/runyte-feature-takes
```

Choose a standalone clip name from the table (lowercase, with hyphens).
`record_features.py` creates a disposable release-checklist project and a local
Git baseline. It uses standalone mode, isolated editor configuration, no LSP,
and a plain shell. Finder and Navigator use actual output from the fixture's
Python script. No personal files or coding-agent accounts are needed.

`recipes/` contains the exact keystrokes for these takes. Re-recording may change
the timing slightly. Temporary outputs include checkpoint PNGs, a contact sheet,
and recording sidecars. Inspect these before copying a take to `static/videos/features/`.
Keep sidecars containing machine paths out of the repository.

### Directory tree

Use `directory-tree` with `record_features.py` and a Runyte build supporting
`Space d d` and `Space d t`. The fixture adds `src/config.py` beside `src/tasks.py`.
Checkpoints verify the tree appears, the neighboring file opens, and the sidebar
hides and returns. The final still is trimmed or padded to exactly 10 seconds;
the script also extracts the poster at 2 seconds. Recording sidecars describe the
raw take before this final duration adjustment. The final media metadata is in
`recordings.json`.

### Session management

The session clip uses its own script and two real persistent hosts:

```sh
python3 demos/features/record_sessions.py \
  --skills-root ../runyte-dev/skills \
  --binary /path/to/runyte \
  --font-dir /path/to/jetbrains-mono-fonts \
  --output-dir /tmp/runyte-session-take \
  --source-ref VERIFIED_BUILD_REVISION
```

- API uses `terafox`, with a rendered README beside Python code.
- Website uses `ember-dark`, with a rendered README beside CSS.
- `Space Space` opens the manager; Tab shows its actions.
- Filtering and Enter opens Website. Shift Left returns to API; Shift Right returns to Website.
- Checkpoints verify the visible content and the active pane's theme color after switching.

The script creates separate temporary projects and configuration/runtime storage.
It waits for both hosts to run, prepares their layouts, and records one client
switching between them. Cleanup stops only those two exact workspaces, including
after a failed take. It never attaches to or stops personal sessions.

## Checks

- Inspect key frames and contact sheets for readability and unintended content.
- Verify saved edits, file operations, and Git staging in the fixture.
- Check the MP4 dimensions, frame rate, codec, and duration with ffprobe.
- Play each clip through in the browser. Check replay, independent playback, and no eager downloads.

The main `:demo` is a separate recording: see [the Navigator recipe](../navigator-video/README.md).
