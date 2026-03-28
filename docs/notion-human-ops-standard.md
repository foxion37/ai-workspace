# Notion Human Ops Standard

This document defines the human-first Notion structure for dashboard, ops pages, and AI session reports.

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

## Page Types

### Hub

Use for `dashboard`, `developer`, `work`, and other human entry pages.

Show:

- what lives here
- where to start
- operating rules
- important child pages

### Work Surface

Use for project hubs and live session pages.

Required sections:

- Goal
- Purpose
- Current Board
- Current Focus
- Active Work
- Checklist
- Open Issues
- For Human
- Next Step

### Database Surface

Use for databases and pages that introduce a database.

Show:

- what the DB stores
- default views
- key properties
- input rules
- update cadence

### Report Surface

Use for `reports`.

Show:

- what belongs here
- timestamp format
- link back to `current` when status changes

### Check Surface

Use for `check log`.

Show:

- what is being checked
- what counts as open
- who should act next

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

## Notion Notes

Current Notion auth may be unavailable during rollout.
Local reports remain canonical until live sync is restored.
