# Mega Auditoría NeTEx-ES — Hallazgos Detallados

> Fecha: 2026-07-07  
> Proyecto: `/root/workspace/netex/`  
> Repo: `github.com/Ntizar/netex` (privado)

## Puntuaciones reales (auditoría independiente)

| Dimensión | Real | README claim | Nórdico | Francés |
|---|---|---|---|---|
| IDs | 6/10 | 8/10 | 8/10 | 5/10 |
| Paradas | 8/10 | 10/10 | 8/10 | 5/10 |
| Modos | 8/10 | 9/10 | 8/10 | 6/10 |
| Tarifas | 5/10 | 9/10 | 9/10 | 4/10 |
| Packaging | 4/10 | 8/10 | 9/10 | 7/10 |
| Validación | 6/10 | 7/10 | 10/10 | 1/10 |
| Conversión GTFS | 7/10 | 9/10 | 5/10 | 7/10 |
| Calendarios | 6/10 | 8/10 | 7/10 | 6/10 |
| Geografía | 5/10 | 6/10 | 7/10 | 9/10 |
| Multilingüe | 1/10 | N/A | 5/10 | 3/10 |
| Flexible | 0/10 spec | 7/10 | 6/10 | 2/10 |
| Versionado | 0/10 | N/A | 7/10 | 3/10 |
| Accesibilidad | 2/10 | N/A | 6/10 | 4/10 |
| **TOTAL** | **~58/130** | **76/100** | **69/100** | **48/100** |

## Tests — estado real

- **Total:** 84 tests (75 passed, 9 FAILED)
- **Causa raíz de los 9 fallos:** Tests buscan PascalCase ('StopPlaces', 'Lines') pero NeTEx usa camelCase ('stopPlaces', 'lines'). El XML está bien, los tests están mal.
- **Tests afectados:** test_stop_places_generated, test_lines_generated, test_routes_generated, test_journey_patterns_generated, test_vehicle_journeys_generated, test_service_frames_generated (test_netex_writer.py) + test_full_conversion, test_conversion_without_options, test_id_uniqueness (test_integration.py)
- **Fix:** cambiar asserts a `assert 'stopPlaces' in xml_str` (camelCase)

## Validador — conteo real

- **218 clases Rule** con método `validate()` implementado (no 209)
- **18 módulos** en `validator/rules/`
- **~10 reglas con `pass`** (placeholders sin implementar)
- **Dependencia:** requiere `lxml` (no es 0-dependencia)
- **XSD validation falla:** HTTP 404 al descargar schema (URL obsoleta)
- **xpath_validator.py** usa lxml pero el converter usa stdlib ElementTree — incompatibilidad

### Reglas por módulo (verificado)

| Módulo | Reglas | Placeholders (pass) |
|---|---|---|
| frame_rules | 32 | 0 |
| stop_rules | 20 | 0 |
| journey_rules | 16 | 0 |
| fare_structure_rules | 15 | 0 |
| flexible_rules | 15 | 0 |
| packaging_rules | 15 | 0 |
| geometry_rules | 12 | 2 |
| interchange_rules | 12 | 2 |
| multilingual_rules | 12 | 2 |
| vehicle_rules | 12 | 2 |
| accessibility_rules | 10 | 0 |
| es_specific | 10 | 3 |
| service_rules | 10 | 1 |
| id_rules | 9 | 0 |
| line_rules | 11 | 1 |
| validity_rules | 5 | 1 |
| mode_rules | 2 | 1 |
| **TOTAL** | **218** | **~15** |

## Spec ↔ implementación — inconsistencias críticas

1. **IDs:** Spec `ES:StopPlace:MTM:28079:001` vs ejemplo `ES:StopPlace:CHAMARTIN:CHAMARTIN`
2. **PointOnRoute:** Spec usa `ref` atributo; ejemplo usa `<scheduledStopPointRef>` hijo + BUG (primero sin ref)
3. **StopPointInJourneyPattern:** Misma inconsistencia + BUG (primero sin StopPointRef)
4. **DayType:** Spec usa string `Mon Tue Wed`; ejemplo usa `<dayOfWeek>Monday</dayOfWeek>` anidado
5. **PlaceType:** Ejemplo usa `stopPlace` genérico donde debería ser `railStation`/`metroStation`
6. **OperatingName:** Todas las líneas dicen "Metro de Madrid" (incluyendo Renfe y EMT)
7. **transportSubMode:** Cercanías C1 = `highSpeedTrain` (debería ser `commuterTrain`)
8. **SalesOfferPackage:** Usado como canal de venta en vez de producto
9. **Sección 1.3 duplicada** en spec (1.3 Alcance + 1.3 Referencias Normativas)
10. **DECISIONES.md** referenciado 5+ veces pero NO EXISTE

## GTFS files no soportados por gtfs_reader.py

| Archivo GTFS | NeTEx equivalente | Estado |
|---|---|---|
| frequencies.txt | HeadwayJourneyGroup + Frequency | ❌ |
| pathways.txt | SitePath + PathLink | ❌ |
| levels.txt | LevelStructure | ❌ |
| translations.txt | MultilingualString | ❌ |
| fare_attributes.txt | FareStructure | ❌ |
| fare_rules.txt | FareStructureElement | ❌ |
| fare_products.txt (v2) | FareProduct + FareLegRule | ❌ |
| bookings.txt | BookingRule | ❌ |
| locations.geojson | zonas flexibles | ❌ |
| attribution.txt | — | ❌ |

## Gap: NO existe convertidor NeTEx→GTFS

Arquitectura propuesta para v3.0:
```
converter/
├── shared_model.py     # Modelo común (extender GTFSFeed)
├── gtfs_reader.py      # Lee GTFS (existe)
├── gtfs_writer.py      # Escribe GTFS (NUEVO)
├── netex_reader.py     # Lee NeTEx XML (NUEVO)
├── netex_writer.py     # Escribe NeTEx XML (existe)
├── gtfs_to_netex.py    # Pipeline directo (refactorizar)
├── netex_to_gtfs.py    # Pipeline inverso (NUEVO)
└── cli.py              # CLI bidireccional
```

Mapeo NeTEx→GTFS:
- StopPlace+Quay → stops.txt (location_type=1+0)
- Line → routes.txt (route_type desde transportMode/subMode)
- VehicleJourney → trips.txt
- Call → stop_times.txt
- DayType+DayTypeAssignment → calendar.txt + calendar_dates.txt
- FareZone → stops.txt zone_id
- LineGeometry → shapes.txt
- Connection → transfers.txt
- Operator → agency.txt
- FlexibleLine → trips.txt + bookings.txt

## Plan de acción v3.0 (8 fases, ~25-35 días)

1. **Estabilizar** (1-2d): fix tests, warnings, README, .gitignore
2. **Cerrar gap spec↔código** (3-5d): unificar IDs, Route, JP, DayType, DECISIONES.md
3. **Añadir gaps a spec** (5-7d): multilingüe, FlexibleLine, Authority, packaging, versionado, accesibilidad, festivos CCAA, CRS, NAP
4. **Convertidor NeTEx→GTFS** (5-7d): netex_reader, gtfs_writer, shared_model, round-trip tests
5. **Mejorar GTFS→NeTEx** (3-5d): frequencies, pathways, translations, GTFS-Fares v2, bookings
6. **Mejorar validador** (3-5d): implementar placeholders, fix XPath, CI
7. **App/frontend** (2-3d): backend, deploy, validación visual
8. **Documentación** (2-3d): README real, guía NAP, ejemplos reales

## Objetivo v3.0

Con v3.0, NeTEx-ES superaría al nórdico en 11 de 14 dimensiones y al francés en 13 de 14. La clave: bidireccionalidad GTFS↔NeTEx + multilingüe + spec normativa respecto al código.
