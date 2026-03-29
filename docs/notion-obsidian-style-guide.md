# Notion Obsidian Style Guide

This document defines the style layer for Notion and Obsidian.

Use `docs/notion-human-ops-standard.md` for the operating contract.
Use this file for naming, icon, heading, link, tag, and emphasis rules.

## Role Split

- `notion-human-ops-standard.md` owns zone, approval, routing, and operating structure
- this guide owns display and writing rules
- when the two documents overlap, the operating contract wins

## Naming Rules

### Notion

Use Korean-first page titles with optional English labels for search and agent readability.

Recommended format:

- `<Korean Name> (<english label>)`

Examples:

- `노션 운영 매뉴얼 (notion manual)`
- `대시보드 보수 체크리스트 (maintenance checklist)`

Fixed functional page names stay in English:

- `dashboard`
- `developer`
- `Ops Center`
- `current`
- `reports`
- `check log`
- `ops log`
- `references`

### Obsidian

Use English-first note names.
Do not use Korean-English bilingual titles by default.

Recommended format:

- `notion-obsidian-style-guide`
- `project-dashboard-template`
- `session-report-2026-03-29`

If a human-friendly Korean label matters later, store it in note body or frontmatter, not in the filename.

### Version And Date Labels

- stable policy or standard docs: `1.0`, `2.0`
- working revisions: `v2`, `v3`
- dated proposals, reports, or logs: `YYYY-MM-DD`

Do not mix version and date in one display title unless the document is explicitly a dated release record.

## Icon Rules

Default rule:

- keep hub, policy, and neutral pages on gray icons
- use color only when the page needs an active status signal
- use Notion icons before emojis

### Color Exceptions

Use color as a controlled status signal.

- `red`: needs review now, blocking issue, high-risk approval wait
- `orange`: actively being edited, restructured, or repaired
- `yellow`: paused, waiting, temporarily held
- `green`: checked, stable, operating normally
- `blue`: guide, manual, reference, index
- `gray`: neutral default
- `light gray`: archive, legacy, read-only history

Rules:

- the same status should use the same color
- when the status signal no longer matters, return to gray
- do not use color just for decoration

## Heading Rules

### Notion

In Notion, the page title already acts like `H1`.
Do not add a body `H1`.
Start body structure at `H2`.

Use this pattern:

1. intro callout
2. `H2` sections
3. `H3` and `H4` only when needed

The intro callout is the summary surface.
Do not add a separate `Summary` heading unless the page genuinely needs a full summary section.

### Obsidian

In Obsidian, filename and `H1` are separate.
Use one body `H1`, then `H2` through `H4`.

Rules:

- exactly one `H1`
- no `H5` or deeper
- do not skip heading levels unless the note is intentionally flat

## Link Rules

### Obsidian

- internal note links: `[[wikilink]]`
- custom display: `[[target note|display name]]`
- external links: standard Markdown links

### Notion

- internal page links: `@mention` or native internal link blocks
- external links: standard URL links

### Canonical Source Rule

When a local Markdown file is the source of truth:

- state that the local file is canonical
- link from Notion to the local source when possible
- keep raw logs and long reasoning in local Markdown, not in Notion dashboards

## Metadata And Top Block

The operating contract metadata remains canonical:

- `Zone`
- `Lead`
- `Owner`
- `Audience`
- `Agent Action`
- `Approval`
- `Source of Truth`
- `Review Cadence`

For human-first top sections, compress this into a visible working block:

- `Purpose`
- `Status`
- `Owner`
- `Next Step`
- `Last Updated`
- `Canonical Links`

This block is a reading aid, not a replacement for the full contract metadata.

## Tag Rules

Use minimal, controlled tags.
Treat tags as search helpers, not as the main taxonomy.

Recommended tag families:

- format: `#guide`, `#report`, `#template`, `#check`
- state: `#active`, `#blocked`, `#waiting`, `#archive`
- area: `#ops`, `#project`, `#reference`

Rules:

- keep most notes at one to three tags
- do not mirror every Notion property into a tag
- do not equate tags with Zone or approval level

## Emphasis And Emoji

Use only three emphasis modes in normal docs:

- `**bold**` for decisions and important labels
- `*italic*` for light nuance only
- ``code`` for page names, fields, paths, commands, and state values

Emoji rule:

- do not prefix page titles with emojis
- allow emoji only when it has a clear functional purpose
- never use emoji as a substitute for the icon status system
