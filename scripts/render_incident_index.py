#!/usr/bin/env python3
"""Render a simple incident INDEX.md from Markdown frontmatter files."""

from __future__ import annotations

import argparse
import pathlib
import re
from typing import Dict, List


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
EXCLUDED_NAMES = {"INDEX.md", "TEMPLATE.md", "TAXONOMY.md"}


def parse_scalar(value: str) -> str:
    value = value.strip()
    if value in {"", "[]"}:
        return ""
    return value.strip("'\"")


def parse_frontmatter(text: str) -> Dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    data: Dict[str, object] = {}
    current_key = None
    current_list: List[str] | None = None

    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - ") and current_key and current_list is not None:
            current_list.append(parse_scalar(line[4:]))
            continue
        if ": " in line:
            key, value = line.split(": ", 1)
            if value == "":
                current_key = key
                current_list = []
                data[key] = current_list
            else:
                current_key = None
                current_list = None
                data[key] = parse_scalar(value)
        elif line.endswith(":"):
            key = line[:-1]
            current_key = key
            current_list = []
            data[key] = current_list

    return data


def markdown_link(path: pathlib.Path, root: pathlib.Path) -> str:
    rel = path.relative_to(root).as_posix()
    return f"[{path.name}]({rel})"


def is_real_incident(path: pathlib.Path, meta: Dict[str, object]) -> bool:
    if path.name in EXCLUDED_NAMES:
        return False

    incident_id = str(meta.get("id", "")).strip()
    if not incident_id or "YYYY" in incident_id:
        return False

    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("incident_dir", type=pathlib.Path)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="INDEX.md output path. Defaults to incident_dir/INDEX.md",
    )
    args = parser.parse_args()

    incident_dir = args.incident_dir
    output = args.output or incident_dir / "INDEX.md"

    incidents = []
    for path in sorted(incident_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if not is_real_incident(path, meta):
            continue
        incidents.append(
            {
                "id": meta.get("id", ""),
                "title": meta.get("title", path.stem),
                "status": meta.get("status", ""),
                "severity": meta.get("severity", ""),
                "category": ", ".join(meta.get("category", [])),
                "system": ", ".join(meta.get("system", [])),
                "date_opened": meta.get("date_opened", ""),
                "path": path,
            }
        )

    lines = [
        "# Incident Index",
        "",
        "This file is generated from incident report frontmatter.",
        "",
        "| ID | Title | Status | Severity | Category | System | Opened | Path |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for incident in sorted(
        incidents,
        key=lambda item: (str(item["date_opened"]), str(item["id"])),
        reverse=True,
    ):
        lines.append(
            "| {id} | {title} | {status} | {severity} | {category} | {system} | {date_opened} | {path} |".format(
                id=incident["id"],
                title=incident["title"],
                status=incident["status"],
                severity=incident["severity"],
                category=incident["category"],
                system=incident["system"],
                date_opened=incident["date_opened"],
                path=markdown_link(incident["path"], incident_dir),
            )
        )

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
