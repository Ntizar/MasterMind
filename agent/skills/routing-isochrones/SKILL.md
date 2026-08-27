---
name: routing-isochrones
description: "Patrones para construir herramientas de isocronas y routing: OpenRouteService, OpenTripPlanner, GTFS/NAP, geocodificación Nominatim. Arquitectura de plugins para motores de routing intercambiables."
version: "1.0.0"
author: David Antizar
tags: [routing, isochrones, gtfs, openrouteservice, opentripplanner, nominatim, leaflet, vanilla-js, mobility]
---

# Routing & Isocronas — Patrón de Herramienta

## Cuándo cargar esta skill

Cuando el usuario pida: isocronas, mapas de accesibilidad, cálculo de rutas, transporte público con horarios, planes de movilidad, "hasta dónde llego en X minutos", routing multi-modal, GTFS, NAP transportes.

## Concepto

Herramienta web que calcula isocronas y rutas de movilidad desde cualquier punto: coche, bicicleta, peatón y transporte público. Pones origen + destino + horario objetivo, obtienes un informe con isocronas y rutas de bus disponibles.

**Arquitectura clave:** Sistema de plugins para motores de routing intercambiables. Cada backend (ORS, OTP, NAP) implementa la misma interfaz.

---

## Patrones de UI (dos variantes)

### Variante A: Punto de interés (simple)
Cuando el usuario quiere "hasta dónde llego desde X" — un solo punto, no formulario de ruta:

```
┌─────────────────────────────────────────────┐
│  Header oscuro (título + subtítulo)          │
├──────────┬──────────────────────────────────┤
│ Sidebar  │  Mapa (CARTO light tiles)        │
│          │                                  │
│ Modo     │  [click en mapa → punto]         │
│ (4 btns) │                                  │
│          │                                  │
│ Tiempo   │                                  │
│ (slider) │                                  │
│          │                                  │
│ Dirección│                                  │
│ (input)  │                                  │
│          │                                  │
│ Calcular │                                  │
│          │                                  │
│ PDF      │                                  │
│          │                                  │
│ Resultados│                                │
│ (KPIs)   │                                  │
└──────────┴──────────────────────────────────┘
```

- **4 botones de modo:** coche 🚗, bici 🚲, andando 🚶, bus 🚌
- **Slider de tiempo:** 5-60 min con presets rápidos (10, 15, 30, 45, 60)
- **Input de dirección:** con debounce 800ms + click en mapa para poner punto
- **Sidebar limpia:** fondo blanco, bordes sutiles, sin gradientes
- **Mapa:** CARTO light tiles, Canvas renderer

### Variante B: Origen + Destino (completa)
Para planes de movilidad laboral con horarios GTFS:

```
Origen (casa) + Destino (oficina) + Horario → Isocronas + Rutas bus
```

---

## Diseño visual — Reglas críticas

**David odia el "look de IA" (dark, neón, glass, gradientes).**

Para herramientas de movilidad:
- ✅ **Header oscuro** (`#1a1a2e`) + **sidebar blanca** + **mapa CARTO light**
- ✅ **Botones con bordes sutiles**, colores por modo (azul=bici, naranja=coche, verde=andando, púrpura=bus)
- ✅ **Tipografía system font** (-apple-system, BlinkMacSystemFont, Segoe UI)
- ✅ **KPIs en grid 2x2** con fondo gris claro
- ❌ **NUNCA** gradientes Aurora, glassmorphism, efectos neón
- ❌ **NUNCA** fondo oscuro en la app completa
- ❌ **NUNCA** decoraciones innecesarias

**CSS base:** `background: #f8f9fa`, `color: #1a1a2e`, `font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

---

## Arquitectura de Plugins

```javascript
// js/plugins.js
const PLUGINS = {
    ors: ORSRouter,    // OpenRouteService (coche/bici/peatón)
    otp: OTPRouter,    // OpenTripPlanner (transit con transbordos)
    nap: GTFSNapRouter // NAP/GTFS España (horarios reales)
};

// Registrar nuevo plugin
registerPlugin('name', {
    resolve(origin, dest, mode) { ... },
    getIsochrones(point, time, mode) { ... }
});
```

**Para añadir un nuevo motor:**
1. Crear `js/routing-{name}.js`
2. Implementar `resolve()` y `getIsochrones()`
3. Registrar: `registerPlugin('name', router)`

### Interfaz IRouter

```javascript
class IRouter {
    // Calcular ruta entre origen y destino
    async resolve(origin, dest, mode) {
        // origin: {lat, lng, name}
        // dest: {lat, lng, name}
        // mode: 'car' | 'bike' | 'walk' | 'transit'
        // Returns: {distance, duration, geometry, steps, mode}
    }

    // Calcular isocrona desde un punto
    async getIsochrones(point, time, mode) {
        // point: {lat, lng}
        // time: segundos
        // Returns: {geojson, area, success}
        //   geojson: FeatureCollection (Polygon)
        //   area: km² (number)
        //   success: boolean
        //   error: string (solo si success=false)
    }
}
```

**⚠️ Shape consistente:** El return de `getIsochrones` debe tener SIEMPRE la misma forma. Si el backend real falla o no hay API key, devolver `{ geojson: simulatedData, area: estimatedArea, success: true }` en vez de tirar error.

---

## Stack tecnológico

| Componente | Tecnología | Justificación |
|---|---|---|
| Mapa | Leaflet (Canvas renderer) | Ligero, sin framework, ya probado |
| Isocronas | OpenRouteService API | Gratis, 3 modos, desnivel incluido |
| Routing TP | OpenTripPlanner | Transbordos reales, GTFS |
| Geocodificación | Nominatim (OSM) | Gratis, no requiere key |
| PDF | jsPDF + autoTable + html2canvas | Generación cliente con captura de mapa |
| CSS | Simple/clean (NO Aurora glass) | Header oscuro + sidebar blanca + CARTO light |
| JS | Vanilla ES modules | Sin bundler, un solo HTML |

---

## OpenRouteService (ORS) v2

**CRITICAL:** The v2 API changed from the v1 format shown in old docs. The correct endpoint and body format are below.

### Endpoint (server-side proxy)

**DO NOT call ORS directly from the browser** — the API key would be exposed. Always use a server-side proxy:

```javascript
// server.mjs — proxy endpoint
if (req.method === 'POST' && req.url.startsWith('/isochrone')) {
  const ORS_KEY = process.env.ORS_API_KEY;
  if (!ORS_KEY) {
    res.writeHead(400, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'ORS_API_KEY no configurada', fallback: true }));
    return;
  }
  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', () => {
    const { profile, locations, range } = JSON.parse(body);
    const bodyObj = { locations: [locations], range, range_type: 'time', attributes: ['area'] };
    // ⚠️ NO incluir 'interval' para rango único — ORS lo rechaza con 400
    if (range.length > 1) bodyObj.interval = range[0];
    const options = {
      hostname: 'api.openrouteservice.org',
      path: `/v2/isochrones/${profile}`,
      method: 'POST',
      headers: {
        'Authorization': ORS_KEY,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json, application/geo+json'
      }
    };
    const proxyReq = https.request(options, (proxyRes) => {
      let data = '';
      proxyRes.on('data', chunk => data += chunk);
      proxyRes.on('end', () => { res.writeHead(proxyRes.statusCode, { 'Content-Type': 'application/json' }); res.end(data); });
    });
    proxyReq.on('error', (err) => { res.writeHead(502); res.end(JSON.stringify({ error: err.message, fallback: true })); });
    proxyReq.write(JSON.stringify(bodyObj));
    proxyReq.end();
  });
  return;
}
```

### Request body (correct v2 format)

```
POST https://api.openrouteservice.org/v2/isochrones/{profile}
Headers:
  Authorization: {api_key}
  Content-Type: application/json; charset=utf-8
  Accept: application/json, application/geo+json
Body: {
  "locations": [[lng, lat]],     // single pair, NOT [{lat, lng}]
  "range": [900],                // seconds (15 min)
  "range_type": "time",
  "attributes": ["area"]         // returns area in m²
  // DO NOT include "interval" for single-range (see quirk below)
}
```

### ⚠️ ORS v2 API quirks

1. **`interval` quirk (CRITICAL):** Adding `"interval": [900]` with a single-range request causes ORS to respond `400: Parameter 'interval' has incorrect value or format.` Never include `interval` for single-range requests. Only use it when auto-generating multiple ranges (e.g. range: [900], interval: 300).

2. **Error response format:** ORS returns errors as string or object. Parse defensively:
   ```javascript
   const errMsg = typeof errData.error === 'string' ? errData.error
     : errData.error?.message || errData.error?.error || resp.statusText;
   ```

3. **Rate limiting (429):** Free ORS tier ≈ 1 req/s. With 12 isochrones (4×3), parallel `Promise.all()` triggers 429. Solution: stagger sequentially with 300-1000ms delay between each request.

4. **"Access to this API has been disallowed":** The key exists but lacks isochrone permissions. Free keys may need upgrade. Health check should validate beyond existence.

5. **No bus profile:** Use `driving-car` as approximation.

6. **Area from ORS:** `features[0].properties.area` is in **m²**. Divide by 1,000,000 for km².

### Pattern: Async fallback con stagger

```javascript
const ORS_PROFILES = {
  car: 'driving-car', bike: 'cycling-regular',
  foot: 'foot-walking', bus: 'driving-car'
};

export async function calcularIsocronaAsync(lng, lat, modo, minutos) {
  try { // Intentar ORS real
    const resp = await fetch('/isochrone', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile: ORS_PROFILES[modo], locations: [lng, lat], range: [minutos * 60] }),
      signal: AbortSignal.timeout(15000)
    });
    if (!resp.ok) {
      const errData = await resp.json().catch(() => ({}));
      if (errData.fallback) throw new Error('ORS no disponible (sin key)');
      const errMsg = typeof errData.error === 'string' ? errData.error
        : errData.error?.message || errData.error?.error || resp.statusText;
      throw new Error(`ORS HTTP ${resp.status}: ${errMsg}`);
    }
    const data = await resp.json();
    const areaKm2 = (data.features?.[0]?.properties?.area || 0) / 1_000_000;
    return { geojson: data, areaKm2, real: true };
  } catch (err) {
    console.warn(`⚠️ ORS fallback ${modo} ${minutos}min: ${err.message}`);
  }
  return { ...calcularIsocronaSim(lng, lat, modo, minutos), real: false };
}

export async function calcularTodasAsync(punto, modos, tiempos) {
  const resultados = [];
  for (const modo of modos) {
    for (const min of tiempos) {
      const r = await calcularIsocronaAsync(punto.lng, punto.lat, modo, min).catch(
        e => ({ modo, minutos: min, geojson: null, areaKm2: 0, error: e.message, real: false })
      );
      resultados.push({ modo, minutos: min, ...r });
      await new Promise(r => setTimeout(r, 300)); // stagger
    }
  }
  return resultados;
}
```

### Health check con validación de key

```javascript
// server.mjs /healthz
res.end(JSON.stringify({
  status: 'ready', uptime: process.uptime(),
  checks: { ors_api: typeof ORS_KEY === 'string' && ORS_KEY.length > 20 }
}));
// ↑ Más robusto que !!ORS_KEY (detecta strings vacíos)
```

### Simulación de isocronas (fallback)

Generar círculos irregulares con jitter cuando ORS no está disponible:

```javascript
function calcularIsocronaSim(lng, lat, modo, minutos) {
  const m = CONFIG.MODOS[modo];
  const radioM = (m.speedKmh / 3.6) * minutos * 60;
  const PTS = 48, coords = [];
  for (let i = 0; i <= PTS; i++) {
    const ang = (i / PTS) * 2 * Math.PI;
    const jitter = 1 - (0.12 * (Math.sin(i * 7.3) * 0.5 + 0.5));
    const r = radioM * jitter;
    const dLat = (r * Math.cos(ang)) / 111320;
    const dLng = (r * Math.sin(ang)) / (111320 * Math.cos(lat * Math.PI / 180));
    coords.push([lng + dLng, lat + dLat]);
  }
  return {
    geojson: { type: 'FeatureCollection', features: [{
      type: 'Feature', geometry: { type: 'Polygon', coordinates: [coords] },
      properties: { modo, minutos, simulado: true }
    }]},
    areaKm2: calcularAreaPoligonoKm2(coords, lat)
  };
}

function calcularAreaPoligonoKm2(coords, refLat) {
  let area = 0; const n = coords.length;
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n;
    area += coords[i][0] * coords[j][1] - coords[j][0] * coords[i][1];
  }
  const cosLat = Math.cos((refLat ?? coords.reduce((s, c) => s + c[1], 0) / n) * Math.PI / 180);
  return Math.abs(area) / 2 * (111.32 * 111.32 * cosLat);
}
```

### Patrón: Wrapper consistente getIsochrone()

**CRÍTICO:** La función `getIsochrone()` DEBE devolver SIEMPRE el mismo shape `{ geojson, area, success }`, tanto si usa la API real como el fallback simulado.

```javascript
// ❌ MAL: devuelve shapes diferentes según el camino
export async function getIsochrone(lng, lat, profile, rangeSeconds) {
  if (!API_KEY) return getSimulatedIsochrone(lng, lat, profile, rangeSeconds);
  // ... fetch ORS ...
  return { geojson: data, area, success: true };
}
// → `computeAllIsochrones` espera `.geojson` y `.area`, pero
//   simulated devuelve el GeoJSON raw → `.geojson` es undefined

// ✅ BIEN: siempre mismo shape
export async function getIsochrone(lng, lat, profile, rangeSeconds) {
  if (!API_KEY) {
    const geojson = getSimulatedIsochrone(lng, lat, profile, rangeSeconds);
    const coords = geojson.features[0].geometry.coordinates[0];
    const area = calculatePolygonAreaKm2(coords, lat);
    return { geojson, area, success: true };
  }
  // ... fetch ORS real ...
  return { geojson: data, area, success: true };
}
```

**Regla de oro:** cualquier wrapper de API externa debe envolver SIEMPRE la respuesta en un shape consistente, independientemente de si la llamada fue real, simulada, o en error.

### Config: evaluación perezosa (getter)

La key de ORS NO debe evaluarse al cargar el módulo, porque si el módulo ES se cachea en el navegador, la key queda congelada en el valor del primer load. Usar un getter:

```javascript
const CONFIG = {
  ORS: {
    get key() {  // ← getter, evaluado CADA VEZ que se accede
      if (typeof window !== 'undefined' && window.__ENV?.ORS_API_KEY) {
        return window.__ENV.ORS_API_KEY;
      }
      return '';
    }
  }
};
```

El servidor inyecta `window.__ENV = { ORS_API_KEY: "..." }` en el HTML antes del módulo. Con el getter, el valor se lee en tiempo de ejecución, no al cargar.

**Endpoint routing:**
```
GET https://api.openrouteservice.org/v2/directions/{o_lng},{o_lat};{d_lng},{d_lat}
Params: ?profile=driving-car
```

**API Key gratis:** https://openrouteservice.org/sign-up (2.000 req/día)

**Desnivel:** ORS ya lo considera internamente:
- `cycling-regular` penaliza subidas
- `cycling-mountain` penaliza más
- `foot-walking` considera pendiente

---

## OpenTripPlanner (OTP)

**Para routing con transbordos reales.**

**Endpoints:**
```
POST /otp/routers/default/plan          — routing general
POST /otp/routers/default/isochrone     — isocronas
POST /otp/routers/default/arriveby      — llegar a hora X
POST /otp/routers/default/departby      — salir a hora X
```

**Docker:**
```bash
docker run -d -p 8080:8080 \
  -v /path/to/config:/opt/otp/config \
  opentripplanner/otp:latest \
  --build
```

**Datos:** Descargar OSM extract de Overpass API + GTFS de cada ciudad.

---

## GTFS + NAP (Transporte Público España)

**NAP es un catálogo de datasets GTFS**, no un motor de routing.

### Flujo completo

```
1. Listar conjuntos GTFS → GET /api/v2/conjunto-dato?regionId=X
2. Filtrar por tipo → solo "Autobús urbano"
3. Descargar fichero GTFS → GET /api/v2/fichero/{id}/descarga
4. Parsear GTFS localmente en JS
5. Calcular paradas cercanas a origen y destino
6. Calcular rutas que conecten ambas zonas
7. Filtrar por horario objetivo (7:30-9:30 / 16:30-18:30)
8. Mostrar resultados
```

### Motor de horarios laborales

```javascript
// Filtrar por horario de llegada al trabajo (7:30-9:30)
const morningArrivals = stopTimes.filter(st => {
    const time = parseTime(st.arrival_time); // "07:45:00" → 7.75 horas
    return time >= 7.5 && time <= 9.5;
});

// Filtrar por horario de salida del trabajo (16:30-18:30)
const eveningDepartures = stopTimes.filter(st => {
    const time = parseTime(st.departure_time);
    return time >= 16.5 && time <= 18.5;
});
```

### Archivos GTFS necesarios

| Archivo | Qué contiene | Uso |
|---|---|---|
| `stops.txt` | Paradas (id, lat, lon, nombre) | Calcular paradas cercanas |
| `routes.txt` | Rutas (id, short_name, agency, type) | Filtrar por tipo |
| `trips.txt` | Viajes (route_id, trip_id, direction_id) | Ida vs vuelta |
| `stop_times.txt` | Horarios por parada | **El más importante** |
| `calendar.txt` | Fechas de servicio | Días laborables |

### Limitación importante

**GTFS no es routing real.** Dice "el bus X llega a la parada Y a las 7:45", pero no calcula transbordos. Para routing real con transbordos se necesita **OpenTripPlanner** o **Valhalla con GTFS**.

### NAP API

- **Base URL:** `https://nap.transportes.gob.es/api/v2`
- **Auth:** API key en header `ApiKey`
- **Endpoint conjuntos:** `GET /api/v2/conjunto-dato`
- **Descarga fichero:** `GET /api/v2/fichero/{id}/descarga`
- **Solo España** — para otros países usar Transitland API

---

## Estructura del proyecto (moderna)

```
project/
├── index.html          # HTML único (frontend)
├── css/
│   └── style.css       # Estilos específicos
├── js/
│   ├── config.js       # Configuración centralizada (velocidades, colores, modos, tiempos, opacidad)
│   ├── utils.js        # geocode(), reverseGeocode(), formatNum(), formatKm2(), debounce
│   ├── map.js          # Leaflet Canvas + marcadores + renderizado isocronas + capturarMapa() para PDF
│   ├── isochrones.js   # Motor async: ORS real con fallback simulación (stagger 300ms)
│   ├── pdf.js          # PDF con jsPDF + autoTable + html2canvas (captura de mapa)
│   ├── shp.js          # Descarga SIG: GeoJSON, CSV, SHP (.shp+.shx+.dbf+.prj empaquetados en ZIP)
│   ├── nap.js          # Catálogo de transporte público: operadores por ciudad detectada
│   ├── clip.js         # Sea clipping: detección de ciudades costeras + preparación para recorte
│   └── main.js         # Orquestador: geocode → isocronas → render → PDF → descargas
├── server.mjs          # Servidor estático + proxy Nominatim + proxy ORS
├── PLAN.md
└── README.md
```

**vs. la versión antigua** (plugin-based con `ors.js`, `gtfs.js`, `plugins.js` separados):
La arquitectura moderna unifica ORS + GTFS en un solo `isochrones.js` con async/await y fallback automático. El sistema de plugins se reemplazó por un patrón de try/catch por request: cada isócrona intenta ORS real, y si falla, usa simulación local. Esto es más simple y robusto que la interfaz IRouter.

---

## Geocodificación Nominatim

```javascript
// Geocodificación directa
const resp = await fetch(
    `${NOMINATIM.baseUrl}/search?format=json&q=${encodeURIComponent(query)}&limit=1`,
    { headers: { 'User-Agent': 'TimeIneco/0.1' } }
);

// Geocodificación inversa
const resp = await fetch(
    `${NOMINATIM.baseUrl}/reverse?format=json&lat=${lat}&lon=${lon}`,
    { headers: { 'User-Agent': 'TimeIneco/0.1' } }
);
```

**Rate limit:** 1 request/segundo. Usar debounce en inputs.

---

## Pitfalls

1. **GTFS no es routing** — solo horarios. Para transbordos reales necesitas OTP o Valhalla con GTFS
2. **NAP solo España** — para otros países necesitas GTFS directo de cada operador o Transitland API
3. **Nominatim rate limit** — 1 req/segundo. Siempre debounce los inputs
4. **ORS API key en frontend** — visible para el usuario. Para producción, usar proxy backend
5. **Leaflet Canvas + interactividad** — eventos de mouse son por bounding box, no por forma exacta. Para polígonos pequeños, usar `tolerance` en `L.canvas({tolerance: 5})`
6. **GTFS stop_times.txt es el archivo más grande** — puede ser 100MB+. Parsear con streaming o filtrar por ruta antes de cargar
7. **ORS wrapper: shape consistente** — `getIsochrone()` debe devolver SIEMPRE `{geojson, area, success}`. Si el fallback simulado devuelve raw GeoJSON (sin wrapper), el consumidor recibe `undefined.geojson` y las isocronas no se renderizan. Ver sección ORS > Patrón de wrapper.
8. **Nominatim geocoding devuelve `lon`, no `lng`** — Nomination usa `lon` para longitud. Si en tu código desestructuras como `{lng}` obtendrás `undefined`. La forma correcta es devolver `lng: parseFloat(data[0].lon)` en el wrapper de geocoding. Este es un gotcha recurrente con OSM/Nominatim.
9. **Config: no evaluar env vars al cargar módulo** — ES modules se cachean por URL en el navegador. Si `CONFIG.ORS.key` se evalúa al cargar el módulo, ese valor queda congelado aunque el servidor inyecte un `window.__ENV` diferente en el HTML. Usar getter para evaluación perezosa (ver sección ORS > Config).
10. **Cache de ES modules en desarrollo** — Los ES modules importados estáticamente se cachean en el navegador POR URL. Cambiar el contenido del archivo en el servidor NO fuerza recarga si la URL es la misma. Soluciones:
    - Añadir `?v=N` a todos los imports: `import { x } from './modulo.js?v=2'` (cascade: el HTML carga `main.js?v=2`, que a su vez importa `./map.js?v=2`, etc.)
    - Configurar el servidor con `Cache-Control: no-cache, no-store, must-revalidate` para JS (no es suficiente solo: el cache ES module es distinto del HTTP cache)
    - Navegar a un dominio COMPLETAMENTE diferente (https://example.com) entre pruebas. `about:blank` no limpia el módulo cache
11. **ORS simulado para desarrollo** — si no hay API key, generar círculos simples como fallback. No confundir con datos reales
12. **ORS `interval` quirk** — NUNCA incluir `interval` en el body cuando se solicita un solo rango. ORS v2 lo rechaza con 400 aunque el valor sea correcto. `interval` solo se usa para generar múltiples rangos automáticamente (ej. range:[900], interval:300 genera isocronas a 300, 600 y 900s)
13. **Stagger sequential > Promise.all** — Con 12 isocronas (4×3), lanzar todas en paralelo con `Promise.all()` provoca 429 Rate Limit en el free tier de ORS (~1 req/s). Usar bucle secuencial con `await delay(300-1000ms)` entre cada request. Aunque tarda más (~3.6s con 300ms stagger), evita los fallos por rate limit
14. **NaN deploy: health check with ORS key validation** — `!!process.env.ORS_API_KEY` devuelve `true` incluso para strings vacíos. Usar `typeof key === 'string' && key.length > 20`. NaN tarda 1-5 min en detectar cambios de GitHub y redeployar. El uptime en healthz confirma si se redeployó
15. **Cache-buster de ES modules** — El script `<script>document.querySelectorAll('script[src*="main.js"]')...</script>` NO funciona para cache-busting porque se ejecuta ANTES de que el `<script type="module">` exista en el DOM. Solución: hardcodear `?v=N` directamente en el src del módulo en el HTML
16. **SHP generation in browser** — No hay librería CDN que genere .shp directamente. Construir el binario manualmente: file header (100B big-endian), record (8B header + Polygon=5 content). Empaquetar .shp+.shx+.dbf+.prj en ZIP via JSZip. Ver session-2026-06-19.md para el patrón completo.
17. **html2canvas for Leaflet map capture** — Las tiles deben permitir CORS (CARTO light_all sí). Usar `useCORS: true, scale: 2` en las opciones. El contenedor del mapa debe estar visible en el viewport antes de capturar.
18. **NAP city detection** — `detectarCiudad()` usa `string.includes()` sobre el `display_name` de Nominatim. Las direcciones largas o con nombres compuestos pueden fallar. Extender el catálogo manualmente para nuevas ciudades.
20. **ES Module import mismatch = failure silencioso** — Si un `import { nombre }` NO coincide exactamente (case-sensitive) con la exportación del módulo destino, ES module falla **sin ningún mensaje de error visible**. No aparece en `window.onerror`, no hay stack trace, no hay 404. El síntoma es que la página carga pero nada funciona — el módulo principal nunca se ejecuta. Debug: verificar cada import contra su export real. Ver `systematic-debugging` → `references/es-module-silent-failure.md`.

---

## Overlap con otros skills

- **`leaflet-canvas-choropleth`** — cubre mapa 2D con Canvas renderer. Este skill usa Leaflet pero se enfoca en routing/isocronas.
- **`geospatial-asset-platform`** — cubre plataforma GIS completa con backend. Este skill es frontend-only, zero backend.
- **`satellite-gis-patterns`** — cubre routing client-side con OpenMapTiles. Este skill cubre isocronas + GTFS + NAP.
- **`frontend-dashboard-patterns`** — cubre patrones de dashboards. Este skill es específico de movilidad/routing.

---

## Referencias

- `references/nap-api.md` — Documentación completa de la API NAP (transportes.gob.es): endpoints, esquemas, tipos de transporte
- `references/config-centralized.md` — Patrón de configuración centralizada para apps multi-API
- `references/ui-patterns.md` — Patrón CSS para UI de herramientas de movilidad: header oscuro + sidebar blanca + CARTO light, botones de modo, slider de tiempo, KPIs, responsive
- `references/browser-es-module-cache.md` — Cache de ES modules en desarrollo: por qué no se refrescan y cómo forzar recarga con `?v=N` en cascade
- `references/session-2026-06-19.md` — TimeIneco sesión: SHP in-browser, html2canvas map capture, NAP city detection, sea clipping
