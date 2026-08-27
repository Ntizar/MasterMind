# Post-extracción: Limpieza y geocodificación — CIAF 2026-06-29

## Problema detectado
269 registros CIAF tenían datos sucios del parsing original:
- 38 registros con coordenadas por defecto (43.336, -8.3953 = A Coruña)
- 26 registros con estación vacía o genérica ("La", "Pk", "")
- Nombres con provincias entre paréntesis: "Tolosa (Guipúzcoa)"
- Nombres truncados: "L'Hospitalet de", "San Vicente de la"
- Gravedad legacy: "fatal" en vez de "muy grave" (RD 929/2022)

## Solución aplicada

### 1. Fix manual para registros críticos
Los 26 registros con estación vacía se arreglaron extrayendo la ubicación del resumen del informe:

| Expediente | Estación original | Estación corregida | Fuente |
|------------|-------------------|-------------------|--------|
| 064/2007 | (vacío) | Oñoro | resumen "paso a nivel entre Oñoro y Fuentes de..." |
| 056/2010 | "La" | Sama de Langreo | resumen "paso a nivel de Sama de Langreo (Asturias)" |
| 060/2008 | "Pk" | La Hiniesta | resumen "en La Hiniesta (Zamora)" |
| 061/2008 | (vacío) | Córdoba Central | resumen "línea Madrid-Sevilla" + coords PK 11+100 |

### 2. Detección de coords por defecto
```python
# Contar frecuencia de coordenadas
from collections import Counter
coord_counts = Counter()
for r in records:
    lat, lng = r.get('lat'), r.get('lng')
    if lat and lng:
        # Redondear a 1 decimal para agrupar
        key = (round(lat, 1), round(lng, 1))
        coord_counts[key] += 1

# Coords con >5 registros = seguro defecto
suspicious = {k: v for k, v in coord_counts.items() if v > 5}
```

### 3. Extracción de estación desde resumen
Cuando el nombre de estación está vacío o es genérico, el resumen del informe contiene la ubicación real:

```python
import re

RESUMEN_PATTERNS = [
    # "estación de Madrid Chamartín"
    r'estaci[oó]n\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+(?:de|del|la|el|los|las|a|en|y)\s+[A-ZÁÉÍÓÚÑ]?[a-záéíóúñ]+)*(?:\s*\([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\))?)',
    # "apeadero de Cazoña"
    r'apeadero\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
    # "paso a nivel de Jaca"
    r'paso a nivel\s+(?:de\s+|entre\s+[^i]+y\s+)([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
    # "en Sama de Langreo, donde..."
    r'en\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+(?:de|del|la|el)\s+[A-ZÁÉÍÓÚÑ]?[a-záéíóúñ]+)*)\s*,',
]

def extract_station_from_resumen(resumen):
    for pat in RESUMEN_PATTERNS:
        m = re.search(pat, resumen, re.IGNORECASE)
        if m:
            station = m.group(1).strip()
            station = re.sub(r'\s*\([^)]*\)\s*$', '', station)  # quitar provincia
            if len(station) >= 4:
                return station
    return None
```

### 4. Limpieza de nombres existentes
```python
def clean_station_name(name):
    if not name or len(name) <= 2:
        return None
    
    cleaned = name.strip()
    
    # Eliminar provincia entre paréntesis
    cleaned = re.sub(r'\s*\([^)]*\)\s*$', '', cleaned)
    
    # Eliminar suffixes basura
    cleaned = re.sub(r'\s+(y suprimido|sobre las \d+|a las \d+:\d+|desde|en|por|y éste|y con)\s*$', '', cleaned, flags=re.IGNORECASE)
    
    # Eliminar "Pk NNN" suffix
    cleaned = re.sub(r'\s+[Pp][Kk]\s*\d+.*$', '', cleaned)
    
    # Eliminar trailing dots
    cleaned = cleaned.rstrip('.').strip()
    
    # Title Case si todo mayúsculas
    if cleaned.isupper() and len(cleaned) > 3:
        cleaned = cleaned.title()
        # Restaurar preposiciones minúsculas
        for prep in ['de', 'del', 'la', 'el', 'los', 'las', 'y', 'a']:
            cleaned = re.sub(rf'\b{prep.title()}\b', prep, cleaned)
    
    # Si quedó muy corto, descartar
    if len(cleaned) < 4:
        return None
    
    return cleaned
```

### 5. Fixes manuales conocidos
Algunos nombres se truncaron de forma predecible:
```python
KNOWN_FIXES = {
    'Atocha)': 'Madrid Puerta de Atocha',
    'Atocha-Cercanías': 'Madrid Atocha Cercanías',
    'Barcelona Estació de': 'Barcelona Estació de França',
    "L'Hospitalet de": "L'Hospitalet de Llobregat",
    'San Vicente de la': 'San Vicente de la Barquera',
    'Caparrates es el': 'Caparrates',
    'Santa María de la': 'Santa María de la Alameda',
    'Chapela y con': 'Chapela',
    'Ronda y éste': 'Ronda',
    'Villamanín por': 'Villamanín',
    'Francia (ancho': 'Irún',
    'Francia y': 'Irún',
    'Urda () y': 'Urda',
}
```

## Resultado final
- **269/269** registros con estación no vacía
- **269/269** registros con coordenadas reales (0 coords por defecto)
- **0** nombres en mayúsculas
- **0** provincias entre paréntesis
- **0** puntos trailing

## Archivos de soporte
- `station-coords.json` — DB de 328 estaciones con coordenadas
- `ltv_lookup.json` — Lookup de 5709 puntos LTV para geocodificación por PK
- `fix_visor_complete.py` — Script de limpieza batch completo
