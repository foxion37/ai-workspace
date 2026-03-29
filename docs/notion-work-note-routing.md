# Notion Work Note Routing

This document defines where work notes should be written in Notion.

## Operating Contract

The current operating contract is:

- work-note routing is `ops` or `project`
- `ops` is for shared operating changes and cross-repo infrastructure
- `project` is for one project hub only
- local Markdown stays canonical
- Notion stays secondary until auth and page IDs are ready
- this session locks the rules only; live sync happens in a later session

## Core Rule

Do not treat Notion as a session log sink.

Write only when a situation matters later for people or agents.

Examples:

- blocker appeared
- blocker cleared
- root cause confirmed
- project status changed
- operating path changed
- recurring failure needs a short preventive note

Raw logs stay in their original paths.
Long explanations stay in local incident or work-note Markdown.

## Routing Rule

Route by ownership first, not by where the work happened.

- if the change affects shared policy, automation, `.orchestra`, home ops, or more than one repo, route to `ops`
- if the change stays inside one project's active status surface, route to that project's hub
- if a repo lives under `developer/projects` but is still missing a wired hub, keep the route as project-scoped and leave sync unconfigured

### `ops log`

Target:

- `dashboard > notion manual 1.0 > ops log`

Use when:

- the change affects home ops, `.orchestra`, NAS, launchd, shared automation, or more than one repo
- the note is about operating policy, shared workflows, or common infrastructure

Examples:

- NAS backup path changed
- incident mirror policy changed
- shared session watcher changed

### Project hub

Target:

- the matching page under `대시보드 (dashboard) > 개발 (developer) > <project>`

Use when:

- the change is contained inside one project
- the note is about current focus, progress, blockers, checks, or reports for that project

Examples:

- project-specific blocker
- project goal change
- project progress update
- project check result

## Project Dashboard Standard

Each project hub should keep a dashboard-style first surface.

Recommended flow:

1. project hub page with overview
2. `current` page as the live dashboard
3. `reports` page for dated snapshots
4. `check log` page for health checks and follow-ups
5. `references` when needed

Required dashboard fields:

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

Operational meaning:

- `current` is the live status surface
- `reports` holds dated snapshots only
- `check log` holds checks, reviews, warnings, and follow-up items
- raw logs stay local and are linked, not pasted
- use an intro callout as the summary surface on Notion pages
- in Notion body content, start at `H2` because the title already acts as `H1`

## Automation Rule

Automatic recording follows the same routing logic.

- ops event -> `ops log`
- project event -> project hub
- incident remains local-first and only mirrors a short summary into Notion

Direct API sync is opt-in for now.

- keep local Markdown as canonical
- queue only when the route has a real parent page ID
- if the project hub is not wired yet, keep `notion_sync: not_configured`
- use manual `session_work_note.py sync` after `NOTION_API_KEY` and page IDs are ready

## Queue And Sync Contract

`session_work_note.py` currently uses these states:

- `pending`: the local work note exists and a Notion payload is queued
- `not_configured`: the local work note exists but the route has no usable parent page ID yet
- `synced`: a queued payload was pushed successfully

Rules:

- `queue-status` is the inspection command before a real sync session
- `sync` is manual and should run only after `NOTION_API_KEY` and required page IDs are ready
- failed sync attempts must leave the local work note intact and keep the queue entry for retry
- `not_configured` items are not queue failures; they are rollout-incomplete routes
- do not bulk backfill Notion until the route and dashboard standard are already fixed locally

## Local-First Principle

Use `local-first / Notion-second` as the default rule.

- write the full state to local Markdown first
- use Notion for a short dashboard-safe mirror only
- keep incidents, long logs, and raw reports in local files
- treat Notion as a readable coordination layer, not the system of record

If Notion sync fails:

- keep the local work note
- keep the queue entry
- retry later

## Current default mapping

- ops / home ops / `.orchestra` / `home-dev-infra` / `.dotfiles`
  - `대시보드 (dashboard) > 노션 운영 매뉴얼 (notion manual) 1.0 > ops log`
- `ai-workspace`
  - `대시보드 (dashboard) > 개발 (developer) > AI Workspace`
- `economy-content-agent`
  - `대시보드 (dashboard) > 개발 (developer) > 경제 콘텐츠 분석`
- `ai-glossary`
  - `대시보드 (dashboard) > 개발 (developer) > AI Glossary`
- `linkbot`
  - `대시보드 (dashboard) > 개발 (developer) > Linkbot`

Archived projects such as `ai-web-project` are excluded from active project routing.
Keep their Notion pages as read-only historical references, but do not queue new project work notes for them.
