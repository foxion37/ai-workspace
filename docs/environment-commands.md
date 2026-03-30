# Environment Commands

This document defines the environment entry and sync callwords used to align work across multiple Macs and chat surfaces.

## Standard Callwords

These are environment-sync requests, not project lifecycle commands.

| 호출어 | 표준 명령 | 의미 |
|---|---|---|
| `워크스페이스 동기화` | `session-start` | 작업 환경을 전체적으로 맞춘다 |
| `맥 세션` | `session-start` | 현재 Mac 기준으로 진입 상태를 맞춘다 |
| `텔레그램 세션` | `session-start` | Telegram 경유 진입 상태를 맞춘다 |

## Natural Language Aliases

Broad phrases that should be treated as environment sync requests when the intent is clear:

- `워크스페이스 동기화`
- `맥 세션 시작`
- `맥 세션 이어줘`
- `맥 작업 동기화`
- `텔레그램 세션 시작`
- `텔레그램으로 이어받기`
- `텔레그램 작업 열어줘`
- `환경 맞춰줘`
- `이 맥에서 이어간다`
- `세션 동기화`

## Contract

- Environment callwords are a sync entry, not a project lifecycle boundary.
- If the user says one of these phrases, first align the environment, then route into the needed project or session command.
- The result must be resumable on another Mac.
- A successful environment sync should leave a current Git baseline, local record, and the latest human-readable state surface available.

## Notion Rule

When an environment sync flow writes to Notion, it must follow the current Notion manual.

- The manual decides the page shape, headings, and table layout.
- If the manual changes, the record format changes with it.
- The callword only decides that syncing should happen; the manual decides how the record is written.

## Placement

Zsh convenience names are stored in `~/.dotfiles/.zshrc`.

## Agent Rule

When a user says `워크스페이스 동기화` or a broad workspace sync phrase, agents should treat it as the primary environment sync request and proceed with the baseline sync flow.

When a user says `맥 세션` or a broad Mac sync phrase, agents should treat it as an environment sync request and proceed with the baseline sync flow.

When a user says `텔레그램 세션` or a broad Telegram sync phrase, agents should treat it as an environment sync request and proceed with the same baseline sync flow.
