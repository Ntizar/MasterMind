---
name: time
version: "7.0.0"
description: "Time — herramienta definitiva de análisis de movilidad laboral en España. Isócrónas ORS/GTFS, datos INE, GBFS, costes, CO₂, teletrabajo, informes DOCX 15 secciones. Click = resultado completo."
author: David Antizar
tags: [time, time2, isochrones, gtfs, routing, ors, nap, leaflet, transport, mobility, docx, shapefile, shp, datos-reales, ign, kaizen, csv, gbfs, co2, teletrabajo, vivienda, costes]
related_skills: [ign-wmts-tiles, isochrone-routing-tools, kaizen-design-system, nap-data-pipeline, gbfsspain]
---

# Time — Isócrónas de Movilidad Laboral

Time (antes TimeIneco) es la herramienta definitiva de análisis de movilidad laboral en España. Calcula isócrónas reales para 5 modos de transporte, integra datos demográficos INE, precios de vivienda, bicicletas compartidas, y genera informes DOCX profesionales de 15 secciones.

**Filosofía UX:** Un clic en el mapa → sale TODO. Sin configurar, sin clics extra. El mapa es la interfaz.

**URL v1:** `https://time-ntizar-ntizar.apps.nan.builders/`
**Repo v1:** `Ntizar/Time` (privado)
**Repo v2 (Time2):** `Ntizar/TimeIneco2` (privado) — sucesor con arquitectura completa
**Plan v2:** `AUDITORIA-Y-PLAN.md` en el repo TimeIneco2
**Diseño:** Kaizen Design System v4.0 (flat corporativo, azul #1A4488 + rojo #CB1823)
**Base map:** IGN WMTS (gris, topográfica, ortofoto)

### Auditoría Time v1.0 — Hallazgos (25/06/2026)

**Lo que funciona bien:**
- Arquitectura modular (12 módulos ES, responsabilidad clara)
- Motor GTFS con BFS + convex hull (bien diseñado, solo le faltan datos reales)
- Export multi-formato (DOCX, CSV, SHP, GeoJSON, KML)
- Datos demográficos reales (28K CPs, salarios INE, población INE)
- Kaizen Design System (flat, corporativo)
- Servidor Node.js autocontenido (sin Express, sin npm deps)
- CityBikes integrado (74 redes España)

**Problemas críticos:**
- 🔴 GTFS datos ficticios (rutas "1","2","3", 0 viajes) — el panel de TP es decorativo
- 🔴 ORS API key puede estar revocada (403) — isócrónas son simulaciones
- 🔴 No hay parsing GTFS real end-to-end (el engine está preparado pero nunca recibe datos reales)
- 🟡 `suavizarPoligono()` es no-op (comenta "skip every 3" pero ejecuta todos)
- 🟡 Fórmula población con número mágico `* 2.5`
- 🟡 Constante `km2PerDeg2 = 12360` solo válida en Madrid

---

## 1. Arquitectura General (v5.0)

```
Frontend (HTML/JS vanilla, sin framework)
    ├── Leaflet (mapa base: IGN WMTS 3 capas + CARTO fallback)
    ├── Kaizen Design System (CDN)
    ├── OpenRouteService API (isocronas reales vía proxy)
    ├── CityBikes API (bicicletas públicas, 74 redes España)
    ├── GTFS Engine browser-side (paradas + rutas + horarios)
    ├── Turf.js (coastline clipping)
    ├── docx-report.js (DOCX 15 secciones)
    ├── csv-export.js (CSV completo)
    ├── interpretaciones.js (interpretaciones automáticas)
    ├── layers.js (control de capas toggleables)
    ├── JSZip (GTFS ZIP upload + export batch)
    └── shp.js (ESRI Shapefile)

Backend (Node.js, server.mjs)
    ├── .env loader manual (sin dotenv)
    ├── Proxy ORS → ORS_API_KEY
    ├── Proxy NAP → NAP_API_KEY
    ├── Proxy CityBikes (sin key)
    ├── GTFS Cache → /gtfs-cache/:city (JSON compacto)
    ├── Health check GET /healthz
    └── Static files
```

## 2. GTFS Pre-cargados (v6.0) — Sin subir archivos

**Concepto:** 5 ciudades con GTFS pre-procesado en JSON compacto. Auto-carga al detectar la ciudad.

**Ciudades disponibles:**
| Ciudad | Paradas | Rutas | Tamaño JSON |
|--------|---------|-------|-------------|
| Bilbao | 533 | 56 | 153KB |
| Málaga | 1,126 | 48 | 315KB |
| Sevilla | 1,038 | 59 | 212KB |
| Valencia | 1,155 | 49 | 336KB |
| Zaragoza | 996 | 55 | 287KB |

**Endpoints servidor:**
- `GET /gtfs-cache/list` → lista ciudades disponibles
- `GET /gtfs-cache/:city` → JSON compacto de la ciudad

**Flujo:**
1. Usuario entra dirección → `detectarCiudad()` identifica la ciudad
2. Si está en `CIUDADES_CON_CACHE` → `verificarCacheDisponible()` comprueba
3. Auto-carga via `cargarDesdeServidor()` → fetch JSON → `cargarDesdeCache()`
4. Sin clic del usuario, las paradas aparecen en el mapa

**JSON compacto formato:**
```json
{
  "city": "bilbao",
  "stops": [{"stop_id", "stop_name", "stop_lat", "stop_lon"}],
  "routes": [{"route_id", "route_short_name", "route_long_name", "route_type"}],
  "route_trip_counts": {"route_id": trip_count},
  "stop_trip_map": {"stop_id": {"trip_count": N, "sample_arrivals": [...]}}
}
```

**Pitfall:** El JSON compacto NO tiene `stop_times` raw. `cargarDesdeServidor()` reconstruye `trips[]` y `stop_times[]` a partir de `route_trip_counts` y `stop_trip_map` para compatibilidad con `cargarDesdeCache()`.

**Procesamiento inicial (Python):**
```bash
cd /root/workspace/Time/data/gtfs
# Procesar cada ciudad desde raw GTFS → JSON compacto
# Guardar en data/gtfs-cache/{city}.json
```

## 3. Mapa Base — IGN WMTS
See `references/time-v5-architecture.md` for tile URLs, layer config, pitfalls.

## 4. Diseño — Kaizen Design System v4.0
See `references/time-v5-architecture.md` for colors, layout, CSS patterns.

## 5-7. Layers, CSV, Interpretaciones
See `references/time-v5-architecture.md` for module APIs and patterns.

## 8. APIs (.env)
- ORS: `Authorization: <key>` (sin Bearer)
- NAP: `ApiKey: <key>` (fichero/{id}/descarga → S3 temporal 15min)
- CityBikes: sin key (api.citybik.es)
- IGN: sin key (CC BY 4.0)
- Nominatim: User-Agent obligatorio

## 9. Datos Demográficos
INE Padrón 2025, INE EAES 2024. SOLO datos REALES, nunca inventar.

## 10. UI Preferences
Ver SOUL.md preferencias David. Kaizen flat, sin dark, sin cards IA, sidebar 380px.

## 11. Lecciones Aprendidas
- .env loader manual, no source .env antes
- Git: NUNCA trackear GTFS (750MB+)
- ORS: enviar locations como pareja simple `[lng, lat]`
- IGN: `FORMAT=image/jpeg` obligatorio
- CSV: BOM UTF-8 para Excel
- NAP: NO usar /conjunto-dato/{id} (404)
- GTFS cache: JSON compacto reconstruye trips[] y stop_times[] para compatibilidad
- **ORS key 403:** Algunas keys v1 no tienen permisos de isócronas. Health check: `ors_api: false`. Fix: crear key nueva en openrouteservice.org
- **Kaizen CSS:** Repo privado → CDN no sirve. Copiar `kaizen.css` local a `css/kaizen.css`
- **Motores locales:** Valhalla Docker (isochrones nativas) o OSMnx+NetworkX (script Python) como alternativa a ORS API. Ver `references/local-routing-engines.md`
- **Subagentes en paralelo:** Si 2+ subagentes modifican el mismo archivo, pueden duplicar funciones. Error silencioso en `node --check`, visible solo en navegador. Ver pitfall #26 en `routing-isochrones`

## 12. Time2 — Arquitectura v2.0 (25/06/2026)

**Repo:** `Ntizar/TimeIneco2` (privado, creado)
**Plan completo:** `AUDITORIA-Y-PLAN.md` en el repo
**Estimación:** ~3500 líneas, ~20h de desarrollo

### 10 capas de datos
1. 🗺️ Mapa IGN + geocodificación Nominatim
2. 🚌 GTFS real de NAP API (161 datasets, España completa)
3. 🚗 Isócrónas ORS reales (coche, bici, andando)
4. 📊 Demografía INE (CPs, población, salarios)
5. 🏠 Vivienda (Idealista, precios alquiler/venta por CP)
6. 🚲 Bicicletas compartidas (CityBikes, 74 redes)
7. 💰 Costes anuales por modo (combustible, abono, IRPF, mantenimiento)
8. 🌍 Emisiones CO₂ por modo (IPCC AR6)
9. 💻 Escenarios teletrabajo (5d presencial, 3+2, 2+3, full remote)
10. 📄 Informe DOCX 15 secciones + CSV + GeoJSON + SHP

### Módulos JS (código estimado)
```
js/
├── app.js                 # Orquestador: click → todos los datos (~500 líneas)
├── map.js                 # Leaflet + 4 capas IGN + click handler (~400 líneas)
├── config.js              # Config centralizada
├── geocoder.js            # Nominatim geocodificación
├── isochrones.js          # ORS → simulación → fallback (~500 líneas)
├── isochrones-gtfs.js     # GTFS BFS + convex hull (~200 líneas)
├── gtfs-engine.js         # Parser GTFS completo (~600 líneas)
├── nap-catalog.js         # Catálogo 161 datasets NAP
├── demographics.js        # INE: CPs, población, salarios (~400 líneas)
├── vivienda.js            # Precios Idealista por CP (~250 líneas)
├── gbfs-engine.js         # CityBikes API (~200 líneas)
├── costes.js              # Cálculo costes por modo
├── co2.js                 # Emisiones IPCC AR6
├── teletrabajo.js         # 4 escenarios teletrabajo
├── layers.js              # Control de capas del mapa
├── markers.js             # Marcadores por tipo
├── popup-builder.js       # Popups ricos con info completa
├── report.js              # DOCX 15 secciones (~600 líneas)
├── csv-export.js          # CSV completo (~150 líneas)
├── geojson-export.js      # GeoJSON isócrónas
├── shp-export.js          # Shapefile QGIS
├── utils.js               # Haversine, formateo
├── cache.js               # Cache localStorage/IndexedDB
├── clip.js                # Clipeo costero Natural Earth
└── vendor/                # docx, jszip, turf (vendored)
```

### Flujo "click = resultado"
```
CLICK EN MAPA
  ├── 1. reverseGeocode(lat, lng) → dirección + CP
  ├── 2. demographics.lookup(lat, lng) → población + salario + vivienda
  ├── 3. gbfs.nearby(lat, lng, 500) → estaciones bici
  ├── 4. gtfs.nearby(lat, lng, 500) → paradas + líneas
  ├── 5. nap.availableForCity(city) → operadores
  ├── 6. PARALELO: isócrónas (5 modos × 3 tiempos = 15 polígonos)
  ├── 7. costes.calcular(todosLosModos)
  ├── 8. co2.calcular(todosLosModos)
  ├── 9. teletrabajo.escenarios(costes, co2)
  └── 10. RENDER: panel + mapa + KPIs → un clic = DOCX
```

### Scripts de datos
- `download-gtfs-nap.py` — Descarga GTFS de NAP API (10 ciudades piloto)
- `precalculate-isochrones.py` — Pre-cálculo OSMnx + NetworkX
- `generate-data-files.py` — Genera datos INE/Idealista/AEAT

### APIs utilizadas
| Fuente | API | Key | Coste |
|--------|-----|-----|-------|
| ORS | REST | `ORS_API_KEY` | 2,500 req/día gratis |
| IGN | WMTS | Ninguna | Gratis CC BY 4.0 |
| NAP/GTFS | REST | `NAP_API_KEY` | Gratis |
| CityBikes | REST | Ninguna | Gratis |
| INE | REST | Ninguna | Gratis |
| Nominatim | REST | User-Agent | 1 req/s |
| Idealista | Scraping | Ninguna | Gratis |
| AEAT | REST | Ninguna | Gratis |
| Natural Earth | GeoJSON | Ninguna | Gratis |
| turf.js / JSZip / docx.js | JS lib | Ninguna | Gratis MIT |

### Pitfalls Time2
- NAP enlaces S3 caducan en 15 min → descargar rápido
- Solo GTFS-ZIP descargables (no GTFS-RT, NetEx, SIRI)
- Nominatim rate limit 1 req/s → no bucle
- ORS quota 2,500/día → usar pre-calculadas cuando posible
- GTFS grandes (>100MB, ej: Galicia 136MB) → parsear solo archivos necesarios
- `km2PerDeg2` no es constante → usar Haversine para áreas
- NaN CDN cache 2-3 min post-push

## Referencias
- `references/time-v5-architecture.md` — Arquitectura completa v5.0 (Time v1)
- `references/time2-master-plan.md` — Plan maestro Time2.0: auditoría + arquitectura completa (25/06/2026)
- `references/docx-report-v2.0.md` — Arquitectura DOCX
- `references/export-shapefile-v2.2.md` — Export multi-formato
- `references/poblacion-cp-metodologia.md` — Metodología datos población
- `references/ine-api-datos-reales.md` — API INE
- `references/citybikes-api-integration.md` — CityBikes API
- `references/nap-api-descarga-gtfs.md` — NAP API
- `references/isocronas-v2.1-engine.md` — Motor simulación
- `references/gtfs-multi-ciudad.md` — GTFS multi-ciudad
- `references/local-routing-engines.md` — Motores locales (Valhalla, OSMnx)
- `scripts/generate-gtfs-synthetic.py` — Generador GTFS sintético
