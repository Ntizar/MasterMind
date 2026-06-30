---
name: leaflet-canvas-choropleth
description: "Patrón completo de choropleth interactivo con Leaflet + Canvas renderer. Miles de polígonos sin lag. 4 escalas de color, pane system, lazy dataset switching. Base para dashboards geodatos vanilla JS."
version: 1.0.0
author: Mastermind
tags: [leaflet, choropleth, canvas, geodata, map, vanilla-js, dashboard]
source: espanatlas.es
---

# Leaflet Canvas Choropleth — Patrón de Referencia

## Cuándo usar
- Dashboard con mapa de áreas coloreadas por datos (municipios, barrios, países)
- >200 polígonos (Canvas obligatorio)
- Cambio de métrica en tiempo real
- Datos vanilla JS sin frameworks

## Stack mínimo

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/topojson-client@3/dist/topojson-client.min.js"></script>
```

## 1. Mapa base con Canvas renderer

```javascript
// CRÍTICO: preferCanvas:true + renderer: L.canvas()
const map = L.map('map', {
  center: [40.1, -3.7],
  zoom: 6,
  preferCanvas: true,     // Canvas por defecto
  zoomSnap: 0.25,
  zoomDelta: 0.25,
  wheelPxPerZoomLevel: 80  // zoom más suave con rueda
});

// Basemap dark
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
  attribution: '© CartoDB © OSM',
  maxZoom: 19,
  subdomains: 'abcd'
}).addTo(map);
```

## 2. Pane system (z-index controlado)

```javascript
// Labels siempre encima del choropleth
map.createPane('labelsPane');
map.getPane('labelsPane').style.zIndex = 450;
map.getPane('labelsPane').style.pointerEvents = 'none';
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}{r}.png', {
  pane: 'labelsPane', attribution: '', maxZoom: 19, subdomains: 'abcd'
}).addTo(map);
```

**Por qué:** Sin panes, las etiquetas del basemap quedan debajo del choropleth. Con pane, controlas el orden de capas independientemente del orden de inserción.

## 3. 4 escalas de color

```javascript
// Escala RdBu divergente (ColorBrewer 9 paradas)
const STOPS = [
  [5,48,97],[33,102,172],[67,147,195],[146,197,222],[247,247,247],
  [244,165,130],[214,96,77],[178,24,43],[103,0,31]
];

// 1. DIVERGENTE: azul → blanco → rojo (variaciones porcentuales)
function getColor(val, lo, hi) {
  if (val == null) return '#1e293b';
  const absMax = Math.max(Math.abs(lo), Math.abs(hi), 0.001);
  const t = Math.max(-1, Math.min(1, val / absMax));
  const s = (t + 1) / 2;  // normalizar -1..1 → 0..1
  const idx = s * (STOPS.length - 1);
  const li = Math.floor(idx), hi_i = Math.min(li + 1, STOPS.length - 1);
  const f = idx - li;
  const [r, g, b] = [0,1,2].map(i =>
    Math.round(STOPS[li][i] + (STOPS[hi_i][i] - STOPS[li][i]) * f)
  );
  return `rgb(${r},${g},${b})`;
}

// 2. SECUENCIAL: blanco → rojo (tasas absolutas)
function getColorSeq(val, lo, hi) {
  if (val == null) return '#1e293b';
  const t = Math.max(0, Math.min(1, (val - lo) / (hi - lo || 1)));
  const idx = 4 + t * 4;  // usa stops 4→8 (blanco→rojo)
  const li = Math.floor(idx), hi_i = Math.min(li + 1, STOPS.length - 1);
  const f = idx - li;
  const [r, g, b] = [0,1,2].map(i =>
    Math.round(STOPS[li][i] + (STOPS[hi_i][i] - STOPS[li][i]) * f)
  );
  return `rgb(${r},${g},${b})`;
}

// 3. SCORE: rojo → verde (0-100, scores/índices)
function getColorScore(val) {
  if (val == null || !isFinite(val)) return '#1e293b';
  const t = Math.max(0, Math.min(1, Number(val) / 100));
  const stops = [[220,38,38],[249,115,22],[245,158,11],[132,204,22],[22,163,74]];
  const idx = t * (stops.length - 1);
  const li = Math.floor(idx), hi_i = Math.min(li + 1, stops.length - 1);
  const f = idx - li;
  const [r,g,b] = [0,1,2].map(i =>
    Math.round(stops[li][i] + (stops[hi_i][i] - stops[li][i]) * f)
  );
  return `rgb(${r},${g},${b})`;
}

// 4. RISK: verde → rojo oscuro (0-100, riesgos)
function getColorRisk(val) {
  if (val == null || !isFinite(val)) return '#1e293b';
  const t = Math.max(0, Math.min(1, Number(val) / 100));
  const stops = [[22,163,74],[132,204,22],[245,158,11],[249,115,22],[220,38,38],[127,29,29]];
  const idx = t * (stops.length - 1);
  const li = Math.floor(idx), hi_i = Math.min(li + 1, stops.length - 1);
  const f = idx - li;
  const [r,g,b] = [0,1,2].map(i =>
    Math.round(stops[li][i] + (stops[hi_i][i] - stops[li][i]) * f)
  );
  return `rgb(${r},${g},${b})`;
}

// Percentil para rangos robustos
function pct95(arr, p) {
  const s = arr.filter(v => v != null).sort((a,b) => a-b);
  return s[Math.floor(s.length * p / 100)] ?? 0;
}
```

## 4. Categorías con colores fijos

```javascript
const CAT_COLORS = {
  elecciones: { PSOE:'#ef4444', PP:'#2563eb', VOX:'#65a30d', SUMAR:'#ec4899' },
  tipos: { A:'#f87171', B:'#f97316', C:'#fbbf24', D:'#94a3b8', E:'#34d399' },
};

// Función para buscar color categórico
function categoricalColor(metric, value) {
  return CAT_COLORS[metric]?.[value] || '#94a3b8';
}
```

## 5. GeoJSON layer con Canvas + estilo dinámico

```javascript
let geoLayer, curMetric = 'variacion', lo = 0, hi = 0;

function styleF(feat) {
  const d = feat.properties.data || {};
  let fill;

  if (curMetric in CAT_COLORS) {
    fill = categoricalColor(curMetric, d[curMetric]);
  } else if (curMetric.includes('score') || curMetric.includes('index')) {
    fill = getColorScore(d[curMetric]);
  } else if (curMetric.includes('risk') || curMetric.includes('flood')) {
    fill = getColorRisk(d[curMetric]);
  } else {
    fill = getColor(d[curMetric], lo, hi);  // divergente por defecto
  }

  return {
    fillColor: fill,
    fillOpacity: d.cod ? 0.83 : 0.07,
    color: '#0f172a',
    weight: 0.35,
    opacity: 0.8
  };
}

// Crear layer una sola vez
geoLayer = L.geoJSON(geoData, {
  style: styleF,
  onEachFeature: (feat, layer) => {
    layer.on('mouseover', () => layer.setStyle({ weight: 2, color: '#c7d2fe', fillOpacity: 0.95 }));
    layer.on('mouseout', () => geoLayer.resetStyle(layer));
    layer.on('click', () => showMunicipalityInfo(feat.properties.cod));
  },
  renderer: L.canvas()  // ← CRÍTICO para rendimiento
}).addTo(map);
```

## 6. Cambio de métrica SIN reconstruir (el truco clave)

```javascript
// NO HACER (lento):
// map.removeLayer(geoLayer);
// geoLayer = L.geoJSON(nuevoGeo, { style: styleF }).addTo(map);

// SÍ HACER (10ms):
async function updateMap() {
  curMetric = document.getElementById('metric-select').value;

  // Cargar dataset si no está cacheado
  const ds = datasetForMetric(curMetric);
  if (DATASET_STATUS[ds] !== 'loaded') {
    await loadDataset(ds);
  }

  // Calcular rangos
  const vals = Object.values(IDX).map(d => d[curMetric]).filter(Number.isFinite);
  lo = pct95(vals, 5);
  hi = pct95(vals, 95);

  // RE-COLOREAR sin tocar geometría ← ¡la magia!
  geoLayer.setStyle(styleF);

  // Actualizar leyenda
  updateLegend();
}
```

## 7. Tooltip informativo

```javascript
function onEachFeature(feat, layer) {
  layer.bindTooltip(() => {
    const d = feat.properties;
    return `<b>${d.nom}</b><br>${curMetric}: ${formatValue(d[curMetric])}`;
  }, { sticky: true, className: 'custom-tooltip' });
}
```

## Pitfalls

1. **Canvas + interactividad:** Los eventos de mouse en Canvas son por bounding box, no por forma exacta. Para polígonos muy pequeños, usar `tolerance` en `L.canvas({tolerance: 5})`
2. **No recrear el layer:** `setStyle()` es 50x más rápido que destruir+crear
3. **Percentiles, no min/max:** Usar pct5/pct95 para rangos, no min/max (outliers rompen la escala)
4. **Liberar memoria TopoJSON:** `topo = null` tras `topojson.feature()`
5. **Canvas no soporta CSS:** Los estilos CSS no funcionan en Canvas renderer
6. **clientWidth=0 en tabs lazy:** Cuando un contenedor está oculto (`display:none`), `container.clientWidth` es 0. SVGs/Charts creados en ese momento quedan con width negativo o cero → invisibles. Fix: `Math.max(600, container.clientWidth)` o `requestAnimationFrame` + retry.
7. **GeoJSON property names:** SpainLayers usa `id`/`name`, no `CODMUN`/`NOMBRE`. Siempre verificar y mapear propiedades al cargar.

## GeoJSON de municipios españoles — SpainLayers

### Fuente fiable: `AlexGPlay/SpainLayers`

Tras probar 15+ fuentes (datos.comunidad.madrid, opendata-pmm, semmler23, Fonsloper, GADM, etc.), la **única fuente que funciona** para GeoJSON de municipios españoles a nivel provincial:

```
https://raw.githubusercontent.com/AlexGPlay/SpainLayers/master/municipalities/{PROVINCIA_CODE}.geojson
```

- **Madrid:** `28.geojson` → 179 municipios, ~5.9MB
- **Barcelona:** `08.geojson`
- **Valencia:** `46.geojson`
- **Código provincia:** 2 dígitos (01-52 + 57)

### Propiedades (¡OJO al mapeo!)

```json
{
  "type": "Feature",
  "properties": {
    "id": "28079",      // ← usa "id", NO "CODMUN"
    "name": "Madrid"    // ← usa "name", NO "NOMBRE"
  },
  "geometry": { "type": "MultiPolygon", "coordinates": [...] }
}
```

**Pitfall crítico:** Si tu dataset usa `CODMUN` o `NOMBRE`, hay que mapear:
```javascript
// Mapear propiedades al cargar
geo.features.forEach(f => {
  f.properties.CODMUN = f.properties.id;
  f.properties.NOMBRE = f.properties.name;
});
```

### Douglas-Peucker — simplificar GeoJSON grande

GeoJSON provincial puede pesar 5-15MB. Simplificar con tolerancia:

```python
def simplify_ring(coords, tolerance=0.002):
    """Douglas-Peucker simplification para un ring"""
    if len(coords) <= 3:
        return coords
    def point_line_dist(p, a, b):
        dx, dy = b[0]-a[0], b[1]-a[1]
        if dx == 0 and dy == 0:
            return ((p[0]-a[0])**2 + (p[1]-a[1])**2)**0.5
        t = max(0, min(1, ((p[0]-a[0])*dx + (p[1]-a[1])*dy) / (dx*dx + dy*dy)))
        return ((p[0]-(a[0]+t*dx))**2 + (p[1]-(a[1]+t*dy))**2)**0.5
    
    max_dist, max_idx = 0, 0
    for i in range(1, len(coords)-1):
        d = point_line_dist(coords[i], coords[0], coords[-1])
        if d > max_dist:
            max_dist, max_idx = d, i
    
    if max_dist > tolerance:
        left = simplify_ring(coords[:max_idx+1], tolerance)
        right = simplify_ring(coords[max_idx:], tolerance)
        return left[:-1] + right
    return [coords[0], coords[-1]]

def simplify_geojson(geo, tolerance=0.002):
    """Simplificar todas las features de un GeoJSON"""
    for f in geo['features']:
        geom = f['geometry']
        if geom['type'] == 'MultiPolygon':
            geom['coordinates'] = [
                [simplify_ring(ring, tolerance) for ring in polygon]
                for polygon in geom['coordinates']
            ]
        elif geom['type'] == 'Polygon':
            geom['coordinates'] = [
                simplify_ring(ring, tolerance) for ring in geom['coordinates']
            ]
    return geo
```

**Tolerancia recomendada:**
- `0.001` (~100m) — alta fidelidad, ~60% reducción
- `0.002` (~200m) — buena fidelidad, ~80-96% reducción (recomendado)
- `0.005` (~500m) — baja fidelidad, ~98% reducción

**Resultado real (Madrid):** 5.9MB → 214KB con tolerancia 0.002 (96% reducción), 149K → 4.8K coordenadas.

## Preferencias de usuario (David) — dashboards geodatos

1. **Polígonos REALES, nunca approximaciones** — Hexágonos, círculos o grid no satisfacen. Usar GeoJSON real de municipios (SpainLayers). Si no hay GeoJSON descargable, Douglas-Peucker con tolerancia 0.002 es aceptable como último recurso, pero la Meta es boundaries reales.
2. **NO circle markers en choropleth** — El usuario dice "los municipios salen como bolas y no funciona bien". Solo polígonos + labels de texto. Los circle markers solo para entidades sin polígono (provincias externas, distritos).
3. **Explicar cada métrica** — "no explican qué es la autocontención". Todo KPI, ratio o indicador derivado DEBE tener un tooltip o ℹ️ con definición clara. El usuario no asume conocimiento técnico.
4. **Flujos bidireccionales en tabla** — El usuario prefiere ver A→B Y B→A por separado (heatmap matrix) a solo flujos netos (Sankey). La matriz 11×11 con celdas coloreadas es más clara que un Sankey para datos OD.
5. **Incluir datos externos del Excel** — Si el Excel tiene entradas de "PROVINCIA DE ÁVILA" o "RESTO DE ESPAÑA", incluirlas en la visualización como marcadores especiales. No filtrar sin preguntar.
6. **Distritos de Madrid** — El usuario pide repetidamente "Madrid por código postal". Añadir layer toggle con distritos (21) como marcadores separados con stats propios.

## Integración con otros skills

- **topojson-performance** → cargar geometrías comprimidas
- **sparse-json-format** → datos compactos por municipio
- **lazy-dataset-loading** → carga escalonada de datasets
- **gtfs-browser-parser** → overlay de rutas de transporte público en mapas geodatos
