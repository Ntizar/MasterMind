---
name: transit-3d-realtime
version: "1.0.0"
description: "Visualización 3D de tránsito urbano en tiempo real — patrón inspirado en Mini Tokyo 3D. Mapa 3D de transporte público con trenes/metros/buses animados, tracking de vehículos, y datos GTFS-realtime."
tags: [transit, 3d, gtfs, realtime, threejs, visualization, transport]
---

# Tránsito 3D en Tiempo Real

## Resumen

Patrón para construir visualizaciones 3D de sistemas de transporte público en tiempo real. Inspirado en [Mini Tokyo 3D](https://minitokyo3d.com) (⭐4.1K) — mapa 3D de Tokyo que muestra trenes, aviones y estaciones en movimiento real.

## Cuándo usar

- Visor 3D de red de metro/autobús con vehículos animados en tiempo real
- Dashboard de movilidad urbana con tracking GPS de flota
- Visualización de datos GTFS-realtime en 3D
- Mapa interactivo de tránsito con route search y playback

## Elegir enfoque: CSS overlay vs Three.js completo

**Regla clave:** "hacer X en 3D sobre el mapa" ≠ "reemplazar el mapa con Three.js".

| Situación | Enfoque | Por qué |
|-----------|---------|---------|
| Mapa funcional existente + añadir vehículos 3D | **CSS overlay + Canvas icons** | Mantiene mapa, búsqueda, popups, controles |
| Visualización donde el mapa ES la app | **Three.js puro (R3F)** | Control total sobre cámara, postprocessing |
| Necesidad de sombras/reflexiones reales en el terreno | **Mapbox Custom Layer + Three.js** | Camera sync automática, terreno real |
| Prototipo rápido con efecto 3D | **CSS 3D transforms** | Sin dependencias nuevas, funciona ya |

### CSS overlay (recomendado para "3D on map")

Mantener Mapbox/Leaflet como base. Posicionar elementos CSS 3D con `map.project()`:

```javascript
// En el animation loop de Mapbox:
function updateOverlays() {
  buses.forEach(bus => {
    const point = map.project(bus.lngLat)
    bus.element.style.transform = `translate(${point.x}px, ${point.y}px)
      perspective(200px) rotateX(15deg)`
  })
}
map.on('move', updateOverlays)
```

Ventajas: mapa funcional, búsqueda, popups, controles intactos.
Ver `references/mapbox-css-3d-overlay.md` para implementación completa.

### Three.js completo (solo si el mapa NO es necesario)

Cuando se pide una escena 3D pura (sin mapa base), usar R3F:

```
src/three/
├── Scene3D.jsx          ← Canvas R3F + cámara + bloom
├── VehicleMesh.jsx      ← Mesh del vehículo
├── RouteTubes.jsx       ← TubeGeometry por ruta
└── Effects.jsx          ← Partículas, bloom, sky
```

Pitfalls R3F:
- NO usar `<primitive object={geo} attach="geometry" />` — usar ref + useEffect
- NUNCA crear geometrías en `useFrame()` — pre-crear con `useMemo`
- Archivos JSX deben tener extensión `.jsx`, NO `.js`

## Arquitectura

```
GTFS estático (rutas, paradas, horarios)
  + GTFS-realtime (posiciones de vehículos, delays)
  + Datos geoespaciales (GeoJSON de líneas)
  ↓
Three.js scene
  ├── Terreno 3D (tiles o plano con elevación)
  ├── Líneas de ruta (TubeGeometry extruded)
  ├── Estaciones (sprites o meshes)
  ├── Vehículos (meshes animados con interpolation)
  └── UI overlay (panel de búsqueda, info, controles)
  ↓
Loop de animación
  ├── Update posiciones de vehículos (fetch cada 3-10s)
  ├── Interpolate entre posiciones (smooth movement)
  ├── Camera tracking (follow vehicle)
  └── LOD: simplificar lejanos, detallar cercanos
```

## Patrón Mini Tokyo 3D

```javascript
// 1. Datos de rutas desde GTFS
const railways = await loadGTFS('railways.json'); // GeoJSON LineString
const stations = await loadGTFS('stations.json'); // puntos con nombre, línea
const vehicles = await fetchRealtime(); // GTFS-realtime vehicle positions

// 2. Renderizar líneas de ruta como tubos 3D
railways.forEach(rail => {
  const points = rail.coordinates.map(c => latLngTo3D(c[1], c[0]));
  const curve = new THREE.CatmullRomCurve3(points);
  const geometry = new THREE.TubeGeometry(curve, 64, 2, 8, false);
  const mesh = new THREE.Mesh(geometry, lineMaterial);
  scene.add(mesh);
});

// 3. Estaciones como meshes
stations.forEach(st => {
  const pos = latLngTo3D(st.lng, st.lat);
  const geom = new THREE.SphereGeometry(3, 16, 16);
  const mesh = new THREE.Mesh(geom, stationMaterial);
  mesh.position.copy(pos);
  mesh.userData = { name: st.name, lines: st.lines };
  scene.add(mesh);
});

// 4. Vehículos animados con interpolación
function updateVehicles(realtimeData) {
  realtimeData.forEach(v => {
    let mesh = vehicleMeshes.get(v.id);
    if (!mesh) {
      mesh = new THREE.Mesh(trainGeometry, trainMaterial);
      vehicleMeshes.set(v.id, mesh);
      scene.add(mesh);
    }
    // Interpolar posición suavemente
    const target = latLngTo3D(v.longitude, v.latitude);
    mesh.userData.target = target;
    mesh.userData.bearing = v.bearing;
  });
}

// 5. Loop: interpolar y renderizar
function animate() {
  requestAnimationFrame(animate);
  const lerpFactor = 0.05; // smooth interpolation
  vehicleMeshes.forEach(mesh => {
    if (mesh.userData.target) {
      mesh.position.lerp(mesh.userData.target, lerpFactor);
      // Rotar hacia bearing
      mesh.rotation.y = THREE.MathUtils.lerp(
        mesh.rotation.y, mesh.userData.bearing, lerpFactor
      );
    }
  });
  renderer.render(scene, camera);
}

// 6. Fetch realtime cada 5 segundos
setInterval(() => fetchRealtime().then(updateVehicles), 5000);
```

## Controles interactivos (patrón Mini Tokyo)

| Acción | Función |
|--------|---------|
| Drag | Pan del mapa |
| Wheel | Zoom in/out |
| Right-click drag | Tilt + rotate |
| Shift + drag | Box zoom |
| Click vehículo | Tracking mode |
| Click estación | Info panel |
| Hover | Tooltip info |
| Playback button | Modo replay temporal |
| Layer button | Toggle capas (trenes, buses, etc.) |

## GTFS-realtime integration

```javascript
// Fetch vehicle positions from GTFS-realtime feed
async function fetchRealtime() {
  const response = await fetch('https://api.transportes.gob.es/gtfs-rt/vehicles');
  const data = await response.json();
  return data.entity.map(e => ({
    id: e.vehicle.vehicle.id,
    latitude: e.vehicle.position.latitude,
    longitude: e.vehicle.position.longitude,
    bearing: e.vehicle.position.bearing,
    speed: e.vehicle.position.speed,
    trip_id: e.vehicle.trip.tripId,
    route_id: e.vehicle.trip.routeId
  }));
}
```

## Pitfalls

- **Vite + JSX extension:** Archivos con JSX deben tener extensión `.jsx`, NO `.js`. Vite/rollup falla con `Expression expected` en archivos `.js` que contienen JSX. Renombrar antes de build.
- **R3F `<primitive>` para geomerías custom:** No usar `<primitive object={geo} attach="geometry" />` para geomerías creadas con `useMemo`. Usar `useRef` + `useEffect` para attach imperativo.
- **Geometría en animation loop:** NUNCA crear/geometrías nuevas en `useFrame()` o `requestAnimationFrame()`. Pre-crear con `useMemo` fuera del loop. Recrear geometría cada frame = OOM y frame drops.
- **Interpolación de posiciones:** NO actualizar posición directamente del fetch. Usar `lerp()` para smooth movement entre updates.
- **Rate limiting GTFS-realtime:** Fetch cada 3-10s, no más frecuente. Cachear última posición.
- **Coordenadas:** Convertir lat/lng a coordenadas 3D del scene. Usar proyección adecuada (WebMercator o local tangent plane).
- **LOD de vehículos:** Si hay >500 vehículos, usar instanced meshes o sprites para lejanos.
- **Underground mode:** Las líneas de metro deben poder ocultarse/visualizarse. Toggle de capa.
- **Eco mode:** Reducir framerate (30fps) para ahorrar batería en mobile.
- **i18n:** Cargar nombres de estaciones en múltiples idiomas desde dictionary JSON.

## React Three Fiber (R3F) — implementación React

Para proyectos React+Vite, usar R3F en vez de Three.js vanilla. Dependencias: `three`, `@react-three/fiber`, `@react-three/drei` (OrbitControls, Text), `@react-three/postprocessing` (Bloom).

### Estructura de archivos recomendada

```
src/
├── App.jsx                 ← HUD React overlay (carga datos, reloj, búsqueda)
├── utils/coords.js         ← Proyección lat/lng → Vector3
└── three/
    ├── Scene3D.jsx          ← Canvas R3F + cámara + bloom + controles
    ├── VehicleMesh.jsx      ← Mesh del vehículo (bus/tren)
    ├── RouteTubes.jsx       ← TubeGeometry por cada ruta
    ├── StopMeshes.jsx       ← Meshes de estaciones/paradas
    └── Effects.jsx          ← Partículas, bloom, sky
```

### Proyección equirectangular (ciudad)

```javascript
const CENTER_LAT = 40.4168  // centro de la ciudad
const CENTER_LNG = -3.7038
const SCALE = 80000          // ~1 unidad = 1.25m a esta latitud

export function geoTo3D(coords) {
  return [
    (coords[0] - CENTER_LNG) * SCALE,   // X: este-oeste
    0,                                     // Y: altura
    -(coords[1] - CENTER_LAT) * SCALE,   // Z: norte-sur (invertido)
  ]
}
```

### Patrón R3F para geomerías custom

NO usar `<primitive object={geo} attach="geometry" />` — falla silenciosamente en algunos entornos. Usar ref + useEffect:

```jsx
const meshRef = useRef()
const customGeo = useMemo(() => createCustomGeometry(), [])

useEffect(() => {
  if (meshRef.current) meshRef.current.geometry = customGeo
}, [customGeo])

return <mesh ref={meshRef}><meshStandardMaterial ... /></mesh>
```

### Patrón R3F para stats sin double-render

```jsx
const lastStats = useRef({ routes: 0, buses: 0 })
if (onStats && (lastStats.current.routes !== routes.length || ...)) {
  lastStats.current = { routes: routes.length, buses: buses.length }
  onStats(lastStats.current)
}
```

### Referencia detallada

Ver `references/r3f-transit-patterns.md` para implementación completa: coordinate projection, PacMan mesh geometry, TubeGeometry routes, bloom setup, pitfalls de Vite+JSX.

---

**Hecho con ❤️ por David Antizar**
