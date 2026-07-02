# Fix: skills-sync-to-github cron divergencia

## Problema
El cron `skills-sync-to-github` (job_id: 55f6ed2e2da8) tenía **dos fallos críticos**:

1. **Ruta incorrecta en rsync**: el prompt decía `rsync -av --delete /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/` — el repo está en `/root/workspace/Mastermind/skills/`, NO en `/root/workspace/Mastermind/hermes-home/skills/`. Esto causaba que los archivos se copiaran en la ruta equivocada.

2. **Branch tracking divergente**: el repo local tenía `main` pero el tracking apuntaba a `origin/master`. El push iba a `main` pero el cron esperaba `master`, causando divergencia de 62 commits locales vs 63 remotos.

## Solución aplicada

### 1. Rebase y sincronización manual
- `git fetch origin` → `git rebase origin/master` → `git push origin main:master`
- Rebase de 62 commits locales sobre el remoto (19 commits skipped, 1 aplicado)
- Actualizado tracking: `git branch -u origin/main main`

### 2. Sync completo de archivos
- 250 archivos copiados (skills nuevos)
- 165 archivos eliminados (skills eliminados de source pero no del repo)
- 2 notes copiadas, 1 extra eliminada
- 3 scripts copiados
- 16 system files excluidos correctamente (`.curator_backups/`, `.hub/`, etc.)

### 3. Prompt del cron actualizado
El nuevo prompt:
- Usa **Python script** para sync bidireccional (copiar missing + borrar extra)
- Excluye system files correctamente (`.curator_backups/`, `.hub/`, etc.)
- **NO usa rsync** (que causaba rutas duplicadas)
- Sync notes y scripts con `cp -n` + limpieza de extras
- Commit + push automático si hay cambios
- Reporte de estado final con conteos

### 4. Estado actual
- Skills: 1175/1175 ✅
- Notes: 37/37 ✅
- Scripts: 170/170 ✅
- Git: working tree limpio, branch up-to-date con origin/main

## Archivos modificados
- `/persist/hermes-home/cron/jobs.json` — prompt del job 55f6ed2e2da8 actualizado
- `/root/workspace/Mastermind/` — sync completo (368 archivos cambiados)
