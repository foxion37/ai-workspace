# Session Commands

This document defines the standard end-of-work commands for both people and agents.

## Natural Language Mapping

- `세션 초기화` means `session-init`
- `세션 저장` means `session-save`
- `세션 완료` means `session-finish`

Use the Korean phrases in conversation.
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

### `session-save`

Use this when work is stopping in the middle.

It does:

1. optional cleanup
2. optional validation
3. `git add -A`
4. local commit

It does not push by default.

### `session-finish`

Use this when the task is ready to close out.

It does:

1. optional cleanup
2. optional validation
3. `git add -A`
4. local commit
5. `git push`

## Optional Repo Config

If a repo needs custom validation or cleanup, create a file named `.sessionrc` at the repo root.

Example:

```bash
SESSION_CLEANUP_CMD="npm run format"
SESSION_VALIDATE_CMD="npm test"
```

Current local defaults:

- `~/developer/projects/ai-workspace/.sessionrc`
  - `SESSION_VALIDATE_CMD="git diff --check"`
- `~/.dotfiles/.sessionrc`
  - `SESSION_VALIDATE_CMD="bash -n .zshrc install.sh scripts/session-common.sh scripts/session-save scripts/session-finish"`

Starter templates:

- `docs` -> `git diff --check`
- `node` -> `npm run format --if-present`, `npm run lint --if-present`, `npm test --if-present`, `npm run build --if-present`
- `python` -> `python3 -m compileall -q .` and `python3 -m pytest -q tests` when a `tests/` folder exists

## Placement

The commands live in:

- `~/.dotfiles/scripts/session-init`
- `~/.dotfiles/scripts/session-save`
- `~/.dotfiles/scripts/session-finish`

Zsh convenience names:

- `세션초기화`
- `세션저장`
- `세션완료`

## Agent Rule

When a user says `세션 초기화`, agents should run `session-init`.

When a user says `세션 저장`, agents should run `session-save`.

When a user says `세션 완료`, agents should run `session-finish`.
