---
name: deteccion-satelite-sentinel
description: "Patrón de procesamiento de imágenes satelitales Sentinel-2 — detección de tráfico vehicular (DRISH-X), descarga de tiles, y análisis GIS con Python. Imágenes gratuitas cada 5 días."
version: 2.0.0
author: Ntizar + Mastermind
---

# Procesamiento de Imágenes Satelitales Sentinel-2

Pipeline completo para trabajar con imágenes satelitales gratuitas (Sentinel-2, Landsat-8): descarga, procesamiento y detección de objetos (tráfico, vegetación, cambios).

## Arquitectura

```
Sentinel-2 (ESA)
   ↓ gratuitas, 10m/pixel, cada 5 días
┌──────────────────────────┐
│ Descarga (satellite-     │
│ downloader / AWS DEM)    │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Procesamiento            │
│ • DRISH-X (detección     │
│   tráfico vehicular)     │
│ • NDVI (vegetación)      │
│ • Bandas espectrales     │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Resultados               │
│ • Mapa de tráfico        │
│ • Cambios temporales     │
│ • Datos GIS              │
└──────────────────────────┘
```

## Descarga de imágenes Sentinel-2

```python
# Con satellite-downloader
from satellite_downloader import Sentinel2Downloader

downloader = Sentinel2Downloader(
    lat=40.4168,      # Madrid centro
    lon=-3.7038,
    start_date="2026-05-01",
    end_date="2026-05-28",
    cloud_cover=20,   # Máx 20% nubes
)

# Descarga imágenes (formato .jp2, ~500MB cada una)
downloader.download_all(output_dir="./sentinel-data")
```

## DRISH-X: Detección de Tráfico Vehicular

Técnica que detecta vehículos en movimiento por el "spectral smear" (arrastre espectral) que producen al moverse mientras el satélite captura.

```python
# Pseudocódigo del pipeline DRISH-X
import numpy as np
from osgeo import gdal

def detect_traffic(sentinel_tile_path):
    """
    Detecta vehículos en movimiento usando la diferencia
    entre bandas espectrales (el 'smear' del movimiento).
    """
    # Cargar bandas RGB + NIR
    ds = gdal.Open(sentinel_tile_path)
    red = ds.GetRasterBand(4).ReadAsArray()
    nir = ds.GetRasterBand(8).ReadAsArray()

    # El "smear" es visible como diferencia entre
    # bandas que se capturan en momentos distintos
    # (los satélites escanean línea por línea)

    # Calcular anomalías temporales entre bandas
    smear = np.abs(red.astype(float) - nir.astype(float))

    # Umbral para detectar vehículos
    threshold = np.mean(smear) + 3 * np.std(smear)
    vehicles = smear > threshold

    return vehicles  # Mapa booleano: True = vehículo detectado

# Resultado: coordenadas de concentración de tráfico
```

## NDVI — Índice de Vegetación

```python
def calculate_ndvi(red_band, nir_band):
    """Normalized Difference Vegetation Index"""
    red = red_band.astype(float)
    nir = nir_band.astype(float)
    ndvi = (nir - red) / (nir + red + 1e-10)
    return ndvi  # -1 (agua) a +1 (vegetación densa)

# NDVI > 0.3 = vegetación saludable
# NDVI < 0 = agua, suelo desnudo
```

## Descarga de Elevación (AWS Terrain Tiles)

```python
# Descargar tiles de elevación para modelos 3D del terreno
from aws_dem_downloader import download_tile

download_tile(
    lat=40.4168, lon=-3.7038,
    zoom=14,  # Nivel de detalle (0-14 global)
    output="./elevation/madrid.tif"
)
# → DEM (Digital Elevation Model) para modelos 3D
```

## Datos gratuitos disponibles

| Fuente | Resolución | Free? | Frecuencia | Uso |
|--------|-----------|-------|------------|-----|
| Sentinel-2 (ESA) | 10m/pixel | ✅ | 5 días | Tráfico, vegetación |
| Landsat-8 (NASA) | 30m/pixel | ✅ | 16 días | Cambios temporales |
| AWS Terrain Tiles | 30m | ✅ | — | Elevación/DEM |
| OpenStreetMap | vectores | ✅ | — | Mapas base |
| Copernicus DEM | 30m | ✅ | — | Elevación global |

## Buenas prácticas

1. **Cloud cover < 20%** — nubes arruinan la detección
2. **Zona urbana para DRISH-X** — funciona mejor en ciudades (más vehículos)
3. **Comparativa temporal** — mismo día de la semana para comparar tráfico
4. **Bandas específicas** — cada banda Sentinel tiene propósito (RGB, NIR, SWIR)
5. **GeoJSON de salida** — convertir detecciones a coordenadas reales para Leaflet

## Pitfalls

- ❌ Nubes → detección falsa de vehículos (sombras de nubes)
- ❌ Sin corrección atmosférica → NDVI incorrecto
- ❌ Imágenes muy grandes (JP2 10Kx10K) → RAM insuficiente (usar tiles)
- ❌ DRISH-X solo detecta vehículos EN MOVIMIENTO — coches aparcados son invisibles
- ❌ Sentinel-2 no tiene banda térmica → usar Landsat-8 para temperatura

## Referencia

- DRISH-X: https://github.com/sparkyniner/DRISH-X (228⭐)
- Sentinel downloader: https://github.com/Aouei/remote-sensing-satellite-downloader
- AWS DEM Downloader: https://github.com/orcunkok/AWS-Dem-Downloader
- Skills relacionadas: frontend-config-mapa-colores, backend/awesome-transit