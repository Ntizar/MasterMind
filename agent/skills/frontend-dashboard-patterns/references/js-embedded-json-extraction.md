# Extracción de JSON Embebido en JS (Template Literal Safety)

## Problema

Los archivos JS con datos incrustados (ej. `CIAF_DATA = { ... }`) contienen
template literals `${...}` dentro de las cadenas que rompen `json.loads()` cuando
se intenta parsear la sección.

## Técnica: Bracket Counting (no Regex)

**NUNCA uses regex simple** (`.*?`) para extraer objetos/arrays JSON de JS —
se corta en el primer `}` de cierre interno, como pasó con `por_anio`.

```python
import re

with open('app.js', 'r') as f:
    js_content = f.read()

# 1. Encontrar la posición del array
m = re.search(r'"reports":\s*\n\s*\[', js_content)
arr_start = m.end() - 1  # posición del [

# 2. Contar corchetes para encontrar el ] de cierre
depth = 1
i = arr_start + 1
while i < len(js_content) and depth > 0:
    ch = js_content[i]
    if ch == '[': depth += 1
    elif ch == ']': depth -= 1
    elif ch == '"':
        i += 1
        while i < len(jsencent) and js_content[i] != '"':
            if js_content[i] == '\\': i += 1
            i += 1
    i += 1

reports_str = js_content[arr_start:i]

# 3. Limpiar trailing commas (JS permite, JSON no)
for _ in range(5):
    reports_str = re.sub(r',\s*}', '}', reports_str)
    reports_str = re.sub(r',\s*\]', ']', reports_str)
    if '},' not in reports_str and '],' not in reports_str:
        break

reports_js = json.loads(reports_str)
```
