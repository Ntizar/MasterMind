---
name: rain2flood-qgis-hydrology
version: "1.0.0"
description: "Usa para análisis hidrológico lluvia-inundación en QGIS."
tags: [qgis, hydrology, flood, rainfall, gis]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [qgis, hydrology, flood, rainfall, gis]
    related_skills: [aemet-llm-report-pipeline]
---
# Rain2Flood — De lluvia a inundación en QGIS

## Resumen
`Rain2Flood` es un plugin de QGIS Processing Toolbox (v2.1) que permite análisis hidrológico completo: desde datos de lluvia hasta mapeo de inundación en un solo workflow. Automatiza análisis de frecuencia de lluvia, cálculo de runoff, generación de hidrograma y exportación a formatos HEC-HMS. Para investigadores, estudiantes, ingenieros de recursos hídricos y modeladores de inundación.

## Uso (comandos reales del README)
Plugin de QGIS Processing Toolbox. Uso primario: instalar el plugin y ejecutar los algoritmos desde el toolbox en el mapa de QGIS (selección de punto desde el mapa, widgets de calendario, dropdowns de parámetros como CN, Manning's n, coeficientes de runoff).

## Patrones / Arquitectura
- Métodos de análisis: **SCS Unit Hydrograph**, **Rational Method** (tormentas cortas), **Time-Area Method**.
- Fuentes de datos de lluvia: API **Open-Meteo** (horario/diario global), soporte de **Excel** para datos custom, y procesamiento mejorado de **IMD** y **CHIRPS**.
- Análisis de flash flood horario para eventos de corta duración.
- Procesamiento de DEM mejorado (extracción de catchment y análisis de pendiente).
- Export HEC-HMS: genera archivos de entrada para modelización hidrológica HEC-HMS.
- Estructura de código modular con algoritmos de procesamiento separados; gestión automática de dependencias.

## Pitfalls
- CHIRPS: el bug de extracción se arregló para usuarios globales (verificar que la versión ≥2.1).
- Análisis de frecuencia para datasets pequeños mejorado; revisar errores y manejo de excepciones.
- Memory leaks en geopandas/rasterio corregidos; para datasets muy grandes vigilar memoria.
- Asegurar instalación automática de dependencias (gestión de paquetes del plugin).

## Verificación
- Ejecutar un análisis de lluvia→hidrograma en un catchment de prueba y verificar el mapeo de inundación.
- Confirmar generación de archivos de entrada HEC-HMS válidos.

## Referencia
README de https://github.com/rahulpandey696/Rain2Flood. Basado en IMDLIB (iamsaswata/imdlib); cita: IMDLIB, Environmental Modelling & Software 171 (2024): 105869. Video workflow: youtu.be/mJp9Be4vQcs.
