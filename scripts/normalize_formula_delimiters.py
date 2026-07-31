#!/usr/bin/env python3
"""Check or normalize legacy MathJax delimiters in Markdown prose."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIPPED_PARTS = {".git", ".venv", "_site", "site", "__pycache__"}
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
REPLACEMENTS = (
    (r"\(", "$"),
    (r"\)", "$"),
    (r"\[", "$$"),
    (r"\]", "$$"),
)


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not SKIPPED_PARTS.intersection(path.relative_to(ROOT).parts)
    )


def transform_prose(line: str) -> tuple[str, int]:
    """Replace delimiters outside inline-code spans on one prose line."""
    result: list[str] = []
    replacements = 0
    cursor = 0

    while cursor < len(line):
        if line[cursor] == "`":
            end_of_run = cursor
            while end_of_run < len(line) and line[end_of_run] == "`":
                end_of_run += 1
            marker = line[cursor:end_of_run]
            closing = line.find(marker, end_of_run)
            if closing != -1:
                closing += len(marker)
                result.append(line[cursor:closing])
                cursor = closing
                continue

        matched = False
        for old, new in REPLACEMENTS:
            if line.startswith(old, cursor):
                result.append(new)
                replacements += 1
                cursor += len(old)
                matched = True
                break
        if not matched:
            result.append(line[cursor])
            cursor += 1

    return "".join(result), replacements


def transform_document(text: str) -> tuple[str, list[tuple[int, int]]]:
    """Return normalized text and changed line/count pairs."""
    output: list[str] = []
    changed_lines: list[tuple[int, int]] = []
    fence: tuple[str, int] | None = None

    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        marker_match = FENCE_RE.match(line)
        if marker_match:
            marker = marker_match.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            output.append(line)
            continue

        if fence is not None:
            output.append(line)
            continue

        transformed, count = transform_prose(line)
        output.append(transformed)
        if count:
            changed_lines.append((line_number, count))

    return "".join(output), changed_lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="rewrite Markdown prose; without this flag the command only checks",
    )
    args = parser.parse_args()

    affected: list[tuple[Path, list[tuple[int, int]]]] = []
    total = 0

    for path in markdown_files():
        original = path.read_text(encoding="utf-8")
        transformed, changed_lines = transform_document(original)
        if not changed_lines:
            continue
        affected.append((path, changed_lines))
        total += sum(count for _, count in changed_lines)
        if args.write:
            path.write_text(transformed, encoding="utf-8")

    if not affected:
        print("Formula delimiter check passed.")
        return 0

    action = "Normalized" if args.write else "Found"
    print(f"{action} {total} legacy delimiters in {len(affected)} Markdown files.")
    for path, changed_lines in affected:
        line_numbers = ", ".join(str(line) for line, _ in changed_lines[:12])
        suffix = ", ..." if len(changed_lines) > 12 else ""
        print(f"- {path.relative_to(ROOT)}: {line_numbers}{suffix}")

    if not args.write:
        print("Run scripts/normalize_formula_delimiters.py --write to normalize them.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
