# Notion Work Note Routing

This document defines where work notes should be written in Notion.

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

- the matching page under `dashboard > developer > <project>`

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
- Progress %
- Todo Checklist
- Current Focus
- Open Issues
- References
- Next Step

## Automation Rule

Automatic recording follows the same routing logic.

- ops event -> `ops log`
- project event -> project hub
- incident remains local-first and only mirrors a short summary into Notion

If Notion sync fails:

- keep the local work note
- keep the queue entry
- retry later

## Current default mapping

- ops / home ops / `.orchestra` / `home-dev-infra` / `ai-workspace` / `.dotfiles`
  - `dashboard > notion manual 1.0 > ops log`
- `economy-content-agent`
  - `dashboard > developer > 경제 콘텐츠 분석`
