---
name: gtfs-browser-parser
description: Parser GTFS completo en navegador + catalogo de operadores por ciudad, busqueda por proximidad, fuentes multiples (cache, ZIP subido, localStorage, proxy), integracion mapa y PDF
version: "1.1.0"
tags: [gtfs, transporte, parser, navegador, movilidad, isocronas]
---

# GTFS Browser Parser — Patrón completo de Integración GTFS

## Descripción

Patrón para integrar datos GTFS de transporte público en aplicaciones web del navegador: detección de ciudad y operadores, carga selectiva de paradas cercanas, visualización en mapa Leaflet, informe PDF y exportación GeoJSON.

## Origen

Derivado de [nap-dashboard](https://github.com/Ntizar/nap-dashboard) (API NAP España) y [TimeIneco](https://timeineco-ntizar-ntizar.apps.nan.builders/) v0.7 (isocronas de movilidad laboral).

## Arquitectura General

```
User input (address)
  → geocode → ciudad detectada
  → catálogo operadores → usuario selecciona
  → cargar GTFS (cache / upload / proxy / localStorage)
  → findStopsNear(punto, radio 2km) → filtrar por Haversine
  → UI: chips de rutas + marcadores mapa + tabla detalle
  → PDF: seccion "Rutas de transporte publico disponibles"
  → Export: GeoJSON de paradas cercanas
```

## Estrategia de Carga: Filtrar en Origen

**REGLAS DE ORO:**

1. **No descargar todo el GTFS** — un feed de ciudad puede pesar 50-200 MB. Solo extrae paradas cercanas al punto de interés del usuario.
2. **El usuario elige el operador** — muestra catálogo de operadores por ciudad, el usuario selecciona uno, solo entonces descargas/cargas su GTFS.
3. **Múltiples fuentes, por orden de prioridad:**
   - Cache simulado (JSON embebido para demo)
   - localStorage (datos previamente cargados)
   - ZIP subido por usuario (el método más práctico)
   - Proxy servidor (descarga desde URL pública)

## Patrón: Catálogo de Operadores por Ciudad

```javascript
const EMPRESAS = {
  madrid: [
    { id: 'emt-madrid', nombre: 'EMT Madrid', modo: 'bus', lineas: 217,
      cacheable: true,  // cacheable = datos simulados embebidos
      gtfsUrl: 'https://opendata.emtmadrid.es/GTFS/Madrid' },
    { id: 'metro-madrid', nombre: 'Metro de Madrid', modo: 'metro', lineas: 13,
      cacheable: false } // requiere subida de ZIP
  ],
  barcelona: [
    { id: 'tmb-bus', nombre: 'TMB (Autobus)', modo: 'bus', lineas: 107, cacheable: false }
  ],
  // ~12+ ciudades espanolas con operadores catalogados
};

function detectarCiudad(displayName) {
  // 1. Buscar en EMPRESAS
  // 2. Fallback: matchear contra lista de ~50 ciudades
  // 3. Si no hay match, mostrar opcion de subir GTFS manualmente
}
```

## Patrón: Búsqueda por Proximidad (Haversine)

Solo extraer paradas dentro de un radio del punto de origen (default 2 km):

```javascript
function findStopsNear(lat, lng, radiusKm = 2) {
  const results = [];
  for (const stop of stops) {
    const dist = haversine(lat, lng, stop.stop_lat, stop.stop_lon);
    if (dist <= radiusKm) {
      const routeIds = stopRoutes[stop.stop_id] || [];
      results.push({ stop, distanciaKm: dist, routes: routeIds });
    }
  }
  results.sort((a, b) => a.distanciaKm - b.distanciaKm);
  return results;
}

function haversine(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 +
    Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dLon/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}
```

## Patrón: Ruteo Inferido (sin stop_times)

Cuando no hay `stop_times.txt` ni `trips.txt`, inferir rutas por coincidencia semántica de nombres:

```javascript
// Modo 1: Coincidencia de palabras entre route_long_name y stop_name
for (const route of data.routes) {
  const routeWords = route.route_long_name.toLowerCase();
  for (const stop of data.stops) {
    for (const word of routeWords.split(/[\s/]+/)) {
      if (word.length > 3 && stop.stop_name.toLowerCase().includes(word)) {
        stopRoutes[stop.stop_id].add(route.route_id);
      }
    }
  }
}

// Modo 2: Fallback — paradas céntricas reciben rutas base
const centralStops = stops.filter(s =>
  s.stop_name.includes('Sol') || s.stop_name.includes('Gran Via') || ...);
```

## Patrón: Múltiples Fuentes de Datos

### 1. Cache simulado (JSON embebido)
```javascript
function cargarDesdeCache(cacheData, operador, ciudad) {
  // cacheData: { routes, stops, stop_times?, trips?, shapes?, _meta }
  construirIndiceStopRoutes(cacheData);
  guardarEstado(operador, ciudad);
  persistirEnLocalStorage(ciudad, operador, data);
}
```

### 2. ZIP subido por usuario
```javascript
async function cargarDesdeZip(file, operador, ciudad) {
  const zip = await JSZip.loadAsync(file);
  const stops = parsearCSV(await leerCSVZip(zip, 'stops.txt'));
  const routes = parsearCSV(await leerCSVZip(zip, 'routes.txt'));
  const trips = parsearCSV(await leerCSVZip(zip, 'trips.txt').catch(()=>''));
  const stopTimes = parsearCSV(await leerCSVZip(zip, 'stop_times.txt').catch(()=>''));
  // Construir indice stop→routes via trips+stopTimes
  // Cargar en estado y cachear en localStorage
}
```

### 3. Proxy servidor (para CORS)
```javascript
// server.mjs
if (req.url.startsWith('/gtfs-download') && req.method === 'POST') {
  const { url } = JSON.parse(body);
  https.get(url, { headers: { 'User-Agent': 'App/1.0' } }, (proxyRes) => {
    const chunks = [];
    proxyRes.on('data', chunk => chunks.push(chunk));
    proxyRes.on('end', () => {
      res.end(Buffer.concat(chunks)); // Streamear ZIP al cliente
    });
  });
}
```

## Patrón: Integración con Mapa Leaflet

```javascript
const iconoParada = L.divIcon({
  html: '<div style="width:10px;height:10px;background:#a855f7;border:2px solid #fff;border-radius:50%;box-shadow:0 1px 4px rgba(0,0,0,0.3)"></div>',
  iconSize: [10, 10], iconAnchor: [5, 5], className: ''
});

for (const item of stopsNear) {
  L.marker([item.stop.stop_lat, item.stop.stop_lon], { icon: iconoParada })
    .bindPopup(`${item.stop.stop_name} (${item.distanciaKm.toFixed(2)} km)<br>${item.routes.length} rutas`)
    .addTo(capaParadas);
}
```

## Patrón: Integración con PDF (jsPDF)

Sección en informes PDF con:
- Tabla de paradas cercanas (nombre, distancia, líneas que sirven)
- Líneas destacadas con paradas que cubren
- Operador, fuente de datos y modo predominante

```javascript
if (gtfsData && gtfsData.totalStops > 0) {
  // Tabla con autoTable: cabecera morada (#a855f7)
  // Columnas: Parada | Distancia | Lineas
  // Max 12 paradas, 10 lineas destacadas
}
```

## Patrón: Exportación GeoJSON

```javascript
function exportarParadasGeoJSON() {
  const features = stops.map(s => ({
    type: 'Feature',
    geometry: { type: 'Point', coordinates: [s.stop_lon, s.stop_lat] },
    properties: { stop_id: s.stop_id, stop_name: s.stop_name }
  }));
  return {
    type: 'FeatureCollection',
    features,
    properties: { fuente: `TimeIneco GTFS — ${operador}`, totalStops: features.length }
  };
}
```

## Patrón: Resumen para UI

```javascript
function getRouteSummary(stopsNear) {
  const rutasUnicas = new Map();
  for (const item of stopsNear) {
    for (const r of item.routes) {
      if (!rutasUnicas.has(r.id)) rutasUnicas.set(r.id, { ...r, paradas: [] });
      rutasUnicas.get(r.id).paradas.push(item.stop.stop_name);
    }
  }
  return {
    operador, ciudad,
    totalStops: stopsNear.length,
    totalRoutes: rutasUnicas.size,
    rutas: [...rutasUnicas.values()],
    modoPredominante, datosFuente
  };
}
```

## CSV Parser (con soporte de comillas)

```javascript
function parsearCSV(text) {
  const lines = text.trim().split('\n');
  if (lines.length < 2) return [];
  const headers = lines[0].split(',').map(h => h.trim());
  const result = [];
  for (let i = 1; i < lines.length; i++) {
    const values = parsearLineaCSV(lines[i]);
    if (values.length !== headers.length) continue;
    const row = {};
    for (let j = 0; j < headers.length; j++) row[headers[j]] = values[j] || '';
    result.push(row);
  }
  return result;
}

function parsearLineaCSV(line) {
  const result = []; let current = ''; let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    if (line[i] === '"') inQuotes = !inQuotes;
    else if (line[i] === ',' && !inQuotes) { result.push(current.trim()); current = ''; }
    else current += line[i];
  }
  result.push(current.trim());
  return result;
}
```

## Implementación Recomendada en Hermes

1. Usar `JSZip` (CDN en index.html) para descompresión ZIP del lado cliente
2. Catálogo de operadores como constante JS (con cacheable flag)
3. Motor GTFS: `gtfs-engine.js` con estado global, findStopsNear, getRouteSummary
4. Panel NAP: `nap.js` como facade de UI con manejo de eventos delegados
5. Mapa: marcadores Leaflet con divIcon y popups informativos
6. PDF: jsPDF + autoTable, colores #a855f7 para cabeceras GTFS
7. Cache en localStorage con prefijo `timeineco_gtfs_`
8. Evento `gtfs:loaded` para sincronizar carga de GTFS con mapa

## Scripts del skill

- `scripts/server-gtfs.py` — Servidor mínimo con /api/zips para auto-carga de ZIPs. `python server-gtfs.py` desde la raiz del proyecto.

## Patrón: Auto-carga de ZIPs desde servidor local (v3.0)

**NUEVO en 2026-06-23:** En vez de arrastrar ZIPs manualmente, el visor se conecta a un servidor mínimo que lista los ZIPs disponibles en `data/` y los carga automáticamente.

### Servidor mínimo (server.py)

```python
# visor/server.py — servidor mínimo HTTP con /api/zips
import http.server, json, os
from pathlib import Path

class GTFSServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/zips':
            self.serve_zips_list()
            return
        super().do_GET()
    
    def serve_zips_list(self):
        zips = []
        for root, dirs, files in os.walk(DATA_DIR):
            for f in files:
                if f.endswith('.zip'):
                    full_path = Path(root) / f
                    rel_path = full_path.relative_to(BASE_DIR)
                    zips.append({
                        "name": f, "path": str(rel_path).replace("\\", "/"),
                        "size": full_path.stat().st_size,
                        "size_human": f"{full_path.stat().st_size / 1024 / 1024:.1f} MB"
                    })
        zips.sort(key=lambda x: x["name"])
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(zips, indent=2).encode())
```

### Auto-carga en el cliente

```javascript
async function autoLoadZips() {
    let zipsList = [];
    try { const resp = await fetch('/api/zips'); if (resp.ok) zipsList = await resp.json(); } catch (e) {}
    if (zipsList.length === 0) return;
    
    const MAX_ZIPS = 25;
    const toLoad = zipsList.slice(0, MAX_ZIPS);
    for (const zf of toLoad) {
        const resp = await fetch('/' + zf.path);
        const blob = await resp.blob();
        const zip = await JSZip.loadAsync(blob);
        await processGTFS(zip, zf.name);
    }
}
```

### Launcher para Windows (.bat)

```bat
@echo off
chcp 65001 >nul
python --version >nul 2>&1 || (echo [ERROR] Python no encontrado & pause & exit /b 1)
cd visor
python server.py
```

### Patrón: Panel de horarios desplegable

Al hacer clic en una parada → panel deslizante desde abajo con rutas y horarios.

```javascript
function showSchedulePanel(stop) {
    const routesData = stop.routes.map(rid => allRoutes[rid]).filter(Boolean);
    // Filtros de ruta como botones clickeables
    // Cards expandibles por ruta con tabla de horarios
    const panel = document.getElementById('schedulePanel');
    panel.innerHTML = htmlContent;
    panel.classList.add('open');
}
```

CSS: `transform: translateY(100%)` → `.open { transform: translateY(0); }` con `transition: 0.3s ease`

## Pitfalls

- **Ficheros grandes** (>15 MB descomprimidos) pueden tardar varios segundos — el parsing ocurre en el hilo principal
- **stop_times masivo** — limitar a 100.000 registros maximo (o usar Web Worker)
- **stop_times sin trips** — si tienes stop_times pero no trips, no puedes enlazar paradas a rutas
- **Ruteo inferido impreciso** — la coincidencia semantica de nombres es heuristica y puede fallar
- **localStorage lleno** — datos GTFS grandes (>5 MB) pueden exceder el limite (~5-10 MB)
- **JSZip no disponible** — asegurarse de cargar la CDN ANTES del modulo principal
- **CORS en descargas GTFS** — la mayoria de feeds publicos no permiten CORS; usar proxy servidor
- **Coordenadas de paradas** — stop_times no lleva coordenadas; siempre referenciar a stops.txt
- **Dedup de paradas** — al filtrar por proximidad, agrupar paradas a menos de ~100m para no saturar el mapa
- **Encoding corrupto** — detectar caracteres U+FFFD y fallback a Windows-1252
- **calendar_dates sin calendar.txt** — algunos feeds usan solo calendar_dates, hay que soportarlo
- **calendar_dates sin calendar.txt** — algunos feeds usan solo calendar_dates, hay que soportarlo

## Pitfall CRÍTICO: Embebido de JSZip inline

**NUNCA** embebas JSZip como `var jszip = 'contenido';` dentro de un `<script>` tag. El contenido de JSZip contiene comillas y caracteres que rompen el string y el HTML.

**MÉTODO CORRECTO:** Insertar JSZip como un `<script>` inline independiente ANTES del script principal:

```html
<script>/* JSZip v3.10.1 minified content here */</script>
<script>
// Tu código del visor que usa JSZip
</script>
```

**MÉTODO INCORRECTO (roto):**
```html
<script>var jszip = '...contenido JSZip...';</script>
```

**Verificación post-embebido:**
1. `document.querySelectorAll('script').length` debe ser 3 (Leaflet CDN + JSZip inline + visor)
2. `typeof JSZip !== 'undefined'` debe ser `true`
3. `typeof window.initMap !== 'undefined'` debe ser `true`
4. Si `initMap` es `undefined`, el script del visor NO se ejecutó — revisa cierres `</script>`

**Patrón de fallo conocido:** Si al hacer un `replace` en el HTML se pierden los cierres `</script>`, `</body>`, `</html>`, el navegador no renderiza el mapa. Siempre verificar que el HTML tiene los 3 cierres.

## Pitfall: Script inline no se ejecuta

Si un `<script>` inline tiene funciones `async`/`await`, `eval()` y `new Function()` fallan con "Unexpected identifier". Esto NO significa que el script tenga error de sintaxis — el navegador ejecuta scripts inline con async/await correctamente. Para depurar, verificar `typeof window.initMap` en la consola del navegador (no usar `eval`).

## Patrón: Visor con Mapa Leaflet Interactivo (v2.0)

**NUEVO en 2026-06-23:** El usuario quiere un visor donde se pueda **elegir un punto desde un mapa**, ver un **círculo de radio visual**, y que las paradas se muestren en el mapa con **colores por modo de transporte**. No basta con una lista de texto.

### Arquitectura del visor con mapa

```
┌──────────────────────────────────────────────────┐
│  Header oscuro                                   │
├──────────┬───────────────────────────────────────┤
│ Sidebar  │  Mapa Leaflet (CARTO light)           │
│          │                                       │
│ Geocodif.│  [click → marcador + círculo radio]   │
│ (Nominat.)│                                       │
│          │  Marcadores paradas: color por modo   │
│ Carga    │                                       │
│ GTFS ZIP │                                       │
│          │  Popup con info de rutas              │
│          │                                       │
│ Radio    │                                       │
│ slider   │                                       │
│          │                                       │
│ Stats    │                                       │
│ (KPIs)   │                                       │
│          │                                       │
│ Lista    │                                       │
│ paradas  │                                       │
└──────────┴───────────────────────────────────────┘
```

### Colores por modo de transporte

```javascript
const MODE_COLORS = {
    '3': '#2563eb',    // Autobús — azul
    '0': '#7c3aed',    // Tranvía — púrpura
    '1': '#dc2626',    // Metro — rojo
    '2': '#dc2626',    // Subterráneo — rojo
    '4': '#16a34a',    // Ferrocarril — verde
    '5': '#ea580c',    // Funicular — naranja
    '6': '#0891b2',    // Barco — cyan
    '7': '#a855f7',    // Teleférico — violeta
    '11': '#0d9488',   // Tren ligero — teal
    '12': '#2563eb'    // Exprés — azul
};
```

### Marcador de usuario con círculo de radio

```javascript
function updateUserMarker(lat, lon, radius) {
    const userIcon = L.divIcon({
        html: '<div style="width:14px;height:14px;background:#2563eb;border:3px solid white;border-radius:50%;box-shadow:0 2px 6px rgba(0,0,0,0.3)"></div>',
        iconSize: [14, 14], iconAnchor: [7, 7], className: ''
    });
    userMarker = L.marker([lat, lon], { icon }).addTo(map);
    searchCircle = L.circle([lat, lon], {
        radius: radius, color: '#2563eb', fillColor: '#2563eb',
        fillOpacity: 0.08, weight: 2, dashArray: '5,5'
    }).addTo(map);
}
```

### Click en mapa → buscar paradas

```javascript
map.on('click', function(e) {
    currentLat = e.latlng.lat;
    currentLon = e.latlng.lng;
    updateUserMarker(currentLat, currentLon);
    buscarParadas();
});
```

### Geocodificación con Nominatim + dropdown

```javascript
async function geocode(query) {
    const resp = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&countrycodes=es`,
        { headers: { 'User-Agent': 'GTFSSpain/1.0' } }
    );
    const data = await resp.json();
    // Mostrar dropdown de 5 resultados, cada uno clickeable
}
```

### Colores de paradas según modo dominante

```javascript
const routeTypes = routeIds.map(rid => allRoutes[rid]).filter(Boolean).map(r => r.type);
const dominantType = routeTypes.length > 0 ? routeTypes[0] : '3';
const color = MODE_COLORS[dominantType] || '#2563eb';

const icon = L.divIcon({
    html: `<div style="width:8px;height:8px;background:${color};border:2px solid white;border-radius:50%"></div>`,
    iconSize: [8, 8], iconAnchor: [4, 4], className: ''
});
```

### UI Requirements

- **Mapa ocupa la mayor parte** — sidebar lateral estrecho (~380px)
- **Sidebar con scroll** — búsqueda arriba, resultados abajo
- **Radio visual** — círculo se actualiza en tiempo real con slider
- **Popups informativos** — clic en parada o ruta
- **KPIs en sidebar** — paradas, rutas, modos en grid 3 columnas
- **Botones rápidos de ciudades** — Madrid, Barcelona, Sevilla, Valencia, POI
- **Carga de ZIPs con barra de progreso** — drag & drop o click

### Estructura

```
visor/
└── index.html          # Todo autocontenido (Leaflet CDN + JSZip inline)
```

### Notas técnicas

- **Leaflet CSS/JS por CDN** — funciona en cualquier navegador moderno
- **JSZip embebido inline** — para funcionamiento 100% offline
- **Nominatim rate limit** — 1 req/segundo, usar debounce
- **CARTO light tiles** — basemap con labels
- **preferCanvas: true** — mejor rendimiento con muchos marcadores

## Referencias

- `references/nap-api-v2.md` — API oficial del Punto de Acceso Nacional de transporte (España)
- `references/nap-volumen-real.md` — Volumen real de datos NAP: 161 datasets, 662 MB, 2M viajes (NUEVO 2026-06-23)
- `references/timeineco-gtfs-integration.md` — Implementación completa en TimeIneco v0.7
- `references/tmb-barcelona-gtfs-sources.md` — Fuentes GTFS TMB Barcelona y URLs probadas
- `references/visor-leaflet-pattern.md` — Patrón de visor con mapa Leaflet interactivo (NUEVO)

## Patrones relacionados

- **`routing-isochrones` > GBFS** — Catálogo de 68 sistemas de bicicletas compartidas en España con feeds GBFS públicos. Para bicis en vez de transporte público.
- **`routing-isochrones` > GBFS** — Catálogo de 68 sistemas de bicicletas compartidas en España con feeds GBFS públicos. Para bicis en vez de transporte público. Repo: `github.com/Ntizar/GBFSSpain`.
- **`nap-data-pipeline`** — Pipeline de descarga y actualización de datos NAP/GTFS desde la API de transportes.gob.es.

## GBFS v3.0 Parsing

**Nuevo 2026-06-25:** GBFS v3.0 tiene diferencias estructurales importantes con v2.x. Ver `references/gbfs-v3-parsing.md` para:
- Discovery feeds en `data.data.feeds` (no `data.feeds`)
- `num_vehicles_available` en vez de `num_bikes_available`
- `name` como array `[{text, language}]` (no string)
- Booleanos vs enteros para `is_installed`/`is_renting`
- Patrones de health check por plataforma

## GTFS Sintético Realista (generación programática)

Cuando no se puede descargar un GTFS real, generar uno sintético con datos realistas:

**Script de referencia:** `scripts/generate-gtfs-synthetic.py` (ver skill `timeineco` sección GTFS Multi-Ciudad)

**Características del GTFS sintético:**
- Paradas con nombres reales de la ciudad (centros, barrios, estaciones)
- Rutas basadas en líneas reales del operador
- Coordenadas geográficas reales (lat/lng de la ciudad)
- Shapes con interpolación entre paradas
- Horarios con intervalos realistas (2-5 min entre paradas)
- Trips de ida y vuelta por cada ruta
- Calendario weekday/saturday/sunday

**Estructura mínima necesaria para búsqueda de paradas:**
- `routes[]` + `stops[]` + `route_stops{}` → suficiente para `findStopsNear()`
- `trips[]` + `stop_times[]` → necesario para isocronas basadas en GTFS (BFS)
- `shapes[]` → necesario para visualizar trazados en mapa

**Pitfall:** Un GTFS sintético con solo `stops[]` y `route_stops{}` funciona para búsqueda de paradas cercanas pero NO para simulación de isocronas basadas en rutas GTFS (motor BFS necesita `stop_times[]` y `trips[]`).

## GTFS Pre-caching en servidor (patrón Time v2.0)

**Nuevo 2026-06-25:** Cuando se dispone de GTFS raw (ZIPs de NAP), crear un cache compacto JSON en el servidor que el frontend cargue automáticamente sin upload manual.

### Flujo

```
GTFS raw (ZIP de NAP)
  → Script Python pre-procesador (extrae stops, routes, trips, stop_times)
  → JSON compacto por ciudad (data/gtfs-cache/{ciudad}.json)
  → Endpoint servidor: /gtfs-cache/:city
  → Frontend: auto-detecta ciudad → fetch JSON →Motor GTFS
```

### Script pre-procesador Python

```python
# scripts/procesar-gtfs-cache.py
import json, csv, zipfile, io, sys, os

def procesar_gtfs(zip_path, city_name):
    data = {'stops': [], 'routes': [], 'trips': [], 'stop_times': [], '_meta': {}}
    with zipfile.ZipFile(zip_path) as z:
        # stops.txt
        with z.open('stops.txt') as f:
            reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8-sig'))
            for row in reader:
                data['stops'].append({
                    'stop_id': row['stop_id'],
                    'stop_name': row['stop_name'],
                    'stop_lat': float(row['stop_lat']),
                    'stop_lon': float(row['stop_lon'])
                })
        # routes.txt
        with z.open('routes.txt') as f:
            reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8-sig'))
            for row in reader:
                data['routes'].append({
                    'route_id': row['route_id'],
                    'route_short_name': row.get('route_short_name', ''),
                    'route_long_name': row.get('route_long_name', ''),
                    'route_type': row.get('route_type', '3')
                })
        # trips.txt (opcional)
        if 'trips.txt' in z.namelist():
            with z.open('trips.txt') as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8-sig'))
                for row in reader:
                    data['trips'].append({
                        'trip_id': row['trip_id'],
                        'route_id': row['route_id']
                    })
        # stop_times.txt (opcional, limitar a 100k)
        if 'stop_times.txt' in z.namelist():
            with z.open('stop_times.txt') as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8-sig'))
                for i, row in enumerate(reader):
                    if i >= 100000: break
                    data['stop_times'].append({
                        'trip_id': row['trip_id'],
                        'stop_id': row['stop_id'],
                        'departure_time': row.get('departure_time', '')
                    })

    data['_meta'] = {
        'city': city_name,
        'stops_count': len(data['stops']),
        'routes_count': len(data['routes']),
        'trips_count': len(data['trips']),
        'stop_times_count': len(data['stop_times'])
    }
    return data
```

### Endpoint servidor (server.mjs)

```javascript
// /gtfs-cache/list → lista ciudades disponibles
app.get('/gtfs-cache/list', (req, res) => {
    const cacheDir = path.join(__dirname, 'data', 'gtfs-cache');
    const files = fs.readdirSync(cacheDir).filter(f => f.endsWith('.json'));
    const cities = files.map(f => {
        const data = JSON.parse(fs.readFileSync(path.join(cacheDir, f)));
        return { city: f.replace('.json', ''), ...data._meta };
    });
    res.json(cities);
});

// /gtfs-cache/:city → devuelve JSON compacto
app.get('/gtfs-cache/:city', (req, res) => {
    const cacheFile = path.join(__dirname, 'data', 'gtfs-cache', `${req.params.city}.json`);
    if (!fs.existsSync(cacheFile)) return res.status(404).json({ error: 'Ciudad no encontrada' });
    res.setHeader('Cache-Control', 'public, max-age=86400'); // 24h cache
    res.json(JSON.parse(fs.readFileSync(cacheFile)));
});
```

### Frontend: auto-carga por ciudad

```javascript
// En nap.js o main.js
async function cargarDesdeServidor(ciudad) {
    try {
        const resp = await fetch(`/gtfs-cache/${ciudad}`);
        if (!resp.ok) return null;
        const data = await resp.json();
        // Alimentar el motor GTFS existente
        construirIndiceStopRoutes(data);
        return data;
    } catch (e) {
        console.warn('Cache GTFS no disponible:', e);
        return null;
    }
}

// Auto-detectar ciudad y cargar
async function autoLoadGTFS(displayName) {
    const ciudad = detectarCiudad(displayName);
    if (!ciudad) return;
    const cacheData = await cargarDesdeServidor(ciudad);
    if (cacheData) {
        console.log(`GTFS pre-cargado: ${cacheData._meta.stops_count} paradas`);
        renderizarPanelGTFS(cacheData);
    }
}
```

### Tamaños típicos

| Ciudad | Paradas | Rutas | Tamaño JSON |
|--------|---------|-------|-------------|
| Bilbao | 533 | 58 | 153 KB |
| Málaga | 1126 | 45 | 315 KB |
| Sevilla | 1038 | 41 | 212 KB |
| Valencia | 1155 | 68 | 336 KB |
| Zaragoza | 996 | 33 | 287 KB |

### Pitfall: no confundir con cache del navegador

Este patrón es un cache **en el servidor** (archivos JSON en `data/gtfs-cache/`), NO el cache del navegador (`localStorage`). El cache del servidor:
- Se actualiza con un script Python (no con upload del usuario)
- Se sirve vía HTTP con cache headers
- Es el mismo para todos los usuarios
- No depende de que el usuario suba un ZIP

El cache del navegador (`localStorage`) sigue siendo útil como fallback offline.

## Pitfall: Catálogo embebido duplicado rompe fallback file://

Cuando un HTML embebe datos inline para funcionar con `file://` (sin servidor), una línea duplicada en la asignación crea un array anidado que rompe el fallback:

**BUG (línea duplicada):**
```javascript
window.GBFS_SYSTEMS_DATA = [
    window.GBFS_SYSTEMS_DATA = [  // ← ESTA LÍNEA ROMPE TODO
  { "name": "Sistema1", ... },
  { "name": "Sistema2", ... }
]
```

**Resultado:** `window.GBFS_SYSTEMS_DATA` es `[[sistema1, sistema2...]]` (anidado), no `[sistema1, sistema2...]`.

**Síntoma:** "No se encontraron sistemas" al abrir con doble clic, pero funciona al servir con `python3 -m http.server`.

**Causa:** La expresión `window.GBFS_SYSTEMS_DATA = [...]` retorna el array, que se envuelve en otro array por el corchete exterior.

**FIX:** Eliminar la línea duplicada. Verificar que solo hay UNA asignación.

**Verificación:** En consola del navegador: `Array.isArray(window.GBFS_SYSTEMS_DATA[0])` debe ser `false` (no `true`).

## Pitfall CRÍTICO: Embebido de JSZip inline

**NUNCA** embebas JSZip como `var jszip = 'contenido';` dentro de un `<script>` tag. El contenido de JSZip contiene comillas y caracteres que rompen el string y el HTML.

**MÉTODO CORRECTO:** Insertar JSZip como un `<script>` inline independiente ANTES del script principal:

```html
<script>/* JSZip v3.10.1 minified content here */</script>
<script>
// Tu código del visor que usa JSZip
</script>
```

**MÉTODO INCORRECTO (roto):**
```html
<script>var jszip = '...contenido JSZip...';</script>
```

**Verificación post-embebido:**
1. `document.querySelectorAll('script').length` debe ser 3 (Leaflet CDN + JSZip inline + visor)
2. `typeof JSZip !== 'undefined'` debe ser `true`
3. `typeof window.initMap !== 'undefined'` debe ser `true`
4. Si `initMap` es `undefined`, el script del visor NO se ejecutó — revisa cierres `</script>`

**Patrón de fallo conocido:** Si al hacer un `replace` en el HTML se pierden los cierres `</script>`, `</body>`, `</html>`, el navegador no renderiza el mapa. Siempre verificar que el HTML tiene los 3 cierres.

## Pitfall: Script inline no se ejecuta

Si un `<script>` inline tiene funciones `async`/`await`, `eval()` y `new Function()` fallan con "Unexpected identifier". Esto NO significa que el script tenga error de sintaxis — el navegador ejecuta scripts inline con async/await correctamente. Para depurar, verificar `typeof window.initMap` en la consola del navegador (no usar `eval`).

## Patrón: Visor con Mapa Leaflet Interactivo (v2.0)

**NUEVO en 2026-06-23:** El usuario quiere un visor donde se pueda **elegir un punto desde un mapa**, ver un **círculo de radio visual**, y que las paradas se muestren en el mapa con **colores por modo de transporte**. No basta con una lista de texto.

### Arquitectura del visor con mapa

```
┌──────────────────────────────────────────────────┐
│  Header oscuro                                   │
├──────────┬───────────────────────────────────────┤
│ Sidebar  │  Mapa Leaflet (CARTO light)           │
│          │                                       │
│ Geocodif.│  [click → marcador + círculo radio]   │
│ (Nominat.)│                                       │
│          │  Marcadores paradas: color por modo   │
│ Carga    │                                       │
│ GTFS ZIP │                                       │
│          │  Popup con info de rutas              │
│          │                                       │
│ Radio    │                                       │
│ slider   │                                       │
│          │                                       │
│ Stats    │                                       │
│ (KPIs)   │                                       │
│          │                                       │
│ Lista    │                                       │
│ paradas  │                                       │
└──────────┴───────────────────────────────────────┘
```

### Colores por modo de transporte

```javascript
const MODE_COLORS = {
    '3': '#2563eb',    // Autobús — azul
    '0': '#7c3aed',    // Tranvía — púrpura
    '1': '#dc2626',    // Metro — rojo
    '2': '#dc2626',    // Subterráneo — rojo
    '4': '#16a34a',    // Ferrocarril — verde
    '5': '#ea580c',    // Funicular — naranja
    '6': '#0891b2',    // Barco — cyan
    '7': '#a855f7',    // Teleférico — violeta
    '11': '#0d9488',   // Tren ligero — teal
    '12': '#2563eb'    // Exprés — azul
};
```

### Marcador de usuario con círculo de radio

```javascript
function updateUserMarker(lat, lon, radius) {
    const userIcon = L.divIcon({
        html: '<div style="width:14px;height:14px;background:#2563eb;border:3px solid white;border-radius:50%;box-shadow:0 2px 6px rgba(0,0,0,0.3)"></div>',
        iconSize: [14, 14], iconAnchor: [7, 7], className: ''
    });
    userMarker = L.marker([lat, lon], { icon }).addTo(map);
    searchCircle = L.circle([lat, lon], {
        radius: radius, color: '#2563eb', fillColor: '#2563eb',
        fillOpacity: 0.08, weight: 2, dashArray: '5,5'
    }).addTo(map);
}
```

### Click en mapa → buscar paradas

```javascript
map.on('click', function(e) {
    currentLat = e.latlng.lat;
    currentLon = e.latlng.lng;
    updateUserMarker(currentLat, currentLon);
    buscarParadas();
});
```

### Geocodificación con Nominatim + dropdown

```javascript
async function geocode(query) {
    const resp = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&countrycodes=es`,
        { headers: { 'User-Agent': 'GTFSSpain/1.0' } }
    );
    const data = await resp.json();
    // Mostrar dropdown de 5 resultados, cada uno clickeable
}
```

### Colores de paradas según modo dominante

```javascript
const routeTypes = routeIds.map(rid => allRoutes[rid]).filter(Boolean).map(r => r.type);
const dominantType = routeTypes.length > 0 ? routeTypes[0] : '3';
const color = MODE_COLORS[dominantType] || '#2563eb';

const icon = L.divIcon({
    html: `<div style="width:8px;height:8px;background:${color};border:2px solid white;border-radius:50%"></div>`,
    iconSize: [8, 8], iconAnchor: [4, 4], className: ''
});
```

### UI Requirements

- **Mapa ocupa la mayor parte** — sidebar lateral estrecho (~380px)
- **Sidebar con scroll** — búsqueda arriba, resultados abajo
- **Radio visual** — círculo se actualiza en tiempo real con slider
- **Popups informativos** — clic en parada o ruta
- **KPIs en sidebar** — paradas, rutas, modos en grid 3 columnas
- **Botones rápidos de ciudades** — Madrid, Barcelona, Sevilla, Valencia, POI
- **Carga de ZIPs con barra de progreso** — drag & drop o click

### Estructura

```
visor/
└── index.html          # Todo autocontenido (Leaflet CDN + JSZip inline)
```

### Notas técnicas

- **Leaflet CSS/JS por CDN** — funciona en cualquier navegador moderno
- **JSZip embebido inline** — para funcionamiento 100% offline
- **Nominatim rate limit** — 1 req/segundo, usar debounce
- **CARTO light tiles** — basemap con labels
- **preferCanvas: true** — mejor rendimiento con muchos marcadores

## Referencias

- `references/nap-api-v2.md` — API oficial del Punto de Acceso Nacional de transporte (España)
- `references/nap-volumen-real.md` — Volumen real de datos NAP: 161 datasets, 662 MB, 2M viajes (NUEVO 2026-06-23)
- `references/timeineco-gtfs-integration.md` — Implementación completa en TimeIneco v0.7
- `references/tmb-barcelona-gtfs-sources.md` — Fuentes GTFS TMB Barcelona y URLs probadas
- `references/visor-leaflet-pattern.md` — Patrón de visor con mapa Leaflet interactivo (NUEVO)

## Patrones relacionados

- **`routing-isochrones` > GBFS** — Catálogo de 68 sistemas de bicicletas compartidas en España con feeds GBFS públicos. Para bicis en vez de transporte público.
- **`routing-isochrones` > GBFS** — Catálogo de 68 sistemas de bicicletas compartidas en España con feeds GBFS públicos. Para bicis en vez de transporte público. Repo: `github.com/Ntizar/GBFSSpain`.
- **`nap-data-pipeline`** — Pipeline de descarga y actualización de datos NAP/GTFS desde la API de transportes.gob.es.