# Validación de inventario de APIs

## Problema

`estado.json` y `README.md` pueden quedar desfasados respecto al conteo real de directorios en `/tmp/inventario-apis/`.

## Causas

1. El script `procesar-apis.py` crea directorios pero no actualiza `estado.json` (bug o interrupción)
2. El README se genera en un momento diferente al procesamiento real
3. Múltiples ejecuciones del cron pueden dejar estados inconsistentes

## Patrón de validación

```python
from pathlib import Path

# Conteo real de directorios (fuente de verdad)
categorias_real = {}
for cat_dir in Path('/tmp/inventario-apis/').iterdir():
    if cat_dir.is_dir() and not cat_dir.name.startswith('.'):
        count = len([d for d in cat_dir.iterdir() if d.is_dir()])
        categorias_real[cat_dir.name] = count

total_real = sum(categorias_real.values())

# Comparar con estado.json
import json
with open('/tmp/inventario-apis/estado.json') as f:
    estado = json.load(f)
total_estado = estado['procesadas']

if total_real != total_estado:
    print(f"⚠️  Desfase detectado: {total_real} directorios vs {total_estado} en estado.json")
```

## APIs nuevas hoy

Para detectar qué APIs se crearon hoy:

```python
from datetime import date

today = date.today()
nuevas = []
for cat_dir in Path('/tmp/inventario-apis/').iterdir():
    if cat_dir.is_dir() and not cat_dir.name.startswith('.'):
        for d in cat_dir.iterdir():
            if d.is_dir():
                mtime = datetime.fromtimestamp(d.stat().st_mtime).date()
                if mtime == today:
                    nuevas.append((cat_dir.name, d.name))
```

## Fuentes de verdad (en orden)

1. **Directorios reales** (`ls -d */`) → conteo más fiable
2. **estado.json** → métricas del script, puede estar desfasado
3. **README.md** → resumen generado, puede tener días de retraso

## Validación dual-repo (junio 2026)

Siempre comparar ambos repos:

```python
import os, json

for base in ['/tmp/inventario-apis', '/opt/hermes-work/inventario-apis']:
    if not os.path.isdir(base):
        continue
    total_dirs = sum(len([d for d in os.listdir(os.path.join(base, c))
                          if os.path.isdir(os.path.join(base, c, d))])
                     for c in ['agentes-ia', 'automatizacion', 'ia'])
    with open(f'{base}/estado.json') as f:
        estado = json.load(f)
    print(f'{base}: {total_dirs} directorios, estado.json={estado["procesadas"]}')
```

Si la diferencia entre repos > 100 → hay divergencia que requiere investigación.
