#!/bin/bash
# backup-hermes-memory.sh — Backup de memoria de Hermes al repo Mastermind
# Este script debe ser llamado por el agente DESPUÉS de guardar memoria,
# para hacer commit y push de los cambios en el repo.
#
# Uso: ./backup-hermes-memory.sh
# El agente debe haber guardado memoria en el repo ANTES de llamar esto.

set -e

REPO_DIR="/root/workspace/Mastermind"

cd "$REPO_DIR"

# 1. Actualizar SOUL.md del repo desde el local (si el local es más grande y válido)
SOUL_LOCAL="/hermes-home/SOUL.md"
SOUL_REPO="$REPO_DIR/mastermind/SOUL.md"
if [ -f "$SOUL_LOCAL" ] && [ -f "$SOUL_REPO" ]; then
    local_size=$(wc -c < "$SOUL_LOCAL")
    repo_size=$(wc -c < "$SOUL_REPO")
    if [ "$local_size" -gt "$repo_size" ] && [ "$local_size" -gt 1000 ]; then
        cp "$SOUL_LOCAL" "$SOUL_REPO"
        echo "✓ SOUL.md actualizado en repo ($local_size bytes)"
    fi
fi

# 2. Copiar skills locales al repo (los que no existen en repo)
HERMES_SKILLS="/hermes-home/skills/mastermind"
REPO_SKILLS="$REPO_DIR/mastermind"
mkdir -p "$REPO_SKILLS"
for f in "$HERMES_SKILLS/"*.md; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    if [ ! -f "$REPO_SKILLS/$fname" ]; then
        cp "$f" "$REPO_SKILLS/$fname"
        echo "✓ Nuevo skill en repo: $fname"
    fi
done

# 3. Commit y push
git add -A
if git diff --cached --quiet; then
    echo "✓ Sin cambios para backup"
else
    git commit -m "auto: backup $(date +%Y-%m-%d\ %H:%M)" 2>/dev/null || true
    git push origin main 2>/dev/null && echo "✓ Backup push: $(date +%Y-%m-%d\ %H:%M)" || echo "⚠ Push fallido (sin conexión o sin permisos)"
fi
