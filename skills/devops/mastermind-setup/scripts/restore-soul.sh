#!/bin/bash
# restore-soul.sh — Restore del SOUL.md desde el repo Mastermind
# Se ejecuta cuando SOUL.md está truncado o corrupto

set -e

REPO_DIR="/root/workspace/Mastermind"
HERMES_SOUL="/hermes-home/SOUL.md"

repo_size=$(wc -c < "$REPO_DIR/mastermind/SOUL.md")
local_size=$(wc -c < "$HERMES_SOUL" 2>/dev/null || echo 0)

if [ "$repo_size" -gt "$local_size" ]; then
    cp "$REPO_DIR/mastermind/SOUL.md" "$HERMES_SOUL"
    echo "✓ SOUL.md restaurado desde repo ($repo_size bytes)"
else
    echo "✓ SOUL.md ya está actualizado ($local_size bytes)"
fi
