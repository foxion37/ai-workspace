# Multi-Agent Orchestration — Shared Operating Spec (2026 H1)

## Purpose

This document is the canonical home-root operating spec for `~/AGENTS.md`.
Use it on any Mac where the same person works across the same workspace model.

Related documents:

- Claude-specific behavior: `~/CLAUDE.md`
- machine manifests and sync rules: `~/developer/projects/ai-workspace/docs/`
- status board and logs: `~/.orchestra/`

## Role

The default operating model is **Codex-led**.

- Codex: PM + main worker
- Claude Code: senior reviewer
- Gemini CLI: research engine

Codex handles task decomposition, implementation, testing, and status management.
Claude focuses on architecture, security, and consistency review.

## Home Root Standard

Treat the home root as a routing layer, not as one giant repo.

Shared standard entries:

- `~/AI-Workspace`
- `~/developer`
- `~/.dotfiles`
- `~/AGENTS.md`
- `~/CLAUDE.md`

Bootstrap files may also be standardized through `~/.dotfiles`, for example:

- `~/.bashrc`
- `~/.zprofile`
- `~/orchestra-init-codex-led.sh`

Usually local-only:

- `~/Library`
- `~/Applications`
- hidden runtime or cache directories such as `~/.codex`, `~/.claude`, `~/.cache`, `~/.npm`, `~/.config`
- auth state, logs, runtime DBs, shell history

Cleanup candidates unless explicitly standardized:

- `~/docs`
- `~/manual`
- legacy backup files in the home root

## Task Management Protocol

Global task status is managed under `~/.orchestra/`.

Key structure:

- `.orchestra/tasks/`: task definitions and status
- `.orchestra/handoffs/`: Claude/Gemini outputs
- `.orchestra/reviews/`: Codex self review
- `.orchestra/logs/activity.log`: activity log
- `.orchestra/context/summary.md`: session summary
- `.orchestra/decisions.md`: major decisions
- `.orchestra/budget.md`: model budget tracking

Task files should use:

- `Status`: `pending | in_progress | self_review | claude_review | done | blocked`
- `Worker`: `codex | codex+gemini | codex+claude`
- `Priority`: `P0 | P1 | P2`
- `Claude필요`: `yes | no`

## Working Rules

- Prefer `~/AI-Workspace` for shared documents, prompts, references, and outputs.
- Prefer `~/developer` for repos, scripts, and code work.
- Use `~/developer/tools` for helper repos and local utility workspaces.
- Keep manual safety snapshots under `~/developer/backups/manual-snapshots/`.
- Do not create new standard aliases like `~/figma` or `~/notebooklm-cowork`.
- If a home-root folder role is unclear, default to `keep` first and document it before moving it.

## Session Routines

### Session Start

1. Check `~/.orchestra/context/summary.md`
2. Scan `~/.orchestra/tasks/`
3. Check `~/.orchestra/budget.md`
4. Check pending handoffs
5. Log session start in `activity.log`

### Session End

1. Update task status
2. Update `~/.orchestra/context/summary.md`
3. Update `decisions.md` if needed
4. Update `budget.md` if needed
5. Log session end in `activity.log`

## Delegation Rules

Codex does:

- implementation
- debugging
- refactoring
- test writing and execution
- Git work
- task decomposition and prioritization
- self review

Send to Gemini:

- current research
- alternative comparison
- document drafts
- outside-view sanity checks

Send to Claude:

- architecture review
- security review
- design tradeoff calls
- interface consistency review

Do not send implementation, simple bug fixes, research gathering, or test writing to Claude.

## Communication Style

- Keep responses short and path-first.
- Prefer summaries over long conversation logs.
- Leave final decisions in docs and the status board.
- Explain for a beginner when the user asks for cleanup or structure work.
