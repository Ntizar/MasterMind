---
name: gtfs-box-3d-viewer
description: GTFS/GTFS Realtime viewer en mapa 3D — visualización en tiempo real de transporte público usando Mini Tokyo 3D como librería base.
category: geospatial
---

# GTFS Box — Viewer GTFS Realtime en 3D

> ⚠️ **SUPERADO (2026-09-04):** la referencia canónica verificada contra el código real es el skill **`mobility/gtfs-box` v2.0.0**. Esta página data de una v1 con API imprecisa (el constructor real es `new mt3d.Map({container, dataSources:[{id,gtfsUrl,vehiclePositionUrl,color}], lang, plugins})`, no `new MiniTokyo3D(options)`). Usar `gtfs-box` para detalles; aquí solo se conserva el mapeo a proyectos de David.

## Qué es

**gtfs-box** (nagix/gtfs-box, 18⭐) es un visor web de GTFS y GTFS Realtime que muestra la operación en tiempo real de sistemas de transporte público en un mapa 3D. Usa **Mini Tokyo 3D** como librería base.

## Características

- Visualización 3D en tiempo real de vehículos GTFS Realtime
- Configurable: URL GTFS zip, URL GTFS-Realtime VehiclePosition, color, zoom, lat/lng, bearing, pitch
- Tracking de vehículos: hover muestra info, click inicia seguimiento
- Lista de paradas y horarios al seleccionar un vehículo
- Presets de operadores pre-registrados
- Demo: https://nagix.github.io/gtfs-box

## Mini Tokyo 3D — Librería base

```javascript
const options = {
  data: {
    gtfs: 'URL_DEL_GTFS_ZIP',
    realtime: 'URL_DEL_GTFS_REALTIME'
  },
  config: {
    zoom: 12,
    center: [40.4168, -3.7038], // Madrid [lat, lng]
    bearing: 0,
    pitch: 60
  }
};
const map = new MiniTokyo3D(options);
map.appendTo(document.getElementById('map'));
```

## Integración con proyectos de David

- **GTFSSpain**: Añadir vista 3D por operador (además de la vista 2D actual)
- **DataHubEspana**: Tab de transporte con visualización 3D realtime
- **Visor Hermes**: Integrar tránsito 3D en visor cartográfico

## Patrón — GTFS Realtime en 3D

```
GTFS Static (zip) → routes, stops, trips, stop_times
GTFS Realtime (protobuf) → VehiclePosition, TripUpdate, Alert
Mini Tokyo 3D → renderiza red 3D + actualiza posiciones de vehículos
```

## Pitfalls

- Mini Tokyo 3D es específico de Tokyo — adaptar para otros mapas requiere configuración
- GTFS Realtime requiere endpoint protobuf — no todos los operadores españoles lo ofrecen
- CORS — el endpoint de GTFS-Realtime debe permitir CORS
- Performance con muchos vehículos — limitar el área visible

## Referencias

- Repo: https://github.com/nagix/gtfs-box
- Demo: https://nagix.github.io/gtfs-box
- Mini Tokyo 3D: https://minitokyo3d.com
- GTFS Realtime: https://gtfs.org/documentation/realtime/
