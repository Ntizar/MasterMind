---
name: gtfs-box
description: "Visor web estática GTFS/GTFS-RT en 3D con Mini Tokyo 3D. Úsalo para ver operación en vivo de cualquier operador."
version: "2.0.0"
tags: [gtfs, gtfs-realtime, 3d-map, transport, webgl, mapbox, mini-tokyo-3d, visualization]
---

# GTFS box — Visor GTFS Realtime en 3D (verificado contra el código, 2026-09-04)

**Repo:** github.com/nagix/gtfs-box (21⭐, MIT, JavaScript, push ago-2026)
**Demo:** https://nagix.github.io/gtfs-box — mismo código servido como GitHub Pages

## Qué es REALMENTE

Visor **web estático puro**: `index.html` + `gtfs-box.js` (786 líneas) + `mini-tokyo-3d.min.js` empaquetados en el repo. **NO tiene build, NO es paquete npm, NO tiene CLI.** (El skill v1 que había aquí documentaba comandos `gtfs-box --gtfs feed.zip` y una clase `GTFSBox` que NO existen — inventados del maratón 2026-06.)

El motor 3D es **Mini Tokyo 3D** (`mt3d`), del mismo autor (nagix). GTFS box es esencialmente una app shell sobre mt3d: panel de configuración, selector de operadores pre-registrados y deep-links por URL.

## Uso real

```bash
git clone https://github.com/nagix/gtfs-box.git
cd gtfs-box && python -m http.server 8080   # cualquier server estático vale
# abrir http://localhost:8080
```

En pantalla: botón «v» arriba a la derecha → panel con GTFS zip URL, GTFS-RT VehiclePosition URL, color, zoom, lat, lng, bearing, pitch → Load. Hover sobre vehículo = info (nº de serie, destino); click = tracking con lista de paradas y horarios.

## API real (lo que hace gtfs-box.js)

```javascript
const map = new mt3d.Map({
  container: 'map',
  dataSources: [{
    id: 'gtfs',
    gtfsUrl: 'URL_DEL_ZIP',
    vehiclePositionUrl: 'URL_GTFS_RT_VEHICLEPOSITION', // opcional
    color: '#000099'
  }],
  dataUrl: undefined,          // datos de Tokyo de serie
  accessToken: 'pk.eyJ1Ij...', // token público Mapbox de mt3d (estilo base)
  lang: 'es',                  // 12 diccionarios en assets/dictionary-*.json
  zoom: 14, center: [-3.7038, 40.4168], // ¡OJO! center es [lng, lat]
  bearing: 0, pitch: 60,
  plugins: [mt3dPrecipitation(), mt3dPlateau({ enabled: false })]
});
map.getMapboxMap();  // acceso al MapGL subyacente (resize, etc.)
```

**Deep-links** (parseados de `location.search` y `location.hash`):

```
https://nagix.github.io/gtfs-box/?index=12
.../ ?gtfsurl=<zip>&gtfsvpurl=<vehiclepositions>&gtfscolor=<RRGGBB>&lang=es
   #zoom/lat/lng/bearing/pitch   ← posición de cámara en el hash
```

## Presets (SOURCES, 51 operadores)

Japón (ODPT: Toei, Yokohama, Kioto…), Lisboa (Carris: `gateway.carris.pt/gateway/gtfs/api/v2.8/GTFS[/realtime/vehiclepositions]`) y muchos EEUU (endpoints InfoPoint de availtec/rideralerts: `…/GTFS-Zip.ashx` + `…/GTFS-Realtime.ashx?Type=VehiclePosition`). **Ninguno español** — para EMT/Metro/Cercanías hay que pegar las URLs a mano en el panel.

## Patrones reutilizables

1. **App shell sobre motor 3D embebible**: UI mínima de 2 inputs (GTFS zip + RT URL) hace que cualquier feed del mundo sea visualizable sin backend — el mismo patrón sirve para GTFSSpain/DataHubEspana como «modo vitrina».
2. **Estado 100% en URL** (query params + hash): compartible, bookmarkeable, testeable headless.
3. **i18n por JSON plano** (`assets/dictionary-es.json` ya existe — incluye castellano).
4. **Plugin system mt3d**: precipitación y «plateau» (edificios 3D Japón) como plugins opcionales.

## Pitfalls

- **Mapbox GL por debajo**: mt3d usa token público + `assets/style.json` de Mapbox → contraviene la regla de David (solo herramientas gratuitas: Leaflet/OSM). Vale como **referencia de patrón**, no como base para producto propio. Para producto, el equivalente libre es MapLibre + GTFS propio (skills `gtfs-client-side-viz`, `threejs-3d-maps`).
- `center` es **[lng, lat]** (orden Mapbox), al revés que el panel de lat/lng — fuente clásica de «el mapa sale en el golfo de Guinea».
- CORS: el endpoint GTFS-RT debe permitir cross-origin (los de ODPT/Carris sí; muchos españoles no → necesitarías proxy).
- Solo consume **VehiclePosition**; no pinta TripUpdates/alertas.
- Datos por operador: uno a la vez; feeds muy grandes degradan el framerate.

## Verificación

Probar con el preset de Carris (Lisboa) en el demo público: si los autobuses se mueven, el pipeline GTFS+RT funciona. En local, servir con cualquier HTTP server estático (no `file://` — los fetch de .gz lo requieren).

## Referencias

- Repo: https://github.com/nagix/gtfs-box · Mini Tokyo 3D: https://minitokyo3d.com
- Hermano (mismo autor, 2D): `gtfs-client-side-viz` · Relacionados: `onebusaway-gtfs-realtime-visualizer`, `transit-3d-realtime`, `awesome-transit`
- Nota: existe `geospatial/gtfs-box-3d-viewer` (v1, menos preciso) — este es el skill canónico.
