# Sync Bidireccional con Filtrado de System Files

**Fecha:** 2026-07-01
**Problema:** El cron `skills-sync-to-github` copia con `cp -r` simple, sin filtrar system files ni borrar archivos eliminados del source.

## Síntomas

- Repo tiene diffs en skills/notes/scripts pero `git status` muestra 0 cambios
- En realidad: archivos faltantes + extras fantasma en el repo
- Git log muestra divergencia: commits locales vs remotos divergentes

## Causa Raíz

1. **System files no filtrados:** `.hub/quarantine/`, `.curator_backups/`, etc. existen en source pero el cron los excluye → quedan "fantasmas" en el repo
2. **Archivos eliminados no se borran:** skills renombrados o eliminados de `/hermes-home/skills/` siguen en el repo
3. **Branch divergence:** `main` vs `master` — el tracking apuntaba a `origin/master`

## Solución: Python shutil con filtrado explícito

```python
import os, shutil

src_dir = '/hermes-home/skills'
dst_dir = '/root/workspace/Mastermind/skills'

SKIP_PATTERNS = [
    '.curator_backups/', '.hub/', '.bundled_manifest',
    '.curator_state', '.skill-learning-state.json',
    '.usage.json', 'INDEX.md', 'STEM-INDEX.md'
]

# 1. Source files (excluyendo system files)
src_files = set()
for root, _, files in os.walk(src_dir):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), src_dir)
        if not any(rel.startswith(p) for p in SKIP_PATTERNS):
            src_files.add(rel)

# 2. Repo files
dst_files = set()
for root, _, files in os.walk(dst_dir):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), dst_dir)
        dst_files.add(rel)

# 3. Copiar faltantes
for rel in src_files - dst_files:
    src_path = os.path.join(src_dir, rel)
    dst_path = os.path.join(dst_dir, rel)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.copy2(src_path, dst_path)

# 4. Borrar extras
for rel in dst_files - src_files:
    path = os.path.join(dst_dir, rel)
    if os.path.exists(path):
        os.remove(path)
```

## Verificación post-sync

```bash
# Debe devolver vacío (0 missing, 0 extra)
diff <(cd /hermes-home/skills && find . -type f | sort) \
     <(cd /root/workspace/Mastermind/skills && find . -type f | sort)
```

## Post-sync: Branch tracking

```bash
cd /root/workspace/Mastermind
git branch -u origin/main main  # Corregir tracking
git status  # Debe mostrar "up to date"
```

## Lecciones

- `cp -r` NO es suficiente para sync — no borra extras ni filtra system files
- `diff` de directorios da falsos positivos con system files
- Siempre verificar tracking de branch con `git branch -vv`
- El cron debería evolucionar a sync bidireccional con filtrado
