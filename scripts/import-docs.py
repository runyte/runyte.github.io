import argparse
import json
from pathlib import Path
import subprocess


DOCUMENTS = (
    ("docs/user-guide.md", "user-guide.md", "Runyte user guide",
     "Complete Runyte reference: modal editing, selections, search, Git, integrated terminals, persistent sessions, keybindings, and configuration."),
    ("docs/faq.md", "faq.md", "Frequently asked questions",
     "Runyte troubleshooting and terminal setup, including macOS Option and Alt keyboard shortcuts."),
)


def import_docs(repository, destination):
    def git(*arguments):
        return subprocess.check_output(
            ["git", "-C", str(repository), *arguments], text=True
        ).strip()

    revision = git("rev-parse", "HEAD")
    documents = []
    for source, filename, title, description in DOCUMENTS:
        content = (repository / source).read_text(encoding="utf-8")
        heading, separator, body = content.partition("\n")
        if not heading.startswith("# ") or not separator:
            raise ValueError(f"Expected a title in {source}")
        metadata = {
            "title": title,
            "description": description,
            "sourcePath": source,
            "sourceRef": revision,
            "lastmod": git("log", "-1", "--format=%cI", "--", source),
        }
        documents.append((filename, json.dumps(metadata, indent=2) + "\n\n" + body.lstrip("\n")))
    destination.mkdir(parents=True, exist_ok=True)
    for filename, content in documents:
        (destination / filename).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()
    import_docs(args.repository.resolve(), Path(__file__).resolve().parents[1] / "content/docs")
