---
name: reearth-flow
description: Reearth Flow — plataforma ETL geoespacial web (motor Rust DAG + servidor Go GraphQL + UI ReactFlow) con 167 acciones tipo FME para CityGML/3D Tiles/GeoJSON.
version: 2.0.0
tags: [gis, geospatial, etl, dag, rust, citygml, 3dtiles, workflow, plateau, cesium]
related_skills: [reearth-visualizer, cesium-3d-tiles-vector-data, plateau-3d-city-mcp, gtfs-tidy, photorealistic-3d-tiles-threejs]
---

# Re:Earth Flow — ETL geoespacial con DAG (motor Rust)

> **Repo:** https://github.com/reearth/reearth-flow · Rust ~9.8 MB + Go + TypeScript · Apache-2.0/MIT · activo (push diario). El README público dice poco ("WIP") — el conocimiento real está en `docs/architecture.md` y `engine/`. Verificado leyendo el código fuente el 2026-09-02.

## Qué es (real)

Monorepo de una plataforma web de workflows ETL geoespaciales, inspirada en FME:

- **`engine/`** — motor de ejecución de DAGs en **Rust**: 167 acciones (source/transform/sink) definidas en `engine/schema/actions.json`.
- **`server/`** — backend **Go** con API GraphQL, MongoDB, colaboración en tiempo real.
- **`ui/`** — frontend **React/TypeScript** con editor visual de flujos (ReactFlow + sincronización Yjs vía WebSocket).

**Flujo end-to-end:** UI diseña el workflow (YAML/JSON validado contra `engine/schema/workflow.json`) → mutation GraphQL lo persiste en MongoDB → Server lo envía a Google Cloud Batch → el Engine ejecuta el DAG y escribe resultados en GCS/S3 → logs y eventos van a Google Pub/Sub → Subscriber los vuelca a MongoDB/Redis → GraphQL subscriptions los retransmiten a la UI → visualización en Cesium.

## El motor: acciones y workflows

**167 acciones** en categorías claras (fuente: `engine/schema/actions.json`, con i18n en `actions_{es,fr,ja,zh}.json`):

- **Lectura/escritura:** CSV, JSON, GeoJSON, GeoPackage, Shapefile, CityGML 2/3, OBJ, CZML, Excel, MVT Writer, **Cesium 3D Tiles Writer**, SQL Reader, HTTP Caller
- **Geometría:** Bufferer, Clipper, Dissolver, Convex Hull, CSG Builder/Evaluator, Extruder, Offsetter, Reprojectors (horizontal / coordinate frame), Geometry Validator/Splitter/Coercer, Grid Divider, Neighbor Finder, Ray Intersector
- **Atributos/features:** Attribute Manager/Mapper/Flattener/Aggregator, Feature Filter/Joiner/Merger/Sorter/Counter, Spatial Filter, Statistics Calculator
- **Serie PLATEAU (`PLATEAU3/4/6.*`):** validadores y extractores para Project PLATEAU de Japón — UDXFolderExtractor, MissingAttributeDetector, UnmatchedXlinkDetector, SolarPositionCalculator, FloodAreaSurfaceGenerator... → es **el reference implementation de pipelines de validación CityGML**; adaptable a otros catálogos 3D urbanos.
- **Scripting embebido:** `Python Script Processor` (Python 3.11+) y `action-wasm-processor` (WASM) para lógica custom dentro del DAG.

**Formato de workflow** (YAML, `required: [id, name, entryGraphId, graphs]`, opcional `with` y `errorPolicy`):

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/reearth/reearth-flow/main/engine/schema/workflow.json
id: 00caad2a-9f7d-4189-b479-153fa9ea36dc
name: "SimpleWorkflow"
entryGraphId: 3e3450c8-2344-4728-afa9-5fdb81eec33a
graphs:
  - id: 3e3450c8-2344-4728-afa9-5fdb81eec33a
    name: entry_point
    nodes:
      - id: 90f40a3e-...
        name: Feature Creator
        type: action
        action: Feature Creator        # debe existir en actions.json
        with:
          creator: |
            [ { "testAttribute": "test01" } ]
```

Los nodos se conectan por puertos tipo FME (sources → processors → sinks). Expresiones inline con `#{...}` dentro de `with`.

## Uso del CLI (modo standalone, sin server)

```bash
cd engine && cargo build --release --bin reearth-flow
# dependencias: Rust stable + libxml2 (Windows: vcpkg install libxml2:x64-windows;
# Linux: libxml2-dev + pkg-config) — sin ellas el build falla con errores de gdal-bindings/xml
./target/release/reearth-flow run --workflow ruta/al/workflow.yaml   # "-" = stdin
./target/release/reearth-flow dot --workflow f.yaml    # grafo del DAG en GraphViz
./target/release/reearth-flow doc-action               # documentación de las 167 acciones
./target/release/reearth-flow schema-workflow          # JSON Schema de workflows
./target/release/reearth-flow view                     # feature-viewer (visord) de resultados
```

`run` auto-escala Rayon a `min(1.2×n_cpus, 64)` threads. Observabilidad nativa OpenTelemetry (`logger::setup_logging_and_tracing` → var de entorno OTel estándar).

## Cuándo usar Re:Earth Flow (vs alternativas)

| Necesidad | Elección |
|---|---|
| Pipeline GIS reproducible con transformación CityGML/3D Tiles, open-source, self-host | **reearth-flow** |
| Solo conversión GTFS→NeTEx / feeds estáticos | `netex-es-conversion`, `gtfs-tidy` |
| Visualización 3D de ciudades en web | `cesium-3d-tiles-vector-data` + output `Cesium 3D Tiles Writer` de Flow |
| Datos PLATEAU Japón 3D city MCP | `plateau-3d-city-mcp` (usa outputs compatibles) |
| ETL general no-geoespacial | FME (comercial) o dbt — Flow es GIS-first |

**Patrón trasladable a proyectos de David (DataHub España / España Atlas):** DAG YAML declarativo + schema JSON validado + catálogo de acciones con i18n + sink 3D Tiles para visualización Cesium. El `Area On Area Overlayer`, `Attribute Aggregator` y `Spatial Filter` cubren gran parte de lo que hoy se hace a mano con geopandas en los dashboards.

## Pitfalls

- **El README del repo es un cascarón** — NO juzgar el proyecto por él; la doc real vive en `docs/architecture.md`, `engine/README.md` y `engine/AGENTS.md`.
- Monorepo: el motor NO compila sin libxml2/pkg-config (en Windows vía vcpkg, paso manual obligatorio).
- `server/` acopla MongoDB + GCP Batch + Pub/Sub: para uso local, usar solo el CLI del engine y workflows YAML.
- Orden de arranque de servicios: MongoDB → Server API → WebSocket → UI (la API debe estar antes que el WebSocket por auth).
- Variables de entorno con prefijos: `FLOW_*` (app), `REEARTH_*` (plataforma), `GOOGLE_*` (credenciales).
- Los nombres de acciones llevan espacios (`"Feature Creator"`) — en YAML irrompibles; validar contra `actions.json`, no adivinar.

## Verificación

```bash
curl -s https://raw.githubusercontent.com/reearth/reearth-flow/main/engine/schema/actions.json \
  | python -c "import json,sys; print(len(json.load(sys.stdin)['actions']),'acciones')"
# → 167 acciones (2026-09-02)
```

## Referencias

- Repo: https://github.com/reearth/reearth-flow · Docs: `docs/architecture.md`, `CHANGELOG.md` (394 KB — histórico vivo del proyecto)
- Esquemas: `engine/schema/{workflow,actions,feature-intermediate,error-codes}.json`
- Ejemplos de workflows de test: `engine/testing/workflow-tests/`
- Origen del motor: fork evolucionado de `flowy-gis/flowy` (Rust)
