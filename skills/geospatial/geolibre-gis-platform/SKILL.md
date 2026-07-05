---
name: geolibre-gis-platform
version: "1.0.0"
description: "GeoLibre — plataforma GIS ligera cloud-native para visualizar, explorar y analizar datos geoespaciales. Funciona en navegador, desktop, mobile y Jupyter. Stack: MapLibre GL + DuckDB + Tauri."
tags: [gis, geospatial, maplibre, duckdb, tauri, data-science, cloud-native]
---

# GeoLibre — Plataforma GIS Cloud-Native

## Resumen

[GeoLibre](https://geolibre.app) (⭐1.4K) es una plataforma GIS open-source ligera que permite visualizar, explorar y analizar datos geoespaciales en cualquier entorno: navegador, desktop (Tauri), mobile, y Jupyter notebooks. Usa MapLibre GL JS para rendering y DuckDB para análisis espacial.

## Cuándo usar

- Plataforma GIS multi-entorno (web + desktop + mobile + notebook)
- Análisis espacial con DuckDB (polygons, points, joins espaciales)
- Visualización de datos geoespaciales grandes sin servidor
- Dashboard GIS con capas personalizadas y queries SQL espaciales

## Stack

| Componente | Tecnología | Función |
|-----------|-----------|---------|
| Rendering | MapLibre GL JS | Mapas vectoriales 2D/3D |
| Análisis | DuckDB-WASM | SQL espacial en navegador |
| Desktop | Tauri | App nativa multiplataforma |
| Mobile | Tauri Mobile | iOS/Android |
| Notebook | Jupyter | Integración Python |

## Patrón de uso

```javascript
import maplibregl from 'maplibre-gl';
import * as duckdb from '@duckdb/duckdb-wasm';

// 1. Inicializar mapa MapLibre
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [-3.7, 40.4],
  zoom: 10
});

// 2. Inicializar DuckDB-WASM para análisis espacial
const db = await duckdb.createDuckDB();
await db.registerFileText('data.geojson', geojsonString);

// 3. Query espacial con DuckDB
const result = await db.query(`
  SELECT nombre, ST_Area(geom) as area_km2
  FROM read_geojson('data.geojson')
  WHERE ST_Contains(geom, ST_Point(-3.7, 40.4))
  ORDER BY area_km2 DESC
`);

// 4. Visualizar resultados en el mapa
map.addSource('results', {
  type: 'geojson',
  data: resultToGeoJSON(result)
});
map.addLayer({
  id: 'results-fill',
  type: 'fill',
  source: 'results',
  paint: {
    'fill-color': ['interpolate', ['linear'], ['get', 'area_km2'], 0, '#f0f0e8', 100, '#0f6d7e'],
    'fill-opacity': 0.7
  }
});
```

## Ventajas sobre alternativas

| vs | GeoLibre | Alternativa |
|----|---------|------------|
| ArcGIS Online | Gratis, self-hosted | Caro, cloud-locked |
| QGIS | En navegador | Desktop only |
| Mapbox Studio | Sin API key | Requiere API key |
| Google Earth Engine | Local | Cloud + API |

## Pitfalls

- **DuckDB-WASM:** Carga inicial lenta (~10MB). Cachear con service worker.
- **MapLibre vs Mapbox:** APIs casi idénticas pero algunas diferencias en expressions.
- **Tauri mobile:** Aún en beta. Usar con cuidado en producción.
- **Datos grandes:** DuckDB-WASM maneja hasta ~1M features en navegador. Más = usar server.

## Referencias

- GeoLibre: https://github.com/opengeos/GeoLibre (demo: https://geolibre.app)
- MapLibre GL: https://maplibre.org/
- DuckDB-WASM: https://duckdb.org/docs/api/wasm

---

**Hecho con ❤️ por David Antizar**
