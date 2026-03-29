# Project Dashboard Template Pack

This document provides copy-ready starter text for project hubs under `대시보드 (dashboard) > 개발 (developer)`.

Use it when a repo needs the standard `current`, `reports`, and `check log` surfaces but the Notion pages are not created yet.

## Rollout Status

- `ai-workspace` -> rollout pending
- `economy-content-agent` -> live, page IDs configured
- `ai-glossary` -> template pending, page IDs missing
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

> This page is the live dashboard.
> Status changes belong here first.
> Long logs stay in local Markdown and are linked, not pasted.

## 목표
- <project goal>

## 목적
- <why this project exists>

## 상태
- <in_progress | blocked | monitoring | done>

## 담당
- <owner>

## 다음 단계
- <next concrete action>

## 마지막 업데이트
- <YYYY-MM-DD HH:MM TZ>

## 진척도
- <0-100 or manual note>
- <[####------] 40%>

## 현재 초점
- <active focus>

## 진행 작업
- <active work item>
- <active work item>

## 체크리스트
- [ ] <next task>
- [ ] <next task>

## 열린 이슈
- <open blocker or monitoring item>

## 기준 링크
- <local source of truth or key report path>
```

Notes:

- In Notion, the page title already acts as `H1`; keep body headings at `H2`.
- Use the intro callout as the summary surface.
- Keep `current`, `reports`, and `check log` as fixed functional page names.
- In Notion, write body copy in Korean-first style.

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
