---
name: simsat
description: "Usa a simular la órbita/accesos de un satélite (SimSat)."
version: "2.0.0"
tags: [simsat, satelite, orbita, simulador, docker, dashboard, api]
related_skills: [simsat, satellite-ai-vision, aws-dem-terrain-tiles]
---

# SimSat — simulador orbital de satélite (Docker + dashboard)

> ⚠️ Corrección 2026-09-05 (auditoría): licencia **AGPL-3.0** (no MIT). **No** es una librería pip (`from simsat import SimSat` / `.generate()` no existe). Es un **simulador Docker/orbital** con dashboard web (localhost:8000) y API REST (localhost:9005), que sirve imágenes (Sentinel/Mapbox) según la órbita/accesibilidad del satélite.

**Repo:** `https://github.com/DPhi-Space/SimSat` (Python, ~62⭐) · Licencia: **AGPL-3.0**.

## When to Use

- Cuando pidas **simular la órbita/accesos de un satélite** (qué zonas ve, cuándo pasa) y servir esas imágenes por API.

## Qué es

Simulador de **accesibilidad orbital** de un satélite: calcula la trayectoria/campos de vista y sirve imágenes (Sentinel/Mapbox) de las zonas cubiertas vía dashboard + API REST.

## Uso

```bash
docker compose up
# dashboard web: http://localhost:8000
# API REST: http://localhost:9005
```

## Pitfalls

- Licencia: **AGPL-3.0**, no MIT.
- Es un **simulador Docker/orbital**, no una librería Python; no hay clase `SimSat`/`.generate()`.
- Describe **accesibilidad/órbita**, no "generación de datos Sentinel/Landsat sintéticos para ML".

## Verificación

- `docker compose up` y comprobar que el dashboard muestra la órbita/accesos y la API sirve imágenes.
