# Folder Governance

This document defines how folders outside `AI-Workspace` should be handled.

## Core Rule

Not every folder under `/Users/seongqkim` should be synced into `AI-Workspace`.

Each folder must be classified into one of these states:

- `adopt`: move or mirror into `AI-Workspace`
- `keep`: leave in place and manage where it already lives
- `backup`: do not use as an active workspace, but include in NAS backup
- `ignore`: do not manage as part of the workspace

## Classification Rules

### adopt

Use `adopt` when a folder is:

- an active working folder
- reusable across devices
- mostly documents, references, outputs, prompts, or project assets
- useful to Claude, Codex, and Gemini as shared context

Typical examples:

- project notes
- reference image collections
- reusable prompt sets
- working documents now scattered on `Desktop`

### keep

Use `keep` when a folder:

- already has a valid home
- is app-specific or ecosystem-specific
- is a code repository that should stay under `developer`
- is better managed by another tool

Typical examples:

- `developer/`
- `Library/`
- `Applications/`
- `Pictures/`

### backup

Use `backup` when a folder:

- is important but not part of the active workspace
- contains historical data
- is too large for day-to-day iCloud sync

Typical examples:

- old exports
- archived media
- legacy snapshots
- large reference bundles

### ignore

Use `ignore` when a folder:

- is cache, temp, or generated state
- is machine-local state
- can be recreated

Typical examples:

- hidden cache folders
- package manager caches
- temporary download folders
- agent session caches

## Home Directory Rules

### `/Users/seongqkim/Desktop`

- Treat as an intake area, not a canonical workspace.
- New working material should be triaged into `AI-Workspace/inbox/`, `reference/`, or `outputs/`.
- Folders that remain active for more than a short period should be reclassified and moved intentionally.

### `/Users/seongqkim/Documents`

- Keep app-owned or personal document storage in place unless it becomes part of the shared workspace.
- Historical backup folders should be classified as `backup`.
- Manual safety snapshots should not be created in the home root. Put them under `developer/backups/manual-snapshots/` or inside the folder being changed.

### `/Users/seongqkim/Downloads`

- Treat as disposable intake.
- Files should be moved out quickly to `AI-Workspace`, a code repo, or deleted.

### `/Users/seongqkim/developer`

- Keep as the source area for code repositories.
- Do not fold all code repos into `AI-Workspace`.
- Only shared rules, prompts, and workspace-level documentation should be mirrored into `AI-Workspace`.

### `/Users/seongqkim/notebooklm-cowork`, `/Users/seongqkim/developer/tools/tmux`

- Classify per project.
- If they contain active cross-device materials, mirror the document layer into `AI-Workspace`.
- If they are tool-specific or temporary, keep them in place and back them up only if needed.

Current default:

- `notebooklm-cowork` -> adopt as shared knowledge DB
- `developer/tools/tmux` -> keep as local helper tooling

Note:

- Figma outputs should live under `AI-Workspace/figma`.
- A separate home-level `~/figma` alias is not required.

## Triage Process

For any folder outside `AI-Workspace`, decide in this order:

1. Is this active working context across devices?
2. Is this code or tool runtime state?
3. Does this need backup only?
4. Can this be ignored?

If the answer is unclear, default to `keep` first and move only after the folder role is stable.

## Immediate Defaults

- `Desktop` -> intake, then reclassify
- `Documents/backup` -> backup
- `Downloads` -> ignore after triage
- `developer` -> keep
- hidden config and cache folders -> ignore
- `AI-Workspace` -> adopt as the shared document layer
