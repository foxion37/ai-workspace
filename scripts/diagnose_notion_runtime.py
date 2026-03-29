#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path("/Users/barq")
CODEX_CONFIG = ROOT / ".codex/config.toml"
TARGETS_CONFIG = ROOT / "developer/projects/ai-workspace/config/notion_work_note_targets.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def contains_enabled_notion_plugin(config_text: str) -> bool:
    return '[plugins."notion@openai-curated"]' in config_text and "enabled = true" in config_text


def contains_notion_mcp_server(config_text: str) -> bool:
    return "[mcp_servers.notion]" in config_text and "https://mcp.notion.com/mcp" in config_text


def run_command(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main() -> int:
    config_text = read_text(CODEX_CONFIG)
    targets = json.loads(read_text(TARGETS_CONFIG))

    print("Notion runtime diagnosis")
    print(f"- codex config: {CODEX_CONFIG}")
    print(f"- notion plugin enabled in config: {'yes' if contains_enabled_notion_plugin(config_text) else 'no'}")
    print(f"- notion mcp server configured: {'yes' if contains_notion_mcp_server(config_text) else 'no'}")
    print(f"- ops page id: {targets['ops']['page_id']}")
    print(f"- ops center page id: {targets['ops_center']['page_id']}")
    print(f"- session reports database id: {targets['session_reports']['database_id']}")

    code, stdout, stderr = run_command(["codex", "mcp", "get", "notion"])
    print("- codex mcp get notion exit code:", code)
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    code, stdout, stderr = run_command(["codex", "mcp", "list"])
    print("- codex mcp list exit code:", code)
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    print("- diagnosis:")
    if contains_enabled_notion_plugin(config_text) and contains_notion_mcp_server(config_text):
        print("  notion plugin and notion MCP server are configured locally.")
        print("  if some Notion tools still fail in-session, treat it as a runtime tool-surface mismatch, not a missing config.")
    else:
        print("  local config is incomplete; fix config before debugging tool behavior.")

    print("- current working contract:")
    print("  use Notion fetch/search/update tools or direct Notion REST scripts for content and database operations.")
    print("  do not assume notion-query-data-sources is available in every Codex runtime.")
    print("  chart views remain a UI automation problem, not a Notion API problem.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
