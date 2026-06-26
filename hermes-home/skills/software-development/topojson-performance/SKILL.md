---
name: topojson-performance
description: "Compresión geográfica con TopoJSON: 70% menos de tamaño que GeoJSON, conversión en runtime, liberación de memoria. Patrón para cargar geometrías de países, municipios o barrios en dashboards web."
version: 1.0.0
author: Mastermind
tags: [topojson, geodata, performance, compression, geojson, vanilla-js]
source: espanatlas.es
---

# TopoJSON Performance — Compresión Geográfica

## Cuándo usar
- Cargar geometrías de áreas (municipios, barrios, provincias, países)
- Archivos GeoJSON >2MB que causan carga lenta
- Miles de polígonos con bordes compartidos
- Dashboards estáticos sin backend

## ¿Por qué TopoJSON?

| Formato | España municipal | World countries |
|---------|-----------------|-----------------|
| GeoJSON | ~18 MB | ~5 MB |
| TopoJSON | ~6 MB | ~1.2 MB |
| **Ahorro** | **67%** | **76%** |

TopoJSON almacena **arcs** (segmentos compartidos) en vez de polígonos completos. Los bordes entre municipios vecinos se escriben una sola vez.

## CDN

```html
<script src="https://cdn.jsdelivr.net/npm/topojson-client@3/dist/topojson-client.min.js"></script>
```

## Conversión en runtime

```javascript
// 1. Cargar TopoJSON
const resp = await fetch('./data/municipios_topo.json');
const topo = await resp.json();

// 2. Convertir a GeoJSON (FeatureCollection)
const geo = topojson.feature(topo, topo.objects.municipios);

// 3. LIBERAR memoria del TopoJSON raw (pesado)
topo = null;

// 4. Usar con Leaflet
L.geoJSON(geo, { style: styleF, renderer: L.canvas() }).addTo(map);
```

## Convención de objetos

En TopoJSON, los polígonos están bajo `topo.objects`:

```json
{
  "type": "Topology",
  "objects": {
    "municipios": {        // ← nombre del objeto (arbitrario)
      "type": "GeometryCollection",
      "geometries": [...]
    }
  },
  "arcs": [...],           // ← bordes comprimidos
  "transform": { ... }     // ← escala opcional
}
```

Para convertir: `topojson.feature(topo, topo.objects.municipios)`

## Generar TopoJSON desde Shapefile

```bash
# Instalar toolchain
npm install -g mapshaper topojson-server topojson-client

# 1. Shapefile → TopoJSON (con simplificación)
mapshaper municipios.shp \
  -simplify 10% keep-shapes \
  -o format=topojson municipios_topo.json \
  --id-field COD_MUNICI

# 2. GeoJSON → TopoJSON
geo2topo municipios=municipios.geojson > municipios_topo.json

# 3. TopoJSON → GeoJSON (para inspeccionar)
topo2geo municipios=- < municipios_topo.json
```

## Simplificación inteligente

```bash
# Preservar shapes importantes al simplificar
mapshaper municipios.shp \
  -simplify 5% keep-shapes \
  -filter-fields COD_MUNICI,NOMBRE \
  -o format=topojson id-field=COD_MUNICI output.json

# Parámetros:
# -simplify 5%  → reducir 95% de vértices (ajustar según calidad necesaria)
# keep-shapes   → preservar polígonos muy pequeños
# -filter-fields → solo conservar campos necesarios (reduce tamaño)
```

## Precisión de coordenadas

```bash
# Reducir decimales (menos precisión = menos tamaño)
mapshaper input.shp \
  -proj wgs84 \
  -o format=topojson precision=0.001 output.json
# precision=0.001 = ~100m de precisión (suficiente para municipios)
```

## Propiedades por feature

```javascript
// Cada feature tiene properties
geo.features.forEach(f => {
  console.log(f.properties.cod);     // código municipal
  console.log(f.properties.nom);     // nombre
  console.log(f.properties);         // todos los campos del shapefile
});
```

## Pitfalls

1. **`topo = null` después de conversión** — sin esto, mantienes 2 copias en memoria
2. **No confundir `objects` keys** — `topo.objects.municipios`, no `topo.features`
3. **Simplificación agresiva borra islas pequeñas** — usar `keep-shapes`
4. **Canvas renderer** — obligatorio para >500 polígonos, ver skill `leaflet-canvas-choropleth`
5. **Presición** — `precision=0.001` es suficiente para mapas a nivel municipal

## Generar datos de prueba

```javascript
// Crear TopoJSON de prueba con 100 polígonos aleatorios
const { default: topojson } = await import('https://cdn.jsdelivr.net/npm/topojson-client@3/+esm');
```

## Integración con otros skills

- **leaflet-canvas-choropleth** → consumir el GeoJSON resultante
- **lazy-dataset-loading** → cargar TopoJSON como primer dataset
