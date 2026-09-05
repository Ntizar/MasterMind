---
name: valhalla-routing
description: "Usa al enrutar e isócronas con Valhalla (org valhalla)."
version: "2.0.0"
tags: [routing, isocronas, valhalla, cpp, costing, contours, docker]
related_skills: [graphhopper-routing, osrm-routing, routing-isochrones, openstreetmap]
---

# Valhalla — motor de routing e isócronas (corrige org y API)

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): imagen Docker bajo org equivocada (`mapbox`), atribución a Mapbox obsoleta y payloads `mode`/`range`/`range_type` inválidos. El campo real es **`costing`** (routing) y **`contours`** (isócronas).

**Repo:** `https://github.com/valhalla/valhalla` (C++, MIT, ~6.2K⭐). Demo público de [FOSSGIS e.V.](https://valhalla.openstreetmap.de) — es el proyecto de routing de la org **valhalla**, no de Mapbox (la org `mapbox` ya no lo publica).

## When to Use

- Cuando pidas **rutas** o **isócronas** (áreas de tiempo/distancia) sobre OpenStreetMap en local.
- Como motor de routing open-source autohosteado (alternativa a OSRM/graphhopper).

## Uso (Docker)

```bash
# Imagen correcta: bajo la org 'valhalla'
docker pull ghcr.io/valhalla/valhalla:latest
# (o ghcr.io/valhalla/valhalla-scripted para el setup con script)
```

## API (payloads válidos)

**Routing** — campo **`costing`** (auto, bicycle, pedestrian...), NO `mode`:

```json
{ "locations": [{"lat":40.0,"lon":-3.0},{"lat":40.5,"lon":-3.5}], "costing": "auto" }
```

**Isócrona** — campo **`contours`** (con `time`/`distance`) y `polygons`/`denoise`, NO `range`/`range_type`:

```json
{
  "locations": [{"lat":40.0,"lon":-3.0}],
  "costing": "auto",
  "contours": [{ "time": 10 }]
}
```

*(`mode`, `range`, `range_type` parecen copiados de OSRM/openrouteservice y NO funcionan en Valhalla.)*

## Pitfalls

- Imagen Docker: **`ghcr.io/valhalla/valhalla`** (o `-scripted`), no `ghcr.io/mapbox/valhalla` (no existe).
- Atribución: hoy es org **valhalla** (demo FOSSGIS), ya no "Valhalla de Mapbox".
- El request usa `costing` (routing) y `contours` (isócronas).

## Verificación

- Levantar con la imagen correcta y hacer un routing `costing:"auto"` + una isócrona `contours:[{time:10}]`; comprobar que devuelven geometría coherente.
