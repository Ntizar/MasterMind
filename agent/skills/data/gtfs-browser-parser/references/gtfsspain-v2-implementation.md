# GTFSSpain v2 — Implementación completa (2026-07-02, actualizado v2.3)

## Repositorio
- **Repo:** `github.com/Ntizar/GTFSSpain-v2` (PÚBLICO)
- **Pages:** `https://ntizar.github.io/GTFSSpain-v2/` (index.html en raíz)
- **Commits:** v2.1 (33f9f6d) → v2.2 (aaa1208) → fix delimiter (8c2521d) → fix Pages (b64ef15) → v2.3 full routes (41ddd86)

## Qué cambia vs v1

| Feature | v1 | v2.1 | v2.2 | v2.3 |
|---------|----|----|------|------|
| Shapes clickeables | ❌ | ✅ | ✅ | ✅ |
| Panel de ruta | ❌ | ✅ | ✅ + horarios por parada | ✅ |
| Filtro por headsign | ❌ | ✅ | ✅ + dirección IDA/VUELTA | ✅ |
| Explorador de rutas | ❌ | ✅ | ✅ | ✅ |
| Shapes en mapa | N/A | clippeados | clippeados (sin bg) | **COMPLETOS** |
| stop_times truncado | N/A | ❌ (200K cap) | ✅ sin límite | ✅ |
| calendar_dates.txt | ❌ | ❌ | ✅ | ✅ |
| frequencies.txt | ❌ | ❌ | ✅ | ✅ |
| transfers.txt | ❌ | ❌ | ✅ | ✅ |
| feed_info.txt | ❌ | ❌ | ✅ | ✅ |
| Distancia de ruta | ❌ | ❌ | ✅ calculada desde shapes | ✅ |
| Countdown próxima salida | ❌ | ❌ | ✅ | ✅ |
| Filtro por día semana | ❌ | ❌ | ✅ | ✅ |

## Cambio v2.3 — Shapes completos sin clip (commit 41ddd86)

**Solicitud de David:** "Las rutas no las muestra enteras hasta que no las pinchas."

**Cambios:**
1. Eliminada función `clipShapeToSearchArea()` del renderizado principal
2. `renderMapStops()` ahora dibuja `allShapeCoords[shapeId]` completo (sin clip)
3. Subtítulo actualizado: "Shapes completos con área de búsqueda"
4. La función `clipShapeToSearchArea()` sigue disponible por si se necesita en el futuro

**Código eliminado:**
```javascript
// ANTES (v2.2): clippeado
const clippedCoords = clipShapeToSearchArea(allShapeCoords[shapeId], nearStopCoords, radius);
if (!clippedCoords || clippedCoords.length < 2) return;
const line = L.polyline(clippedCoords, { color, weight: 5, opacity: 0.85 });
```

**Código nuevo (v2.3):**
```javascript
// AHORA: ruta completa
const fullCoords = allShapeCoords[shapeId];
const line = L.polyline(fullCoords, { color, weight: 5, opacity: 0.85, smoothFactor: 2 });
```

**¿Por qué?** El usuario quiere ver la ruta entera para entender por dónde pasa. El círculo de búsqueda muestra qué paradas están cerca; las líneas muestran la infraestructura completa.

## Bugs corregidos en v2.2

1. **Líneas de fondo** — El v2.1 dibujaba `allShapeCoords[shapeId]` completo con opacity 0.15. Parecía que se mostraban TODAS las líneas. FIX: eliminar bgLine, solo mostrar clipped.
2. **stop_times truncado** — `Math.min(lines.length, 200000)` causaba datos incompletos. FIX: sin límite.
3. **Sin calendar_dates.txt** — EMT Fuenlabrada solo tiene calendar_dates.txt (no calendar.txt). FIX: parsear ambos.
4. **Horarios superficiales** — El timetable solo mostraba primera/última salida. FIX: mostrar horarios completos por parada.

## Bug v2.2.1 — CSV delimiter silencioso (commit 8c2521d)

**Síntoma:** Al clickear paradas, UI mostraba "0 rutas" sin error visible.

**Causa:** `parseCSVLine(lines[i])` se llamaba sin delimiter en la línea de parseo de stop_times.txt. La función compara `char === delimiter` — cuando delimiter es `undefined`, `char === undefined` siempre es `false`, así que la línea entera se trata como un solo campo. `vals.length === 1` → la condición `if (vals.length !== headers.length)` descarta TODAS las filas de stop_times. Resultado: `stop.routes` siempre vacío.

**FIX:** Auto-detección de delimiter (comma/tab/semicolon) + pass explícito del delimiter a parsearLineaCSV tanto para headers como para datos.

**Patrón de fallo general:** En JavaScript, parámetros default a `undefined` no lanzan errores. Una función que espera un string como segundo argumento puede recibir `undefined` y ejecutarse sin fallo visible — solo produce datos incorrectos. SIEMPRE verificar que las funciones CSV reciben el delimiter correctamente.

## Variables globales v2.2

```javascript
let allCalendarDates = {};   // service_id -> [{date, exception_type}]
let allFrequencies = [];     // [{trip_id, start_time, end_time, headway_secs}]
let allTransfers = {};       // stopId -> [{to_stop_id, transfer_type, min_transfer_time}]
let allFeedInfo = [];        // [{publisher, version, start_date, end_date}]
let tripDirectionMap = {};   // tripId -> direction_id (0=IDA, 1=VUELTA)
```

## Funciones del v2 (31 en total)

### Core
- `initMap()` — Inicialización Leaflet con CARTO light + preferCanvas
- `cargarZip(filename, filepath)` — Carga ZIP y procesa GTFS
- `processGTFS(zip, filename)` — Extrae todos los archivos GTFS, construye índices

### Interacción mapa
- `onMapClick(e)` — Click vacío en mapa → panel de contexto
- `openRouteDetail(routeId)` — ABRE el panel de ruta detallado
- `closeRouteDetail()` — Cierra panel de ruta
- `highlightRoute(routeId)` — Zoom + polyline resaltado en mapa

### Panel de ruta
- `renderRouteKPIs(route)` — KPIs: viajes, paradas, direcciones
- `getRouteStopsOrdered(routeId)` — Paradas ordenadas por stop_sequence
- `getRouteTripStats(routeId)` — Viajes totales + primera/última hora
- `getRouteDirections(routeId)` — Direcciones/headsigns únicos
- `getRouteTripsByHeadsign(routeId, headsign)` — Viajes filtrados por dirección
- `getRouteScheduleStats(trips)` — Estadísticas de horarios

### Schedule
- `buildTimetableHTML(routeId, headsignsMap, filterHeadsign)` — Tabla de horarios filtrada

### Explorer
- `updateRouteExplorer()` — Lista de todas las rutas en sidebar
- `filterRoutes(query)` — Filtra rutas por texto

### Paradas
- `showSchedulePanel(stop)` — Panel de horarios de parada
- `getRouteSummary(stopsNear)` — Resumen de rutas para parada

### Helpers
- `detectDelimiter(headerLine)` — Auto-detecta delimiter (comma/tab/semicolon) del header
- `parsearCSV(text)` — CSV parser con comillas + auto-detección de delimiter
- `parsearLineaCSV(line, delimiter)` — Línea individual con delimiter explícito
- `haversine(lat1, lon1, lat2, lon2)` — Distancia en km
- `findStopsNear(lat, lng, radiusKm)` — Búsqueda por proximidad
- `getModeColor(type)` — Color por tipo de transporte
- `getModeLabel(type)` — Label por tipo
- `formatTime(timeStr)` — Formato HH:MM
- `formatSize(bytes)` — Formato legible
- `setLoadingState(loading)` — Estado de carga
- `clearAllLayers()` — Limpia mapa

## Estado global (variables)

```javascript
let map, markersLayer, shapesLayer, highlightLayer;
let allStops = [], allRoutes = [], allTrips = [], allStopTimes = [], allShapes = [];
let stopRouteMap = {}, routeShapeMap = {}, tripRouteMap = {}, routeTripCount = {};
let allShapeCoords = {};
let loadedZips = new Set();
```

## Datos
- Symlink `data → /root/workspace/GTFSSpain/data` (379MB, 37+ datasets)
- .gitignore excluye data/ y README.md
- server.py para desarrollo local (puerto 8000)

## Estructura de archivos

```
GTFSSpain-v2/
├── index.html          # EN RAÍZ — necesario para GitHub Pages
├── visor/
│   ├── index.html      # 147KB, self-contained (copia de backup)
│   └── server.py       # HTTP server con /api/zips
├── data → ../GTFSSpain/data/  # symlink
├── README.md           # Informe de cambios
├── .gitignore
├── descargar-nap.py    # Descargador NAP API
├── cron-update.sh      # Script actualización semanal
└── iniciar.bat         # Launcher Windows
```

## Pitfalls del v2

1. **`L.DomEvent.stop(e)` en click de polyline** — Sin esto, el click se propaga al mapa y cierra el panel inmediatamente
2. **Paradas sin stop_sequence** — Algunos feeds no lo tienen; fallback a orden de aparición en stop_times
3. **Headsigns vacíos** — trips.route_id puede existir sin trip_headsign; usar `Sin dirección` como fallback
4. **Symlink data/** — Git no commitea symlinks pesados; el .gitignore excluye data/
5. **GitHub Pages path** — Pages con source `/` solo sirve archivos de la raíz. Si `index.html` está en `visor/`, Pages no lo encuentra y sirve README.md. FIX: `cp visor/index.html ./index.html` + commit + push. Verificar con `curl -s "https://usuario.github.io/repo/" | head -5`.
