---
name: gtfs2shp
description: GTFS2SHP — convertir feeds GTFS a shapefiles ESRI para GIS (Go, CLI).
version: "2.0.0"
tags: [gtfs, shapefile, esri, gis, go, transporte]
---

# GTFS2SHP — GTFS a Shapefile ESRI

## Qué es

`gtfs2shp` (github.com/patrickbr/gtfs2shp, Go, GPL-2.0) convierte un feed GTFS (zip) a shapefile ESRI:

- **Entidad principal = shapes GTFS** (`shapes.txt`): la geometría de las rutas; los trips/rutas que usan cada shape se agregan como atributos del shapefile (IDs y `route_short_name` agregados).
- **Estaciones como puntos** (`-s`): con todos sus atributos GTFS, en un shapefile aparte `<nombre>.station.shp`.
- **Trips explícitos** (`-t`): una geometría por trip con atributos trip/ruta — genera geometrías redundantes (más pesado).
- **Reproyección** (`-p <EPSG>`): salida por defecto en WGS84 (lat/lon); con `-p 3857` u otro código EPSG reproyecta.

## Instalación

```bash
go install github.com/patrickbr/gtfs2shp@latest   # requiere Go >= 1.7
```

## Uso

```bash
# Shapes -> shapefile (atributos con rutas agregadas)
gtfs2shp -i google_transit.zip -f output.shp

# Añadir estaciones (output.station.shp)
gtfs2shp -i google_transit.zip -f output.shp -s

# Geometría explícita por trip
gtfs2shp -i google_transit.zip -f output.shp -t

# Reproyectar a EPSG:3857
gtfs2shp -i google_transit.zip -f output.shp -p 3857
```

## Casos de uso para David

- Llevar feeds GTFS de España (Cercanías, metro, autobús) a QGIS/ArcGIS para análisis espacial de coberturas.
- Generar shapefiles de trazados para sistemas GIS legacy o entregables de planes de movilidad.
- Combinar con `gtfs-manager` / `node-GTFS`: validación y consulta previa, exporte GIS con gtfs2shp.

## Pitfalls

- La entidad por defecto son **shapes**, no routes: cada línea del shapefile es un `shape_id`, con las rutas agregadas en atributos — si se necesita por-route puro, usar `-t`.
- `-t` duplica geometrías (un trip por fila) — feeds grandes como Madrid generan cientos de MB.
- Shapefile limita nombres de campo a 10 caracteres y 2 GB por archivo.
- Salida WGS84 por defecto; en ESPG proyectados (ej. ETRS89 / UTM zona 30, EPSG:25830, habitual en España) pasar `-p 25830`.
- No maneja GTFS Realtime — solo feeds estáticos.
- Herramienta pequeña (27⭐) pero mantenida (push 2026-01); alternativa Python: `gtfs2geojson` + `gdal` si ya hay pipeline Python.

## Verificación

1. Abrir el `.shp` en QGIS y comprobar que el recuento de entidades coincide con `shapes.txt` del feed.
2. Con `-s`, verificar que `output.station.shp` existe y tiene tantas filas como `stops.txt`.
3. Reproyección: `ogrinfo -oo SHAPE_ENCODING=latin1 output.shp` y confirmar el `.prj`.

## Referencias

- Repo: https://github.com/patrickbr/gtfs2shp (27⭐, GPL-2.0)
- Registry: `patrickbr/gtfs2shp` (re-procesado y auditado contra README real el 2026-09-03)
