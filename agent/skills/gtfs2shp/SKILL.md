---
name: gtfs2shp
description: GTFS2SHP — convertir feeds GTFS a shapefiles ESRI para GIS.
category: geospatial
---

# GTFS2SHP — GTFS a Shapefile ESRI

## Qué es

GTFS2SHP es una herramienta en Go para convertir feeds GTFS a shapefiles ESRI:
- **Shape conversion** — convertir rutas GTFS a shapefiles
- **Station geometries** — incluir paradas como puntos
- **Explicit trips** — geometría explícita por trip/ruta
- **Reprojection** — reproject to any EPSG

## Instalación

```bash
go install github.com/patrickbr/gtfs2shp@latest
```

## Uso básico

```bash
# Convertir rutas a shapefile
gtfs2shp -i feed.zip -f output.shp

# Incluir estaciones
gtfs2shp -i feed.zip -f output.shp -s

# Geometría explícita por trip
gtfs2shp -i feed.zip -f output.shp -t

# Reproject to EPSG:3857
gtfs2shp -i feed.zip -f output.shp -p 3857
```

## Casos de uso para David

- **GIS integration** — feeds GTFS en QGIS/ArcGIS
- **Shapefile generation** — para sistemas legacy
- **Analysis** — análisis espacial de rutas de transporte

## Pitfalls

- Output es WGS84 por defecto (EPSG:4326)
- Shapefiles tienen limitación de 2GB
- Requiere feed GTFS válido
- No maneja GTFS-RT (realtime)

## Referencias

- Repo: `github.com/patrickbr/gtfs2shp` (27⭐)
