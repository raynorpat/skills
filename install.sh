#!/usr/bin/env bash
# Install every skill in this repo (dirs containing SKILL.md) into a skills folder.
# Usage: ./install.sh [target-dir]   (default: ~/.claude/skills)
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)"
dest="${1:-$HOME/.claude/skills}"
mkdir -p "$dest"
for skill in "$src"/*/SKILL.md; do
  [ -e "$skill" ] || continue
  dir="$(dirname "$skill")"; name="$(basename "$dir")"
  mkdir -p "$dest/$name"
  cp -R "$dir/." "$dest/$name/"
  echo "installed $name -> $dest/$name"
done
