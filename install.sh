#!/usr/bin/env bash
# Install every skill in this repo (dirs containing SKILL.md).
# Usage: ./install.sh [claude|codex|opencode|all|<dir>]...   (default: all)
#   claude   -> ~/.claude/skills
#   codex    -> ~/.agents/skills
#   opencode -> ~/.config/opencode/skills
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)"

install_to() {
  local dest="$1"
  mkdir -p "$dest"
  for skill in "$src"/*/SKILL.md; do
    [ -e "$skill" ] || continue
    local dir name; dir="$(dirname "$skill")"; name="$(basename "$dir")"
    mkdir -p "$dest/$name"
    cp -R "$dir/." "$dest/$name/"
    echo "installed $name -> $dest/$name"
  done
}

[ $# -eq 0 ] && set -- all
for t in "$@"; do
  case "$t" in
    all)      set -- claude codex opencode; break ;;
  esac
done
for t in "$@"; do
  case "$t" in
    claude)   install_to "$HOME/.claude/skills" ;;
    codex)    install_to "$HOME/.agents/skills" ;;
    opencode) install_to "$HOME/.config/opencode/skills" ;;
    *)        install_to "$t" ;;
  esac
done
