# Visor GTFS — Stop Timetable + Catalog Embedding (v2.0)

> Basado en GTFStoCSV v2.0. Añadido 2026-07-03.

## Patrón: routesByStop — Índice inverso parada→rutas

Cuando parseas un GTFS en el navegador, necesitas un índice inverso que te diga qué rutas sirven cada parada:

```javascript
// Construir durante parseGTFSZip()
const _routesByStop = {};
stopTimes.forEach(st => {
    const stopId = st.stop_id;
    if (!_routesByStop[stopId]) _routesByStop[stopId] = [];
    const trip = trips.find(t => t.trip_id === st.trip_id);
    if (!trip) return;
    const route = routesById[trip.route_id];
    if (!route) return;
    _routesByStop[stopId].push({
        route_id: trip.route_id,
        route_name: route.route_long_name || route.route_short_name || trip.route_id,
        route_short_name: route.route_short_name || '',
        route_color: route.route_color || '',
        route_type: route.route_type || '',
        trip_headsign: trip.trip_headsign || '',
        departure_time: st.departure_time || st.arrival_time || '',
        trip_id: st.trip_id,
        stop_sequence: parseInt(st.stop_sequence) || 0
    });
});

// Exponer globalmente
window._routesByStop = _routesByStop;
```

**Pitfall:** `stopTimes.forEach()` puede ser masivo (76K+ stop_times). El `find()` dentro de cada iteración es O(n²). Para GTFS grandes, construir primero un `Map<trip_id, trip>` y otro `Map<route_id, route>`:

```javascript
const tripMap = new Map(trips.map(t => [t.trip_id, t]));
const routeMap = new Map(routes.map(r => [r.route_id, r]));
// Luego en el loop:
const trip = tripMap.get(st.trip_id);
if (!trip) return;
const route = routeMap.get(trip.route_id);
```

## Patrón: stopsByRoute — Paradas ordenadas de cada ruta

```javascript
const _stopsByRoute = {};
routes.forEach(r => {
    const rid = r.route_id;
    const trips = tripsByRoute[rid] || [];
    const orderedStops = getOrderedStops(rid, trips, stopTimesByTrip, stopsById);
    _stopsByRoute[rid] = orderedStops.map(s => s.stop_id).filter(Boolean);
});
```

### getOrderedStops — Elegir el viaje con más paradas

```javascript
function getOrderedStops(routeId, trips, stopTimesByTrip, stopsById) {
    let bestTrip = null, maxStops = 0;
    trips.forEach(t => {
        const sts = stopTimesByTrip[t.trip_id] || [];
        if (sts.length > maxStops) { maxStops = sts.length; bestTrip = sts; }
    });
    if (!bestTrip) return [];
    bestTrip.sort((a,b) => parseInt(a.stop_sequence||0) - parseInt(b.stop_sequence||0));
    return bestTrip.map(st => ({ ...(stopsById[st.stop_id] || {}), departure_time: st.departure_time })).filter(s => s.stop_id);
}
```

**Razón:** No todos los viajes (trips) de una ruta cubren todas las paradas. El viaje con más stop_times es el más completo.

## Patrón: Stop Timetable Panel (gtfs-to-html style)

Cuando el usuario hace clic en una parada del mapa, mostrar todas las líneas y sus horarios:

```javascript
function openStopPanel(stopId) {
    const rbs = window._routesByStop;
    const entries = rbs[stopId] || [];

    // 1. DEDUP — mismo (route_id + headsign + departure_time) aparece una vez
    const seen = new Set();
    const uniqueEntries = [];
    entries.forEach(e => {
        const key = e.route_id + '|' + e.trip_headsign + '|' + e.departure_time;
        if (!seen.has(key)) { seen.add(key); uniqueEntries.push(e); }
    });

    // 2. SORT by departure_time
    uniqueEntries.sort((a, b) => (a.departure_time || '').localeCompare(b.departure_time || ''));

    // 3. GROUP by route_id
    const byRoute = {};
    uniqueEntries.forEach(e => {
        if (!byRoute[e.route_id]) byRoute[e.route_id] = [];
        byRoute[e.route_id].push(e);
    });

    // 4. RENDER — por cada ruta: badge de color + tabla de horarios
    const routeIds = Object.keys(byRoute).sort();
    let routesHtml = '';
    routeIds.forEach(rid => {
        const times = byRoute[rid];
        const rows = times.map(t =>
            `<tr><td>${t.trip_headsign || '—'}</td><td>${t.departure_time || '—'}</td></tr>`
        ).join('');
        routesHtml += `
            <div class="stop-route-card">
                <div class="sr-header">
                    <span class="route-badge" style="background:${color}">${shortName}</span>
                    <span>${routeType} ${routeName}</span>
                    <span>${times.length} salidas</span>
                </div>
                <div class="sr-body">
                    <table><thead><tr><th>Dirección</th><th>Salida</th></tr></thead>
                    <tbody>${rows}</tbody></table>
                </div>
            </div>`;
    });
}
```

**KPIs del panel:**
- Número de rutas distintas que sirven la parada
- Número total de salidas (departures)
- Botón de exportar CSV

### Export CSV de horarios de parada

```javascript
function exportStopCSV(stopId) {
    const entries = window._routesByStop[stopId] || [];
    // Dedup + sort
    const data = dedupedEntries.map(e => ({
        parada_id: stopId,
        parada_nombre: stopName,
        ruta_id: e.route_id,
        ruta_nombre: e.route_name,
        trip_headsign: e.trip_headsign || '',
        departure_time: e.departure_time || '',
        trip_id: e.trip_id || ''
    }));
    exportTableCSV(data, `horarios_${stopId}`);
}
```

### CSS del stop panel

```css
#stop-panel {
    position: fixed; top: var(--header-h); right: 0; bottom: 0;
    width: 520px; background: white; border-left: 2px solid var(--kz-azul);
    z-index: 1500; transform: translateX(100%);
    transition: transform .3s ease; overflow-y: auto;
}
#stop-panel.open { transform: translateX(0); }

.stop-route-card {
    border: 1px solid var(--kz-gris-200);
    border-radius: var(--kz-radius-md); margin-bottom: 8px; overflow: hidden;
}
.stop-route-card .sr-header {
    padding: 8px 12px; display: flex; align-items: center; gap: 8px;
    background: var(--kz-gris-50); font-size: var(--kz-text-sm); font-weight: 500;
}
.stop-route-card .sr-body { padding: 8px 12px; max-height: 300px; overflow-y: auto; }
```

## Patrón: Catálogo de operadores NAP embebido

Para visores HTML autocontenidos (sin servidor), embedir el catálogo de operadores como constante JS:

```javascript
// 160 operadores de transporte español (250KB compacto)
const OPERADORES = [{"id":920,"nombre":"AECFA slots","organizacion":"AECFA","tipo":["Aéreo"],...}];

// Renderizar grid de tarjetas
function renderCatalog(operadores) {
    grid.innerHTML = operadores.map(op => `
        <div class="catalog-card" onclick="showOperatorDetail(${op.id})">
            <h4>${tipoIcon} ${op.nombre}</h4>
            <div class="catalog-org">${op.organizacion}</div>
            <div class="catalog-stats">${op.num_rutas} rutas · ${op.num_paradas} paradas</div>
            <div class="catalog-region">📍 ${op.regiones[0]}</div>
        </div>
    `).join('');
}
```

En el detalle de cada operador:

```javascript
function showOperatorDetail(id) {
    const op = OPERADORES.find(o => o.id === id);
    // Mostrar: nombre, organización, tipo, #rutas, #paradas, tamaño, región
    // Mensaje: "Descarga el GTFS desde la NAP y arrastra el ZIP aquí"
    // Link: abrir NAP en nueva pestaña
}
```

**Toggle catalog ↔ GTFS data:**

```css
#catalog-container.hidden { display: none; }
#gtfs-content { display: none; }
#gtfs-content.visible { display: block; }
```

En `renderAll()` (cuando se carga GTFS):
```javascript
document.getElementById('catalog-container').classList.add('hidden');
document.getElementById('gtfs-content').classList.add('visible');
```

**Pitfall Tamaño:** El catálogo de 160 operadores pesa ~250KB en formato compacto (sin indentación, con `separators=(',',':')`). Es aceptable para GitHub Pages pero NO para embederlo inline en el HTML. Mejor tenerlo como archivo separado (`operadores.json`) que el visor carga con `fetch()`.

### Catálogo → URL directa NAP

Cada operador en el NAP tiene un ID de fichero GTFS. La URL de descarga directa es:
```
https://nap.transportes.gob.es/descarga/{file_id}
```

No exponer la URL completa en el catálogo (los IDs internos de fichero cambian). En su lugar, mostrar:
- Organización + nombre del dataset
- Link genérico a `https://nap.transportes.gob.es/`
- Mensaje para que el usuario busque el operador en la web de la NAP

## Catálogo de operadores: formato compacto

Para minimizar tamaño, usar este formato (sin indentación, claves cortas):

```json
{"id":920,"nombre":"AECFA slots","organizacion":"AECFA","tipo":["Aéreo"],
 "regiones":["Álava","Andalucía","Aragón",...],
 "operadores":["AECFA"],
 "num_rutas":1590,"num_paradas":37,"num_viajes":101621,"tamanio_kb":3374}
```

Generar con Python:
```python
compact = [{k: v for k,v in op.items() if k in ['id','nombre','organizacion','tipo',
    'regiones','operadores','num_rutas','num_paradas','num_viajes','tamanio_kb']}
    for op in catalog]
json.dump(compact, f, ensure_ascii=False, separators=(',',':'))
```