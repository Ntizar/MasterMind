# ArcGIS FeatureServer + Leaflet — Patrones de Integración

## Paginación del FeatureServer

ArcGIS FeatureServer tiene `maxRecordCount` (normalmente 1000). Para datasets grandes, usa paginación:

```javascript
let offset = 0;
while (true) {
    const params = new URLSearchParams({
        where: '1=1', outSR: '4326', returnGeometry: 'true', f: 'geojson',
        outFields: 'campo1,campo2,...',
        resultOffset: offset, resultRecordCount: 1000
    });
    const resp = await fetch(`${FEATURE_SERVER_URL}/query?${params}`);
    const data = await resp.json();
    if (!data.features || data.features.length === 0) break;
    // procesar data.features...
    if (data.features.length < 1000) break;
    offset += 1000;
}
```

**⚠️ Pitfall:** `resultRecordCount` puede ser ignorado si supera `maxRecordCount` del servidor. Usa siempre 1000 como valor seguro. El servidor responde con 1000 aunque pidas 2000.

## Carga por BBox (recomendado para >10k features)

Para datasets enormes (50k+ polilíneas), **nunca cargues todo de golpe**. Usa carga espacial por bbox visible:

```javascript
async function loadByBBox(layerGroup, featureServerUrl, layerId, fields) {
    const b = map.getBounds();
    const bbox = `${b.getWest()},${b.getSouth()},${b.getEast()},${b.getNorth()}`;
    layerGroup.clearLayers();
    let offset = 0;
    while (true) {
        const params = new URLSearchParams({
            geometry: bbox, geometryType: 'esriGeometryEnvelope',
            spatialRel: 'esriSpatialRelIntersects', inSR: '4326', outSR: '4326',
            returnGeometry: 'true', f: 'geojson',
            outFields: fields, resultOffset: offset, resultRecordCount: 1000
        });
        const resp = await fetch(`${featureServerUrl}/${layerId}/query?${params}`);
        const data = await resp.json();
        if (!data.features || data.features.length === 0) break;
        // añadir features al layerGroup...
        if (data.features.length < 1000) break;
        offset += 1000;
    }
}
```

**Trigger:** Cargar en `zoomend` con guard anti-doble-carga:

```javascript
let loading = false;
map.on('zoomend', async function() {
    if (map.getZoom() >= 9 && !loading) {
        loading = true;
        await loadByBBox(myLayer, URL, 2, 'field1,field2');
        loading = false;
    }
});
```

## FeatureServer → GeoJSON con propiedades enriquecidas

El formato `f=geojson` devuelve GeoJSON estándar con `properties` en vez de `attributes`. Para colorear por un campo:

```javascript
function getColor(value) {
    const map = { 'Internacional': '#CB1823', 'Ibérico': '#2563eb', 'Estrecho': '#f97316' };
    return map[value] || '#6B96CF';
}

data.features.forEach(f => {
    const p = f.properties || {};
    const layer = L.geoJSON(f, {
        style: { color: getColor(p.ancho_viad), weight: 2, opacity: 0.7 }
    });
    layer.bindPopup(`<b>${p.nombre}</b><br>Ancho: ${p.ancho_viad}`);
    layerGroup.addLayer(layer);
});
```

## Fuentes de datos ferroviarios España

| Fuente | URL base | Tipo | Contenido |
|--------|----------|------|-----------|
| IGN Red Ferrocarriles | `https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/RedFerrocarrilesIGN/FeatureServer` | FeatureServer | 50k tramos líneas + 3k estaciones, CC-BY 4.0 |
| ADIF Tramificación | `https://ideadif.adif.es/gservices/Tramificacion/wms` | WMS raster | Visualización de vías (sin atributos) |
| ADIF LTV | `https://services7.arcgis.com/XTupIrLX53AjaJqO/arcgis/rest/services/LTV_2/FeatureServer` | FeatureServer | ~1.162 restricciones velocidad |
| Renfe Tiempo Real | `https://tiempo-real.renfe.com/renfe-visor/flota.json` | JSON | Posición GPS trenes Cercanías (solo 15 núcleos) |

### IGN FeatureServer — Capas

| Layer ID | Nombre | Tipo几何 | Features | Campos clave |
|----------|--------|----------|----------|-------------|
| 1 | estaciones | Point | 3.035 | nombre, cod_est, tipo_estfd, tipo_usod, n_andenes, estadofisd |
| 2 | lineas | Polyline | 50.165 | nombre, codigo, ancho_viad, electrifid, uso_ppald, titulard, red_tentd, n_via, estadofisd, situaciond, tipo_lined |
| 3 | areaffcc | Polygon | 8.167 | nombre, tip_areafd |

### Renfe Tiempo Real — Endpoints

| Endpoint | Contenido |
|----------|-----------|
| `/renfe-visor/lineas.geojson` | 73 líneas Cercanías (15 núcleos), con color y nombre |
| `/data/estaciones.geojson` | 879 estaciones Cercanías, con coords, accesibilidad, conexiones |
| `/renfe-visor/flota.json` | Posición actual trenes (~143 activos): codTren, codLinea, retrasoMin, lat/long, estación actual/siguiente |
| `/renfe-visor/flota_anterior.json` | Posiciones anteriores (para animación) |

**Limitación:** Solo Cercanías. NO incluye AVE, Alvia, Avlo, Media Distancia.

### Renfe Flota — Campos por tren

```json
{
  "tripId": "5178M25718R1",
  "codTren": "25718",
  "codLinea": "R1",
  "retrasoMin": "2",
  "codEstAct": "79404",
  "codEstSig": "79404",
  "horaLlegadaSigEst": "2026-06-30T08:39:31",
  "codEstDest": "72305",
  "codEstOrig": "79600",
  "latitud": 41.46291,
  "longitud": 2.2722147,
  "nucleo": "50",
  "accesible": false,
  "via": "2"
}
```
