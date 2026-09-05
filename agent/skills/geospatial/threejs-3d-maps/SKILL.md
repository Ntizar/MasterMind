---
name: threejs-3d-maps
version: "1.0.0"
description: "Mapas 3D con three.js — geo-three, maptalks.three, map33.js. Visualización geoespacial 3D en navegador con tile providers (OSM, Bing, MapBox), terrain height maps, y extrude polygons GeoJSON."
tags: [threejs, maps, 3d, geospatial, webgl, visualization, gis]
---

# Mapas 3D con Three.js

## Resumen

Patrón para crear visualizaciones de mapas 3D en el navegador usando three.js como motor de render. Cubre tres librerías que integran mapas tile-based con three.js: **geo-three**, **maptalks.three**, y **map33.js**.

## Cuándo usar

- Visor 3D de datos geoespaciales (terrain, buildings, routes)
- Mapa 3D con tiles de OSM/Bing/MapBox como textura
- Visualización de datos GeoJSON con extrusión 3D (población, altura)
- Dashboard geoespacial interactivo con cámara orbital

## Librerías

### 1. geo-three (tentone/geo-three, ⭐938)

Librería completa para mapas 3D tile-based en three.js. Soporta múltiples providers y terrain height maps.

```javascript
import * as THREE from 'three';
import { MapView, OpenStreetMapsProvider } from 'geo-three';

// Crear provider de tiles
const provider = new OpenStreetMapsProvider();

// Crear mapa 3D y añadir a escena
const map = new MapView(MapView.PLANAR, provider);
scene.add(map);

// Convertir lat/lng a coordenadas three.js (EPSG:900913)
const coords = Geo.UnitsUtils.datumsToSpherical(40.4168, -3.7038);
controls.target.set(coords.x, 0, -coords.y);
```

**Providers soportados:** BingMaps, GoogleMaps, HereMaps, MapBox, MapTiler, OpenMapTiles, OpenStreetMaps, DebugProvider.

**LOD automático:** Ray casting para subdividir/simplificar tiles según distancia a cámara. Configurable con `subdivisionRays`, `thresholdUp`, `thresholdDown`.

**Terrain 3D:** Genera geometría 3D desde height data con GPU displacement maps o software-generated tiles.

**Instalación:** `npm install geo-three three`

### 2. maptalks.three (maptalks/maptalks.three, ⭐646)

Capa de three.js para maptalks.js — renderiza geometría 3D sobre mapas 2D.

```javascript
import * as THREE from 'three';
import * as maptalks from 'maptalks';
import { ThreeLayer } from 'maptalks.three';

const map = new maptalks.Map('map', {
  center: [0, 0],
  zoom: 3,
  baseLayer: new maptalks.TileLayer('base', { urlTemplate: '...' })
});

const threeLayer = new ThreeLayer('t');
threeLayer.prepareToDraw = function(gl, scene, camera) {
  const light = new THREE.DirectionalLight(0xffffff);
  light.position.set(0, -10, -10).normalize();
  scene.add(light);

  // Extrude polygons GeoJSON con altura variable
  const material = new THREE.MeshPhongMaterial();
  countries.features.forEach(g => {
    const height = g.properties.population;
    const extrudePolygon = threeLayer.toExtrudePolygon(g, { height }, material);
    threeLayer.addMesh(extrudePolygon);
  });
};
threeLayer.addTo(map);
```

**APIs clave:** `toExtrudePolygon(geojson, opts, material)`, `toBar(coords, opts, material)`, `toLine(coords, opts, material)`, `addMesh(mesh)`.

**Instalación:** `npm install maptalks maptalks.three three`

### 3. map33.js (blaze33/map33.js, ⭐500)

Librería ligera para mapas 3D con three.js. Enfoque minimalista.

```javascript
import { Map, Source, MapPicker } from 'map33';   // API real (paquete 'map33', no 'map33.js')
const map = new Map(scene, camera, source, position, { nTiles: 3, zoom: 12 });
```

## Patrón de uso — Visor geoespacial 3D

```javascript
// 1. Setup escena three.js estándar
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, w/h, 0.1, 10000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

// 2. Añadir mapa 3D con tiles OSM
const provider = new OpenStreetMapsProvider();
const map = new MapView(MapView.PLANAR, provider);
scene.add(map);

// 3. Convertir coordenadas reales a three.js
const coords = Geo.UnitsUtils.datumsToSpherical(lat, lng);
camera.position.set(coords.x, 500, -coords.y);

// 4. Añadir datos GeoJSON con extrusión 3D
geojson.features.forEach(feature => {
  const height = feature.properties.value * 10;
  const mesh = threeLayer.toExtrudePolygon(feature, { height }, material);
  threeLayer.addMesh(mesh);
});

// 5. Animación con LOD automático
function animate() {
  requestAnimationFrame(animate);
  map.update(); // LOD: subdividir/simplificar tiles
  renderer.render(scene, camera);
}
```

## Pitfalls

- **EPSG:900913 vs WGS84:** geo-three usa coordenadas XY en metros (EPSG:900913). Convertir SIEMPRE con `UnitsUtils.datumsToSpherical(lat, lng)`.
- **three.js >=128:** El paquete UMD por defecto es ES6. Si tu entorno no soporta ES6, usar versión ES5.
- **z position reversed:** Desde maptalks.three v0.6.0, la posición z está invertida respecto a v0.5.x.
- **API keys:** Bing, Google, MapBox, MapTiler requieren API key. OSM y Debug no.
- **Performance:** El LOD por ray-casting puede ser costoso. Ajustar `subdivisionRays` (default: 2) según necesidades.
- **Tile size:** Los tiles se cargan asíncronamente. Mostrar loading indicator mientras cargan.

## Comparativa de alternativas (actualizada 2026-09-03)

- **Navara** (`maplibre/navara`, ~260⭐, donado por Re:Earth a MapLibre; núcleo GIS Rust/WASM + render three.js, globo real, 3D Tiles, API en 4 niveles) — la evolución del motor de mapa 3D en three.js. Este skill (`threejs-3d-maps`) sigue vigente para casos planos ligeros (tiles 2D proyectados + extrusión GeoJSON sin globo ni WASM); para globo 3D serio con terrain/vectores/3D Tiles, usar **`navara-3d-globe-engine`**.
- **`photorealistic-3d-tiles-threejs`** — cuando el requisito es la malla fotorrealista de ciudad (Google 3D Tiles vía Cesium Ion) con efectos TSL, no un motor GIS completo.
- geo-three (938⭐) lleva meses sin actividad frente a Navara (push diario): para proyectos nuevos de globo, Navara es la vía; geo-three sigue válida para código existente.
- **[apinanaivot/IKEA...](https://github.com/apinanaivot)** — userscript que captura GLB de páginas de producto (p. ej. IKEA) para alimentar escenas three.js con modelos reales.
- **[shihanqu/voronoi-studio](https://github.com/shihanqu/voronoi-studio)** — generador Voronoi orgánico en un single-file que envuelve un STL *watertight* e imprime en 3D.

## Referencias

- geo-three: https://github.com/tentone/geo-three (docs: https://tentone.github.io/geo-three/docs/)
- maptalks.three: https://github.com/maptalks/maptalks.three (demos: https://maptalks.github.io/maptalks.three/demo/index.html)
- map33.js: https://github.com/blaze33/map33.js
- three.js: https://threejs.org/

---

**Hecho con ❤️ por David Antizar**
