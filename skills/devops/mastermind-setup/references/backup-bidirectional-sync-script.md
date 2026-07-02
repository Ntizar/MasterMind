# Python Sync Script — Bidireccional con filtrado

## Cuándo usar
- Cuando el cron de backup produce divergencias (archivos faltantes + extras fantasma)
- Cuando el repo tiene archivos de `.hub/quarantine/` o `.curator_backups/` que no deberían estar
- Cuando skills han sido renombrados/eliminados en source pero persisten en repo
- Como verificación post-sync para confirmar 0 missing + 0 extra

## Script completo

```python
import os, shutil

src_dir = '/hermes-home/skills'
dst_dir = '/root/workspace/Mastermind/skills'

# System files que NO deben ir al repo
SKIP_PATTERNS = [
    '.curator_backups/',
    '.hub/',
    '.bundled_manifest',
    '.curator_state',
    '.skill-learning-state.json',
    '.usage.json',
    'INDEX.md',
    'STEM-INDEX.md',
]

# 1. Obtener lista de source files EXCLUYENDO system files
src_files = set()
for root, _, files in os.walk(src_dir):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), src_dir)
        if any(rel.startswith(p) for p in SKIP_PATTERNS):
            continue
        src_files.add(rel)

# 2. Obtener lista de repo files
dst_files = set()
for root, _, files in os.walk(dst_dir):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), dst_dir)
        dst_files.add(rel)

# 3. Borrar extras en repo (existen en repo pero no en source)
to_delete = dst_files - src_files
deleted = 0
for rel in to_delete:
    path = os.path.join(dst_dir, rel)
    if os.path.exists(path):
        os.remove(path)
        deleted += 1

# 4. Copiar faltantes (existen en source pero no en repo)
copied = 0
for root, _, files in os.walk(src_dir):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), src_dir)
        if any(rel.startswith(p) for p in SKIP_PATTERNS):
            continue
        src_path = os.path.join(root, f)
        dst_path = os.path.join(dst_dir, rel)
        if not os.path.exists(dst_path):
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            copied += 1

# 5. Reporte
print(f"SYNC: copied={copied}, deleted={deleted}")

# 6. Verificación final
dst_after = set()
for root, _, files in os.walk(dst_dir):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), dst_dir)
        dst_after.add(rel)

extra = dst_after - src_files
missing = src_files - dst_after
print(f"VERIFY: extra={len(extra)}, missing={len(missing)}")

if len(extra) == 0 and len(missing) == 0:
    print("✅ SYNC PERFECTO")
else:
    print("⚠️ QUEDAN DIFERENCIAS:")
    for e in sorted(extra)[:5]:
        print(f"  extra: {e}")
    for m in sorted(missing)[:5]:
        print(f"  missing: {m}")
```

## Notas
- Usar `shutil.copy2()` para preservar timestamps y metadata
- El script es **determinístico** — ejecutar dos veces produce el mismo resultado
- Compatible con Python 3.6+
- No requiere dependencias externas
