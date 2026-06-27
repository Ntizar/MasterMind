# Cp Double Nesting Pitfall — Backup al Repo Mastermind

## El problema

Todos los comandos `cp` con directorios tienen el mismo problema cuando el destino ya existe:

```bash
# ⚠️ DOBLE NESTING — produce /dest/subdir/subdir/
cp -r /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/
cp -a /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/
cp -r /hermes-home/skills/* /root/workspace/Mastermind/hermes-home/skills/  # también si dir destino existe
```

**Resultado:** si `/root/workspace/Mastermind/hermes-home/skills/` ya existe,
`cp -a /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/`
produce `/root/workspace/Mastermind/hermes-home/skills/skills/` (doble nesting).

## Soluciones

### 1. Borrar destino antes de copiar (recomendado)
```bash
rm -rf /root/workspace/Mastermind/hermes-home/skills/
cp -a /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/
```

### 2. `cp -T` (no en todos los sistemas)
```bash
cp -rT /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/
```
**Nota:** `cp -T` puede no estar disponible en todas las implementaciones de coreutils.

### 3. Copiar contenido interno
```bash
cp -a /hermes-home/skills/. /root/workspace/Mastermind/hermes-home/skills/
```
El punto al final (`skills/.`) copia el **contenido** del directorio, no el directorio en sí.

### 4. Python fallback
```python
import shutil, os
src = '/hermes-home/skills/'
dst = '/root/workspace/Mastermind/hermes-home/skills/'
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(src, dst)
```

## Verificación post-copia

```bash
# Contar archivos en origen y destino (deben coincidir)
echo "Origen: $(find /hermes-home/skills -type f | wc -l)"
echo "Destino: $(find /root/workspace/Mastermind/hermes-home/skills -type f | wc -l)"

# Detectar doble nesting
find /root/workspace/Mastermind/hermes-home/skills -type d -name "skills" -not -path "*/hermes-home/skills" | head -5
```

## Historial de incidentes

| Fecha | Causa | Archivo(s) afectado(s) |
|-------|-------|----------------------|
| 2026-06-20 | `cp -r` doble nesting en todos los dirs | hermes-backup/* |
| 2026-06-27 | `cp -a` doble nesting en skills/ | hermes-home/skills/skills/ |

**Lección aprendida:** Ningún `cp` es seguro si el destino puede existir. Siempre `rm -rf` primero.
