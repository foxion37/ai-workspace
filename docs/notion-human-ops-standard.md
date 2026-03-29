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

Use for `dashboard`, `developer`, `work`, and other human entry pages.

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

Treat the following as fixed functional page names in Notion:

- `dashboard`
- `developer`
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

## Naming Rules

- use the real live page names from the workspace
- prefer breadcrumb notation like `dashboard > developer > ...` in docs
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

## Notion Notes

Current Notion auth may be unavailable during rollout.
Local reports remain canonical until live sync is restored.

Role split and cadence for specialist Notion sessions live in `docs/notion-subagent-team.md`.
