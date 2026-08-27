---
name: valhalla-routing
description: Valhalla — motor de routing open-source de Mapbox para isocronas, rutas multimodales y geocoding.
category: routing-isochrones
---

# Valhalla — Motor de Routing Open-Source

## Qué es

Valhalla de Mapbox es un motor de routing open-source de alta calidad que ofrece:
- **Routing multimodal** — coche, bici, peatón, moto, transporte público
- **Isocronas** — polígonos de accesibilidad temporal
- **Geocoding** — búsqueda de direcciones y POIs
- **Traffic-aware** — routing considerando tráfico en tiempo real
- **Tile generation** — generación de tiles vectoriales desde OSM

## Instalación

```bash
# Docker (recomendado)
docker pull ghcr.io/mapbox/valhalla:latest

# O compilar desde fuente
git clone https://github.com/valhalla/valhalla.git
cd valhalla
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
```

## Uso básico

```bash
# Routing simple
curl -X POST 'http://localhost:8002/route' \
  -H 'Content-Type: application/json' \
  -d '{
    "locations": [
      {"lat": 40.4168, "lon": -3.7038},
      {"lat": 41.3874, "lon": 2.1686}
    ],
    "mode": "car"
  }'

# Isochrone
curl -X POST 'http://localhost:8002/isochrone' \
  -H 'Content-Type: application/json' \
  -d '{
    "locations": [{"lat": 40.4168, "lon": -3.7038}],
    "range": [300, 600, 900],
    "range_type": "time",
    "mode": "drive"
  }'
```

## Casos de uso para David

- **Isocronas** — calcular accesibilidad temporal en España
- **Routing multimodal** — coche + transporte público
- **Traffic-aware** — routing considerando tráfico real
- **Integración con Three.js** — visualizar rutas en 3D

## Pitfalls

- Necesita datos OSM (download desde geofabrik.de)
- La inicialización del motor es lenta (minutos)
- Las isocronas pueden ser lentas para áreas grandes
- Configurar traffic requiere datos adicionales
- El motor consume ~2-4GB RAM

## Referencias

- Repo: `github.com/valhalla/valhalla` (5K⭐)
- Docs: `https://valhalla.readthedocs.io`
- Datos OSM: `https://download.geofabrik.de`
