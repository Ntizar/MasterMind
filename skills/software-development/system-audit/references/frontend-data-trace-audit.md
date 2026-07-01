# CIAF-visor: Data-Trace Audit — De 330 MB a 13 MB

## Contexto

CIAF-visor es un frontend SPA que visualiza informes de accidentes ferroviarios de España (CIAF, 2007-2025). El repo acumuló 330+ MB de archivos que el frontend nunca cargaba.

## Hallazgo

El frontend (`frontend/index.html`) solo cargaba:
1. `data/index.json` — lista de años
2. `data/reports/YYYY.json` — informes por año
3. `data/memorias/YYYY.json` — memorias anuales
4. APIs externas: IGN WMTS, ADIF WMS, ArcGIS LTV

Pero el repo contenía:

| Directorio/Archivo | Tamaño | ¿Lo usa el frontend? |
|-------------------|--------|---------------------|
| `pdfs/` (322 archivos) | 322 MB | ❌ Nunca |
| `data/images/` (249 archivos) | 249 MB | ❌ Nunca |
| `data/train-tracks.geojson` | 7.5 MB | ❌ Usa WMS en vivo |
| `ltv_lookup.json` | 170 KB | ❌ Carga ArcGIS en vivo |
| `data/station-coords.json` | 32 KB | ❌ Nunca referenciado |
| `data/relations.json` | 51 KB | ❌ Calcula in-memory |
| `scripts/` (archived) | varios | ❌ Completados |
| `frontend/css/`, `frontend/js/` | varios | ❌ Todo inline |

## Técnica aplicada

1. **grep en frontend** — buscar `fetch()`, `src=`, `href=` para mapear dependencias
2. **Cruzar** — cada archivo del repo → ¿lo referencia el frontend?
3. **Eliminar** — archivos huérfanos en un solo commit
4. **Regenerar** — `index.json` desde los JSONs limpios

## Resultado

- **Antes:** 330+ MB, ~500 archivos
- **Después:** 13 MB, 57 archivos
- **Commit:** `6e56f04` — 35 files changed, 43,512 deletions

## Pitfall: CI/CD roto

Tras eliminar archivos, el workflow `pages.yml` tenía `cp data/train-tracks.geojson data/relations.json frontend/css/` que ya no existían. Deploy falló. Fix: reescribir workflow para copiar solo `index.json`, `reports/*.json`, `memorias/*.json`, `index.html`.

## Lección

Cada vez que se limpian archivos de un repo, verificar `.github/workflows/` con `grep` por referencias a archivos eliminados.
