# Remaining Tasks Checklist

Current status:

- `ai-workspace` policy docs are pushed
- `mac-dotfiles` shared baseline is pushed
- Mac mini workspace aliases are created
- Mac mini SSH publickey login is working
- home-root policy docs now have a canonical source under `ai-workspace/docs/home-root/`
- home-root bootstrap files now have a canonical source under `mac-dotfiles`

## Priority 1: Codex Local Override Split

- [ ] Decide the final split between shared Codex baseline and Mac mini-only GSD additions
- [ ] Move Mac mini-only Codex additions into a local-only override path or documented local patch flow
- [ ] Keep shared `mac-dotfiles/codex/config.toml` machine-neutral
- [ ] Verify MacBook Codex still works with the shared baseline
- [ ] Verify Mac mini Codex still works after the local-only split

## Priority 2: Claude Config Split

- [ ] Compare MacBook `~/.claude/settings.json` with Mac mini `~/.claude/settings.json`
- [ ] Extract only machine-neutral settings into the shared baseline
- [ ] Keep machine-path hooks and local permission exceptions in `settings.local.json`
- [ ] Confirm both machines still start Claude with the intended hooks and plugins

## Priority 3: Dotfiles Deployment Consistency

- [ ] Run `./install.sh` on Mac mini after final dotfiles changes are settled
- [ ] Confirm `~/.bashrc`, `~/.zprofile`, `~/.zshrc`, `~/.gitconfig`, `~/.tmux.conf`, and `~/.codex/config.toml` point to `.dotfiles`
- [ ] Confirm `~/orchestra-init-codex-led.sh` points to `.dotfiles/scripts/orchestra-init-codex-led.sh`
- [ ] Confirm `ssh/config` still supports passwordless `ssh mini` from MacBook
- [ ] Confirm local-only files remain untracked: `.env`, `.gitconfig.local`, `.zshrc.local`, `settings.local.json`

## Priority 4: Documentation Closure

- [ ] Verify `~/AGENTS.md` and `~/CLAUDE.md` deploy from `ai-workspace/docs/home-root/`
- [ ] Remove `~/docs` and `~/manual` from the target standard home layout after content triage
- [ ] Update `diff-report.md` again once `docs` and `manual` are fully cleared or rehomed

## Final Verification

- [ ] `ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no -T mini exit` succeeds
- [ ] `git -C ~/.dotfiles status --short` is clean on MacBook
- [ ] `git -C ~/.dotfiles status --short` is clean on Mac mini
- [ ] `git -C ~/developer/projects/ai-workspace status --short` is clean on both machines
- [ ] Both machines can enter the shared workspace through:
  - `~/AI-Workspace`
