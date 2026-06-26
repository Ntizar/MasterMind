---
name: time-isochrones-precalculated
description: "Pre-cálculo de isócronas reales con OSMnx + NetworkX para el proyecto Time. Genera GeoJSON basado en red viaria OSM real. Patrón para calcular isócronas sin API externa."
version: "1.0.0"
author: David Antizar
tags: [isochrones, osmnx, networkx, openstreetmap, python, offline, time]
---

# Isochoronas Pre-calculadas — Time

## Cuándo usar esta skill

Cuando necesites:
- Calcular isócronas reales sin depender de APIs externas
- Añadir nuevas ciudades al proyecto Time
- Mejorar la precisión de las isócronas existentes
- Entender cómo funciona el cálculo offline

## Arquitectura

```
Python (OSMnx + NetworkX) → JSON GeoJSON → Server Node.js → Frontend Leaflet
     ↓                          ↓                ↓                ↓
Descarga grafo OSM     Guarda isócronas    Sirve /isochrones/   Renderiza polígonos
```

## Scripts

### `scripts/precalcular-isocronas.py` (principal)

Genera isócronas para TODAS las ciudades configuradas.

```bash
# Instalar dependencias
pip3 install osmnx networkx numpy shapely

# Calcular todas las ciudades
python3 scripts/precalcular-isocronas.py

# Calcular una ciudad específica
python3 scripts/precalcular-isocronas.py --ciudad bilbao

# Listar ciudades disponibles
python3 scripts/precalcular-isocronas.py --listar
```

### `scripts/calcular-isocronas.py` (helper)

Calcula una isócrona individual para debugging.

```bash
# Calcular isócona de coche 30min en Bilbao
python3 scripts/calcular-isocronas.py --ciudad bilbao --modo car --tiempo 30
```

## Ciudades configuradas

| Ciudad | Query OSM | Centro | Radio |
|--------|-----------|--------|-------|
| bilbao | Bilbao, Bizkaia, España | 43.263, -2.935 | 15km |
| malaga | Málaga, Andalucía, España | 36.721, -4.421 | 15km |
| sevilla | Sevilla, Andalucía, España | 37.389, -5.984 | 15km |
| valencia | Valencia, España | 39.470, -0.376 | 15km |
| zaragoza | Zaragoza, Aragón, España | 41.649, -0.889 | 15km |

## Formato de salida

### JSON combinado (`data/isochrones/{ciudad}.json`)

```json
{
  "ciudad": "bilbao",
  "centro": [43.263, -2.935],
  "generado": "2026-06-25T18:00:00Z",
  "isochrones": {
    "car": {
      "15": { "geojson": {...}, "area_km2": 12.5, "radio_m": 6000 },
      "30": { "geojson": {...}, "area_km2": 45.2, "radio_m": 12000 },
      "60": { "geojson": {...}, "area_km2": 156.8, "radio_m": 24000 }
    },
    "bike": { ... },
    "foot": { ... }
  }
}
```

### JSON individual (`data/isochrones/{ciudad}_{modo}_{tiempo}.json`)

```json
{
  "ciudad": "bilbao",
  "modo": "car",
  "tiempo_min": 30,
  "area_km2": 45.2,
  "radio_m": 12000,
  "geojson": {
    "type": "FeatureCollection",
    "features": [{
      "type": "Feature",
      "geometry": { "type": "Polygon", "coordinates": [...] },
      "properties": { "modo": "car", "minutos": 30, "area_km2": 45.2 }
    }]
  }
}
```

## Endpoints del servidor

| Endpoint | Descripción |
|----------|-------------|
| `GET /isochrones/list` | Lista ciudades disponibles con metadata |
| `GET /isochrones/{ciudad}` | Todas las isócronas de una ciudad |
| `GET /isochrones/{ciudad}/{modo}/{min}` | Isócrona específica |

## Algoritmo OSMnx + NetworkX

```python
import osmnx as ox
import networkx as nx

# 1. Descargar grafo de calles
G = ox.graph_from_place("Bilbao, España", network_type='drive')

# 2. Encontrar nodo más cercano al punto
center = ox.geocode("Plaza Mayor, Bilbao")
origin_node = ox.distance.nearest_nodes(G, center[1], center[0])

# 3. Calcular distancias desde el origen (Dijkstra)
lengths = nx.single_source_dijkstra_path_length(G, origin_node, cutoff=1800)  # 30 min

# 4. Filtrar nodos alcanzables
reachable_nodes = [n for n, l in lengths.items() if l <= 1800]

# 5. Generar polígono convexo hull
from shapely.geometry import MultiPoint
points = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in reachable_nodes]
polygon = MultiPoint(points).convex_hull

# 6. Convertir a GeoJSON
from shapely.geometry import mapping
geojson = mapping(polygon)
```

## Velocidades por modo y tipo de vía

| Modo | Velocidad base | Calles principales | Secundarias | Carriles bici |
|------|---------------|-------------------|-------------|---------------|
| car | 50 km/h | Autovías | Urbanas | N/A |
| bike | 15 km/h | Carriles bici | Calles tranquilas | Prioridad |
| foot | 5 km/h | Aceras | Calles peatonales | N/A |

## Pitfalls

1. **OSMnx descarga datos grandes** — El grafo de una ciudad puede ocupar 50-200MB en cache. Usar `cache/` directory.
2. **Tiempo de cálculo** — 1-5 minutos por ciudad dependiendo del tamaño. Ejecutar como batch job.
3. **network_type** — `'drive'` para coche, `'bike'` para bici, `'walk'` para peatón, `'all'` para todos.
4. **cutoff en segundos** — Dijkstra usa segundos, no minutos. 15min = 900s, 30min = 1800s, 60min = 3600s.
5. **convex hull** — El polígono resultante es convex hull, no sigue la costa. Para ciudades costeras, recortar con shoreline.
6. **RAM** — OSMnx puede consumir 1-2GB RAM para ciudades grandes. Ejecutar en máquina con suficiente memoria.
7. **Primera ejecución** — Descarga datos de Overpass API. Necesita internet solo la primera vez.
8. **Actualizaciones** — Los datos OSM cambian. Recalcular periódicamente (mensual recomendado).

## Futuras mejoras

1. **Shoreline clipping** — Recortar isócronas costeras con Natural Earth data
2. **Valhalla local** — Para isócronas con elevación real (desnivel)
3. **OTP integration** — Isochrone de transporte público con transbordos reales
4. **Cron de actualización** — Recalcular isócronas mensualmente vía cron job
5. **More cities** — Añadir Madrid, Barcelona, etc.
