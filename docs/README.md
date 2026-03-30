# Docs Map

Use this file to decide which document to open first.

## Canonical Docs

- `ai-workspace-rules.md`: top-level policy for storage, sync, secrets, and backups
- `sync-matrix.md`: exact tracked, template-only, and local-only path rules
- `session-commands.md`: standard session command behavior
- `project-commands.md`: project lifecycle, version saves, and project sync contract
- `environment-commands.md`: environment entry and sync callwords such as `맥 세션` and `텔레그램 세션`
- `notion-queue-operating-standard.md`: canonical Notion queue, source-of-truth, and logging contract
- `notion-obsidian-style-guide.md`: supplementary title, icon, heading, link, tag, and emphasis rules
- `notion-subagent-team.md`: supplementary role split and cadence for Notion specialist subagents
- `home-root/AGENTS.md`: home-root operating routine for Codex-led work

## Reference Docs

- `folder-governance.md`: folder classification rules outside `AI-Workspace`
- `tool-and-db-governance.md`: policy categories for tools, DBs, runtime state, and secrets
- `home-root/README.md`: how home-root docs are deployed
- `machines/README.md`: how machine baseline docs are organized

## State Docs

- `machines/macbook-home-manifest.md`: current MacBook facts
- `machines/macmini-home-manifest.md`: current Mac mini facts
- `machines/diff-report.md`: convergence notes between the two Macs
- `machines/remaining-tasks-checklist.md`: open follow-up tasks

## Rules

- Define each rule once in a canonical doc.
- Keep user-specific paths in `machines/` docs, not policy docs.
- Prefer logical paths such as `~/AI-Workspace` in policy text.
- Treat checklists and manifests as state, not policy.
