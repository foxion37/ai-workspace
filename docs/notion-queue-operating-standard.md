# Notion Queue Operating Standard

이 문서는 현재 유효한 Notion 운영 정본이다.

기준은 다음과 같다.

- Notion은 모든 구조화된 데이터의 source of truth다
- 로컬 데이터는 읽기 전용 캐시와 로그 용도다
- 로컬 데이터를 기준으로 Notion을 덮어쓰지 않는다
- Notion 데이터를 실행 코드나 시스템 소스로 사용하지 않는다
- 양방향 동기화는 금지한다
- 전체 데이터베이스를 재작성하지 않는다

## Queue Workflow

작업은 queue 기반으로만 처리한다.

1. Notion QUEUE에서 `pending` 상태의 작업을 조회한다
2. Notion MASTER DB에서 중복 여부를 확인한다
3. 데이터를 분석하고 처리한다
4. 결과를 Notion에 업데이트한다
5. QUEUE 상태를 `done`으로 변경한다
6. 로컬에는 상세 로그를 남기고 Notion에는 요약 로그만 남긴다

## Logging

- 상세 로그는 로컬에 저장한다
- Notion에는 요약 로그만 기록한다
- 로컬 로그는 추적과 재현을 위한 보조 기록이다

## Conflict Policy

- 충돌이 있으면 Notion 데이터를 우선한다
- 불확실하면 작업을 중단하고 보고한다
- 데이터 무결성을 우선한다
- 자동화보다 안정성을 우선한다

## Forbidden Actions

- 로컬 기준으로 Notion을 수정하는 행위
- Notion 데이터 임의 삭제
- DB 스키마 변경
- 전체 overwrite
- queue를 무시한 작업 수행
- 양방향 sync

## Operational Scope

이 문서가 우선한다.
다른 Notion 운영 문서와 충돌하면 이 문서를 따른다.

