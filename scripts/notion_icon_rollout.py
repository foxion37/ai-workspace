#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

import bootstrap_notion_human_ops as bootstrap

ROOT = Path("/Users/barq")
CONFIG_PATH = ROOT / "developer/projects/ai-workspace/config/notion_work_note_targets.json"


def load_env() -> None:
    bootstrap.load_env()


def safe_update_page_icon(page_id: str, name: str, color: str) -> None:
    try:
        bootstrap.update_page_icon(page_id, bootstrap.native_icon(name, color))
        print(f"[ok] page icon updated: {page_id}", flush=True)
    except Exception as exc:
        print(f"[warn] page icon skipped: {page_id} ({exc.__class__.__name__})", flush=True)


def safe_update_database_icon(database_id: str, name: str, color: str) -> None:
    try:
        bootstrap.update_database_icon(database_id, bootstrap.native_icon(name, color))
        print(f"[ok] database icon updated: {database_id}", flush=True)
    except Exception as exc:
        print(f"[warn] database icon skipped: {database_id} ({exc.__class__.__name__})", flush=True)


def main() -> int:
    load_env()
    config = json.loads(CONFIG_PATH.read_text())

    # Shared navigation surfaces
    manual_page_id = config["ops_center"].get("manual_page_id", bootstrap.MANUAL_PAGE_ID)
    safe_update_page_icon(manual_page_id, "document", "blue")
    safe_update_page_icon(bootstrap.DEVELOPER_PAGE_ID, "document", "gray")
    safe_update_page_icon(config["ops_center"]["page_id"], "home", "blue")
    safe_update_page_icon(config["ops"]["page_id"], "document", "gray")

    # Developer project surfaces: same icon role mapping everywhere.
    for slug, project in config["projects"].items():
        safe_update_page_icon(project["hub_page_id"], "document", "orange")
        safe_update_page_icon(project["dashboard_page_id"], "document", "orange")
        safe_update_page_icon(project["reports_page_id"], "document", "gray")
        safe_update_page_icon(project["check_log_page_id"], "document", "yellow")
        print(f"[ok] project icon scheme applied: {slug}", flush=True)

    # Session report DB is a database, not a page.
    safe_update_database_icon(config["session_reports"]["database_id"], "document", "green")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
