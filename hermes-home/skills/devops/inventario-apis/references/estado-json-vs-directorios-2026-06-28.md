# Estado.json vs Directorios Reales — Diagnóstico 28/06/2026

## Problema

`estado.json` puede tener un conteo de `procesadas` MUY diferente al número real de directorios en disco. Esto NO es lo mismo que el dual-repo divergence — es un desfase DENTRO del mismo repo.

## Ejemplo del 28/06

**Repo `/tmp/inventario-apis/`:**
- `estado.json` dice: `procesadas: 1475`
- Directorios reales en disco: **4.364**
- Desfase: **+2.889 APIs** (196% más directorios que lo que dice estado.json)

**Distribución real por categoría (directorios):**
- `automatizacion`: 2.486 directorios
- `ia`: 1.044 directorios
- `agentes-ia`: 834 directorios
- resto: 0 directorios

**Distribución por categoría (estado.json):**
- `categorias: {}` — campo vacío (no hay desglose)

## Causa probable

El script `procesar-apis.py` crea directorios para cada API procesada y hace commit, pero **no siempre actualiza `estado.json`** con el nuevo conteo. Los commits dicen "Procesadas 5 APIs" pero el campo `api_procesadas` en estado.json puede no reflejar todas las APIs creadas.

## Diagnóstico

```python
import os, json

repo = '/tmp/inventario-apis'
with open(f'{repo}/estado.json') as f:
    estado = json.load(f)

# Contar directorios reales
total_dirs = 0
por_categoria = {}
for cat in os.listdir(repo):
    cat_path = os.path.join(repo, cat)
    if os.path.isdir(cat_path) and not cat.startswith('.') and cat != '.git':
        dirs = [d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))]
        por_categoria[cat] = len(dirs)
        total_dirs += len(dirs)

print(f"estado.json procesadas: {estado['procesadas']}")
print(f"Directorios reales: {total_dirs}")
print(f"Desfase: {total_dirs - estado['procesadas']}")
print(f"Por categoría: {por_categoria}")
```

## Fuentes de verdad (orden de fiabilidad)

1. **Directorios reales en disco** — siempre correcto, pero no tiene metadatos
2. **`estado.json`** — tiene metadatos pero puede estar desfasado
3. **`api_procesadas` en estado.json** — puede tener duplicados o APIs sin directorio
4. **README.md** — el más desactualizado, confiar solo como referencia visual

## Regla

**Siempre validar conteo de directorios reales como fuente de verdad complementaria.** No confiar ciegamente en `estado.json['procesadas']` sin verificar `find` o `os.listdir`.
