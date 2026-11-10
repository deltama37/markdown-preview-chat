#!/usr/bin/env python3
"""Render a Markdown file into an Artifact-ready HTML review page.

Usage:
    python3 render.py SOURCE.md OUT.html [--title T] [--rev N] [--note "what changed"]

The Markdown is embedded as JSON and rendered in the browser (marked + DOMPurify),
so the page needs no build step. Re-run after every edit and republish OUT.html
to the same artifact.
"""
import argparse
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent


def safe_json(value) -> str:
    # Escaping "<" keeps "</script>" and "<!--" inside the JSON from closing the tag.
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


def guess_title(md: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+?)\s*#*\s*$", md, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("out")
    ap.add_argument("--title")
    ap.add_argument("--rev", type=int, default=1)
    ap.add_argument("--note", default="", help="one-line summary of this revision's changes")
    ap.add_argument("--label", help="path shown in the header (defaults to SOURCE as given)")
    a = ap.parse_args()

    src = pathlib.Path(a.source)
    md = src.read_text(encoding="utf-8")
    title = a.title or guess_title(md, src.stem)

    page = (HERE / "template.html").read_text(encoding="utf-8")
    page = (
        page.replace("{{TITLE}}", html.escape(title))
        .replace("{{REV}}", str(a.rev))
        .replace("{{SOURCE}}", html.escape(a.label or a.source))
        .replace("{{META_JSON}}", safe_json({"rev": a.rev, "note": a.note}))
        .replace("{{MARKDOWN_JSON}}", safe_json(md))
    )

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} (title={title!r}, rev={a.rev}, {len(page)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
