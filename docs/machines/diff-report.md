# Machine Diff Report

## Status

- current status: first live comparison completed
- comparison target: MacBook -> GitHub baseline -> Mac mini

## Confirmed Differences

### path aliases missing on Mac mini

- `~/AI-Workspace`

`~/AI-Workspace` was added as a compatibility symlink that points into `~/icloud/AI-Workspace`.

### same shape, mostly aligned

- `.zshrc` -> symlink to `.dotfiles/.zshrc` on both machines
- `.gitconfig` -> symlink to `.dotfiles/git/gitconfig` on both machines
- `.tmux.conf` -> symlink to `.dotfiles/tmux/tmux.conf` on both machines

### shared config divergence

- `mac-dotfiles/ssh/config`
  - MacBook has `mini` host and Colima include
  - Mac mini only has GitHub host config
- `mac-dotfiles/codex/config.toml`
  - Mac mini has a richer baseline
  - parts of that file depend on `/Users/barq/...` and local GSD files

### intentionally local differences

- Mac mini has `icloud`, `docs`, and `manual`
- MacBook uses `AI-Workspace` as the only standard home-level workspace entry point
- MacBook keeps `developer/tools/tmux/dev.sh` as local tooling, while Mac mini uses `~/.tmux/plugins/tpm`

## Convergence Rule

- make document workspace entry paths match by adding aliases on Mac mini
- use `mac-dotfiles` as the actual shared config repo
- promote only machine-neutral parts of richer Mac mini config into the shared baseline
- keep machine-path hooks, auth, secrets, and runtime state local
