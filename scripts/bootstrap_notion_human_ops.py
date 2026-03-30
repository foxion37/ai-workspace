#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import socket
import time
from pathlib import Path
from urllib import request

ROOT = Path("/Users/barq")
CONFIG_PATH = ROOT / "developer/projects/ai-workspace/config/notion_work_note_targets.json"
LEGACY_NOTION_VERSION = "2022-06-28"
ICON_NOTION_VERSION = "2026-03-11"

DASHBOARD_ROOT_ID = "32b883f1-56f5-8098-94a6-ffa4ea21a9b9"
DEVELOPER_PAGE_ID = "32a883f1-56f5-8121-8685-ce680592ff2a"
LEGACY_MANUAL_PAGE_ID = "32a883f1-56f5-819a-87fa-f67a32877819"
MANUAL_PAGE_ID = LEGACY_MANUAL_PAGE_ID
OPS_LOG_PAGE_ID = "330883f1-56f5-81fd-9a10-ce37eeac532f"
PROJECT_BOARD_DB_ID = "6e94c178-b8d8-4e47-8013-cd8134f3d636"
DOCUMENT_BOARD_DB_ID = "e8b2bdc8-9059-4c33-9149-3f709c387c63"
SHARED_DATABASES_DB_ID = "001db86a-af75-4962-a14c-162e8ffd3cd8"


def progress_bar(percent: int, width: int = 10) -> str:
    clamped = max(0, min(100, percent))
    filled = round((clamped / 100) * width)
    return "[" + ("#" * filled) + ("-" * (width - filled)) + f"] {clamped}%"


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
    last_error: Exception | None = None
    for attempt in range(3):
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
        try:
            with request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except socket.timeout as exc:
            last_error = exc
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    raise last_error or RuntimeError("unknown Notion request error")


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


def divider_block() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def bilingual_heading(ko: str, en: str) -> dict:
    return text_block("heading_2", f"{ko} / {en}")


def bilingual_callout(ko: str, en: str) -> dict:
    return callout(f"{ko}\n{en}")


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


def update_database_icon(database_id: str, icon_payload: dict) -> None:
    notion_request(
        "PATCH",
        f"https://api.notion.com/v1/databases/{database_id}",
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
        try:
            notion_request("PATCH", f"https://api.notion.com/v1/blocks/{child['id']}", {"archived": True})
        except Exception as exc:
            print(f"[warn] failed to archive child block {child['id']}: {exc.__class__.__name__}", flush=True)


def replace_page_content(page_id: str, blocks: list[dict]) -> None:
    clear_children(page_id)
    if blocks:
        notion_request("PATCH", f"https://api.notion.com/v1/blocks/{page_id}/children", {"children": blocks[:100]})


def archive_page(page_id: str) -> None:
    notion_request("PATCH", f"https://api.notion.com/v1/pages/{page_id}", {"archived": True})


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
                "상태 (Status)": {"select": {"options": [{"name": "Inbox"}, {"name": "In Progress"}, {"name": "Blocked"}, {"name": "Review"}, {"name": "Done"}]}},
                "진행률 % (Progress %)": {"number": {"format": "number"}},
                "담당 에이전트 (Agent)": {"select": {"options": [{"name": "Codex"}, {"name": "Claude"}, {"name": "Gemini"}, {"name": "User"}, {"name": "Mixed"}]}},
                "영역 (Area)": {"rich_text": {}},
                "시작일 (Started At)": {"date": {}},
                "마지막 업데이트 (Last Updated)": {"date": {}},
                "짧은 요약 (Summary)": {"rich_text": {}},
                "원본 경로 (Local Source)": {"rich_text": {}},
            },
        },
    )
    return database["id"]


def ensure_database_with_schema(parent_id: str, title: str, properties: dict) -> str:
    database_id = find_child(parent_id, "child_database", title)
    if database_id:
        return database_id
    database = notion_request(
        "POST",
        "https://api.notion.com/v1/databases",
        {
            "parent": {"page_id": parent_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties,
        },
    )
    return database["id"]


def rename_database(database_id: str, title: str) -> None:
    notion_request(
        "PATCH",
        f"https://api.notion.com/v1/databases/{database_id}",
        {"title": [{"type": "text", "text": {"content": title}}]},
    )


def make_text_schema(*names: str) -> dict:
    schema = {"Title": {"title": {}}}
    for name in names:
        schema[name] = {"rich_text": {}}
    return schema


def make_link_schema(*names: str) -> dict:
    schema = {"Title": {"title": {}}}
    for name in names:
        schema[name] = {"url": {}}
    return schema


def create_row(database_id: str, title: str, properties: dict, icon_color: str = "blue") -> None:
    notion_request(
        "POST",
        "https://api.notion.com/v1/pages",
        {
            "parent": {"database_id": database_id},
            "icon": native_icon("document", icon_color),
            "properties": {
                "Title": title_property(title),
                **properties,
            },
        },
    )


def query_database_rows(database_id: str) -> list[dict]:
    data = notion_request(
        "POST",
        f"https://api.notion.com/v1/databases/{database_id}/query",
        {
            "page_size": 100,
            "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}],
        },
        version=ICON_NOTION_VERSION,
    )
    return data.get("results", [])


def find_database_row(database_id: str, title: str) -> dict | None:
    for row in query_database_rows(database_id):
        title_prop = row.get("properties", {}).get("Title", {}).get("title", [])
        current = "".join(part.get("plain_text", "") for part in title_prop)
        if current == title:
            return row
    return None


def create_db_row(database_id: str, title: str, status: str, progress: int, agent: str, area: str, summary: str, local_source: str = "", blocks: list[dict] | None = None) -> str:
    existing = find_database_row(database_id, title)
    properties = {
        "Title": title_property(title),
        "상태 (Status)": {"select": {"name": status}},
        "진행률 % (Progress %)": {"number": progress},
        "담당 에이전트 (Agent)": {"select": {"name": agent}},
        "영역 (Area)": {"rich_text": [{"type": "text", "text": {"content": area}}]},
        "시작일 (Started At)": {"date": {"start": "2026-03-28"}},
        "마지막 업데이트 (Last Updated)": {"date": {"start": "2026-03-28"}},
        "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": summary[:1900]}}]},
        "원본 경로 (Local Source)": {"rich_text": [{"type": "text", "text": {"content": local_source[:1900]}}]},
    }
    if existing:
        notion_request(
            "PATCH",
            f"https://api.notion.com/v1/pages/{existing['id']}",
            {"properties": properties, "icon": native_icon("document", "orange")},
            version=ICON_NOTION_VERSION,
        )
        replace_page_content(existing["id"], blocks or [])
        return existing["id"]
    page = notion_request(
        "POST",
        "https://api.notion.com/v1/pages",
        {
            "parent": {"database_id": database_id},
            "icon": native_icon("document", "orange"),
            "properties": properties,
        },
        version=ICON_NOTION_VERSION,
    )
    replace_page_content(page["id"], blocks or [])
    return page["id"]


def update_config(ops_center_page_id: str, manual_page_id: str, project_ids: dict[str, str], session_db_id: str) -> None:
    config = json.loads(CONFIG_PATH.read_text())
    config["ops_center"] = {
        "page_id": ops_center_page_id,
        "manual_page_id": manual_page_id,
        "route": "대시보드 (dashboard) > 운영 센터 (ops center)",
        "title": "운영 센터 (ops center)",
    }
    config["ops"] = {
        "page_id": OPS_LOG_PAGE_ID,
        "route": "대시보드 (dashboard) > 운영 센터 (ops center) > 운영 로그 (ops log)",
        "title": "운영 로그 (ops log)",
    }
    config["projects"]["notion-structure-ops"] = {
        "hub_page_id": project_ids["hub"],
        "dashboard_page_id": project_ids["current"],
        "reports_page_id": project_ids["reports"],
        "check_log_page_id": project_ids["check_log"],
        "route": "대시보드 (dashboard) > 개발 (developer) > 노션 구조 정리",
        "rollout_status": "live",
        "template": "current/reports/check log",
        "title": "노션 구조 정리",
    }
    config["session_reports"] = {
        "database_id": session_db_id,
        "route": "대시보드 (dashboard) > 개발 (developer) > AI 세션 리포트 (AI Session Reports)",
        "title": "AI 세션 리포트 (AI Session Reports)",
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=True, sort_keys=True) + "\n")


def main() -> int:
    load_env()

    manual_blocks = [
        callout("이 페이지는 운영 센터 (ops center) 아래의 노션 운영 계약 정본이다. 스타일 세부 규칙은 notion-obsidian-style-guide 문서를 참조한다."),
        text_block("heading_2", "매뉴얼 구조"),
        bullet("표현은 작업요청서 (request form)로 통일한다."),
        bullet("최상위 페이지 1개를 정본 허브로 둔다."),
        bullet("같은 성격의 페이지는 인라인 table DB로 묶는다."),
        bullet("장문 설명은 본문 일반 문단보다 table DB 행이나 하단 참고로 보낸다."),
        bullet("다른 페이지에 저장할 내용은 복제하지 않고 링크 1개로 배분한다."),
        bullet("로컬 문서와 Notion 연결도 링크 1개로 대체한다."),
        bullet("구조도 페이지는 별도로 두되, 정본 허브 아래에서만 연결한다."),
        text_block("heading_2", "실제 child DB"),
        bullet("페이지 맵 (Page Map)"),
        bullet("작업요청서 (Request Form)"),
        bullet("체크리스트 (Checklist)"),
        bullet("변경 기록 (Change Log)"),
        text_block("heading_2", "프로젝트 진행 절차"),
        bullet("1. 에이전트가 구조와 본문을 수정한다 → 정본 초안을 만든다."),
        bullet("2. 사용자가 세세한 지침, 단어, 위치, 모양을 직접 수정한다 → 사용자 정본이 된다."),
        bullet("3. 에이전트가 사용자가 수정한 내용과 기존에 자신이 작성한 내용을 비교 검토한다 → 업데이트 기획안을 작성한다."),
        bullet("4. 최종 매뉴얼을 완성한다 → 충돌 지점을 해소한다."),
        bullet("5. 다른 페이지에 같은 규칙을 배포한다 → 구조를 확장한다."),
        bullet("6. 하위 카테고리 페이지의 디테일 수정 기획을 만든다 → 세부 정리로 내려간다."),
        bullet("사용자 수정본이 있으면 그 버전을 우선 정본으로 본다."),
        bullet("에이전트는 그 정본을 기준으로 다시 비교하고, 차이를 설명 가능한 형태로 정리한 뒤 반영한다."),
        text_block("heading_2", "고정 기능 페이지명"),
        bullet("대시보드 (dashboard)"),
        bullet("개발 (developer)"),
        bullet("운영 센터 (ops center)"),
        bullet("현재 상태 (current)"),
        bullet("진행 기록 (reports)"),
        bullet("점검 기록 (check log)"),
        bullet("운영 로그 (ops log)"),
        bullet("기준 자료 (references)"),
        text_block("heading_2", "페이지 구성 순서"),
        bullet("허브: 소개 문구 → 이 영역의 목적 → 시작 위치 → 하위 페이지 → 규칙 → 기준 자료"),
        bullet("현재 상태: 소개 문구 → 목표 → 목적 → 상태 → 짧은 요약 → 인라인 로그 DB → 체크리스트 → 열린 이슈 → 정본 링크"),
        bullet("진행 기록: 소개 문구 → 입력 형식 → 페이지 본문 table DB → 정본 메모"),
        bullet("점검 기록: 소개 문구 → 열린 항목 규칙 → 페이지 본문 table DB → 보관 규칙"),
        text_block("heading_2", "컬러 사용 매뉴얼"),
        bullet("컬러 값은 노션 블록의 텍스트 색상 태그로 입력한다."),
        bullet("코드값은 hex 문자열이 아니라 노션 블록 포맷 안의 색상 태그 의미다."),
        bullet("색 이름은 항상 `한글 (영문)`으로 적는다."),
        bullet("갈색 (brown), 분홍 (pink), 보라 (purple)는 user-assigned로 둔다."),
        bullet("장문 컬러 설명은 한글을 먼저 쓰고, 영문 표기는 하단 참고로 내린다."),
        text_block("heading_2", "아이콘 규칙"),
        bullet("아이콘은 개성이 아니라 구분을 위한 표식이다."),
        bullet("고정 매핑은 표면 역할 기준으로 유지한다."),
        bullet("개발 루트는 회색 문서, 매뉴얼은 파란 문서, 활성 허브와 현재 표면은 주황 문서, 보고 표면은 회색 문서, 점검과 후속 표면은 노랑 문서, 기준 표면은 파란 문서를 쓴다."),
        bullet("DB 행은 상태 색을 따르고, 문서 행은 기본으로 파란 문서를 쓴다."),
        text_block("heading_2", "헤딩 규칙"),
        bullet("노션에서는 페이지 제목이 H1 역할을 한다."),
        bullet("본문은 H2부터 시작한다."),
        bullet("흐름이 중요한 문장은 한글 블록과 영문 블록을 가운데 구분선으로 나누고, 영문은 회색으로 둔다."),
        text_block("heading_2", "시각화 규칙"),
        bullet("AI 세션 리포트 (AI Session Reports) DB는 요약 속성만 얇게 두고, 상세 기록은 페이지 본문 table DB에 둔다."),
        bullet("페이지 본문에는 짧은 진행 바와 구조도, 인라인 로그 DB를 함께 넣어 첫 화면에서 상태를 읽게 한다."),
        bullet("진행 단계 표시는 `→`만 쓴다."),
        divider_block(),
        text_block("heading_2", "영문 참고"),
        bullet("Long-form text stays in Korean."),
        bullet("Short labels use Korean (English)."),
        bullet("If English is needed for a long section, place it below a divider."),
        bullet("Use only the arrow glyph →."),
        bullet("Color values are recorded as Notion text color tags, not hex strings."),
        bullet("When English and Korean are both needed for a long block, place Korean above and English below a divider."),
        divider_block(),
        text_block("heading_2", "복구된 기존 내용"),
        bullet("현재 보드 (current board)는 현재 상태 (current)의 현재 상태 영역으로 복구해 둔다."),
        bullet("활성 작업 보기 (active work view)는 페이지 본문 table DB로 옮겨 둔다."),
        bullet("담당자 (Owner), 다음 단계 (Next Step), 마지막 업데이트 (Last Updated), 현재 초점 (Current Focus) 같은 넓은 상위 속성은 줄이고 본문 로그로 내린다."),
        bullet("Progress %와 Status는 화면 읽기를 위한 최소 속성만 남긴다."),
        bullet("dashboard와 developer는 항상 대시보드 (dashboard)와 개발 (developer)로 쓴다."),
        bullet("운영 센터 (ops center)와 AI 세션 리포트 (AI Session Reports)는 사람 중심 입구와 인덱스 역할만 유지한다."),
    ]
    update_page_icon(DEVELOPER_PAGE_ID, native_icon("document", "gray"))
    print("[ok] manual template prepared", flush=True)

    ops_center_blocks = [
        callout("이 페이지는 운영 매뉴얼 (ops manual), 운영 로그, 세션 리포트로 들어가는 사람 중심 운영 입구다."),
        text_block("heading_2", "시작하기"),
        bullet("운영 기준은 운영 매뉴얼 (ops manual)에서 확인한다."),
        bullet("현재 운영 로그는 운영 로그 (ops log)에서 확인한다."),
        bullet("AI와 사람이 진행 중인 작업은 개발 (developer) 아래 AI 세션 리포트 (AI Session Reports) DB에서 확인한다."),
        text_block("heading_2", "컬러 사용 매뉴얼"),
        bullet("중립 페이지는 회색 아이콘을 기본으로 쓰고, 컬러가 필요할 때만 쓴다."),
        bullet("갈색, 핑크, 보라색은 user-assigned로 둔다."),
        text_block("heading_2", "진척도 시각화"),
        bullet(progress_bar(70)),
        bullet("차트 뷰는 사용자 수동 관리 표면으로 두고, 에이전트는 DB 건전성과 상태 문구 일관성을 먼저 본다."),
        text_block("heading_2", "구조도"),
        bullet("운영 센터 (ops center) → 운영 매뉴얼 (ops manual) → 운영 로그 (ops log) → 세션 리포트"),
        text_block("heading_2", "어떻게 운영하나"),
        bullet("긴 로그보다 현재 상태, 막힌 점, 다음 액션을 먼저 본다."),
        bullet("프로젝트별 현재 상태 (current) / 진행 기록 (reports) / 점검 기록 (check log) 흐름은 developer 허브 표준을 따른다."),
        bullet("각 페이지의 세부 내용은 page-body table DB에 쌓는다."),
        bullet("Notion은 정본 표면이고, 로컬은 상세 로그 캐시로 유지한다."),
    ]
    ops_center_page_id = ensure_page(DASHBOARD_ROOT_ID, "운영 센터 (ops center)", ops_center_blocks, native_icon("home", "blue"))
    print("[ok] ops center updated", flush=True)

    manual_page_id = ensure_page(ops_center_page_id, "운영 매뉴얼 (ops manual)", manual_blocks, native_icon("document", "blue"))
    if manual_page_id != LEGACY_MANUAL_PAGE_ID:
        try:
            archive_page(LEGACY_MANUAL_PAGE_ID)
        except Exception as exc:
            print(f"[warn] legacy manual archive skipped: {exc.__class__.__name__}", flush=True)
    update_page_icon(manual_page_id, native_icon("document", "blue"))
    print("[ok] manual moved under ops center", flush=True)

    hub_blocks = [
        callout("이 페이지는 노션 구조 정리 세션의 프로젝트 허브다."),
        text_block("heading_2", "무엇을 하는 곳인가"),
        bullet("대시보드 (dashboard), 운영 문서, 세션 리포트 구조를 사람 중심으로 정리한다."),
        bullet("현재 상태는 현재 상태 (current), 시점 기록은 진행 기록 (reports), 점검 항목은 점검 기록 (check log)에서 본다."),
        bullet("각 페이지의 세부 내용은 페이지 본문 table DB가 담당한다."),
        text_block("heading_2", "진척도 시각화"),
        bullet(progress_bar(100)),
        text_block("heading_2", "구조도"),
        bullet("노션 구조 정리 → 현재 상태 (current)"),
        bullet("노션 구조 정리 → 진행 기록 (reports)"),
        bullet("노션 구조 정리 → 점검 기록 (check log)"),
        bullet("노션 구조 정리 → 기준 자료 (references)"),
        text_block("heading_2", "바로 가기"),
        bullet("현재 상태 (current)"),
        bullet("진행 기록 (reports)"),
        bullet("점검 기록 (check log)"),
        bullet("기준 자료 (references)"),
    ]
    hub_page_id = ensure_page(DEVELOPER_PAGE_ID, "노션 구조 정리", hub_blocks, native_icon("document", "orange"))
    print("[ok] hub updated", flush=True)

    current_blocks = [
        callout("현재 기준 상태만 짧게 보여주는 사람 중심 작업판이다."),
        text_block("heading_2", "목표"),
        bullet("초보 개발자도 지금 AI가 무엇을 하는지 바로 이해할 수 있는 노션 구조를 만든다."),
        text_block("heading_2", "목적"),
        bullet("운영 문서, 세션 리포트, 프로젝트 허브의 역할을 분리해 탐색 비용을 낮춘다."),
        text_block("heading_2", "상태"),
        bullet("상태 (Status): 진행 중"),
        bullet("진행률 % (Progress %): 35%"),
        text_block("heading_2", "요약"),
        bullet("페이지 본문 table DB로 세부 기록을 쌓고, 표면은 현재 상태만 보여준다."),
        text_block("heading_2", "진척도 시각화"),
        bullet(progress_bar(35)),
        text_block("heading_2", "인라인 로그 DB"),
        bullet("2026-03-29 00:00 KST | current refresh | 다음 단계와 현재 초점을 페이지 본문 table DB에 둔다."),
        bullet("2026-03-29 00:00 KST | current refresh | current/reports/check log를 페이지 본문 table DB 기준으로 맞춘다."),
        text_block("heading_2", "체크리스트"),
        bullet("운영 센터 (ops center)를 루트에서 보이게 만든다."),
        bullet("개발 (developer) 아래 AI 세션 리포트 (AI Session Reports) DB를 만든다."),
        bullet("세션 시작/저장/종료 시 Notion queue와 로컬 로그를 함께 갱신한다."),
        bullet("프로젝트 허브 표준과 타이틀 규칙을 문서화한다."),
        text_block("heading_2", "열린 이슈"),
        bullet("차트 뷰는 사용자 수동 관리 표면으로 두고, 에이전트는 DB 속성과 상태 문구 정합성을 먼저 본다."),
        text_block("heading_2", "기준 링크"),
        bullet("notion-queue-operating-standard.md"),
        bullet("notion-obsidian-style-guide.md"),
    ]
    current_page_id = ensure_page(hub_page_id, "현재 상태 (current)", current_blocks, native_icon("document", "orange"))
    print("[ok] current updated", flush=True)

    reports_page_id = ensure_page(
        hub_page_id,
        "진행 기록 (reports)",
        [
            callout("이 페이지는 날짜형 스냅샷과 시점 기록만 둔다."),
            text_block("heading_2", "입력 형식"),
            bullet("활성 상태가 바뀌면 현재 상태 (current)도 함께 갱신한다."),
            bullet("상세 로그는 로컬에 두고 여기에는 요약만 남긴다."),
            bullet("세부 항목은 페이지 본문 table DB에 쌓는다."),
            text_block("heading_2", "정본 규칙"),
            bullet("원문과 긴 reasoning은 로컬 상세 로그로 남기고 Notion에는 요약만 기록한다."),
        ],
        native_icon("document", "gray"),
    )
    print("[ok] reports updated", flush=True)

    check_log_page_id = ensure_page(
        hub_page_id,
        "점검 기록 (check log)",
        [
            callout("이 페이지는 점검, 경고, follow-up만 둔다."),
            text_block("heading_2", "열린 항목 규칙"),
            bullet("title 불일치, 구조 충돌, 수동 후속 조치를 여기에 남긴다."),
            text_block("heading_2", "보관 규칙"),
            bullet("완료된 항목은 접거나 archive 처리한다."),
            bullet("세부 점검 내역은 페이지 본문 table DB에 쌓는다."),
        ],
        native_icon("document", "red"),
    )
    print("[ok] check log updated", flush=True)

    ensure_page(
        hub_page_id,
        "기준 자료 (references)",
        [
            callout("이 페이지는 기준 문서와 외부 참고 링크만 모은다."),
            bullet("notion-queue-operating-standard.md"),
            bullet("notion-obsidian-style-guide.md"),
            bullet("notion-subagent-team.md"),
            bullet("session-commands.md"),
        ],
        native_icon("document", "blue"),
    )
    print("[ok] references updated", flush=True)

    session_db_id = ensure_database(DEVELOPER_PAGE_ID, "AI 세션 리포트 (AI Session Reports)")
    update_database_icon(session_db_id, native_icon("document", "green"))
    print("[ok] session db ensured", flush=True)
    print("[ok] sample session row skipped", flush=True)

    page_map_db_id = ensure_database_with_schema(
        manual_page_id,
        "페이지 맵 (Page Map)",
        {
            "Title": {"title": {}},
            "구분 (Type)": {"select": {"options": [{"name": "hub"}, {"name": "manual"}, {"name": "dashboard"}, {"name": "log"}, {"name": "database"}, {"name": "page"}, {"name": "link"}]}},
            "링크 (Link)": {"url": {}},
            "상태 (Status)": {"select": {"options": [{"name": "Live"}, {"name": "Legacy"}, {"name": "Link only"}]}},
            "짧은 요약 (Summary)": {"rich_text": {}},
        },
    )
    update_database_icon(page_map_db_id, native_icon("document", "blue"))
    create_row(
        page_map_db_id,
        "운영 센터 (ops center)",
        {
            "구분 (Type)": {"select": {"name": "hub"}},
            "링크 (Link)": {"url": f"https://www.notion.so/{ops_center_page_id.replace('-', '')}"},
            "상태 (Status)": {"select": {"name": "Live"}},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "운영 진입 허브"}}]},
        },
    )
    create_row(
        page_map_db_id,
        "운영 매뉴얼 (ops manual)",
        {
            "구분 (Type)": {"select": {"name": "manual"}},
            "링크 (Link)": {"url": f"https://www.notion.so/{manual_page_id.replace('-', '')}"},
            "상태 (Status)": {"select": {"name": "Live"}},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "정본 운영 계약 문서"}}]},
        },
    )
    create_row(
        page_map_db_id,
        "운영 로그 (ops log)",
        {
            "구분 (Type)": {"select": {"name": "log"}},
            "링크 (Link)": {"url": f"https://www.notion.so/{OPS_LOG_PAGE_ID.replace('-', '')}"},
            "상태 (Status)": {"select": {"name": "Live"}},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "공유 운영 로그"}}]},
        },
    )
    create_row(
        page_map_db_id,
        "개발 (developer)",
        {
            "구분 (Type)": {"select": {"name": "hub"}},
            "링크 (Link)": {"url": f"https://www.notion.so/{DEVELOPER_PAGE_ID.replace('-', '')}"},
            "상태 (Status)": {"select": {"name": "Live"}},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "개발 허브"}}]},
        },
    )
    create_row(
        page_map_db_id,
        "현재 상태 (current)",
        {
            "구분 (Type)": {"select": {"name": "dashboard"}},
            "링크 (Link)": {"url": f"https://www.notion.so/{current_page_id.replace('-', '')}"},
            "상태 (Status)": {"select": {"name": "Live"}},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "라이브 상태 표면"}}]},
        },
    )
    create_row(
        page_map_db_id,
        "진행 기록 (reports)",
        {
            "구분 (Type)": {"select": {"name": "dashboard"}},
            "링크 (Link)": {"url": f"https://www.notion.so/{reports_page_id.replace('-', '')}"},
            "상태 (Status)": {"select": {"name": "Live"}},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "날짜형 스냅샷"}}]},
        },
    )
    create_row(
        page_map_db_id,
        "점검 기록 (check log)",
        {
            "구분 (Type)": {"select": {"name": "dashboard"}},
            "링크 (Link)": {"url": f"https://www.notion.so/{check_log_page_id.replace('-', '')}"},
            "상태 (Status)": {"select": {"name": "Live"}},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "점검과 후속 조치"}}]},
        },
    )
    create_row(
        page_map_db_id,
        "기준 자료 (references)",
        {
            "구분 (Type)": {"select": {"name": "link"}},
            "링크 (Link)": {"url": f"https://www.notion.so/{hub_page_id.replace('-', '')}"},
            "상태 (Status)": {"select": {"name": "Live"}},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "기준 문서 모음"}}]},
        },
    )

    request_db_id = ensure_database_with_schema(
        manual_page_id,
        "작업요청서 (Request Form)",
        {
            "Title": {"title": {}},
            "범주 (Category)": {"select": {"options": [{"name": "Structure"}, {"name": "Content"}, {"name": "Style"}, {"name": "Workflow"}, {"name": "Link"}, {"name": "Exception"}]}},
            "상태 (Status)": {"select": {"options": [{"name": "Inbox"}, {"name": "Draft"}, {"name": "Review"}, {"name": "Approved"}, {"name": "Applied"}]}},
            "우선순위 (Priority)": {"number": {"format": "number"}},
            "대상 링크 (Target Link)": {"url": {}},
            "짧은 요약 (Summary)": {"rich_text": {}},
        },
    )
    update_database_icon(request_db_id, native_icon("document", "orange"))
    create_row(
        request_db_id,
        "운영 매뉴얼 구조 수정",
        {
            "범주 (Category)": {"select": {"name": "Structure"}},
            "상태 (Status)": {"select": {"name": "Approved"}},
            "우선순위 (Priority)": {"number": 1},
            "대상 링크 (Target Link)": {"url": f"https://www.notion.so/{manual_page_id.replace('-', '')}"},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "정본 허브와 링크 운영 구조를 매뉴얼에 반영한다."}}]},
        },
    )

    checklist_db_id = ensure_database_with_schema(
        manual_page_id,
        "체크리스트 (Checklist)",
        {
            "Title": {"title": {}},
            "항목 (Item)": {"rich_text": {}},
            "상태 (Status)": {"select": {"options": [{"name": "Todo"}, {"name": "Doing"}, {"name": "Done"}]}},
            "대상 링크 (Target Link)": {"url": {}},
            "짧은 요약 (Summary)": {"rich_text": {}},
        },
    )
    update_database_icon(checklist_db_id, native_icon("document", "yellow"))
    create_row(
        checklist_db_id,
        "운영 센터 구조 확인",
        {
            "항목 (Item)": {"rich_text": [{"type": "text", "text": {"content": "운영 센터와 운영 매뉴얼의 child DB 노출 여부를 확인한다."}}]},
            "상태 (Status)": {"select": {"name": "Doing"}},
            "대상 링크 (Target Link)": {"url": f"https://www.notion.so/{ops_center_page_id.replace('-', '')}"},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "DB가 실제로 보이는지 확인한다."}}]},
        },
    )

    change_log_db_id = ensure_database_with_schema(
        manual_page_id,
        "변경 기록 (Change Log)",
        {
            "Title": {"title": {}},
            "비교 대상 (Compared)": {"rich_text": {}},
            "상태 (Status)": {"select": {"options": [{"name": "Open"}, {"name": "Applied"}, {"name": "Archived"}]}},
            "날짜 (Date)": {"date": {}},
            "대상 링크 (Target Link)": {"url": {}},
            "짧은 요약 (Summary)": {"rich_text": {}},
        },
    )
    update_database_icon(change_log_db_id, native_icon("document", "gray"))
    create_row(
        change_log_db_id,
        "운영 센터 원본 이동",
        {
            "비교 대상 (Compared)": {"rich_text": [{"type": "text", "text": {"content": "기존 텍스트 표면 -> 페이지 맵 중심 구조"}}]},
            "상태 (Status)": {"select": {"name": "Applied"}},
            "날짜 (Date)": {"date": {"start": "2026-03-30"}},
            "대상 링크 (Target Link)": {"url": f"https://www.notion.so/{manual_page_id.replace('-', '')}"},
            "짧은 요약 (Summary)": {"rich_text": [{"type": "text", "text": {"content": "다른 페이지는 링크로 두고 원본은 manual 아래로 모은다."}}]},
        },
    )

    rename_database(PROJECT_BOARD_DB_ID, "레거시 프로젝트 보드 (Legacy Project Board)")
    rename_database(DOCUMENT_BOARD_DB_ID, "레거시 문서 보드 (Legacy Document Board)")
    rename_database(SHARED_DATABASES_DB_ID, "레거시 공용 데이터베이스 (Legacy Shared Databases)")

    update_config(
        ops_center_page_id,
        manual_page_id,
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
            "manual_page_id": manual_page_id,
            "ops_log_page_id": OPS_LOG_PAGE_ID,
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
