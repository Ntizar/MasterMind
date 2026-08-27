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

## Alternativa: CSR binario para Web Workers (ISOTime)

En vez de generar GeoJSON estático, se puede serializar el grafo OSM a **binario CSR (Compressed Sparse Row)** y cargarlo en un Web Worker para correr Dijkstra en el navegador. Esto permite isocronas en tiempo real 100% client-side, sin API ni servidor.

**Implementado en ISOTime** (`github.com/Ntizar/ISOTime`):
- Python (OSMnx) → binario CSR (1-2MB por ciudad) → fetch estático → Web Worker → Dijkstra + binary heap → polígono
- 40K nodos se calculan en <1s en el navegador
- Formato: header (32B) + city name (32B) + node coords (f32) + CSR offsets (u32) + edge targets/lengths/speeds
- Ver skill `routing-isochrones` → `references/dijkstra-web-worker-csr.md` para formato completo y código

## Pitfalls

1. **OSMnx descarga datos grandes** — El grafo de una ciudad puede ocupar 50-200MB en cache. Usar `cache/` directory.
2. **Tiempo de cálculo** — 1-5 minutos por ciudad dependiendo del tamaño. Ejecutar como batch job.
3. **network_type** — `'drive'` para coche, `'bike'` para bici, `'walk'` para peatón, `'all'` para todos.
4. **cutoff en segundos** — Dijkstra usa segundos, no minutos. 15min = 900s, 30min = 1800s, 60min = 3600s.
5. **convex hull** — El polígono resultante es convex hull, no sigue la costa. Para ciudades costeras, recortar con shoreline.
6. **⚠️ OSMnx OOM en VMs pequeñas (2GB RAM)** — Radio de 20km para Madrid (40K+ nodos) causa OOM (exit 137, killed). Usar **12km máximo** para ciudades grandes (Madrid, Barcelona, Valencia). Ciudades pequeñas (Bilbao, Zaragoza) toleran 15km. Síntoma: el proceso Python muere sin traceback, exit code 137. Solución: reducir `dist` en `graph_from_point()` o usar `graph_from_place()` con un boundary más pequeño.
7. **Primera ejecución** — Descarga datos de Overpass API. Necesita internet solo la primera vez.
8. **Actualizaciones** — Los datos OSM cambian. Recalcular periódicamente (mensual recomendado).
9. **CSR binario vs GeoJSON** — CSR binario es 10-50x más pequeño que GeoJSON y permite cálculo en tiempo real en el navegador. GeoJSON es más simple pero estático (no puedes cambiar el tiempo/modo sin regenerar). Usar CSR para apps client-side, GeoJSON para pre-visualización o export.

## Alternativa: OSRM Real-time (sin API key) — Boundary Detection

Cuando necesites calcular isócronas **en tiempo real** desde el navegador sin depender de APIs premium, usar el endpoint público de OSRM con **boundary detection por dirección**.

**⚠️ NO usar convex hull** — Produce círculos de mierda. David lo probó y corrigió. Usar boundary detection que genera formas irregulares siguiendo la red de carreteras.

### Concepto

```
72 direcciones × 8 radios = 576 puntos radiales
  → OSRM Table endpoint (multi-batch de 89 coords)
  → Para cada dirección: interpolación lineal último alcanzable / primero que excede
  → Polígono irregular que sigue la red vial real
```

### Algoritmo

1. **Generar puntos radiales:** 72 direcciones (cada 5°) × radios adaptativos
   - Radios: `[2, 5, 8, 12, 18, 25, 35, 50, 65, 80]` filtrados por `max(minutos * 0.9, 5)`
   - Ejemplo 30min: `[2, 5, 8, 12, 18, 25]` → 432 puntos

2. **Query OSRM `table` por batches** (max 89 coords, stagger 80ms):
   ```
   GET https://router.project-osrm.org/table/v1/driving/{coords}?annotations=duration
   ```

3. **Para cada dirección, encontrar boundary:**
   ```javascript
   const ptsDir = resultados.filter(r => r.dir === d).sort((a,b) => a.radioKm - b.radioKm);
   let lastReach = null, firstOver = null;
   for (const p of ptsDir) {
     if (p.dur <= targetSec) lastReach = p;
     else if (!firstOver) { firstOver = p; break; }
   }
   // Interpolación lineal
   if (lastReach && firstOver && firstOver.dur > lastReach.dur) {
     const frac = (targetSec - lastReach.dur) / (firstOver.dur - lastReach.dur);
     rBoundary = lastReach.radioKm + frac * (firstOver.radioKm - lastReach.radioKm);
   }
   ```

4. **Cerrar polígono** — Conectar boundary points en orden angular (sin convex hull)

### Resultados comparados (Madrid, 30min coche)

| Método | Área | Forma |
|--------|------|-------|
| ❌ Convex hull | 1250 km² | Círculo irregular |
| ✅ Boundary detection | 879 km² | Forma irregular real, sigue carreteras |

### Pitfalls OSRM

1. **OSRM público solo tiene `driving`** — No hay perfil `foot` o `bicycle`. Para andar, usar ORS o simulación.
2. **Variable case-sensitive** — `dlat` ≠ `dLat`. JS no da error, solo `undefined`.
3. **Max ~89 coordenadas por llamada `table`** — Dividir en batches, stagger 80ms.
4. **Rate limit no documentado** — En la práctica tolerante con stagger.
5. **Sin semáforos ni restricciones horarias** — OSRM usa datos OSM básicos.
6. **No hay datos de elevación** — La velocidad es plana. Para pendientes, usar Valhalla con DEM.
7. **Radios muy bajos = pocos puntos** — Asegurar al menos `[2, 5]` km para tiempos cortos.

### Cadena de fallback recomendada

```javascript
async function calcularIsocrona(lng, lat, modo, minutos) {
  // 1. ORS (si hay key — más preciso)
  const apiKey = localStorage.getItem('isotime_ors_key');
  if (apiKey) {
    try { return await calcularIsocronaORS(lng, lat, modo, minutos, apiKey); }
    catch (e) { console.warn('ORS failed:', e.message); }
  }
  // 2. OSRM (solo coche — routing real sin key)
  if (modo === 'car') {
    try { return await calcularIsocronaOSRM(lng, lat, minutos); }
    catch (e) { console.warn('OSRM failed:', e.message); }
  }
  // 3. Simulación (fallback final)
  return calcularIsocronaSim(lng, lat, modo, minutos);
}
```

## Futuras mejoras

1. **Shoreline clipping** — Recortar isócronas costeras con Natural Earth data
2. **Valhalla local** — Para isócronas con elevación real (desnivel)
3. **OTP integration** — Isochrone de transporte público con transbordos reales
4. **Cron de actualización** — Recalcular isócronas mensualmente vía cron job
5. **More cities** — Añadir Madrid, Barcelona, etc.
