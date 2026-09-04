---
name: gtfs-tidy
description: "GTFS Tidy — validación y minimización de feeds GTFS con CLI Go (semánticamente equivalente)."
version: "2.0.0"
author: "David Antizar (Ntizar) — vía stars-explorer"
license: "GPL-2.0 (herramienta CLI; sin impacto al invocarla desde pipelines propios)"
tags: [gtfs, transporte, validacion, minimizacion, go, cli, datos-abiertos]
---

# GTFS Tidy — Limpieza y Validación de Feeds GTFS

## Qué es

`gtfstidy` (github.com/patrickbr/gtfstidy, Go, GPL-2.0, 149⭐, push 2026-08) es el CLI de referencia para **comprobar, sanear y minimizar feeds GTFS**. Garantía central: la salida es **semánticamente equivalente** al input — mismos trips con mismos atributos desde la perspectiva del viajero. Del mismo autor que `gtfs2shp` (herramienta hermana), muy usado en pipelines de datos de transporte.

Dato de peso (medido en su README): feed Suiza → `calendar_dates.txt` de 4,38M líneas/113MB a 456K líneas/6.6MB, y zip total 80MB→63MB. Praga → 16MB→9.4MB.

## Instalación

```bash
go install github.com/patrickbr/gtfstidy@latest   # o binarios en Releases
gtfstidy --help
```

## Uso

```bash
# Salida: -o <dir> suelta o -o archivo.zip (el .zip es OBLIGATORIO para zip)
gtfstidy -v feed.zip                    # solo validación (no processors)
gtfstidy -W feed.zip -o salida.zip      # validar + mostrar avisos
gtfstidy -eDnz -p '-' feed.zip -o s.zip # --fix: sanear sin minimizar
gtfstidy --compress feed.zip -o s.zip   # -OSRCcIAP: minimización segura
gtfstidy --Compress feed.zip -o s.zip   # + -T y emparejamiento difuso: máxima compresión
gtfstidy -SCRmTcdsOeD feed.zip -o s.zip # proceso completo (flags sueltos, orden interno fijo)
gtfstidy feed.zip -o s.zip --bounding-box -4.0,39.9,-3.0,40.6   # recorte geográfico
gtfstidy feed.zip -o s.zip --polygon-file madrid.geojson        # filtro por GeoJSON
gtfstidy feed.zip -o s.zip -M 2,3 -N 7                          # filtrar por modo (metro+tren, sin ferri)
```

## Flags de procesadores (verificados en `gtfstidy.go`)

| Flag | Qué hace |
|---|---|
| `-e` | valores por defecto GTFS en lugar de errores (campos no requeridos) |
| `-z` | arregla jerarquía del ZIP |
| `-n` | detecta coordenadas (0,0) |
| `-p <str>` | rellena campos requeridos vacíos no críticos |
| `-D` | **elimina** entradas erróneas (cascada: borra trips/stops huérfanos) → subconjunto sin errores |
| `-O [lista]` | elimina entidades huérfanas (all,agency,routes,services,shapes,stops,transfers,trips) |
| `-m` / `-r` | remide `shape_dist_traveled` / stop_times (rellena huecos interpolando) |
| `-s` | minimiza geometrías (Douglas-Peucker, ε≈1m en EPSG:3857; **implica -m**) |
| `-S` / `-R` / `-C` / `-P` / `-I` / `-A` | eliminan duplicados: shapes, rutas, servicios, paradas/niveles, trips, agencias |
| `-c` | minimiza `calendar.txt` + `calendar_dates.txt` (cobertura óptima rango/excepción) |
| `-T` | comprime trips explícitos en `frequencies.txt` (algoritmo CAP de Bast & Storandt; `-min-headway`/`-max-headway` lo acotan) |
| `-i` / `-d` | IDs densos numéricos / base-36 |
| `-E` | reclusteriza paradas (`-recluster-stops-dist` 75m, `-recluster-stops-simi` 0.55) |
| `-M` / `-N` | mantener / descartar lista de MOTs (1 tranvía, 2 metro, 3 tren, 4 bus, 5 barco, 6 teleférico, 7 ferri) |
| `-F` | conserva columnas extra no-GTFS del input |
| `--keep-*` | preserva IDs externos: `--keep-ids`, `--keep-trip-ids`, `--keep-route-ids`, `--keep-shape-ids`, `--keep-station-ids`, `--keep-service-ids`, `--keep-block-ids`... |

Regla mnemotécnica: **mayúsculas ELIMINAN o fusionan** entidades; minúsculas modifican.

## Orden de procesado (fijo, independiente del orden de flags)

1. `-e` defaults → 2. `-D` drop errores → 3. `-O` huérfanos → 4. `-m` remedir → 5. `-s` minimizar shapes → 6. `-S` → 7. `-R` → 8. `-C` → 9. `-c` → 10. `-T` → 11. `-i`/`-d` IDs.

## Casos de uso para David

- **Prefiltro en GBFSSpain / GTFS Spain**: antes de cargar feeds oficiales (Cercanías, EMT, metro) en el visor o en SQLite (node-gtfs), pasar `--compress` → menos MB, menos parsing, misma semántica. El recorte geográfico (`--bounding-box`) reduce feeds nacionales a Madrid/área de interés.
- **Diagnóstico de feeds rotos**: `gtfstidy -v feed.zip` detecta referencias rotas, headways inválidos, coordenadas 0,0, códigos ISO de idioma… complemento ligero del MobilityData GTFS Validator.
- **Planes de movilidad (plandemovilidad)**: `calendar_dates` inflados por operadores españoles → `-c` los convierte en patrones de calendario legibles.
- **Preparación para GIS**: encadenar con `gtfs2shp` (validar con `-v`, sanear `-eDnz`, exportar shapes/stations a QGIS).

## Pitfalls

- **Minimizar IDs (`-i`/`-d`) ROMPE referencias externas** (GTFS-RT, apps propias, dashboards que cacheen trip_ids). Si el feed se consume desde fuera: `--keep-ids` o no usar `-i`/`-d`. `--Compress` (mayúscula) incluye `-d` → **destruye referencias externas** por diseño.
- `--output` sin `.zip` escribe un **directorio**; para zip pon `-o salida.zip` (error común: sin extensión → carpeta sorpresa).
- `-T` reescribe la realidad: trips explícitos se funden en frecuencias. Semánticamente equivalente para el viajero, pero quien liste `trips.txt` verá muchos menos trips.
- `--bounding-box`/`--polygon` **cortan trips a mitad** salvo `--complete-filtered-trips`.
- `-D` silencia errores borrando datos: en feeds oficiales usa SIEMPRE primero `--fix` (`-eDnz -p '-'`) y revisa el diff de recuentos antes de aceptar `-D` masivo.
- Filtro de fechas: `-date-start` / `-date-end` como `YYYYMMDD`.
- El repo original estaba en `bfreuer/gtfstidy` → ahora `patrickbr/gtfstidy` (fork mantenido, más activo).

## Verificación

1. `gtfstidy -v feed.zip` sin errores (o lista clara de ellos) → base para decidir processors.
2. Tras procesar: comparar recuentos de `trips.txt`/`stop_times.txt` (antes vs. después) y abrir el zip de salida en el visor GTFS propio (gtfs-box / node-gtfs) — debe reproducir las mismas rutas y horarios.
3. Si se usó `-T`: comprobar en `frequencies.txt` que los headways generados son plausibles (`min-headway`/`max-headway`).

## Comparativa de alternativas (consultado 2026-09-04)

- **MobilityData/gtfs-validator** (Java): validación oficial más exhaustiva, pero sin capacidad de *sanear/minimizar*. gtfstidy = saneador + validador ligero; gtfs-validator = auditor certificado.
- **gtfs-kit** (Python): para análisis en notebook, no para limpiar feeds.
- **gtfs-manager** (skill `mobility/gtfs-manager`): gestión/edición interactiva de feeds locales.

## Referencias

- Repo: `github.com/patrickbr/gtfstidy` (148⭐)

## Comparativa de alternativas

- **[patrickbr/gtfstidy](https://github.com/patrickbr/gtfstidy)** — tidy GTFS en Go que minimiza tamaño y corrige inconsistencias con equivalencia semántica; una alternativa de validación/limpieza escrita en Go.
- Paper `-T`: Bast & Storandt, SIGSPATIAL 2014 (frequency extraction, CAP).
- Registry: `patrickbr/gtfstidy` — auditado v2.0.0 el 2026-09-04 contra README + `gtfstidy.go` (v1 tenía CLI inventado: `--input/--output`, `--validate`, `--info`).
