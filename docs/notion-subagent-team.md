# Notion Subagent Team

This document defines the specialist subagent team for future Notion-heavy sessions.

Use this team when the work is primarily about Notion structure, routing, dashboards, sync, or human-readable operations.

## Core Rule

Keep these rules fixed:

- local-first / Notion-second
- `ops` vs `project` routing
- human-first dashboard
- raw logs stay local
- Notion mirrors status, not full raw history

## Efficiency Decision

Running all four roles every day is inefficient.

Recommended cadence:

- `Operations`: daily when state changed
- `Maintenance`: 2-3 times per week, or after visible structure drift
- `Development`: event-driven when templates, sync, page IDs, or project surfaces change
- `Growth`: weekly review, not daily

This keeps daily cost low while preserving visibility.

## Team Roles

### Maintenance

Mission:

- keep the current Notion structure readable and consistent

Owns:

- broken links
- duplicate pages
- stale titles
- drift in `current / reports / check log`
- `pending` / `not_configured` cleanup triage

KPIs:

- broken-link count
- stale-page count
- queue aging
- current-page freshness

### Operations

Mission:

- keep `ops log`, incident state, and shared status surfaces trustworthy

Owns:

- `ops log`
- queue inspection
- routing correctness
- incident state reflection
- shared infra and cross-repo status mirrors

KPIs:

- ops log freshness
- route accuracy
- local/Notion mismatch count
- queue backlog

### Development

Mission:

- make implementation state readable without turning Notion into a code dump

Owns:

- project `current`
- `reports`
- `check log`
- project templates
- project-specific status mirrors

KPIs:

- current-page freshness
- report delay after meaningful change
- check-log aging
- next-session context restore speed

### Growth

Mission:

- improve findability, adoption, and repeat usefulness of the Notion system

Owns:

- information architecture improvements
- naming and entry-flow polish
- template evolution
- dashboard usage review
- expansion priorities

KPIs:

- first-click success
- repeated-question reduction
- `current` adoption
- useful-page retention vs unused-page growth

## Default Session Flow

1. `Operations` decides whether the session routes to `ops` or `project`.
2. `Development` updates project surfaces only if implementation state changed.
3. `Maintenance` cleans drift created by the session.
4. `Growth` runs only when there is a repeated pattern worth standardizing.

## Anti-Patterns

- running all four roles every day regardless of signal
- treating Notion as raw log storage
- mixing shared infra notes into project hubs
- optimizing page aesthetics before route clarity
- changing structure without recording the rule locally
- fixing local canonical truth last

## Lead Rule

Codex remains the PM and main executor.

The Notion team is a specialist sidecar:

- `Operations` is the default lead
- `Maintenance`, `Development`, and `Growth` are activated as needed
