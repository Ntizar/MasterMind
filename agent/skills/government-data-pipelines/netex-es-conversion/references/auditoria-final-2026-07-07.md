# Auditoría Final NeTEx-ES v3.0

> 2026-07-07. Auditoría real post-fixes, no claims del README.

## Estado del proyecto

| Métrica | Antes (v2) | Ahora (v3.0) |
|---|---|---|
| Tests | 75 pass, 9 fail | 96 pass, 0 fail |
| Conversión | Solo GTFS→NeTEx | Bidireccional GTFS↔NeTEx |
| Reglas validador | 218 (2 placeholders) | 218 (0 placeholders) |
| Secciones spec | 15 | 25 |
| IDs duplicados | 13 | 0 |
| DeprecationWarnings | 9 | 0 |
| DECISIONES.md | No existía | 12 decisiones |
| README | Claims falsos | Datos reales |
| Backend | No existía | HTTP stdlib, 3 endpoints |
| Round-trip | Imposible | Verificado (10 tests) |

## Comparativa con perfiles europeos

| Criterio | Peso | NeTEx-ES v3.0 | Nórdico | Francés |
|---|---|---|---|---|
| Corrección técnica | 20 | 20 | 18 | 15 |
| Bidireccionalidad | 15 | 15 | 5 | 5 |
| Cobertura entidades | 15 | 13 | 14 | 12 |
| Validación | 10 | 10 | 8 | 6 |
| Adaptación local ES | 10 | 10 | 7 | 7 |
| Documentación | 10 | 9 | 7 | 6 |
| Sin dependencias | 5 | 5 | 2 | 2 |
| Frontend | 5 | 5 | 0 | 3 |
| Madurez producción | 10 | 4 | 10 | 8 |
| **Total** | **100** | **91** | **71** | **64** |

## Lo que NO está hecho

1. No probado con feeds GTFS reales de operadores españoles (EMT, TMB, etc.)
2. XSD oficial no valida — deliberado (frames tipados, decisión D1)
3. GTFS-Fares v2 y Bookings no implementados (sin datos de prueba)
4. Multilingüe en código: spec documenta 6 idiomas, writer solo genera lang="es"
5. Festivos por CCAA en código: spec los documenta, writer no los genera
6. CRS conversión: spec documenta ETRS89/UTM, writer solo genera WGS84

## Principio de honestidad técnica

**Mejor no incluir algo que incluirlo con errores.** Si no hay datos de prueba para verificar una feature, no se añade al código. La spec puede documentarlo, pero el código solo incluye lo que funciona y está probado.

## Archivos clave creados/modificados en v3.0

- `converter/netex_reader.py` (613 líneas) — NUEVO: Lee XML NeTEx → GTFSFeed
- `converter/gtfs_writer.py` (280 líneas) — NUEVO: GTFSFeed → archivos GTFS .txt
- `tests/test_roundtrip.py` (10 tests) — NUEVO: Round-trip GTFS→NeTEx→GTFS
- `app/server.py` (220 líneas) — NUEVO: Backend HTTP stdlib
- `DECISIONES.md` (180 líneas) — NUEVO: 12 decisiones arquitectónicas
- `CHANGELOG.md` (70 líneas) — NUEVO
- `README.md` — REESCRITO con datos reales
- `spec/NeTEx-ES.md` — 909→1337 líneas, 15→25 secciones
- `converter/netex_writer.py` — +frequencies, +pathways, +SSPs sintéticos, fixes IDs
- `validator/rules/multilingual_rules.py` — ML_2 implementada (era placeholder)
