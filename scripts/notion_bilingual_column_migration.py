#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path("/Users/barq")
SCRIPT_DIR = ROOT / "developer/projects/ai-workspace/scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import bootstrap_notion_human_ops as bootstrap  # noqa: E402
import session_work_note as work_note  # noqa: E402


PROJECTS_DATA_SOURCE_ID = "d44d1642-4422-447c-b774-fdc8ba4d98b2"
DOCUMENTS_DATA_SOURCE_ID = "2d74e3e1-a301-4bd1-bbc3-b973857d77e6"
SESSION_DATA_SOURCE_ID = "331883f1-56f5-81d5-b2a3-000b52aa26c1"


def patch_properties(database_id: str, properties: dict[str, object]) -> None:
    bootstrap.notion_request(
        "PATCH",
        f"https://api.notion.com/v1/data_sources/{database_id}",
        {"properties": properties},
        version=bootstrap.ICON_NOTION_VERSION,
    )


def migrate_projects() -> None:
    patch_properties(
        PROJECTS_DATA_SOURCE_ID,
        {
            "Reports Page": None,
            "Hub Page": None,
            "Check Log Page": None,
            "Current Page": None,
            "Next Step": None,
            "Current Focus": {"name": "짧은 요약 (Summary)"},
            "Lead Agent": {"name": "담당 에이전트 (Lead Agent)"},
            "Local Source": {"name": "원본 경로 (Local Source)"},
            "Status": {"name": "상태 (Status)"},
            "Priority": {"name": "우선순위 (Priority)"},
            "Visibility": {"name": "공개 범위 (Visibility)"},
            "Last Updated": {"name": "마지막 업데이트 (Last Updated)"},
            "Progress %": {"name": "진행률 % (Progress %)"},
            "Owner": {"name": "담당자 (Owner)"},
        },
    )


def migrate_documents() -> None:
    patch_properties(
        DOCUMENTS_DATA_SOURCE_ID,
        {
            "Local Source": {"name": "원본 경로 (Local Source)"},
            "Status": {"name": "상태 (Status)"},
            "Owner": {"name": "담당자 (Owner)"},
            "Purpose": {"name": "짧은 요약 (Summary)"},
            "Doc Type": {"name": "문서 유형 (Doc Type)"},
            "Last Updated": {"name": "마지막 업데이트 (Last Updated)"},
            "Page URL": {"name": "페이지 링크 (Page URL)"},
        },
    )


def migrate_session_reports() -> None:
    patch_properties(
        SESSION_DATA_SOURCE_ID,
        {
            "Next Step": None,
            "Agent": {"name": "담당 에이전트 (Agent)"},
            "Progress %": {"name": "진행률 % (Progress %)"},
            "Project / Session": {"name": "프로젝트 / 세션 (Project / Session)"},
            "Started At": {"name": "시작일 (Started At)"},
            "Local Source": {"name": "원본 경로 (Local Source)"},
            "Last Updated": {"name": "마지막 업데이트 (Last Updated)"},
            "Human Summary": {"name": "짧은 요약 (Summary)"},
            "Area": {"name": "영역 (Area)"},
            "Status": {"name": "상태 (Status)"},
        },
    )


def main() -> int:
    work_note.load_env_from_known_files()
    migrate_projects()
    migrate_documents()
    migrate_session_reports()
    print("[ok] bilingual column migration completed", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
