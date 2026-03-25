# AI Workspace Rules

This document is the shared operating rule for Claude, Codex, and Gemini.
It is written to survive a merge with the local Mac mini rule document.

## 1. Source of Truth

- The Mac mini workspace is the reference machine for this workspace layout.
- iCloud is the primary storage location for active documents, data, images, and outputs.
- GitHub private repo stores only code, directory structure, scripts, prompts, and secret-free config templates.
- NAS is used for scheduled backups and long-term recovery copies.

## 2. Read Order

Use these documents in this order:

1. `README.md` for the entry point.
2. `docs/ai-workspace-rules.md` for the top-level policy.
3. `docs/storage-map.md` for the file placement table.
4. `docs/workspace-structure.md` for the structure diagram.
5. `docs/folder-governance.md` for folders outside the workspace root.
6. `docs/tool-and-db-governance.md` for non-code assets such as DBs, docs, and tool state.
7. `docs/runbook.md` for the operating sequence.
8. `docs/decision-log.md` for the rationale.

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

## 6. Merge Rule for the Mac mini Local Document

When this document is combined with the local Mac mini rule file:

- The local Mac mini document may override machine-specific details.
- This document keeps the top-level policy for storage, secrets, and sync.
- If the two documents conflict on a machine-specific path, prefer the local path rule.
- If the two documents conflict on a storage or secret policy, prefer this document.

## 7. Operational Flow

1. Work on the Mac mini.
2. Save working data to iCloud when it is meant to sync.
3. Commit only code and workflow structure to GitHub private repo.
4. Push a backup copy to NAS on a schedule.
5. Never treat the NAS copy as the active working copy.

## 8. Practical Defaults

- Apple ecosystem is the default security layer.
- GitHub is the source for versioned structure and code.
- iCloud is the source for day-to-day files and device sync.
- NAS is the safety net.
