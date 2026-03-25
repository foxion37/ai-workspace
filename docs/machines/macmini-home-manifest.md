# Mac mini Home Manifest

Captured from the reference machine after SSH key auth was restored on 2026-03-25.

## Home Root

- path: `/Users/barq`
- role: reference machine for richer local tool setup
- physical iCloud entry: `/Users/barq/icloud/AI-Workspace`
- preferred cross-machine alias target: `/Users/barq/AI-Workspace`

## Top-Level Structure

### workspace and routing

- `icloud` -> symlink to iCloud Drive root
- `developer` -> code repositories

### config and tooling

- `.dotfiles` -> reusable config repo
- `AGENTS.md` -> home-root policy doc sourced from `ai-workspace`
- `CLAUDE.md` -> Claude-specific home-root policy doc sourced from `ai-workspace`
- `.bashrc` -> bootstrap file sourced from `mac-dotfiles`
- `.zprofile` -> bootstrap file sourced from `mac-dotfiles`
- `orchestra-init-codex-led.sh` -> shared bootstrap script sourced from `mac-dotfiles`
- `.zshrc` -> symlink to `.dotfiles/.zshrc`
- `.gitconfig` -> symlink to `.dotfiles/git/gitconfig`
- `.tmux.conf` -> symlink to `.dotfiles/tmux/tmux.conf`
- `.codex/config.toml` -> symlink to `.dotfiles/codex/config.toml`

### current gaps versus current MacBook layout

- `~/AI-Workspace` -> added as alias to `~/icloud/AI-Workspace`
- `~/tmux` is intentionally not treated as a shared alias baseline

### cleanup candidates

- `~/docs` -> stray local document folder, not part of the target standard layout
- `~/manual` -> local reference folder, not part of the target standard layout

## Shared Config Baseline

### tracked through `mac-dotfiles`

- `.bashrc`
- `.zprofile`
- `.zshrc`
- `git/gitconfig`
- `tmux/tmux.conf`
- `codex/config.toml`
- `ssh/config`
- `scripts/orchestra-init-codex-led.sh`

### tracked through `ai-workspace`

- `docs/home-root/AGENTS.md`
- `docs/home-root/CLAUDE.md`

### local only

- `.gitconfig.local`
- `.claude/settings.local.json`
- `.dotfiles/.env`
- auth state, runtime DBs, logs, caches, shell history

## Standard Home Root Entries

- `~/AI-Workspace`
- `~/developer`
- `~/.dotfiles`
- `~/AGENTS.md`
- `~/CLAUDE.md`
- `~/.bashrc`
- `~/.zprofile`
- `~/orchestra-init-codex-led.sh`

## Current Notes

- `.zshrc` and `.gitconfig` already match the MacBook baseline closely.
- `.tmux.conf` is close but the Mac mini file has extra clipboard and copy-mode bindings.
- `~/figma` and `~/notebooklm-cowork` are not part of the current baseline and should not be kept as standard aliases.
- `.codex/config.toml` is richer than the MacBook version, but some parts are machine-path-specific and need filtering before becoming the shared baseline.
- `.claude/settings.json` and `.claude/settings.local.json` are not currently managed through `mac-dotfiles`.
- `~/docs` and `~/manual` remain present locally but are no longer part of the target standard home layout.
