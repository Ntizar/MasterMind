---
name: lazy-dataset-loading
description: "Carga progresiva de datasets: solo lo que el usuario necesita, cuando lo necesita. Patrón con ensureDataset, cache de estado, merge en hash index, y precarga idle. reduce tiempo de carga inicial de 10s a 250ms."
version: 1.0.0
author: Mastermind
tags: [lazy-loading, dataset, performance, progressive, vanilla-js, dashboard]
source: espanatlas.es
---

# Lazy Dataset Loading — Carga Progresiva de Datos

## Cuándo usar
- Dashboard con 10+ datasets que el usuario puede explorar
- Carga inicial de >5MB que bloquea la UI
- Datos que se cargan por categorías (salud, economía, elecciones...)
- Aplicación donde el usuario solo ve 1-2 datasets a la vez

## Problema: cargar todo al inicio

```javascript
// ❌ LENTO — 10+ segundos de carga inicial
const salud = await fetch('./data/health.json');      // 7MB
const elecciones = await fetch('./data/elec.json');    // 10MB
const presupuestos = await fetch('./data/budget.json'); // 8MB
const aire = await fetch('./data/air.json');            // 3MB
// Total: ~28MB + parsing time = bloqueado 10s+
```

## Solución: carga bajo demanda

```javascript
// ✅ RÁPIDO — 250ms carga inicial, datasets bajo demanda
const core = await fetch('./data/core.json');  // 2MB → siempre
// Los demás se cargan cuando el usuario los necesita
```

## Arquitectura completa

```javascript
// Estado global
const DATASET_STATUS = {};    // 'pending' | 'loading' | 'loaded' | 'error'
const DATASETS = {};

// Registry de datasets
DATASETS.salud = {
  url: './data/health_municipal_metrics.json',
  label: 'Salud',
  loader: async () => {
    const rows = await fetchJSON(DATASETS.salud.url);
    return rows;
  },
  merge: (rows) => {
    rows.forEach(d => {
      if (IDX[d.cod]) Object.assign(IDX[d.cod], d);
    });
  }
};

DATASETS.elec = {
  url: './data/elecciones_2023.json',
  label: 'Elecciones',
  loader: async () => {
    const rows = await fetchJSON(DATASETS.elec.url);
    return rows;
  },
  merge: (rows) => {
    rows.forEach(d => {
      if (IDX[d.cod]) Object.assign(IDX[d.cod], d);
    });
  }
};
```

## ensureDataset — patrón central

```javascript
async function ensureDataset(key) {
  // 1. Ya cargado → no hacer nada
  if (DATASET_STATUS[key] === 'loaded') return;

  // 2. Ya cargándose → esperar a que termine
  if (DATASET_STATUS[key] instanceof Promise) {
    return DATASET_STATUS[key];
  }

  // 3. Marcar como cargando
  DATASET_STATUS[key] = 'loading';

  try {
    const ds = DATASETS[key];
    const rows = await ds.loader();
    ds.merge(rows);
    DATASET_STATUS[key] = 'loaded';
    console.info(`✅ ${ds.label}: ${rows.length} registros`);
  } catch (err) {
    DATASET_STATUS[key] = 'error';
    console.error(`❌ Error cargando ${key}:`, err);
  }
}
```

## Carga por métrica (el patrón España Atlas)

```javascript
// Cada métrica sabe qué dataset necesita
function datasetsForMetric(metric) {
  const MAP = {
    'tParo25': ['empleo'],          // solo necesita datos de empleo
    'renta23': ['base'],            // ya está en el core
    'elec23_ganador': ['elec'],     // solo necesita elecciones
    'saludApPor100k18': ['salud'],  // solo necesita salud
    'liqGastoHab24': ['budget'],    // solo necesita presupuestos
    'tipoCluster': ['salud', 'business', 'budget'],  // necesita 3 datasets
  };
  return MAP[metric] || ['base'];
}

// Al cambiar métrica, solo carga lo que falta
async function updateMap() {
  const metric = document.getElementById('metric-select').value;
  const needed = datasetsForMetric(metric);

  const missing = needed.filter(k => DATASET_STATUS[k] !== 'loaded');
  if (missing.length) {
    showLoading('Cargando datos...');
    await Promise.all(missing.map(ensureDataset));
    hideLoading();
  }

  // Re-colorear mapa
  geoLayer.setStyle(styleF);
}
```

## Carga con progreso visual

```javascript
async function fetchWithProgress(url, label, pctFrom, pctTo) {
  const resp = await fetch(url);
  const total = +resp.headers.get('Content-Length') || 0;
  const reader = resp.body.getReader();
  const chunks = [];
  let loaded = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    loaded += value.length;

    if (total > 0) {
      const pct = pctFrom + (loaded / total) * (pctTo - pctFrom);
      setProgress(pct, `${label} ${Math.round(loaded / 1e6)} MB…`);
    }
  }

  const all = new Uint8Array(chunks.reduce((a, c) => a + c.length, 0));
  let pos = 0;
  for (const c of chunks) { all.set(c, pos); pos += c.length; }
  return JSON.parse(new TextDecoder().decode(all));
}
```

## Precarga idle (sin bloquear UI)

```javascript
function runIdle(fn, timeout = 2000) {
  if ('requestIdleCallback' in window) {
    requestIdleCallback(fn, { timeout });
  } else {
    setTimeout(fn, 100);
  }
}

// Precargar datasets secundarios cuando el navegador esté libre
runIdle(() => {
  preloadDatasetsStaggered(['elec', 'health', 'air']);
}, 1800);

// Carga escalonada (no todo a la vez)
async function preloadDatasetsStaggered(keys) {
  for (const key of keys) {
    await runIdle(() => ensureDataset(key));
  }
}
```

## Caché de estado

```javascript
// Para datasets calculados (no descargados)
const COMPUTED_CACHE = {};

async function ensureComputed(key, computeFn) {
  if (COMPUTED_CACHE[key]) return COMPUTED_CACHE[key];
  COMPUTED_CACHE[key] = computeFn();
  return COMPUTED_CACHE[key];
}

// Ejemplo: rankings
async function buildRankings() {
  return ensureComputed('rankings', () => {
    const rows = Object.values(IDX);
    const sorted = rows.sort((a, b) => (b[curMetric] || 0) - (a[curMetric] || 0));
    return { top: sorted.slice(0, 10), bottom: sorted.slice(-10) };
  });
}
```

## Merge en IDX (patrón España Atlas)

```javascript
// IDX es el hash central de datos
let IDX = {};

// Los datos base se cargan primero
const base = await fetch('./data/municipios_core.json');
base.forEach(d => { IDX[d.cod] = d; });

// Los datasets secundarios se fusionan
function mergeMetricRows(rows, label) {
  rows.forEach(d => {
    const cod = String(d.cod).padStart(5, '0');
    if (IDX[cod]) Object.assign(IDX[cod], d);  // añade nuevas keys al objeto existente
  });
  // Recalcular métricas derivadas
  recomputeDerivedMetrics();
  console.info(`Datos cargados: ${label}`);
}
```

## Flujo completo

```
Carga inicial (250ms):
  core.json → IDX (8132 objetos)
  municipios_topo.json → GeoJSON → Canvas layer
  ↓
  Primer choropleth listo

Usuario cambia a "calidad del aire":
  ensureDataset('air') → fetch air.json (3MB)
  mergeMetricRows() → fusiona en IDX
  geoLayer.setStyle() → re-colorea
  ↓
  Mapa actualizado en 300ms

Usuario vuelve a métrica base:
  Dataset ya cacheado → sin fetch
  geoLayer.setStyle() → re-colorea
  ↓
  Instantáneo
```

## Métricas de rendimiento

| Escenario | Carga total | Tiempo |
|-----------|------------|--------|
| Todo al inicio | ~28 MB | ~10s |
| Lazy loading | ~2 MB inicial + ~3MB/dataset | ~250ms inicial |
| Con cache | 0 MB (ya cargado) | ~10ms |

## Pitfalls

1. **Race conditions** — si el usuario cambia rápido de métrica, cancelar fetch anterior con `AbortController`
2. **Merge conflictivo** — si datasets tienen la misma key con valores distintos, el último sobrescribe
3. **Memoria** — `Object.assign()` no libera datos viejos; con muchos datasets crece el heap
4. **Progresión falsa** — si el servidor no envía `Content-Length`, el progress bar no funciona
5. **Precarga agresiva** — no precargar todos los datasets en móvil (data limits)

## Integración con otros skills

- **sparse-json-format** → datasets sparse se expanden antes del merge
- **hash-index-data** → IDX es el hash index central
- **leaflet-canvas-choropleth** → `setStyle()` tras carga de datos
