---
name: geospatial-mcp-power-pack
description: "21 MCP geoespaciales modulares con router de orquestación."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [mcp, geoespacial, uvx, stac, raster, orquestacion, agentes]
    related_skills: [native-mcp, mcp-servers-modelcontextprotocol, osm-infrastructure-mapping]
---

# Power-pack de MCP geoespaciales

Pack de **21 paquetes** Python: el Power Hub (`kiro-geospatial`), la base compartida (`geo-common`) y **19 servidores MCP** (56 herramientas), instalables à la carte con `uvx`, con un **router de orquestación** discover → process → analyze con degradación elegante.

## When to Use (cuándo usarlo)

- Quieres **dar capacidades geoespaciales a un agente** sin escribir conectores desde cero.
- Diseñas tu propio servidor MCP: aquí está el contrato base (`BaseGeoServer`), taxonomía de errores y manejo de rate-limit.
- Necesitas un patrón de **orquestación multi-servidor** con resultado parcial etiquetado.

## Instalación real (cada server es un paquete Python)

```bash
uvx kiro-geospatial        # hub
uvx geo-stac               # catálogos STAC
uvx geo-vector             # vectores
uvx geo-geocode-route      # geocoding + routing
uvx geo-terrain            # terreno/DEM
uvx geo-weather-climate
uvx geo-biodiversity
uvx geo-ops
uvx geo-raster
uvx geo-pointcloud
uvx geo-index
uvx geo-foundation-models
uvx geo-embedding-search
uvx geo-warehouse
uvx aws-geo-compute
uvx geo-formats            # conversión de formatos
uvx geo-query              # consultas espaciales
uvx geo-commercial-imagery # imagery comercial
uvx geo-ogc                # servicios OGC
uvx geo-3d                 # datos 3D
# + geo-common (base compartida, no se lanza solo) = 21 paquetes en packages/
```

## Arquitectura en 3 pilares (regla de diseño explícita)

- **A — Conectores**: catálogos, imagery, vector, geocoding/routing, terrain, weather/climate, biodiversity.
- **B — Procesado**: CRS, geometría, formatos, spatial SQL, raster/zonal stats, point clouds, indexación.
- **C — GeoAI**: embeddings, segmentación, vector search, change detection.
- Regla: **B nunca con menos servidores que A**.

`geo-common` aporta el cliente HTTP async (httpx con retry + backoff exponencial), `Error_Taxonomy` común, manejo de rate-limit y el contrato `BaseGeoServer`.

Router: orden estricto de pilares, consultas concurrentes y **degradación elegante** — si una fuente falla se registra provenance y el resultado se etiqueta `partial`.

## QA de desarrollo (Makefile)

```bash
make venv            # Python 3.12 + mcp, pytest, hypothesis, moto, geo-common editable
make install-smoke
make install-heavy
make smoke-mcp SERVERS="geo-index geo-ops"     # por defecto: geo-index geo-embedding-search
```

Incluye `skills/` listos para copiar como skills de agente: `stac-metadata.md`, `cloud-optimized-formats.md`, `crs-handling.md`, `spatial-sql.md`, `geoai-embedding.md`, `tiling.md`, `geometry-complexity.md`, `tool-selection.md`; y `examples/` con backend local de Clay/Prithvi y embeddings custom.

## Pitfalls

- Instalar los 21 servidores satura el contexto del agente: **activar solo los que se usen** (à la carte es el diseño).
- `aws-geo-compute` y `geo-warehouse` (AWS/warehouse) y `geo-commercial-imagery` (Maxar vía Sentinel Hub TPDI, Planet Data/Orders: propietario/licenciado) asumen servicios externos de pago; el resto es local/abierto.
- Es material de `aws-samples` (repo de ejemplo): verificar mantenimiento antes de depender de un paquete concreto.

## Referencia

- Repo: `aws-samples/sample-geospatial-kiro-power-pack` (~19 ⭐, consultado 2026-09-15). Detalles en `POWER.md`.
