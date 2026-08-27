# LLM Text Recombination — Algoritmo de re-combinación de texto fragmentado

## Problema

Cuando un LLM extrae texto de PDFs y lo estructura en arrays JSON, puede fragmentar párrafos en líneas individuales de ~60 chars. Cada línea se convierte en un bullet/elemento de array separado, rompiendo la legibilidad.

**Patrón detectado:** 49.8% de los informes CIAF tenía exactamente 20 items en `conclusiones` (corte del pipeline LLM), cada uno era un fragmento de oración.

**Ejemplo del problema:**
```json
"conclusiones": [
  "No se han detectado comportamientos anómalos ni en la infraestructura, ni en las instalaciones, ni",
  "en las actuaciones del maquinista, por lo que del análisis realizado sobre este suceso se pueden",
  "extraer los siguientes resultados:",
  "1.- Las condiciones climáticas el día 11/09/2021 a las 22:15h, en el lugar del suceso eran de tormenta"
]
```

**Lo que debería ser:**
```json
"conclusiones": [
  "No se han detectado comportamientos anómalos ni en la infraestructura, ni en las instalaciones, ni en las actuaciones del maquinista, por lo que del análisis realizado sobre este suceso se pueden extraer los siguientes resultados.",
  "1.- Las condiciones climáticas el día 11/09/2021 a las 22:15h, en el lugar del suceso eran de tormenta con abundante aparato eléctrico y fuertes rachas de viento."
]
```

## Algoritmo de re-combinación

### Pasada 1: Unir líneas fragmentadas

**Lógica de continuidad:**
- Línea empieza con minúscula → continuación de la anterior (UNIR)
- Línea anterior termina sin puntuación de fin (., !, ?) → la siguiente es continuación (UNIR)
- Línea empieza con número (1.-, 2.-, etc.) → nuevo párrafo (SEPARAR)
- Línea anterior termina en punto + siguiente empieza con mayúscula → nuevo párrafo (SEPARAR)
- Línea vacía → separador de párrafo

```python
def recombine_fragmented_lines(lines):
    paragraphs, current = [], []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip metadata/headers
        if re.match(r'^(Informe Final|Comisión de|Subsecretaría|Ministerio|SECRETARÍA)', line, re.I):
            continue
        if line.upper() in ['RECOMENDACIONES', 'CONCLUSIONES', 'MEDIDAS ADOPTADAS']:
            continue
        
        starts_new = False
        if not current:
            starts_new = True
        elif re.match(r'^\d+[\.\-\)]\s', line):
            starts_new = True  # Numbered item starts new paragraph
        elif current[-1].endswith('.') and line[0].isupper():
            starts_new = True  # Sentence ended + new starts with capital
        elif line[0].islower():
            starts_new = False  # Continuation (lowercase start)
        elif not current[-1].endswith(('.', '!', '?', ':')):
            starts_new = False  # Previous didn't end sentence
        else:
            starts_new = True
        
        if starts_new and current:
            paragraphs.append(' '.join(current))
            current = [line]
        else:
            current.append(line)
    
    if current:
        paragraphs.append(' '.join(current))
    
    return [re.sub(r'\s+', ' ', p).strip() for p in paragraphs if len(p) > 10]
```

### Pasada 2: Limpiar headers embebidos

Muchos JSONs tienen headers de sección mezclados con el contenido:
- `5.1. RESUMEN DEL ANÁLISIS Y CONCLUSIONES RELACIONADAS CON EL SUCESO`
- `➢ Conclusiones:`
- `Investigación del accidente nº 0006/2010`

```python
def deep_clean_conclusiones(items):
    cleaned = []
    for item in items:
        # Remove section headers
        item = re.sub(r'^\d+\.\d+\.?\s+(RESUMEN|CONCLUSIONES|ANÁLISIS|DESCRIPCIÓN)[^\n]*', '', item, flags=re.I).strip()
        item = re.sub(r'^[➢•●]\s*Conclusiones:\s*', '', item, flags=re.I).strip()
        item = re.sub(r'^Investigación del (accidente|incidente)\s*\d*\.?\d*\.?\s*', '', item, flags=re.I).strip()
        item = re.sub(r'^\d+\.\d+\.\s*', '', item).strip()
        item = re.sub(r'Informe Final \d+/\d+', '', item).strip()
        
        if item and len(item) > 10:
            cleaned.append(item)
    return cleaned
```

### Pasada 3: Merge de fragmentos restantes

Algunos items quedan como oraciones incompletas después de las pasadas anteriores:

```python
def final_merge(cleaned):
    merged = []
    for item in cleaned:
        if not merged:
            merged.append(item)
            continue
        prev = merged[-1]
        # Merge if current starts lowercase and prev doesn't end sentence
        if item[0].islower() and not prev.endswith(('.', '!', '?')):
            merged[-1] = prev + ' ' + item
        else:
            merged.append(item)
    return merged
```

## Métricas de resultado (CIAF 269 informes)

| Métrica | Antes | Después |
|---------|-------|---------|
| Total items | 1,022 | ~600 |
| Promedio chars/item | ~60 | ~230 |
| Informes con 20 items exactos | 134 (49.8%) | 0 |
| Informes actualizados | — | 194/269 (72%) |

## Detección automática

Para detectar si un JSON tiene texto fragmentado:

```python
def is_fragmented(items):
    if not items: return False
    avg_len = sum(len(i) for i in items) / len(items)
    has_cap = len(items) == 20  # Pipeline cap
    short_items = sum(1 for i in items if len(i) < 80)
    return avg_len < 100 or has_cap or short_items > len(items) * 0.5
```

## Edge cases

1. **Items que son headers legítimos** (ej: "4.3. CONCLUSIONES") → la pasada 2 los elimina
2. **Items con tablas markdown** → detectar por `|` y `---`, eliminar filas de tabla
3. **Items bilingües** (inglés al final) → cortar antes de "SAFETY RECOMMENDATIONS"
4. **Items con números de recomendación** (ej: "11/2023-1") → preservar como items separados
5. **Items con PK/punto kilométrico** → preservar como items separados (son datos estructurados)
