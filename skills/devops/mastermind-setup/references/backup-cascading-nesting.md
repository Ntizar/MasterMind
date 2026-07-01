# Backup Cascading Nesting — Fix de Doble Anidamiento en 70+ Categorías

## El problema

Cuando `cp -a /hermes-home/skills/ /dest/skills/` se ejecuta sobre un destino que ya existe, produce nesting a DOS niveles:

1. **Nivel raíz:** `skills/skills/` (el directorio skills dentro de skills)
2. **Nivel categoría:** dentro de cada categoría, el mismo patrón se repite: `ai-patterns/ai-patterns/`, `creative/creative/`, `stem/stem/`, `mlops/mlops/`, etc.

**Resultado:** 70+ directorios anidados que git detecta como nuevos archivos.

## Diagnóstico

```bash
# Detectar nesting raíz
ls -d /dest/skills/skills/ 2>/dev/null && echo "ROOT NESTING FOUND"

# Detectar nesting en categorías (70+ casos)
find /dest/skills -mindepth 2 -maxdepth 2 -type d | while read dir; do
  parent=$(basename "$(dirname "$dir")")
  child=$(basename "$dir")
  if [ "$parent" = "$child" ]; then
    echo "NESTED: $dir"
  fi
done
```

## Solución en dos pasos

### Paso 1: Fijar nesting raíz

```bash
cd /dest/skills/
# Copiar contenido de skills/skills/ arriba
for item in skills/*; do
  name=$(basename "$item")
  if [ -d "skills/$name" ]; then
    cp -a "skills/$name" "$name"
  elif [ -f "skills/$name" ]; then
    cp -f "skills/$name" "$name"
  fi
done
# Copiar archivos ocultos
cp -a skills/.hub skills/.curator_backups skills/.bundled_manifest skills/.curator_state skills/.usage.json 2>/dev/null
# Borrar nesting raíz
rm -rf skills/
```

### Paso 2: Loop sistemático para TODAS las categorías

```bash
cd /dest/skills/
find . -mindepth 2 -maxdepth 2 -type d | while read dir; do
  parent=$(basename "$(dirname "$dir")")
  child=$(basename "$dir")
  if [ "$parent" = "$child" ]; then
    mv "$dir"/* "$dir"/.* . 2>/dev/null
    rm -rf "$dir"
    echo "Fixed: $parent/"
  fi
done
```

## Verificación post-fix

```bash
# Debe devolver vacío (0 líneas)
find /dest/skills -mindepth 2 -maxdepth 2 -type d | while read dir; do
  parent=$(basename "$(dirname "$dir")")
  child=$(basename "$dir")
  if [ "$parent" = "$child" ]; then
    echo "STILL NESTED: $dir"
  fi
done

# Contar archivos finales
find /dest/skills -type f | wc -l
```

## Historial

| Fecha | Causa | Detalle |
|-------|-------|---------|
| 2026-06-28 | `cp -a` sobre skills/ existente | 70+ categorías anidadas, 2097 archivos afectados |

## Prevención

**NUNCA** usar `cp -a /source/ /dest/` cuando `/dest/` puede existir. Siempre:
```bash
rm -rf /dest/
cp -a /source/ /dest/
```

O usar Python:
```python
import shutil
shutil.rmtree('/dest/', ignore_errors=True)
shutil.copytree('/source/', '/dest/')
```
