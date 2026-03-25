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

### `/Users/seongqkim/developer/tools/tmux`

- Classify per project.
- If they contain active cross-device materials, mirror the document layer into `AI-Workspace`.
- If they are tool-specific or temporary, keep them in place and back them up only if needed.

Current default:

- `developer/tools/tmux` -> keep as local helper tooling

Note:

- Figma outputs are no longer part of the default home-level workspace layout.
- `notebooklm-cowork` was removed from the home layout and should not be recreated as a standard alias.

### home-root policy docs

- Keep `~/AGENTS.md` and `~/CLAUDE.md` as standard home-root entry documents.
- Canonical source lives in `ai-workspace/docs/home-root/`.
- Deployed copies in the home root should be links or generated copies, not hand-maintained snowflakes.

### home-root bootstrap files

- Keep `.bashrc`, `.zprofile`, and other bootstrap scripts in `~/.dotfiles`.
- Deploy them into the home root from `mac-dotfiles`.
- Do not treat runtime state or local overrides as shared bootstrap.

### `/Users/seongqkim/docs`

- Do not treat `~/docs` as a permanent standard folder.
- If it contains active shared documents, move them into `AI-Workspace/docs/`, `reference/`, or `archive/`.
- Otherwise classify it as a cleanup candidate and remove it from the standard home layout.

### `/Users/seongqkim/manual`

- Do not treat `~/manual` as a permanent standard folder.
- Move reusable references into `AI-Workspace/reference/` or another intentional location.
- After migration, remove it from the standard home layout.

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
- `AGENTS.md`, `CLAUDE.md` -> keep as standard home-root policy docs
- `.bashrc`, `.zprofile`, home bootstrap scripts -> keep through `mac-dotfiles`
- `docs`, `manual` -> cleanup candidate unless intentionally rehomed
- hidden config and cache folders -> ignore
- `AI-Workspace` -> adopt as the shared document layer
