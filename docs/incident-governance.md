# Incident Governance

This document defines how incidents should be recorded across the workspace.

## Purpose

Use incident reports when an issue needs to be understood later by both people and agents.

Examples:

- backup failures
- permission errors
- authentication problems
- automation regressions
- structure conflicts between tools or folders

Do not use raw logs as the primary human-facing record.

## Three Layers

### 1. Raw logs

Raw logs remain in the systems that produce them.

Examples in this environment:

- `/Users/barq/.orchestra/logs/activity.log`
- `/Users/barq/.orchestra/tasks/`
- `/Users/barq/.orchestra/handoffs/`
- `/Users/barq/developer/home-dev-infra/reports/`

Rules:

- keep the existing path as the source of truth
- do not force a central move
- optimize for evidence preservation, not readability

### 2. Incident reports

Incident reports are the canonical human and agent summary for one issue.

Canonical path:

- `~/AI-Workspace/knowledge-db/incidents/`

Helper script:

- `/Users/barq/developer/projects/ai-workspace/scripts/render_incident_index.py`

Rules:

- one incident per Markdown file
- local Markdown first
- point to raw evidence paths instead of copying long logs
- include status, severity, categories, systems, and follow-up state

### 3. Notion DB

Notion is the dashboard and query layer.

Rules:

- sync key fields from the incident report
- do not treat Notion as the raw evidence store
- do not make Notion the only source of truth

## Role Split

| Layer | Primary role | Format | Source of truth |
| --- | --- | --- | --- |
| Raw logs | machine evidence | log, task, handoff, report files | yes |
| Incident report | human and agent summary | Markdown | yes |
| Notion DB | dashboard, filters, rollups | database rows | no |

## Canonical Flow

1. A failure or operational anomaly is detected in raw logs.
2. If the issue matters beyond the immediate session, create an incident report.
3. The incident report links the evidence, summarizes impact and cause, and tracks resolution.
4. Notion mirrors the incident metadata for dashboarding.
5. If the issue is project-specific, pair the incident with a short project work note or dashboard update instead of copying the full incident body into Notion.

## Minimal Metadata

Required frontmatter fields:

- `id`
- `title`
- `status`
- `severity`
- `category`
- `system`
- `date_opened`
- `summary`
- `raw_evidence_paths`

Recommended fields:

- `date_closed`
- `detected_via`
- `related_tasks`
- `related_incidents`
- `recurrence_risk`
- `notion_sync`

## Status Values

- `open`
- `investigating`
- `blocked`
- `monitoring`
- `resolved`
- `closed`

Use `monitoring` after a fix has landed but before enough successful runs have passed.

## Severity Values

- `low`
- `medium`
- `high`
- `critical`

## Category System

Use 1-3 categories per incident.

Primary categories:

- `operations_issue`
- `backup_failure`
- `permission_issue`
- `authentication_issue`
- `configuration_drift`
- `structure_conflict`
- `sync_issue`
- `review_pipeline_issue`
- `automation_failure`
- `data_integrity_risk`

System labels:

- `nas`
- `smb`
- `backup`
- `launchd`
- `notion`
- `n8n`
- `.orchestra`
- `ai-workspace`
- `home-dev-infra`

## Authoring Rules

- Keep the summary short enough to understand in one minute.
- Prefer absolute paths for evidence.
- Add a recurrence checklist when the issue can happen again.
- Link to the task path if there is an active remediation task.
- Update the existing incident when the same event chain continues.
- Open a new incident when the failure mode is materially different.

## Session Routine

When an incident is created or updated in a session:

1. update the incident Markdown
2. rerender `~/AI-Workspace/knowledge-db/incidents/INDEX.md`
3. reflect the incident state in the relevant `.orchestra` task or session summary when it changes task status or next actions

When the incident is important enough to keep visible in Notion:

4. add or update a short work-note style summary in the correct target
   - ops incident -> `dashboard > notion manual 1.0 > ops log`
   - project incident -> matching project hub dashboard/check log

Use this command:

```bash
python3 /Users/barq/developer/projects/ai-workspace/scripts/render_incident_index.py \
  /Users/barq/AI-Workspace/knowledge-db/incidents
```

## Retrieval Rules

### Human flow

1. Find the issue in Notion or `INDEX.md`.
2. Read the incident report.
3. Follow evidence paths only when detail is needed.

### Agent flow

1. Search incident Markdown by category, system, or status.
2. Use the incident as the primary context artifact.
3. Verify details through `raw_evidence_paths`.

## Migration Rule

Keep existing paths in place.

Adopt this order:

1. add incident reports
2. add `INDEX.md`
3. optionally sync metadata into Notion
4. automate index and sync later

Do not start with a raw log migration.

Example index render: see the Session Routine command above.
