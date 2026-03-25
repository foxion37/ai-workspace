# Runbook

This is the operating sequence for the workspace.

## Daily Flow

1. Work on the Mac mini when the workspace needs a stable source.
2. Keep active files in iCloud Drive.
3. Store credentials in iCloud Keychain or Apple Passwords.
4. Commit code and folder structure only to the GitHub private repo.
5. Push backup copies to NAS on a schedule.

## Workspace Path Rule

- On this Mac, `/Users/seongqkim/AI-Workspace` should resolve to the iCloud-backed workspace.
- The path should stay stable even if the actual storage lives under the iCloud Drive directory.

## File Flow

- Drafts, notes, reference images, and outputs go to iCloud first.
- Code, prompts, templates, and secret-free rules go to GitHub.
- Backups, archives, and recovery copies go to NAS.
- Temporary files stay local and are cleaned up regularly.

## Exceptions

- Never put secrets in GitHub.
- Never use NAS as the active working copy.
- Never let temporary files become the canonical source.
