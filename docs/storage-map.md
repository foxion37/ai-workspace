# Storage Map

| Type | Primary Location | Backup / Mirror | Notes |
| --- | --- | --- | --- |
| Passwords, passkeys, account secrets | iCloud Keychain / Apple Passwords | macOS Keychain where needed | Do not store in GitHub |
| Working docs and notes | iCloud Drive | NAS backup | Keep active documents here |
| Incident reports and knowledge indexes | iCloud Drive | NAS backup, optional Notion mirror | Local Markdown first, Notion second |
| Reference images and PDFs | iCloud Drive | NAS backup | Use `reference/` naming in the repo mirror |
| Generated outputs | iCloud Drive | NAS backup | Commit only small, useful artifacts |
| Code and workflow rules | GitHub private repo | NAS backup | No secrets in repo |
| Raw operational logs and run reports | Existing source paths | NAS backup where already covered | Keep source systems in place and index them from incident reports |
| Large archive files | NAS | Optional iCloud copy only if needed | Prefer NAS for heavy binaries |
| Temporary scratch files | Local device only | None | Clean up regularly |

## Naming Rules

- Dates use `YYYY-MM-DD`.
- Versions use short tags like `v1`, `v2`, `final`.
- Result files should be named by purpose, not by vague labels.
- Temporary files should start with `tmp-`.
