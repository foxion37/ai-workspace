#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
from urllib import request

ROOT = Path("/Users/barq")
CONFIG_PATH = ROOT / "developer/projects/ai-workspace/config/notion_work_note_targets.json"
LEGACY_NOTION_VERSION = "2022-06-28"
ICON_NOTION_VERSION = "2026-03-11"

DASHBOARD_ROOT_ID = "32b883f1-56f5-8098-94a6-ffa4ea21a9b9"
DEVELOPER_PAGE_ID = "32a883f1-56f5-8121-8685-ce680592ff2a"
MANUAL_PAGE_ID = "32a883f1-56f5-819a-87fa-f67a32877819"
OPS_LOG_PAGE_ID = "330883f1-56f5-81fd-9a10-ce37eeac532f"


def load_env() -> None:
    for path in [ROOT / ".dotfiles/.env", ROOT / "developer/notion-auto-sync/.env"]:
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip().removeprefix("export ").strip()
            if key and key not in os.environ:
                os.environ[key] = value.strip().strip('"').strip("'")
    if "NOTION_API_KEY" not in os.environ and "NOTION_AGENT_TOKEN" in os.environ:
        os.environ["NOTION_API_KEY"] = os.environ["NOTION_AGENT_TOKEN"]


def notion_request(method: str, url: str, body: dict | None = None, version: str = LEGACY_NOTION_VERSION) -> dict:
    token = os.environ["NOTION_API_KEY"]
    req = request.Request(
        url,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": version,
            "Content-Type": "application/json",
        },
        method=method,
    )
    with request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def text_block(block_type: str, text: str) -> dict:
    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": [{"type": "text", "text": {"content": text[:1900]}}],
        },
    }


def bullet(text: str) -> dict:
    return text_block("bulleted_list_item", text)


def callout(text: str) -> dict:
    return text_block("quote", text)


def title_property(title: str) -> dict:
    return {"title": [{"type": "text", "text": {"content": title[:180]}}]}


def native_icon(name: str, color: str) -> dict:
    return {"type": "icon", "icon": {"name": name, "color": color}}


def update_page_icon(page_id: str, icon_payload: dict) -> None:
    notion_request(
        "PATCH",
        f"https://api.notion.com/v1/pages/{page_id}",
        {"icon": icon_payload},
        version=ICON_NOTION_VERSION,
    )


def list_children(parent_id: str) -> list[dict]:
    data = notion_request("GET", f"https://api.notion.com/v1/blocks/{parent_id}/children?page_size=100")
    return data.get("results", [])


def clear_children(page_id: str) -> None:
    for child in list_children(page_id):
        if child.get("type") in {"child_page", "child_database"}:
            continue
        notion_request("PATCH", f"https://api.notion.com/v1/blocks/{child['id']}", {"archived": True})


def replace_page_content(page_id: str, blocks: list[dict]) -> None:
    clear_children(page_id)
    if blocks:
        notion_request("PATCH", f"https://api.notion.com/v1/blocks/{page_id}/children", {"children": blocks[:100]})


def find_child(parent_id: str, block_type: str, title: str) -> str | None:
    for child in list_children(parent_id):
        if child.get("type") != block_type:
            continue
        payload = child.get(block_type, {})
        current = payload.get("title", "")
        if current == title:
            return child["id"]
    return None


def ensure_page(parent_id: str, title: str, blocks: list[dict], icon_payload: dict | None = None) -> str:
    page_id = find_child(parent_id, "child_page", title)
    if not page_id:
        body = {"parent": {"page_id": parent_id}, "properties": {"title": title_property(title)}}
        if icon_payload is not None:
            body["icon"] = icon_payload
        page = notion_request(
            "POST",
            "https://api.notion.com/v1/pages",
            body,
            version=ICON_NOTION_VERSION if icon_payload is not None else LEGACY_NOTION_VERSION,
        )
        page_id = page["id"]
    if icon_payload is not None:
        update_page_icon(page_id, icon_payload)
    replace_page_content(page_id, blocks)
    return page_id


def ensure_database(parent_id: str, title: str) -> str:
    database_id = find_child(parent_id, "child_database", title)
    if database_id:
        return database_id
    database = notion_request(
        "POST",
        "https://api.notion.com/v1/databases",
        {
            "parent": {"page_id": parent_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": {
                "Title": {"title": {}},
                "Status": {"select": {"options": [{"name": "Inbox"}, {"name": "In Progress"}, {"name": "Blocked"}, {"name": "Review"}, {"name": "Done"}]}},
                "Progress %": {"number": {"format": "number"}},
                "Agent": {"select": {"options": [{"name": "Codex"}, {"name": "Claude"}, {"name": "Gemini"}, {"name": "User"}, {"name": "Mixed"}]}},
                "Area": {"rich_text": {}},
                "Started At": {"date": {}},
                "Last Updated": {"date": {}},
                "Next Step": {"rich_text": {}},
                "Human Summary": {"rich_text": {}},
                "Local Source": {"rich_text": {}},
            },
        },
    )
    return database["id"]


def create_db_row(database_id: str, title: str, status: str, progress: int, agent: str, area: str, summary: str, next_step: str, local_source: str, blocks: list[dict]) -> str:
    page = notion_request(
        "POST",
        "https://api.notion.com/v1/pages",
        {
            "parent": {"database_id": database_id},
            "icon": native_icon("document", "orange"),
            "properties": {
                "Title": title_property(title),
                "Status": {"select": {"name": status}},
                "Progress %": {"number": progress},
                "Agent": {"select": {"name": agent}},
                "Area": {"rich_text": [{"type": "text", "text": {"content": area}}]},
                "Started At": {"date": {"start": "2026-03-28"}},
                "Last Updated": {"date": {"start": "2026-03-28"}},
                "Next Step": {"rich_text": [{"type": "text", "text": {"content": next_step[:1900]}}]},
                "Human Summary": {"rich_text": [{"type": "text", "text": {"content": summary[:1900]}}]},
                "Local Source": {"rich_text": [{"type": "text", "text": {"content": local_source[:1900]}}]},
            },
        },
        version=ICON_NOTION_VERSION,
    )
    replace_page_content(page["id"], blocks)
    return page["id"]


def update_config(ops_center_page_id: str, project_ids: dict[str, str], session_db_id: str) -> None:
    config = json.loads(CONFIG_PATH.read_text())
    config["ops_center"] = {
        "page_id": ops_center_page_id,
        "route": "dashboard > Ops Center",
        "title": "Ops Center",
    }
    config["projects"]["notion-structure-ops"] = {
        "hub_page_id": project_ids["hub"],
        "dashboard_page_id": project_ids["current"],
        "reports_page_id": project_ids["reports"],
        "check_log_page_id": project_ids["check_log"],
        "route": "dashboard > developer > 노션 구조 정리",
        "rollout_status": "live",
        "template": "current/reports/check log",
        "title": "노션 구조 정리",
    }
    config["session_reports"] = {
        "database_id": session_db_id,
        "route": "dashboard > developer > AI Session Reports",
        "title": "AI Session Reports",
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=True, sort_keys=True) + "\n")


def main() -> int:
    load_env()

    manual_blocks = [
        callout("이 페이지는 노션 운영 계약의 정본이다. 스타일 세부 규칙은 notion-obsidian-style-guide 문서를 참조한다."),
        text_block("heading_2", "Role Split"),
        bullet("운영 계약: Zone, Lead, Approval, routing, source of truth."),
        bullet("스타일 가이드: 제목, 아이콘, 헤딩, 링크, 태그, 강조."),
        text_block("heading_2", "Fixed Functional Page Names"),
        bullet("dashboard"),
        bullet("developer"),
        bullet("Ops Center"),
        bullet("current"),
        bullet("reports"),
        bullet("check log"),
        bullet("ops log"),
        bullet("references"),
        text_block("heading_2", "Page Surface Order"),
        bullet("Hub: intro callout -> what this area is for -> start here -> child pages -> rules -> references."),
        bullet("Current: intro callout -> Goal -> Purpose -> Status -> Owner -> Next Step -> Last Updated -> Current Focus -> Active Work -> Checklist -> Open Issues -> Canonical Links."),
        bullet("Reports: intro callout -> entry format -> current linkage rule -> source-of-truth note."),
        bullet("Check log: intro callout -> open item rule -> owner or next action -> archive rule."),
        text_block("heading_2", "Status Signals"),
        bullet("Gray: default."),
        bullet("Orange: currently editing."),
        bullet("Yellow: paused or waiting."),
        bullet("Red: needs review now."),
        bullet("Green: checked or stable."),
        bullet("Blue: guide or reference."),
        bullet("Light gray: archive or legacy."),
        text_block("heading_2", "Heading Rule"),
        bullet("In Notion, the page title already acts as H1."),
        bullet("Body content starts at H2."),
    ]
    replace_page_content(MANUAL_PAGE_ID, manual_blocks)
    update_page_icon(MANUAL_PAGE_ID, native_icon("document", "blue"))
    print("[ok] manual updated", flush=True)

    ops_center_blocks = [
        callout("이 페이지는 운영 매뉴얼, 운영 로그, 세션 리포트로 들어가는 사람 중심 운영 입구다."),
        text_block("heading_2", "Start Here"),
        bullet("운영 기준은 노션 운영 매뉴얼 (notion manual) 1.0에서 확인한다."),
        bullet("현재 운영 로그는 운영 로그 (ops log)에서 확인한다."),
        bullet("AI와 사람이 진행 중인 작업은 developer 아래 AI Session Reports DB에서 확인한다."),
        text_block("heading_2", "Status Signal"),
        bullet("중립 페이지는 회색 아이콘을 기본으로 쓰고, 상태 신호가 필요할 때만 컬러를 쓴다."),
        text_block("heading_2", "How It Works"),
        bullet("긴 로그보다 현재 상태, 막힌 점, 다음 액션을 먼저 본다."),
        bullet("프로젝트별 current / reports / check log 흐름은 developer 허브 표준을 따른다."),
        bullet("로컬 문서가 원장이고, Notion은 사람이 읽는 현재 상태판으로 유지한다."),
    ]
    ops_center_page_id = ensure_page(DASHBOARD_ROOT_ID, "Ops Center", ops_center_blocks, native_icon("home", "blue"))
    print("[ok] Ops Center updated", flush=True)

    hub_blocks = [
        callout("이 페이지는 노션 구조 정리 세션의 프로젝트 허브다."),
        text_block("heading_2", "무엇을 하는 곳인가"),
        bullet("대시보드, 운영 문서, 세션 리포트 구조를 인간 중심으로 정리한다."),
        bullet("현재 상태는 current, 시점 기록은 reports, 점검 항목은 check log에서 본다."),
        text_block("heading_2", "바로 가기"),
        bullet("current"),
        bullet("reports"),
        bullet("check log"),
        bullet("references"),
    ]
    hub_page_id = ensure_page(DEVELOPER_PAGE_ID, "노션 구조 정리", hub_blocks, native_icon("document", "orange"))
    print("[ok] hub updated", flush=True)

    current_blocks = [
        callout("현재 기준 상태만 짧게 보여주는 사람 중심 작업판이다."),
        text_block("heading_2", "Goal"),
        bullet("초보 개발자도 지금 AI가 무엇을 하고 있는지 바로 이해할 수 있는 노션 구조를 만든다."),
        text_block("heading_2", "Purpose"),
        bullet("운영 문서, 세션 리포트, 프로젝트 허브의 역할을 분리해 탐색 비용을 낮춘다."),
        text_block("heading_2", "Status"),
        bullet("Status: In Progress"),
        bullet("Progress: 35%"),
        text_block("heading_2", "Owner"),
        bullet("Codex"),
        text_block("heading_2", "Next Step"),
        bullet("AI Session Reports DB와 current 문구를 손본 뒤 linked view 수동 정리를 이어간다."),
        text_block("heading_2", "Last Updated"),
        bullet("2026-03-29 00:00 KST"),
        text_block("heading_2", "Current Focus"),
        bullet("운영 센터 승격, developer 세션 리포트 DB, 세션 자동 기록"),
        text_block("heading_2", "Active Work"),
        bullet("Ops Center 문구 정비"),
        bullet("current / reports / check log 템플릿 고정"),
        text_block("heading_2", "Checklist"),
        bullet("Ops Center를 루트에서 보이게 만든다."),
        bullet("developer 아래 AI Session Reports DB를 만든다."),
        bullet("세션 시작/저장/종료 시 로컬 리포트를 자동 갱신한다."),
        bullet("프로젝트 허브 표준과 타이틀 규칙을 문서화한다."),
        text_block("heading_2", "Open Issues"),
        bullet("linked database view와 아이콘 색상은 수동 정리가 필요하다."),
        text_block("heading_2", "Canonical Links"),
        bullet("notion-human-ops-standard.md"),
        bullet("notion-obsidian-style-guide.md"),
    ]
    current_page_id = ensure_page(hub_page_id, "current", current_blocks, native_icon("document", "orange"))
    print("[ok] current updated", flush=True)

    reports_page_id = ensure_page(
        hub_page_id,
        "reports",
        [
            callout("이 페이지는 날짜형 스냅샷과 시점 기록만 둔다."),
            text_block("heading_2", "Entry Format"),
            bullet("활성 상태가 바뀌면 current도 함께 갱신한다."),
            bullet("긴 로그는 로컬 문서에 두고 여기에는 요약만 남긴다."),
            text_block("heading_2", "Source Of Truth"),
            bullet("원문과 긴 reasoning은 local Markdown이 정본이다."),
        ],
        native_icon("document", "gray"),
    )
    print("[ok] reports updated", flush=True)

    check_log_page_id = ensure_page(
        hub_page_id,
        "check log",
        [
            callout("이 페이지는 점검, 경고, follow-up만 둔다."),
            text_block("heading_2", "Open Item Rule"),
            bullet("title 불일치, 구조 충돌, 수동 후속 조치를 여기에 남긴다."),
            text_block("heading_2", "Archive Rule"),
            bullet("완료된 항목은 접거나 archive 처리한다."),
        ],
        native_icon("document", "red"),
    )
    print("[ok] check log updated", flush=True)

    ensure_page(
        hub_page_id,
        "references",
        [
            callout("이 페이지는 기준 문서와 외부 참고 링크만 모은다."),
            bullet("notion-human-ops-standard.md"),
            bullet("notion-obsidian-style-guide.md"),
            bullet("notion-work-note-routing.md"),
            bullet("project-dashboard-standard.md"),
        ],
        native_icon("document", "blue"),
    )
    print("[ok] references updated", flush=True)

    session_db_id = ensure_database(DEVELOPER_PAGE_ID, "AI Session Reports")
    print("[ok] session db ensured", flush=True)
    create_db_row(
        session_db_id,
        "2026-03-28 | 노션 구조 정리 | session report",
        "In Progress",
        35,
        "Codex",
        "developer",
        "운영 문서, 세션 리포트, 현황판 구조를 사람 중심으로 재설계하는 세션이다.",
        "Ops Center와 current 페이지 문구를 손보고 linked views를 수동 정리한다.",
        str(ROOT / ".orchestra/work-notes/2026-03-28__ops__ai-workspace.md"),
        [
            callout("이 페이지는 이번 세션의 사람 중심 리포트다."),
            text_block("heading_2", "Goal"),
            bullet("운영 문서와 세션 리포트를 초보 개발자도 이해 가능한 흐름으로 정리한다."),
            text_block("heading_2", "Purpose"),
            bullet("지금 무엇이 진행 중인지, 막힌 것은 무엇인지, 다음에 어디부터 봐야 하는지 바로 알게 한다."),
            text_block("heading_2", "Status"),
            bullet("Status: In Progress"),
            bullet("Progress: 35%"),
            text_block("heading_2", "Owner"),
            bullet("Codex"),
            text_block("heading_2", "Next Step"),
            bullet("linked view 구성과 후속 title tuning"),
            text_block("heading_2", "Last Updated"),
            bullet("2026-03-29 00:00 KST"),
            text_block("heading_2", "Checklist"),
            bullet("Ops Center 생성"),
            bullet("AI Session Reports DB 생성"),
            bullet("노션 구조 정리 프로젝트 허브 생성"),
            bullet("세션 자동 기록 로컬/노션 동시 업데이트 경로 확장"),
            text_block("heading_2", "Canonical Links"),
            bullet(str(ROOT / ".orchestra/work-notes/2026-03-28__ops__ai-workspace.md")),
        ],
    )
    print("[ok] sample session row created", flush=True)

    update_config(
        ops_center_page_id,
        {
            "hub": hub_page_id,
            "current": current_page_id,
            "reports": reports_page_id,
            "check_log": check_log_page_id,
        },
        session_db_id,
    )
    print("[ok] config updated", flush=True)

    print(json.dumps(
        {
            "ops_center_page_id": ops_center_page_id,
            "project_hub_page_id": hub_page_id,
            "project_current_page_id": current_page_id,
            "project_reports_page_id": reports_page_id,
            "project_check_log_page_id": check_log_page_id,
            "session_reports_database_id": session_db_id,
            "manual_page_id": MANUAL_PAGE_ID,
            "ops_log_page_id": OPS_LOG_PAGE_ID,
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
