---
name: omt-router-ptv
version: "1.0.0"
description: "Rutas e isócronas en navegador desde OpenMapTiles."
tags: [routing, isochrones, vector-tiles, maplibre, webworkers, client-side]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [routing, isochrones, maplibre, client-side]
    related_skills: [graphhopper-routing, valhalla-routing, routing-isochrones, transit-data-pipelines]
---
# OMT Router — Enrutado e Isócronas en Navegador (OpenMapTiles)

## Resumen
Librería de routing client-side (`omt-router`, npm) que construye un grafo desde *vector tiles OpenMapTiles* en Web Workers y ejecuta algoritmos de ruta en el navegador, sin backend de routing. Calcula rutas óptimas e isócronas (polígonos de alcanzabilidad) para `car`, `pedestrian` y `bicycle` — usuarios de los mismos tiles usados en el basemap (provider-agnostic, reduce overhead de red/operación).

## Uso (features reales)
- **Motores**: `bidirectional-astar`, `adaptive-barrier`, `delta-stepping`, `ultra-dijkstra`.
- Selector automático de motor en runtime (entrenado con benchmarks) con fallbacks conservadores; forzar motor vía `engineId` o `auto`.
- **Modos de transporte**: `car`, `pedestrian`, `bicycle`.
- IsoPHAST para isócronas.
- Endpoint snapping con guard de calidad configurable (`maxAcceptableSnapDistanceM`).
- Worker pool `PowerPool` + caché de parseo `PowerCache`.
- Control ligero para MapLibre (integración rápida en mapas web).
- Live demo: https://abelvm.github.io/omt-router/example/

## Patrones / Arquitectura
- Unión de tiles sin costuras mediante clipping Liang–Barsky para nodos frontera *bit-idénticos* entre tiles.
- Compensación de rendimiento vs fiabilidad mediante selección flexible de motor.
- Sin terceros: construcción de grafo y ruta 100% en cliente.

## Pitfalls
- Requiere tiles vectoriales compatibles con el esquema OpenMapTiles.
- Los motores difieren en paralelismo/fit: `adaptive-barrier` y `delta-stepping` están listos para ejecución paralela en grafos densos; `bidirectional-astar` brilla en rutas largas/esparcidas. Ver `benchmark/README.md`.

## Verificación
- Cargar el ejemplo y trazar una ruta + una isócrona para cada modo; verificar unión de tiles en fronteras.

## Referencia
- NPM: `omt-router` (Licencia AGPL v3). Repo: https://github.com/AbelVM/omt-router
