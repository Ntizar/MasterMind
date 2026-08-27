---
name: simsat
description: Simulador de datos satelitales — generación de datos Sentinel/Landsat sintéticos para ML y testing.
version: "1.0.0"
tags: [satellite, simulation, ML, testing, Sentinel, Landsat, synthetic]
---

# SimSat — Simulador de Datos Satelitales

## Resumen

Simulador de datos satelitales — generación de datos Sentinel/Landsat sintéticos para ML y testing. 62⭐.

## Repo de referencia

- **GitHub:** `github.com/DPhi-Space/SimSat`
- **Lenguaje:** Python
- **Licencia:** MIT

## Instalación

```bash
git clone https://github.com/DPhi-Space/SimSat.git
cd SimSat && pip install -r requirements.txt
```

## Uso Básico

```python
from simsat import SimSat

# Generar datos satelitales sintéticos
simulator = SimSat(
    region="Madrid",
    resolution=10,  # metros
    bands=["B02", "B03", "B04", "B08"],  # Sentinel-2
    dates=["2024-01-01", "2024-06-01", "2024-12-01"]
)

# Generar imágenes
images = simulator.generate()

# Añadir ruido realista
images.noisy = simulator.add_noise(images, level=0.1)

# Exportar
simulator.export(images, "sentinel_synth.tif")
```

## Funcionalidades

1. **Bandas:** Soporte para Sentinel-2, Landsat-8, MODIS
2. **Resolución:** Configuración de resolución espacial
3. **Temporal:** Series temporales con variación estacional
4. **Ruido:** Simulación de nubes, atmósfera, sensor
5. **Export:** GeoTIFF, NetCDF, PNG

## Integración con Mastermind

- Complementa `rs-change-detection-satellite` — datos sintéticos para training
- Útil para `satellite-ai-vision` — datasets de prueba
- Ideal para `geodeep` — datos de entrenamiento sintéticos
- Reemplaza búsqueda de datos reales para prototipos

## Pitfalls

- **Realismo:** Los datos sintéticos no capturan toda la variabilidad real
- **Calibración:** Los parámetros deben calibrarse con datos reales
- **Formato:** GeoTIFF puede requerir GDAL para procesamiento

## Referencias

- [GitHub: DPhi-Space/SimSat](https://github.com/DPhi-Space/SimSat)
