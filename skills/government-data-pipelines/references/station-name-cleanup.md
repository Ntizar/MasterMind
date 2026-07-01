# Station Name Cleanup — Patrones de limpieza post-parseo

Cuando un parser de PDFs extrae texto libre, los campos de "estación" o "ubicación" a menudo contienen oraciones completas del PDF en vez de solo el nombre del lugar.

## Detección

```python
import re

def is_contaminated_station(station: str) -> bool:
    """Detecta nombres de estación que son frases del PDF."""
    if len(station) > 35:
        return True
    # Palabras que indican texto narrativo, no nombre de lugar
    narrative_words = [
        'condiciones', 'observa', 'maquinista', 'persona', 'situacion',
        'circulacion', 'consecuencia', 'velocidad', 'permitida', 'dispone',
        'fueron', 'resultan', 'trayecto', 'relevo', 'existen'
    ]
    return any(w in station.lower() for w in narrative_words)
```

## Patrones de limpieza (orden de prioridad)

### 1. Truncar en primer punto + mayúscula
```python
# "Tarancón. Los viajeros fueron transbordados en" → "Tarancón"
m = re.match(r'^(.+?)\.\s+[A-ZÁÉÍÓÚÑ]', station)
if m:
    station = m.group(1).strip()
```

### 2. Truncar en patrones narrativos conocidos
```python
SEPARATORS = [
    ' a la altura del', ' y el ', ' por el ', ' el jefe',
    ' ubicada en', ' situada en', ' se fusionó', ' en rampa',
    ' en condiciones', ' observa que', ' a las '
]
for sep in SEPARATORS:
    if sep in station:
        station = station.split(sep)[0].strip()
        break
```

### 3. Eliminar paréntesis descriptivos largos
```python
# "Zalla (Vizcaya) situada en el PK 2+057" → "Zalla"
m = re.match(r'^(.+?)\s+\((.+?)\)\s*$', station)
if m and len(m.group(2)) > 20:
    station = m.group(1).strip()
```

### 4. Fix manual para casos edge-case
```python
MANUAL_FIXES = {
    'A': 'León',  # Texto truncado por parser
    'Francia .............................. 27': 'Francia',
}
```

## Verificación post-limpieza

```python
# Revisar que no quedan estaciones contaminadas
for r in reports:
    station = r.get('ubicacion', {}).get('estacion', '')
    if is_contaminated_station(station):
        print(f"STILL DIRTY: {r['expediente']}: {station[:60]}")
```

## Limpieza de estaciones en visor existente (post-carga)

Cuando el visor ya tiene datos cargados, las estaciones pueden tener problemas diferentes al parser:

### Mayúsculas completas
```python
# "MADRID-CHAMARTÍN-CLARA CAMPOAMOR" → "Madrid-Chamartín-Clara Campoamor"
station = station.title()  # Python title case
# Fix: "de" y "del" deben quedar en minúscula
for prep in [' de ', ' del ', ' la ', ' el ', ' los ', ' las ']:
    station = station.replace(prep.upper(), prep)
```

### Provincias entre paréntesis
```python
# "Pradell de la Teca (Tarragona)" → "Pradell de la Teca"
# "Cerdido (A Coruña)" → "Cerdido"
m = re.match(r'^(.+?)\s*\([A-ZÁÉÍÓÚÑ][a-záéíóúñ ]+\)\s*$', station)
if m:
    station = m.group(1).strip()
```

### Patrones PK en el nombre
```python
# "P.K. 429,825 Estación X" → "Estación X"
station = re.sub(r'P\.?\s*K\.?\s*[\d,\.]+', '', station).strip()
# "415+648" al inicio
station = re.sub(r'^\d{1,4}\+\d{1,4}\s*', '', station).strip()
```

### Texto descriptivo residual
```python
# "Estación de San Feliz de las Minas. La estación se encuentra..."
station = re.split(r'\.\s+[A-Z]', station)[0]
# Truncar en comas si > 40 chars
if len(station) > 40:
    station = station.split(',')[0].strip()
```

### Puntuación trailing
```python
station = station.rstrip('.,;:')
```

## Prevención en el parser

La mejor limpieza es no contaminar en el primer lugar:
- Limitar la captura del regex de estación a 30-40 chars
- Usar `[^\.]+?` en vez de `.+` para capturar solo hasta el primer punto
- Para patrones como `"estación de X"`, capturar solo el nombre propio después de "de"

---

## ⚠️ LIMPIEZA DEMASIADO AGRESIVA (VERIFICADO 2026-06-29)

**Pitfall crítico:** Una limpieza que elimina paréntesis y sufijos puede destruir nombres de estación reales.

### Ejemplos de destrucción
| Original | Limpieza incorrecta | Resultado correcto |
|----------|-------------------|-------------------|
| "Vila-real (Castellón)" | elimina `(Castellón)` + trunca en `de` → "Vila" | "Vila-real" |
| "Sama de Langreo (Asturias)" | elimina `(Asturias)` + trunca → "La" | "Sama de Langreo" |
| "L'Hospitalet de Llobregat" | elimina "de Llobregat" → "L'Hospitalet de" | "L'Hospitalet de Llobregat" |
| "Sant Vicenç de Calders" | elimina "de Calders" → "Sant" | "Sant Vicenç de Calders" |

### Reglas de seguridad
1. **NUNCA truncar en "de" si el resultado queda < 6 chars** — "Vila" es sospechoso, "Vila-real" no
2. **Eliminar provincia entre paréntesis SOLO al final** — "Vila-real (Castellón)" → "Vila-real", NO "Vila"
3. **Preservar preposiciones** — "de", "del", "la", "el" son parte del nombre, no basura
4. **Si el nombre limpiado es genérico** ("La", "El", "Los", "San", "Sant"), extraer del resumen del informe en vez de limpiar

### Patrón correcto de limpieza
```python
def safe_clean_station(name):
    if not name or len(name) < 3:
        return name
    
    cleaned = name.strip()
    
    # 1. Eliminar SOLO provincia entre paréntesis al FINAL
    cleaned = re.sub(r'\s*\(([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)*)\)\s*$', '', cleaned)
    
    # 2. Eliminar PK suffix
    cleaned = re.sub(r'\s+[Pp][Kk]\s*\d+.*$', '', cleaned)
    
    # 3. Eliminar trailing junk
    cleaned = re.sub(r'\s+(?:desde|por|y éste|y con)\s*$', '', cleaned, flags=re.IGNORECASE)
    
    cleaned = cleaned.rstrip('.').strip()
    
    # 4. VERIFICAR: si quedó muy corto, es seguro que se destruyó algo
    if len(cleaned) < 4:
        return name  # Devolver original — necesita extracción del resumen
    
    return cleaned
```

### Detección de nombres destruidos
```python
GENERIC_NAMES = {'la', 'el', 'los', 'las', 'san', 'sant', 'de', 'del', 'que', 'pk', 'fran', 'río'}

def is_likely_destroyed(name):
    return name.lower().strip() in GENERIC_NAMES or len(name) <= 3
```
