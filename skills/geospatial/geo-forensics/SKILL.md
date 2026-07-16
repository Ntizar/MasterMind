---
name: geo-forensics
description: Análisis forense geoespacial — investigación con datos satelitales, GIS y análisis temporal.
version: "1.0.0"
tags: [GIS, forensics, satellite, temporal, analysis, geospatial]
---

# Refloow Geo-Forensics

## Resumen

Análisis forense geoespacial — investigación con datos satelitales, GIS y análisis temporal. 169⭐.

## Repo de referencia

- **GitHub:** `github.com/Refloow/Refloow-Geo-Forensics`
- **Lenguaje:** Python
- **Licencia:** MIT

## Instalación

```bash
git clone https://github.com/Refloow/Refloow-Geo-Forensics.git
cd Refloow-Geo-Forensics && pip install -r requirements.txt
```

## Uso Básico

```python
from refloow_geoforensics import GeoForensics

# Análisis temporal de imágenes satelitales
analysis = GeoForensics(
    start_date="2020-01-01",
    end_date="2025-01-01",
    bbox=[-3.75, 40.35, -3.65, 40.45],  # Madrid
    satellite="sentinel-2"
)

# Detección de cambios
changes = analysis.detect_changes()
for change in changes:
    print(f"{change.date}: {change.type} at {change.location}")

# Exportar informe
analysis.report("informe_forensico.pdf")
```

## Funcionalidades

1. **Change detection:** Detección de cambios temporales
2. **Satellite imagery:** Sentinel-2, Landsat, Planet
3. **GIS analysis:** Buffers, overlays, spatial joins
4. **Temporal analysis:** Series temporales de imágenes
5. **Evidence reporting:** Informes forenses automáticos

## Integración con Mastermind

- Complementa `rs-change-detection-satellite` — forense vs detección genérica
- Útil para `satellite-ai-vision` — análisis temporal de satélites
- Ideal para `osm-infrastructure-mapping` — cambios en infraestructura
- Reemplaza análisis manual de imágenes satelitales

## Pitfalls

- **Datos satelitales:** Acceso a datos de alta resolución puede ser limitado
- **Procesamiento:** Análisis temporal requiere mucho cómputo
- **Nubes:** Imágenes con cobertura de nubes son inútiles
- **Georeferenciación:** Exactitud geográfica variable

## Referencias

- [GitHub: Refloow/Refloow-Geo-Forensics](https://github.com/Refloow/Refloow-Geo-Forensics)
