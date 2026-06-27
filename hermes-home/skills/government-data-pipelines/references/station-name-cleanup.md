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

## Prevención en el parser

La mejor limpieza es no contaminar en el primer lugar:
- Limitar la captura del regex de estación a 30-40 chars
- Usar `[^\.]+?` en vez de `.+` para capturar solo hasta el primer punto
- Para patrones como `"estación de X"`, capturar solo el nombre propio después de "de"
