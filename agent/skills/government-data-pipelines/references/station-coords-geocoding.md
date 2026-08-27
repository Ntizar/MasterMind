# Station Coords — Geocoding Local para Estaciones de Tren

## Concepto

Archivo `data/station-coords.json` con 328 estaciones españolas pre-geolocalizadas. Lookup instantáneo sin API.

## Formato del JSON

```json
{
  "Madrid Chamartín": {"lat": 40.4726, "lng": -3.6825},
  "Barcelona Sants": {"lat": 41.3726, "lng": 2.1411},
  "Cuenca-Fernando Zóbel": {"lat": 40.0583, "lng": -2.1283},
  ...
}
```

## Cobertura

- 328 estaciones (173 de informes + 155 adicionales)
- Cubre: todas las capitales de provincia + nudos ferroviarios principales
- Geolocaliza 71% de los 277 informes (196/277)

## Script generador

`/root/workspace/CIAF-visor/scripts/build-station-map.py` — genera el JSON desde:
1. Estaciones únicas extraídas de los informes
2. Capitales de provincia españolas
3. Coordenadas de Wikipedia/OSM

## Matching flexible

```python
import unicodedata, re

def normalize(s):
    s = s.upper().strip()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', s).strip()

def lookup(station, coords):
    norm = normalize(station)
    # 1. Exact match
    if station in coords: return coords[station]
    # 2. Normalized match
    for name, c in coords.items():
        if normalize(name) == norm: return c
    # 3. Partial match (first 2 significant words)
    words = [w for w in norm.split() if len(w) > 2][:2]
    key = ' '.join(words)
    for name, c in coords.items():
        if key in normalize(name): return c
    return None
```

## Estaciones más comunes en informes CIAF

| Estación | Informes | Coordenadas |
|----------|----------|-------------|
| Madrid Chamartín | 15+ | 40.4726, -3.6825 |
| Barcelona Sants | 10+ | 41.3726, 2.1411 |
| León Clasificación | 5+ | 42.5987, -5.5672 |
| Cuenca-Fernando Zóbel | 3 | 40.0583, -2.1283 |
| Salou | 3 | 41.0766, 1.1531 |

## Pitfalls

- Nombres con puntuación: "Cuenca-Fernando Zóbel" vs "Cuenca-Fernando" → matching parcial
- Nombres con "Clasificación": "León Clasificación" → buscar "León" como fallback
- Estaciones de apeadero: "Apeadero de Abaroa-San Miguel" → nombre largo, limitar a 50 chars
