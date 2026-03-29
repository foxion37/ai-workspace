# Notion Human Ops Standard

This document defines the human-first Notion structure for dashboard, ops pages, and AI session reports.

This file is the operating contract layer.
For naming, icons, links, tags, and emphasis rules, use `docs/notion-obsidian-style-guide.md`.

## Design Goal

The first screen should answer:

- what this space is for
- what is active now
- what is blocked
- where a beginner should click next

This standard is for people first.
Agents may read it, but the layout should not assume technical fluency.

Notion page body text should default to Korean-first.
Top-level area pages should use Korean-first bilingual names.
Only slot pages such as `current`, `reports`, and `check log` stay in English.

## Core Pattern

Use this order on human entry pages:

1. intro callout
2. current board
3. active work view
4. how this area works
5. references

Keep raw logs and long reasoning out of the first screen.
Link to detail pages instead.

The intro callout is the default summary surface.
Do not add a separate `Summary` heading unless the page needs a longer explanatory section.

## Page Types

### Hub

Use for `대시보드 (dashboard)`, `개발 (developer)`, `업무 (work)`, and other human entry pages.

Show:

- what lives here
- where to start
- operating rules
- important child pages

Default section order:

1. intro callout
2. what this area is for
3. start here
4. important child pages
5. operating rules
6. references

### Work Surface

Use for project hubs and live session pages.

Required sections:

- intro callout
- Goal
- Purpose
- Status
- Owner
- Next Step
- Last Updated
- Current Focus
- Active Work
- Checklist
- Open Issues
- Canonical Links
- For Human

Treat the title as the page-level `H1`.
In Notion body content, start at `H2`.

### Database Surface

Use for databases and pages that introduce a database.

Show:

- what the DB stores
- default views
- key properties
- input rules
- update cadence

Recommended order:

1. intro callout
2. what the DB stores
3. key properties
4. default views
5. update cadence
6. references

### Report Surface

Use for `reports`.

Show:

- what belongs here
- timestamp format
- link back to `current` when status changes

Recommended order:

1. intro callout
2. entry format
3. current linkage rule
4. source-of-truth note

### Check Surface

Use for `check log`.

Show:

- what is being checked
- what counts as open
- who should act next

Recommended order:

1. intro callout
2. open item rule
3. owner or next action rule
4. archive rule

## Dashboard Layout

The root dashboard should be split into three visible zones:

- `Start Here`
- `Now`
- `How It Works`

Do not put every database first.
Put filtered current views first.

## Ops Center

Promote current Notion operating manual and operating log into one visible category named `Ops Center`.

Suggested contents:

- manual
- ops log
- session reports
- check log
- references

Do not break old routes immediately.
Expose the new category first, then migrate links.

Treat the following as stable live names in Notion:

- `대시보드 (dashboard)`
- `개발 (developer)`
- `Ops Center`
- `current`
- `reports`
- `check log`
- `ops log`
- `references`

## AI Session Reports

Create one database under `developer` as the human-friendly index of current work.

Suggested properties:

- `Title`
- `Status`
- `Progress %`
- `Agent`
- `Area`
- `Project / Session`
- `Started At`
- `Last Updated`
- `Next Step`
- `Human Summary`
- `Local Source`

Suggested views:

- active now
- blocked
- by agent
- by project
- recently done

Each row page should use the Work Surface template.

## Projects And Documents

Under `개발 (developer)`, separate object types explicitly.

- Projects belong to a `프로젝트 (Projects)` table DB.
- Documents belong to a `문서 (Documents)` table DB or an equivalent document-only surface.
- Shared databases such as `AI Session Reports` should stay in their own database section and must not be mixed into project lists.

Project rules:

- every active developer project should have one row in `프로젝트 (Projects)`
- every project row should link to its hub page and `current / reports / check log`
- project hubs are human entry pages, but the DB row is the canonical index

Document rules:

- reference pages, manuals, intake pages, and dated writeups are documents, not projects
- document hubs should not be presented as project hubs
- names should make the document role explicit, such as `공용 문서 (shared documents)`

## Naming Rules

- use the real live page names from the workspace
- prefer breadcrumb notation like `대시보드 (dashboard) > 개발 (developer) > ...` in docs
- keep project display titles stable once chosen
- keep `current`, `reports`, and `check log` as fixed functional page names
- use the live page name `family` for the current structure

Page title style itself is owned by `docs/notion-obsidian-style-guide.md`.
This file only locks which live route names are operationally fixed.

## Status Signal Rule

Use gray icons by default.
Only use color when the page must signal active status.

- `red`: needs review now
- `orange`: currently being edited
- `yellow`: paused or waiting
- `green`: checked or stable
- `blue`: guide or reference
- `light gray`: archive or legacy

The exact color policy and emoji limits live in `docs/notion-obsidian-style-guide.md`.
Automation should prefer native Notion icons with color when the API path supports them.

## Visualization Rule

Use Notion-native visualisation first.

- use `Progress %` and `Status` properties so chart views can be added inside Notion
- use a short text progress bar in the page body for immediate readability
- add a small structure map on hub or manual pages when the page explains information architecture
- avoid external plugins unless Notion-native chart views are insufficient

### Chart View Rule

Treat chart views as a UI-managed summary layer on top of `AI Session Reports`.

Required chart views:

- `상태 분포 (차트)`: donut chart grouped by `Status`
- `진척도 비교 (차트)`: bar chart using `Project / Session` and `Progress %`

Placement rule:

- keep the canonical chart views inside `AI Session Reports`
- mirror them into `Ops Center` or `current` only as linked views if they improve first-screen readability
- do not replace `current` text status with charts alone

Operating rule:

- chart views are user-managed in the live Notion UI
- agents should not treat chart creation or chart layout control as a required automation target
- agents are responsible for keeping the chart input data truthful: `Status`, `Progress %`, `Project / Session`, `Agent`, and `Last Updated`
- if chart automation is not trustworthy, stop at DB health and text progress bars instead of trying to force UI control
- chart view names should stay stable once chosen so humans and agents refer to the same surface

## Freshness Rule

Treat freshness as a content check, not just a sync check.

- update the local work note first, then refresh the matching human-facing Notion surface
- for `ops` routing, refresh `ops log` first and then any shared status surface such as `Ops Center` or `AI Session Reports`
- for project routing, refresh `current` first, then `reports` or `check log` if the session changed user-visible state
- `queue empty` does not mean the surface is fresh; compare the latest local note against `current`, `reports`, `check log`, and session-report rows
- duplicate session rows, stale progress values, or missing required DB properties count as structure drift and should activate `Maintenance` plus `Development`
- missing chart views must not block a truthful `current` page, report entry, or check-log item

## Notion Notes

Current Notion auth may be unavailable during rollout.
Local reports remain canonical until live sync is restored.

Role split and cadence for specialist Notion sessions live in `docs/notion-subagent-team.md`.
