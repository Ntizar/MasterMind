---
name: node-gtfs
description: "Usa a importar y consultar GTFS en Node con node-gtfs."
version: "2.0.0"
tags: [gtfs, node, sqlite, node-gtfs, import, consulta]
related_skills: [node-gtfs, gtfs-manager, gtfs-box, transit-data-pipelines]
---

# node-GTFS — importar y consultar GTFS en SQLite (Node)

> ⚠️ Corrección 2026-09-05 (auditoría): la API es **`importGtfs`** + imports nombrados (`getStops`, `getRoutes`, `getStopsAsGeoJSON`, `getShapesAsGeoJSON`); **no** `gtfs.importFeed()`/`gtfs.routes()`/`gtfs.exportToGeoJSON()`. CLIs: `gtfs-import`, `gtfsrealtime-update`, `gtfs-export`.

**Repo:** `https://github.com/BlinkTagInc/node-gtfs` (TypeScript, ~500⭐).

## When to Use

- Cuando pidas **importar y consultar un feed GTFS** (SQLite local) desde Node.js.

## Uso (API real)

```bash
npm install node-gtfs
```

```js
import { importGtfs, getStops, getRoutes, getStopsAsGeoJSON } from 'gtfs';
await importGtfs({ agencies: [{ agency_key:'mi', url:'http://.../google_transit.zip' }] });
const stops = getStops();          // o getRoutes(), getStopsAsGeoJSON(), getShapesAsGeoJSON()
```

CLIs: `gtfs-import`, `gtfsrealtime-update`, `gtfs-export`.

## Pitfalls

- API: **`importGtfs`** + imports nombrados (`getStops`/`getRoutes`/`getStopsAsGeoJSON`/`getShapesAsGeoJSON`).
- **No** `gtfs.importFeed()` ni `gtfs.routes({lat,lng,maxDistance})`/`exportToGeoJSON`.
- CLI de import: `gtfs-import` (busca la config `agencies` con `url`/`path`).

## Verificación

- `importGtfs(config)` con un feed, luego `getStops()` y comprobar paradas.
