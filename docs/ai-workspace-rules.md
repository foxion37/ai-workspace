# AI Workspace Rules

This document is the top-level policy for storage, sync, and secret handling.
Keep exact path decisions in `docs/sync-matrix.md` and machine-specific facts in `docs/machines/`.

## 1. Source of Truth

- The Mac mini workspace is the reference machine for this workspace layout.
- iCloud is the primary storage location for active documents, data, images, and outputs.
- GitHub private repo stores only code, directory structure, scripts, prompts, and secret-free config templates.
- NAS is used for scheduled backups and long-term recovery copies.

## 2. Read Order

Use these documents in this order:

1. `docs/README.md` for the document map.
2. `docs/ai-workspace-rules.md` for top-level policy.
3. `docs/sync-matrix.md` for tracked, template-only, and local-only paths.
4. `docs/session-commands.md` for session automation behavior.
5. `docs/home-root/AGENTS.md` for home-root operating rules.

## 3. Storage Policy

### Keep in iCloud

- Working documents
- Reference files
- Images
- Final outputs
- Notes
- Small exported artifacts that need to move across devices

### Keep in GitHub Private Repo

- Code
- Folder structure rules
- Prompts
- Templates
- Non-secret config files
- Documentation that describes the workflow

GitHub is the shared baseline for reusable structure only. Do not use it to move local-only machine state between Macs.

### Keep in NAS

- Periodic backups
- Archived files
- Large binary files
- Recovery snapshots

### Keep only on device

- Temporary cache
- Build cache
- Scratch files
- Local-only exports that are not meant to be synced

## 4. Secret Policy

- Do not store passwords, passkeys, tokens, or account secrets in GitHub.
- Use iCloud Keychain or Apple Passwords for credentials.
- Use macOS Keychain for Mac-specific secure items when needed.
- If Chrome needs password storage, keep it aligned with the Apple/Google account policy chosen for the workspace.

## 5. Agent-Neutral Working Rules

- Keep instructions short, explicit, and reproducible.
- Prefer plain language over agent-specific jargon.
- State assumptions instead of hiding them.
- If a file or rule is ambiguous, do not invent a new meaning.
- When multiple agents read the same rule, they must be able to follow it without extra context.

## 6. Operational Flow

1. Work on the Mac mini.
2. Save working data to iCloud when it is meant to sync.
3. Commit only code and workflow structure to GitHub private repo.
4. Push a backup copy to NAS on a schedule.
5. Never treat the NAS copy as the active working copy.

## 7. Practical Defaults

- Apple ecosystem is the default security layer.
- GitHub is the source for versioned structure and code.
- iCloud is the source for day-to-day files and device sync.
- NAS is the safety net.
