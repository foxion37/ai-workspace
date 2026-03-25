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
- `docs` -> local docs folder
- `manual` -> local manual/reference folder
- `developer` -> code repositories

### config and tooling

- `.dotfiles` -> reusable config repo
- `.zshrc` -> symlink to `.dotfiles/.zshrc`
- `.gitconfig` -> symlink to `.dotfiles/git/gitconfig`
- `.tmux.conf` -> symlink to `.dotfiles/tmux/tmux.conf`
- `.codex/config.toml` -> symlink to `.dotfiles/codex/config.toml`

### current gaps versus current MacBook layout

- `~/AI-Workspace` -> added as alias to `~/icloud/AI-Workspace`
- `~/notebooklm-cowork` -> added as alias to `~/icloud/AI-Workspace/knowledge-db/notebooklm-cowork`
- `~/tmux` is intentionally not treated as a shared alias baseline

## Shared Config Baseline

### tracked through `mac-dotfiles`

- `.zshrc`
- `git/gitconfig`
- `tmux/tmux.conf`
- `codex/config.toml`
- `ssh/config`

### local only

- `.gitconfig.local`
- `.claude/settings.local.json`
- `.dotfiles/.env`
- auth state, runtime DBs, logs, caches, shell history

## Current Notes

- `.zshrc` and `.gitconfig` already match the MacBook baseline closely.
- `.tmux.conf` is close but the Mac mini file has extra clipboard and copy-mode bindings.
- Figma outputs should be opened through `~/AI-Workspace/figma`; no separate `~/figma` alias is required.
- `.codex/config.toml` is richer than the MacBook version, but some parts are machine-path-specific and need filtering before becoming the shared baseline.
- `.claude/settings.json` and `.claude/settings.local.json` are not currently managed through `mac-dotfiles`.
