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

## Referencias

- `references/nap-api-v2.md` — API oficial del Punto de Acceso Nacional de transporte (España)
- `references/timeineco-gtfs-integration.md` — Implementación completa en TimeIneco v0.7