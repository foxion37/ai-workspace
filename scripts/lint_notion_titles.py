#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/Users/barq")
CONFIG_PATH = ROOT / "developer/projects/ai-workspace/config/notion_work_note_targets.json"
FILES_TO_SCAN = [
    ROOT / "developer/projects/ai-workspace/docs/notion-queue-operating-standard.md",
    ROOT / "developer/projects/ai-workspace/docs/notion-obsidian-style-guide.md",
    ROOT / "developer/projects/ai-workspace/docs/notion-subagent-team.md",
    ROOT / "Downloads/NOTION_OPERATION_PLAN.md",
    ROOT / "developer/notion-auto-sync/docs/2026-03-21-notion-agent-design.md",
]

FIXED_FUNCTIONAL_NAMES = {
    "운영 센터 (ops center)",
    "운영 매뉴얼 (ops manual)",
    "현재 상태 (current)",
    "진행 기록 (reports)",
    "점검 기록 (check log)",
    "운영 로그 (ops log)",
    "기준 자료 (references)",
}

REQUIRED_BILINGUAL_TITLES = {
    "대시보드 (dashboard)",
    "개발 (developer)",
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
        if path.name == "notion-queue-operating-standard.md":
            if "Notion은 모든 구조화된 데이터의 source of truth다" not in text:
                findings.append(f"[error] missing source-of-truth rule in queue standard: {path}")
            if "Queue Workflow" not in text:
                findings.append(f"[error] missing queue workflow section: {path}")
            if "Forbidden Actions" not in text:
                findings.append(f"[error] missing forbidden actions section: {path}")
        if path.name == "notion-obsidian-style-guide.md" and "정본은 `docs/notion-queue-operating-standard.md`이다." not in text:
            findings.append(f"[error] missing queue-standard reference in style guide: {path}")

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
