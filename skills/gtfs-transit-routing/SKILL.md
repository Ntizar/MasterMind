---
name: gtfs-transit-routing
version: "1.0.0"
description: >
  Motor de routing de transporte público con GTFS real: calcular rutas con transbordo
  (0, 1 o 2 transbordos), horarios reales de stop_times.txt, calendar.txt para
  filtrado de días laborables, ranking de rutas por tiempo total.
tags: [gtfs, routing, transit, transbordo, horarios, stop_times, calendar, isochrones, transporte-publico]
---

# GTFS Transit Routing — Motor de Rutas con Transbordo

## Cuándo cargar esta skill

Cuando el usuario pida: routing de transporte público con transbordos, calcular rutas reales entre dos puntos con horarios GTFS, "hasta dónde llego en bus/metro a las X", planes de movilidad con horarios, ranking de rutas de TP.

## Concepto

Un motor de routing que usa datos GTFS reales (`stop_times.txt`, `trips.txt`, `calendar.txt`) para calcular rutas de transporte público entre un origen y un destino, con transbordos, horarios reales y ranking por tiempo total.

**Diferencia con GTFS básico:** `gtfs-browser-parser` solo busca paradas cercanas y rutas disponibles. Este skill calcula rutas reales con horarios.

## Arquitectura

```
Input: origen (lat,lng) + destino (lat,lng) + horario objetivo
  → findStopsNear(origen, 500m) → paradas_origen[]
  → findStopsNear(destino, 500m) → paradas_destino[]
  → buildTransitGraph(gtfsData) → grafo de paradas con horarios
  → findRoutes(origen, destino, maxTransfers=2) → rutas[]
  → filterBySchedule(rutas, horario) → rutas_filtradas[]
  → sort(tiempo_total) → ranking de rutas
```

## 1. Construir Grafo de Transporte

A partir de `stop_times.txt` + `trips.txt` + `routes.txt`:

```javascript
function buildTransitGraph(gtfsData) {
  const { stops, trips, stopTimes, routes } = gtfsData;

  // 1. trip_id → route_id + direction_id
  const tripInfo = new Map();
  for (const trip of trips) {
    tripInfo.set(trip.trip_id, {
      route_id: trip.route_id,
      direction_id: trip.direction_id
    });
  }

  // 2. stop_times por trip, ordenados por secuencia
  const tripStops = new Map(); // trip_id → [{stop_id, arrival_time, departure_time, sequence}]
  for (const st of stopTimes) {
    const tid = st.trip_id;
    if (!tripStops.has(tid)) tripStops.set(tid, []);
    tripStops.get(tid).push({
      stop_id: st.stop_id,
      arrival_time: st.arrival_time,
      departure_time: st.departure_time || st.arrival_time,
      sequence: parseInt(st.stop_sequence) || 0
    });
  }
  // Ordenar por secuencia
  for (const [tid, stops] of tripStops) {
    stops.sort((a, b) => a.sequence - b.sequence);
  }

  // 3. Grafo: stop_id → [{trip_id, route_id, from_sequence, to_sequence, times}]
  const adjacency = new Map();
  for (const stop of stops) {
    adjacency.set(stop.stop_id, []);
  }

  for (const [tripId, stopsInTrip] of tripStops) {
    const info = tripInfo.get(tripId);
    if (!info) continue;

    for (let i = 0; i < stopsInTrip.length - 1; i++) {
      const from = stopsInTrip[i];
      const to = stopsInTrip[i + 1];
      const travelTime = calcularDiferenciaHoraria(from.departure_time, to.arrival_time);

      adjacency.get(from.stop_id).push({
        to_stop_id: to.stop_id,
        trip_id: tripId,
        route_id: info.route_id,
        travel_time_sec: travelTime,
        departure_time: from.departure_time,
        arrival_time: to.arrival_time
      });
    }
  }

  return { adjacency, tripStops, tripInfo, stops };
}
```

## 2. Calcular Diferencia Horaria

```javascript
function parseTime(timeStr) {
  // "07:45:00" → { hours: 7, minutes: 45, seconds: 0 }
  const parts = timeStr.split(':').map(Number);
  return parts[0] * 3600 + parts[1] * 60 + (parts[2] || 0);
}

function calcularDiferenciaHoraria(fromTime, toTime) {
  const from = parseTime(fromTime);
  const to = parseTime(toTime);
  let diff = to - from;
  // Manejar cruce de medianoche
  if (diff < 0) diff += 86400;
  return diff; // segundos
}

function formatarTiempo(segundos) {
  const mins = Math.round(segundos / 60);
  return `${Math.floor(mins / 60)}h ${mins % 60}min`;
}
```

## 3. Encontrar Rutas con Transbordos

Algoritmo BFS con límite de transbordos:

```javascript
function findRoutes(graph, origenStops, destinoStops, maxTransfers = 2) {
  const { adjacency, tripStops, tripInfo } = graph;
  const allRoutes = [];

  // Para cada combinación origen-destino
  for (const origStop of origenStops) {
    for (const destStop of destinoStops) {
      // BFS con límite de transbordos
      const routes = bfsWithTransfers(
        origStop.stop_id, destStop.stop_id, maxTransfers, adjacency,
        tripStops, tripInfo
      );
      allRoutes.push(...routes);
    }
  }

  return allRoutes;
}

function bfsWithTransfers(startStop, endStop, maxTransfers, adjacency,
                          tripStops, tripInfo) {
  const results = [];

  // Estado: { stop_id, transfers, route_id, arrival_time, path: [{stop, route, trip, arrival}] }
  const visited = new Map(); // stop_id → min_transfers para llegar aquí
  const queue = [{
    stop_id: startStop,
    transfers: 0,
    current_route: null,
    arrival_time: 0,
    path: [{ stop_id: startStop, route_id: null, trip_id: null, arrival_time: 0 }]
  }];

  while (queue.length > 0) {
    const state = queue.shift();

    // Si llegamos al destino
    if (state.stop_id === endStop) {
      results.push({
        path: [...state.path],
        transfers: state.transfers,
        total_time: state.arrival_time,
        route_ids: [...new Set(state.path.map(p => p.route_id).filter(Boolean))]
      });
      continue;
    }

    // No explorar si ya superamos transbordos
    if (state.transfers > maxTransfers) continue;

    // Explorar vecinos
    const neighbors = adjacency.get(state.stop_id) || [];
    for (const edge of neighbors) {
      const newTransfers = state.current_route && edge.route_id !== state.current_route
        ? state.transfers + 1
        : state.transfers;

      if (newTransfers > maxTransfers) continue;

      // Evitar ciclos
      const stateKey = `${state.stop_id}_${newTransfers}`;
      if (visited.has(stateKey) && visited.get(stateKey) <= newTransfers) continue;
      visited.set(stateKey, newTransfers);

      queue.push({
        stop_id: edge.to_stop_id,
        transfers: newTransfers,
        current_route: edge.route_id,
        arrival_time: state.arrival_time + edge.travel_time_sec,
        path: [...state.path, {
          stop_id: edge.to_stop_id,
          route_id: edge.route_id,
          trip_id: edge.trip_id,
          arrival_time: edge.arrival_time,
          departure_time: edge.departure_time
        }]
      });
    }
  }

  return results;
}
```

## 4. Filtrar por Horario Laboral

```javascript
function filterBySchedule(routes, horarioObjetivo) {
  // horarioObjetivo: { type: 'arrive'|'depart', time: "08:30:00" }
  const targetSec = parseTime(horarioObjetivo.time);

  return routes.filter(route => {
    // Calcular tiempo de llegada estimado
    const arrivalSec = route.total_time;

    if (horarioObjetivo.type === 'arrive') {
      // Ruta válida si llega dentro de la ventana
      const windowMin = 900; // ±15 min
      return Math.abs(arrivalSec - targetSec) <= windowMin;
    } else {
      // Ruta válida si sale dentro de la ventana
      const departureSec = route.path[0].departure_time || 0;
      const windowMin = 900;
      return Math.abs(departureSec - targetSec) <= windowMin;
    }
  });
}

function filterHorarioLaboral(routes) {
  // Filtrar por horarios laborales: 7:30-9:30 (ida), 16:30-18:30 (vuelta)
  const morningWindow = (t) => {
    const sec = parseTime(t);
    return sec >= parseTime("07:30:00") && sec <= parseTime("09:30:00");
  };
  const eveningWindow = (t) => {
    const sec = parseTime(t);
    return sec >= parseTime("16:30:00") && sec <= parseTime("18:30:00");
  };

  return routes.filter(r => {
    // Verificar que al menos una parada tenga horario laboral
    return r.path.some(p => morningWindow(p.arrival_time) || eveningWindow(p.arrival_time));
  });
}
```

## 5. Ranking de Rutas

```javascript
function rankRoutes(routes, preferencia = 'tiempo') {
  // preferencia: 'tiempo' | 'transbordos' | 'directa'
  return routes.sort((a, b) => {
    if (preferencia === 'tiempo') {
      return a.total_time - b.total_time;
    } else if (preferencia === 'transbordos') {
      return a.transfers - b.transfers;
    } else if (preferencia === 'directa') {
      // Prefiere rutas sin transbordo
      const aDirect = a.transfers === 0 ? 0 : 1;
      const bDirect = b.transfers === 0 ? 0 : 1;
      if (aDirect !== bDirect) return aDirect - bDirect;
      return a.total_time - b.total_time;
    }
  });
}
```

## 6. Integración con isochrones-gtfs.js

```javascript
// En isochrones-gtfs.js, añadir:
import { findTransitRoutes, buildTransitGraph } from './transit-routing.js';

export async function calcularRutasGTFS(lng1, lat1, lng2, lat2, modo, gtfsData) {
  // 1. Construir grafo transit
  const graph = buildTransitGraph(gtfsData);

  // 2. Encontrar paradas cercanas a origen y destino
  const origStops = buscarParadasCercanas(lng1, lat1, 0.5, gtfsData);
  const destStops = buscarParadasCercanas(lng2, lat2, 0.5, gtfsData);

  if (origStops.length === 0 || destStops.length === 0) return { rutas: [], error: 'No hay paradas en origen o destino' };

  // 3. Calcular rutas con transbordos
  const rutas = findRoutes(graph, origStops, destStops, 2);

  // 4. Filtrar por horario laboral
  const filtradas = filterHorarioLaboral(rutas);

  // 5. Ranking
  const ranking = rankRoutes(filtradas, 'tiempo');

  return {
    rutas: ranking,
    total: filtradas.length,
    mejor: ranking[0] || null,
    origen: { lat: lat1, lng: lng1, paradas: origStops.length },
    destino: { lat: lat2, lng: lng2, paradas: destStops.length }
  };
}
```

## 7. Integración con main.js

```javascript
// En main.js, exponer:
window.__timeineco_rutas = {
  rutas: [],
  mejor: null,
  total: 0,
  origen: null,
  destino: null
};

// Al calcular con origen + destino:
import { calcularRutasGTFS } from './isochrones-gtfs.js';

async function handleCalcularRutas() {
  if (!state.punto || !state.destino) return;
  const gtfs = window.__timeineco_gtfs;
  if (!gtfs) return;

  const result = await calcularRutasGTFS(
    state.punto.lng, state.punto.lat,
    state.destino.lng, state.destino.lat,
    'bus', gtfs
  );

  window.__timeineco_rutas = result;
  renderizarRutas(result);
}
```

## 8. Integración con DOCX Report

```javascript
// En docx-report.js, añadir sección de rutas:
function generarSeccionRutas(rutas) {
  if (!rutas || !rutas.rutas || rutas.rutas.length === 0) return [];

  const secciones = [];
  secciones.push(_tituloSeccion('Rutas de Transporte Público Calculadas', COLOR.purple));

  for (const [i, ruta] of rutas.rutas.slice(0, 5).entries()) {
    secciones.push(_subtitulo(`Ruta ${i + 1} — ${formatarTiempo(ruta.total_time)}`, COLOR.primary));
    secciones.push(_cuerpo(`Transbordos: ${ruta.transfers} | Rutas: ${ruta.route_ids.join(', ')}`));

    for (const [j, parada] of ruta.path.entries()) {
      secciones.push(_cuerpo(`  ${j + 1}. ${parada.stop_name} — ${parada.arrival_time || '—'}`));
    }
  }

  return secciones;
}
```

## Datos GTFS Necesarios

| Archivo | Necesario para | Sin él |
|---------|--------------|--------|
| `stops.txt` | Paradas cercanas | No funciona |
| `routes.txt` | Identificar línea | No funciona |
| `trips.txt` | trip→route mapping | Inferir de route_stops |
| `stop_times.txt` | **Horarios reales** | Solo BFS por paradas (sin horarios) |
| `calendar.txt` | Filtrar días laborables | Sin filtro de día |
| `shapes.txt` | Visualizar trazado | No necesario para routing |

**Pitfall crítico:** El GTFS de Madrid en `gtfs-cache.json` tiene `trips: []` y `stop_times: []`. Esto es suficiente para búsqueda de paradas cercanas pero NO para routing con horarios. Para routing real, se necesita un GTFS con `stop_times.txt` poblado.

## Pitfalls

1. **GTFS sin stop_times:** Si `stop_times.txt` está vacío, el grafo transit no se puede construir. Fallback a BFS simple (isochrones-gtfs.js actual).
2. **Cruce de medianoche:** `departure_time` puede ser 23:55 y `arrival_time` 00:10. Calcular diferencia como `(to - from + 86400) % 86400`.
3. **stop_sequence no empieza en 0:** Algunos GTFS usan secuencias arbitrarias. Ordenar siempre por `stop_sequence` numérico.
4. **Paradas de transbordo:** Dos paradas físicamente cercanas pero con IDs distintos. Para transbordos realistas, considerar paradas a <100m como conectables (caminando).
5. **Performance:** BFS con transbordos puede explotar combinatoriamente. Limitar `maxTransfers=2` y usar `visited` map para evitar ciclos.
6. **Horarios de fin de semana:** `calendar.txt` puede tener `calendar_dates.txt` en vez de `calendar.txt`. Algunos feeds usan solo `calendar_dates`. Soportar ambos.
7. **Direccionalidad:** `trips.direction_id` puede ser 0 o 1. Para routing ida/vuelta, verificar que la dirección del trip coincide con la dirección deseada.

## Referencias

- `references/gtfs-transit-routing-algorithm.md` — Algoritmo BFS con transbordos, complejidad y optimizaciones
- `references/gtfs-schedule-filtering.md` — Filtrado por horarios laborales, calendar.txt, calendar_dates.txt
