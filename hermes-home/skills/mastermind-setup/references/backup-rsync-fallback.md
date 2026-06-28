# rsync Fallback — Python-Based Sync

**Creado:** 2026-06-26

## Problema

`rsync` NO está disponible en la MicroVM de NaN.builders. Si un procedimiento lo requiere, usar Python con `shutil.copy2()` como fallback.

## Procedimiento de Fallback

```python
import os, shutil, filecmp

def rsync_fallback(src, dst):
    """
    Simula rsync -av --delete con Python.
    src: directorio fuente (con / final)
    dst: directorio destino (con / final)
    """
    # 1. --delete: remover archivos en dst que no existen en src
    for root, dirs, files in os.walk(dst):
        for f in files:
            src_file = os.path.join(root, f).replace(dst, src, 1)
            if not os.path.exists(src_file):
                os.remove(os.path.join(root, f))
    
    # 2. Limpiar dirs vacíos
    for root, dirs, files in os.walk(dst, topdown=False):
        for d in dirs:
            try:
                if not os.listdir(os.path.join(root, d)):
                    os.rmdir(os.path.join(root, d))
            except OSError:
                pass
    
    # 3. Copiar/actualizar archivos
    copied = updated = skipped = 0
    for root, dirs, files in os.walk(src):
        for f in files:
            src_file = os.path.join(root, f)
            rel = os.path.relpath(src_file, src)
            dst_file = os.path.join(dst, rel)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            
            if not os.path.exists(dst_file):
                shutil.copy2(src_file, dst_file)
                copied += 1
            elif not filecmp.cmp(src_file, dst_file, shallow=False):
                shutil.copy2(src_file, dst_file)
                updated += 1
            else:
                skipped += 1
    
    return copied, updated, skipped
```

## Uso

```python
copied, updated, skipped = rsync_fallback(
    '/hermes-home/skills/',
    '/root/workspace/Mastermind/hermes-home/skills/'
)
print(f"Copiados: {copied}, Actualizados: {updated}, Sin cambios: {skipped}")
```

## Limitaciones

- No tiene paralelo de rsync (es secuencial)
- No soporta `--exclude` pattern matching como rsync
- Es suficiente para backups periódicos del sistema Mastermind
