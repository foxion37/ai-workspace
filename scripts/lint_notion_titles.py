#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/Users/barq")
CONFIG_PATH = ROOT / "developer/projects/ai-workspace/config/notion_work_note_targets.json"
FILES_TO_SCAN = [
    ROOT / "developer/projects/ai-workspace/docs/notion-work-note-routing.md",
    ROOT / "developer/projects/ai-workspace/docs/project-dashboard-standard.md",
    ROOT / "developer/projects/ai-workspace/docs/project-dashboard-template.md",
    ROOT / "developer/projects/ai-workspace/docs/notion-human-ops-standard.md",
    ROOT / "developer/projects/ai-workspace/docs/notion-obsidian-style-guide.md",
    ROOT / "Downloads/NOTION_OPERATION_PLAN.md",
    ROOT / "developer/notion-auto-sync/docs/2026-03-21-notion-agent-design.md",
]

FIXED_FUNCTIONAL_NAMES = {
    "dashboard",
    "developer",
    "Ops Center",
    "current",
    "reports",
    "check log",
    "ops log",
    "references",
}


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def main() -> int:
    findings: list[str] = []
    warnings: list[str] = []

    config = load_config()
    for name, project in sorted(config.get("projects", {}).items()):
        title = project.get("title", "").strip()
        route = project.get("route", "")
        if not title:
            findings.append(f"[error] missing title for project key: {name}")
        if route and "/" in route and "dashboard >" not in route:
            findings.append(f"[error] route should use breadcrumb style: {name} -> {route}")
        if title and route and title not in route:
            warnings.append(f"[warn] route does not include display title: {name} -> {route}")

    for path in FILES_TO_SCAN:
        if not path.exists():
            warnings.append(f"[warn] missing scan file: {path}")
            continue
        text = path.read_text()
        if "dashboard/developer" in text:
            warnings.append(f"[warn] slash route notation found: {path}")
        if "home-home" in text or "홈-home" in text:
            warnings.append(f"[warn] legacy family naming found: {path}")
        if path.name == "notion-obsidian-style-guide.md" and "Do not use Korean-English bilingual titles by default." not in text:
            findings.append(f"[error] missing Obsidian naming rule in style guide: {path}")
        if path.name == "notion-human-ops-standard.md":
            for fixed_name in sorted(FIXED_FUNCTIONAL_NAMES):
                if f"`{fixed_name}`" not in text:
                    warnings.append(f"[warn] fixed functional name not listed in manual: {fixed_name}")

    if findings:
        print("\n".join(findings + warnings))
        return 1

    if warnings:
        print("\n".join(warnings))
    else:
        print("[ok] notion title and route rules look consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
