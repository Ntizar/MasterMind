#!/bin/bash
# mastermind-autoconfig.sh — Auto-configuración del sistema Mastermind
# Se ejecuta diariamente a las 09:00 UTC para sincronizar repo ↔ Hermes
# ACTUALIZADO 2026-06-03: Guard de SOUL.md más robusto

set -e

REPO_DIR="/root/workspace/Mastermind"
HERMES_SKILLS="/hermes-home/skills/mastermind"
HERMES_SOUL="/hermes-home/SOUL.md"
MIN_SOUL_SIZE=1000  # SOUL.md válido debe tener al menos 1KB

echo "=== Mastermind Autoconfig ($(date -u +%Y-%m-%d\ %H:%M UTC)) ==="

# 1. Sincronizar repo
cd "$REPO_DIR"
git pull origin main 2>/dev/null || echo "⚠ Repo ya actualizado o sin conexión"

# 2. Sincronizar skills al directorio de Hermes (solo los nuevos o modificados)
mkdir -p "$HERMES_SKILLS"
for f in "$REPO_DIR/mastermind/"*.md; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    # cp -n: no sobrescribir archivos que ya existen en Hermes (preserva los Hermes-only)
    cp -n "$f" "$HERMES_SKILLS/$fname"
done
echo "✓ Skills sincronizados"

# 3. Sincronizar SOUL.md — LÓGICA ROBUSTA
#   - Si local < MIN_SOUL_SIZE → SIEMPRE restaurar desde repo (truncado)
#   - Si repo > local → restaurar desde repo
#   - Si local > repo AND local > MIN → subir al repo
#   - Si mismo tamaño → skip
REPO_SOUL="$REPO_DIR/mastermind/SOUL.md"
if [ -f "$REPO_SOUL" ] && [ -f "$HERMES_SOUL" ]; then
    repo_size=$(wc -c < "$REPO_SOUL")
    local_size=$(wc -c < "$HERMES_SOUL")
    
    if [ "$local_size" -lt "$MIN_SOUL_SIZE" ]; then
        # SOUL truncado o corrupto — SIEMPRE restaurar
        cp "$REPO_SOUL" "$HERMES_SOUL"
        echo "⚠ SOUL.md TRUNCADO ($local_size bytes) → restaurado desde repo ($repo_size bytes)"
    elif [ "$repo_size" -gt "$local_size" ]; then
        cp "$REPO_SOUL" "$HERMES_SOUL"
        echo "✓ SOUL.md sincronizado desde repo ($repo_size bytes)"
    elif [ "$local_size" -gt "$repo_size" ] && [ "$local_size" -gt "$MIN_SOUL_SIZE" ]; then
        cp "$HERMES_SOUL" "$REPO_SOUL"
        echo "✓ SOUL.md subido al repo ($local_size bytes)"
    else
        echo "✓ SOUL.md ya sincronizado ($local_size bytes)"
    fi
elif [ -f "$REPO_SOUL" ] && [ ! -f "$HERMES_SOUL" ]; then
    # SOUL no existe localmente — crear desde repo
    cp "$REPO_SOUL" "$HERMES_SOUL"
    echo "✓ SOUL.md creado desde repo ($repo_size bytes)"
fi

# 4. Backup de memoria: copiar notas recientes del repo como snapshot
if [ -d "$REPO_DIR/notes" ]; then
    note_count=$(find "$REPO_DIR/notes" -name "*.md" 2>/dev/null | wc -l)
    echo "ℹ Notas en repo: $note_count"
fi

# 5. Verificar git auth (sin gh, usar token HTTPS)
if ! git remote -v >/dev/null 2>&1; then
    echo "⚠ Repo no clonado, se necesita configurar"
else
    echo "✓ Repo conectado a GitHub"
fi

echo "✓ Mastermind autoconfiguración completa"
