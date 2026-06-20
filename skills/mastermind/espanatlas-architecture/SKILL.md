---
name: espanatlas-architecture
description: "Arquitectura completa de España Atlas (espanatlas.es) — atlas municipal español con 8.132 municipios, choropleth Leaflet, TopoJSON, 20+ datasets, Canvas renderer, lazy loading. Patrón de referencia para dashboards geodatos vanilla JS."
version: 1.0.0
author: Mastermind
tags: [espanatlas, geodatos, leaflet, choropleth, dashboard, vanilla-js, topjson, cartodb]
---

# España Atlas — Arquitectura de Referencia

## Resumen

**espanatlas.es** es un atlas municipal español con 8.132 municipios, 20+ datasets temáticos, rankings, correlaciones y análisis automatizados. Toda la app está en **un solo HTML** (~1MB, 16.379 líneas) con JS vanilla, sin frameworks.

**Autor original:** @CalcetinLetal
**Fuentes:** INE, SEPE, Min. Interior, AEAT, AEMET, SNCZI, DGT

## Stack Tecnológico

| Componente | Tecnología | Versión |
|---|---|---|
| **Mapa** | Leaflet.js | 1.9.4 |
| **Basemap** | CartoDB dark (nolabels + labels separados) | — |
| **Geometrías** | TopoJSON → GeoJSON (topojson-client 3.x) | — |
| **Renderer** | L.canvas() (NO SVG — rendimiento con miles de polígonos) | — |
| **Framework** | Ninguno — vanilla JS + DOM directo | — |
| **Hosting** | Estático (sin backend) | — |

## Arquitectura de Datos

### Datos geográficos
- **Archivo:** `./data/municipios_topo.json` (~5.9 MB TopoJSON)
- **Objeto:** `topo.objects.municipios`
- **Conversión:** `topojson.feature(topo, topo.objects.municipios)` → FeatureCollection
- **Cada feature** tiene `properties.cod` (código municipal INE, 5 dígitos)
- Se liberan memoria inmediatamente: `topo = null` tras conversión

### Datos temáticos (20+ archivos lazy-loaded)
Cada dataset es un JSON array con objetos `[{cod, nom, prov, acom, ...metricas}]`:

| Archivo | Contenido | ~Tamaño |
|---|---|---|
| `budget_municipal_metrics_sparse_part1.json` | Presupuestos (parte 1) | ~5 MB |
| `budget_municipal_metrics_sparse_part2.json` | Presupuestos (parte 2) | ~5 MB |
| `health_municipal_metrics.json` | Salud (7.4 MB) | 8.132 filas |
| `elecciones_2023.json` | Elecciones municipales 2023 | ~10 MB |
| `census_income_municipal.json` | Renta censal | — |
| `business_type_metrics.json` | Tejido empresarial | — |
| `immigration_municipal_metrics.json` | Inmigración | — |
| `roma_municipal_metrics.json` | Población gitana | — |
| `air_quality_municipal_metrics.json` | Calidad del aire | — |
| `road_safety_municipal_metrics.json` | Siniestralidad vial | — |
| `wildfire_municipal_metrics.json` | Incendios forestales | — |
| `irpf_municipal_metrics.json` | IRPF AEAT | — |
| `flood_municipal_metrics.json` | Inundaciones SNCZI | — |
| `broadband_municipal_metrics.json` | Conectividad digital | — |
| `aemet_temperature_municipal_metrics.json` | Temperatura AEMET | — |
| `policy_budget_model.json` | Modelo política-presupuesto | — |
| `nap_gtfs_municipal_metrics.json` | Transporte público GTFS | — |
| `education_centers_municipal_metrics.json` | Centros educativos | — |
| `historical_population_ageing_metrics.json` | Historia municipal | — |
| `birthplace_relation_metrics.json` | Origen residencial | — |

### Datos complementarios
- **Secciones censales:** Lazy-loaded desde INE GeoServer (`geoserver/ogc/features/v1/collections/WMS_INE_SECCIONES_G01`)
- **Pirámides demográficas:** `./data/pyramids_proj_2035_2050/index.json`
- **Secciones censales geo:** `./data/census_sections_2023/index.json` + archivos por provincia
- **Geopolítica:** GeoJSON embebido para Sáhara Occidental y Palestina

## Patrón de Carga de Datos

```javascript
// 1. Datos principales se cargan por categorías (lazy)
const DATASETS = {
  base: async () => {
    // Dataset core: siempre se carga
    await fetchWithProgress('./data/main_metrics.json', 'Base', 0, 8);
  },
  health: async () => mergeMetricRows(
    await fetchWithProgress('./data/health_municipal_metrics.json', 'Salud', 8, 18),
    'Salud'
  ),
  elec: async () => { /* elecciones */ },
  // ... 20+ datasets
};

// 2. Carga escalonada para no bloquear
async function preloadDatasetsStaggered(keys, onDone) {
  for (const key of keys) {
    await runIdle(() => ensureDataset(key));
  }
  onDone?.();
}

// 3. requestIdleCallback para no bloquear UI
function runIdle(fn, timeout = 2000) {
  if ('requestIdleCallback' in window) requestIdleCallback(fn, { timeout });
  else setTimeout(fn, 100);
}
```

## Sistema de Colores

### Paleta RdBu (divergente) — 9 paradas
```javascript
const STOPS = [
  [5,48,97],[33,102,172],[67,147,195],[146,197,222],[247,247,247],
  [244,165,130],[214,96,77],[178,24,43],[103,0,31]
];
// Azul (negativo) → Blanco (0) → Rojo (positivo)
```

### Funciones de color (4 escalas)
1. **`getColor(val, lo, hi)`** — Divergente RdBu para variaciones
2. **`getColorSeq(val, lo, hi)`** — Secuencial blanco→rojo para tasas absolutas
3. **`getColorScore(val)`** — Verde→rojo (0-100) para scores/índices
4. **`getColorRisk(val)`** — Verde→rojo→rojo oscuro (0-100) para riesgos

### Colores categóricos
```javascript
const CAT_COLORS = {
  elec23_ganador: { PSOE:'#ef4444', PP:'#2563eb', VOX:'#65a30d', SUMAR:'#ec4899', ... },
  tipoCluster: {'0':'#f87171','1':'#f97316','2':'#fbbf24','3':'#94a3b8','4':'#34d399','5':'#60a5fa','6':'#818cf8'},
  crecTipo: { dinamico:'#4ade80', atraccion:'#60a5fa', nativo:'#34d399', ... },
};
```

### Rank map (bandas percentiles)
```javascript
const RANK_BAND_COLORS = {
  top1:'#14532d', top5:'#15803d', top10:'#22c55e', high:'#86efac',
  mid:'#94a3b8',
  low:'#fdba74', bot10:'#f97316', bot5:'#dc2626', bot1:'#7f1d1d'
};
```

## Gestión de Páneas Leaflet

```javascript
// Labels pane — z-index 450, siempre encima del choropleth
map.createPane('labelsPane');
map.getPane('labelsPane').style.zIndex = 450;
map.getPane('labelsPane').style.pointerEvents = 'none';
L.tileLayer('dark_only_labels', { pane: 'labelsPane' }).addTo(map);

// Census pane — z-index 430, entre choropleth y labels
map.createPane('censusPane');
map.getPane('censusPane').style.zIndex = 430;

// Territory pane — z-index 455, encima de todo
map.createPane('territoryPane');
map.getPane('territoryPane').style.zIndex = 455;
```

## Canvas Renderer (CRÍTICO para rendimiento)

```javascript
// SIEMPRE usar Canvas para miles de polígonos
geoLayer = L.geoJSON(geo, {
  style: styleF,
  onEachFeature: onEach,
  renderer: L.canvas()  // NO L.svg()
}).addTo(map);
```

**¿Por qué?** SVG genera un DOM node por polígono. Con 8.132 municipios = 8.132 nodos SVG → lag. Canvas pinta todo en un solo elemento `<canvas>`.

## Choropleth Pattern

```javascript
function styleF(feat) {
  const cod = feat.properties.cod;
  const d = cod ? (IDX[cod] || {}) : {};
  let fill;

  if (RANK_MAP_ON && rankMapAvailable(curM)) {
    fill = rankMapColor(d);
  } else if (CATEGORICAL_M.has(curM)) {
    const cv = metricValueFor(d);
    fill = cv != null ? ((CAT_COLORS[curM]?.[cv]) || '#94a3b8') : '#1e293b';
  } else if (SCORE_M.has(curM)) {
    fill = getColorScore(metricValueFor(d));
  } else {
    fill = getColor(metricValueFor(d), lo, hi);  // divergente por defecto
  }

  return {
    fillColor: fill,
    fillOpacity: cod ? 0.83 : 0.07,
    color: '#0f172a',
    weight: 0.35,
    opacity: 0.8
  };
}
```

## Layout de UI

### Top bar (controles)
```css
#ctrl {
  position: absolute;
  top: 12px;
  left: 50%; transform: translateX(-50%);
  background: rgba(15,23,42,.95);
  backdrop-filter: blur(8px);
  border-radius: 14px;
  border: 1px solid rgba(99,102,241,.3);
  box-shadow: 0 8px 32px rgba(0,0,0,.7);
}
```

### Panel lateral (colapsable)
- Secciones: Resumen Nacional, Rankings, Correlaciones, Índices Sintéticos
- Toggle con clase `collapsed` + botón `+`/`-`
- Cada sección tiene `renderTab` lazy

### Búsqueda
- Ctrl+K para buscar municipio
- Panel de selección de mapa con búsqueda por nombre
- Sinónimos para métricas: `MAP_SEARCH_SYNONYMS`

## Funcionalidades Principales

1. **Choropleth interactivo** — cambio de métrica en tiempo real
2. **Rankings** — top 10 / bottom 10 de cualquier métrica
3. **Correlaciones** — scatter plots entre métricas (Chart.js)
4. **Índices Sintéticos** — scoring compuesto 0-100
5. **Municipio Ideal** — filtros combinados para encontrar el "mejor"
6. **Comparación** — `/comparar/?a=XXX&b=YYY`
7. **Municipios similares** — grafo kNN con comunidades Leiden
8. **Secciones censales** — zoom > 8 carga datos del INE
9. **Descarga** — export PNG del mapa
10. **Compartir** — URL con estado codificado (m, cod, lat, lng, z)

## Fuentes de Datos (APIs)

| Fuente | Tipo | Uso |
|---|---|---|
| INE | CSV/API | Población, renta, censos, secciones censales |
| SEPE | CSV | Empleo, paro registrado |
| Min. Interior | CSV | Elecciones municipales |
| AEAT | CSV | IRPF municipal |
| AEMET | API | Temperaturas, calidad del aire |
| SNCZI | WFS | Zonas inundables |
| DGT | CSV | Siniestralidad vial |
| Catastro | API | Valor catastral, tipología |
| GTFS | Archivos | Transporte público |
| BDNS | API | Subvenciones públicas |

## Arquitectura de Rendimiento (Deep Dive)

Cómo 8.132 municipios + 20+ datasets caben en un single-page vanilla JS con TTFB 158ms.

### 1. TopoJSON → GeoJSON con liberación inmediata

TopoJSON comparte bordes entre polígonos vecinos (~70% menos que GeoJSON puro). Se convierte una sola vez y se libera:

```javascript
let topo = await fetch('./data/municipios_topo.json');  // 5.9 MB
const geo = topojson.feature(topo, topo.objects.municipios);
topo = null; // ← libera 5.9MB de memoria inmediatamente
```

**Regla:** Siempre TopoJSON para geometrías. GeoJSON puro = 15-20 MB para los mismos datos.

### 2. Canvas renderer (el truco más importante)

```javascript
L.geoJSON(geo, { renderer: L.canvas() })  // NO L.svg()
```

SVG genera **un nodo DOM por polígono** → 8.132 nodos SVG = lag. Canvas pinta todo en **un solo `<canvas>`** como un videojuego. Diferencia: ~50x en rendimiento para >500 polígonos.

**Regla:** Siempre Canvas para >500 polígonos. SVG solo para <100 con interacciones complejas por feature.

### 3. Hash index `IDX` — acceso O(1) por código

```javascript
let IDX = {};
muni.forEach(d => { IDX[d.cod] = d; });
// Después: IDX['28079'] → acceso directo, sin búsqueda
```

No hay arrays que recorrer para encontrar un municipio. Merge de datasets posteriores usa `Object.assign(IDX[cod], d)` para añadir métricas al objeto existente.

### 4. Re-render sin reconstruir — `setStyle()`

Cuando el usuario cambia de métrica:
```javascript
// ❌ MALO: destruir y recrear la capa completa
map.removeLayer(geoLayer);
geoLayer = L.geoJSON(nuevoGeo, { style: nuevoStyle }).addTo(map);

// ✅ BUENO: re-aplicar estilo a geometría existente
geoLayer.setStyle(styleF);  // ← re-colorea 8.132 polígonos SIN tocar geometría
```

La geometría (pesada, 5.9MB) no se toca. Solo cambian los colores (~10ms).

### 5. Sparse rows — compresión de datos tabulares

Los archivos de presupuestos usan formato compacto para evitar repetir nombres de métricas:

```javascript
// Formato sparse: keys se escribe UNA vez, cada fila solo referencia índices
{ keys: ["gastoTotal","inversion","deuda",...],  // 50+ nombres, una vez
  rows: [["28079", [0, 1234, 1, 567, ...]],      // Madrid: [índice, valor, índice, valor]
         ["07019", [0, 890, 1, 234, ...]]] }     // Palma

function expandSparseRows(payload) {
  return payload.rows.map(row => {
    const out = { cod: row[0] };
    for (let i = 0; i < row[1].length; i += 2)
      out[payload.keys[row[1][i]]] = row[1][i + 1];
    return out;
  });
}
```

Reduce el JSON un ~40% comparado con objetos completos.

### 6. Carga lazy escalonada por categorías

Los 20+ datasets NO se cargan todos al inicio:

```
Fase 1 (siempre): municipios_core.json → IDX[hash] → 8.132 objetos
Fase 2 (siempre): municipios_topo.json → TopoJSON → GeoJSON → Canvas
Fase 3 (on demand): datasets temáticos → merge en IDX cuando usuario cambia métrica
```

```javascript
async function ensureDataset(key) {
  if (DATASET_STATUS[key] === 'loaded') return;  // ya cacheado
  // ... fetch y merge
  DATASET_STATUS[key] = 'loaded';
}

// En updateMap():
const missing = datasets.filter(ds => DATASET_STATUS[ds] !== 'loaded');
if (missing.length) await Promise.all(missing.map(ensureDataset));
```

### 7. `requestIdleCallback` para carga no bloqueante

```javascript
function runIdle(fn, timeout = 2000) {
  if ('requestIdleCallback' in window) requestIdleCallback(fn, { timeout });
  else setTimeout(fn, 100);  // fallback para Safari
}

// Preload de datasets secundarios cuando el navegador está libre
runIdle(() => preloadDatasetsStaggered(['elec','health','roma']), 1800);
```

### 8. Precomputación en carga inicial

Al arrancar, calcula todo lo que pueda para evitar recálculos posteriores:

```javascript
// Log-densidad, log-población (para k-means y mapa)
Object.values(IDX).forEach(d => {
  if (d.densidad > 0) d.logDens = Math.log10(d.densidad);
  if (d.p25 > 0) d.logPop = Math.log10(d.p25);
});
// % de población nacional
const totalPob25 = Object.values(IDX).reduce((s, d) => s + (d.p25 || 0), 0);
// Medianas por provincia (capital vs resto)
PROV_ROWS.forEach(([k]) => {
  PROV_MED_REST[pr][k] = arrMedian(rest.map(d => d[k]));
});
```

### 9. Pane system — z-index sin reordenar capas

En vez de reordenar capas (costoso), usa panes con z-index fijo:
- `overlayPane` (400): choropleth
- `censusPane` (430): secciones censales
- `labelsPane` (450): etiquetas del basemap (pointer-events: none)
- `territoryPane` (455): Sáhara, Palestina

### 10. fetch con streaming de progreso

```javascript
async function fetchWithProgress(url, label, from, to) {
  const resp = await fetch(url);
  const reader = resp.body.getReader();
  const chunks = [];
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    // Actualizar barra de progreso en tiempo real
  }
  const all = new Uint8Array(chunks.reduce((a, c) => a + c.length, 0));
  return JSON.parse(new TextDecoder().decode(all));
}
```

### Resumen del flujo de rendimiento

```
Carga inicial (~250ms):
  municipios_core.json → IDX[hash] → 8.132 objetos en memoria
  → municipios_topo.json → TopoJSON → GeoJSON → Canvas layer
  → geoLayer.setStyle(styleF) → choropleth listo

Cambio de métrica (~10ms):
  Cargar dataset si no está cacheado → merge en IDX
  → geoLayer.setStyle(styleF) → re-colorea 8.132 polígonos
  → buildRankings() → ordena y pinta sidebar
```

## Skills Derivados (reutilizables)

| Skill | Categoría | Patrón |
|---|---|---|
| `leaflet-canvas-choropleth` | software-development | Mapa interactivo con Canvas + 4 escalas de color |
| `topojson-performance` | software-development | Compresión geográfica 70% |
| `sparse-json-format` | software-development | JSON compacto 40-60% menos |
| `lazy-dataset-loading` | software-development | Carga progresiva por demanda |
| `hash-index-data` | software-development | Acceso O(1) con idx hash |

## Lecciones para Replicar

### SÍ hacer
- ✅ Canvas renderer para >500 polígonos
- ✅ TopoJSON (compresión superior a GeoJSON puro)
- ✅ Lazy loading de datasets temáticos
- ✅ Pane system para z-index controlado
- ✅ requestIdleCallback para carga no bloqueante
- ✅ Datos embebidos en HTML si son críticos (Sáhara, Palestina)
- ✅ Búsqueda con sinónimos
- ✅ URL state para compartir vistas
- ✅ Metadata rica (LD+JSON, OG tags)

### NO hacer
- ❌ SVG renderer con >1000 polígonos
- ❌ Cargar todos los datasets al inicio
- ❌ GeoJSON sin TopoJSON (doble de tamaño)
- ❌ Canvas sin L.canvas() explícito
- ❌ z-index manual sin sistema de panes
- ❌ Hexágonos approximados en vez de boundaries reales — los usuarios notan la diferencia

### Fuentes GeoJSON para municipios españoles

Si no tienes TopoJSON propio, la fuente fiable es **AlexGPlay/SpainLayers**:
```
https://raw.githubusercontent.com/AlexGPlay/SpainLayers/master/municipalities/{PROVINCIA}.geojson
```
- 179 municipios Madrid = 5.9MB → simplificar con Douglas-Peucker (tolerancia 0.002) → 214KB
- Propiedades: `id` (código INE) y `name` (nombre municipio)
- Ver `leaflet-canvas-choropleth` para código de simplificación y mapeo de propiedades

## Patrón de Reutilización

Para crear un atlas similar con otros datos:

1. **Preparar TopoJSON** de las geometrías (municipios, barrios, países)
2. **Crear JSONs** por categoría con `{cod, nom, ...métricas}`
3. **Implementar 4 escalas de color** (divergente, secuencial, score, risk)
4. **Montar Leaflet** con Canvas + panes
5. **Lazy load** datasets por categoría
6. **Añadir sidebar** con rankings, correlaciones, filtros
7. **URL state** para compartir
