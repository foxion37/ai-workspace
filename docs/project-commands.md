# Project Commands

This document defines the standard project commands, callwords, aliases, and sync contract.

## Standard Callwords

Use these Korean phrases in conversation. They map to the project lifecycle wrappers below.

| 호출어 | 표준 명령 | 의미 |
|---|---|---|
| `프로젝트 시작` | `project-start` | 프로젝트 전체 기준 상태를 연다 |
| `프로젝트 저장` | `project-save` | 버전 단위 정본을 남긴다 |
| `프로젝트 재개` | `project-resume` | 다른 Mac에서 같은 프로젝트를 다시 연다 |
| `프로젝트 완료` | `project-finish` | validate, commit, push, archive로 닫는다 |

## Natural Language Aliases

The following broad phrases also map to the project lifecycle when the intent is clear:

- `프로젝트 시작해줘`
- `프로젝트 이어줘`
- `프로젝트 저장해`
- `프로젝트 재개할게`
- `이 프로젝트 마무리`
- `프로젝트를 버전으로 묶어줘`
- `프로젝트 기록 남겨줘`

## Commands

### `project-start`

Use this when a new project cycle begins or when you want to open the project baseline on a different Mac.

It does:

1. sync the shared baseline
2. read the current project state
3. initialize the project surface if needed
4. prepare the next session entry point

### `project-save`

Use this when you want to freeze a project version.

It does:

1. optional cleanup
2. optional validation
3. `git add -A`
4. local commit
5. project-version work note update
6. Notion project record update through the current manual
7. NAS/archive handoff when applicable

### `project-resume`

Use this when you want to reopen the project as a whole, often from another Mac.

It behaves like `project-start` with the intent that the project state should be reconstructed from the latest synced sources.

### `project-finish`

Use this when the project is ready to close.

It does:

1. optional cleanup
2. optional validation
3. `git add -A`
4. local commit
5. `git push`
6. final project record update
7. archive handoff when applicable

## Contract

- `project-save` is version-based.
- `project-resume` restores the versioned project baseline.
- `project-save` and `project-finish` both keep local record, Git history, Notion record, and NAS/archive state aligned.
- The project layer is the container for one or more sessions.
- A project can have many sessions, but a session does not exist independently of a project.
- Natural language aliases are broad, but the short standard form stays `프로젝트 시작`.

## Placement

The wrappers live in:

- `~/.dotfiles/scripts/project-start`
- `~/.dotfiles/scripts/project-resume`
- `~/.dotfiles/scripts/project-save`
- `~/.dotfiles/scripts/project-finish`

The shared helper that writes project and session notes lives in:

- `~/developer/projects/ai-workspace/scripts/session_work_note.py`

## Agent Rule

When a user says `프로젝트 시작`, agents should run `project-start`.

When a user says `프로젝트 저장`, agents should run `project-save`.

When a user says `프로젝트 재개`, agents should run `project-resume`.

When a user says `프로젝트 완료`, agents should run `project-finish`.

When a user says a broad project-start/save/resume/finish phrase with the same intent, normalize it to the matching project command.
