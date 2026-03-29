# Notion MCP Runtime Diagnosis — 2026-03-29

## Summary

The current machine does have a live Notion MCP connection.
The problem is not "Notion MCP is missing."
The problem is that the available Notion tool surface is only partially exposed in this runtime.

## Verified Locally

- `~/.codex/config.toml` is symlinked to `~/.dotfiles/codex/config.toml`
- `plugins."notion@openai-curated"` is enabled
- `[mcp_servers.notion]` points to `https://mcp.notion.com/mcp`
- `codex mcp list` shows `notion` as `enabled`
- `codex mcp get notion` shows a live remote MCP server with OAuth auth

## Verified In-Session

- `mcp__notion__notion_fetch` works
- `mcp__notion__notion_search` works
- live reads for `Ops Center`, `AI Session Reports`, and `노션 구조 정리` succeeded
- `mcp__codex_apps__notion_mcp_server_notion_query_data_sources` failed with `tool not found`

## Diagnosis

This is a runtime mismatch between:

- the Notion plugin/app documentation and examples
- the actual tool aliases exposed in the current Codex session

So the current state is:

- Notion MCP server: present
- Notion auth: present
- basic Notion tools: present
- advanced query tool alias used in this session: not reliably present

## Working Contract

Use these paths as the stable baseline:

1. `mcp__notion__notion_fetch`
2. `mcp__notion__notion_search`
3. `mcp__notion__notion_update_page`
4. local-first scripts that call the Notion REST API directly

Do not assume `notion-query-data-sources` is callable in every Codex runtime, even if plugin docs mention it.

## Chart View Implication

The chart-view blocker is not the MCP connection itself.
It is a UI-layer problem.

Notion chart views are still best treated as:

- local-first planning
- Notion API for content and database structure
- authenticated browser automation for chart probing
- live UI manual creation as the fallback

## Next Practical Path

Two scripts are now the intended starting point:

- [diagnose_notion_runtime.py](/Users/barq/developer/projects/ai-workspace/scripts/diagnose_notion_runtime.py)
- [notion_chart_probe.mjs](/Users/barq/developer/projects/ai-workspace/scripts/notion_chart_probe.mjs)

`diagnose_notion_runtime.py` confirms the machine/runtime state.

`notion_chart_probe.mjs` is the first step toward a trustworthy chart-view automation path:

- use an authenticated Chrome profile
- open the `AI Session Reports` database
- confirm whether Notion is actually logged in
- capture candidate buttons/selectors before attempting write automation

That keeps chart automation as a dry-run probe first, instead of blind UI mutation.

## First Probe Result

The first escalated headless probe completed successfully against the target database URL.

Result:

- browser launch path: works
- artifact/report path: works
- Notion login state in the dedicated profile: missing
- candidate chart/view buttons: none yet, because the page is still at the login gate

So the next blocking step is now explicit:

1. sign into Notion once in the dedicated profile directory
2. rerun `npm run probe:notion-chart:headless`
3. only after selectors are visible, add a write-capable chart creation flow
