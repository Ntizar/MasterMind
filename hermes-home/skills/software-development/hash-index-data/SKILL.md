---
name: hash-index-data
description: "Índice hash para acceso O(1) a registros en datasets grandes. Patrón IDX: array → objeto hash por key, merge de datasets, precomputación de métricas derivadas. Base para dashboards con 1K-100K registros."
version: 1.0.0
author: Mastermind
tags: [hash, index, performance, data-structure, o1, vanilla-js, dashboard]
source: espanatlas.es
---

# Hash Index Data — Acceso O(1) a Registros

## Cuándo usar
- Dataset con >500 registros que se buscan por un campo key
- Múltiples datasets que se fusionan por la misma key
- Búsquedas frecuentes en tiempo real (tooltips, filtros, rankings)
- Precomputación de métricas derivadas sobre datos tabulares

## Problema: acceso lineal es lento

```javascript
// ❌ LENTO — O(n) por cada búsqueda
const municipios = await fetch('./data/municipios.json');
// Buscar Madrid:
const madrid = municipios.find(m => m.cod === '28079');  // recorre 8132 registros
// Buscar Barcelona:
const bcn = municipios.find(m => m.cod === '08019');     // otro recorrido completo
// Para 100 búsquedas: 813.200 operaciones
```

## Solución: índice hash O(1)

```javascript
// ✅ RÁPIDO — O(1) por búsqueda
const IDX = {};
municipios.forEach(d => { IDX[d.cod] = d; });
// Buscar Madrid:
const madrid = IDX['28079'];  // acceso directo, sin búsqueda
// Buscar Barcelona:
const bcn = IDX['08019'];     // acceso directo
// Para 100 búsquedas: 100 operaciones (vs 813.200)
```

## Patrón IDX (España Atlas)

```javascript
// 1. Crear hash index desde array
let IDX = {};
const data = await fetch('./data/core.json').then(r => r.json());
data.forEach(d => { IDX[d.cod] = d; });

// 2. Acceso O(1)
const madrid = IDX['28079'];
console.log(madrid.nom);      // 'Madrid'
console.log(madrid.p25);      // 3223334

// 3. Iterar todos (cuando necesitas)
Object.values(IDX).forEach(d => {
  d.derivedMetric = computeSomething(d);
});

// 4. Buscar con fallback
const item = IDX[codigo] || { nom: 'Desconocido', p25: 0 };
```

## Merge de datasets por key

```javascript
// Dataset base
const base = await fetch('./data/core.json').then(r => r.json());
base.forEach(d => { IDX[d.cod] = d; });  // 8132 registros

// Dataset salud (se fusiona al existente)
const salud = await fetch('./data/health.json').then(r => r.json());
salud.forEach(d => {
  const cod = String(d.cod).padStart(5, '0');
  if (IDX[cod]) {
    Object.assign(IDX[cod], d);  // añade keys de salud al objeto existente
  }
});

// Después del merge, Madrid tiene:
// IDX['28079'] = { cod:'28079', nom:'Madrid', p25:3223334, saludApPor100k18:45.2, ... }
```

## Precomputación de métricas derivadas

```javascript
// Calcular métricas que dependen de TODOS los registros
function computeDerivedMetrics() {
  const rows = Object.values(IDX);

  // 1. Media nacional
  const totalPob = rows.reduce((s, d) => s + (d.p25 || 0), 0);

  // 2. Percentiles para ranking
  const vals = rows.map(d => d.renta23).filter(Number.isFinite).sort((a,b) => a-b);
  const p5 = vals[Math.floor(vals.length * 0.05)];
  const p95 = vals[Math.floor(vals.length * 0.95)];

  // 3. Normalización por registro
  rows.forEach(d => {
    d.pctPob = totalPob > 0 ? (d.p25 / totalPob * 100).toFixed(4) : 0;
    d.rentaPercentile = vals.indexOf(d.renta23) / vals.length * 100;
    d.rentaNorm = Math.max(0, Math.min(100, (d.renta23 - p5) / (p95 - p5) * 100));
  });
}
```

## Lookup table para datos auxiliares

```javascript
// Códigos → nombres (provincias, CCAA, etc.)
const PROV = {
  '28': 'Madrid', '41': 'Sevilla', '08': 'Barcelona',
  '46': 'Valencia', '29': 'Málaga', '15': 'A Coruña'
};

// Mapeo inverso si necesitas
const PROV_BY_NAME = Object.fromEntries(
  Object.entries(PROV).map(([k, v]) => [v, k])
);

// Función helper
function provName(cod) {
  return PROV[String(cod).slice(0, 2)] || 'Desconocida';
}
```

## Métricas percentiles precomputadas

```javascript
// Mapa de percentiles para ranking rápido
function metricPercentileMap(rows, key) {
  const vals = rows
    .map(d => Number(d[key]))
    .filter(Number.isFinite)
    .sort((a, b) => a - b);

  const map = new Map();
  rows.forEach(d => {
    const v = Number(d[key]);
    if (!Number.isFinite(v)) return;
    // Buscar posición (binary search sería más rápido para 8K+)
    let pos = 0;
    while (pos < vals.length && vals[pos] < v) pos++;
    map.set(d.cod, Math.round(pos / vals.length * 100));
  });

  return map;  // { cod → percentil 0-100 }
}

// Usar
const rentaPct = metricPercentileMap(Object.values(IDX), 'renta23');
console.log(rentaPct.get('28079'));  // 95 (percentil 95)
```

## Agrupaciones precomputadas

```javascript
// Agrupar por provincia
const PROV_MUNS = {};
Object.values(IDX).forEach(d => {
  const pr = String(d.cod).slice(0, 2);
  (PROV_MUNS[pr] ??= []).push(d);
});

// Calcular media por provincia
const PROV_MED = {};
Object.entries(PROV_MUNS).forEach(([pr, muns]) => {
  PROV_MED[pr] = {
    avgRenta: arrMedian(muns.map(d => d.renta23).filter(Number.isFinite)),
    count: muns.length
  };
});

// Capital vs resto
const PROV_CAP = { '28': '28079', '41': '41091', '08': '08019' };
const cap = IDX[PROV_CAP['28']];
const rest = PROV_MUNS['28'].filter(d => d.cod !== PROV_CAP['28']);
```

## Iteración segura

```javascript
// Object.values() crea un array nuevo cada vez — cachear si se itera mucho
let cachedValues = null;
let cacheDirty = true;

function getIDXValues() {
  if (cacheDirty || !cachedValues) {
    cachedValues = Object.values(IDX);
    cacheDirty = false;
  }
  return cachedValues;
}

// Marcar como dirty cuando se fusionan datos
function markDirty() {
  cacheDirty = true;
}
```

## Pitfalls

1. **Key normalization** — siempre normalizar: `String(d.cod).padStart(5, '0')`
2. **Object.assign muta** — fusionar con cuidado; el último dataset sobrescribe keys duplicadas
3. **Object.values() es O(n)** — no iterar en cada frame; cachear resultados
4. **Memoria** — 8132 objetos × 50 keys = ~5MB en heap. Con más datasets crece
5. **No confundir con Map()** — `IDX` es un plain object; para keys no-string usar `Map`

## Cuándo usar Map() en vez de object

```javascript
// Object: keys deben ser strings
const IDX = {};
IDX['28079'] = { nom: 'Madrid' };

// Map: keys pueden ser cualquier tipo
constIDX = new Map();
idx.set(28079, { nom: 'Madrid' });  // number key
idx.get(28079);                       // O(1)
```

Para la mayoría de dashboards con codes/IDs string, un plain object es suficiente y más rápido.

## Integración con otros skills

- **lazy-dataset-loading** → cada dataset hace merge en IDX
- **sparse-json-format** → expandir antes de insertar en IDX
- **leaflet-canvas-choropleth** → `styleF()` lee de IDX para colorear
