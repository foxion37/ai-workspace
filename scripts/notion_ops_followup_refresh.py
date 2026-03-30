#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import bootstrap_notion_human_ops as bootstrap
import session_work_note as work_note

ROOT = Path("/Users/barq")
WORK_NOTE_PATH = ROOT / ".orchestra/work-notes/2026-03-29__ops__ai-workspace.md"
TODAY = "2026-03-29"


def now_display() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")


def rich_text(value: str) -> list[dict]:
    return [{"type": "text", "text": {"content": value[:1900]}}]


def chart_view_names() -> tuple[str, str]:
    return ("상태 분포 (차트)", "진척도 비교 (차트)")


def patch_database_properties(database_id: str) -> None:
    database = bootstrap.notion_request("GET", f"https://api.notion.com/v1/databases/{database_id}")
    properties = database.get("properties", {})
    if "프로젝트 / 세션 (Project / Session)" in properties:
        return
    bootstrap.notion_request(
        "PATCH",
        f"https://api.notion.com/v1/databases/{database_id}",
        {"properties": {"프로젝트 / 세션 (Project / Session)": {"rich_text": {}}}},
    )
    print("[ok] session DB property added: 프로젝트 / 세션 (Project / Session)", flush=True)


def query_database_rows(database_id: str) -> list[dict]:
    data = bootstrap.notion_request(
        "POST",
        f"https://api.notion.com/v1/databases/{database_id}/query",
        {
            "page_size": 100,
            "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}],
        },
    )
    return data.get("results", [])


def title_text(row: dict) -> str:
    title_prop = row["properties"]["Title"]["title"]
    return "".join(part.get("plain_text", "") for part in title_prop)


def rich_text_value(row: dict, name: str) -> str:
    prop = row["properties"].get(name, {})
    prop_type = prop.get("type")
    if not prop_type:
        return ""
    value = prop.get(prop_type)
    if not isinstance(value, list):
        return ""
    return "".join(part.get("plain_text", "") for part in value)


def rich_text_value_any(row: dict, *names: str) -> str:
    for name in names:
        value = rich_text_value(row, name)
        if value:
            return value
    return ""


def archive_page(page_id: str) -> None:
    bootstrap.notion_request(
        "PATCH",
        f"https://api.notion.com/v1/pages/{page_id}",
        {"in_trash": True},
        version=bootstrap.ICON_NOTION_VERSION,
    )


def dedupe_session_rows(database_id: str) -> None:
    rows = query_database_rows(database_id)
    grouped: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        key = (title_text(row), rich_text_value_any(row, "원본 경로 (Local Source)", "Local Source"))
        grouped.setdefault(key, []).append(row)
    archived = 0
    for entries in grouped.values():
        if len(entries) < 2:
            continue
        keep = entries[0]
        for duplicate in entries[1:]:
            archive_page(duplicate["id"])
            archived += 1
        print(f"[ok] kept session row {keep['id']} and archived {len(entries) - 1} duplicates", flush=True)
    if archived == 0:
        print("[ok] session DB duplicates not found", flush=True)


def backfill_project_session(database_id: str) -> None:
    rows = query_database_rows(database_id)
    updated = 0
    for row in rows:
        title = title_text(row)
        project_value = rich_text_value_any(row, "프로젝트 / 세션 (Project / Session)", "Project / Session")
        if project_value or "노션 구조 정리" not in title:
            continue
        bootstrap.notion_request(
            "PATCH",
            f"https://api.notion.com/v1/pages/{row['id']}",
            {"properties": {"프로젝트 / 세션 (Project / Session)": {"rich_text": rich_text("노션 구조 정리")}}},
            version=bootstrap.ICON_NOTION_VERSION,
        )
        updated += 1
    print(f"[ok] backfilled 프로젝트 / 세션 (Project / Session) on {updated} rows", flush=True)


def row_blocks() -> list[dict]:
    status_chart, progress_chart = chart_view_names()
    return [
        bootstrap.callout("이 페이지는 노션 구조 정리 세션의 사람 중심 리포트다."),
        bootstrap.text_block("heading_2", "목표"),
        bootstrap.bullet("운영 표면과 프로젝트 표면이 서로 다른 역할을 유지하도록 정리한다."),
        bootstrap.text_block("heading_2", "상태"),
        bootstrap.bullet("상태 (Status): 진행 중"),
        bootstrap.bullet("진행률 % (Progress %): 90%"),
        bootstrap.text_block("heading_2", "현재 요약"),
        bootstrap.bullet("운영 센터 (ops center), 현재 상태 (current), 진행 기록 (reports), 점검 기록 (check log)의 stale 표면을 다시 맞췄다."),
        bootstrap.bullet("AI 세션 리포트 (AI Session Reports) DB의 중복 row를 정리하고 누락 속성을 보강했다."),
        bootstrap.bullet("세부 세션 흐름은 page-body table DB에 쌓고, 표면은 짧은 요약만 남긴다."),
        bootstrap.bullet(f"차트 표준 이름은 {status_chart}, {progress_chart}로 고정하되 생성과 연결은 사용자 수동 관리로 둔다."),
        bootstrap.text_block("heading_2", "다음 단계"),
        bootstrap.bullet("새 구조를 더 만들지 않고 제목 규칙과 상태 문구를 유지한다."),
        bootstrap.bullet("다음 단계 (next step)와 현재 초점 (current focus)은 page-body table DB로 넘긴다."),
        bootstrap.text_block("heading_2", "열린 이슈"),
        bootstrap.bullet("브라우저 자동화에서는 Notion이 비로그인 셸로만 열려 차트 뷰 (chart view) 자동 생성이 아직 불안정하다."),
        bootstrap.bullet("desktop app 접근성 트리는 얕아서 blind click 자동화에 적합하지 않았다."),
        bootstrap.text_block("heading_2", "기준 링크"),
        bootstrap.bullet(str(WORK_NOTE_PATH)),
    ]


def ensure_today_session_row(database_id: str) -> None:
    today_title = f"{TODAY} | 노션 구조 정리 | session report"
    status_chart, progress_chart = chart_view_names()
    rows = query_database_rows(database_id)
    target = None
    for row in rows:
        if title_text(row) == today_title:
            target = row
            break
    properties = {
        "Title": bootstrap.title_property(today_title),
        "상태 (Status)": {"select": {"name": "In Progress"}},
        "진행률 % (Progress %)": {"number": 90},
        "담당 에이전트 (Agent)": {"select": {"name": "Codex"}},
        "영역 (Area)": {"rich_text": rich_text("developer")},
        "프로젝트 / 세션 (Project / Session)": {"rich_text": rich_text("노션 구조 정리")},
        "시작일 (Started At)": {"date": {"start": TODAY}},
        "마지막 업데이트 (Last Updated)": {"date": {"start": TODAY}},
        "짧은 요약 (Summary)": {"rich_text": rich_text("노션 운영 표면 stale 정리, session reports 중복 제거, 현재 상태/진행 기록/점검 기록 재동기화와 제목 규칙 정리를 진행 중이다.")},
        "원본 경로 (Local Source)": {"rich_text": rich_text(str(WORK_NOTE_PATH))},
    }
    if target:
        bootstrap.notion_request(
            "PATCH",
            f"https://api.notion.com/v1/pages/{target['id']}",
            {"properties": properties, "icon": bootstrap.native_icon("document", "orange")},
            version=bootstrap.ICON_NOTION_VERSION,
        )
        bootstrap.replace_page_content(target["id"], row_blocks())
        print(f"[ok] updated session row {target['id']}", flush=True)
        return
    created_id = bootstrap.create_db_row(
        database_id=database_id,
        title=today_title,
        status="In Progress",
        progress=90,
        agent="Codex",
        area="developer",
        summary="노션 운영 표면 stale 정리, session reports 중복 제거, 현재 상태/진행 기록/점검 기록 재동기화와 제목 규칙 정리를 진행 중이다.",
        local_source=str(WORK_NOTE_PATH),
        blocks=row_blocks(),
    )
    bootstrap.notion_request(
        "PATCH",
        f"https://api.notion.com/v1/pages/{created_id}",
        {
            "properties": {
                "프로젝트 / 세션 (Project / Session)": {"rich_text": rich_text("노션 구조 정리")},
                "시작일 (Started At)": {"date": {"start": TODAY}},
                "마지막 업데이트 (Last Updated)": {"date": {"start": TODAY}},
            }
        },
        version=bootstrap.ICON_NOTION_VERSION,
    )
    print(f"[ok] created session row {created_id}", flush=True)


def refresh_ops_center(page_id: str) -> None:
    status_chart, progress_chart = chart_view_names()
    blocks = [
        bootstrap.callout("이 페이지는 운영 매뉴얼 (ops manual), 운영 로그, 세션 리포트로 들어가는 사람 중심 운영 입구다."),
        bootstrap.text_block("heading_2", "시작하기"),
        bootstrap.bullet("운영 기준은 운영 매뉴얼 (ops manual)에서 확인한다."),
        bootstrap.bullet("현재 운영 로그는 운영 로그 (ops log)에서 확인한다."),
        bootstrap.bullet("AI와 사람이 진행 중인 작업은 developer 아래 AI 세션 리포트 (AI Session Reports) DB에서 확인한다."),
        bootstrap.text_block("heading_2", "컬러 사용 매뉴얼"),
        bootstrap.bullet("중립 페이지는 회색 아이콘을 기본으로 쓰고, 컬러가 필요할 때만 쓴다."),
        bootstrap.bullet("갈색, 핑크, 보라색은 user-assigned로 둔다."),
        bootstrap.text_block("heading_2", "진척도 시각화"),
        bootstrap.bullet(bootstrap.progress_bar(90)),
        bootstrap.bullet("오늘 세션에서는 오래된 현재 상태 표면과 세션 리포트 drift를 우선 정리했다."),
        bootstrap.bullet(f"차트 표면은 AI 세션 리포트 (AI Session Reports) 안의 {status_chart}, {progress_chart} 두 뷰를 기준으로 보되 수동 UI 관리로 둔다."),
        bootstrap.text_block("heading_2", "구조도"),
        bootstrap.bullet("운영 센터 (ops center) → 운영 매뉴얼 (ops manual) → 운영 로그 (ops log) → 세션 리포트"),
        bootstrap.text_block("heading_2", "어떻게 운영하나"),
        bootstrap.bullet("긴 로그보다 현재 상태, 막힌 점, 다음 액션을 먼저 본다."),
        bootstrap.bullet("queue가 비어 있어도 현재 상태 (current), 진행 기록 (reports), 점검 기록 (check log), AI 세션 리포트 (AI Session Reports)를 함께 대조한다."),
        bootstrap.bullet("차트 뷰가 아직 없어도 현재 상태와 진행 기록이 먼저 truthful해야 한다."),
        bootstrap.bullet("차트 생성은 사용자 수동 관리로 두고, 에이전트는 DB 속성과 페이지 문구 정합성을 먼저 본다."),
    ]
    bootstrap.replace_page_content(page_id, blocks)
    bootstrap.update_page_icon(page_id, bootstrap.native_icon("home", "blue"))
    print("[ok] ops center refreshed", flush=True)


def refresh_hub(page_id: str) -> None:
    status_chart, progress_chart = chart_view_names()
    blocks = [
        bootstrap.callout("이 페이지는 노션 구조 정리 세션의 프로젝트 허브다."),
        bootstrap.text_block("heading_2", "무엇을 하는 곳인가"),
        bootstrap.bullet("대시보드, 운영 문서, 세션 리포트 구조를 인간 중심으로 정리한다."),
        bootstrap.bullet("현재 상태는 현재 상태 (current), 시점 기록은 진행 기록 (reports), 점검 항목은 점검 기록 (check log)에서 본다."),
        bootstrap.bullet("각 페이지의 세부 내용은 page-body table DB가 담당한다."),
        bootstrap.text_block("heading_2", "진척도 시각화"),
        bootstrap.bullet(bootstrap.progress_bar(90)),
        bootstrap.text_block("heading_2", "구조도"),
        bootstrap.bullet("노션 구조 정리 > 현재 상태 (current)"),
        bootstrap.bullet("노션 구조 정리 > 진행 기록 (reports)"),
        bootstrap.bullet("노션 구조 정리 > 점검 기록 (check log)"),
        bootstrap.bullet("노션 구조 정리 > 기준 자료 (references)"),
        bootstrap.text_block("heading_2", "현재 초점"),
        bootstrap.bullet("stale 현재 상태/진행 기록/점검 기록 정리"),
        bootstrap.bullet("AI 세션 리포트 (AI Session Reports) DB 중복 row 정리"),
        bootstrap.bullet(f"{status_chart}, {progress_chart} 차트 뷰는 수동 관리 표면으로 유지"),
        bootstrap.text_block("heading_2", "바로 가기"),
        bootstrap.bullet("현재 상태 (current)"),
        bootstrap.bullet("진행 기록 (reports)"),
        bootstrap.bullet("점검 기록 (check log)"),
        bootstrap.bullet("기준 자료 (references)"),
    ]
    bootstrap.replace_page_content(page_id, blocks)
    bootstrap.update_page_icon(page_id, bootstrap.native_icon("document", "orange"))
    print("[ok] notion structure hub refreshed", flush=True)


def refresh_current(page_id: str) -> None:
    status_chart, progress_chart = chart_view_names()
    blocks = [
        bootstrap.callout("현재 기준 상태만 짧게 보여주는 사람 중심 작업판이다."),
        bootstrap.text_block("heading_2", "목표"),
        bootstrap.bullet("초보 개발자도 지금 AI가 무엇을 하고 있는지 바로 이해할 수 있는 노션 구조를 만든다."),
        bootstrap.text_block("heading_2", "목적"),
        bootstrap.bullet("운영 문서, 세션 리포트, 프로젝트 허브의 역할을 분리해 탐색 비용을 낮춘다."),
        bootstrap.text_block("heading_2", "상태"),
        bootstrap.bullet("상태 (Status): 진행 중"),
        bootstrap.bullet("진행률 % (Progress %): 90%"),
        bootstrap.text_block("heading_2", "요약"),
        bootstrap.bullet("page-body table DB로 세부 기록을 쌓고, 표면은 현재 상태만 보여준다."),
        bootstrap.text_block("heading_2", "진척도 시각화"),
        bootstrap.bullet(bootstrap.progress_bar(90)),
        bootstrap.bullet(f"차트 표면 목표: {status_chart}, {progress_chart}"),
        bootstrap.text_block("heading_2", "인라인 로그 DB"),
        bootstrap.bullet(f"{now_display()} | current refresh | 다음 단계와 현재 초점을 page-body table DB 안에 둔다"),
        bootstrap.bullet(f"{now_display()} | current refresh | 현재 상태 / 진행 기록 / 점검 기록을 page-body table DB 표준과 맞춘다"),
        bootstrap.text_block("heading_2", "체크리스트"),
        bootstrap.bullet("ops center 표면을 최신 상태로 맞춘다."),
        bootstrap.bullet("AI Session Reports DB 중복과 누락 속성을 정리한다."),
        bootstrap.bullet("reports와 check log에 오늘 변경을 남긴다."),
        bootstrap.text_block("heading_2", "열린 이슈"),
        bootstrap.bullet("브라우저 자동화에서는 Notion이 비로그인 셸로 열려 차트 뷰 (chart view) 직접 생성이 아직 불안정하다."),
        bootstrap.bullet("그래도 사람 기준 첫 화면은 progress bar와 다음 단계 문구로 읽히게 유지한다."),
        bootstrap.text_block("heading_2", "기준 링크"),
        bootstrap.bullet("notion-queue-operating-standard.md"),
        bootstrap.bullet("notion-session-handoff-2026-03-29.md"),
    ]
    bootstrap.replace_page_content(page_id, blocks)
    bootstrap.update_page_icon(page_id, bootstrap.native_icon("document", "orange"))
    print("[ok] notion structure current refreshed", flush=True)


def refresh_reports_root(page_id: str) -> None:
    status_chart, progress_chart = chart_view_names()
    blocks = [
        bootstrap.callout("이 페이지는 날짜형 스냅샷과 시점 기록만 둔다."),
        bootstrap.text_block("heading_2", "입력 형식"),
        bootstrap.bullet("활성 상태가 바뀌면 current도 함께 갱신한다."),
        bootstrap.bullet("상세 로그는 로컬에 두고 여기에는 요약만 남긴다."),
        bootstrap.bullet("세부 항목은 page-body table DB에 쌓는다."),
        bootstrap.text_block("heading_2", "정본 규칙"),
        bootstrap.bullet("원문과 긴 reasoning은 로컬 상세 로그로 남기고 Notion에는 요약만 기록한다."),
        bootstrap.text_block("heading_2", "오늘 확인한 항목"),
        bootstrap.bullet("queue 상태와 surface freshness를 함께 본다."),
        bootstrap.bullet(f"차트 표면 기준 이름은 {status_chart}, {progress_chart}로 고정한다."),
    ]
    bootstrap.replace_page_content(page_id, blocks)
    bootstrap.update_page_icon(page_id, bootstrap.native_icon("document", "gray"))
    print("[ok] reports root refreshed", flush=True)


def ensure_report_entry(parent_id: str) -> None:
    status_chart, progress_chart = chart_view_names()
    blocks = [
        bootstrap.callout("이 페이지는 2026-03-29 노션 운영 표면 정리의 시점 기록이다."),
        bootstrap.text_block("heading_2", "변경 요약"),
        bootstrap.bullet("ops center와 current 허브의 오래된 진행률 / 다음 단계 문구를 최신 상태로 갱신했다."),
        bootstrap.bullet("AI Session Reports DB의 중복 row를 정리하고 누락 속성을 보강했다."),
        bootstrap.text_block("heading_2", "현재 상태"),
        bootstrap.bullet("진행률은 90%로 본다."),
        bootstrap.bullet(f"남은 핵심 과제는 {status_chart}, {progress_chart} 생성과 현재 상태 (current) 연결이다."),
        bootstrap.text_block("heading_2", "인라인 로그 DB"),
        bootstrap.bullet("2026-03-29 | session report | current/reports/check log child DB alignment"),
        bootstrap.bullet("2026-03-29 | session report | keep next step and current focus inside page-body table DB"),
        bootstrap.text_block("heading_2", "기준 링크"),
        bootstrap.bullet(str(WORK_NOTE_PATH)),
    ]
    bootstrap.ensure_page(parent_id, "2026-03-29 운영 정리", blocks, bootstrap.native_icon("document", "gray"))
    print("[ok] report entry ensured", flush=True)


def refresh_check_log_root(page_id: str) -> None:
    status_chart, progress_chart = chart_view_names()
    blocks = [
        bootstrap.callout("이 페이지는 점검, 경고, follow-up만 둔다."),
        bootstrap.text_block("heading_2", "열린 항목 규칙"),
        bootstrap.bullet("title 불일치, 구조 충돌, 수동 후속 조치를 여기에 남긴다."),
        bootstrap.text_block("heading_2", "보관 규칙"),
        bootstrap.bullet("완료된 항목은 접거나 archive 처리한다."),
        bootstrap.bullet("세부 점검 내역은 page-body table DB에 쌓는다."),
        bootstrap.text_block("heading_2", "현재 열린 항목"),
        bootstrap.bullet(f"{status_chart}, {progress_chart} 생성 및 연결"),
    ]
    bootstrap.replace_page_content(page_id, blocks)
    bootstrap.update_page_icon(page_id, bootstrap.native_icon("document", "yellow"))
    print("[ok] check log root refreshed", flush=True)


def ensure_check_item(parent_id: str) -> None:
    status_chart, progress_chart = chart_view_names()
    blocks = [
        bootstrap.callout("이 페이지는 차트 뷰 (chart view) 생성과 연결을 위한 열린 항목이다."),
        bootstrap.text_block("heading_2", "문제"),
        bootstrap.bullet("브라우저 자동화에서 Notion 페이지가 비로그인 셸로만 렌더되어 live UI 제어가 안정적이지 않았다."),
        bootstrap.bullet("desktop app 접근성 트리도 제한적이라 blind click 자동화를 안전하게 쓰기 어렵다."),
        bootstrap.text_block("heading_2", "다음 액션"),
        bootstrap.bullet(f"실제 로그인 세션에서 {status_chart}를 `상태 (Status)` 기준 도넛 차트로 만든다."),
        bootstrap.bullet(f"실제 로그인 세션에서 {progress_chart}를 `프로젝트 / 세션 (Project / Session)` x `진행률 % (Progress %)` 막대 차트로 만든다."),
        bootstrap.bullet("자동화가 계속 불안정하면 수동 chart 생성 절차를 표준화한다."),
        bootstrap.text_block("heading_2", "상태"),
        bootstrap.bullet("열림"),
    ]
    bootstrap.ensure_page(parent_id, "2026-03-29 차트 뷰 자동화 확인 (chart view)", blocks, bootstrap.native_icon("document", "yellow"))
    print("[ok] check item ensured", flush=True)


def main() -> int:
    bootstrap.load_env()
    config = json.loads((ROOT / "developer/projects/ai-workspace/config/notion_work_note_targets.json").read_text())
    session_db_id = config["session_reports"]["database_id"]
    project = config["projects"]["notion-structure-ops"]

    patch_database_properties(session_db_id)
    dedupe_session_rows(session_db_id)
    backfill_project_session(session_db_id)
    ensure_today_session_row(session_db_id)

    refresh_ops_center(config["ops_center"]["page_id"])
    refresh_hub(project["hub_page_id"])
    refresh_current(project["dashboard_page_id"])
    refresh_reports_root(project["reports_page_id"])
    ensure_report_entry(project["reports_page_id"])
    refresh_check_log_root(project["check_log_page_id"])
    ensure_check_item(project["check_log_page_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
