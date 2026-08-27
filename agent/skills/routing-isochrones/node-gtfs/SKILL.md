---
name: node-gtfs
version: "1.0.0"
description: "node-GTFS — importar y consultar datos GTFS en SQLite con consultas espaciales y soporte GTFS-Realtime"
---

# node-GTFS — GTFS en SQLite

## Descripción

Librería de Node.js que carga datos de tránsito en formato GTFS (General Transit Feed Specification) en una base de datos SQLite. Proporciona métodos para consultar agencias, rutas, paradas, horarios, tarifas, calendarios y más. Incluye consultas espaciales para encontrar paradas/rutas cercanas y conversión a GeoJSON.

## Por qué importa para David

- **SQLite + GTFS**: Pattern ligero de almacenamiento de datos de transporte público
- **Consultas espaciales**: Find nearby stops, routes, agencies — directamente en SQL
- **GTFS-Realtime**: Soporta importar actualizaciones en tiempo real al mismo SQLite
- **GeoJSON export**: Convertir stops y shapes a GeoJSON para visualización en Leaflet/MapLibre
- **Lightweight**: Sin necesidad de PostgreSQL/PostGIS para datos medianos

## Arquitectura

```
GTFS Feed (zip) → node-GTFS → SQLite Database
                                              ↓
                                    Query Methods:
                                    - agencies()
                                    - routes()
                                    - stops()
                                    - trips()
                                    - stopTimes()
                                    - fares()
                                    - spatial queries (nearby)
                                              ↓
                                    GeoJSON export / Realtime updates
```

Stack: TypeScript, SQLite, GTFS, GeoJSON

## Instalación

```bash
npm install gtfs
```

## Uso básico

```javascript
const gtfs = require('gtfs');

// Import GTFS feed
await gtfs.importFeed({
  directory: './data/gtfs',
  mode: 'sqlite'
});

// Query routes
const routes = await gtfs.routes();

// Query nearby stops
const nearbyStops = await gtfs.stops({
  latitude: 40.4168,
  longitude: -3.7038,
  maxDistance: 500  // meters
});

// Export to GeoJSON
await gtfs.exportToGeoJSON({
  entityType: 'stops',
  filename: 'stops.geojson'
});

// GTFS-Realtime updates
await gtfs.importRealtime({
  agencyId: 'MTM',
  frequency: '15min'  // poll every 15 min
});
```

## Integración con proyectos de David

- **Time**: Backend de datos GTFS para isocronas y rutas de transporte
- **Esios**: Cargar datos de transporte público de múltiples ciudades
- **España Atlas**: Capa de transporte público con datos reales GTFS
- **NAP DGT**: Patrón de consulta de movilidad con SQLite

## Pitfalls

- SQLite tiene límite de ~140GB por base de datos → OK para una ciudad, no para España completo
- GTFS-Realtime requiere polling regular para mantener datos frescos
- No todos los feeds GTFS son de calidad → limpiar datos antes de importar
- Spatial queries requieren extensiones de SQLite (RTree) para performance en grandes datasets
- Para España completo con múltiples comunidades, mejor usar PostgreSQL/PostGIS

## Referencias

- GitHub: https://github.com/BlinkTagInc/node-gtfs
- npm: https://www.npmjs.com/package/gtfs
- GTFS spec: https://gtfs.org/
- GTFS-Realtime: https://gtfs.org/documentation/realtime/
