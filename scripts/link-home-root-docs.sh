#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$HOME/developer/backups/manual-snapshots/home-root-docs"
TIMESTAMP="$(date '+%Y%m%d-%H%M%S')"

link_file() {
  local source_path="$1"
  local target_path="$2"
  local backup_path

  mkdir -p "$(dirname "$target_path")" "$BACKUP_DIR"

  if [ -L "$target_path" ] && [ "$(readlink "$target_path")" = "$source_path" ]; then
    echo "Already linked: $target_path"
    return
  fi

  if [ -e "$target_path" ] || [ -L "$target_path" ]; then
    backup_path="$BACKUP_DIR/$(basename "$target_path").$TIMESTAMP.bak"
    mv "$target_path" "$backup_path"
    echo "Backed up $target_path -> $backup_path"
  fi

  ln -s "$source_path" "$target_path"
  echo "Linked $target_path -> $source_path"
}

link_file "$REPO_ROOT/docs/home-root/AGENTS.md" "$HOME/AGENTS.md"
link_file "$REPO_ROOT/docs/home-root/CLAUDE.md" "$HOME/CLAUDE.md"
