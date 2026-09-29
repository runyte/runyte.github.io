# runyte.com

Source of the [Runyte](https://github.com/runyte/runyte) website, built with
[Hugo](https://gohugo.io/) and deployed to GitHub Pages by GitHub Actions on
every push to `main` and daily. The build imports the user guide
from `runyte/runyte` on `main`. A local build takes an editor checkout as the
argument to `scripts/import-docs.py`. Imported documentation is generated input; edit the originals in the editor
repository.

The site introduces Runyte and includes documentation and workflow guides:

- About
- Features
- Plugins
- Screenshots
- Installation
- Performance
- Documentation
- Workflow guides

Content lives in `content/`, layouts in `layouts/`, and styles in
`assets/css/main.css`. The homepage renders `assets/ascii/logo.txt` as plain text, matching Runyte’s
`:about` page. The shared frame provides quiet top navigation, a status bar,
and keyboard controls.

```sh
python3 scripts/import-docs.py ../runyte
hugo server   # local preview at http://localhost:1313/
hugo --gc --minify
python3 scripts/check-site.py public
```

The theme is custom (no `theme` key in `hugo.yaml`); layouts live in
`layouts/`, styles in `assets/css/main.css`. Its colors follow Runyte’s
`ocean-dark` palette in `src/config/core_themes.rs`. Secondary text uses a brighter
muted tone for browser readability. Selection backgrounds use the palette’s
deeper blue so secondary text and links remain readable when highlighted.

Screenshots live in `static/images/screenshots/` and open in a shared dialog
controlled by `assets/js/screenshot-viewer.js`. All eight gallery images were
captured from Runyte 0.2.0 (`188b03f`) on 7 September 2026 using isolated demo
projects and decoded PTY output at 160×58 cells, rendered with JetBrainsMono
Nerd Font Medium and its bold/italic variants. Claude Code and Codex are
real terminal applications. Each image uses a different theme, identified in
its caption. Older assets remain available for existing external links.

The About page opens the overview demo in an overlay with native controls.
The video paths are configured in `hugo.yaml` (`demoVideo` and `demoPoster`).
The overview is the 60-second Runyte 0.3.3 / Claude Code recording documented in
[demos/navigator-video/](demos/navigator-video/). Its poster is the Navigator at
47 seconds, with Claude marked unread. The editor README uses a separate GitHub attachment of the same video.
See the Navigator recipe for its upload URL and replacement procedure.

The Features page has nine dedicated recordings in `static/videos/features/`.
[demos/features/](demos/features/) contains their fixture, replay recipes, and
version records. Each clip runs for 10–22 seconds. Media URLs include content
hashes so replacing a recording also refreshes browser caches.

Keep benchmark dates and measured source versions alongside their tables;
they are historical results, not timings of whichever release is current.


## Website interactions

`assets/js/editor.js` owns keyboard sequences, hints, Navigator, website help,
command entry, the demo overlay, and the quit fallback. The actions share one
registry. Page navigation comes from `data/navigation.json`.

- `Space ?`: website help and the shortcut setting.
- `Space n`: filter and open website pages.
- `:help`, `:about`, `:demo`, `:q`: documentation, home, video, and quit.
- `Esc`: close the current dialog or cancel a pending sequence.

Ordinary links work without JavaScript. `:q` shows an exit view when the browser
refuses to close its tab. Native video controls remain usable without scripts.

Browser checks require Playwright and a browser installation:

```sh
hugo server --disableFastRender --renderToMemory
# In another terminal:
node scripts/check-interactions.cjs
```

Set `PLAYWRIGHT_MODULE` to an existing Playwright module path if it is not in
Node's lookup path. `CHROME_BIN` can select a local Chromium executable.
Checks cover keyboard interactions, focus, playback, mobile widths, and links
without JavaScript. They write review screenshots to `/tmp/`.


## Split user guide

The import script copies the full guide into `assets/imported/user-guide.json`
with its source revision and date. The JSON is ignored by Git. CI refreshes it before every build; locally, rerun
`python3 scripts/import-docs.py ../runyte-dev` after editing the upstream guide.

`content/docs/_content.gotmpl` creates the guide pages during every Hugo build,
including live rebuilds when the imported resource changes. There are no
individual section files to maintain. `layouts/partials/guide/sections.html`
splits the guide at level-two and level-three ATX headings, preserving fenced
examples, reference links, explicit anchors, and duplicate heading IDs.

The guide has a narrow TOC pane and an independently scrolling content pane.
On mobile, Contents becomes a collapsible panel above the selected section.
Pages have real URLs and work without JavaScript. Old guide fragment links
redirect to their section with JavaScript, or show a continuation link without
it. The link render hook routes internal guide links directly to section pages.

Check generation with `python3 scripts/test-guide-generation.py`. The browser
checks also cover both panes, old links, and mobile and no-JavaScript navigation.
