# Sync Matrix

This document is the official baseline for MacBook -> GitHub -> Mac mini sync.

Use it to decide which paths are:

- tracked directly in Git
- kept as templates only
- local-only

Mac mini is the initial reference machine for structure.
After the first alignment pass, GitHub becomes the distribution source for the shared baseline.

## Repositories

- `ai-workspace` repo stores policy, sync rules, and machine manifests
- `mac-dotfiles` repo stores actual reusable shell and tool config

## Rules

- Track structure, rules, templates, and stable config in Git.
- Do not track secrets, auth state, runtime DBs, logs, or local-only overrides.
- Keep iCloud knowledge assets out of Git unless they are lightweight rules or documents.
- If a path needs machine-specific values, track a template and keep the final values local.

## Matrix

| Path | Category | Git Tracked | Template Only | Local Only | Notes |
| --- | --- | --- | --- | --- | --- |
| `AI-Workspace` | knowledge root | no | no | yes | iCloud-backed working data, not a Git payload |
| `developer` | code area | no | no | yes | repos live here, but this home-level path is not the shared baseline |
| `figma` | knowledge | no | no | yes | synced through iCloud and backup |
| `notebooklm-cowork` | knowledge | no | no | yes | shared knowledge DB, not a Git payload |
| `tmux` | config | yes | no | no | reusable tool config folder |
| `.bashrc` | config | yes | no | no | lightweight shell bootstrap |
| `.dotfiles/.zshrc` | config | yes | no | no | shared shell behavior |
| `.dotfiles/git/gitconfig` | config | yes | no | no | shared Git defaults |
| `.dotfiles/tmux/tmux.conf` | config | yes | no | no | shared tmux behavior |
| `.dotfiles/ssh/config` | config | no | yes | no | keep shared shape only, final values belong in local overlay |
| `.dotfiles/.env` | secret | no | no | yes | may hold shell-exposed tokens |
| `.env.local` | secret | no | no | yes | local-only env values |
| `.gitconfig.local` | local override | no | no | yes | local Git behavior |
| `.zshrc.local` | local override | no | no | yes | machine-specific shell additions |
| `ssh/config.local` | local override | no | no | yes | machine-specific SSH targets and overrides |
| `.codex/config.toml` | config | yes | no | no | only stable, secret-free settings |
| `.codex/AGENTS.md` | config | yes | no | no | stable local agent guidance |
| `.codex/rules/default.rules` | config | yes | no | no | shared Codex behavior |
| `.codex/auth.json` | secret | no | no | yes | auth state |
| `.codex/history.jsonl` | runtime | no | no | yes | session history |
| `.codex/log*` | runtime | no | no | yes | logs |
| `.codex/*.sqlite` | runtime | no | no | yes | runtime DBs |
| `.claude/settings.json` | config | yes | no | no | stable Claude setup |
| `.claude/settings.local.json` | local override | no | no | yes | local permissions and env-sensitive behavior |
| `.claude/agents/**` | config | yes | no | no | reusable agent definitions |
| `.claude/commands/**` | config | yes | no | no | reusable commands |
| `.claude/hooks/**` | config | yes | no | no | reusable hooks |
| `.claude/package.json` | config | yes | no | no | plugin/hook dependency metadata |
| `.claude/debug/**` | runtime | no | no | yes | debug output |
| `.claude/cache/**` | runtime | no | no | yes | cache |
| `.claude/backups/**` | runtime | no | no | yes | generated backups |
| `*.local-backup-*` | backup | no | no | yes | recovery-only snapshots |

## Notes

- If a tracked config later needs secrets or machine-specific values, split it into a tracked template and a local override.
- Use `docs/machines/` for actual machine manifests and diff reports.
- `~/AI-Workspace`, `~/figma`, and `~/notebooklm-cowork` are the preferred cross-machine entry paths even if the physical iCloud path differs per machine.
- `tmux` top-level helper folders are not part of the cross-machine baseline; use `.dotfiles/tmux` and `~/.tmux.conf` as the shared tmux source.
