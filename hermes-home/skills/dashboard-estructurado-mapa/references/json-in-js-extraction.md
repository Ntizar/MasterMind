# Extracción de JSON embebido en JavaScript y verificación de sincronización

## Contexto

Proyectos como CIAF-data incrustan un objeto JSON grande dentro de un archivo JS:
```js
const CIAF_DATA = {
  "version": "2.1",
  "stats": { ... },
  "reports": [ { ... }, ... ]
};
```

Además existe un archivo `data/reports.json` separado como fuente de verdad. Ambos deben estar sincronizados.

## Patrón 1: Extraer JSON embebido en JS

El JSON dentro de JS no es parseable directamente porque:
1. Está precedido por `const CIAF_DATA = `
2. Puede tener sintaxis JS no-JSON (comentarios, trailing commas, etc.)
3. El objeto puede estar truncado o tener errores de estructura

### Algoritmo de extracción

```python
import re, json

with open('app.js', 'r') as f:
    js_content = f.read()

# 1. Encontrar inicio del objeto
match = re.search(r'const\s+CIAF_DATA\s*=\s*\{', js_content)
if not match:
    raise ValueError("No se encontró CIAF_DATA")

start = match.end()

# 2. Matching de brace depth para encontrar el cierre
depth = 1
i = start
while i < len(js_content) and depth > 0:
    if js_content[i] == '{':
        depth += 1
    elif js_content[i] == '}':
        depth -= 1
    i += 1

# 3. Extraer y parsear
js_data_str = '{' + js_content[start:i-1] + '}'
data = json.loads(js_data_str)
```

**Pitfall — `];` duplicado:** El cierre del array de reports puede tener un `];` extra que rompe el brace matching. Verificar que la estructura es `]` + `}` (no `]` + `];` + `}`).

**Pitfall — `}` faltante:** Si falta el `}` de cierre del objeto, el brace matching llegará al final del archivo sin encontrarlo. Verificar que `depth == 0` al terminar el loop.

## Patrón 2: Verificar sincronización entre JSON y JS

```python
import json, re

# Cargar ambos archivos
with open('data/reports.json') as f:
    json_data = json.load(f)
json_reports = json_data['reports']

# Extraer de JS (ver Patrón 1)
js_reports = data_js['reports']

# 1. Conteo
assert len(json_reports) == len(js_reports), \
    f"Count mismatch: JSON={len(json_reports)} JS={len(js_reports)}"

# 2. IDs
json_ids = set(r['id'] for r in json_reports)
js_ids = set(r['id'] for r in js_reports)
assert json_ids == js_ids, f"ID mismatch: {json_ids ^ js_ids}"

# 3. Campos clave por reporte
json_by_id = {r['id']: r for r in json_reports}
js_by_id = {r['id']: r for r in js_reports}

for rid in json_by_id:
    j = json_by_id[rid]
    s = js_by_id[rid]
    for field in ['año', 'tipo', 'fecha', 'hora', 'estacion', 'lat', 'lng', 'gravedad']:
        assert j.get(field) == s.get(field), \
            f"{rid}.{field}: JSON={j.get(field)!r} JS={s.get(field)!r}"
```

## Pitfalls específicos de CIAF-data

1. **Versiones desalineadas:** `reports.json` puede tener version 2.1 mientras `app.js` tiene 2.0. Actualizar ambos.
2. **Stats keys diferentes:** JSON y JS pueden tener keys de stats con nombres distintos (ej: `con_coordenadas` vs `con_coords`) pero valores consistentes. Esto es normal si se refactorizó una parte pero no la otra.
3. **Cierre de objeto CIAF_DATA:** Tras el array de reports, la estructura debe ser `]` + `}` + `// === Estado ===`. Un `];` duplicado o `}` faltante rompen el parse.
4. **Linter de Node.js:** El linter de Node.js no entiende archivos JS que contienen JSON embebido (da error en la línea 2). Es un falso positivo — el archivo es válido JS, solo que el linter empieza a parsear desde la línea 2 donde ve `"version": "2.0"`.

## Archivos afectados

- `dashboard/data/reports.json` — Fuente de verdad, parseable como JSON válido
- `js/app.js` — Datos incrustados en variable `CIAF_DATA`
- `index.html` — Referencia a ambos (fetch JSON o usa CIAF_DATA)
