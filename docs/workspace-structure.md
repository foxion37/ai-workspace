# Workspace Structure

## Roles

```text
iCloud       -> active documents, images, notes, outputs
iCloud Keychain -> passwords, passkeys, account secrets
GitHub       -> code, prompts, templates, structure rules
Mac mini     -> reference machine and source of workspace rules
NAS          -> backups, archives, recovery copies
```

## Local Path Mapping

```text
This Mac:
  /Users/seongqkim/AI-Workspace -> iCloud-backed workspace path

Mac mini:
  /Users/barq/AI-Workspace -> same logical workspace root
```

## Folder Tree

```text
iCloud/
  AI-Workspace/
    docs/
    reference/
    knowledge-db/
    figma/
    outputs/
    archive/
    temp/

GitHub private repo/
  docs/
  public/
  scripts/
  rules/

NAS/
  AI-Workspace-backup/
    snapshots/
    archive/
    releases/
```

## Naming Reference

- See `docs/naming-convention.md` for folder and file naming rules.

## Naming Rules

- Use `YYYY-MM-DD` for dates.
- Use short version tags such as `v1`, `v2`, or `final`.
- Use clear names for results, for example `topic-type-date`.
- Use `tmp-` only for disposable files.
