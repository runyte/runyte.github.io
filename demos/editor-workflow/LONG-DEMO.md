# Forty-second editing workflow

[Watch the 40-second version](runyte-editor-demo-40s.mp4).

The first 20 seconds are the saved matrix demo, preserved frame for frame.
The second half visibly switches to gruvbox, fuzzy-finds a Markdown document,
renders its table, switches persistent sessions, and builds four live panes.

| Time | Action |
| --- | --- |
| 0–20s | Original matrix workflow: modal editing, search, Explorer, directory tree, shell terminals, and Navigator. |
| 20–22s | Open the theme picker and choose gruvbox. |
| 22–24s | Finder uses the noncontiguous query `dlnmd` to find `docs/launch.md`; open the match. |
| 24–26s | `?` renders the Markdown checklist and release-board table. |
| 26–29s | Space Space opens the session manager; filter for Workbench and open it. |
| 29–35s | Split the workspace, open a help page and Explorer, and start real htop. |
| 35–40s | Hold the four-pane layout while htop continues updating. |

The final grid has Python source at top left, Runyte's “Files, buffers, and
panes” help page at top right, htop at bottom left, and the integrated Explorer
at bottom right. The Workbench session uses gruvbox too.

## Reproduce

Use the dependencies and fonts in [README.md](README.md), plus `htop` and
permission to create local Unix sockets for Runyte's persistent sessions:

```sh
/tmp/runyte-video-venv/bin/python demos/editor-workflow/record_long_demo.py \
  --skills-root ../runyte-dev/skills \
  --binary ../runyte-dev/target/release/runyte \
  --font-dir "$HOME/.local/share/fonts" \
  --output-dir /tmp/runyte-editor-40s-review
```

Choose a new, empty output directory outside the repository. The default intro
is the MP4 beside this recipe and must match `reviewed-take.json`. After review,
copy only `runyte-editor-demo-40s.mp4` and the sanitized provenance into this
directory. Keep intermediate media, full recording metadata, and PNGs temporary.

- `long-recipe.json` defines the second half's exact keys, typing, pauses, and checkpoints.
- `launch.md` adds the Markdown fixture to both temporary projects.
- `record_long_demo.py` creates isolated Release and Workbench sessions, reconstructs the previous ending before recording, and captures the continuation.
- `reviewed-long-take.json` records the media hashes, checkpoint timings, and validation results.

The script owns and stops only the two temporary session hosts it creates.
Configuration and runtime directories are separate from the project fixtures.
Both sessions use a plain shell and have LSP disabled. Htop uses a dedicated
configuration with compact meters and no username column; it runs in read-only
mode and shows only its own PID. Its display comes from the actual htop process.
No coding assistants are launched or mentioned in the recording.

## Assembly and verification

The original 20-second video is joined to a separately recorded 20-second
continuation using stream copy. No intro frames are re-encoded. The script checks
the decoded hashes of all 300 intro frames against the saved original.

The result is 40.000 seconds: 600 frames at 15 fps, 2400 × 1300 pixels,
silent H.264/yuv420p. Interaction speed is unchanged. The final reading pause
is recorded live so htop keeps updating; only any small final duration adjustment
uses frame trimming or padding.

Checkpoints verify the new workflow and the contents of each final quadrant.
Review the extracted checkpoint PNGs and the final video before publishing.
The original 20-second MP4 remains available beside the longer version.

## Website and editor README

The website's overview uses a byte-identical copy at
`../../static/videos/runyte-demo.mp4`. Its poster,
`../../static/videos/runyte-demo-poster.webp`, is the four-pane frame at 37 seconds.
The existing `demoVideo` and `demoPoster` settings in `hugo.yaml` point to these
paths; the media URL helper adds content hashes for cache refreshes.

The editor README embeds the same MP4 through this GitHub attachment:

https://github.com/user-attachments/assets/86edfda0-f8cb-4999-b35d-4f450f4ad3c3

Keep that canonical URL on its own line for GitHub's inline player. Its caption
links to the website MP4 with the video hash in the query string. The video and
poster hashes, poster timestamp, and attachment URL are recorded in
`reviewed-long-take.json`.

To replace the video again, copy the reviewed final MP4 to the website path,
extract a matching poster, and upload the identical MP4 for the editor README:

```sh
video_repo_id=$(gh api repos/runyte/runyte --jq .id)
gh api --method POST \
  "https://uploads.github.com/user-attachments/assets?name=runyte-demo.mp4&content_type=video%2Fmp4&repository_id=${video_repo_id}" \
  --header 'Content-Type: application/octet-stream' \
  --header 'Accept: application/vnd.github+json' \
  --input static/videos/runyte-demo.mp4 --jq .url
```

Update the README attachment, caption, and provenance together. Validate the
Hugo build and browser playback before publishing the repository changes.
