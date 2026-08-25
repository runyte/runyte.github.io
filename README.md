# runyte.com

Source of the [Runyte](https://github.com/runyte/runyte) website, built with
[Hugo](https://gohugo.io/) and deployed to GitHub Pages by GitHub Actions on
every push to `main`.

Currently a placeholder: the ASCII logo, centered.

```sh
hugo server   # local preview at http://localhost:1313/
hugo --gc --minify
```

The theme is custom (no `theme` key in `hugo.yaml`); layouts live in
`layouts/`, styles in `assets/css/main.css`.
