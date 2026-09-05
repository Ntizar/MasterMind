---
name: gtfs-to-html-timetables
description: "Usa a generar horarios HTML desde GTFS."
version: "2.0.0"
tags: [gtfs, horarios, html, blinktag, gtfs-to-html, timetable]
related_skills: [gtfs-to-html-timetables, gtfs-to-chart, gtfs-to-blocks, gtfs-box]
---

# GTFS-to-HTML — horarios legibles desde GTFS

> ⚠️ Corrección 2026-09-05 (auditoría): claves de config correctas son **`agencies`** (array), **`outputFormat`** y **`outputPath`**; el flag CLI es **`--configPath`**. `routes:['1']` no es una opción documentada.

**Repo:** `https://github.com/BlinkTagInc/gtfs-to-html` (TypeScript, ~228⭐). Docs: `gtfstohtml.com/docs/configuration`.

## When to Use

- Cuando pidas **generar horarios de transporte legibles en HTML** desde un feed GTFS.

## Uso (API/cli real)

```bash
gtfs-to-html --configPath config.json
```

```json
{
  "agencies": [ { "agency_key":"mi", "url":"http://.../google_transit.zip" } ],
  "outputFormat": "html",        // antes 'format'
  "outputPath": "output"         // antes 'output'
}
```

## Pitfalls

- Config: **`agencies`** (array), **`outputFormat`**, **`outputPath`** — no `agency`/`format`/`output`.
- CLI: **`--configPath`**, no `--config`.
- `routes:['1']` no es opción documentada (mirar gtfstohtml.com/docs).

## Verificación

- Correr con `--configPath` y abrir el HTML de ruta generado.
