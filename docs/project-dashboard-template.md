# Project Dashboard Template Pack

This document provides copy-ready starter text for project hubs under `dashboard > developer`.

Use it when a repo needs the standard `current`, `reports`, and `check log` surfaces but the Notion pages are not created yet.

## Rollout Status

- `economy-content-agent` -> live, page IDs configured
- `ai-glossary` -> template pending, page IDs missing
- `ai-web-project` -> template pending, page IDs missing
- `linkbot` -> template pending, page IDs missing

Until a project gets its Notion page IDs, `session_work_note.py` keeps the local work note and marks `notion_sync: not_configured`.

## Hub Page Template

```md
# <Project Name>

이 페이지는 프로젝트 허브다.

- live status: `current`
- dated snapshots: `reports`
- checks and follow-up: `check log`
- references: 필요할 때만 추가

현재 상태는 `current`에서 보고, 기록성 메모는 `reports`로 보낸다.
```

## `current` Template

```md
# current

## Goal
- <project goal>

## Purpose
- <why this project exists>

## Status
- <in_progress | blocked | monitoring | done>

## Progress %
- <0-100 or manual note>

## Todo Checklist
- [ ] <next task>
- [ ] <next task>

## Current Focus
- <active focus>

## Open Issues
- <open blocker or monitoring item>

## References
- <canonical doc or repo>

## Next Step
- <next concrete action>
```

## `reports` Template

```md
# reports

이 페이지는 날짜 기준 스냅샷만 둔다.

## Entry Format
- `YYYY-MM-DD HH:MM TZ` | 상태 | 한 줄 요약
- 세부 내용은 로컬 work note, incident, report 경로 링크로 연결
- active status가 바뀌면 `current`도 같이 갱신
```

## `check log` Template

```md
# check log

이 페이지는 health check, review, audit, follow-up만 둔다.

## Entry Format
- `YYYY-MM-DD` | check | result | owner | next step
- resolved 항목은 접거나 archive 처리
- 여전히 영향이 있는 failure와 warning만 유지
```
