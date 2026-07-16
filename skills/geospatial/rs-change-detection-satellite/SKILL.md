---
name: rs-change-detection-satellite
description: Detección de cambios en imágenes satelitales con Sentinel/Landsat — remote sensing, Earth Engine, Planetary Computer, NDVI/NDBI, deforestación, inundaciones.
category: geospatial
---

# RS Change Detection — Detección de Cambios Satelitales

## Qué es

**rs-change-detection** (firmanhadi21/rs-change-detection, 3⭐) es una librería Python para detectar cambios en imágenes satelitales usando Sentinel-2 y Landsat. Integra Google Earth Engine y Microsoft Planetary Computer.

## Capacidades

- Detección de deforestación (comparar NDVI entre fechas)
- Detección de inundaciones (cambios en cuerpos de agua)
- Expansión urbana (cambios en NDBI)
- Análisis multitemporal
- Output visual: mapas PNG con matplotlib + contextily

## Índices espectrales

```python
# NDVI — Vegetation
ndvi = (nir - red) / (nir + red)

# NDBI — Built-up
ndbi = (swir1 - nir) / (swir1 + nir)

# MNDWI — Water
mndwi = (green - swir1) / (green + swir1)

# Change detection
change = ndvi_date2 - ndvi_date1
# Negativo = pérdida vegetación, Positivo = ganancia
```

## Uso con Planetary Computer (STAC)

```python
from pystac_client import Client
import planetary_computer as pc
import rioxarray

catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
search = catalog.search(
    collections=["sentinel-2-l2a"],
    intersects={"type": "Point", "coordinates": [-3.7038, 40.4168]},
    datetime="2026-01-01/2026-06-30",
    query={"eo:cloud_cover": {"lt": 20}}
)
items = [pc.sign(item) for item in search.get_items()]
nir = rioxarray.open_rasterio(items[0].assets["B08"].href)
```

## Casos de uso para David

- **DataHubEspana**: Tab de medio ambiente con detección de deforestación
- **Parques Nacionales**: Monitorear cambios en vegetación
- **CallesDinamicas**: Detectar expansión urbana para nuevas ciudades
- **Visor Hermes**: Capa de cambio de uso de suelo

## Pitfalls

- Earth Engine requiere autenticación (`ee.Authenticate()`)
- Planetary Computer es más accesible — no requiere auth para STAC
- Resolución: Sentinel-2 10m, Landsat 30m
- Filtrar por cloud cover < 20%
- Gap temporal: Sentinel-2 5 días, Landsat 16 días
- rioxarray es lazy pero `.compute()` carga todo en RAM

## Dependencias

```
earthengine-api
planetary-computer
pystac-client
odc-stac
rasterio
rioxarray
numpy
matplotlib
contextily
```

## Referencias

- Repo: https://github.com/firmanhadi21/rs-change-detection
- Earth Engine: https://earthengine.google.com
- Planetary Computer: https://planetarycomputer.microsoft.com
- STAC: https://stacspec.org
