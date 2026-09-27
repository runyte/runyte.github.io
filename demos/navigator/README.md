# Navigator screenshot

`../../static/images/screenshots/navigator.webp` was captured from real Runyte
0.3.3 (editor source `f310698`) on 27 September 2026. It uses terafox-soft,
160 columns × 58 rows at 12×26 pixels (1920×1508), and JetBrainsMono Nerd Font
Medium with bold/italic variants. The image is the editor's terminal output
rendered by the editor repository's `runyte-screenshots` skill, not a desktop
screenshot.

`navigator.py` builds a small Cargo project named `api` in an empty workspace,
commits it, and leaves uncommitted changes in `src/main.rs` and `README.md`.
It opens About, adds an unsaved line to `README.md` so the row shows `[+]`,
and opens `docs/design.md`. Two terminals keep running after `Space t q` hides
them: `docs server` runs `python3 -m http.server` bound to 127.0.0.1, and `git`
shows `git log`. The visible layout is `src/main.rs` on the left, the workspace
explorer top right, and a `tests` terminal below it that has run `cargo test`.
`Space n` then opens the Navigator with the `tests` terminal selected, so the
preview shows its test output.

Terminals start `bash --norc --noprofile` with `PS1='$ '`, so no user name,
host name or personal shell setup reaches the image. The workspace path is
visible in pane titles and the status line; use `/tmp/runyte-site-demo/api`
to match the other gallery screenshots.

To make a new take, build Runyte and install the skill's Python requirements.
Python 3, Cargo and Git must be installed.

```sh
python3 -m venv /tmp/runyte-capture-venv
/tmp/runyte-capture-venv/bin/pip install -r /path/to/runyte/skills/runyte-screenshots/scripts/requirements.txt
/tmp/runyte-capture-venv/bin/python navigator.py \
  --skills-root /path/to/runyte/skills \
  --binary /path/to/runyte/target/release/runyte \
  --font-dir /path/to/jetbrains-mono-nerd-fonts \
  --workspace /tmp/runyte-site-demo/api \
  --output /tmp/navigator.webp \
  --label 'Runyte <version> (<revision>); Navigator scene'
```

The workspace must be empty or absent. The font directory must contain the
four JetBrainsMono font files named by the script. The capture writes `.txt`
and `.json` sidecars next to the image; they contain local paths, so keep them
out of the repository. Open the image at full size and check the row states,
the terminal preview and the absence of a `stale` Git marker in the status line.

The editor README loads this image as
`https://runyte.com/images/screenshots/navigator.webp?v=<hash>`, where `<hash>`
is the first 12 hexadecimal characters of the file's SHA-256. Update it after
replacing the image.
