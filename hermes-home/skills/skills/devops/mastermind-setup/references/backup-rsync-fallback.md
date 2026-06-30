# rsync Fallback — Copia sin rsync

**Creado:** 2026-06-26  
**Actualizado:** 2026-06-29

## Problema

`rsync` NO está disponible en la MicroVM de NaN.builders. Si un procedimiento lo requiere, usar alternativas.

## Solución Confirmada (2026-06-29)

**`rm -rf` + `cp -a`** — el patrón que funciona de verdad:

```bash
# Borrar destino ANTES de copiar (evita nesting)
rm -rf /root/workspace/Mastermind/hermes-home/skills/
cp -a /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/
```

**Por qué funciona:** `rm -rf` elimina el destino existente, luego `cp -a` copia todo desde cero sin nesting. `cp -a` preserva permisos, timestamps y enlaces simbólicos.

**Qué copiar:**
```bash
# skills
rm -rf /root/workspace/Mastermind/hermes-home/skills/
cp -a /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/

# memories
rm -rf /root/workspace/Mastermind/hermes-home/memories/
cp -a /hermes-home/memories/ /root/workspace/Mastermind/hermes-home/memories/

# notes
rm -rf /root/workspace/Mastermind/hermes-home/notes/
cp -a /hermes-home/notes/ /root/workspace/Mastermind/hermes-home/notes/

# scripts
rm -rf /root/workspace/Mastermind/hermes-home/scripts/
cp -a /hermes-home/scripts/ /root/workspace/Mastermind/hermes-home/scripts/

# archivos individuales
cp /hermes-home/config.yaml /root/workspace/Mastermind/hermes-home/config.yaml
```

> **Nota:** `INDEX.md` y `STEM-INDEX.md` pueden no existir en `/hermes-home/` — omitirlos sin error (son generados).

## Procedimiento de Fallback Python (alternativa)

```python
import os, shutil, filecmp

def rsync_fallback(src, dst):
    """
    Simula rsync -av con Python.
    src: directorio fuente (con / final)
    dst: directorio destino (con / final)
    """
    # 1. Limpiar destino
    if os.path.exists(dst):
        shutil.rmtree(dst)
    
    # 2. Copiar todo
    shutil.copytree(src, dst)
    
    # 3. Contar
    copied = sum(len(files) for _, _, files in os.walk(dst))
    return copied
```

## Uso

```python
copied = rsync_fallback(
    '/hermes-home/skills/',
    '/root/workspace/Mastermind/hermes-home/skills/'
)
print(f"Archivos copiados: {copied}")
```

## Limitaciones

- No tiene paralelo de rsync (es secuencial)
- No soporta `--exclude` pattern matching como rsync
- Es suficiente para backups periódicos del sistema Mastermind
- `rm -rf` + `cp -a` en bash es más rápido que Python para directorios grandes
