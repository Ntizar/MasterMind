# GeoJSON, Choropleths y Flujos — Referencia AtlasMadrid2024

## Fuentes GeoJSON para municipios españoles

**NO intentar datos.comunidad.madrid** — timeout siempre.

| Fuente | URL | Resultado |
|--------|-----|-----------|
| ✅ SpainLayers | `https://raw.githubusercontent.com/AlexGPlay/SpainLayers/master/municipalities/{CODPROV}.geojson` | Funciona. Props: `{id:"28092", name:"Móstoles"}` |
| ✅ GADM nivel 2 | `https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_ESP_2.json` | Solo provincia, NO municipal |
| ❌ CM GeoServer | datos.comunidad.madrid WFS endpoints | Timeout |
| ❌ GitHub search | "municipios madrid geojson" | 404s |

Codificación provincias: 28=Madrid, 05=Ávila, 16=Cuenca, 19=Guadalajara, 40=Segovia, 45=Toledo.

## Centroides: SIEMPRE desde GeoJSON

```python
# BIEN: centroides desde polígonos reales
for f in geojson['features']:
    coords = []
    for poly in f['geometry']['coordinates']:
        for ring in poly:
            coords.extend(ring)
    avg_lng = sum(c[0] for c in coords) / len(coords)
    avg_lat = sum(c[1] for c in coords) / len(coords)
```

**Pitfall AtlasMadrid2024:** 179 centroides generados algorítmicamente → 172 con errores 80-115km. Labels de municipios en posiciones completamente equivocadas.

## Simplificación GeoJSON

GeoJSON municipal ~6MB → Douglas-Peucker tolerancia 0.002 → ~200KB (96% reduction). Coords: 149K → 5K. Forma recognoscible preservada.

## Sankey vs Matriz de Flujos

d3-sankey NO soporta ciclos ni bidireccional. Para datos OD:
- **Sankey:** Solo flujos netos (A→B si net > 0). Perde dirección original.
- **Matriz heatmap 11×11:** Muestra A→B y B→A explícitamente. SUPERIOR para análisis OD.

## Choropleth: Sin Circle Markers

Si hay GeoJSON polygons → NO añadir L.circleMarker. Solo polygons + text labels (L.divIcon). Usuario rechazó "bolas" explícitamente.

## Chart.js Rankings — Patrones

- Value labels en cada barra (datalabelPlugin inline)
- Gradientes: `rgba(R,G,B,${0.95 - i*0.04})`
- Formato K/M: `n >= 1e6 ? (n/1e6).toFixed(1)+'M' : n >= 1e3 ? (n/1e3).toFixed(1)+'K'`
- Gridlines sutiles, tooltips con formato completo
