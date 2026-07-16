---
name: graphhopper-routing
description: GraphHopper — motor de routing rápido y eficiente para isocronas, rutas y geocoding.
category: routing-isochrones
---

# GraphHopper — Motor de Routing Rápido

## Qué es

GraphHopper es un motor de routing open-source de alta velocidad que ofrece:
- **Routing ultra-rápido** — uno de los más rápidos del mundo
- **Isocronas** — cálculo eficiente de polígonos de accesibilidad
- **Multimodal** — coche, bici, peatón, moto, truck
- **Traffic-aware** — routing considerando tráfico
- **Java-based** — fácil de integrar en JVM ecosystem

## Instalación

```bash
# Docker
docker run -p 8989:8989 graphhopper/graphhopper:latest

# O standalone
wget https://github.com/graphhopper/graphhopper/releases/latest/download/graphhopper-web.sh
chmod +x graphhopper-web.sh
./graphhopper-web.sh import europe-latest.osm.pbf
./graphhopper-web.sh server
```

## Uso básico

```bash
# Routing
curl 'http://localhost:8989/route?point=40.4168,-3.7038&point=41.3874,2.1686&vehicle=car'

# Isochrone
curl 'http://localhost:8989/isochrone?point=40.4168,-3.7038&range=300&vehicle=car'
```

## Casos de uso para David

- **Isocronas rápidas** — cálculo de accesibilidad en España
- **Routing multimodal** — integrar con GTFS
- **Comparativa** — comparar con Valhalla para validar resultados
- **Dashboard** — servir routing via REST API

## Pitfalls

- Los datos OSM grandes consumen mucha RAM (8GB+)
- La importación de datos es lenta (horas para Europa)
- Las isocronas requieren configuración adicional
- Menos documentación que Valhalla para casos avanzados

## Referencias

- Repo: `github.com/graphhopper/graphhopper` (6K⭐)
- Docs: `https://docs.graphhopper.com`
