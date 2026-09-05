---
name: pfaedle-routing
description: "Usa a map-matchear GTFS sobre OSM con pfaedle."
version: "2.0.0"
tags: [pfaedle, gtfs, osm, map-matching, routing, cpp]
related_skills: [pfaedle-routing, valhalla-routing, gtfs-to-netex-conversion]
---

# pfaedle — map-matching de GTFS sobre OpenStreetMap

> ⚠️ Corrección 2026-09-05 (auditoría): el uso real es `pfaedle -x <osm.pbf> <feed_gtfs.zip>` (argumentos posicionales) con salida en **`./gtfs-out`**; **no** flags `--gtfs`/`--tracks`/`--output`/`--validate-shapes`. El concepto es **map-matching de GTFS sobre OSM** (no de tracks GPS). Importante `--recurse-submodules` en el clone.

**Repo:** `https://github.com/ad-freiburg/pfaedle` (C++, ~290⭐).

## When to Use

- Cuando pidas **proyectar/fijar un feed GTFS a la red real de OSM** (map-matching preciso de rutas y paradas sobre las calles).

## Uso (real)

```bash
git clone --recurse-submodules https://github.com/ad-freiburg/pfaedle.git
cd pfaedle && ./build.sh    # (build según README)
pfaedle -x osm.pbf feed.zip      # OSM + GTFS; salida en ./gtfs-out
```

## Pitfalls

- CLI: `pfaedle -x <osm> <gtfs>` (posicional), salida en **`./gtfs-out`**; no `--gtfs`/`--output`/`--validate-shapes`.
- Clone **`--recurse-submodules`** (si no, el build falla).
- Concepto: **GTFS sobre OSM**, no map-matching de tracks GPS de vehículos.

## Verificación

- Correr con un OSM pbf y un feed, comprobar en `gtfs-out` que las rutas siguen la red.
