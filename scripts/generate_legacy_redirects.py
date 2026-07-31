#!/usr/bin/env python3
"""Generate compatibility routes for the former ComputerScience site name."""

from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path


OLD_SITE_NAME = "ComputerScience"
NEW_SITE_NAME = "DataStructuresAndAlgorithms"
PAGES_PREFIX = "/notes"


def redirect_document(target: str) -> str:
    escaped_target = html.escape(target, quote=True)
    javascript_target = json.dumps(target)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="robots" content="noindex">
    <meta http-equiv="refresh" content="0; url={escaped_target}">
    <link rel="canonical" href="{escaped_target}">
    <title>Notes moved</title>
    <script>
      const target = {javascript_target};
      window.location.replace(target + window.location.search + window.location.hash);
    </script>
  </head>
  <body>
    <p>This note moved to <a href="{escaped_target}">{escaped_target}</a>.</p>
  </body>
</html>
"""


def generate(output_dir: Path) -> int:
    source_dir = output_dir / NEW_SITE_NAME
    legacy_dir = output_dir / OLD_SITE_NAME
    if not source_dir.is_dir():
        raise SystemExit(f"Missing built site: {source_dir}")

    if legacy_dir.exists():
        shutil.rmtree(legacy_dir)
    shutil.copytree(source_dir, legacy_dir)

    html_files = sorted(legacy_dir.rglob("*.html"))
    for legacy_file in html_files:
        relative_path = legacy_file.relative_to(legacy_dir).as_posix()
        target = f"{PAGES_PREFIX}/{NEW_SITE_NAME}/{relative_path}"
        legacy_file.write_text(redirect_document(target), encoding="utf-8")

    return len(html_files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "_site",
    )
    args = parser.parse_args()
    count = generate(args.output_dir.resolve())
    print(
        f"Generated {count} legacy HTML redirects: "
        f"{OLD_SITE_NAME} -> {NEW_SITE_NAME}"
    )


if __name__ == "__main__":
    main()
