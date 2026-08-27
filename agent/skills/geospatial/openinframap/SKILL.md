---
name: openinframap
version: "1.0.0"
description: "Open Infrastructure Map — visualización de infraestructura global desde datos de OpenStreetMap con MapLibre GL JS, Tegola y PostGIS"
---

# Open Infrastructure Map

## Descripción

Mapa que muestra la infraestructura global del mundo a partir de datos de OpenStreetMap. Incluye redes eléctricas, gas, agua, telecomunicaciones y más. Stack con imposm3, MapLibre GL JS, Tegola y PostGIS.

## Por qué importa para David

- **Infraestructura OSM**: Pattern de extraer y visualizar infraestructura específica de OSM
- **PostGIS + Tegola**: Stack de tile server para rendering de datos geográficos complejos
- **MapLibre GL JS**: Motor de mapas web moderno y performante
- **Capas temáticas**: Pattern de capas de infraestructura que se puede adaptar

## Arquitectura

```
OSM Data (extract from planet.osm)
    ↓
imposm3 (import y transform)
    ↓
PostGIS (almacenamiento + queries)
    ↓
Tegola (tile server)
    ↓
MapLibre GL JS (frontend rendering)
```

## Instalación local

```bash
# Docker compose (oficial)
docker-compose up -d

# Requiere:
# - PostgreSQL + PostGIS
# - imposm3 para importar datos OSM
# - Tegola como tile server
# - MapLibre para frontend
```

## Integración con proyectos de David

- **España Atlas**: Capa de infraestructura para visualización regional
- **Time**: Mostrar infraestructura de transporte en isocronas
- **Control Center**: Dashboard de infraestructura urbana

## Pitfalls

- Datos OSM completos de España = varios GB, importación lenta
- Tegola requiere configuración de proveedores (PostGIS + SQL queries custom)
- imposm3 necesita mappers personalizados para extraer datos de infraestructura específicos
- No es trivial actualizar datos (need to reimport from fresh OSM extracts)

## Referencias

- GitHub: https://github.com/openinframap/openinframap
- Web: https://openinframap.org/
- Docs: https://github.com/openinframap/openinframap/tree/main/docs
- MapLibre: https://maplibre.org/
- Tegola: https://tegola.io/
