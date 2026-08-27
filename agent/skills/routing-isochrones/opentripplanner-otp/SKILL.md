---
name: opentripplanner-otp
version: "1.0.0"
description: "OpenTripPlanner — planificador de rutas multimodal con GTFS, OSM, GraphQL API y actualizaciones en tiempo real"
---

# OpenTripPlanner (OTP) — Multi-Modal Trip Planner

## Descripción

OpenTripPlanner es un planificador de rutas multimodal de código abierto, enfocado en transporte público combinado con bicicleta, caminar y servicios de movilidad. Usa datos GTFS y OpenStreetMap como fuentes principales.

## Por qué importa para David

- **Core de transporte público**: OTP es la referencia open-source en planificación de rutas multimodales
- **GraphQL API**: Expone APIs GraphQL que pueden integrarse directamente en dashboards frontend
- **Real-time**: Soporta actualizaciones en tiempo real de servicio/alertas
- **GTFS + OSM**: Pipeline de datos que David ya usa en otros proyectos (Time, Esios)

## Arquitectura

```
OSM Data + GTFS Feeds
    ↓
OTP Server (Java)
    ↓
GraphQL API + REST API
    ↓
Frontend (OTP-UI / custom)
```

- Backend: Java (JVM), Docker-native
- Branch actual: OTP 2.x (dev-2.x), bajo desarrollo activo desde 2018
- Datos: GTFS estático + GTFS-Realtime para actualizaciones

## Uso básico

```bash
# Docker compose (oficial)
docker-compose up -d

# API GraphQL endpoint
curl -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ plan(fromLatitude: 40.4168, fromLongitude: -3.7038, toLatitude: 40.4530, toLongitude: -3.6883) { ... } }"}'
```

## Integración con proyectos de David

- **Time**: Usar OTP como backend de routing (alternativa a ORS)
- **Esios Dashboard**: Mostrar rutas multimodales con datos en tiempo real
- **GTFS data pipeline**: OTP consume GTFS → reutilizar los ingestores existentes
- **Real-time alerts**: OTP soporta GTFS-Realtime feed updates

## Pitfalls

- OTP 2.x tiene API diferente de OTP 1.x — verificar versión antes de integrar
- Requiere descargar y procesar datos OSM grandes (España completo = varios GB)
- Java JVM requiere 1-2GB RAM mínimo
- El rendering de mapas depende de OTP-UI o integración custom con Leaflet/MapLibre

## Referencias

- GitHub: https://github.com/opentripplanner/OpenTripPlanner
- Docs: https://docs.opentripplanner.org/
- Docker: https://hub.docker.com/r/opentripplanner/opentripplanner
- OTP-UI (frontend): https://github.com/opentripplanner/otp-ui
