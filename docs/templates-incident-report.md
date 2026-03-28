---
id: INC-YYYY-MM-DD-001
title: Short incident title
status: open
severity: medium
category:
  - operations_issue
system:
  - system-name
date_opened: YYYY-MM-DD
date_closed:
detected_via: manual_check
summary: One-paragraph summary of the issue and current state.
raw_evidence_paths:
  - /absolute/path/to/evidence.md
related_tasks:
  - /absolute/path/to/task.md
related_incidents: []
recurrence_risk: medium
notion_sync: pending
---

# Summary

State the issue in 3-5 sentences.

## Symptoms

- What failed
- What the operator observed
- What signals pointed to the issue

## Impact

- What was blocked or degraded
- What data, service, or workflow was affected

## Timeline

- `YYYY-MM-DD HH:MM TZ`: detection
- `YYYY-MM-DD HH:MM TZ`: key attempt or change
- `YYYY-MM-DD HH:MM TZ`: fix or current state

## Evidence

- `/absolute/path/to/raw/log`
- `/absolute/path/to/report`
- `/absolute/path/to/handoff`

## Root Cause

State the best current understanding.

## Resolution

State what changed and what now works.

## Recurrence Checklist

- [ ] Confirm the triggering command or schedule runs successfully again
- [ ] Confirm the latest report is healthy
- [ ] Confirm the expected target path or service state exists
- [ ] Confirm related automation is enabled only after validation

## Related Changes

- Documents updated
- Config changed
- Permission adjusted

## Follow-ups

- Remaining risks
- Optional next improvements
