"""Integration checks for guide generation. Requires Hugo; uses only temporary files."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GuideGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="runyte-guide-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in (
            "content/docs/_content.gotmpl",
            "layouts/partials/guide/sections.html",
            "layouts/_default/_markup/render-link.html",
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        (self.root / "hugo.toml").write_text(
            'baseURL = "https://runyte.com/"\n'
            'disableKinds = ["taxonomy", "term", "rss"]\n'
            '[markup.goldmark.renderer]\nunsafe = true\n'
        )
        layout = '<h1 id="{{ .Params.guideID }}">{{ .Title }}</h1>{{ .Content }}'
        for name in ("single.html", "list.html"):
            (self.root / "layouts/_default" / name).write_text(layout)
        self.resource = self.root / "assets/imported/user-guide.json"
        self.resource.parent.mkdir(parents=True)
        self.build_number = 0

    def write_source(self, body):
        self.resource.write_text(json.dumps({
            "body": body,
            "sourcePath": "docs/user-guide.md",
            "sourceRef": "fixture",
            "lastmod": "2026-09-27T00:00:00Z",
        }))

    def build(self):
        self.build_number += 1
        destination = self.root / f"output-{self.build_number}"
        subprocess.run(
            ["hugo", "--source", str(self.root), "--destination", str(destination)],
            check=True, capture_output=True, text=True,
        )
        return destination

    def test_sections_preserve_code_duplicate_anchors_and_cross_section_links(self):
        self.write_source('''An introduction.

## First
First overview. [Go to second](#repeated-1).

### Repeated
First repeated section. [A shared reference][shared].

````markdown
## Not a section
```nested
### Not a subsection
```
````

~~~text
## Also not a section
~~~

    ## Indented code

<!--
## Hidden heading
-->

#### Detail
First detail.

## Second
Second overview.

### Repeated
Second repeated section. [Go to first](#repeated).

#### Detail
Second detail.

### Explicit {#chosen}
Explicit heading body.

[shared]: https://example.com/reference
''')
        output = self.build()
        guide = output / "docs/user-guide"
        first = (guide / "first/repeated/index.html").read_text()
        second = (guide / "second/repeated-1/index.html").read_text()
        self.assertIn('id="detail"', first)
        self.assertIn('id="detail-1"', second)
        self.assertIn('id="repeated-1"', second)
        self.assertIn('/docs/user-guide/first/repeated/#repeated', second)
        self.assertIn('/docs/user-guide/second/repeated-1/#repeated-1', (guide / 'first/index.html').read_text())
        self.assertIn('href="https://example.com/reference"', first)
        self.assertIn('Not a section', first)
        self.assertIn('Also not a section', first)
        self.assertIn('Indented code', first)
        self.assertTrue((guide / "second/chosen/index.html").exists())
        pages = list(guide.rglob("index.html"))
        self.assertEqual(len(pages), 6, 'Code and comments must not become pages')
        self.assertNotIn('Second repeated section.', first)

    def test_rebuild_derives_pages_from_changed_source(self):
        self.write_source('Introduction.\n\n## Original\nOriginal text.\n')
        first = self.build()
        self.assertTrue((first / "docs/user-guide/original/index.html").exists())
        self.write_source('Introduction.\n\n## Replacement\nUpdated text.\n\n### New child\nChild text.\n')
        second = self.build()
        self.assertFalse((second / "docs/user-guide/original/index.html").exists())
        self.assertTrue((second / "docs/user-guide/replacement/new-child/index.html").exists())
        self.assertIn('Updated text.', (second / "docs/user-guide/replacement/index.html").read_text())


if __name__ == "__main__":
    unittest.main()
