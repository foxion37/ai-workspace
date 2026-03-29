# Project Dashboard Standard

This document defines the default structure for project hubs in Notion.

Copy-ready starter text lives in `docs/project-dashboard-template.md`.

## Goal

The first project surface should answer:

- what the project is for
- what state it is in
- what is blocked
- what to do next

It should not become a dump of raw logs.

## Standard Contract

The standard project surface is:

- hub page for orientation
- `현재 상태 (current)` as the source of truth
- `진행 기록 (reports)` for dated snapshots
- `점검 기록 (check log)` for checks and follow-up

This standard is fixed before live Notion rollout work.

## Hub Structure

Recommended structure:

- project hub page
- `현재 상태 (current)`
- `진행 기록 (reports)`
- `점검 기록 (check log)`
- `기준 자료 (references)` when needed

### Project hub page

Use this as the human entry point.

It should explain:

- what the project is
- where live status is tracked
- where dated reports go
- where check items go

### `현재 상태 (current)`

This is the live dashboard page.

Required sections:

- intro callout
- Goal
- Purpose
- Status
- Owner
- Next Step
- Last Updated
- Progress %
- Todo Checklist
- Current Focus
- Open Issues
- References
- Canonical Links

Rules:

- in Notion, treat the page title as `H1` and start body headings at `H2`
- keep the intro callout as the summary surface
- keep only the latest valid state
- overwrite stale status instead of stacking snapshots
- show only open blockers and active watch items
- use links for detail, not pasted raw logs
- do not move shared ops policy or multi-repo automation notes into this page

### `진행 기록 (reports)`

Use this for dated work notes and snapshots.

Rules:

- store time-stamped notes only
- do not use it as the current dashboard
- link back to `현재 상태 (current)` when the snapshot changes active status
- treat local work-note Markdown as the canonical long-form source when more detail is needed

### `점검 기록 (check log)`

Use this for checks, audits, review items, and follow-ups.

Rules:

- keep entries short
- track only items that still need attention or should stay visible for monitoring
- archive or collapse resolved items when they stop mattering
- use this page for review/audit/check items, not progress journaling

## Progress Rule

Default progress is checklist-based.

- calculate from the current todo checklist when possible
- allow manual override when checklist percent is misleading
- show the final displayed value on the dashboard

## Open Issues Rule

Only show issues that are currently open.

Include:

- blocked tasks
- open or monitoring incidents
- recent failed checks or reports that still need follow-up

Do not include:

- raw logs
- closed incidents
- historical failures that no longer affect decisions

## Writing Rule

Keep dashboard text short.

- summary first
- details by link
- latest valid state only

Use the full operating metadata contract where needed, but keep the visible top block compact for humans.
See `docs/notion-obsidian-style-guide.md` for the style-layer rules.

## Routing Boundary

Project hubs are for project-scoped state only.

- send shared ops, `.orchestra`, NAS, launchd, or cross-repo automation updates to `운영 로그 (ops log)`
- send project focus, blockers, reports, and checks to the matching project hub
- when the route is ambiguous, prefer `ops` for shared infrastructure and `project` for product/workstream state

## Local-First Rollout Rule

Until auth and page IDs are ready everywhere:

- keep the same dashboard structure locally first
- allow project notes to remain `notion_sync: not_configured`
- do not treat missing page IDs as a sync error
- run live sync only in a dedicated follow-up session

## Rollout Note

Known developer project rollout targets now include:

- `ai-workspace`
- `economy-content-agent` as the live reference implementation
- `ai-glossary`
- `linkbot`

Projects without Notion page IDs should still follow the same local-first structure, but their work notes remain `notion_sync: not_configured` until the hub pages exist.
