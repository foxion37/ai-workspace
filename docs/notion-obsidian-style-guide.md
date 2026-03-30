# Notion Obsidian Style Guide

이 문서는 노션과 옵시디언의 표시 규칙을 보조적으로 정리한다.
정본은 `docs/notion-queue-operating-standard.md`이다.

이 파일은 명명, 아이콘, 헤딩, 링크, 태그, 강조 규칙만 맡는다.

## 역할 분리 (Role Split)

- `notion-queue-operating-standard.md`는 Notion queue, source of truth, logging contract를 맡는다
- 이 가이드는 표시와 작성 규칙을 맡는다
- 두 문서가 겹치면 정본 문서가 우선한다

## 명명 규칙 (Naming Rules)

### 노션 (Notion)

페이지 제목은 한국어 우선에 영어를 괄호로 붙여 검색과 에이전트 읽기성을 확보한다.
본문도 기본은 한국어 우선이다.
고정 기능 페이지 이름도 같은 한국어 우선 병기 규칙을 따른다.

Recommended format:

- `<Korean Name> (<english label>)`

Examples:

- `운영 매뉴얼 (ops manual)`
- `대시보드 보수 체크리스트 (maintenance checklist)`

Top-level functional and area pages should use Korean-first bilingual titles:

- `대시보드 (dashboard)`
- `개발 (developer)`
- `운영 센터 (ops center)`

Functional page names also use Korean-first bilingual titles:

- `현재 상태 (current)`
- `진행 기록 (reports)`
- `점검 기록 (check log)`
- `운영 로그 (ops log)`
- `기준 자료 (references)`

### 옵시디언 (Obsidian)

노트 이름은 영어 우선을 기본으로 쓴다.
기본값으로 한국어-영어 병기 제목은 쓰지 않는다.

Recommended format:

- `notion-obsidian-style-guide`
- `project-dashboard-template`
- `session-report-2026-03-29`

사람이 보기 좋은 한국어 라벨이 나중에 필요하면 파일명이 아니라 본문이나 frontmatter에 둔다.
옵시디언 본문은 필요할 때 병기할 수 있지만 파일명은 영어 우선으로 유지한다.

### 버전과 날짜 라벨 (Version And Date Labels)

- stable policy or standard docs: `1.0`, `2.0`
- working revisions: `v2`, `v3`
- dated proposals, reports, or logs: `YYYY-MM-DD`

Do not mix version and date in one display title unless the document is explicitly a dated release record.

## 아이콘 규칙 (Icon Rules)

기본 규칙:

- 허브, 정책, 중립 페이지는 회색 아이콘을 쓴다
- 페이지가 활동 상태를 드러내야 할 때만 색을 쓴다
- 이모지보다 노션 아이콘을 먼저 쓴다

### 색상 예외 (Color Exceptions)

Use color as a controlled status signal.

- `red`: needs review now, blocking issue, high-risk approval wait
- `orange`: actively being edited, restructured, or repaired
- `yellow`: paused, waiting, temporarily held
- `green`: checked, stable, operating normally
- `blue`: guide, manual, reference, index
- `gray`: neutral default
- `light gray`: archive, legacy, read-only history

규칙:

- 같은 상태는 같은 색을 쓴다
- 상태 신호가 더는 필요 없으면 회색으로 돌아간다
- 장식 목적만으로 색을 쓰지 않는다

자동화 규칙:

- Notion API 쓰기에는 색이 명시된 노션 기본 아이콘을 우선한다
- 아이콘 자체가 색상 신호보다 더 많은 의미를 가져야 할 때만 이모지를 쓴다
- 기본 자동화 모양은 유지하고 색만 바꿔도 된다

## 헤딩 규칙 (Heading Rules)

### 노션 (Notion)

노션에서는 페이지 제목이 이미 `H1` 역할을 한다.
본문 `H1`은 추가하지 않는다.
본문 구조는 `H2`부터 시작한다.

이 순서를 따른다:

1. intro callout
2. `H2` sections
3. `H3` and `H4` only when needed

소개 말풍선 블록은 요약 표면이다.
정말 필요한 경우가 아니면 별도의 `Summary` 헤딩을 추가하지 않는다.

### 옵시디언 (Obsidian)

옵시디언에서는 파일명과 `H1`이 분리되어 있다.
본문 `H1` 하나를 두고, 그다음 `H2`부터 `H4`까지 쓴다.

규칙:

- `H1`은 정확히 하나만 쓴다
- `H5` 이상은 쓰지 않는다
- 노트가 의도적으로 평면 구조가 아닌 이상 헤딩 레벨을 건너뛰지 않는다

## 링크 규칙 (Link Rules)

### 옵시디언 (Obsidian)

- internal note links: `[[wikilink]]`
- custom display: `[[target note|display name]]`
- external links: standard Markdown links

### 노션 (Notion)

- internal page links: `@mention` or native internal link blocks
- external links: standard URL links

### 정본 원칙 (Canonical Source Rule)

When a local Markdown file is the source of truth for a local-only reference:

- state that the local file is canonical
- link from Notion to the local source when possible
- keep detailed logs in local Markdown only when the file is explicitly local-only
- do not use this rule to override the Notion queue operating standard

## 메타데이터와 상단 블록 (Metadata And Top Block)

The operating contract metadata remains canonical:

- `구역 (Zone)`
- `책임자 (Lead)`
- `담당자 (Owner)`
- `대상자 (Audience)`
- `에이전트 행동 (Agent Action)`
- `승인 (Approval)`
- `정본 (Source of Truth)`
- `검토 주기 (Review Cadence)`

For human-first top sections, compress this into a visible working block:

- `목적 (Purpose)`
- `상태 (Status)`
- `담당자 (Owner)`
- `다음 단계 (Next Step)`
- `마지막 업데이트 (Last Updated)`
- `정본 링크 (Canonical Links)`

This block is a reading aid, not a replacement for the full contract metadata.

## 태그 규칙 (Tag Rules)

태그는 최소한으로 통제해서 쓴다.
태그는 검색 보조 수단이지 주 분류 체계가 아니다.

Recommended tag families:

- format: `#guide`, `#report`, `#template`, `#check`
- state: `#active`, `#blocked`, `#waiting`, `#archive`
- area: `#ops`, `#project`, `#reference`

규칙:

- 대부분의 노트는 한 개에서 세 개 태그만 유지한다
- 모든 노션 속성을 태그로 옮기지 않는다
- 태그를 구역 (Zone)이나 승인 수준 (approval level)과 동일시하지 않는다

## 강조와 이모지 (Emphasis And Emoji)

일반 문서에서는 강조 방식을 세 가지로만 쓴다:

- `**bold**`는 결정과 중요한 라벨에 쓴다
- `*italic*`은 가벼운 뉘앙스에만 쓴다
- ``code``는 페이지 이름, 필드, 경로, 명령, 상태 값에 쓴다

이모지 규칙:

- 페이지 제목 앞에 이모지를 붙이지 않는다
- 기능적 목적이 분명할 때만 이모지를 허용한다
- 이모지를 아이콘 상태 시스템의 대체물로 쓰지 않는다
