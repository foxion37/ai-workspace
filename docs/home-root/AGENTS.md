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

## Tool Routing

Default routing:

- Codex + GSD: coding, planning, execution, debugging, testing, refactoring, Git work, repo-state work
- Claude Code: architecture review, security review, design tradeoff calls, research synthesis, long-form drafting only when explicitly routed
- Gemini CLI: current research, alternative comparison, outside-view sanity checks

Tool retention:

- keep: Codex, GSD
- limited keep: SCC, Telegram, Notion, selected Claude-side plugins and MCP utilities with a clear non-code role
- defer: MoAI-ADK

MoAI-ADK is not part of the default environment.
It overlaps heavily with GSD and SCC, so do not install or route to it by default.

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

1. Run `프로젝트 시작` / `project-start` or `세션 시작` / `세션 재개` / `session-start` to sync the shared baseline from GitHub
2. Check `~/.orchestra/context/summary.md`
3. Scan `~/.orchestra/tasks/`
4. Check `~/.orchestra/budget.md`
5. Check pending handoffs
6. Log session start in `activity.log`

Environment sync phrases such as `워크스페이스 동기화`, `맥 세션`, `텔레그램 세션`, `이 맥에서 이어간다`, and `환경 맞춰줘` should be treated as a sync entry first, then routed into the needed project or session command.

### Session End

1. Update task status
2. Update `~/.orchestra/context/summary.md`
3. If any incident report was created or updated, rerender `~/AI-Workspace/knowledge-db/incidents/INDEX.md`
4. Update the local work note if the session created a meaningful blocker, resolution, or operating change
5. Update `decisions.md` if needed
6. Update `budget.md` if needed
7. Log session end in `activity.log`

Project lifecycle commands are documented separately in `docs/project-commands.md`.
Environment sync callwords are documented separately in `docs/environment-commands.md`.

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
- research synthesis when explicitly requested
- long-form drafting when explicitly requested

Do not send implementation, simple bug fixes, research gathering, or test writing to Claude.
Do not use Claude or Gemini as a second default executor when Codex + GSD can handle the task directly.

## Communication Style

- Keep responses short and path-first.
- Prefer summaries over long conversation logs.
- Leave final decisions in docs and the status board.
- Explain for a beginner when the user asks for cleanup or structure work.
