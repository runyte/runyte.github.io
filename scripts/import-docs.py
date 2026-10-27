import argparse
import json
import re
from pathlib import Path
import subprocess


DOCUMENTS = (
    ("docs/user-guide/README.md", "user-guide.md", "Runyte user guide",
     "Complete Runyte reference: modal editing, selections, search, Git, integrated terminals, persistent sessions, keybindings, and configuration."),
)


def import_docs(repository, destination, assets):
    def git(*arguments):
        return subprocess.check_output(
            ["git", "-C", str(repository), *arguments], text=True
        ).strip()

    revision = git("rev-parse", "HEAD")
    documents = []
    for source, filename, title, description in DOCUMENTS:
        # Allow the website change to deploy before the editor source split.
        if not (repository / source).exists():
            source = "docs/user-guide.md"
        content = (repository / source).read_text(encoding="utf-8")
        chapters = re.findall(r"^- \[.*?\]\(([^)]+)\)$", content, re.MULTILINE) if source != "docs/user-guide.md" else []
        source_paths = {}
        bodies = []
        for chapter in chapters:
            chapter_path = "docs/user-guide/" + chapter
            chapter_body = (repository / chapter_path).read_text(encoding="utf-8").split("<!-- navigation -->")[0].rstrip()
            chapter_title = chapter_body.splitlines()[0][3:]
            source_paths[chapter_title] = chapter_path
            # Chapter links become guide anchors, preserving the existing routes.
            for target in chapters:
                chapter_body = chapter_body.replace("](" + target + "#", "](#")
            bodies.append(chapter_body)
        heading, separator, body = content.partition("\n")
        if chapters:
            introduction = body.split("## Maintaining the guide")[0].replace("## Contents", "**Contents**").strip()
            body = introduction + "\n\n" + "\n\n".join(bodies)
        if not heading.startswith("# ") or not separator:
            raise ValueError(f"Expected a title in {source}")
        metadata = {
            "title": title,
            "description": description,
            "sourcePath": source,
            "sourceRef": revision,
            "lastmod": git("log", "-1", "--format=%cI", "--", "docs/user-guide", "docs/user-guide.md"),
            "sourcePaths": source_paths,
        }
        if filename == "user-guide.md":
            # Hugo splits this single source into pages on every rebuild.
            assets.mkdir(parents=True, exist_ok=True)
            (assets / "user-guide.json").write_text(
                json.dumps({**metadata, "body": body.lstrip("\n")}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        else:
            documents.append((filename, json.dumps(metadata, indent=2) + "\n\n" + body.lstrip("\n")))
    destination.mkdir(parents=True, exist_ok=True)
    for filename, content in documents:
        (destination / filename).write_text(content, encoding="utf-8")
    # Remove obsolete generated pages, never hand-written files.
    for filename in ("user-guide.md", "faq.md"):
        old_page = destination / filename
        if old_page.exists() and f'"sourcePath": "docs/{filename}"' in old_page.read_text(encoding="utf-8"):
            old_page.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    import_docs(args.repository.resolve(), root / "content/docs", root / "assets/imported")
