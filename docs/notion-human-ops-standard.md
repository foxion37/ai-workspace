# Notion Human Ops Standard

이 문서는 사람 중심의 노션 운영 구조를 정의한다.

대상 범위는 `대시보드 (dashboard)`, 운영 페이지, 프로젝트 허브, `AI 세션 리포트 (AI Session Reports)`다.

이 문서는 운영 계약 계층이다.
제목 스타일, 아이콘, 링크, 태그, 강조 규칙은 `docs/notion-obsidian-style-guide.md`를 따른다.

## Design Goal

첫 화면은 아래 질문에 바로 답해야 한다.

- 이 공간은 무엇을 하는 곳인가
- 지금 무엇이 진행 중인가
- 무엇이 막혀 있는가
- 초보자는 어디를 먼저 눌러야 하는가

이 기준은 사람 우선이다.
에이전트도 읽을 수 있지만, 기술적 맥락을 많이 아는 사람만 이해할 수 있게 만들면 안 된다.

노션 페이지 본문과 소제목은 한글 중심으로 쓴다.
상위 허브뿐 아니라 하위 기능 페이지도 한글 우선-영문 병기 제목을 쓴다.

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

Use for `진행 기록 (reports)`.

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

Use for `점검 기록 (check log)`.

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

현재 노션 운영 매뉴얼과 운영 로그를 `운영 센터 (Ops Center)`라는 사람 중심 입구로 묶는다.

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
- `운영 센터 (Ops Center)`
- `현재 상태 (current)`
- `진행 기록 (reports)`
- `점검 기록 (check log)`
- `운영 로그 (ops log)`
- `기준 자료 (references)`

## AI Session Reports

`개발 (developer)` 아래에는 현재 작업의 사람 중심 인덱스로 `AI 세션 리포트 (AI Session Reports)` DB를 둔다.

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

`개발 (developer)` 아래에서는 객체 종류를 분명하게 나눈다.

- Projects belong to a `프로젝트 (Projects)` table DB.
- Documents belong to a `문서 (Documents)` table DB or an equivalent document-only surface.
- `AI 세션 리포트 (AI Session Reports)` 같은 공용 DB는 별도 섹션에 두고 프로젝트 목록과 섞지 않는다.

Project rules:

- every active developer project should have one row in `프로젝트 (Projects)`
- every project row should link to its hub page and `current / reports / check log`
- project hubs are human entry pages, but the DB row is the canonical index

Document rules:

- reference pages, manuals, intake pages, and dated writeups are documents, not projects
- document hubs should not be presented as project hubs
- names should make the document role explicit, such as `공용 문서 (shared documents)`

## Naming Rules

- 워크스페이스의 실제 live 페이지 이름을 문서 기준으로 쓴다.
- 문서 안의 경로 표기는 `대시보드 (dashboard) > 개발 (developer) > ...` 같은 breadcrumb 표기를 우선한다.
- 프로젝트 표시 이름은 한 번 정하면 쉽게 바꾸지 않는다.
- 기능 페이지 이름도 영어 단독으로 두지 않고 한글 우선-영문 병기로 고정한다.
- 현재 구조의 민감 개인 섹션 이름은 live 이름인 `family`를 유지한다.

기능 페이지 기본 이름은 아래를 기준으로 고정한다.

- `운영 센터 (Ops Center)`
- `현재 상태 (current)`
- `진행 기록 (reports)`
- `점검 기록 (check log)`
- `운영 로그 (ops log)`
- `기준 자료 (references)`

페이지 제목 스타일의 세부 규칙은 `docs/notion-obsidian-style-guide.md`가 맡고, 이 문서는 live route 이름과 운영 계약만 잠근다.

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

시각화는 노션 기본 기능을 먼저 쓴다.

- `Progress %`와 `Status` 속성을 유지해 chart view를 노션 안에서 바로 붙일 수 있게 한다.
- 페이지 본문에는 짧은 텍스트 진행 바를 남겨 첫 화면에서 상태를 읽게 한다.
- 허브나 매뉴얼 페이지가 정보 구조를 설명할 때는 작은 구조도를 함께 둔다.
- 노션 기본 chart view가 부족하지 않은 한 외부 플러그인에 의존하지 않는다.

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
