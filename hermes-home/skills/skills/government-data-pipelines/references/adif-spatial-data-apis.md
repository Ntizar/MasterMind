# ADIF — APIs de datos espaciales ferroviarios

Fuentes de datos abiertos de ADIF (Administrador de Infraestructuras Ferroviarias) para integrar en visualizadores geoespaciales.

> **⚠️ ACTUALIZADO 2026-06-29:** Tramificación WMS reemplaza al INSPIRE WMS como capa principal de red. LTV corregido (geometría requerida).

---

## 1. WMS — Tramificación Común ADIF (⭐ RECOMENDADO)

**URL base:** `https://ideadif.adif.es/gservices/Tramificacion/wms`
**Versión:** WMS 1.1.1 / 1.3.0
**Formatos:** image/png, image/jpeg
**CRS soportados:** EPSG:4326, EPSG:3857, EPSG:25830
**Acceso:** Público, sin autenticación
**Atribución:** `© Administrador de infraestructuras ferroviarias`

### Capas disponibles

| Capa | Nombre | Descripción |
|------|--------|-------------|
| TramificacionComun | `Tramificacion:TramificacionComun` | ⭐ Red completa por segmentos (más detallado que INSPIRE) |
| TramosServicio | `Tramificacion:TramosServicio` | Tramos activos en servicio |
| TramosFueraServicio | `Tramificacion:TramosFueraServicio` | Tramos dados de baja |
| Dependencias | `Tramificacion:Dependencias` | Estaciones y dependencias |
| PKTeoricos | `Tramificacion:PKTeoricos` | Puntos kilométricos |

**⚠️ `TramificacionComun` es MUY superior al INSPIRE WMS** — muestra segmentos individuales de vía con colores por estado, no solo líneas genéricas. Verificado en CIAF-visor.

### Integración Leaflet

```javascript
const tramWms = L.tileLayer.wms('https://ideadif.adif.es/gservices/Tramificacion/wms', {
    layers: 'Tramificacion:TramificacionComun',
    format: 'image/png',
    transparent: true,
    version: '1.3.0',
    crs: L.CRS.EPSG3857,
    attribution: '© ADIF — Tramificación Común',
    maxZoom: 18
});
tramWms.addTo(map);
```

### GetCapabilities
```
https://ideadif.adif.es/gservices/Tramificacion/wms?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0
```

---

## 1b. WMS — Red de Transporte Ferroviario (INSPIRE) — ⚠️ MENOS DETALLADO

**URL base:** `https://ideadif.adif.es/services/wms`
**Mismo esquema que Tramificación pero con capas INSPIRE genéricas:**

| Capa | Nombre | Descripción |
|------|--------|-------------|
| RailwayLink | `TN.RailTransportNetwork.RailwayLink` | Tramos de vía (líneas) |
| RailwayNode | `TN.RailTransportNetwork.RailwayNode` | Nodos/intersecciones |
| RailwayStationNode | `TN.RailTransportNetwork.RailwayStationNode` | Estaciones |

**Usar solo si se necesita conformidad INSPIRE explícita.** Para visualización, Tramificación es mejor.

---

## 2. LTV — Límites Temporales de Velocidad (ArcGIS FeatureServer)

**URL base:** `https://services7.arcgis.com/XTupIrLX53AjaJqO/arcgis/rest/services/LTV_2/FeatureServer`
**Layer 0:** `LTV` (puntos, esriGeometryPoint)
**Formato de salida:** GeoJSON, JSON, PBF
**~1.162 registros** (verificado 2026-06-29)
**🔄 DATOS DINÁMICOS:** ADIF actualiza el FeatureServer en tiempo casi real (última edición verificada: 2026-06-29 08:17 UTC). Reflejan cambios por obras, señalización, calendarización.

### Campos principales

| Campo | Tipo | Descripción |
|-------|------|-------------|
| CODLINEA | String | Código de línea |
| DESCLINEA | String | Nombre de la línea |
| RESTRICCIONVELOCIDAD | SmallInteger | Velocidad limitada (km/h) |
| MOTIVO | String | Motivo de la restricción |
| PKINI / PKFIN | Double | Punto kilométrico inicio/fin |
| DESCPSINI / DESCPSFIN | String | Descripción del tramo |
| TIPOTREN | String | Tipo de tren afectado |
| VIAS | String | Vías afectadas |
| HORAVIGORLTV | String | Fecha/hora de vigencia |
| FECHAVIGORLTV | Date | Fecha de vigencia |
| OBSERVACIONES | String | Observaciones |
| NOSENIALIZADASISTEMA | String | ¿Sin senyalización de sistema? |
| NOSENIALIZADAVIA | String | ¿Sin senyalización de vía? |

### 🔴 PITFALL CRÍTICO: Coordenadas X/Y son NULL con outSR=4326

Cuando se pide `outSR=4326`, los atributos `X` e `Y` vienen **NULL**. Las coordenadas **SOLO** están en el objeto `geometry`:

```javascript
// ❌ INCORRECTO — f.properties.X e f.properties.Y son NULL
const lat = f.properties.Y;
const lng = f.properties.X;

// ✅ CORRECTO — usar f.geometry
const lat = f.geometry.coordinates[1];  // GeoJSON
const lng = f.geometry.coordinates[0];

// ✅ CORRECTO — si se usa JSON de ArcGIS (no GeoJSON)
const lat = f.geometry.y;
const lng = f.geometry.x;
```

**También es OBLIGATORIO** incluir `returnGeometry=true` en el query. Sin esto, el server no devuelve `geometry` y no hay coordenadas de ningún modo.

### Query correcto (verificado 2026-06-29)

```javascript
const url = 'https://services7.arcgis.com/XTupIrLX53AjaJqO/arcgis/rest/services/LTV_2/FeatureServer/0/query';
const params = new URLSearchParams({
    where: '1=1',
    outFields: 'CODLINEA,DESCLINEA,RESTRICCIONVELOCIDAD,MOTIVO,PKINI,PKFIN,DESCPSINI,DESCPSFIN,HORAVIGORLTV,TIPOTREN,VIAS',
    outSR: '4326',
    returnGeometry: true,          // ⚠️ OBLIGATORIO
    f: 'geojson',
    resultRecordCount: 2000
});
const resp = await fetch(`${url}?${params}`);
const data = await resp.json();

// ⚠️ Usar geometry, NO properties.X/Y
L.geoJSON(data, {
    pointToLayer: (feature, latlng) => L.marker(latlng, { icon: ltvIcon }),
    onEachFeature: (feature, layer) => {
        const f = feature.properties;
        layer.bindPopup(`<b>LTV</b><br>Línea: ${f.DESCLINEA}<br>Vel: ${f.RESTRICCIONVELOCIDAD} km/h`);
    }
}).addTo(map);
```

### Hub ArcGIS
- **URL:** `https://ltv-adif.hub.arcgis.com`
- **Experiencia:** `https://experience.arcgis.com/experience/1d8dbf2ab3214b3c8d88592044ee13a8`

---

## 3. Tramificación Común ADIF (WFS)

**URL base:** `https://ideadif.adif.es/gservices/Tramificacion/wfs`
**Versión:** WFS 2.0.0
**CRS por defecto:** EPSG:25830 (UTM zona 30N)
**Output formats:** application/json, GeoJSON, CSV, KML, SHAPE-ZIP
**Acceso:** Público, sin autenticación
**Límite por defecto:** 1.000.000 features

### FeatureTypes

| Nombre | Título | Descripción |
|--------|--------|-------------|
| `Tramificacion:TramosServicio` | Tramos en servicio | Segmentos activos de la red |
| `Tramificacion:TramosFueraServicio` | Tramos fuera de servicio | Segmentos dados de baja |
| `Tramificacion:Dependencias` | Dependencias | Estaciones y dependencias |
| `Tramificacion:PKTeoricos` | PK Teóricos | Puntos kilométricos |

### Query GeoJSON

```javascript
const url = 'https://ideadif.adif.es/gservices/Tramificacion/wfs';
const params = new URLSearchParams({
    service: 'WFS',
    version: '2.0.0',
    request: 'GetFeature',
    typeName: 'Tramificacion:TramosServicio',
    outputFormat: 'application/json',
    srsName: 'EPSG:4326',
    count: 5000
});
const resp = await fetch(`${url}?${params}`);
const data = await resp.json();
// data.features[].geometry.type = MultiLineString o LineString
L.geoJSON(data, {
    style: { color: '#1A4488', weight: 3, opacity: 0.5, dashArray: '6,4' }
}).addTo(map);
```

---

## 4. Red de Ferrocarriles IGN (ArcGIS FeatureServer)

**URL:** `https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/RedFerrocarrilesIGN/FeatureServer`
**Propietario:** IGN (Instituto Geográfico Nacional)

### Capas

| ID | Nombre | Tipo |
|----|--------|------|
| 1 | estaciones | Feature Layer |
| 2 | lineas | Feature Layer |
| 3 | areaffcc | Feature Layer |

**Nota:** Datos del IGN, no de ADIF. Útil como referencia geográfica complementaria.

---

## 5. Velocidades Bitcarrier (ArcGIS FeatureServer)

Mediciones reales de velocidad de trenes de control (Bitcarrier). Múltiples datasets mensuales:

- `https://services2.arcgis.com/NEwhEo9GGSHXcRXV/arcgis/rest/services/Velocidades_Bitcarrier_[Mes]_[Año]/FeatureServer`
- Meses disponibles: Enero-Diciembre, años 2019-2022
- **Útil para:** validar LTV con datos reales de velocidad

---

## Patrón de integración en Leaflet — CIAF-visor (verificado 2026-06-29)

Para un visor que combine datos CIAF + infraestructura ADIF:

```javascript
// 1. Capa base IGN
L.tileLayer('https://www.ign.es/wmts/ign-base?...', { attribution: '© IGN' }).addTo(map);

// 2. Red ferroviaria ADIF — ⭐ Tramificación WMS (NO el INSPIRE)
const tramWms = L.tileLayer.wms('https://ideadif.adif.es/gservices/Tramificacion/wms', {
    layers: 'Tramificacion:TramificacionComun',
    format: 'image/png', transparent: true, version: '1.3.0'
}).addTo(map);

// 3. LTV (FeatureServer → GeoJSON) — ⚠️ usar geometry, NO properties.X/Y
const ltvUrl = 'https://services7.arcgis.com/XTupIrLX53AjaJqO/arcgis/rest/services/LTV_2/FeatureServer/0/query';
fetch(`${ltvUrl}?where=1=1&outFields=*&outSR=4326&returnGeometry=true&f=geojson&resultRecordCount=2000`)
    .then(r => r.json())
    .then(data => {
        L.geoJSON(data, {
            pointToLayer: (f, ll) => L.marker(ll, { icon: ltvIcon }),
            onEachFeature: (f, layer) => {
                const p = f.properties;
                layer.bindPopup(`<b>LTV</b><br>${p.DESCLINEA}<br>${p.RESTRICCIONVELOCIDAD} km/h`);
            }
        }).addTo(map);
    });

// 4. Tramificación (WFS → GeoJSON, para interacción clic)
fetch('https://ideadif.adif.es/gservices/Tramificacion/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=Tramificacion:TramosServicio&outputFormat=application/json&srsName=EPSG:4326&count=5000')
    .then(r => r.json())
    .then(data => {
        L.geoJSON(data, { style: { color: '#1A4488', weight: 3, opacity: 0.5, dashArray: '6,4' } })
            .addTo(map);
    });

// 5. Control de capas
L.control.layers(null, {
    '🚂 Red ADIF (Tramificación)': tramWms,
    '⚡ Limitaciones de Velocidad': ltvLayer,
    '🛤️ Tramificación (WFS)': tramLayer
}).addTo(map);
```

### Patrón de interacción: Marcadores → Panel de detalle (no popup)

Para visores con datos ricos (CIAF, informes), usar **panel lateral** en vez de popups de Leaflet:

```javascript
// Click en marcador → abrir panel con ficha completa
marker.on('click', () => {
    showDetailPanel(report);  // Función que renderiza HTML en panel lateral
});

// Tooltip con info resumida (se ve al hover)
marker.bindTooltip(`
    <b>${report.id}</b><br>
    ${report.date} · ${report.line}
`, { direction: 'top', offset: [0, -10] });
```

**Ventaja:** el panel muestra todos los campos (conclusiones, recomendaciones, entidades) sin sobrecarga visual del mapa.

### 🔴 NO usar etiquetas de líneas hardcodeadas

Posiciones predefinidas de líneas ferroviarias (etiquetas tipo "Madrid – Barcelona") se ven **terrible** porque las posiciones aproximadas no se alinean con la geometría real del mapa. **No implementar esta capa.** Si se necesitan nombres de líneas, usar los atributos `DESCLINEA` del FeatureServer LTV o del WFS Tramificación como popup/tooltip al hacer clic en un tramo.

### Pitfalls

- **🔴 LTV geometry bug (CRÍTICO):** `outSR=4326` hace que `properties.X` y `properties.Y` sean NULL. **Usar SIEMPRE** `f.geometry.coordinates` (GeoJSON) o `f.geometry.x/y` (ArcGIS JSON). Incluir `returnGeometry=true` en el query.
- **🔄 LTV datos dinámicos:** ADIF actualiza el FeatureServer en tiempo casi real. No cachear indefinidamente — recargar al abrir el visor o con TTL de 1h.
- **WMS vs WFS:** WMS devuelve tiles renderizados (rápido, no consultable). WFS devuelve geometrías (consultable, más lento). Para capas de fondo, usar WMS. Para interacción (clic → popup), usar WFS/FeatureServer.
- **⭐ Tramificación > INSPIRE:** El WMS de Tramificación (`/gservices/Tramificacion/wms`) muestra segmentos individuales con colores por estado. El INSPIRE (`/services/wms`) muestra líneas genéricas. Usar Tramificación para visualización.
- **CRS:** El WMS acepta EPSG:3857 y EPSG:4326. El WFS usa EPSG:25830 por defecto — especificar `srsName=EPSG:4326` para Leaflet.
- **Límite WFS:** `CountDefault=1000000`. Para tramos en servicio, usar `count=5000` para no sobrecargar.
- **FeatureServer ArcGIS:** `resultRecordCount` limita resultados. Para LTV (~1162 puntos), 2000 es suficiente.
- **Atribución obligatoria:** ADIF requiere `© Administrador de infraestructuras ferroviarias`.
- **Etiquetas de líneas hardcodeadas:** Para 34 líneas principales, un GeoJSON estático con posiciones predefinidas es más rápido y fiable que queries WFS en tiempo real. El WFS solo se necesita para tramos interactivos.
- **Geolocalización limitada en informes CIAF:** Solo 2% de informes tienen lat/lng reales. 71% tienen PK, 92% nombre de estación. Opciones: (1) geocodificación por estación con Nominatim (ver `references/station-coords-geocoding.md`), (2) interpolación PK + geometría WFS de Tramificación, (3) **interpolación PK via LTV (VERIFICADO 2026-06-29):** los puntos LTV tienen PKINI/PKFIN + coordenadas. Para un PK dado, encontrar el punto cuyo rango lo contiene. 49/61 líneas CIAF tienen cobertura LTV → 71% geocodificación. Ver `references/excel-json-cross-reference.md` para código completo.
