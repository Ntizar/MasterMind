---
name: satellite-traffic-detection
description: "DRISH-X — detección de tráfico de vehículos desde imágenes satelitales Sentinel-2. Aprovecha el parpadeo RGB del sensor (1.01s entre canales) + YOLO para inteligencia de carga en carreteras"
version: 1.0.0
author: Ntizar
tags: [vision, satellite, traffic, DRISH-X]

---

# DRISH-X — Satellite-Powered Freight Intelligence

## Descripción

Inteligencia automatizada de tráfico de vehículos desde imágenes satelitales Sentinel-2. Responde: "¿cuánto tráfico hay en esta carretera y cómo ha cambiado con el tiempo?"

## Referencia Principal

- **Repo**: sparkyniner/DRISH-X-Satellite-powered-freight-intelligence- (233★)
- **URL**: https://github.com/sparkyniner/DRISH-X-Satellite-powered-freight-intelligence-
- **License**: MIT

## Tecnologías

- Python 3.10+
- FastAPI (API)
- Sentinel-2 / Copernicus (imágenes satelitales)
- YOLO (detección de vehículos)

## Principio Científico

El sensor Sentinel-2 registra los canales rojo, verde y azul con un desfase de **1.01 segundos**. Cualquier objeto estático se ve normal, pero un vehículo moviéndose a velocidad autopista aparece desplazado entre los canales. Este "parpadeo RGB" es la señal explotada para detección.

## Pasos de Implementación

1. **Descargar imágenes Sentinel-2** desde Copernicus Data Space
2. **Preprocesar**: extraer canales RGB con desfase temporal
3. **Detectar vehículos**: YOLO sobre imágenes procesadas
4. **Contar y rastrear**: agregación por segmento de carretera
5. **API FastAPI**: exponer resultados para consumo

## Casos de Uso

- **Freight intelligence**: conteo y seguimiento de camiones en autopistas
- **Traffic analysis**: patrones de tráfico temporal
- **Infrastructure planning**: datos para planificación de infraestructura
- **Environmental monitoring**: impacto del tráfico en zonas sensibles

## Targets de Interés

- Autopistas principales
- Corredores de carga
- Fronteras y puntos de control
- Zonas industriales

## Pitfalls

- Requiere acceso a Copernicus Data Space (gratuito pero con registro)
- La resolución de Sentinel-2 (10m/píxel) limita la detección en carreteras secundarias
- Las condiciones climáticas (nubes) afectan la disponibilidad de imágenes
- El desfase temporal de 1.01s requiere corrección de geometría

## Herramientas Complementarias

- **Aouei/remote-sensing-satellite-downloader**: descarga de Sentinel-2/Landsat
- **orcunkok/AWS-Dem-Downloader**: descargas de DEM de elevación
- **c2g-dev/city2graph**: análisis de grafos sobre datos geoespaciales
