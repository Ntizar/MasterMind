---
name: satellite-gis-patterns
description: "Patrones de procesamiento de datos satelitales y GIS — DRISH-X (tráfico por satélite), Sentinel-2, y herramientas client-side routing."
version: 1.0.0
author: Mastermind (auto-generated from exploration)
tags: [vision, satellite, GIS, Sentinel-2]

---

# Satellite & GIS Patterns

Patrones para trabajar con datos satelitales, GIS y routing client-side, inspirados en repos explorados.

## 1. DRISH-X — Tráfico desde Satélite

**Fuente:** [sparkyniner/DRISH-X](https://github.com/sparkyniner/DRISH-X-Satellite-powered-freight-intelligence-) (⭐228)

### Técnica clave: Spectral Smear Detection
Los satélites Sentinel-2 capturan R, G, B con 1.01s de diferencia. Los vehículos en movimiento dejan un "spectral smear" distintivo (desplazamiento azul-verde-rojo).

### Pipeline
```
Sentinel-2 imagery → Detect spectral smears → Count vehicles → Estimate speed/direction → Time-series analysis
```

### Datos
- **Fuente:** Copernicus (gratis)
- **Resolución:** 10m (bandas RGB)
- **Revisita:** 5 días (constelación Sentinel-2)
- **Ejecución:** Local en browser, sin infraestructura terrestre

### Aplicaciones
- Monitoreo de tráfico en cualquier carretera del mundo
- Análisis de volumen por horas/días/semanas
- Detección de patrones estacionales

## 2. Client-Side Routing

**Fuente:** [AbelVM/omt-router](https://github.com/AbelVM/omt-router) (⭐11)

### Concepto
Routing 100% client-side usando OpenMapTiles vector tiles. Sin backend de routing.

### Algoritmos disponibles
- **bidirectional-astar** — Rápido, bueno para distancias largas
- **adaptive-barrier** — Balance velocidad/calidad
- **delta-stepping** — Óptimo para redes grandes
- **ultra-dijkstra** — Más lento pero más preciso

### Modos de transporte
- 🚗 Car
- 🚶 Pedestrian
- 🚲 Bicycle

### Integración
- MapLibre GL JS
- Web Workers para no bloquear UI
- Tile caching para rendimiento

### Aplicación a Mastermind
- Dashboard Bicimad sin necesidad de backend de routing
- Isolineas (reachability polygons) para estaciones de bike
- Integración con OpenMapTiles existentes

## 3. Descarga de Datos Satelitales

**Fuentes:**
- [Aouei/remote-sensing-satellite-downloader](https://github.com/Aouei/remote-sensing-satellite-downloader) — Sentinel-2, Landsat-8 via Copernicus OData
- [orcunkok/AWS-Dem-Downloader](https://github.com/orcunkok/AWS-Dem-Downloader) — AWS Terrain Tiles (elevación)

### Comandos útiles
```bash
# Descargar tiles de elevación AWS
aws-dem-downloader --bbox -3.7,40.4,-3.6,40.5 --zoom 12

# Descargar Sentinel-2
python -m satellite_downloader --sentinel --bbox --date
```

## 4. City2Graph — GNN para Ciudades

**Fuente:** [c2g-dev/city2graph](https://github.com/c2g-dev/city2graph) (⭐1.2k)

Transforma relaciones geoespaciales en grafos para Graph Neural Networks.

### Pipeline
```
City spatial data → Graph representation → GNN training → Predictions
```

### Aplicaciones
- Predicción de tráfico
- Planificación urbana
- Análisis de movilidad

## Integración con Mastermind

Para proyectos de movilidad/bicimad:
1. Usar omt-router para routing client-side en dashboards
2. DRISH-X como referencia para datos satelitales de tráfico
3. City2Graph para análisis avanzado con ML
4. Sentinel-2 downloader para obtener datos brutos

## 5. Isocronas — Patrón Híbrido ORS + NAP

**Proyecto:** [Ntizar/TimeIneco](https://github.com/Ntizar/TimeIneco)

Arquitectura zero-backend para isocronas de movilidad:
- **Coche/Bici/Peatón:** OpenRouteService API (gratis, desnivel incluido)
- **Transporte público:** NAP/GTFS España (catálogo de datos, parseo local)
- **PDF:** jsPDF + autoTable (informe profesional)
- **Todo en un HTML:** Leaflet Canvas + vanilla JS

**Ver referencias:** `references/nap-gtfs-integration.md`, `references/isochrone-architecture.md`

## Referencias
- https://github.com/sparkyniner/DRISH-X-Satellite-powered-freight-intelligence-
- https://github.com/AbelVM/omt-router
- https://github.com/c2g-dev/city2graph
- https://github.com/Aouei/remote-sensing-satellite-downloader
- **references/nap-gtfs-integration.md** — API NAP completa (endpoints, esquemas, flujos)
- **references/isochrone-architecture.md** — Patrón arquitectura isocronas ORS+NAP
