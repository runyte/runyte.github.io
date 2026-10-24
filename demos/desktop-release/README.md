# Terminal and desktop release demo

The overview is 44.93 seconds (approximately 45 seconds), 2560 × 1440, 30 fps, H.264/yuv420p, silent.
The focused desktop clip is 26 seconds at the same geometry and frame rate.

The overview preserves selected scenes from the previous 40-second demo:

| New time | Original time | Scene |
| --- | --- | --- |
| 0–7 s | 0–7 s | Modal editing and file navigation |
| 7–12 s | 9.5–14.5 s | Shell command and one Navigator visit |
| 12–19 s | 21.5–28.5 s | Finder, rendered Markdown, persistent sessions |
| 19–45 s | New desktop capture | Images, PDF, pane swaps and expansion |

Repeated Navigator visits and the four-pane construction/final hold were removed.
Retained scenes play at their original speed. The older terminal capture is
2400 × 1300 at 15 fps, centered without upscaling on the new canvas; frames are
repeated for the 30 fps output. The new desktop capture is 2560 × 1380 at 30 fps
with a 60-pixel editorial caption band above it. Captions identify modifier keys;
all editor content and mouse movements come from the running application.

## Desktop sequence

- Open an animated GIF alongside source using `:vsplit`.
- Open a PDF below it using `:hsplit`.
- Alt-drag the GIF onto the source pane to swap them.
- Shift-Alt-drag the PDF upward to expand it into the neighbouring source pane.
- Zoom the PDF and return to fit.
- Alt-drag to swap the PDF and GIF, then hold the result.

Recorded from editor revision `f0692a1`, a 0.4.1 candidate still reporting 0.4.0,
on Linux using ocean-dark and the native embedded font at 22 logical pixels.
The native display is an isolated Xvfb server with lavapipe. Project files,
configuration, cache, and runtime storage belong to the recording fixture.
The source snippet is a static fixture and is never compiled or executed.

## Reproduce and review

`record_native.py` drives physical X11 input through libXtst and records the
real window with FFmpeg. Pass the desktop executable, GIF, PDF, a new output
directory, and an isolated workspace. The original media are supplied by the
maintainer and are not redistributed here as standalone source assets.

Use `DISPLAY` for a dedicated 2560 × 1440 X server and `VK_DRIVER_FILES` for a
working Vulkan ICD. Do not point the recorder at a personal desktop display.
`edit_demo.py` combines the reviewed take with the saved 40-second editing demo.
It requires FFmpeg with libx264 and a Noto Sans font for captions.

Inspect the full clip, plus transition frames showing the actual drag outlines,
swap results, expansion result, and zoom. `reviewed-take.json` records the
source hashes, cut decisions, output geometry, and review evidence. The final
media are `static/videos/runyte-demo.mp4` and
`static/videos/features/desktop.mp4`; poster frames show source, GIF, and PDF.
GitHub attachments are byte-identical copies for the editor README and release PR.
