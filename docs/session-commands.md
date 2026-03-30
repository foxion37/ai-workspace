# Session Commands

This document defines the standard session commands, callwords, and aliases for both people and agents.

## Standard Callwords

Use these Korean phrases in conversation. They all map to the shell commands below.

| 호출어 | 표준 명령 | 의미 |
|---|---|---|
| `세션 초기화` | `session-init` | repo type에 맞는 `.sessionrc`를 만든다 |
| `세션 시작` | `session-start` | 오늘 작업 세션을 시작한다 |
| `세션 재개` | `session-start` | 다른 Mac에서 이어서 작업한다 |
| `세션 저장` | `session-save` | 날짜/시간 기반 체크포인트를 남긴다 |
| `세션 완료` | `session-finish` | validate, commit, push로 마무리한다 |

## Optional Phrases

These are also treated as environment-sync requests or `session-start` when the intent is to continue work on another machine or re-sync the environment:

- `워크스페이스 동기화`
- `이 맥에서 이어간다`
- `환경 맞춰줘`
- `세션 동기화`

The project layer has its own document:

- `project-commands.md`

Environment sync callwords are documented separately:

- `environment-commands.md`

Use the shell commands in the terminal.

## Commands

### `session-init`

Use this when a repo does not have a `.sessionrc` yet.

It does:

1. detect the repo type
2. create a starter `.sessionrc`
3. print the generated config

Detection order:

- `package.json` -> Node template
- `pyproject.toml`, `requirements.txt`, or `setup.py` -> Python template
- otherwise -> document repo template

### `session-start`

Use this before starting work on a shared baseline machine.

It does:

1. inspect the shared baseline repos only
2. stop if a repo is dirty
3. stop if local-only files are tracked
4. run `git fetch` + `git pull --ff-only`
5. run `~/.dotfiles/install.sh` if `.dotfiles` changed
6. print compact local context through the work-note helper when available

Shared baseline repos:

- `~/developer/projects/ai-workspace`
- `~/.dotfiles`

It does not sync normal project repos, iCloud working files, or local runtime state.
It now also creates or updates a human-readable local session log.
If the Notion route is wired and auth works, it also queues the matching Notion update through the queue standard.

### `session-save`

Use this when work is stopping in the middle.

It does:

1. optional cleanup
2. optional validation
3. `git add -A`
4. local commit
5. local work note update

`session-save` is a timestamped checkpoint. It keeps the local record, Git history, and any active Notion or NAS links aligned, but it does not define a version boundary for the project as a whole.

It does not push by default.

Before running it, rerender `~/AI-Workspace/knowledge-db/incidents/INDEX.md` if the session created or updated any incident report.
If the shared work-note helper is installed, it also updates the current session report and the local session-report index.

### `session-finish`

Use this when the task is ready to close out.

It does:

1. optional cleanup
2. optional validation
3. `git add -A`
4. local commit
5. `git push`
6. local work note update

Before running it, rerender `~/AI-Workspace/knowledge-db/incidents/INDEX.md` if the session created or updated any incident report.
If the shared work-note helper is installed, it also updates the current session report and the local session-report index after a successful finish.

## Optional Repo Config

If a repo needs custom validation or cleanup, create a file named `.sessionrc` at the repo root.

Example:

```bash
SESSION_CLEANUP_CMD="npm run format"
SESSION_VALIDATE_CMD="npm test"
```

Optional reporting hooks:

```bash
SESSION_CONTEXT_CMD="..."
SESSION_SAVE_WORK_NOTE_CMD="..."
SESSION_FINISH_WORK_NOTE_CMD="..."
```

These override the shared default helper when a repo needs custom behavior.

Optional dirty-status ignore patterns:

```bash
SESSION_DIRTY_IGNORE_PATTERNS=$'path/to/local-override\nanother/path'
```

Use this only for known local-only overrides that should not block `session-start`.

Current local defaults:

- `~/developer/projects/ai-workspace/.sessionrc`
  - `SESSION_VALIDATE_CMD="git diff --check"`
- `~/.dotfiles/.sessionrc`
  - `SESSION_VALIDATE_CMD="bash -n .zshrc install.sh scripts/session-common.sh scripts/session-start scripts/session-save scripts/session-finish"`
  - `SESSION_CONTEXT_CMD`, `SESSION_SAVE_WORK_NOTE_CMD`, `SESSION_FINISH_WORK_NOTE_CMD` are provided by the shared helper when available

Starter templates:

- `docs` -> `git diff --check`
- `node` -> `npm run format --if-present`, `npm run lint --if-present`, `npm test --if-present`, `npm run build --if-present`
- `python` -> `python3 -m compileall -q .` and `python3 -m pytest -q tests` when a `tests/` folder exists

## Placement

The commands live in:

- `~/.dotfiles/scripts/session-init`
- `~/.dotfiles/scripts/session-start`
- `~/.dotfiles/scripts/session-save`
- `~/.dotfiles/scripts/session-finish`

The shared reporting helper lives in:

- `~/developer/projects/ai-workspace/scripts/session_work_note.py`

The callword summary command lives in:

- `~/.dotfiles/scripts/callwords`

The human-readable local session-report index lives in:

- `~/AI-Workspace/knowledge-db/session-reports/INDEX.md`

Manual helper commands:

- `python3 ~/developer/projects/ai-workspace/scripts/session_work_note.py queue-status`
- `python3 ~/developer/projects/ai-workspace/scripts/session_work_note.py sync`

Use `queue-status` to inspect pending Notion queue items.
Use `sync` only after `NOTION_API_KEY` and the target page IDs are configured.
Use `start` to create or refresh the current session report if a session begins outside the standard wrapper.

Zsh convenience names:

- `세션초기화`
- `세션시작`
- `세션저장`
- `세션완료`

See also:

- `project-commands.md`
- `environment-commands.md`
- `callwords`

## Agent Rule

When a user says `세션 초기화`, agents should run `session-init`.

When a user says `세션 시작`, agents should run `session-start`.

When a user says `세션 재개`, agents should run `session-start`.

When a user says `세션 저장`, agents should run `session-save`.

When a user says `세션 완료`, agents should run `session-finish`.

When a user says `워크스페이스 동기화`, `이 맥에서 이어간다`, `환경 맞춰줘`, `세션 동기화`, or similar, agents should run `session-start`.

When a user says `맥 세션`, `텔레그램 세션`, or a broader environment sync phrase, agents should treat it as an environment sync request first and then proceed with the needed command.

If a meaningful blocker, resolution, or operating change happens and the user forgets to run a session command, agents should still update the local work log and related canonical artifacts, then queue Notion updates if the route is wired.
