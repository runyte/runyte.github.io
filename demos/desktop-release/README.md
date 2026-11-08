# Desktop release demo

`static/videos/runyte-demo.mp4` is 23 seconds, 2560 × 1380, 30 fps,
H.264/yuv420p, silent. The homepage hero, the demo overlay, and the editor README
all use it. `static/videos/features/desktop.mp4` is its 9.7-second pane section.

Everything is one uncut capture of the real native window on the `dark` theme,
working in a private clone of the Runyte repository:

| Time | Scene |
| --- | --- |
| 0–6 s | `overlay_rectangles` in `src/ui.rs`: select the function, then rename all 18 uses of `area` with multiple cursors |
| 6–16 s | Leave full-screen for six panes. Shift-Alt-drag extends panes down, up, right, left and up; Alt-drag swaps two columns |
| 16–23 s | The Navigator lists files and terminals, including those covered above, and brings back a hidden terminal |

Terminals are covered but never shrunk on camera, because a live shell loses its
visible output when its pane gets shorter.

Recorded from Runyte 0.4.3 (`fad66590`) on Linux with the native embedded font at
22 logical pixels. The display is an isolated Xvfb server with lavapipe. The
configuration, cache, runtime storage, shell home, and workspace belong to the
recording.

## Reproduce and review

`record_native.py` drives physical X11 input through libXtst and records the real
window with FFmpeg. Use `DISPLAY` for a dedicated 2560 × 1440 X server and
`VK_DRIVER_FILES` for a working Vulkan ICD. Do not point the recorder at a personal
desktop display.

```sh
python3 record_native.py --output OUT --workspace /srv/runyte-demo \
  --binary path/to/runyte-desktop --source file:///path/to/runyte
python3 edit_demo.py --native OUT/raw.mp4 --output EDITED
```

`--scene pdf-shot --pdf PDF --size 1920x1508 --theme everforest-dark-medium
--font-size 20` takes the homepage PDF screenshot. The PDF is supplied by the
maintainer and is not redistributed here. Only its cover is shown.

`edit_demo.py` also writes the poster frames. The homepage shows the first frame
as a still before the video plays, so replace them together. `reviewed-take.json`
records the checkpoints and hashes. The editor README embeds a GitHub attachment
of the same file.
