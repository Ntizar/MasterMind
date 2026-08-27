---
name: reearth-flow
description: Reearth Flow — herramienta ETL web para construir y ejecutar flujos de trabajo automatizados de datos geoespaciales.
---

# Reearth Flow — ETL Geoespacial

## Qué hace

[Reearth Flow](https://github.com/reearth/reearth-flow) es una herramienta ETL (Extract-Transform-Load) web para construir y ejecutar flujos de trabajo automatizados de datos geoespaciales. Permite calcular y convertir variables geométricas, ideal para pipelines de GIS.

## Instalación

```bash
# Necesita Rust y Go instalados
git clone https://github.com/reearth/reearth-flow.git
cd reearth-flow

# Construir el motor Rust
cd engine && cargo build --release && cd ..

# Construir el backend Go
cd server && go build -o reearth-flow . && cd ..
```

## Uso básico

```bash
# Iniciar el servidor
./reearth-flow --config flow.yaml --port 8080

# Definir un flujo (YAML)
# flow.yaml
# extract:
#   type: geojson
#   source: "https://example.com/data.geojson"
# transform:
#   - type: project
#     crs: "EPSG:4326"
#   - type: filter
#     condition: "area > 1000"
# load:
#   type: postgres
#   connection: "postgres://user:pass@localhost/gis"
```

```javascript
// API REST para ejecutar flujos
// POST /api/v1/flows/run
fetch('http://localhost:8080/api/v1/flows/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ flowId: 'my-flow' })
});
```

## Pitfalls

- Requiere configuración de PostgreSQL para el destino de carga
- El motor Rust necesita compilación desde fuente en algunas plataformas
- La documentación es limitada — consultar el código fuente para detalles
- Compatible con formatos GeoJSON, GML, Shapefile

## Referencias

- Repo: https://github.com/reearth/reearth-flow
- Relacionado: `geodeep`, `geoai-city2graph-pattern`, `cesium-3d-tiles-vector-data`, `ign-wmts-tiles`