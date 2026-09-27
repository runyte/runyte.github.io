# Feature videos

Seven real Runyte recordings for `/features/`. Recorded on 27 September 2026.

| Clip | Seconds | Theme | Action |
| --- | ---: | --- | --- |
| Modal editing | 16.2 | gruvbox | Replace six matches, undo, redo, save |
| Key hints | 16.1 | ocean-dark | Space hints, Git hints, contextual help |
| Markdown | 14.3 | nordbones-dark-soft | Render a table and return to source |
| Finder | 13.8 | everforest-dark-medium | Find names, search contents, preview matches |
| Navigator | 18.1 | matrix | Switch between files and a terminal |
| File management | 16.4 | gruvbox | Move, create, delete, review and apply |
| Git | 14.4 | rosebones-dark | Compare changes and stage a file |

## Capture

- Runyte 0.3.3. The binary hash is in `recordings.json`; its exact source revision was not verified.
- 200 × 50 terminal cells. 2400 × 1300 pixels. 15 fps. H.264, CRF 18, yuv420p.
- JetBrainsMono Nerd Font Medium, with bold and italic variants.
- Actual PTY output, rendered by the editor repository's `runyte-demo-videos` skill.
- Original timing, including short reading pauses. No speed changes or audio.
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

Choose a clip name from the table (lowercase, with hyphens).
`record_features.py` creates a disposable release-checklist project and a local
Git baseline. It uses standalone mode, isolated editor configuration, no LSP,
and a plain shell. Finder and Navigator use actual output from the fixture's
Python script. No personal files or coding-agent accounts are needed.

`recipes/` contains the exact keystrokes for these takes. Re-recording may change
the timing slightly. Temporary outputs include checkpoint PNGs, a contact sheet,
and recording sidecars. Inspect these before copying a take to `static/videos/features/`.
Keep sidecars containing machine paths out of the repository.

## Checks

- Inspect key frames and contact sheets for readability and unintended content.
- Verify saved edits, file operations, and Git staging in the fixture.
- Check the MP4 dimensions, frame rate, codec, and duration with ffprobe.
- Play each clip through in the browser. Check replay, independent playback, and no eager downloads.

The main `:demo` is a separate recording: see [the Navigator recipe](../navigator-video/README.md).
