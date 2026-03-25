# Machine Baselines

This folder stores the machine-level comparison baseline for the workspace.

## Purpose

- capture the current MacBook home layout
- capture the current Mac mini home layout
- compare the two without turning runtime or secret files into shared assets
- define the standard home-root entries that should feel identical across both Macs

## Files

- `macbook-home-manifest.md`: current known baseline from this Mac
- `macmini-home-manifest.md`: target baseline from the Mac mini reference machine
- `diff-report.md`: comparison output and convergence checklist
- `../home-root/`: canonical home-root policy docs deployed to `~/`

## Working Rule

- Mac mini is the initial reference machine.
- GitHub stores the shared baseline after the first comparison pass.
- `ai-workspace` holds the policy and machine manifests.
- `mac-dotfiles` holds the reusable config that gets applied on each machine.
- `ai-workspace/docs/home-root/` is the source of truth for `~/AGENTS.md` and `~/CLAUDE.md`.
- `mac-dotfiles` is the source of truth for `.bashrc`, `.zprofile`, and root bootstrap scripts.
