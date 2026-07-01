#!/bin/bash
# backup-hermes-memory.sh — Backup de memoria de Hermes al repo Mastermind
# Este script copia el estado actual de la memoria de Hermes al repo
# Se ejecuta como cron job diario o manualmente

set -e

REPO_DIR="/root/workspace/Mastermind"
MEMORY_DIR="$REPO_DIR/memory"

# 1. Asegurar directorio
mkdir -p "$MEMORY_DIR"

# 2. Backup de SOUL.md (si existe y es más grande que el local)
SOUL_LOCAL="/hermes-home/SOUL.md"
SOUL_REPO="$REPO_DIR/mastermind/SOUL.md"
if [ -f "$SOUL_LOCAL" ] && [ -f "$SOUL_REPO" ]; then
    local_size=$(wc -c < "$SOUL_LOCAL")
    repo_size=$(wc -c < "$SOUL_REPO")
    if [ "$local_size" -gt "$repo_size" ]; then
        cp "$SOUL_LOCAL" "$SOUL_REPO"
        echo "✓ SOUL.md actualizado en repo ($local_size bytes)"
    fi
fi

# 3. Backup de memoria y usuario
# La memoria de Hermes se gestiona internamente, pero podemos guardar un snapshot
# de las notas más recientes del repo como referencia

# 4. Commit si hay cambios
cd "$REPO_DIR"
git add -A
if git diff --cached --quiet; then
    echo "✓ Sin cambios para backup"
else
    git commit -m "auto: backup $(date +%Y-%m-%d)" 2>/dev/null || true
    echo "✓ Backup commit: $(date +%Y-%m-%d)"
    # No hacemos push automático para evitar conflictos
    git push origin main 2>/dev/null || echo "⚠ Push fallido"
fi
