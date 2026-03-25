# AI Tool Installation

This document defines where AI-related tools should be installed and how agents should classify them.

## Core Rule

Do not treat `developer/tools/` as the place for every installed app binary.

Use it as a managed workspace for:

- tool helper repos
- wrapper scripts
- launch scripts
- local automation
- install notes
- tool-specific config that you manage directly

## Install Decision

### 1. GUI app

If the tool is a normal macOS app, install it in:

- `/Applications`
- or `~/Applications`

Examples:

- ChatGPT
- Claude
- Cursor
- LM Studio

### 2. Git-based tool or local utility repo

If the tool is cloned from GitHub or managed as a local repo, place it in:

- `~/developer/tools/<tool-name>/`

Examples:

- local MCP helper repo
- Open WebUI repo
- Ollama helper scripts
- model management wrappers

### 3. Regular software project

If it is a buildable app or product project rather than a personal utility, place it in:

- `~/developer/projects/<project-name>/`

### 4. Outputs and prompts

If the tool generates documents, prompts, screenshots, exports, or other working files, store those in:

- `~/AI-Workspace/`

## Do Not Move

Do not force these into `developer/tools/`:

- app-managed caches
- model weights
- system-managed application support folders
- package-manager runtime files
- macOS app bundles that belong in `Applications`

## Agent Rule

When an agent is asked to install an AI-related tool:

1. Decide whether it is a GUI app, local utility repo, or normal project.
2. Use `developer/tools/` only for managed tool workspaces and helper repos.
3. Use `Applications` for normal macOS apps.
4. Use `AI-Workspace` for outputs, not for installed software.

## Local Convention

For this machine, the preferred place for agent-managed AI tool helpers is:

- `~/developer/tools/`

Examples:

- `~/developer/tools/tmux`
- `~/developer/tools/codex-monitoring`
