#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
DEST="$CODEX_HOME/skills"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)/skills"

mkdir -p "$DEST"

for dir in "$SRC_DIR"/*; do
  name="$(basename "$dir")"
  rm -rf "$DEST/$name"
  cp -R "$dir" "$DEST/$name"
  echo "✅ Installed skill: $name"
done

echo "\nSkills instaladas en: $DEST"
echo "Reinicia Codex para que cargue los nuevos skills."
