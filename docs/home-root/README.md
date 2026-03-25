# Home Root Canonical Docs

This directory stores the canonical documents deployed to the home root on each Mac.

## Source Of Truth

- `AGENTS.md` -> deployed to `~/AGENTS.md`
- `CLAUDE.md` -> deployed to `~/CLAUDE.md`

These files belong in `ai-workspace` because they define home-root policy and cross-machine structure, not local shell bootstrap.

## Related Repos

- `ai-workspace` -> home-root policy, machine manifests, sync rules
- `mac-dotfiles` -> `.bashrc`, `.zprofile`, shell/tool bootstrap, install-time links

## Working Rule

- Edit the canonical files here.
- Keep deployed home-root copies as links or generated copies.
- Do not treat `~/docs` or `~/manual` as permanent standard folders.
- Do not store secrets, auth state, caches, or runtime logs here.

## Deployment

Use:

```bash
~/developer/projects/ai-workspace/scripts/link-home-root-docs.sh
```

That script links `~/AGENTS.md` and `~/CLAUDE.md` to the canonical files here and makes a timestamped backup first if needed.
