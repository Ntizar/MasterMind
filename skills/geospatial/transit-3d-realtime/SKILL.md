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

- **Interpolación de posiciones:** NO actualizar posición directamente del fetch. Usar `lerp()` para smooth movement entre updates.
- **Rate limiting GTFS-realtime:** Fetch cada 3-10s, no más frecuente. Cachear última posición.
- **Coordenadas:** Convertir lat/lng a coordenadas 3D del scene. Usar proyección adecuada (WebMercator o local tangent plane).
- **LOD de vehículos:** Si hay >500 vehículos, usar instanced meshes o sprites para lejanos.
- **Underground mode:** Las líneas de metro deben poder ocultarse/visualizarse. Toggle de capa.
- **Eco mode:** Reducir framerate (30fps) para ahorrar batería en mobile.
- **i18n:** Cargar nombres de estaciones en múltiples idiomas desde dictionary JSON.

## Referencias

- Mini Tokyo 3D: https://github.com/nagix/mini-tokyo-3d (demo: https://minitokyo3d.com)
- GTFS-realtime spec: https://gtfs.org/realtime/
- NAP DGT España: skill `nap-dgt` para datos de movilidad

---

**Hecho con ❤️ por David Antizar**
