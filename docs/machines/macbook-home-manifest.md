# MacBook Home Manifest

Generated from the current machine on 2026-03-25.

## Home Root

- path: `/Users/seongqkim`
- role: local home routing layer
- canonical sync path for documents: `/Users/seongqkim/AI-Workspace`

## Top-Level Structure

### shared workspace and knowledge

- `AI-Workspace` -> iCloud-backed shared document layer

### code and config

- `developer` -> code repositories
- `developer/tools/tmux` -> local tmux helper scripts
- `.dotfiles` -> shell, Git, and SSH config source

### intake

- `Desktop` -> intake only
- `Downloads` -> intake only

### machine-local or backup

- `Library` -> app-owned machine state
- `Applications` -> app-owned machine state
- `developer/backups/manual-snapshots/2026-03-25` -> manual backup snapshot location

## Shared Config Baseline

### tracked directly

- `.bashrc`
- `.dotfiles/.zshrc`
- `.dotfiles/git/gitconfig`
- `.dotfiles/tmux/tmux.conf`
- `skills-lock.json`
- `.codex/config.toml` (stable settings only)
- `.codex/AGENTS.md`
- `.codex/rules/default.rules`
- `.claude/settings.json`
- `.claude/agents/**`
- `.claude/commands/**`
- `.claude/hooks/**`
- `.claude/package.json`

### template only

- `.dotfiles/ssh/config`

### local only

- `.dotfiles/.env`
- `.gitconfig.local`
- `.zshrc.local`
- `ssh/config.local`
- `.claude/settings.local.json`
- `.codex/auth.json`
- runtime DBs, logs, caches, session history

## Current Notes

- `.zshrc` sources `.dotfiles/.env`, but the checked token variables are currently empty.
- `.claude/settings.local.json` references environment variable names and local permissions, so it stays local-only.
- `figma` and `notebooklm-cowork` were removed from the home-level workspace layout on 2026-03-25.
- `.codex/config.toml` currently contains stable model, MCP, and trust settings without embedded secrets.
