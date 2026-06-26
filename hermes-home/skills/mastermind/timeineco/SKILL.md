---
name: time
version: "5.0.0"
description: "Time — visor de isocronas multi-modo con ORS, IGN maps, GTFS upload, GBFS, Kaizen Design, CSV export, interpretaciones automáticas. Informes profesionales DOCX. Desplegado en NaN.builders."
author: David Antizar
tags: [time, isochrones, gtfs, routing, ors, nap, leaflet, transport, mobility, docx, shapefile, shp, datos-reales, ign, kaizen, csv, gbfs]
related_skills: [ign-wmts-tiles, isochrone-routing-tools, kaizen-design-system]
---

# Time — Isocronas de Movilidad Laboral

Time (antes TimeIneco) calcula y visualiza **isocronas** (áreas accesibles en X tiempo) para múltiples modos de transporte. Genera informes DOCX profesionales + CSV completo con datos demográficos reales del INE, paradas GTFS, estaciones de bicicleta compartida, y análisis de costes/emisiones.

**URL:** `https://time-ntizar-ntizar.apps.nan.builders/`
**Repositorio:** GitHub `Ntizar/Time` (privado, renombrado desde TimeIneco)
**Diseño:** Kaizen Design System v4.0 (flat corporativo, azul #1A4488 + rojo #CB1823)
**Base map:** IGN WMTS (gris, topográfica, ortofoto)

---

## 1. Arquitectura General (v5.0)

```
Frontend (HTML/JS vanilla, sin framework)
    ├── Leaflet (mapa base: IGN WMTS 3 capas + CARTO fallback)
    ├── Kaizen Design System (CDN: cdn.jsdelivr.net/gh/Ntizar/kaizen-design-system@master/kaizen.css)
    ├── OpenRouteService API (isocronas reales vía proxy Node.js)
    ├── CityBikes API (bicicletas públicas tiempo real, 74 redes España)
    ├── GTFS Engine browser-side (paradas cercanas + rutas + horarios)
    ├── Turf.js (coastline clipping)
    ├── docx-report.js (DOCX informe 15 secciones)
    ├── csv-export.js (CSV completo para análisis longitudinal)
    ├── interpretaciones.js (interpretaciones automáticas del dato)
    ├── layers.js (control de capas toggleables)
    ├── JSZip (subida de GTFS ZIP + export batch)
    └── shp.js (ESRI Shapefile QGIS-compatible + filtrado por distancia/modo)

Backend (Node.js, server.mjs)
    ├── .env loader manual (sin dotenv)
    ├── Proxy ORS (POST /isochrone)         ← ORS_API_KEY
    ├── Proxy NAP (POST /nap-download-gtfs)  ← NAP_API_KEY
    ├── Proxy CityBikes (GET /citybikes/*)   ← sin key
    ├── Proxy GTFS download (POST /gtfs-download)
    ├── Proxy Nominatim (GET /geocode)
    ├── Health check (GET /healthz)
    └── Static files
```

### Módulos nuevos (v5.0)

| Módulo | Función | Fichero |
|--------|---------|---------|
| `layers.js` | Control de capas toggleables del mapa | `js/layers.js` |
| `csv-export.js` | CSV completo con todos los datos | `js/csv-export.js` |
| `interpretaciones.js` | Generador automático de interpretaciones | `js/interpretaciones.js` |
| `config.js` | Config centralizada con URLs IGN | `js/config.js` |

---

## 2. Mapa Base — IGN WMTS

**Fuente:** Instituto Geográfico Nacional, WMTS gratuito, CC BY 4.0
**URL:** `https://www.ign.es/wmts/ign-base`

### Capas disponibles

| Capa | Descripción | Default |
|------|-------------|---------|
| `IGNBase-gris` | Topográfico en escala de grises | ✅ SÍ (mejor para datos) |
| `IGNBaseTodo` | Topográfico completo (colores) | |
| `IGNBaseOrto` | Ortofotografía (foto aérea) | |
| CARTO Light | Fallback OSM | |

### Tile URL pattern
```javascript
`${IGN.base}?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=${capa}&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILECOL={x}&TILEROW={y}&FORMAT=image/jpeg`
```

### Pitfalls IGN
- `FORMAT=image/jpeg` OBLIGATORIO (si no → error 400)
- NO usar `IGNBaseSimplificado` ni `IGNBaseTodo-nofondo` (devuelven 400)
- Atribución: `© IGN — Instituto Geográfico Nacional (CC BY 4.0)`

### Integración en map.js
```javascript
tileLayers.ignGris = L.tileLayer(CONFIG.IGN.tileUrl(CONFIG.IGN.capas.gris), {
  attribution: CONFIG.IGN.attribution,
  maxZoom: CONFIG.IGN.maxZoom
});
// Default: IGN Gris
tileLayers.ignGris.addTo(mapa);
// Control de capas
L.control.layers({
  '🗺️ IGN Gris (datos)': tileLayers.ignGris,
  '🏔️ IGN Topográfica': tileLayers.ignTopo,
  '🛰️ IGN Ortofotografía': tileLayers.ignOrto,
  '🌐 CARTO Light': tileLayers.cartoLight
}, null, { position: 'topright' }).addTo(mapa);
```

---

## 3. Diseño — Kaizen Design System v4.0

**CDN:** `cdn.jsdelivr.net/gh/Ntizar/kaizen-design-system@master/kaizen.css`
**CSS custom:** `css/time-custom.css` (<100 líneas, overrides mínimos)

### Colores oficiales

| Color | Hex | Uso |
|-------|-----|-----|
| Azul principal | `#1A4488` | Header, botones primarios, acentos, isócrona coche |
| Rojo | `#CB1823` | Complementario, alertas |
| Azul medio | `#3463AC` | Complementario secundario |
| Azul claro | `#6B96CF` | Complementario terciario |

### Layout
- Sidebar 380px fijo (`.kz-sidebar`)
- Header 60px (`.kz-header`)
- Mapa full-width (`.kz-map`)
- Grid: `.kz-grid-sidebar { display: grid; grid-template-columns: 380px 1fr; }`

### Reglas Kaizen
- **NO** cards bordeadas pesadas, sombras, gradientes, bordes >1px
- **SÍ** diseño plano, separadores sutiles (1px), títulos azul con línea debajo
- Clases: `kz-btn-primary`, `kz-input`, `kz-chips`, `kz-chip`, `kz-table-mini`, `kz-dropzone`, `kz-stats-row`, `kz-stat-box`

### HTML pattern
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/kaizen-design-system@master/kaizen.css">
<link rel="stylesheet" href="css/time-custom.css?v=1">
```

---

## 4. Sistema de Capas (layers.js)

Toggle individual de capas del mapa. Cada capa es un `L.layerGroup()` independiente.

### Capas disponibles

| Capa ID | Nombre | Default | Grupo |
|---------|--------|---------|-------|
| `isocrona_coche` | 🚗 Isócrona Coche | ON | isocronas |
| `isocrona_bici` | 🚲 Isócrona Bici | ON | isocronas |
| `isocrona_foot` | 🚶 Isócrona Andando | ON | isocronas |
| `isocrona_bus` | 🚌 Isócrona Bus | ON | isocronas |
| `isocrona_metro` | 🚇 Isócrona Metro | ON | isocronas |
| `paradas_gtfs` | 🚏 Paradas GTFS | OFF | transporte |
| `lineas_gtfs` | 📐 Líneas de Ruta | OFF | transporte |
| `estaciones_gbfs` | 🚲 Estaciones Bici | OFF | bici |
| `radio_500m` | ⭕ Radio 500m | ON | auxiliar |
| `cp_boundary` | 📮 Código Postal | OFF | auxiliar |

### API
```javascript
import { initLayers, toggleCapa, renderPanelCapas, limpiarTodasCapas, getLayerGroup } from './layers.js';
initLayers(mapa);           // Crear layerGroups
toggleCapa('paradas_gtfs');  // Toggle ON/OFF
renderPanelCapas();          // Renderizar panel en sidebar
getLayerGroup('isocrona_car'); // Obtener L.layerGroup para agregar features
```

---

## 5. Export — DOCX + CSV + ZIP

### DOCX (15 secciones)
1. Portada, 2. Resumen Ejecutivo, 3. Mapa de Isocronas, 4. Datos Demográficos, 5. Transporte Público, 6. Bicicletas, 7. Comparativa por Modo, 8. Costes, 9. Escenarios Teletrabajo, 10. CO₂, 11. Ranking CPs, 12. Alertas, 13. Rutas Recomendadas, 14. Metodología y Fuentes, 15. Créditos

### CSV completo (csv-export.js)
Archivo con TODOS los datos para análisis longitudinal (comparativa año a año).

**Estructura:** `seccion,categoria,indicador,valor,unidad,fuente,anio_fuente,fecha_generacion`

**Secciones CSV:** resumen, isocrona, transporte, bici, costes, co2

**Pitfall:** Incluir BOM UTF-8 (`\uFEFF`) para compatibilidad con Excel.

### ZIP batch
Un click genera ZIP con: `time-datos.csv`, `time-isocronas.geojson`, `time-paradas-gtfs.geojson`, `time-estaciones-bici.geojson`, `README.md`

---

## 6. Interpretaciones Automáticas (interpretaciones.js)

Genera texto narrativo profesional a partir de los datos calculados.

### Secciones
- **Accesibilidad:** Compara áreas por modo, ratio coche/pie
- **Transporte público:** Número de paradas, líneas, frecuencia estimada
- **Bicicletas:** Estaciones cercanas, bicis disponibles, más cercana
- **Costes:** Coste anual por modo, ahorro teletrabajo por escenarios
- **CO₂:** Emisiones anuales, equivalente en árboles, reducción con TP
- **Demografía:** Población, salario, precios de la zona
- **Recomendaciones:** Acciones concretas basadas en los datos

### API
```javascript
import { generarInterpretaciones } from './interpretaciones.js';
const interp = generarInterpretaciones(resultados, punto, modos, tiempos, gtfsData, biciData, transporteCercano, demograficos);
// interp.accesibilidad, interp.transportePublico, interp.bicicletas, interp.costes, interp.co2, interp.demografia, interp.recomendaciones
```

---

## 7. APIs Configuradas (.env)

**CRÍTICO:** El servidor NO usa dotenv. Loader manual en server.mjs.

### ORS
- **Env:** `ORS_API_KEY`
- **Endpoint:** `POST /isochrone` → `https://api.openrouteservice.org/v2/isochrones/{profile}`
- **Perfiles:** `driving-car`, `cycling-regular`, `foot-walking`
- **Auth:** `Authorization: <key>` (NO Bearer, NO Key prefix)
- **Pitfall:** Frontend enviar `locations: [-3.7, 40.4]` (pareja simple), NO `[[-3.7, 40.4]]`

### CityBikes/GBFS
- Sin key (API abierta)
- 74 redes España, incluyendo BiciMAD, Bicing, Valenbisi
- Módulo: `js/citybikes.js` (global `window.CityBikes`)

### NAP/GTFS
- **Env:** `NAP_API_KEY`
- `GET /api/v2/fichero/{id}/descarga` → redirect S3 temporal (15 min)
- Dataset IDs: Sevilla=1567, Valencia=1166, Bilbao=1460, Zaragoza=1176, Málaga=1494

### IGN WMTS
- Sin key, CC BY 4.0
- URL: `https://www.ign.es/wmts/ign-base`

### Nominatim
- User-Agent obligatorio: `Time/2.0 (time@antizar.es)`
- Rate limit: 1 req/s

---

## 8. Datos Demográficos

### Datasets (en `/data/`)

| Dataset | Fuente | Cobertura |
|---------|--------|-----------|
| `codigos-postales-spain.json` | INE + Wikipedia | 299 CPs |
| `poblacion-cp.json` | INE Padrón 2025 | 299 CPs |
| `salarios-medios.json` | INE EAES 2024 | 51 provincias |
| `salarios-por-cp.json` | INE EAES 2024 | 299 CPs |
| `ciudades-gtfs-nap.json` | NAP metadata | Multi-ciudad |

### ⚠️ Regla de David: SOLO datos REALES
- NUNCA inventar datos demográficos o económicos
- Si no hay dato real → "No disponible" en el informe
- Cada dato en DOCX debe tener fuente y año de referencia

---

## 9. Preferencias de UI (David)

### ❌ NO hacer
- Dark mode, glass borders, horizontal lines, cards icono+titulo+texto
- Botones de export múltiples overwhelming
- Selector de ciudad redundante
- Tabla comparativa en HTML (duplica DOCX)

### ✅ SÍ hacer
- Fondo light, Kaizen flat corporativo
- Datos reales con links a fuentes en sidebar
- Sidebar simplificada: dirección + modos + tiempo + botón + capas
- Panel NAP colapsable
- Dropzone drag & drop para GTFS
- 3 botones de export: DOCX (primario), CSV, ZIP batch

---

## 10. Estructura de Archivos (v5.0)

```
Time/
├── index.html              # Entry point (Kaizen CSS)
├── css/
│   └── time-custom.css     # Overrides Kaizen (<100 líneas)
├── js/
│   ├── main.js             # Orquestación principal v2.0
│   ├── map.js              # Leaflet: IGN tiles + capas + marcadores
│   ├── config.js           # Config: modos, IGN URLs, colores Kaizen
│   ├── layers.js           # Control de capas toggleables [NUEVO]
│   ├── csv-export.js       # CSV completo exportable [NUEVO]
│   ├── interpretaciones.js # Interpretaciones automáticas [NUEVO]
│   ├── isochrones.js       # Motor: ORS proxy + simulación v2.1
│   ├── isochrones-gtfs.js  # Motor GTFS (BFS + convex hull)
│   ├── gtfs-engine.v7.js   # Motor GTFS browser-side
│   ├── demographics.js     # Datos demográficos INE/CP
│   ├── nap.js              # Catálogo NAP: operadores por ciudad
│   ├── docx-report.js      # DOCX informe (15 secciones)
│   ├── shp.js              # Export SHP/GeoJSON/CSV
│   ├── clip.js             # Coastline clipping
│   ├── utils.js            # Geocodificación, helpers
│   ├── citybikes.js        # CityBikes/GBFS API (74 redes España)
│   └── vendor/docx.umd.js  # Librería DOCX vendored
├── data/                   # Datos demográficos + GTFS
├── server.mjs              # Node.js: proxies + .env loader
├── .env                    # ORS_API_KEY + NAP_API_KEY
├── Dockerfile
└── README.md
```

---

## 11. Despliegue en NaN

```bash
# Local
cd /root/workspace/Time
node server.mjs  # El .env loader carga automáticamente

# NaN: push a GitHub → auto-deploy
# Health check: curl http://localhost:4000/healthz
```

---

## 12. Lecciones Aprendidas

### Git hygiene — archivos grandes
GTFS raw 750MB+ → NUNCA trackear en git. `.gitignore` con `data/gtfs/`, `data/gtfs-cache/`

### .env loader sin dotenv
Loader manual que SOLO carga variables que NO existen en `process.env`. No hacer `source .env` antes.

### CRÍTICO: Pérdida de .env al reescribir repo
SIEMPRE: `cp Repo/.env /root/.env-Time.bak` ANTES de reescribir repo

### Git push OOM con repos grandes
VM 2GB RAM. Crear repo fresco con solo código fuente si history > 500MB

### ORS proxy formato request
Frontend: `{ profile, locations: [-3.7, 40.4], range: [900] }` (pareja simple)
Servidor envuelve en `[[locations]]` para ORS

### NAP API patrón descarga
`/api/v2/fichero/{id}/descarga` → 200 con `enlaceDescarga` S3 temporal (15 min)
NO usar `/api/v2/conjunto-dato/{id}` (devuelve 404)

### IGN WMTS
`FORMAT=image/jpeg` OBLIGATORIO. NO usar capas `IGNBaseSimplificado` ni `IGNBaseTodo-nofondo`

### CSV UTF-8 BOM
Incluir `\uFEFF` al inicio del CSV para que Excel detecte UTF-8 correctamente

---

## Referencias

- `references/time-v5-architecture.md` — Arquitectura completa v5.0 (nuevos módulos, patrones)
- `references/docx-report-v2.0.md` — Arquitectura DOCX
- `references/export-shapefile-v2.2.md` — Export multi-formato
- `references/poblacion-cp-metodologia.md` — Metodología datos población
- `references/ine-api-datos-reales.md` — API INE: tablas, mapeo provincias
- `references/citybikes-api-integration.md` — CityBikes API
- `references/nap-api-descarga-gtfs.md` — NAP API: patrón descarga
- `references/isocronas-v2.1-engine.md` — Motor simulación
- `references/gtfs-multi-ciudad.md` — GTFS multi-ciudad
- `scripts/generate-gtfs-synthetic.py` — Generador GTFS sintético
