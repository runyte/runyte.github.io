# Navigator video

`../../static/videos/runyte-demo.mp4` was recorded on 27 September 2026 from
real Runyte 0.3.3 (editor source `f310698` on `dev`) and Claude Code 2.1.283,
whose banner showed Opus 5.5. It is 200 columns × 50 rows at 12×26 pixels
(2400×1300), 15 fps, silent H.264/yuv420p: 900 frames, exactly 60 seconds.
The font is JetBrainsMono Nerd Font Medium with bold and italic variants.
`runyte-demo.edit.json` records the cuts and each act's time scale for that
take (1.17, 1.03 and 0.90). It replaces the Codex video described in
`../website/`.

A 60-second video in three 20-second acts, one theme each. Claude Code works
in the left pane while the right pane shows ordinary work, and the Navigator
keeps track of both.

1. **ocean-dark, 0:00–0:20.** Start on About and split the screen. Start
   `claude` in the left pane and rename its terminal `claude`. `Ctrl-g` opens
   Claude Code's prompt as a Runyte buffer. The task from `prompt.md` is
   pasted, `?` renders its table, and `:wbc` hands it back to Claude, which
   starts working.
2. **gruvbox, 0:20–0:40.** `Space n` switches the left pane to `README.md`,
   which hides Claude while it keeps working. In the right pane, `Space e`
   opens the explorer.
   `notes.md` is renamed to `docs/notes.md`, `CHANGELOG.md` is added, and
   `scratch.txt` is removed. `:w` shows the filesystem plan and Enter applies
   it. `Tab t` opens a `tests` terminal and runs `cargo test`.
3. **matrix, 0:40–1:00.** `Space n` lists everything, with live previews,
   and the right pane jumps to `src/main.rs`. Once Claude finishes,
   `Space n` shows `claude` as `unread`. Visiting it and pressing `gf` on the
   file named in its reply opens `src/store.rs`, where the gutter marks
   Claude's change.

Each act starts as the theme picker opens (`Space o t`), so the colours change
just after 0:20 and 0:40.

Moments in the published take, in seconds of the final video:

| Time | Moment |
| --- | --- |
| 0 | About |
| 6–8 | `claude` starts in the left pane |
| 8–11 | `Ctrl-g` opens the prompt and the task is pasted |
| 11.5–15 | Rendered task table |
| 16.5–20 | Prompt returned to Claude, which starts working |
| 20–24 | gruvbox; `Space n` hides Claude behind `README.md` |
| 26–34.5 | Explorer edits, filesystem plan, applied |
| 34.5–40 | `tests` terminal, `cargo test` passes 3 tests |
| 40–42 | matrix |
| 42–45 | Navigator with live previews; right pane to `src/main.rs` |
| 46–50 | Navigator shows `claude` as `unread`; visit it |
| 50–53 | Claude's reply in review; `gf` on `src/store.rs` |
| 53–56 | `src/store.rs` with gutter marks |
| 56–60 | Final Navigator |

## Files

- `scene.py` builds the demo Cargo project and the isolated settings.
- `prompt.md` is the task pasted into Claude Code.
- `navigator_video.py` records the raw take through the editor repository's
  `runyte-demo-videos` skill.
- `edit_video.py` cuts the waits for Claude Code and fits each act to exactly
  20 seconds.
- `runyte-demo.edit.json` is the edit record of the published take.

## Isolation

The recording never touches your own settings:

- Runyte runs as a persistent session with its own temporary config, so the
  theme picker's saves go there.
- Terminals get a temporary home whose `.bashrc` only sets `PS1='$ '`. No user
  name, host name or personal shell setup can reach the video. Cargo and
  rustup still use the real toolchain.
- Claude Code gets a temporary `CLAUDE_CONFIG_DIR`, deleted when the script
  exits. It holds a copy of the Claude Code login from `.credentials.json`,
  onboarding marked done, the workspace marked trusted, and the LSP plugin
  recommendation turned off. Of your own Claude Code state it copies only
  which notices were already seen. Edits and `cargo test` are pre-approved;
  any other command would ask for permission.
- Before every checkpoint the script compares the screen with the account
  name and email in your local Claude Code state, kept in memory only. It
  stops the recording if either appears.

## Recording a take

Build Runyte and install the skill's Python requirements:

```sh
python3 -m venv /tmp/runyte-video-venv
/tmp/runyte-video-venv/bin/pip install -r /path/to/runyte/skills/runyte-demo-videos/scripts/requirements.txt
/tmp/runyte-video-venv/bin/python navigator_video.py \
  --skills-root /path/to/runyte/skills \
  --binary /path/to/runyte/target/release/runyte \
  --font-dir /path/to/jetbrains-mono-nerd-fonts \
  --workspace /tmp/runyte-video-demo/api \
  --output /tmp/navigator-take.mp4
python3 edit_video.py /tmp/navigator-take.mp4 /tmp/runyte-demo.mp4
```

The workspace must be empty or absent. Its path is visible in the video. Git,
Cargo, FFmpeg with libx264, FFprobe and a logged-in Claude Code are required.
The font directory must contain the four JetBrainsMono files named by the
script.

`--stand-in` rehearses every Runyte step with a plain shell in place of Claude
Code. It needs no login, and never publish that take. Use it after changing
the scene.

Each checkpoint saves a PNG next to the output. If a step fails, the script
writes `<output>.failure.png` and `.failure.txt`. The script also stops if
Claude has already finished before its terminal is hidden, because it could
then not be shown as `unread`. Record another take in that case.

Review the checkpoint images before editing. Check in particular that Claude
Code's startup screen shows no account details, the rendered table, the
filesystem plan, the `unread` row, and the opened `src/store.rs`. The raw
take, its sidecars and the checkpoint images contain local paths; keep them
out of the repository.

The Claude Code screen markers (`CLAUDE_BUSY`, `CLAUDE_READY`, `CLAUDE_TRUST`)
are at the top of `navigator_video.py`. If Claude Code changes its interface
and a readiness wait times out, adjust them there.

The editor README embeds a GitHub video attachment rather than the website
file. When replacing the demo, upload the final MP4 to GitHub as well and
update the attachment URL near the beginning of the editor README.

The current attachment is
<https://github.com/user-attachments/assets/b11679ab-0369-4bca-be4c-43c419b528c0>.
Its bytes were checked against `static/videos/runyte-demo.mp4`, and the public
README player was checked without signing in.

GitHub supports authenticated media uploads through the endpoint used by
[GitHub CLI's attachment uploader](https://github.com/cli/cli/blob/trunk/internal/attachments/client.go).
A browser upload is not required. From the website repository:

```sh
video_repo_id=$(gh api repos/runyte/runyte --jq .id)
gh api --method POST \
  "https://uploads.github.com/user-attachments/assets?name=runyte-demo.mp4&content_type=video%2Fmp4&repository_id=${video_repo_id}" \
  --header 'Content-Type: application/octet-stream' \
  --header 'Accept: application/vnd.github+json' \
  --input static/videos/runyte-demo.mp4 --jq .url
```

Use the returned canonical attachment URL as its own README paragraph. Preserve
the caption. Verify the public README player after publishing the reference;
an unattached upload may not yet be accessible anonymously. Do not store the
player's temporary signed download URL in Markdown.
