# runyte.com

Source of the [Runyte](https://github.com/runyte/runyte) website, built with
[Hugo](https://gohugo.io/) and deployed to GitHub Pages by GitHub Actions on
every push to `main`.

The site is a small seven-page introduction to Runyte:

- Intro
- Features
- Screenshots
- Installation
- Performance
- Help
- Acknowledgements

Content lives in `content/`, layouts in `layouts/`, and styles in
`assets/css/main.css`. The shared header renders `assets/ascii/logo.txt` as
plain text, matching the logo in Runyte’s `:about` page.

```sh
hugo server   # local preview at http://localhost:1313/
hugo --gc --minify
```

The theme is custom (no `theme` key in `hugo.yaml`); layouts live in
`layouts/`, styles in `assets/css/main.css`. Its colors follow Runyte’s
`ocean-dark` palette in `src/config/core_themes.rs`. Secondary text uses the
palette’s brighter muted color to stay readable at small browser font sizes.

Screenshots live in `static/images/screenshots/` and open in a shared dialog
controlled by `assets/js/screenshot-viewer.js`. All eight gallery images were
captured from Runyte 0.2.0 (`188b03f`) on 7 September 2026 using isolated demo
projects and decoded PTY output at 160×58 cells, rendered with JetBrainsMono
Nerd Font Medium and its bold/italic variants. Claude Code and Codex are
real terminal applications. Each image uses a different theme, identified in
its caption. Older assets remain available for existing external links.

The Intro page embeds the 60-second demo with native playback controls through
`layouts/shortcodes/video.html`. The video and poster live in `static/videos/`;
the editor README links its poster directly to the hosted MP4. Codex recorded
the real prompt-editor → Codex → Rust diagnostics → Finder workflow at 200×50 terminal
cells. [demos/website/](demos/website/) contains the source/version record, prompt,
replay script, and edit recipe.

Keep benchmark dates and measured source versions alongside their tables;
they are historical results, not timings of whichever release is current.
