---
name: geodeep
version: "1.0.0"
description: "GeoDeep — librería Python para detección de objetos y segmentación semántica en rasters geoespaciales (GeoTIFFs) con modelos ONNX"
---

# GeoDeep — AI en Rasters Geoespaciales

## Descripción

Librería Python rápida y ligera para detección de objetos y segmentación semántica en rásters geoespaciales (GeoTIFFs), con modelos pre-construidos incluidos. Detecta coches, edificios y más desde ortofotos.

## Por qué importa para David

- **AI + Geospatial**: Integración directa de IA con datos geográficos
- **ONNX models**: Modelos ligeros y portables para deployment
- **GeoTIFF input/output**: Formato estándar en GIS
- **CLI + Python API**: Útil tanto para scripts como para integración en pipelines

## Arquitectura

```
GeoTIFF / Orthophoto
    ↓
GeoDeep (ONNX models)
    ├── Detección de objetos → GeoJSON (bounding boxes)
    └── Segmentación semántica → GeoJSON (polygons) / raster mask
```

Stack: Python, ONNX Runtime, rasterio, PyTorch, GeoTIFF

## Instalación

```bash
pip install -U geodeep
```

## Uso básico

```python
# Detección de objetos (coches)
from geodeep import detect
bboxes, scores, classes = detect('orthophoto.tif', 'cars')
geojson = detect('orthophoto.tif', 'cars', output_type="geojson")

# Segmentación semántica (edificios)
from geodeep import segment
polygons = segment('orthophoto.tif', 'buildings')

# Exportar mask georreferenciada
segment('orthophoto.tif', 'buildings', output_type='mask')

# Listar modelos disponibles
# geodeep --list-models
```

Modelos disponibles: cars, buildings, trees, pools, solar-panels, y más

## Integración con proyectos de David

- **España Atlas**: Detección automática de edificios/coches desde ortofotos
- **Satellite AI Vision**: Complemento a skills existentes de visión satelital
- **Urban planning**: Análisis de cobertura de edificios, vehículos, infraestructura
- **Change detection**: Comparar ortofotos temporales con detección de cambios

## Pitfalls

- Precisión del modelo depende de resolución de la ortofoto
- Modelos pre-construidos pueden no cubrir todos los escenarios de España
- ONNX models requieren GPU para performance en imágenes grandes
- GeoTIFFs grandes pueden consumir mucha RAM (considerar tile processing)
- Solo soporta Python 3.6+

## Referencias

- GitHub: https://github.com/uav4geo/GeoDeep
- pypi: https://pypi.org/project/geodeep/
- Homepage: https://uav4geo.github.io/GeoDeep/
