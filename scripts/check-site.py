import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET


BASE_URL = "https://runyte.com/"


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links = []
        self.ids = set()
        self.meta = {}
        self.canonical = None
        self.h1_count = 0
        self.title = ""
        self.in_title = False
        self.in_schema = False
        self.schema = ""
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag in ("img", "script", "video", "source") and "src" in attrs:
            self.links.append(attrs["src"])
        if tag == "video":
            for attr in ("poster", "data-src"):
                if attrs.get(attr):
                    self.links.append(attrs[attr])
        if tag == "meta":
            self.meta[attrs.get("name", attrs.get("property", attrs.get("http-equiv", "").lower()))] = attrs.get("content")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.in_title = True
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_schema = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script":
            self.in_schema = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_schema:
            self.schema += data


def check_site(root):
    pages = {}
    redirects = {}
    errors = []
    for file in root.rglob("index.html"):
        route = "/" + file.parent.relative_to(root).as_posix().strip(".")
        route = route.rstrip("/") + "/"
        page = Page(file.read_text(encoding="utf-8"))
        if page.meta.get("refresh"):
            redirects[route] = page
        else:
            pages[route] = page
    for route, page in redirects.items():
        target = urlsplit(page.canonical or "")
        if target.netloc != "runyte.com" or target.path not in pages:
            errors.append(f"{route}: invalid redirect target {page.canonical}")
        if page.canonical not in page.meta["refresh"]:
            errors.append(f"{route}: redirect does not match canonical target")
    for route, page in pages.items():
        canonical = urljoin(BASE_URL, route)
        if page.canonical != canonical:
            errors.append(f"{route}: incorrect canonical {page.canonical}")
        if not page.title.strip() or page.h1_count != 1:
            errors.append(f"{route}: expected a title and one h1")
        for field in ("description", "og:title", "og:description", "og:image", "og:image:alt", "twitter:card"):
            if not page.meta.get(field):
                errors.append(f"{route}: missing {field}")
        for link in page.links + [page.meta.get("og:image", "")]:
            target = urlsplit(urljoin(canonical, link))
            if target.netloc != "runyte.com":
                continue
            path = unquote(target.path)
            if path in pages:
                if target.fragment and unquote(target.fragment) not in pages[path].ids:
                    errors.append(f"{route}: missing anchor {link}")
            elif not (root / path.lstrip("/")).is_file():
                errors.append(f"{route}: missing target {link}")
    required = {"/docs/", "/docs/user-guide/", "/guides/coding-agents/", "/guides/persistent-workspaces/", "/guides/from-helix/"}
    if not required <= pages.keys():
        errors.append(f"Missing pages: {required - pages.keys()}")
    sitemap = ET.parse(root / "sitemap.xml")
    urls = {element.text for element in sitemap.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    expected = {urljoin(BASE_URL, route) for route in pages}
    if urls != expected:
        errors.append(f"Sitemap mismatch: {urls ^ expected}")
    robots = (root / "robots.txt").read_text()
    if "Sitemap: https://runyte.com/sitemap.xml" not in robots or "Disallow: /" in robots:
        errors.append("Unexpected robots policy or missing sitemap")
    schema = json.loads(pages["/"].schema)
    if schema.get("@type") != "SoftwareApplication" or schema.get("name") != "Runyte":
        errors.append("Missing Runyte software data")
    if not pages["/"].title.startswith("Runyte — Modal Terminal Editor"):
        errors.append("Unexpected homepage title")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(pages)} pages: metadata, headings, internal links and anchors, preview images, sitemap, robots, and software data.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("public", type=Path)
    check_site(parser.parse_args().public.resolve())
