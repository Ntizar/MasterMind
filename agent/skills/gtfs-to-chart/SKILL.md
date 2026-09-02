---
name: gtfs-to-chart
version: "2.0.0"
description: "Use al crear gráficos stringline (Marey) desde GTFS."
tags: [gtfs, stringline, marey, horarios, visualizacion, transporte, nodejs]
related_skills: [gtfs-to-html-timetables, gtfs-to-blocks, gtfs-box, transit-data-pipelines]
---

# GTFS-to-Chart — Gráficos Stringline (diagramas de Marey)

**Repo fuente:** `github.com/BlinkTagInc/gtfs-to-chart` (MIT, Node.js, ~42⭐, mantenimiento activo) — mismo autor que gtfs-to-html y gtfs-to-blocks.

> ⚠️ Corrección 2026-09-02 (stars-explorer): la v1 decía "gráficos de frecuencia de rutas". Falso: genera **stringline charts** — el diagrama tiempo-estación de todos los vehículos de una línea (tipo Marey, 1873). Reescrito con el README real.

## When to Use

- Cuando pidas un **diagrama tiempo-recorrido (stringline/Marey/crayón)** de una línea de transporte desde GTFS.
- Para **comparar oferta entre fechas** (pre/post pandemia, cambio de temporada): dos gráficos y se ven huecos, solapes y cambios de velocidad.
- Para detectar **sobrepasos de servicios rápidos, tiempos de espera (dwell) y cruces de direcciones opuestas** de un vistazo.

## Qué genera

Eje X = estaciones **a escala de distancia**; eje Y = tiempo. Cada vehículo es una línea:
- **Pendiente = velocidad** (más vertical = más lento; tramos verticales cortos = dwell en parada).
- Dos direcciones en el mismo gráfico (bajada = ida, subida = vuelta); **cruces = vehículos que se rebasan/pasan**.
- Servicios exprés: se ven **adelantando** a los lentos (dos líneas de la misma pendiente que se cruzan).

Ejemplos vivos: `gtfs-charts.blinktag.com/sfmta-2020-03-10/14R.html` vs `.../sfmta-2020-07-21/14R.html`. Basado en código de Mike Bostock (Observable: "Marey's trains").

## Uso

```bash
npm install gtfs-to-chart -g
gtfs-to-chart --configPath /ruta/config.json
```

`config.json` (copiar de `config-sample.json`; todo `config*.json` está gitignored → múltiples ficheros tipo `config-caltrain.json`):

| opción | tipo | descripción |
|---|---|---|
| `agencies` | array | feeds GTFS por `url` o `path` local, cada uno con `agency_key` corto |
| `chartDate` | string | fecha concreta para generar el diagrama |
| `beautify` | boolean | formatear HTML de salida |
| `templatePath` | string | plantilla pug propia para render del chart |

```json
{ "agencies": [ { "agency_key": "mi-linea", "url": "http://.../google_transit.zip" } ] }
```

API en código: `import gtfsToChart from 'gtfs-to-chart'; gtfsToChart(config).then(...)`. Salida: HTML estático por ruta (comparable pre/post) — encaja en pipeline de digest estático publicable en GitHub Pages.

## Cuándo NO funciona (límites del propio README)

- Rutas donde no todos los viajes siguen el mismo patrón (paradas variables) → gráfico ilegible.
- Rutas con ida y vuelta por trazados distintos → no cuadran en un solo eje X.
- **Rutas circulares**: la línea salta a través del gráfico en la última parada (sin resolver).
- Es horario TEÓRICO (del feed); para comparación con la operación real → `gtfs-box` con GTFS-RT.

## Integración con proyectos de David

- **Análisis de oferta ferroviaria/autobuses España** (NAP DGT, MITMA S3): stringlines por línea Regional/rodalies para ver huecos de servicio y comparar temporada verano/invierno.
- Encaja en el patrón `static-digest-pipeline`: feed → chart → Pages, sin servidor.
- Hermandad de config con `gtfs-to-html` (horarios HTML) y `gtfs-to-blocks` (bloques de personal): mismo esquema `agency_key` + `url`/`path` — se puede compartir config.json entre los tres.
- Para stringlines de datos REALTIME en vez de teóricos, extender con `onebusaway-gtfs-realtime-visualizer` como referencia.

## Pitfalls

- Requiere Node moderno (ESM, `import`); usa better-sqlite3 → necesita toolchain de compilación en Windows si falla el prebuilt.
- Las frecuencias/dwell salen del feed; si el feed tiene horarios inconsistentes el gráfico los refleja (validar antes con `gtfs-tidy`).
- Comunidad pequeña (~42⭐) pero del autor mantenedor del ecosistema BlinkTag GTFS.

## Verificación

```bash
gtfs-to-chart --configPath config.json
# abrir out/<agency_key>/<date>/<route>.html
# comprobar: nº de líneas del chart == nº viajes del feed para esa fecha en esa ruta
```

## Referencias

- Repo: https://github.com/BlinkTagInc/gtfs-to-chart · npm: `gtfs-to-chart`
- Inspiración: observablehq.com/@mbostock/mareys-trains
- Reescrito por stars-explorer 2026-09-02 (v1→v2) tras leer README real.
