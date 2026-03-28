# Project Dashboard Standard

This document defines the default structure for project hubs in Notion.

## Goal

The first project surface should answer:

- what the project is for
- what state it is in
- what is blocked
- what to do next

It should not become a dump of raw logs.

## Hub Structure

Recommended structure:

- project hub page
- `current`
- `reports`
- `check log`
- `references` when needed

### Project hub page

Use this as the human entry point.

It should explain:

- what the project is
- where live status is tracked
- where dated reports go
- where check items go

### `current`

This is the live dashboard page.

Required sections:

- Goal
- Purpose
- Status
- Progress %
- Todo Checklist
- Current Focus
- Open Issues
- References
- Next Step

Rules:

- keep only the latest valid state
- overwrite stale status instead of stacking snapshots
- show only open blockers and active watch items
- use links for detail, not pasted raw logs

### `reports`

Use this for dated work notes and snapshots.

Rules:

- store time-stamped notes only
- do not use it as the current dashboard
- link back to `current` when the snapshot changes active status

### `check log`

Use this for checks, audits, review items, and follow-ups.

Rules:

- keep entries short
- track only items that still need attention or should stay visible for monitoring
- archive or collapse resolved items when they stop mattering

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
