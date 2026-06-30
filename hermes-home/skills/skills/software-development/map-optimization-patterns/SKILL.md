---
name: map-optimization-patterns
description: "Patrones para construir herramientas de optimización combinatoria sobre mapas: p-median, p-center, TSP, problema de transporte. Heurísticas JS, integración ORS/OSRM, UI con Leaflet."
version: "1.0.0"
author: David Antizar
tags: [optimization, combinatorial, p-median, p-center, tsp, transportation, leaflet, operations-research, routing, maps]
---

# Optimización Combinatoria sobre Mapas

## Cuándo cargar esta skill

Cuando el usuario pida: optimización de ubicación de instalaciones, p-median, p-center, TSP (viajante), problema de transporte/supply-demand, rutas óptimas que visitan múltiples puntos, ubicación óptima de almacenes/centros, logística de distribución.

## Contexto

Inspirado en un proyecto R Shiny ("組合せ最適化 on Map — ompr版") que resuelve 4 problemas clásicos de investigación operativa sobre un mapa Leaflet interactivo. Extraemos los patrones para implementarlos en nuestro stack (Node.js + Vanilla JS + Leaflet).

---

## Los 4 Problemas Clásicos

### 1. Facility Location — Ubicación de Instalaciones

**Pregunta:** ¿Dónde poner *p* instalaciones para minimizar la distancia a los usuarios?

#### p-median
- **Objetivo:** Minimizar la **distancia total ponderada** entre cada punto de demanda y su instalación más cercana
- **Uso:** Hospitales, centros de salud, almacenes, estaciones de bomberos
- **Input:** Puntos de demanda (lat, lng, peso) + número *p* de instalaciones
- **Output:** Ubicaciones óptimas + asignación demanda→instalación

```javascript
// p-median: minimizar distancia total ponderada
// min Σ_i Σ_j w_i * d_ij * x_ij
// s.t. Σ_j x_ij = 1  (cada demanda asignada a 1 instalación)
//      Σ_j y_j = p    (exactamente p instalaciones)
//      x_ij ≤ y_j     (solo se asigna a instalaciones abiertas)
```

#### p-center
- **Objetivo:** Minimizar la **distancia máxima** (el peor caso)
- **Uso:** Emergencias, cobertura garantizada, SLA de servicio
- **Input:** Igual que p-median
- **Output:** Ubicaciones que minimizan la distancia del punto más desfavorecido

```javascript
// p-center: minimizar la peor distancia
// min D
// s.t. d_ij * x_ij ≤ D  para todo i,j
//      Σ_j x_ij = 1
//      Σ_j y_j = p
```

**Diferencia clave:** p-median optimiza el promedio, p-center optimiza el peor caso. Un hospital usa p-center (nadie debe quedar lejos). Un almacén usa p-median (coste total mínimo).

### 2. TSP — Traveling Salesman Problem (Problema del Viajante)

**Pregunta:** ¿Cuál es el circuito más corto que visita todas las ciudades exactamente una vez?

- **Uso:** Rutas de reparto, logística de última milla, planificación de visitas
- **Input:** Lista de ciudades (lat, lng)
- **Output:** Orden óptimo de visita + distancia total

**Complejidad:** NP-hard. Exacto viable ≤ 12 ciudades (branch & bound / MTZ). Para más → heurísticas.

### 3. Transportation Problem — Problema de Transporte (Supply-Demand)

**Pregunta:** ¿Cómo mover mercancía de orígenes (oferta) a destinos (demanda) minimizando coste?

- **Uso:** Distribución logística, suministro, planificación de rutas multi-origen
- **Input:** Orígenes con capacidad + Destinos con demanda + Matriz de costes (distancia/tiempo)
- **Output:** Flujos óptimos (cuánto enviar de cada origen a cada destino)

```javascript
// min Σ_i Σ_j c_ij * x_ij   (coste total de transporte)
// s.t. Σ_j x_ij ≤ supply_i   (no enviar más de lo que hay)
//      Σ_i x_ij ≥ demand_j   (cubrir toda la demanda)
//      x_ij ≥ 0
```

---

## Heurísticas JS (sin solver LP/MIP)

Para tamaños < 50 puntos, las heurísticas dan resultados ≈ óptimos en milisegundos. No necesitamos GLPK, ompr, ni ningún solver externo.

### p-median — Greedy Interchange

```javascript
// Algoritmo: Greedy + intercambio 1-opt
function solvePMedian(demandPoints, p, distanceFn) {
  const n = demandPoints.length;
  if (p >= n) return demandPoints.map((_, i) => i);

  // 1. Greedy: añadir instalación que más reduce la distancia total
  let facilities = [];
  let assignments = new Array(n).fill(-1);

  for (let iter = 0; iter < p; iter++) {
    let bestIdx = -1, bestCost = Infinity;
    for (let c = 0; c < n; c++) {
      if (facilities.includes(c)) continue;
      // Calcular coste total si c fuera la nueva instalación
      let totalCost = 0;
      const testFacilities = [...facilities, c];
      for (let d = 0; d < n; d++) {
        const minDist = Math.min(...testFacilities.map(f =>
          distanceFn(demandPoints[d], demandPoints[f])
        ));
        totalCost += (demandPoints[d].weight || 1) * minDist;
      }
      if (totalCost < bestCost) { bestCost = totalCost; bestIdx = c; }
    }
    facilities.push(bestIdx);
  }

  // 2. Intercambio 1-opt: intentar swap facility↔non-facility
  let improved = true;
  while (improved) {
    improved = false;
    for (let i = 0; i < facilities.length; i++) {
      for (let c = 0; c < n; c++) {
        if (facilities.includes(c)) continue;
        const testFacilities = facilities.map((f, idx) => idx === i ? c : f);
        const newCost = totalCostPMedian(demandPoints, testFacilities, distanceFn);
        const oldCost = totalCostPMedian(demandPoints, facilities, distanceFn);
        if (newCost < oldCost - 0.01) {
          facilities[i] = c;
          improved = true;
        }
      }
    }
  }

  // Asignar cada demanda a su instalación más cercana
  for (let d = 0; d < n; d++) {
    let minD = Infinity, bestF = 0;
    for (const f of facilities) {
      const dist = distanceFn(demandPoints[d], demandPoints[f]);
      if (dist < minD) { minD = dist; bestF = f; }
    }
    assignments[d] = bestF;
  }

  return { facilities, assignments };
}

function totalCostPMedian(points, facilities, distFn) {
  return points.reduce((sum, p, i) => {
    const minDist = Math.min(...facilities.map(f => distFn(p, points[f])));
    return sum + (p.weight || 1) * minDist;
  }, 0);
}
```

### p-center — Minimax Greedy

```javascript
// Igual que p-median pero minimizando el MÁXIMO en vez del total
function solvePCenter(demandPoints, p, distanceFn) {
  // Misma estructura greedy, pero evaluando Math.max en vez de Math.sum
  // El intercambio busca reducir la distancia del punto MÁS LEJANO
  // (ver implementación completa en references/tsp-heuristics.md)
}
```

### TSP — Nearest Neighbor + 2-opt

```javascript
// Nearest Neighbor: heurística greedy (rapida, ~25% óptimo)
function tspNearestNeighbor(points, distFn) {
  const n = points.length;
  const visited = new Array(n).fill(false);
  const tour = [0];
  visited[0] = true;

  for (let step = 1; step < n; step++) {
    const last = tour[tour.length - 1];
    let bestNext = -1, bestDist = Infinity;
    for (let j = 0; j < n; j++) {
      if (visited[j]) continue;
      const d = distFn(points[last], points[j]);
      if (d < bestDist) { bestDist = d; bestNext = j; }
    }
    tour.push(bestNext);
    visited[bestNext] = true;
  }
  return tour;
}

// 2-opt: mejora local intercambiando 2 aristas
function tsp2Opt(tour, points, distFn) {
  let improved = true;
  while (improved) {
    improved = false;
    for (let i = 1; i < tour.length - 1; i++) {
      for (let j = i + 1; j < tour.length; j++) {
        // Calcular coste antes y después del intercambio
        const d1 = distFn(points[tour[i-1]], points[tour[i]])
                 + distFn(points[tour[j]], points[tour[(j+1) % tour.length]]);
        const d2 = distFn(points[tour[i-1]], points[tour[j]])
                 + distFn(points[tour[i]], points[tour[(j+1) % tour.length]]);
        if (d2 < d1 - 0.01) {
          // Reversar el segmento tour[i..j]
          tour.splice(i, j - i + 1, ...tour.slice(i, j + 1).reverse());
          improved = true;
        }
      }
    }
  }
  return tour;
}

// Combinación: Nearest Neighbor → 2-opt
function solveTSP(points, distFn) {
  const tour = tspNearestNeighbor(points, distFn);
  return tsp2Opt(tour, points, distFn);
}
```

**Límite práctico:** 2-opt funciona bien hasta ~30-50 puntos. Para más, usar 3-opt o Lin-Kernighan (complejidad mayor).

### Transportation Problem — Simplex de Transporte

```javascript
// Implementación simple del método de transporte (Vogel's Approximation + MODI)
function solveTransportation(supply, demand, costMatrix) {
  // supply: [cap1, cap2, ...]  (origenes)
  // demand: [dem1, dem2, ...]  (destinos)
  // costMatrix: [[c11, c12, ...], [c21, c22, ...]]  (coste unitario)

  const m = supply.length, n = demand.length;
  const flows = Array.from({length: m}, () => new Array(n).fill(0));

  // Vogel's Approximation Method (VAM)
  const sup = [...supply], dem = [...demand];
  for (let iter = 0; iter < m * n; iter++) {
    // Calcular penalizaciones (diferencia entre 2 menores costos)
    // Seleccionar celda con mayor penalización
    // Asignar el máximo posible
    // Actualizar supply/demand restante
    // (implementación completa en references/transport-simplex.md)
  }

  return flows; // flows[i][j] = cuánto enviar del origen i al destino j
}
```

---

## Distancia: Euclidiana vs Real

### Euclidiana (rápida, sin API)

```javascript
function haversine(lat1, lon1, lat2, lon2) {
  const R = 6371000; // metros
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2
    + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180)
    * Math.sin(dLon/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// Para TSP y p-median, usar matriz de distancias precalculada
function buildDistanceMatrix(points, distFn) {
  const n = points.length;
  const matrix = Array.from({length: n}, () => new Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const d = distFn(points[i], points[j]);
      matrix[i][j] = d;
      matrix[j][i] = d;
    }
  }
  return matrix;
}
```

### Real por carretera (ORS/OSRM)

**CRÍTICO:** No usar API de routing para calcular la matriz de distancias completa — sería O(n²) llamadas y se agota el rate limit.

**Solución:** Precalcular la matriz con euclidiana para resolver la optimización, y luego usar ORS/OSRM solo para dibujar la ruta final en el mapa.

```javascript
// Patrón: optimizar con euclidiana, visualizar con routing real
async function solveAndVisualize(points, p, distanceMode) {
  // 1. Resolver con euclidiana (instantáneo)
  const solution = solvePMedian(points, p, haversine);

  // 2. Si el usuario quiere ruta real, resolver solo las rutas necesarias
  if (distanceMode === 'road') {
    for (const d of solution.demandPoints) {
      const facility = points[solution.assignments[d.id]];
      const route = await fetchRoute(d, facility, 'car'); // ORS/OSRM
      renderRoute(route); // dibujar en mapa
    }
  }

  return solution;
}
```

### Matrices precalculadas (para matrices grandes)

```javascript
// Para 50+ puntos, precalcular en worker
// y cachear en localStorage
const cacheKey = `dist-matrix-${points.length}-${hash}`;
const cached = localStorage.getItem(cacheKey);
if (cached) return JSON.parse(cached);

const matrix = buildDistanceMatrix(points, haversine);
localStorage.setItem(cacheKey, JSON.stringify(matrix));
return matrix;
```

---

## UI Pattern: Mapa + Optimización

### Layout estándar

```
┌─────────────────────────────────────────────┐
│  Header oscuro (#1a1a2e)                     │
├──────────┬──────────────────────────────────┤
│ Sidebar  │  Mapa Leaflet Canvas              │
│ (280px)  │                                   │
│          │  [click → añadir punto]           │
│ Problema │                                   │
│ (select) │  [resultado → polígonos/rutas]    │
│          │                                   │
│ Params   │                                   │
│ (p, modo)│                                   │
│          │                                   │
│ Input    │                                   │
│ (click/  │                                   │
│  CSV)    │                                   │
│          │                                   │
│ Solucionar│                                  │
│          │                                   │
│ Resultado│                                   │
│ (KPIs)   │                                   │
│          │                                   │
│ Fórmula  │                                   │
│ (math)   │                                   │
└──────────┴──────────────────────────────────┘
```

### Entrada de datos: Click + CSV

```javascript
// Patrón: dual input (click en mapa o subir CSV)
let points = [];

// Click en mapa
map.on('click', (e) => {
  points.push({
    lat: e.latlng.lat,
    lng: e.latlng.lng,
    name: `Punto ${points.length + 1}`,
    weight: 1
  });
  renderPoints(points);
});

// CSV upload
function parseOptimizationCSV(text) {
  const lines = text.trim().split('\n');
  const headers = lines[0].toLowerCase().split(',').map(h => h.trim());
  return lines.slice(1).map(line => {
    const vals = line.split(',').map(v => v.trim());
    const obj = {};
    headers.forEach((h, i) => obj[h] = vals[i]);
    return {
      lat: parseFloat(obj.lat),
      lng: parseFloat(obj.lng || obj.lon),
      name: obj.name || `Punto`,
      weight: parseFloat(obj.weight) || 1,
      type: obj.type || 'demand' // para transportation
    };
  });
}
```

### Visualización de resultados

```javascript
// Colores por tipo de resultado
const COLORS = {
  facility: '#2563eb',    // azul: instalaciones seleccionadas
  demand: '#f97316',      // naranja: puntos de demanda
  assigned: '#10b981',    // verde: asignación demanda→instalación
  route: '#8b5cf6',       // púrpura: ruta TSP
  supply: '#3b82f6',      // azul claro: origen supply
  demandTP: '#ef4444',    // rojo: destino demanda
  flow: '#6366f1'         // indigo: flujo supply→demand
};

// Líneas de asignación (p-median/p-center)
function renderAssignments(points, assignments, facilities) {
  facilities.forEach((fIdx, i) => {
    points.forEach((p, dIdx) => {
      if (assignments[dIdx] === i) {
        L.polyline(
          [[p.lat, p.lng], [points[fIdx].lat, points[fIdx].lng]],
          { color: COLORS.assigned, weight: 1.5, opacity: 0.6, dashArray: '5,5' }
        ).addTo(map);
      }
    });
  });
}

// Ruta TSP (polyline en orden)
function renderTSPTour(points, tour) {
  const coords = tour.map(i => [points[i].lat, points[i].lng]);
  coords.push(coords[0]); // cerrar circuito
  L.polyline(coords, { color: COLORS.route, weight: 3 }).addTo(map);
}

// Flujos transportation (grosor proporcional)
function renderFlows(supply, demand, flows, maxFlow) {
  for (let i = 0; i < supply.length; i++) {
    for (let j = 0; j < demand.length; j++) {
      if (flows[i][j] > 0) {
        const weight = 1 + (flows[i][j] / maxFlow) * 8;
        L.polyline(
          [[supply[i].lat, supply[i].lng], [demand[j].lat, demand[j].lng]],
          { color: COLORS.flow, weight, opacity: 0.7 }
        ).addTo(map);
      }
    }
  }
}
```

---

## Fórmula Matemática (HTML render)

El proyecto original muestra la formulación matemática del problema en cada pestaña. Patrón para renderizar con KaTeX:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>

<div id="formula"></div>

<script>
// p-median formulation
const formula = `
$$\\min \\sum_{i \\in D} \\sum_{j \\in F} w_i \\cdot d_{ij} \\cdot x_{ij}$$
$$\\text{s.t.} \\quad \\sum_{j \\in F} x_{ij} = 1 \\quad \\forall i \\in D$$
$$\\sum_{j \\in F} y_j = p$$
$$x_{ij} \\leq y_j \\quad \\forall i \\in D, \\forall j \\in F$$
$$x_{ij}, y_j \\in \\{0, 1\\}$$
`;
katex.render(formula, document.getElementById('formula'), {
  displayMode: true, throwOnError: false
});
</script>
```

---

## Integración con Routing Externo

### Patrón: resolver local, visualizar con ORS

```javascript
// 1. Resolver optimización con euclidiana (sin API)
const solution = solveTSP(points, haversine);

// 2. Obtener ruta real solo para visualización
async function getRealRoute(from, to, mode) {
  const profile = { car: 'driving-car', bike: 'cycling-regular', foot: 'foot-walking' }[mode];
  const resp = await fetch('/ors-directions', {  // proxy backend
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      coordinates: [[from.lng, from.lat], [to.lng, to.lat]],
      profile
    })
  });
  return resp.json();
}

// 3. Dibujar ruta real encima del mapa
async function renderRealTour(points, tour, mode) {
  for (let i = 0; i < tour.length; i++) {
    const from = points[tour[i]];
    const to = points[tour[(i + 1) % tour.length]];
    const route = await getRealRoute(from, to, mode);
    const coords = decodePolyline(route.routes[0].geometry); // polyline → coordinates
    L.polyline(coords, { color: '#8b5cf6', weight: 3 }).addTo(map);
    await new Promise(r => setTimeout(r, 300)); // stagger para rate limit
  }
}
```

### Polyline decoder (ORS/OSRM usan Google polyline encoding)

```javascript
function decodePolyline(encoded) {
  const points = [];
  let index = 0, lat = 0, lng = 0;
  while (index < encoded.length) {
    let b, shift = 0, result = 0;
    do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
    lat += ((result & 1) ? ~(result >> 1) : (result >> 1));
    shift = 0; result = 0;
    do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
    lng += ((result & 1) ? ~(result >> 1) : (result >> 1));
    points.push([lat / 1e5, lng / 1e5]);
  }
  return points;
}
```

---

## Cuándo Usar Cada Problema

| Problema | Pregunta | Ejemplo real |
|---|---|---|
| **p-median** | ¿Dónde poner p instalaciones para minimizar distancia promedio? | Almacenes, centros logísticos |
| **p-center** | ¿Dónde poner p instalaciones para que nadie esté lejos? | Hospitales, bomberos, emergencias |
| **TSP** | ¿Cuál es la ruta más corta que visita todos los puntos? | Reparto, inspecciones, visitas |
| **Transporte** | ¿Cómo mover mercancía de origen a destino minimizando coste? | Distribución multi-origen, cadena de suministro |

### Decisiones de implementación

| Decisión | Opción A | Opción B |
|---|---|---|
| Solver | Heurísticas JS (sin dependencia) | GLPK/CPLEX vía WASM (más preciso) |
| Distancia | Euclidiana (gratis, instantáneo) | ORS/OSRM (real, rate limited) |
| Tamaño | < 50 puntos → 2-opt viable | > 50 puntos → metaheurísticas (SA, GA) |
| UI | Click en mapa (simple) | CSV upload (bulk) |

---

## Pitfalls

1. **TSP exacto escala mal** — Branch & bound / MTZ solo viable ≤ 12 ciudades. Para más, 2-opt da 95%+ óptimo en milisegundos
2. **p-median greedy no es óptimo** — pero el intercambio 1-opt mejora significativamente. Gap típico: 2-5% vs óptimo
3. **Matriz de distancias O(n²)** — Para 100 puntos = 10,000 pares. Con euclidiana es instantáneo, con ORS API serían 10,000 llamadas (nunca hacer esto)
4. **Transporte: supply vs demand deben equilibrarse** — Si Σsupply < Σdemand, el problema es infactible. Normalizar o añadir demanda ficticia
5. **ORS rate limit en visualización** — Para TSP con 20 puntos = 20 llamadas a ORS. Con stagger de 300ms = 6 segundos. Mostrar progreso
6. **CSV encoding** — Archivos CSV de Excel pueden venir en Latin1/CP1252. Detectar encoding y convertir a UTF-8
7. **Haversine vs vincenty** — Haversine tiene error ~0.5% en distancias largas. Para distancias urbanas (< 50km) es perfecto
8. **TSP cerrado vs abierto** — El proyecto original usa circuito cerrado (vuelta al inicio). Para rutas de reparto, puede ser abierto (no volver). Añadir toggle
9. **p-median con distancias reales puede dar diferente que euclidiana** — Las calles no son rectas. Mostrar ambas distancias y explicar la diferencia
10. **Transporte: costes no simétricos** — Ir de A→B puede costar diferente que B→A (pendiente, dirección). La matriz de costes debe soportar asimetría

---

## Cross-references

- **`routing-isochrones`** — Motores de routing (ORS, OSRM, Valhalla), isocronas, GTFS/GBFS, geocodificación. Complementa este skill: aquí resolvemos optimización, allí resolvemos routing
- **`isochrone-routing-tools`** — Arquitectura detallada de ORS, Valhalla, simulación. Útil cuando se necesita routing real como parte de la optimización
- **`frontend-dashboard-patterns`** — Patrones UI para dashboards. Aplica al layout sidebar+mapa

## Referencias

- **Proyecto original:** R Shiny "組合せ最適化 on Map — ompr版" (análisis completo en esta sesión)
- **ompr R package:** https://cran.r-project.org/package=ompr (referencia de formulación, no de implementación)
- **TSP heurísticas:** 2-opt, 3-opt, Lin-Kernighan — standard OR literature
- **p-median:** ReVelle & Eiselt (2005) — "Location Analysis: Fundamentals and Applications"
