---
name: portolan-transit-maps
version: "1.0.0"
description: "Use al crear mapas tipo metro desde datos GTFS."
tags: [gtfs, transit-map, cartografia, osm, maplibre, go, pipeline, geospatial]
related_skills: [transit-map-simulation, gtfs-box-3d-viewer, transit-3d-realtime, gtfs-to-html-timetables]
---

# Portolan — Mapas de Tránsito que se Dibujan Solos

**Repo fuente:** `github.com/alexwohlbruck/portolan` (MIT, Go, activo 2026) — https://github.com/alexwohlbruck/portolan

## Qué es

**Pipeline GTFS → mapa de tránsito esquemático automático** (no estaciones sobre coordenadas, sino el clásico diagrama de metro con líneas de colores). Da un feed GTFS de una ciudad + geometría de vías de OpenStreetMap y produce cartografía donde:

- Cada línea tiene su color; líneas que comparten vía corren como **bandas paralelas con spacing uniforme**.
- Los corredores comparten una **línea central (centerline)** y las bandas se separan/unen con **curvas suaves en los nudos** a cualquier nivel de zoom.
- Estaciones agrupadas por datos de transbordo del propio feed (un complejo = una etiqueta con todos los marcadores de ruta).
- Reconstrucción de ciudad completa en **segundos** (compilación Go <1s), bucle edición→rebuild→revisión muy rápido.

17 ciudades configuradas (NYC, Chicago, Londres, París, Berlín, Tokio, **Barcelona**, Boston, Toronto, Viena, Santiago…), TODO por config en `portolan.json` — cero código específico por ciudad.

## Cuándo usar este skill

- Cuando pidas un **mapa tipo metro/esquemático** de una red de transporte (metro, tranvía, cercanías) generado desde GTFS real.
- Cuando haya que resolver el problema del "spaghetti": 15 líneas superpuestas en el mismo corredor.
- Diferenciación: `transit-map-simulation` = vehículos animados en tiempo real sobre mapa; `gtfs-box-3d-viewer` = visualización 3D de operación; **Portolan = cartografía esquemática generada automáticamente**.

## Uso básico

```bash
# Workbench interactivo (selector de ciudad, mapa vivo, slider de hora del día)
go run ./cmd/portolan atlas          # http://127.0.0.1:8765

# Construir una ciudad desde CLI
go run ./cmd/portolan chart --gtfs nyc.zip --rail nyc-rail.geojson --out nyc.geojson

# Extraer geometría de vías desde OSM
tools/feed.sh rail london

# Ciudades configuradas y estado de inputs
make cities
make city CITY=london   # construye + puntúa

# Score de calidad geométrica contra un dibujo humano de referencia
portolan sound --network testdata/sketches/nyc.json --build nyc.geojson
# → jaggedness / wobble p90 / desviación media / self-intersections / PASS-FAIL
```

## Las 7 etapas del pipeline (docs/ALGORITHM.md)

1. **CHART** — cargar y normalizar GTFS + geometría.
2. **SOUND** — sondeos de sección transversal perpendiculares para medir offsets entre vías.
3. **BUNDLE** — empaquetado de vías paralelas sostenidas y centerline por mediana.
4. **BERTH** — asignación de "atraques": qué ruta va en qué posición de la banda.
5. **ORDER** — orden de líneas dentro del corredor (heurística local, no solve exacto).
6. **FAIR** — alisado/fairing de curvas en nudos (forks que salen con rampa coseno).
7. **EMIT** — salida GeoJSON + gates de calidad.

## Leyes de geometría (docs/LESSONS.md — tercera tentativa, dos pipelines muertos)

Estas reglas son el verdadero valor del repo; cada una costó defectos visibles:

1. **NUNCA media ponderada por distancia → siempre mediana.** La media atrae "gravitatoriamente" la línea hacia strands extraños; la mediana adopta u ignora honestamente.
2. **Secciones transversales por intersección perpendicular, nunca proyección al punto más cercano** (la proyección se ancla a endpoints → cuerdas en extremos y sesgo en curvas).
3. **Las sondas caminan por el arco, nunca por la tangente recta** (±75 m rectos se salen del corredor en cada curva → esquinas cortadas de 10 m).
4. **Cambios de nº de strands con rampa, nunca escalón**: suavizar la SERIE de offsets (σ≈5 muestras), no la geometría.
5. **Bundling exige paralelismo sostenido** (≥~60 m dentro de ~12 m) — esto hace que los "kiss-welds" fantasma sean irrepresentables. El bundling es VISUAL (2D): vías apiladas sin conexión física también se agrupan.
6. **Extremos empalman en nodos con ventana escalada por offset** (~5 m de recorrido por m de offset, rampa coseno), y solo en nodos reales y asentados.
7. **Ley de diseño: prohibidas las pasadas de reparación.** Una salida mala = una etapa mala. Arreglar aguas abajo genera interacciones que rompen otros sitios (la lección que mató el intento 2: 13 passes `_fix_*` compitiendo entre sí).
8. **Nada de raster para la topología** — el esqueleto raster de eje medial (intento 2) lo cuantizaba todo: wobble, nodos 130 m desplazados, uniones fantasma, costuras de teselas. Geometría vectorial exacta end-to-end.

## Integración con proyectos de David

- **España Atlas / DataHub**: Barcelona ya está configurada en Portolan — patrón directo para mapa esquemático de metro desde feeds GTFS del consorcio.
- **Análisis de corredores GTFS**: detectar "corredor = paralelismo sostenido" es reutilizable para agrupar rutas por infraestructura compartida (planes de movilidad).
- **Calidad verificable**: el patrón "golden sketch + scorer PASS/FAIL" (desviación media <2 m vs dibujo humano) es exportable a cualquier pipeline geométrico — adoptar como práctica.
- Rendering con **MapLibre**: spacing uniforme en zoom continuo exige build de MapLibre con *variable line offsets*; con offsets fijos pre-horneados funciona MapLibre estándar.

## Pitfalls

- Buses NO implementados (necesitan modelo de corredor viario, no de vía); ferris sí (la shape publicada ES la geometría).
- Donde OSM no tiene vías, cae al shape tosco del feed (artefactos visibles).
- Interiores de nudos muy congestionados (tipo City Hall loop) aún con artefactos.
- Orden en corredores es estimación local — líneas pueden cruzarse sin razón en splits complejos.
- Proyecto joven (agosto 2026, ~48⭐): API inestable, leer docs/CLI.md de la versión clonada.

## Verificación

```bash
cd portolan && go build ./... && go run ./cmd/portolan chart --gtfs <feed.zip> --rail <rail.geojson> --out test.geojson
# Gate real: `portolan sound` contra testdata/sketches/nyc.json debe dar PASS
# (jaggedness max turn <~25°, 0 self-intersections, desviación media <2 m)
```

## Referencias

- docs/ALGORITHM.md (7 etapas), docs/LESSONS.md (leyes geométricas), docs/CITIES.md (añadir ciudad), docs/SERVICE-SCENARIOS.md (mapas por hora del día), docs/TOOLS.md (workbench y scorer)
- Creado por el pipeline stars-explorer el 2026-09-02.
