---
name: embedded-json-extraction
description: "Extraer y parsear JSON arrays/objects embebidos en archivos de código (JS, Python, etc.) cuando el bracket counting simple falla por corchetes dentro de strings."
version: 1.0.0
author: Mastermind
tags: [json, parsing, javascript, extraction, bracket-counting, demjson3]
---

# Embedded JSON Extraction — Parsear JSON desde Archivos de Código

Extraer y parsear JSON arrays/objects embebidos dentro de JavaScript, Python, u otros archivos de código donde el bracket counting simple falla.

## Por qué falla

JSON embebido en código parece válido pero rompe parsers estándar porque:
1. **Bracket counting falla** al encontrar `]` o `}` dentro de strings entrecomillados (ej: `"trenes": []`)
2. **Código trailing** después de `];` se incluye en la extracción
3. **Secuencias doble-escape** (`\\\\s`, `\\\\n`) en source confunden la inspección de strings
4. **Comillas smart** y chars UTF-8 (•, –, ") son JSON válido pero activan falsos alarms en regex

## Patrones

### Pattern 1: Bracket counter FUERA de strings

```python
def find_matching_bracket(raw, open_char, close_char):
    """Find position of matching close_char, ignoring inside quoted strings."""
    depth = 1
    in_string = False
    escape = False
    for i, c in enumerate(raw):
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == open_char:
            depth += 1
        elif c == close_char:
            depth -= 1
            if depth == 0:
                return i
    return -1
```

### Pattern 2: Parsear objetos individuales (cuando el array parsea mal pero los objetos son válidos)

```python
objects = []
depth_obj = 0
in_str = False
esc = False
obj_start = None

for i, c in enumerate(raw):
    if esc: continue
    if c == '\\': esc = True; continue
    if c == '"': in_str = not in_str; continue
    if in_str: continue
    if c == '{' and depth_obj == 0:
        obj_start = i
    if c == '{': depth_obj += 1
    elif c == '}' and depth_obj > 0:
        depth_obj -= 1
        if depth_obj == 0 and obj_start is not None:
            objects.append(raw[obj_start:i+1])
            obj_start = None
```

### Pattern 3: Regex boundary detection

Cuando el array va seguido de un patrón trailing único (ej: `];\n//`):

```python
import re
footer_pos = content.find('// === Estado ===')
pattern = re.search(r'\n\]\n\s*\]', content[footer_pos-500:footer_pos])
# El ] antes de \n  ]; es el cierre del array
```

### Pattern 4: demjson3 para parsing leniente

```python
import demjson3
data = demjson3.decode(raw.replace('None', 'null'))
# Maneja: newlines literales en strings, Python None, trailing commas
```

### Pattern 5: Wrap y validar

```python
# Después de extraer entre [ y ]
wrapped = '[' + array_raw + ']'
data = json.loads(wrapped)
```

## Workflow

1. **Localizar** el boundary del JSON — usar bracket counting O trailing pattern matching
2. **Extraer** contenido raw entre delimitadores (cuidado con lo que va después del `]` closing)
3. **Normalizar** — replace `None` → `null`, strip trailing non-JSON
4. **Probar** `json.loads()` primero → fallback a `demjson3` → fallback a individual-object parsing
5. **Validar** re-parseando y verificando campos/estructura esperados

## Pitfalls

- Un `]` dentro de un string (como `"trenes": []`) cerrará prematuramente un depth counter ingenuo
- El error "Extra data" de `json.loads()` significa que el JSON es válido pero hay contenido trailing
- Newlines double-escaped en strings (`\\\\n`) son JSON válido (backslash + letra n)
- Smart quotes en strings JSON están bien — son UTF-8 válido, no errores de parsing

## Related

- `references/ciaf-json-extraction.md` — Transcript completo de auditoría con edge cases
