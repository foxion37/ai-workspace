# Notion Session Handoff — 2026-03-29

This handoff is for the next agent continuing Notion operations and structure work.

## Context

- The specialist Notion team model is now defined in `docs/notion-subagent-team.md`.
- Daily full-team operation was rejected as inefficient.
- Default lead is `Operations`.
- `Maintenance`, `Development`, and `Growth` should be activated only when the signal justifies it.

## Operating Decision

Use this cadence by default:

- `Operations`: daily when state changed
- `Maintenance`: 2-3 times per week or after visible drift
- `Development`: event-driven when templates, sync, page IDs, or project surfaces changed
- `Growth`: weekly review, not daily

## What The Next Agent Should Do

1. Read `docs/notion-subagent-team.md`.
2. Treat local docs as canonical and Notion as the human-facing mirror.
3. Start the next Notion session with `Operations` routing:
   - decide `ops` vs `project`
   - confirm whether there is queue backlog or local/Notion mismatch
4. Activate additional roles only if needed:
   - `Maintenance` for stale pages, duplicate pages, broken links, queue aging
   - `Development` for `current / reports / check log` or template changes
   - `Growth` for repeated navigation or adoption problems
5. Do not turn Notion into a raw session log dump.

## Known Drift To Check First

- `queue empty` may still hide stale human-facing pages.
- `dashboard > developer > 노션 구조 정리 > current` was last seen with `35%` progress and an older next-step line.
- `dashboard > developer > 노션 구조 정리` hub was last seen with the same stale `35%` progress bar.
- `AI Session Reports` may contain duplicate bootstrap rows for the same local source.
- `AI Session Reports` should be checked for duplicate rows, missing `Project / Session`, and stale `Progress %` before any chart-dependent reading.

## Session Update

- Route stayed `ops`.
- Activated roles: `Operations`, `Maintenance`, `Development`.
- `운영 센터 (ops center)`, `노션 구조 정리`, `current`, `reports`, `check log` were refreshed to reflect the latest human-facing state.
- `AI Session Reports` now includes `Project / Session`, the duplicate `2026-03-28` rows were reduced to one historical row, and a new `2026-03-29` row was added.
- Browser automation did not become a trustworthy chart-control path. The dedicated probe still hit the sign-in gate or unstable session state.
- Chart views are now treated as explicitly user-managed. Keep the standard names `상태 분포 (차트)` and `진척도 비교 (차트)` when the user creates or adjusts them inside `AI Session Reports`.
- The next agent should focus on DB health and human-facing freshness, not on chart automation.

## Prompt For The Next Agent

```text
Continue the Notion operating model from /Users/barq/developer/projects/ai-workspace/docs/notion-subagent-team.md.

Use Operations as the lead role.
First decide whether today's work routes to ops or to a project hub.
Check for local/Notion mismatch, queue backlog, and any stale current/report/check-log surfaces.
Only activate Maintenance, Development, or Growth if the signal requires it.

Keep local docs canonical. Notion should mirror human-readable status, not raw logs.
Treat chart views as user-managed UI surfaces. Do not spend the session trying to automate chart creation unless the user explicitly reopens that workstream.
Keep `AI Session Reports` healthy enough that the user-controlled charts stay readable.
Before making structural changes, record the rule locally.
At the end, leave a short update in local notes and identify any remaining backlog for the next session.
```
