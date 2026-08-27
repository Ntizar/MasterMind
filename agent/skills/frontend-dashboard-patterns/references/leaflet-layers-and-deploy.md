# Leaflet Layer Management + GitHub Pages Deploy

## Leaflet Layer Management — Capas activables con datos externos

Patrón para añadir capas de datos (GBFS, OSM, APIs) a un mapa Leaflet con toggle on/off.

### Arquitectura
```javascript
const layerState = {
    'layer-id': { active: false, layer: null, data: null, loading: false }
};

async function toggleLayer(layerId) {
    const state = layerState[layerId];
    state.active = !state.active;
    if (state.active) {
        if (!state.data && !state.loading) await loadLayerData(layerId);
        if (state.layer) state.layer.addTo(map);
    } else {
        if (state.layer) map.removeLayer(state.layer);
    }
}
```

### Overpass API (OpenStreetMap)
```javascript
//IMPORTANTE: usar bbox del CÍRCULO de búsqueda, no del viewport
const center = [lat, lon];
const radius = 2000;
const margin = radius * 0.009;
const bbox = `${center[0]-margin},${center[1]-margin},${center[0]+margin},${center[1]+margin}`;

// Para polígonos: `out geom body;` | Para puntos: `out center body;`
const query = `[out:json][timeout:25];(node["amenity"="parking"](${bbox}););out geom body;`;
const resp = await fetch('https://overpass-api.de/api/interpreter', {
    method: 'POST', body: 'data=' + encodeURIComponent(query)
});
```

**Pitfall:** No usar viewport del mapa como bbox —Overpass devuelve demasiados resultados. Usar siempre el área de interés.

### GBFS (Bicicletas públicas)
- Catálogo: `https://raw.githubusercontent.com/Ntizar/GBFSSpain/main/data/systems.json`
- Systems.json **no tiene lat/lon** — solo nombre de ciudad. Necesitar coordenadas embebidas para filtrar por proximidad.
- Discovery URL → feeds → station_information → estaciones con lat/lon
- Timeout 8s + Promise.allSettled para no bloquear por sistema caído
- Batch de 3-5 sistemas simultáneos

### Renderizado de polígonos OSM
```javascript
if (el.type === 'way' && el.geometry && el.geometry.length > 2) {
    const latlngs = el.geometry.map(p => [p.lat, p.lon]);
    L.polygon(latlngs, { color, weight: 2, fillColor: color, fillOpacity: 0.2 })
     .bindPopup(popup);
}
if (el.type === 'relation' && el.members) {
    el.members.filter(m => m.type === 'way' && m.geometry).forEach(m => { ... });
}
```

### Refresco de capas tras búsqueda
```javascript
// No refrescar en moveend. Refrescar tras buscar.
const _origBuscar = buscarParadas;
buscarParadas = function() {
    _origBuscar();
    setTimeout(() => {
        Object.keys(layerState).forEach(id => {
            if (layerState[id].active) loadLayerData(id);
        });
    }, 500);
};
```

---

## GitHub Pages — Deploy de HTML autocontenido

### Pages muestra README en vez de index.html
**Causa:** Pages source `/` pero index.html está en subdirectorio.

**Fix:** Copiar a raíz del repo:
```bash
cp visor/index.html ./index.html
git add index.html && git commit
```

**Regla:** index.html DEBE estar en la raíz para source `/`. API solo acepta `/` o `/docs`.

---

## Shapes completos vs clippeados en Leaflet

**Problema:** Polylines clippeadas al viewport/círculo se ven truncadas.

**Fix:** Dibujar la polyline completa (`allShapeCoords[shapeId]`) en vez de clippear:
```javascript
// ANTES (mal): const clipped = clipShapeToSearchArea(coords, nearStops, radius);
// DESPUÉS (bien): const line = L.polyline(allShapeCoords[shapeId], { color, weight: 5 });
```

Leaflet renderiza eficientemente polylines largas. No hay necesidad de clippear manualmente.
