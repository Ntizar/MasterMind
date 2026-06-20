---
name: isochrone-routing-tools
description: "Análisis completo de cómo construir herramientas de isocronas: motores de routing (ORS, Valhalla, OSRM, GraphHopper, NAP), GTFS/OTP para transporte público, penalización por desnivel en walking/cycling, y arquitecturas recomendadas (MVP cloud vs self-hosted completo)."
version: "2.1.0"
author: David Antizar
tags: [isochrones, routing, gtfs, otp, nap, valhalla, ors, osrm, graphhopper, walking, cycling, elevation, transport]
---

# Isocronas — Arquitectura y Viabilidad

Análisis completo de cómo construir herramientas de isocronas con herramientas open source, comparando motores de routing, niveles de detalle y viabilidad.

## Tabla de Contenidos

1. [Motores de Routing](#1-motores-de-routing) — ORS, Valhalla, OSRM, GraphHopper, NAP
2. [Isocronas vs Routing](#2-isocronas-vs-routing) — Qué es cada uno y cuándo usar
3. [Transporte Público](#3-transporte-público) — GTFS, OTP, NAP
4. [Caminando y Bicicleta con Desnivel](#4-caminando-y-bicicleta-con-desnivel) — Elevation, penalizaciones
5. [Arquitectura Recomendada](#5-arquitectura-recomendada) — Stack mínimo viable
6. [Limitaciones y Pitfalls](#6-limitaciones-y-pitfalls)
7. [Proxy ORS con Node.js](#7-proxy-ors-con-nodejs) — Servidor con API Key oculta

---

## 1. Motores de Routing

### OpenRouteService (ORS)

- **API:** REST, 2.500 req/día gratis
- **Perfiles:** driving-car, foot-walking, cycling-regular, cycling-mountain
- **Isocronas:** SÍ (POST `/v2/isochrones/{lon},{lat}`)
- **Routing:** SÍ (POST `/v2/directions/{mode}`)
- **Desnivel:** NO nativo (usa perfil de elevación de SRTM)
- **Open source:** SÍ (backend: Valhalla/OSRM)
- **Deploy self-hosted:** SÍ (Docker)
- **Ideal para:** MVP rápido, pruebas, uso personal

### Valhalla

- **API:** REST/gRPC
- **Isocronas:** SÍ (`/tarball` y `/time_region`)
- **Desnivel:** SÍ nativo (penalización en walking/cycling)
- **Open source:** SÍ (GitHub: valhalla/valhalla)
- **Deploy self-hosted:** SÍ (Docker, más complejo)
- **Ideal para:** Herramienta completa, self-hosted, con desnivel

### OSRM

- **API:** REST
- **Isocronas:** NO nativo (requiere `osrm-contract` + post-procesado)
- **Desnivel:** NO
- **Open source:** SÍ
- **Deploy self-hosted:** SÍ
- **Ideal para:** Routing rápido, no isocronas

### GraphHopper

- **API:** REST
- **Isocronas:** NO nativo (requiere `elevation` plugin + post-procesado)
- **Desnivel:** SÍ
- **Open source:** SÍ (core open, isocronas en pro)
- **Deploy self-hosted:** SÍ
- **Ideal para:** Routing con elevación

### NAP (Red de Transporte Público)

- **API:** REST (GTFS real-time + static)
- **Isocronas:** NO (routing específico de transporte público)
- **Datos:** GTFS de todas las ciudades españolas
- **Open source:** SÍ (datos GTFS, API REST)
- **Deploy self-hosted:** NO (API pública)
- **Ideal para:** Transporte público en España

---

## 2. Isocronas vs Routing

### Isocrona

- **Qué es:** Área accesible en X tiempo desde un punto
- **Resultado:** Polígono (GeoJSON)
- **Motores:** ORS, Valhalla
- **Uso:** "¿Dónde puedo llegar en 15 min?"

### Routing

- **Qué es:** Ruta entre dos puntos
- **Resultado:** Ruta (GeoJSON polyline) + tiempo + distancia
- **Motores:** ORS, Valhalla, OSRM, GraphHopper
- **Uso:** "¿Cómo llego de A a B?"

### Diferencia clave

Las isocronas son **más costosas computacionalmente** porque requieren explorar múltiples direcciones desde el punto de origen. El routing es más simple (un solo camino).

---

## 3. Transporte Público

### OpenTripPlanner (OTP)

- **API:** REST
- **Isocronas:** SÍ (`/isochrone`)
- **Routing TP:** SÍ (GTFS)
- **Desnivel:** NO (no aplica a TP)
- **Open source:** SÍ
- **Deploy self-hosted:** SÍ (Docker)
- **Datos:** GTFS de cualquier ciudad
- **Ideal para:** Herramienta completa de TP

### NAP API

- **API:** REST (GTFS estático + real-time)
- **Isocronas:** NO
- **Routing TP:** SÍ (específico España)
- **Datos:** GTFS de todas las ciudades españolas
- **Deploy self-hosted:** NO
- **Ideal para:** España, sin self-hosting

### GTFS — Estructura

```
stops.txt      → Paradas/estaciones
routes.txt     → Líneas (bus, metro, tren)
trips.txt      → Viajes individuales
stop_times.txt → Horarios de paso
calendar.txt   → Fechas de servicio
```

### Horarios laborales

Para simular desplazamientos al trabajo:

```javascript
// Filtrar viajes que llegan entre 7:30 y 9:30
const morningArrivals = stopTimes.filter(st => {
    const time = parseGTFSHour(st.arrival_time);
    return time >= 7.5 && time <= 9.5;
});
```

---

### 3b. GTFS en el Navegador (Client-Side Engine)

Arquitectura probada para parsear y consultar GTFS **desde el frontend**, sin servidor. Implementada en TimeIneco v0.7.

#### Cuándo usarlo

- El proyecto HTML/JS no tiene backend Node.js pesado
- Solo necesitas consultar **paradas cercanas** y **rutas disponibles** (no routing complejo OTP)
- Quieres demo visual sin infraestructura
- El usuario puede subir su propio GTFS ZIP

#### Stack frontend

| Componente | Tecnología |
|------------|-----------|
| ZIP parser | JSZip (CDN, ~100KB) |
| Proximidad | Haversine (manual, sin lib) |
| Cache | localStorage (serializado) |
| Descarga proxy | Endpoint POST en server.mjs |
| Visualización | Leaflet markers con popups |

#### Arquitectura del motor

```javascript
class GTFSEngine {
  // Carga desde cache localStorage
  cargarDesdeCache(ciudadId) → { stops, routes, trips, stopTimes, calendar }

  // Carga desde ZIP subido por usuario (JSZip)
  async cargarDesdeZip(file) → mismo formato

  // Haversine: paradas en radio
  findStopsNear(lat, lng, radiusKm=1.5) → stops[ ] con distancia

  // Resumen de rutas que pasan por un conjunto de paradas
  getRouteSummary(stopIds) → { routeId, routeName, routeType, trips }
}
```

#### Flujo de integración

```
1. Usuario escoge origen en mapa
2. Frontend detecta ciudad (desde geocode inverso o coordenadas)
3. Muestra operadores candidatos (EMT, ALSA, EMTusa, etc.)
4. Usuario elige operador → carga GTFS de cache o fetch ZIP
5. GTFSEngine.findStopsNear(origin, 1.5km) → paradas
6. Mapa: marcadores morados con popup (distancia + rutas)
7. GTFSEngine.getRouteSummary(stopIds) → chips de líneas
8. PDF puede incluir esta info (tabla paradas + rutas destacadas)
```

#### Datos simulados (demo sin API)

Para desarrollo, se puede crear un `gtfs-cache.json` con estructura GTFS simplificada:

```json
{
  "ciudades": {
    "madrid": {
      "operador": "EMT Madrid",
      "stops": [
        {"stop_id":"101","stop_name":"Plaza Mayor","stop_lat":40.415,"stop_lon":-3.707},
        ...
      ],
      "routes": [
        {"route_id":"L1","route_short_name":"1","route_long_name":"Plaza Mayor - Atocha","route_type":3},
        ...
      ],
      "trips": [...],
      "stop_times": [
        {"trip_id":"T1_L1_001","stop_id":"101","stop_sequence":1,"arrival_time":"07:00:00"},
        ...
      ]
    }
  }
}
```

### Subida manual de ZIP

El usuario puede subir su propio GTFS ZIP para cualquier ciudad:

```javascript
// En el frontend
const zip = await JSZip.loadAsync(file);
const stops = parseCSV(await zip.file('stops.txt').async('string'));
const routes = parseCSV(await zip.file('routes.txt').async('string'));
const trips = parseCSV(await zip.file('trips.txt').async('string'));
const stopTimes = parseCSV(await zip.file('stop_times.txt').async('string'));

// Guardar en localStorage
localStorage.setItem('gtfs-ciudad', JSON.stringify({ stops, routes, trips, stopTimes }));
```

#### Proxy para feeds externos (CORS)

Muchos feeds GTFS públicos no permiten CORS. Endpoint proxy en server.mjs:

```javascript
// POST /gtfs-download
// Body: { url: "https://..." }
// Response: binary ZIP
if (req.method === 'POST' && req.url.startsWith('/gtfs-download')) {
  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', async () => {
    const { url } = JSON.parse(body);
    const resp = await fetch(url);
    const buffer = await resp.arrayBuffer();
    // Devolver como application/zip
    res.writeHead(200, {
      'Content-Type': 'application/zip',
      'Content-Length': buffer.byteLength
    });
    res.end(Buffer.from(buffer));
  });
}
```

#### Pitfalls

- **No usar `?v=N` en ES module imports** — los imports no llevan query params. Si necesitas cache-busting en NaN/CDN, versiona el nombre del archivo (ej: `gtfs-engine.v7.js`)
- **localStorage tiene límite ~5-10MB** — un GTFS de ciudad grande (Madrid: 100+ rutas, 2000+ paradas) ocupa ~200-500KB. Suficiente. Para regiones enteras, usar IndexedDB.
- **Haversine vs Turf.js** — Haversine manual es 1KB, turf.js es 200KB+. Para solo distancia punto-parada, Haversine es suficiente. Usa turf solo si necesitas operaciones geométricas (intersect, buffer).
- **JSZip desde CDN** — asegurarse de cargar el script antes que el motor GTFS. Orden en HTML: `<script src="cdn/jszip.min.js">` → `<script type="module" src="main.js">`
- **Coordenadas GTFS son (lat, lon)** — al revés que GeoJSON (lon, lat). Cuidado al crear markers de Leaflet.
- **stop_times puede ser enorme** — filtrar solo paradas cercanas + solo días laborables antes de procesar. No cargar stop_times completos de ciudades grandes sin filtrar.
- **Radio de búsqueda: preferir 500m para TP accesible a pie** — para aplicaciones de movilidad laboral, 500m es más realista que 2km. Un radio de 500m equivale a ~5-7 min andando hasta la parada.
- **DOCX sobre PDF para informes de equipo** — cuando el informe lo va a editar un equipo (Word track changes), generar DOCX en vez de PDF. La librería `docx@8.5.1` (CDN) genera .docx con tablas reales, colores, estilos. jsPDF es mejor para informes finales (no editables).
- **Cache de CDN en deployments** — si despliegas a NaN.builders, Cloudflare cachea 404 por 4h. Si el archivo GTFS.js es nuevo, renombrar con versión (ver skill `nan-deploy-sync`).

---

### 3c. Exportación GeoJSON de paradas

```javascript
function exportarParadasGeoJSON(stops, filename = 'paradas-gtfs.geojson') {
  const geojson = {
    type: 'FeatureCollection',
    features: stops.map(s => ({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [s.stop_lon, s.stop_lat] },
      properties: {
        stop_id: s.stop_id,
        stop_name: s.stop_name,
        distance_km: s.distance_km,
        routes: s.routes?.join(', ') || ''
      }
    }))
  };

  const blob = new Blob([JSON.stringify(geojson, null, 2)], {type: 'application/geo+json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
```

---

## 4. Caminando y Bicicleta con Desnivel

### Cómo afecta el desnivel

Los motores de routing profesionales usan datos de elevación (SRTM, ASTER, Copernicus DEM) para penalizar el tiempo de viaje según el desnivel:

| Perfil | Velocidad base | Penalización desnivel |
|--------|---------------|----------------------|
| Andando (plano) | 5 km/h | +1 min por cada 10m subida |
| Andando (subida) | 3 km/h | +2 min por cada 10m |
| Bicicleta (plana) | 15 km/h | +0.5 min por cada 10m |
| Bicicleta (montaña) | 8 km/h | +1 min por cada 10m |

### Implementación simple

```javascript
// Penalización basada en desnivel acumulado
function adjustWalkingTime(baseTime, elevationGain) {
    return baseTime + (elevationGain / 10) * 60;
}

function adjustCyclingTime(baseTime, elevationGain) {
    return baseTime + (elevationGain / 10) * 30;
}
```

### Datos de elevación

- **SRTM:** 30m resolución, gratis
- **ASTER GDEM:** 30m resolución, gratis
- **Copernicus DEM:** 30m resolución, gratis (Europa)
- **Open Elevation:** API REST, gratis

### ¿Cómo lo hacen las web profesionales?

- **OpenRouteService:** Usa SRTM para elevación, penalización automática en walking/cycling
- **Valhalla:** Usa SRTM/ASTER, perfil de elevación nativo
- **Google Maps:** Usa datos propios (no open source)
- **Mapillary:** Datos de calle (no elevación directa)

---

### 4b. Simulación de Isocronas (fallback cuando ORS no está disponible)

Cuando la API de ORS no responde o no hay conexión, se usa un **motor de simulación local** que genera isocronas orgánicas (no círculos perfectos). Implementado en TimeIneco (`js/isochrones.js`, junio 2026).

#### Arquitectura de la simulación

```
72 puntos base (5° spacing)
    + 5 capas de ruido multicapa (frecuencias: 0.7, 2.3, 5.1, 11.3, 17.1)
    + 12 corredores radiales (calles principales)
    + [Bici] Campo de elevación simulado
    → Desplazamiento radial de cada punto
    → Suavizado Gaussiano 3-ventana
    → Clipeo costero (turf.intersect)
```

#### Ruido multicapa (noise shaping)

```javascript
function ruidoMulticapa(angulo, amplitudes, frecuencias) {
    let total = 0;
    for (let i = 0; i < amplitudes.length; i++) {
        total += amplitudes[i] * Math.sin(angulo * frecuencias[i] + Math.PI * i);
    }
    return total;
}
```

5 capas de frecuencias crecientes: la baja frecuencia (0.7) da la forma general, las altas (11.3, 17.1) añaden irregularidad fina.

#### Corredores radiales (calles simuladas)

```javascript
function factorCalles(angulo) {
    let factor = 1.0;
    // Calles principales cada 30° (especular para calles ortogonales)
    for (let i = 0; i < 6; i++) {
        const dir = (Math.PI / 6) * i;
        const dif = Math.abs(normalizarAngulo(angulo - dir));
        factor += Math.exp(-(dif * dif) / (2 * sigma * sigma)) * peso;
    }
    // Calles secundarias cada 15° (offset 7.5°)
    for (let i = 0; i < 6; i++) {
        const dir = (Math.PI / 6) * i + Math.PI / 12;
        const dif = Math.abs(normalizarAngulo(angulo - dir));
        factor += Math.exp(-(dif * dif) / (2 * sigma * sigma)) * (peso * 0.5);
    }
    return factor;
}
```

Las calles principales tienen peso completo, las secundarias la mitad. El factor multiplica el radio base.

#### Perfiles de transporte (diferencias clave)

| Parámetro | Andando | Bici | Coche |
|-----------|---------|------|-------|
| Velocidad base | 5 km/h | 15 km/h | 40 km/h |
| σ calles principales | 0.18 (difuso) | 0.12 (estrecho) | 0.10 (muy estrecho) |
| Peso calles | 0.07 | 0.20 | 0.35 |
| Elevación simulada | No | Sí (5 capas) | No |
| Forma resultante | Orgánica, suave | Estrellada, con radios | Compacta, calles marcadas |

#### Elevación simulada (solo bici)

Para bicicleta, se simula un campo de elevación con 5 capas de ruido a frecuencias más bajas:

```javascript
// Campo orográfico simulado para penalizar ciclistas
function campoElevacionSimulado(lat, lng, origenLat, origenLng) {
    const dx = (lng - origenLng) * 111320 * Math.cos(origenLat * PI / 180);
    const dy = (lat - origenLat) * 111320;
    let elev = 0;
    const frecs = [0.2, 0.5, 1.1, 2.3, 4.7];
    const amps = [8, 5, 3, 2, 1];
    for (let i = 0; i < 5; i++) {
        elev += amps[i] * Math.sin(dx * frecs[i] / 1000) * Math.cos(dy * frecs[i] / 1000 + i);
    }
    return Math.max(0, elev + 10); // mínimo 10m
}
```

La elevación simulada penaliza el radio hasta un 30% en subidas. No reemplaza datos reales SRTM/DEM, pero da una forma más realista que un círculo perfecto.

#### Suavizado

```javascript
function suavizarPuntos(coords) {
    const n = coords.length;
    const suaves = [];
    for (let i = 0; i < n; i++) {
        const prev = coords[(i - 1 + n) % n];
        const cur = coords[i];
        const next = coords[(i + 1) % n];
        suaves.push([
            (prev[0] + cur[0] + next[0]) / 3,
            (prev[1] + cur[1] + next[1]) / 3
        ]);
    }
    return suaves;
}
```

Suavizado Gaussiano de 3 puntos (ventana [0.25, 0.50, 0.25]) para eliminar picos artificiales del ruido.

#### Cuándo usar simulación vs ORS real

| Situación | Usar |
|-----------|------|
| ORS responde | ORS real (red viaria, elevación real) |
| ORS timeout/error | Simulación multicapa |
| Sin conexión | Simulación multicapa |
| Walking/cycling | Ambas (ORS si posible, simulación si no) |
| Valladolid palote | Si la ciudad está en Soria (ORS no tiene cobertura), simulación |
| Coche | Siempre preferir ORS (la simulación coche es menos realista) |

#### Limitaciones conocidas

- **No hay intersección con OSM:** la simulación no sabe dónde están las calles reales
- **Elevación simulada:** no reemplaza datos DEM reales, solo da forma orgánica
- **Coche poco realista:** los corredores radiales funcionan mejor para bici/andando que para coche
- **No escala por modo:** la simulación no ajusta la red de calles por modo de transporte (una calle principal para coche puede ser autovía, para bici es carril bici)

---

### 4c. Prioridad de fuentes (fallback chain)

Para walking/cycling en producción:

```
1. try ORS real (POST /isochrone) → si 200, usar
2. catch → simulación multicapa con corredores radiales
3. Final → clipeo costero a tierra firme
```

La simulación NO intenta competir con ORS — ORS es siempre superior porque usa la red viaria real de OSM con elevación real SRTM. La simulación es un fallback visualmente aceptable cuando ORS no está disponible.

---

## 5. Arquitectura Recomendada

### MVP mínimo (una sola máquina, sin self-hosting)

```
Frontend (HTML/JS)
    ├── ORS API (isocronas) — cloud
    ├── NAP API (TP España) — cloud
    └── Leaflet (mapa) — local
```

**Ventajas:**
- Cero infraestructura
- Gratis para uso personal (< 2.500 req/día)
- Despliegue en cualquier hosting estático

**Desventajas:**
- Límite de API
- Dependencia de servicios externos

### Completo (self-hosted)

```
Frontend (HTML/JS)
    ├── Valhalla (isocronas + desnivel) — self-hosted
    ├── OTP (transporte público) — self-hosted
    ├── Copernicus DEM (elevación) — local
    └── Leaflet (mapa) — local
```

**Ventajas:**
- Sin límites de API
- Control total de datos
- Desnivel preciso

**Desventajas:**
- Requiere servidor dedicado
- Más complejo de desplegar

---

## 6. Limitaciones y Pitfalls

### Limitaciones conocidas

1. **ORS gratis:** 2.500 req/día — suficiente para uso personal, no para producción
2. **GTFS incompleto:** Algunas ciudades pequeñas no tienen GTFS
3. **Desnivel en ORS:** Penalización automática pero no configurable
4. **Tiempo de cálculo:** Isocronas complejas pueden tardar varios segundos
5. **Precisión TP:** Los horarios pueden no reflejar retrasos en tiempo real

### Pitfalls

- **No confundir isocrona con routing:** Una isocrona es un polígono, no una ruta
- **GTFS no es routing:** Es solo datos estáticos, necesitas un motor (OTP) para routing
- **No hardcodear API keys:** Usar inyección en servidor (ver skill `frontend-dashboard-patterns`)
- **Self-hosting Valhalla:** Requiere al menos 2GB RAM para cargar los datos de Europa
- **ORS proxy con Node.js: error silencioso por `--env-file`:** Si el servidor proxy Node.js no se arranca con `node --env-file=.env server.mjs`, `process.env.ORS_API_KEY` está vacío aunque el `.env` exista. El proxy ORS devuelve "ORS_API_KEY no configurada" y el frontend cae a simulación sin que el usuario sepa por qué.
- **ORS proxy: endpoint path mismatch:** El frontend llama a `fetch('/isochrone')` (sin 's') y el servidor escucha `req.url.startsWith('/isochrones')` (con 's'). Si no coinciden exactamente, la petición nunca llega al proxy y recibe 404 → simulation fallback.
- **ORS proxy: API key truncada por redacción del sistema:** Al escribir `.env` desde un agente con herramientas de archivo, la key JWT puede ser truncada por sistemas de redacción de credenciales. Verificar siempre la longitud con `node --env-file=.env -e 'console.log(process.env.ORS_API_KEY.length)'`. Una key JWT ORS válida tiene ~120 caracteres.
- **Coastline clipping con turf.js: la ORS real ya evita el mar:** ORS usa red viaria OSM, que no cruza el mar (excepto puentes/ferries). El clipeo costero es principalmente útil para el fallback de simulación (círculos que sí invaden el mar) y para zonas portuarias donde el polígono ORS bordea la costa sin recorte limpio.
- **MIME type para `.geojson`:** El servidor Node.js debe incluir `'.geojson': 'application/geo+json'` en el mapa MIME, o los navegadores pueden tratar el archivo como texto plano.

---

## 7. Proxy ORS con Node.js (Servidor con API Key oculta)

### Arquitectura

Para aplicaciones frontend que consumen ORS, **nunca expongas la API key en el frontend**. En vez de eso:

```
Frontend (fetch) ──POST /isochrone──→ Node.js Proxy ──POST ORS API──→ openrouteservice.org
                                            │
                                            └── .env (ORS_API_KEY)
```

El frontend hace `fetch('/isochrone', {...})` al mismo servidor que sirve los estáticos. El servidor añade el `Authorization` header con la key desde `process.env.ORS_API_KEY` y reenvía la petición a ORS.

### Implementación mínima (server.mjs)

```javascript
// Proxy ORS isochrone
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
    const bodyObj = {
      locations: [locations],   // ORS espera [[lng, lat]]
      range,                    // [segundos]
      range_type: 'time',
      attributes: ['area']
    };

    const proxyReq = https.request({
      hostname: 'api.openrouteservice.org',
      path: `/v2/isochrones/${profile}`,
      method: 'POST',
      headers: {
        'Authorization': ORS_KEY,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json, application/geo+json'
      }
    }, (proxyRes) => {
      let data = '';
      proxyRes.on('data', chunk => data += chunk);
      proxyRes.on('end', () => {
        res.writeHead(proxyRes.statusCode, { 'Content-Type': 'application/json' });
        res.end(data);
      });
    });

    proxyReq.write(JSON.stringify(bodyObj));
    proxyReq.end();
  });
}
```

### Arranque correcto

```
node --env-file=.env server.mjs
```

En Node.js 20+, `--env-file` carga variables del `.env` en `process.env`. Sin esta flag, `process.env.ORS_API_KEY` estará vacío.

### Frontend (fetch)

```javascript
const resp = await fetch('/isochrone', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    profile: 'foot-walking',
    locations: [-3.7038, 40.4167],  // [lng, lat]
    range: [900]                     // segundos
  })
});
const data = await resp.json();
// data.type === 'FeatureCollection' → ORS real
// data.fallback === true → ORS no disponible
```

### Health check endpoint

```javascript
// GET /healthz
const ORS_KEY = process.env.ORS_API_KEY;
res.end(JSON.stringify({
  status: 'ready',
  checks: {
    ors_api: typeof ORS_KEY === 'string' && ORS_KEY.length > 20
  }
}));
```

### Ver referencia técnica

`references/ors-proxy-nodejs.md` — implementación completa con proxy Nominatim incluido y Dockerfile.

---

## 8. Coastline Clipping (Sea Clipping)

Recorta isocronas a tierra firme para evitar que los polígonos se extiendan sobre el mar. Vital en ciudades costeras (Barcelona, Gijón, Málaga, etc.).

### Por qué es necesario

- **ORS real** ya evita el mar porque usa red viaria OSM (no hay calles en el agua)
- **Simulación local** genera círculos perfectos que invaden el mar sin control
- **Zonas portuarias**: el polígono ORS bordea la costa pero el recorte da un resultado más limpio
- **PDF profesional**: un informe con isocronas que se salen al mar queda poco serio

### Stack

| Componente | Tecnología | Tamaño |
|-----------|-----------|--------|
| Coastline global | Natural Earth 110m land | 135KB (127 features) |
| Motor geométrico | turf.js (CDN) | ~200KB gzipped |
| Recorte | turf.intersect() | instantáneo (<10ms) |

### Fuente de datos

```bash
# Natural Earth 110m land polygons (~135KB, mundo entero)
curl -L -o data/ne_110m_land.geojson \
  "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson"
```

Otras resoluciones disponibles:
- **110m** → 135KB (suficiente para isocronas urbanas, recomendada)
- **50m** → ~2MB (para isocronas regionales)
- **10m** → ~200MB (demasiado grande para web)

### Arquitectura (carga lazy)

```
Punto geográfico
    │
    ├─ esZonaCostera() ── No ──→ devolver coords originales (sin cargar coastline)
    │
    └─ Si ──→ loadCoastline() ── fetch /data/ne_110m_land.geojson (una vez)
                    │
                    └─ clipToLand(coords) ── turf.intersect(isocrona, land)
                                │
                                └─ coords recortadas (o polígono mínimo si está en mar)
```

### Implementación (clip.js)

```javascript
import { clipToLand } from './clip.js';

async function aplicarClipeo(resultado, lat, lng) {
  if (!resultado.geojson?.features?.[0]) return resultado;

  const coords = resultado.geojson.features[0].geometry.coordinates[0];
  const clipped = await clipToLand(coords, lat, lng);

  if (clipped !== coords) {
    resultado.geojson.features[0].geometry.coordinates = [clipped];
    resultado.areaKm2 = calcularAreaPoligonoKm2(clipped, lat);
  }
  return resultado;
}
```

### Detección de zona costera (esZonaCostera)

Se define un radio alrededor de cada ciudad costera conocida (~15-20km). Si el punto está dentro, se activa la carga del coastline. Las ciudades incluidas:

Gijón, Barcelona, Valencia, Málaga, Bilbao, Alicante, Cádiz, San Sebastián, A Coruña, Palma, Cartagena, Huelva, Santander, Vigo, Almería, Tarragona

### MIME type necesario

En `server.mjs`, añadir `.geojson` al mapa de tipos:

```javascript
const MIME = {
  ...
  '.geojson': 'application/geo+json',
  ...
};
```

### Fallback para isocronas completamente marítimas

Si `turf.intersect()` no encuentra tierra (isócrona que cayó toda en el mar), devolver un **polígono mínimo** (~50m) alrededor del punto original en vez de un polígono vacío:

```javascript
function createMinimalPolygon(lat, lng) {
  const dLat = 0.0005 / 111.32;
  const dLng = 0.0005 / (111.32 * Math.cos(lat * Math.PI / 180));
  return [
    [lng - dLng, lat - dLat],
    [lng + dLng, lat - dLat],
    [lng + dLng, lat + dLat],
    [lng - dLng, lat + dLat],
    [lng - dLng, lat - dLat]
  ];
}
```

### Ver referencia técnica

`references/coastline-clipping.md` — implementación completa de clip.js, incluyendo manejo de MultiPolygon y fusión de partes con turf.union().

---