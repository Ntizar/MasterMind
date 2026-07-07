# Sync: Skills alineados con Hermes (188)

## Problema
El repo Mastermind tenía desalineación con Hermes:
- **188 skills** en Hermes activo
- **198 skills** en repo (10 históricos/obsoletos de más)
- **238 SKILL.md** en `hermes-home/` (copia antigua con histórico)
- 1 skill nuevo (`gtfs-to-netex-conversion`) no respaldado
- Archivos de sistema (.curator_backups, .hub, etc.) contaminando el repo

## Solución aplicada

### 1. Limpieza del repo
- Eliminados 10 skills obsoletos que no existen en Hermes
- Eliminados 9 archivos de sistema (.curator_backups, .hub, INDEX.md, etc.)
- Añadido `gtfs-to-netex-conversion` (único skill de Hermes no respaldado)

### 2. Estado actual
- **Hermes activo**: 188 skills
- **Repo skills/**: 188 skills (idénticos a Hermes)
- **Repo hermes-home/**: 238 SKILL.md (histórico, se mantiene como backup antiguo)
- **Contenido idéntico**: ✅ True

### 3. Cron nocturno
- `skills-sync-to-github` actualizado: cada día a 05:00 UTC
- Script: `~/.hermes/scripts/sync-skills-to-mastermind.sh`
- Copia `/hermes-home/skills/` → `/root/workspace/Mastermind/skills/`
- Commit + push automático si hay cambios

## Archivos modificados
- `/root/workspace/Mastermind/skills/` — Limpieza completa
- `/hermes-home/scripts/sync-skills-to-mastermind.sh` — Script de sync
- `~/.hermes/scripts/sync-skills-to-mastermind.sh` — Script ejecutable por cron
- Cron job `55f6ed2e2da8` — Actualizado a 05:00 UTC diario

## Verificación
```bash
# Contar skills en cada lugar
find /hermes-home/skills -name "SKILL.md" | wc -l  # 188
find /root/workspace/Mastermind/skills -name "SKILL.md" | wc -l  # 188

# Verificar igualdad
diff <(cd /hermes-home/skills && find . -name "SKILL.md" | sort) \
     <(cd /root/workspace/Mastermind/skills && find . -name "SKILL.md" | sort)
# (sin salida = idénticos)
```

---
**Hecho con ❤️ por David Antizar** · 2026-07-07
