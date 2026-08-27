# ISOTime — Multi-Engine Audit Case Study

**Fecha:** 2026-07-01
**Proyecto:** ISOTime (Ntizar/ISOTime) — Calculadora de isócronas en España
**Stack:** Vanilla JS, Leaflet, Web Workers, Dijkstra, OSRM, CSR binary graphs

## Architecture

```
ORS (API key) → Dijkstra local (Web Worker) → OSRM público (sin key) → Simulación
```

- **ORS:** Máxima precisión, requiere API key del usuario
- **Dijkstra local:** Grafo viario pre-calculado (CSR binario), 4 ciudades disponibles, sin API
- **OSRM público:** Routing real sin key, solo coche, boundary detection 72 direcciones
- **Simulación:** Círculo jittered, fallback final

## Bugs Found

### 1. CRITICAL: Dijkstra cutoff was dead code

**File:** `js/dijkstra-worker.js`, line 176

```js
// BEFORE (broken)
const { node, d } = heap.pop();  // d is ALWAYS undefined
if (d > cutoffSec) break;        // undefined > number = false → never fires

// AFTER (fixed)
const { node, dist: d } = heap.pop();  // d = actual distance value
```

**Impact:** Dijkstra explored the ENTIRE graph instead of stopping at the time cutoff. For Madrid (thousands of nodes), this meant 5-10x more computation than needed. The algorithm still produced correct results, but was much slower than necessary.

**Root cause:** MinHeap.pop() returns `{ node, dist }` but the destructuring used `{ node, d }`. JavaScript destructuring silently assigns `undefined` when the property name doesn't match — no error, no warning.

**Detection pattern:**
```bash
# Find destructuring of heap/priority-queue return values
grep -rn 'heap\.\(pop\|dequeue\|poll\)' --include='*.js' .
# Then verify the destructured names match the return type
```

**Lesson:** When auditing algorithms with priority queues, always verify that destructured property names EXACTLY match the return type of the data structure's methods.

### 2. MEDIUM: `new Promise(async ...)` anti-pattern

**File:** `js/graph-loader.js`, line 86

```js
// BEFORE (anti-pattern)
export function calcularIsocronaLocal(lat, lng, modo, minutos) {
  return new Promise(async (resolve, reject) => {
    try {
      await loadCityGraph(city.name);  // If this throws, rejection may not propagate
      // ...
    } catch (err) {
      reject(err);
    }
  });
}

// AFTER (clean async/await)
export async function calcularIsocronaLocal(lat, lng, modo, minutos) {
  try {
    await loadCityGraph(city.name);
    return await new Promise((resolve, reject) => {
      // Only the Worker communication is Promise-wrapped
      // Everything else uses native async/await
    });
  } catch (err) {
    throw err;
  }
}
```

**Why it matters:** The `async` inside `new Promise()` means the constructor's try/catch doesn't catch errors from the async callback. If `loadCityGraph()` throws before the Promise executor finishes, the rejection may be unhandled.

**Detection:**
```bash
grep -rn 'new Promise(async' --include='*.js' .
```

### 3. LOW: Dead config values

**File:** `js/config.js`

```js
// These were defined but never imported/used by any module:
OSRM_RADII: [3, 6, 10, 15, 20, 30, 45, 60, 80],
OSRM_POINTS_PER_RING: 36,
```

The OSRM function in `isochrones.js` defines its own `radios` and `N_DIR` constants inline.

**Detection:**
```bash
# For each key in CONFIG, check if it's used outside config.js
for key in OSRM_RADII OSRM_POINTS_PER_RING; do
  grep -rn "$key" --include='*.js' . | grep -v config.js
done
# Empty output = dead config
```

### 4. LOW: Config declares 20 cities, only 4 have data

`GRAPH_CITIES` in config lists 20 cities with radius, but only `madrid.bin`, `bilbao.bin`, `sevilla.bin`, `zaragoza.bin` exist in `data/graphs/`.

`hasLocalGraph()` returns `true` for all 20 (checks config), but `loadCityGraph()` fails with HTTP 404 for the 16 without .bin files. The "🧠 Grafo local disponible" indicator appears incorrectly.

**Fix:** Either generate the missing .bin files, or verify .bin existence before showing the indicator.

## Files Modified

| File | Change | Lines |
|------|--------|-------|
| `js/dijkstra-worker.js` | `{ node, d }` → `{ node, dist: d }` | 1 line |
| `js/graph-loader.js` | `new Promise(async ...)` → proper `async/await` | ~40 lines refactored |
| `js/config.js` | Removed `OSRM_RADII`, `OSRM_POINTS_PER_RING` | 2 lines removed |

## Verification

After fix, tested on live deployment (https://ntizar.github.io/ISOTime/):
- Madrid 30min car: Dijkstra computes significantly faster (cutoff now works)
- Fallback chain: ORS → Dijkstra → OSRM → Simulation all functional
- Export GeoJSON/Shapefile: works regardless of engine used
