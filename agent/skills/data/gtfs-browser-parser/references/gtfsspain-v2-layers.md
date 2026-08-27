# GTFSSpain v2.2 — Sistema de capas (2026-07-02)

## Commits
- v2.2 layers: `4cfe1b4` — feat: capas GBFS, Parkings y ZBE

## Capas implementadas

| Capa | ID | Fuente | Datos |
|------|-----|--------|-------|
| 🚲 Bicicletas GBFS | `gbfs` | API GBFS (68 sistemas) | Estaciones con capacidad |
| 🅿️ Parkings públicos | `parking-public` | Overpass API (OSM) | Amenity=parking, access≠private |
| 🏢 Parkings privados | `parking-private` | Overpass API (OSM) | Amenity=parking, access=private/customers |
| 🚫 ZBE / Regulado | `zbe` | Overpass API (OSM) | boundary=low_emission_zone, parking:regulation |

## GBFS — Fuentes de datos

- **Catálogo:** `https://raw.githubusercontent.com/Ntizar/GBFSSpain/main/data/systems.json`
- **Discovery:** Cada sistema tiene `discovery_url` (GBFS v3.0)
- **Feeds:** `station_information` → coordenadas + capacidad
- **Filtro:** Solo sistemas dentro de bounding box España (lat 35.5-44.0, lon -10.0-5.0)
- **Batch:** 5 sistemas en paralelo con `Promise.allSettled`

### GBFS CORS
Algunas APIs GBFS bloquean CORS en navegador. Si falla fetch, la capa se muestra vacía (sin error visible). En servidor local (`python server.py`) funciona correctamente.

## Overpass API — Queries

### Parkings públicos
```
[out:json][timeout:25];(
  node["amenity"="parking"]["access"!="private"]["access"!="customers"](bbox);
  way["amenity"="parking"]["access"!="private"]["access"!="customers"](bbox);
);out center body;
```

### Parkings privados
```
[out:json][timeout:25];(
  node["amenity"="parking"]["access"="private"](bbox);
  node["amenity"="parking"]["access"="customers"](bbox);
  way["amenity"="parking"]["access"="private"](bbox);
  way["amenity"="parking"]["access"="customers"](bbox);
);out center body;
```

### ZBE / Estacionamiento regulado
```
[out:json][timeout:25];(
  way["boundary"="low_emission_zone"](bbox);
  relation["boundary"="low_emission_zone"](bbox);
  node["amenity"="parking"]["parking:regulation"="yes"](bbox);
  way["amenity"="parking"]["parking:regulation"="yes"](bbox);
);out center body;
```

**NOTA:** Overpass API tiene rate limits (~2 req/s). El debounce de 1s en `map.on('moveend')` evita saturar la API.

## Arquitectura del código

### Variables globales
```javascript
const layerState = {
  'gbfs':            { active: false, layer: null, data: null, loading: false },
  'parking-public':  { active: false, layer: null, data: null, loading: false },
  'parking-private': { active: false, layer: null, data: null, loading: false },
  'zbe':             { active: false, layer: null, data: null, loading: false }
};
let gbfsCatalog = null; // Cache del catálogo GBFS
```

### Funciones
- `toggleLayer(layerId)` — Activa/desactiva capa
- `loadLayerData(layerId)` — Carga datos si no están cacheados
- `loadGBFSLayer()` — Fetch GBFS stations
- `loadOSMLayer(layerId, type)` — Fetch Overpass API
- `map.on('moveend')` — Auto-refresh con debounce 1s

### CSS
- `.layer-toggle` — Contenedor del toggle
- `.layer-toggle.active` — Estado activo (azul)
- `.layer-switch` — Switch visual (pill con bola blanca)
- `.layer-count` — Contador de elementos
- `.layer-loading` / `.layer-error` — Estados de carga

## Pitfalls

1. **Overpass API timeout** — Queries complejas en bbox grande pueden tardar >25s. Aumentar `timeout:25` o dividir en queries más pequeñas.
2. **GBFS CORS** — APIs como Bicing (Barcelona) bloquean CORS. Funciona en localhost pero no en Pages.
3. **Doble carga** — Si el usuario activa una capa, mueve el mapa, y la capa se recarga, los marcadores se duplican. FIX: `map.removeLayer()` antes de `addTo(map)`.
4. **way sin center** — Algunos ways de OSM no tienen `center` (polígonos muy grandes). Filtrar elementos sin `lat/lon`.
