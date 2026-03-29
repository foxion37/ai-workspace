#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, request

ROOT = Path("/Users/barq")
ORCHESTRA_DIR = ROOT / ".orchestra"
WORK_NOTES_DIR = ORCHESTRA_DIR / "work-notes"
STATE_DIR = ORCHESTRA_DIR / "state"
LEDGER_PATH = STATE_DIR / "work-note-ledger.json"
QUEUE_PATH = STATE_DIR / "notion-sync-queue.json"
CONFIG_PATH = ROOT / "developer/projects/ai-workspace/config/notion_work_note_targets.json"
INCIDENT_DIR = ROOT / "AI-Workspace/knowledge-db/incidents"
TASK_DIR = ORCHESTRA_DIR / "tasks"
REPORT_ROOT = ROOT / "developer/home-dev-infra/reports"
SUMMARY_PATH = ORCHESTRA_DIR / "context/summary.md"
SESSION_REPORT_DIR = ROOT / "AI-Workspace/knowledge-db/session-reports"
SESSION_REPORT_INDEX_PATH = SESSION_REPORT_DIR / "INDEX.md"

IMPORTANT_TASK_STATUSES = {"blocked", "done", "self_review", "claude_review"}
OPEN_INCIDENT_STATUSES = {"open", "investigating", "blocked", "monitoring"}


@dataclass
class RouteInfo:
    kind: str
    scope_slug: str
    scope_title: str
    notion_target: str
    ops_parent_page_id: str | None = None
    project_hub_page_id: str | None = None
    dashboard_page_id: str | None = None
    reports_page_id: str | None = None
    check_log_page_id: str | None = None


def now_kst() -> datetime:
    return datetime.now().astimezone()


def iso_now() -> str:
    return now_kst().isoformat(timespec="seconds")


def display_now() -> str:
    return now_kst().strftime("%Y-%m-%d %H:%M %Z")


def ensure_runtime_dirs() -> None:
    WORK_NOTES_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return default


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True, sort_keys=True) + "\n")


def load_config() -> dict[str, Any]:
    return load_json(CONFIG_PATH, {})


def load_ledger() -> dict[str, Any]:
    default = {"notes": {}, "watch": {"tasks": {}, "incidents": {}, "reports": {}}}
    return load_json(LEDGER_PATH, default)


def save_ledger(data: dict[str, Any]) -> None:
    save_json(LEDGER_PATH, data)


def load_queue() -> list[dict[str, Any]]:
    data = load_json(QUEUE_PATH, [])
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return data
    # Recover from an earlier malformed save where (queue, errors) was serialized.
    if (
        isinstance(data, list)
        and len(data) == 2
        and isinstance(data[0], list)
        and all(isinstance(item, dict) for item in data[0])
    ):
        return data[0]
    return []


def save_queue(data: list[dict[str, Any]]) -> None:
    save_json(QUEUE_PATH, data)


def slugify(text: str) -> str:
    lowered = text.lower()
    chars = []
    for ch in lowered:
        if ch.isalnum():
            chars.append(ch)
        elif ch in {" ", "-", "_", "/"}:
            chars.append("-")
    slug = "".join(chars).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "note"


def run_git(args: list[str], repo_root: Path, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=check,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def detect_repo_root(cwd: Path) -> Path | None:
    current = cwd.resolve()
    while True:
        if (current / ".git").exists():
            return current
        if current == current.parent:
            return None
        current = current.parent


def parse_simple_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}
    data: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        if line.startswith("  - ") and current_key and current_list is not None:
            current_list.append(line[4:].strip())
            continue
        if ": " in line:
            key, value = line.split(": ", 1)
            current_key = key.strip()
            current_list = None
            if value.strip() == "":
                current_list = []
                data[current_key] = current_list
            else:
                data[current_key] = value.strip()
        elif line.endswith(":"):
            current_key = line[:-1].strip()
            current_list = []
            data[current_key] = current_list
    return data


def parse_task(path: Path) -> dict[str, Any]:
    text = path.read_text()
    status = "unknown"
    title = path.stem
    checklist_total = 0
    checklist_done = 0
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
        if line.startswith("- **Status**:"):
            status = line.split(":", 1)[1].strip()
        if line.lstrip().startswith("- ["):
            checklist_total += 1
            if line.lstrip().startswith("- [x]"):
                checklist_done += 1
    return {
        "path": str(path),
        "title": title,
        "status": status,
        "checklist_total": checklist_total,
        "checklist_done": checklist_done,
    }


def parse_incident(path: Path) -> dict[str, Any]:
    fm = parse_simple_frontmatter(path)
    return {
        "path": str(path),
        "title": fm.get("title", path.stem),
        "status": fm.get("status", "open"),
        "summary": fm.get("summary", ""),
        "related_tasks": fm.get("related_tasks", []) or [],
        "system": fm.get("system", []) or [],
    }


def iter_real_incident_files() -> list[Path]:
    excluded = {"INDEX.md", "TEMPLATE.md", "TAXONOMY.md"}
    paths: list[Path] = []
    if not INCIDENT_DIR.exists():
        return paths
    for path in sorted(INCIDENT_DIR.glob("*.md")):
        if path.name in excluded:
            continue
        fm = parse_simple_frontmatter(path)
        if not fm.get("id"):
            continue
        paths.append(path)
    return paths


def parse_report_status(path: Path) -> tuple[str, str]:
    try:
        text = path.read_text().lower()
    except OSError:
        return "missing", "report unreadable"
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            summary = stripped
            break
    else:
        summary = path.name
    if "status: success" in text or "result: success" in text:
        return "success", summary
    if "status: failed" in text or "failure" in text or "failed" in text or "blocked" in text:
        return "failed", summary
    if "warning" in text or "warn" in text:
        return "warning", summary
    return "info", summary


def find_related_tasks(repo_root: Path | None) -> list[dict[str, Any]]:
    if not TASK_DIR.exists():
        return []
    matches = []
    repo_name = repo_root.name if repo_root else ""
    repo_path = str(repo_root) if repo_root else ""
    for path in sorted(TASK_DIR.glob("*.md")):
        text = path.read_text()
        if repo_name and repo_name in text or repo_path and repo_path in text:
            matches.append(parse_task(path))
    return matches


def find_related_incidents(repo_root: Path | None) -> list[dict[str, Any]]:
    matches = []
    repo_name = repo_root.name if repo_root else ""
    repo_path = str(repo_root) if repo_root else ""
    for path in iter_real_incident_files():
        text = path.read_text()
        if repo_name and repo_name in text or repo_path and repo_path in text:
            matches.append(parse_incident(path))
    return matches


def checklist_progress(tasks: list[dict[str, Any]]) -> int | None:
    total = sum(task["checklist_total"] for task in tasks)
    done = sum(task["checklist_done"] for task in tasks)
    if total <= 0:
        return None
    return int((done / total) * 100)


def summarize_open_issues(tasks: list[dict[str, Any]], incidents: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    for task in tasks:
        if task["status"] == "blocked":
            issues.append(f"Blocked task: {task['title']} ({task['path']})")
    for incident in incidents:
        if incident["status"] in OPEN_INCIDENT_STATUSES:
            issues.append(f"{incident['status']}: {incident['title']} ({incident['path']})")
    return issues[:5]


def load_env_from_known_files() -> None:
    candidates = [
        ROOT / ".dotfiles/.env",
        ROOT / "developer/notion-auto-sync/.env",
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            for line in path.read_text().splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                key = key.strip()
                if key.startswith("export "):
                    key = key[len("export ") :].strip()
                if key and key not in os.environ:
                    os.environ[key] = value.strip().strip('"').strip("'")
        except OSError:
            continue
    if "NOTION_API_KEY" not in os.environ and "NOTION_AGENT_TOKEN" in os.environ:
        os.environ["NOTION_API_KEY"] = os.environ["NOTION_AGENT_TOKEN"]


def route_for_repo(repo_root: Path | None, config: dict[str, Any]) -> RouteInfo:
    repo_overrides = config.get("repo_overrides", {})
    projects = config.get("projects", {})
    ops = config.get("ops", {})

    if repo_root is None:
        return RouteInfo(
            kind="ops",
            scope_slug="global",
            scope_title="global",
            notion_target=ops.get("route", "dashboard > notion manual 1.0 > ops log"),
            ops_parent_page_id=ops.get("page_id"),
        )

    repo_name = repo_root.name
    override = repo_overrides.get(repo_name)
    if override == "ops":
        return RouteInfo(
            kind="ops",
            scope_slug=slugify(repo_name),
            scope_title=repo_name,
            notion_target=ops.get("route", "dashboard > notion manual 1.0 > ops log"),
            ops_parent_page_id=ops.get("page_id"),
        )

    project = projects.get(repo_name)
    if project:
        return RouteInfo(
            kind="project",
            scope_slug=slugify(repo_name),
            scope_title=project.get("title", repo_name),
            notion_target=project.get("route", f"dashboard > developer > {repo_name}"),
            project_hub_page_id=project.get("hub_page_id"),
            dashboard_page_id=project.get("dashboard_page_id"),
            reports_page_id=project.get("reports_page_id"),
            check_log_page_id=project.get("check_log_page_id"),
        )

    if str(repo_root).startswith(str(ROOT / "developer/projects/")):
        return RouteInfo(
            kind="project",
            scope_slug=slugify(repo_name),
            scope_title=repo_name,
            notion_target=f"dashboard > developer > {repo_name}",
        )

    return RouteInfo(
        kind="ops",
        scope_slug=slugify(repo_name),
        scope_title=repo_name,
        notion_target=ops.get("route", "dashboard > notion manual 1.0 > ops log"),
        ops_parent_page_id=ops.get("page_id"),
    )


def route_parent_page_id(route: RouteInfo) -> str | None:
    if route.kind == "ops":
        return route.ops_parent_page_id
    return route.reports_page_id


def status_label(status: str) -> str:
    mapping = {
        "in_progress": "In Progress",
        "blocked": "Blocked",
        "done": "Done",
        "monitoring": "Monitoring",
        "warning": "Warning",
        "success": "Success",
        "failed": "Failed",
        "self_review": "Self Review",
        "claude_review": "Claude Review",
        "start": "Started",
        "save": "Checkpoint",
        "finish": "Finished",
        "info": "Info",
    }
    return mapping.get(status, status.replace("_", " ").title())


def note_goal(route: RouteInfo) -> str:
    if route.kind == "project":
        return f"{route.scope_title} 작업의 현재 상태와 다음 행동을 사람 기준으로 이해 가능하게 유지한다."
    return f"{route.scope_title} 관련 운영 변화와 후속 조치를 빠르게 복원 가능하게 기록한다."


def note_purpose(route: RouteInfo) -> str:
    if route.kind == "project":
        return "초보 개발자도 이 페이지 하나만 보면 지금 무엇을 하는지, 어디가 막혔는지, 다음에 무엇부터 해야 하는지 알 수 있게 한다."
    return "공유 운영 변화가 흩어지지 않게 모으고, 다음 세션에서 같은 판단을 반복하지 않게 한다."


def checklist_items(tasks: list[dict[str, Any]]) -> list[str]:
    items: list[str] = []
    for task in tasks[:6]:
        marker = "x" if task["status"] == "done" else " "
        suffix = ""
        if task["status"] not in {"done", "unknown"}:
            suffix = f" ({task['status']})"
        items.append(f"- [{marker}] {task['title']}{suffix}")
    return items or ["- [ ] Task checklist not linked yet"]


def note_progress(status: str, tasks: list[dict[str, Any]]) -> int:
    progress = checklist_progress(tasks)
    if progress is not None:
        if progress >= 100 and status not in {"done", "success"}:
            return 90
        return progress
    if status in {"done", "success"}:
        return 100
    if status in {"blocked", "failed"}:
        return 0
    return 15


def current_focus(route: RouteInfo, tasks: list[dict[str, Any]], incidents: list[dict[str, Any]]) -> str:
    blocked = next((task for task in tasks if task["status"] == "blocked"), None)
    if blocked:
        return f"Blocked task: {blocked['title']}"
    open_incident = next((incident for incident in incidents if incident["status"] in OPEN_INCIDENT_STATUSES), None)
    if open_incident:
        return f"Open incident: {open_incident['title']}"
    if tasks:
        return f"Active task: {tasks[0]['title']}"
    if route.kind == "project":
        return "Project current page and next step alignment"
    return "Shared operating changes and follow-up"


def active_work_items(note: dict[str, Any], route: RouteInfo) -> list[str]:
    recent_changes = note.get("changes", [])[-3:]
    if recent_changes:
        return recent_changes
    if route.kind == "project":
        return ["Project session started; fill current focus, blockers, and next step."]
    return ["Ops session started; collect relevant changes and keep the log short."]


def human_guidance(note: dict[str, Any], route: RouteInfo) -> list[str]:
    lines = [
        f"지금 상태: {status_label(note['status'])}, 진행률: {note.get('progress', 0)}%",
        f"다음에 열면 먼저 볼 것: {note.get('current_focus', 'current focus not set')}",
        f"바로 할 일: {note.get('next_step', 'next step not set')}",
    ]
    if route.kind == "project":
        lines.append("세부 변경 기록보다 Active Work와 Checklist를 먼저 본다.")
    else:
        lines.append("세부 로그보다 Open Issues와 Next Step을 먼저 본다.")
    return lines


def update_log_items(note: dict[str, Any], mode: str) -> list[str]:
    items = list(note.get("update_log", []))
    items.append(f"{display_now()} | {status_label(mode)} | {note['summary']}")
    return items[-12:]


def enrich_note(note: dict[str, Any], route: RouteInfo, tasks: list[dict[str, Any]], incidents: list[dict[str, Any]], mode: str) -> None:
    note["goal"] = note_goal(route)
    note["purpose"] = note_purpose(route)
    note["progress"] = note_progress(note["status"], tasks)
    note["current_focus"] = current_focus(route, tasks, incidents)
    note["active_work"] = active_work_items(note, route)[:5]
    note["open_issues"] = summarize_open_issues(tasks, incidents)[:5]
    note["checklist"] = checklist_items(tasks)
    note["human_guidance"] = human_guidance(note, route)
    note["update_log"] = update_log_items(note, mode)


def render_session_report_index(ledger: dict[str, Any]) -> str:
    notes = list(ledger.get("notes", {}).values())
    notes.sort(key=lambda item: item.get("date_updated", ""), reverse=True)
    active = [note for note in notes if note.get("status") not in {"done", "success"}][:20]
    recent = notes[:20]
    lines = [
        "# Session Reports",
        "",
        "이 문서는 로컬 세션 리포트 인덱스다.",
        "인간이 지금 어떤 작업이 진행 중인지 빠르게 파악하는 용도로만 쓴다.",
        "",
        "## Active Now",
        "",
        "| Session | Status | Progress | Updated | Next Step |",
        "| --- | --- | --- | --- | --- |",
    ]
    if not active:
        lines.append("| none | - | - | - | - |")
    for note in active:
        session_name = note.get("scope", note["title"])
        lines.append(
            f"| {session_name} | {status_label(note['status'])} | {note.get('progress', 0)}% | {note.get('date_updated', '-')[:16]} | {note.get('next_step', '-')} |"
        )
    lines.extend(
        [
            "",
            "## Recently Updated",
            "",
            "| Session | Status | Updated | Scope |",
            "| --- | --- | --- | --- |",
        ]
    )
    if not recent:
        lines.append("| none | - | - | - |")
    for note in recent:
        session_name = note.get("scope", note["title"])
        lines.append(
            f"| {session_name} | {status_label(note['status'])} | {note.get('date_updated', '-')[:16]} | {note.get('scope', '-')} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_session_report_index(ledger: dict[str, Any]) -> None:
    SESSION_REPORT_INDEX_PATH.write_text(render_session_report_index(ledger))


def render_work_note(note: dict[str, Any]) -> str:
    def list_block(items: list[str]) -> str:
        if not items:
            return "  -\n"
        return "".join(f"  - {item}\n" for item in items)

    lines = [
        "---",
        f"id: {note['id']}",
        f"type: {note['type']}",
        f"status: {note['status']}",
        f"scope: {note['scope']}",
        f"repo: {note.get('repo', '')}",
        f"date_opened: {note['date_opened']}",
        f"date_updated: {note['date_updated']}",
        f"summary: {note['summary']}",
        f"progress: {note.get('progress', 0)}",
        "related_tasks:",
        list_block(note.get("related_tasks", [])),
        "related_incidents:",
        list_block(note.get("related_incidents", [])),
        "local_refs:",
        list_block(note.get("local_refs", [])),
        f"notion_target: {note['notion_target']}",
        f"notion_sync: {note['notion_sync']}",
        f"notion_page_id: {note.get('notion_page_id', '')}",
        "---",
        "",
        f"# {note['title']}",
        "",
        "## Goal",
        f"- {note.get('goal', 'Goal not set')}",
        "",
        "## Purpose",
        f"- {note.get('purpose', 'Purpose not set')}",
        "",
        "## Current Board",
        f"- Status: {status_label(note['status'])}",
        f"- Progress: {note.get('progress', 0)}%",
        f"- Scope: {note['scope']}",
        f"- Route: {note['notion_target']}",
        f"- Last Updated: {note['date_updated']}",
        "",
        "## Situation",
        f"- {note['situation']}",
        "",
        "## Current Focus",
        f"- {note.get('current_focus', 'Current focus not set')}",
        "",
        "## Active Work",
    ]
    lines.extend(f"- {item}" for item in note.get("active_work", []))
    lines.extend(
        [
            "",
            "## Checklist",
        ]
    )
    lines.extend(note.get("checklist", []))
    lines.extend(
        [
            "",
            "## Open Issues",
        ]
    )
    lines.extend(f"- {item}" for item in note.get("open_issues", []) or ["- none"])
    lines.extend(
        [
            "",
            "## For Human",
        ]
    )
    lines.extend(f"- {item}" for item in note.get("human_guidance", []))
    lines.extend(
        [
            "",
            "## Update Log",
        ]
    )
    lines.extend(f"- {item}" for item in note.get("update_log", []))
    lines.extend(
        [
            "",
            "## References",
        ]
    )
    lines.extend(f"- {item}" for item in note.get("local_refs", []))
    lines.extend(
        [
            "",
            "## Next Step",
            f"- {note['next_step']}",
            "",
        ]
    )
    return "\n".join(lines).replace("\n  -\n", "\n")


def enqueue_notion_sync(queue: list[dict[str, Any]], note: dict[str, Any], route: RouteInfo) -> None:
    parent_id = route_parent_page_id(route)
    if not parent_id:
        note["notion_sync"] = "not_configured"
        return
    payload = {
        "note_id": note["id"],
        "kind": route.kind,
        "title": note["title"],
        "parent_page_id": parent_id,
        "content_markdown": build_notion_markdown(note),
        "page_id": note.get("notion_page_id"),
        "dashboard_page_id": route.dashboard_page_id,
        "notion_target": route.notion_target,
        "updated_at": note["date_updated"],
    }
    fingerprint = hashlib.sha1(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    existing_index = next((i for i, item in enumerate(queue) if item.get("note_id") == note["id"]), None)
    if existing_index is not None and queue[existing_index].get("fingerprint") == fingerprint:
        note["notion_sync"] = "pending"
        return
    payload["fingerprint"] = fingerprint
    if existing_index is not None:
        queue[existing_index] = payload
    else:
        queue.append(payload)
    note["notion_sync"] = "pending"


def notion_request(method: str, url: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    token = os.environ.get("NOTION_API_KEY")
    if not token:
        raise RuntimeError("NOTION_API_KEY missing")
    req = request.Request(
        url,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        method=method,
    )
    with request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_paragraph_block(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text[:1900]}}],
        },
    }


def build_quote_block(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "quote",
        "quote": {
            "rich_text": [{"type": "text", "text": {"content": text[:1900]}}],
        },
    }


def build_heading_block(level: int, text: str) -> dict[str, Any]:
    block_type = f"heading_{level}"
    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": [{"type": "text", "text": {"content": text[:1900]}}],
        },
    }


def build_bulleted_block(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text[:1900]}}],
        },
    }


def build_todo_block(text: str, checked: bool) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "checked": checked,
            "rich_text": [{"type": "text", "text": {"content": text[:1900]}}],
        },
    }


def page_title_payload(title: str) -> dict[str, Any]:
    return {
        "title": {
            "title": [{"type": "text", "text": {"content": title[:180]}}]
        }
    }


def list_block_children(page_id: str) -> list[str]:
    data = notion_request("GET", f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100")
    return [item["id"] for item in data.get("results", []) if item.get("id")]


def clear_page_children(page_id: str) -> None:
    for child_id in list_block_children(page_id):
        notion_request(
            "PATCH",
            f"https://api.notion.com/v1/blocks/{child_id}",
            {"archived": True},
        )


def replace_page_children(page_id: str, content_markdown: str) -> None:
    clear_page_children(page_id)
    blocks: list[dict[str, Any]] = []
    for raw_line in content_markdown.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("> "):
            blocks.append(build_quote_block(stripped[2:].strip()))
            continue
        if stripped.startswith("## "):
            blocks.append(build_heading_block(2, stripped[3:].strip()))
            continue
        if stripped.startswith("### "):
            blocks.append(build_heading_block(3, stripped[4:].strip()))
            continue
        if stripped.startswith("- [ ] "):
            blocks.append(build_todo_block(stripped[6:].strip(), checked=False))
            continue
        if stripped.startswith("- [x] "):
            blocks.append(build_todo_block(stripped[6:].strip(), checked=True))
            continue
        if stripped.startswith("- "):
            blocks.append(build_bulleted_block(stripped[2:].strip()))
            continue
        blocks.append(build_paragraph_block(stripped))
    if blocks:
        notion_request(
            "PATCH",
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            {"children": blocks[:80]},
        )


def build_notion_markdown(note: dict[str, Any]) -> str:
    refs = "\n".join(f"- {item}" for item in note.get("local_refs", [])[:3]) or "- none"
    active = "\n".join(f"- {item}" for item in note.get("active_work", [])[:4]) or "- none"
    checklist = "\n".join(note.get("checklist", [])[:6]) or "- [ ] checklist not linked"
    issues = "\n".join(f"- {item}" for item in note.get("open_issues", [])[:4]) or "- none"
    human = "\n".join(f"- {item}" for item in note.get("human_guidance", [])[:4]) or "- none"
    return (
        "> This page is the live human-readable status mirror.\n\n"
        f"## Goal\n- {note.get('goal', 'Goal not set')}\n\n"
        f"## Purpose\n- {note.get('purpose', 'Purpose not set')}\n\n"
        f"## Status\n- Status: {status_label(note['status'])}\n- Progress: {note.get('progress', 0)}%\n- Route: {note['notion_target']}\n\n"
        f"## Owner\n- Codex\n\n"
        f"## Next Step\n- {note['next_step']}\n\n"
        f"## Last Updated\n- {note['date_updated']}\n\n"
        f"## Current Focus\n- {note.get('current_focus', 'Current focus not set')}\n\n"
        f"## Active Work\n{active}\n\n"
        f"## Checklist\n{checklist}\n\n"
        f"## Open Issues\n{issues}\n\n"
        f"## Canonical Links\n{refs}\n\n"
        f"## For Human\n{human}\n\n"
        f"## Situation\n- {note['situation']}\n"
    )


def sync_queue(queue: list[dict[str, Any]], dry_run: bool) -> tuple[list[dict[str, Any]], list[str], dict[str, str]]:
    if not queue:
        return [], [], {}
    load_env_from_known_files()
    if dry_run or not os.environ.get("NOTION_API_KEY"):
        return queue, [], {}

    remaining: list[dict[str, Any]] = []
    errors: list[str] = []
    synced: dict[str, str] = {}
    for item in queue:
        try:
            page_id = item.get("page_id")
            if page_id:
                notion_request(
                    "PATCH",
                    f"https://api.notion.com/v1/pages/{page_id}",
                    {"properties": page_title_payload(item["title"])},
                )
            else:
                page = notion_request(
                    "POST",
                    "https://api.notion.com/v1/pages",
                    {
                        "parent": {"page_id": item["parent_page_id"]},
                        "properties": page_title_payload(item["title"]),
                    },
                )
                page_id = page["id"]
            replace_page_children(page_id, item["content_markdown"])
            synced[item["note_id"]] = page_id
        except RuntimeError as exc:
            remaining.append(item)
            errors.append(f"{item['title']}: {exc}")
        except error.HTTPError as exc:
            remaining.append(item)
            try:
                message = exc.read().decode("utf-8")
            except OSError:
                message = str(exc)
            errors.append(f"{item['title']}: HTTP {exc.code} {message[:240]}")
        except (error.URLError, KeyError) as exc:
            remaining.append(item)
            errors.append(f"{item['title']}: {exc}")
    return remaining, errors, synced


def queue_summary_lines(queue: list[dict[str, Any]]) -> list[str]:
    if not queue:
        return ["[queue] empty"]
    grouped: dict[str, int] = {}
    for item in queue:
        target = item.get("notion_target", "unknown")
        grouped[target] = grouped.get(target, 0) + 1
    lines = [f"[queue] pending={len(queue)}"]
    for target, count in sorted(grouped.items()):
        lines.append(f"[target] {target} ({count})")
    for item in queue[:5]:
        lines.append(f"[item] {item['title']} -> {item['notion_target']}")
    return lines


def write_note(note: dict[str, Any], ledger: dict[str, Any]) -> Path:
    note_path = WORK_NOTES_DIR / f"{note['id']}.md"
    note_path.write_text(render_work_note(note))
    ledger.setdefault("notes", {})[note["id"]] = note
    write_session_report_index(ledger)
    return note_path


def upsert_note(
    *,
    route: RouteInfo,
    mode: str,
    repo_path: str,
    status: str,
    summary: str,
    situation: str,
    changes: list[str],
    why_it_matters: list[str],
    refs: list[str],
    next_step: str,
    related_tasks: list[str],
    related_incidents: list[str],
    tasks: list[dict[str, Any]],
    incidents: list[dict[str, Any]],
    dry_run: bool,
) -> tuple[dict[str, Any], Path | None]:
    ensure_runtime_dirs()
    ledger = load_ledger()
    queue = load_queue()
    day = now_kst().strftime("%Y-%m-%d")
    note_id = f"{day}__{route.kind}__{route.scope_slug}"
    note = ledger.setdefault("notes", {}).get(note_id)
    if not note:
        note = {
            "id": note_id,
            "type": f"{route.kind}_note",
            "title": f"{day} | {route.scope_title} | work note",
            "status": status,
            "scope": route.scope_title,
            "repo": repo_path,
            "date_opened": iso_now(),
            "date_updated": iso_now(),
            "summary": summary,
            "related_tasks": [],
            "related_incidents": [],
            "local_refs": [],
            "notion_target": route.notion_target,
            "notion_sync": "pending",
            "notion_page_id": "",
            "situation": situation,
            "changes": [],
            "why_it_matters": [],
            "next_step": next_step,
            "update_log": [],
        }
    note["status"] = status
    note["repo"] = repo_path
    note["date_updated"] = iso_now()
    note["summary"] = summary
    note["situation"] = situation
    note["next_step"] = next_step
    note["changes"] = list(dict.fromkeys(note.get("changes", []) + changes))[-10:]
    note["why_it_matters"] = list(dict.fromkeys(note.get("why_it_matters", []) + why_it_matters))[-6:]
    note["local_refs"] = list(dict.fromkeys(note.get("local_refs", []) + refs))[:10]
    note["related_tasks"] = list(dict.fromkeys(note.get("related_tasks", []) + related_tasks))[:10]
    note["related_incidents"] = list(dict.fromkeys(note.get("related_incidents", []) + related_incidents))[:10]
    enrich_note(note, route, tasks, incidents, mode)
    enqueue_notion_sync(queue, note, route)
    if not dry_run:
        note_path = write_note(note, ledger)
        remaining_queue, _sync_errors, synced_pages = sync_queue(queue, dry_run=False)
        if note["id"] in synced_pages:
            note["notion_page_id"] = synced_pages[note["id"]]
            note["notion_sync"] = "synced"
        write_note(note, ledger)
        save_ledger(ledger)
        save_queue(remaining_queue)
        return note, note_path
    return note, None


def default_next_step(route: RouteInfo, tasks: list[dict[str, Any]], incidents: list[dict[str, Any]]) -> str:
    for task in tasks:
        if task["status"] == "blocked":
            return f"Unblock task: {task['title']}"
    for incident in incidents:
        if incident["status"] in OPEN_INCIDENT_STATUSES:
            return f"Review incident: {incident['title']}"
    if route.kind == "project":
        return "Update the dashboard current page and keep reports/check log in sync."
    return "Review ops log and pending incidents."


def command_context(args: argparse.Namespace) -> int:
    ensure_runtime_dirs()
    cwd = Path(args.cwd or os.getcwd())
    repo_root = Path(args.repo_root) if args.repo_root else detect_repo_root(cwd)
    ledger = load_ledger()
    route = route_for_repo(repo_root, load_config())
    tasks = find_related_tasks(repo_root)
    incidents = find_related_incidents(repo_root)
    blocked = [task for task in tasks if task["status"] == "blocked"]
    latest_note = None
    note_prefix = f"{now_kst().strftime('%Y-%m-%d')}__{route.kind}__{route.scope_slug}"
    latest_note = ledger.get("notes", {}).get(note_prefix)
    lines = [
        f"[scope] {route.scope_title} -> {route.notion_target}",
        f"[tasks] related={len(tasks)} blocked={len(blocked)}",
        f"[incidents] open={len([i for i in incidents if i['status'] in OPEN_INCIDENT_STATUSES])}",
    ]
    progress = checklist_progress(tasks)
    if progress is not None:
        lines.append(f"[progress] {progress}% from checklist")
    if latest_note:
        lines.append(f"[latest-note] {latest_note['summary']}")
    for issue in summarize_open_issues(tasks, incidents)[:3]:
        lines.append(f"[issue] {issue}")
    if SUMMARY_PATH.exists():
        lines.append(f"[summary] {SUMMARY_PATH}")
    print("\n".join(lines))
    return 0


def command_start(args: argparse.Namespace) -> int:
    cwd = Path(args.cwd or os.getcwd())
    repo_root = Path(args.repo_root) if args.repo_root else detect_repo_root(cwd)
    route = route_for_repo(repo_root, load_config())
    tasks = find_related_tasks(repo_root)
    incidents = find_related_incidents(repo_root)
    summary = args.summary or f"{route.scope_title}: session started"
    if repo_root:
        situation = args.situation or f"{repo_root.name} 세션이 시작됐고, 현재 상태를 사람 기준 리포트로 초기화했다."
        refs = [str(repo_root)]
    else:
        situation = args.situation or f"{route.scope_title} 세션이 시작됐고, 현재 상태를 사람 기준 리포트로 초기화했다."
        refs = []
    next_step = args.next_step or default_next_step(route, tasks, incidents)
    note, note_path = upsert_note(
        route=route,
        mode="start",
        repo_path=str(repo_root) if repo_root else "",
        status=args.status,
        summary=summary,
        situation=situation,
        changes=[f"{display_now()} session started from {cwd}"],
        why_it_matters=["세션 시작 시점의 상태를 사람과 에이전트가 함께 복원할 수 있게 한다."],
        refs=refs,
        next_step=next_step,
        related_tasks=[task["path"] for task in tasks[:5]],
        related_incidents=[incident["path"] for incident in incidents[:5]],
        tasks=tasks,
        incidents=incidents,
        dry_run=args.dry_run,
    )
    if args.dry_run:
        print(json.dumps(note, ensure_ascii=False, indent=2))
    else:
        print(note_path)
    return 0


def command_record(args: argparse.Namespace) -> int:
    cwd = Path(args.cwd or os.getcwd())
    repo_root = Path(args.repo_root) if args.repo_root else detect_repo_root(cwd)
    route = route_for_repo(repo_root, load_config())
    tasks = find_related_tasks(repo_root)
    incidents = find_related_incidents(repo_root)
    changes: list[str] = []
    refs: list[str] = []
    summary = args.summary
    situation = args.situation

    if repo_root:
        try:
            commit_subject = run_git(["log", "-1", "--pretty=%s"], repo_root)
            commit_hash = run_git(["rev-parse", "--short", "HEAD"], repo_root)
            changed_files = [
                line
                for line in run_git(["show", "--name-only", "--format=", "HEAD"], repo_root).splitlines()
                if line.strip()
            ]
            summary = summary or f"{repo_root.name}: {commit_subject}"
            situation = situation or f"{repo_root.name} 작업 상태가 {args.mode} 단계에서 정리됐다."
            changes.append(f"{display_now()} commit {commit_hash}: {commit_subject}")
            refs.extend(str(repo_root / path) for path in changed_files[:5])
        except subprocess.CalledProcessError:
            summary = summary or f"{route.scope_title}: work note update"
            situation = situation or f"{route.scope_title}의 현재 상태를 기록했다."
    else:
        summary = summary or f"{route.scope_title}: work note update"
        situation = situation or f"{route.scope_title}의 현재 상태를 기록했다."

    changes.extend(args.change or [])
    refs.extend(args.ref or [])
    related_tasks = [task["path"] for task in tasks[:5]]
    related_incidents = [incident["path"] for incident in incidents[:5]]
    why_it_matters = summarize_open_issues(tasks, incidents) or [
        "다음 세션에서 현재 상태를 빠르게 복원할 수 있게 한다."
    ]
    next_step = args.next_step or default_next_step(route, tasks, incidents)
    note, note_path = upsert_note(
        route=route,
        mode=args.mode,
        repo_path=str(repo_root) if repo_root else "",
        status=args.status,
        summary=summary,
        situation=situation,
        changes=changes,
        why_it_matters=why_it_matters,
        refs=list(dict.fromkeys(refs)),
        next_step=next_step,
        related_tasks=related_tasks,
        related_incidents=related_incidents,
        tasks=tasks,
        incidents=incidents,
        dry_run=args.dry_run,
    )
    if args.dry_run:
        print(json.dumps(note, ensure_ascii=False, indent=2))
    else:
        print(note_path)
    return 0


def record_watch_event(
    *,
    route: RouteInfo,
    mode: str,
    status: str,
    summary: str,
    situation: str,
    ref_path: str,
    next_step: str,
    dry_run: bool,
) -> None:
    upsert_note(
        route=route,
        mode=mode,
        repo_path="",
        status=status,
        summary=summary,
        situation=situation,
        changes=[f"{display_now()} detected: {summary}"],
        why_it_matters=[situation],
        refs=[ref_path],
        next_step=next_step,
        related_tasks=[],
        related_incidents=[],
        tasks=[],
        incidents=[],
        dry_run=dry_run,
    )


def watch_once(dry_run: bool, quiet: bool) -> int:
    ensure_runtime_dirs()
    ledger = load_ledger()
    config = load_config()
    watch_state = ledger.setdefault("watch", {"tasks": {}, "incidents": {}, "reports": {}})

    for path in sorted(TASK_DIR.glob("*.md")):
        task = parse_task(path)
        previous = watch_state["tasks"].get(str(path))
        current = {"status": task["status"], "mtime": path.stat().st_mtime}
        if previous is None:
            watch_state["tasks"][str(path)] = current
            continue
        if previous != current:
            watch_state["tasks"][str(path)] = current
            if task["status"] in IMPORTANT_TASK_STATUSES:
                route = route_for_repo(None, config)
                record_watch_event(
                    route=route,
                    mode="watch",
                    status=task["status"],
                    summary=f"Task state changed: {task['title']} -> {task['status']}",
                    situation="중요 task 상태 전환이 발생했다.",
                    ref_path=str(path),
                    next_step=f"Review task status: {path}",
                    dry_run=dry_run,
                )
                if not quiet:
                    print(f"[task] {path} -> {task['status']}")

    for path in iter_real_incident_files():
        incident = parse_incident(path)
        previous = watch_state["incidents"].get(str(path))
        current = {"status": incident["status"], "mtime": path.stat().st_mtime}
        if previous is None:
            watch_state["incidents"][str(path)] = current
            continue
        if previous != current:
            watch_state["incidents"][str(path)] = current
            route = route_for_repo(None, config)
            record_watch_event(
                route=route,
                mode="watch",
                status=incident["status"],
                summary=f"Incident updated: {incident['title']} -> {incident['status']}",
                situation="반복 확인이 필요한 incident 상태가 바뀌었다.",
                ref_path=str(path),
                next_step=f"Review incident: {path}",
                dry_run=dry_run,
            )
            if not quiet:
                print(f"[incident] {path} -> {incident['status']}")

    for path in sorted(REPORT_ROOT.glob("**/latest.md")):
        report_status, report_summary = parse_report_status(path)
        previous = watch_state["reports"].get(str(path))
        current = {"status": report_status, "mtime": path.stat().st_mtime}
        if previous is None:
            watch_state["reports"][str(path)] = current
            continue
        if previous != current:
            watch_state["reports"][str(path)] = current
            if previous.get("status") != report_status or report_status in {"failed", "warning"}:
                route = route_for_repo(ROOT / "developer/home-dev-infra", config)
                record_watch_event(
                    route=route,
                    mode="watch",
                    status=report_status,
                    summary=f"Report changed: {path.parent.name}/latest.md -> {report_status}",
                    situation=report_summary,
                    ref_path=str(path),
                    next_step=f"Check latest report: {path}",
                    dry_run=dry_run,
                )
                if not quiet:
                    print(f"[report] {path} -> {report_status}")

    if not dry_run:
        save_ledger(ledger)
    return 0


def command_watch_once(args: argparse.Namespace) -> int:
    return watch_once(dry_run=args.dry_run, quiet=args.quiet)


def command_watch(args: argparse.Namespace) -> int:
    while True:
        watch_once(dry_run=args.dry_run, quiet=args.quiet)
        time.sleep(args.interval)


def command_queue_status(args: argparse.Namespace) -> int:
    del args
    ensure_runtime_dirs()
    queue = load_queue()
    print("\n".join(queue_summary_lines(queue)))
    return 0


def command_sync(args: argparse.Namespace) -> int:
    ensure_runtime_dirs()
    queue = load_queue()
    if not queue:
        print("[sync] queue empty")
        return 0

    load_env_from_known_files()
    has_api_key = bool(os.environ.get("NOTION_API_KEY"))
    remaining_queue, sync_errors, synced_pages = sync_queue(queue, dry_run=args.dry_run)
    synced = len(queue) - len(remaining_queue)
    if not args.dry_run and synced_pages:
        ledger = load_ledger()
        for note_id, page_id in synced_pages.items():
            note = ledger.get("notes", {}).get(note_id)
            if not note:
                continue
            note["notion_page_id"] = page_id
            note["notion_sync"] = "synced"
        save_ledger(ledger)

    lines = [
        f"[sync] attempted={len(queue)} synced={synced} remaining={len(remaining_queue)}",
    ]
    if args.dry_run:
        lines.append("[mode] dry-run")
    elif not has_api_key:
        lines.append("[status] waiting_for_api_key")
    for sync_error in sync_errors[:5]:
        lines.append(f"[error] {sync_error}")

    lines.extend(queue_summary_lines(remaining_queue))

    if not args.dry_run:
        save_queue(remaining_queue)

    print("\n".join(lines))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    context = sub.add_parser("context")
    context.add_argument("--cwd")
    context.add_argument("--repo-root")
    context.set_defaults(func=command_context)

    start = sub.add_parser("start")
    start.add_argument("--cwd")
    start.add_argument("--repo-root")
    start.add_argument("--summary")
    start.add_argument("--situation")
    start.add_argument("--next-step")
    start.add_argument("--status", default="in_progress")
    start.add_argument("--dry-run", action="store_true")
    start.set_defaults(func=command_start)

    for mode in ("save", "finish"):
        record = sub.add_parser(mode)
        record.add_argument("--cwd")
        record.add_argument("--repo-root")
        record.add_argument("--summary")
        record.add_argument("--situation")
        record.add_argument("--next-step")
        default_status = "done" if mode == "finish" else "in_progress"
        record.add_argument("--status", default=default_status)
        record.add_argument("--change", action="append", default=[])
        record.add_argument("--ref", action="append", default=[])
        record.add_argument("--dry-run", action="store_true")
        record.set_defaults(func=command_record, mode=mode)

    watch_once_parser = sub.add_parser("watch-once")
    watch_once_parser.add_argument("--dry-run", action="store_true")
    watch_once_parser.add_argument("--quiet", action="store_true")
    watch_once_parser.set_defaults(func=command_watch_once)

    watch = sub.add_parser("watch")
    watch.add_argument("--interval", type=int, default=180)
    watch.add_argument("--dry-run", action="store_true")
    watch.add_argument("--quiet", action="store_true")
    watch.set_defaults(func=command_watch)

    queue_status = sub.add_parser("queue-status")
    queue_status.set_defaults(func=command_queue_status)

    sync = sub.add_parser("sync")
    sync.add_argument("--dry-run", action="store_true")
    sync.set_defaults(func=command_sync)
    return parser


def main() -> int:
    ensure_runtime_dirs()
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
