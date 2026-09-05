---
name: geodeep
description: "Usa a detectar objetos satelitales con GeoDeep."
version: "2.0.0"
tags: [geodeep, deteccion, satelite, onnx, rasterio, python, geo]
related_skills: [geodeep, satellite-ai-vision, rs-change-detection-satellite]
---

# GeoDeep — detección de objetos desde satélite (ONNX)

> ⚠️ Corrección 2026-09-05 (auditoría): los IDs de modelos `pools`/`solar-panels` **no existen**; los reales incluyen `cars`, `trees`, `trees_yolov9`, `birds`, `planes`, `aerovision`, `buildings`, `roads`, `utilities`, `waldo30_nano`. Stack es **ONNX Runtime + rasterio** (no PyTorch); export de mask vía `save_mask_to_raster` / CLI `-t mask`.

**Repo:** `https://github.com/opengeos/geodeep` (Python, ~510⭐).

## When to Use

- Cuando pidas **detección/segmentación de objetos** sobre imágenes satelitales con modelos preentrenados.

## Uso (API real)

```python
import geodeep
result = geodeep.detect(..., model='cars', ...)   # IDs reales: cars, trees, buildings, roads, utilities...
# export de mask: geodeep.save_mask_to_raster(...) o CLI -t mask
```

## Pitfalls

- IDs de modelos reales: **cars / trees / birds / planes / buildings / roads / utilities / aerovision / waldo30_nano**, etc. — **no** `pools`/`solar-panels`.
- Stack: **ONNX Runtime + rasterio**, no PyTorch.
- Export de mask: `save_mask_to_raster` (o CLI `-t mask`), no `output_type='mask'`.

## Verificación

- Detectar sobre una imagen satelital con un ID válido y guardar el resultado.
