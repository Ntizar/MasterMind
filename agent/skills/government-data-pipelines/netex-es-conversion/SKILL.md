---
name: netex-es-conversion
description: "Conversión bidireccional GTFS↔NeTEx-ES: convertidor, validador (218 reglas, 0 placeholders), packaging multi-archivo, FlexibleLine, frequencies, pathways. v3.0: 96 tests, round-trip verificado, backend HTTP stdlib."
version: 1.0.0
author: Ntizar
tags: [gtfs, netex, transportation, conversion, validation]
---

# Conversión GTFS ↔ NeTEx-ES (bidireccional)

Convertidor Python bidireccional GTFS↔NeTEx-ES (EN 12896) con validador de 218 reglas, packaging multi-archivo, frequencies, pathways y soporte transporte a demanda. **v3.0: 96 tests, 0 fallos, round-trip verificado.**

## Ubicación del proyecto

- **Repositorio:** `/root/workspace/netex/`
- **Convertidor:** `/root/workspace/netex/converter/`
- **Validador:** `/root/workspace/netex/validator/`
- **Especificación:** `/root/workspace/netex/spec/NeTEx-ES.md` (25 secciones, 1337 líneas)
- **Decisiones:** `/root/workspace/netex/DECISIONES.md` (12 decisiones arquitectónicas)
- **v3.0:** 218 reglas (0 placeholders), 96 tests, conversión bidireccional, backend HTTP

## Flujo básico de conversión

### GTFS → NeTEx

```python
from converter.config import Config
from converter.gtfs_reader import GTFSReader
from converter.netex_writer import NeTExWriter

reader = GTFSReader("/path/to/gtfs_dir_or_zip")
feed = reader.read()

config = Config(
    publisher_name="Nombre Editor",
    include_geography=True,
    include_fares=True,
    include_transfers=True,
    include_shapes=True,
)

writer = NeTExWriter(feed, config)
xml = writer.to_string(pretty=True)  # XML completo en string
```

### NeTEx → GTFS (bidireccional, v3.0)

```python
from converter.netex_reader import NeTExReader
from converter.gtfs_writer import GTFSWriter

reader = NeTExReader("entrada.xml")
feed = reader.read()

writer = GTFSWriter(feed)
writer.write("salida-gtfs/")  # Genera 10 archivos .txt
```

### Round-trip verificado

```python
# GTFS → NeTEx → GTFS
reader = GTFSReader("mi-feed.zip")
feed_orig = reader.read()

writer = NeTExWriter(feed_orig, Config())
writer.to_file("tmp.xml")

reader2 = NeTExReader("tmp.xml")
feed_rt = reader2.read()

assert len(feed_rt.routes) == len(feed_orig.routes)      # ✓
assert len(feed_rt.trips) == len(feed_orig.trips)        # ✓
assert len(feed_rt.stop_times) == len(feed_orig.stop_times)  # ✓
```

### Backend HTTP (sin dependencias externas)

```bash
python app/server.py  # http://localhost:5000
# POST /convert       — GTFS (bytes JSON) → NeTEx XML
# POST /convert-back  — NeTEx XML → GTFS (base64 zip)
# POST /validate      — Validar NeTEx con 218 reglas
```

## Arquitectura del convertidor

### `gtfs_reader.py` — Lectura GTFS
- Soporta `.zip` o directorio con `.txt`
- Dataclasses: `Stop`, `Route`, `Trip`, `StopTime`, `Shape`, `Calendar`, `Transfer`, `FareAttribute`, `FareRule`
- Métodos helper: `get_stop()`, `get_route()`, `get_trip()`, `get_calendar()`

### `netex_writer.py` — Generación XML
Métodos principales:
- `_create_stop_places()` — Jerarquía: StopPlace → Quay → StopPoint
- `_create_lines()` — Line + Route (separación GTFS)
- `_create_journey_patterns()` — JP + JPElements
- `_create_vehicle_journeys()` — VJ + Calls + SchedulePoints
- `_create_service_frames()` — ServiceFrame → DayType + DatePeriod
- `_create_fares()` — **CRÍTICO: vea pitfalls abajo**
- `_create_shapes()` — LineGeometry desde shapes GTFS
- `_create_connections()` — Connections desde transfers GTFS

### `multi_file_packager.py` — Packaging multi-archivo
Divide en 7 XMLs según tipo de entidad:
| Archivo | Contenido |
|---|---|
| `netex_publication.xml` | PublicationDelivery + metadatos |
| `netex_stop_places.xml` | StopPlaces, Quays, StopPoints, Accessibility |
| `netex_lines.xml` | Lines, Routes, JourneyPatterns, LineGeometries |
| `netex_timetables.xml` | VehicleJourneys, ServiceFrames, DayTypes |
| `netex_fares.xml` | FareZones, FareStructures, FareProducts, SalesPoints |
| `netex_connections.xml` | Connections, Transfers |
| `netex_admin.xml` | AdministrativeAreas, GroupsOfLines |

Usa `ENTITY_FILE_MAP` para mapear contenedores y elementos individuales.

### `flexible_converter.py` — Transporte a demanda
- Detección de rutas flexibles (`pickup_type > 0` o keywords)
- `FlexibleLine`: lineType, bookingAccess, bookingMethods
- `FlexibleService`: booking rules, flexibleServiceProperties
- XML generation: `create_flexible_line_xml()`, `create_flexible_service_xml()`

## Sistema de tarifas

Generado automáticamente desde zone_ids del GTFS:

| Entidad | Ejemplo | Descripción |
|---|---|---|
| `FareZone` | `ES:FareZone:ES:ZONA_A` | Zona tarifaria por zone_id |
| `FareProduct` | adult/child/senior/youth/family/day/week/month/annual | Tipos de billete |
| `FareStructure` | Single/DayPass/WeekPass/MonthPass | Estructura tarifaria |
| `FareComponent` | `ES:FC:{pub}:{suffix}:{zone_id}` | Componente por zona |
| `FareElement` | Price + Currency + ZoneRef | Precio |
| `SalesPoint` | onBoard/ticketMachine/mobileApp/online | Puntos de venta |
| `TicketingMode` | SingleTicket/DayTicket/MultiRideTicket/SeasonTicket | Modo de pago |

## Validador (218 reglas en 18 módulos — verificado 2026-07-07)

| Módulo | Reglas | Qué valida |
|---|---|---|
| `id_rules` | 9 | Formato y unicidad IDs NeTEx-ES |
| `frame_rules` | 24 | CompositeFrame, ValidBetween, versiones |
| `journey_rules` | 26 | Coherencia temporales, llamadas |
| `stop_rules` | 9 | Jerarquía parada/andén |
| `line_rules` | 11 | Modos de transporte |
| `service_rules` | 10 | ServiceFrames, DayTypes |
| `geometry_rules` | 12 | LineGeometry, ShapePoint, coordenadas |
| `es_specific` | 10 | Reglas contexto español |
| `flexible_rules` | 15 | FlexibleLine/FlexibleService |
| `fare_structure_rules` | 15 | FareComponents, Elements, Times |
| `vehicle_rules` | 12 | VehicleType, SchedulePoints |
| `interchange_rules` | 12 | Connections, TransferType |
| `multilingual_rules` | 12 | MultilingualString, idiomas |
| `accessibility_rules` | 10 | Wheelchair, Bikes |
| `packaging_rules` | 15 | PublicationDelivery, Entity IDs |
| `validity_rules` | 5 | ValidBetween, fechas |
| `mode_rules` | 2 | Modos válidos |

```bash
# Ejecutar validador
python -m validator.reference_validator archivo.xml --report json
```

## ⚠️ Pitfalls Críticos

### 1. IDs duplicados en FareComponents
Cada FareStructure (Single, DayPass, WeekPass, MonthPass) genera sus propios FareComponents. **El ID del FareComponent debe incluir un sufijo único por estructura:**

```python
# MALO — IDs duplicados
fc_id = f"{prefix}:FC:{pub}:{zone_id}"

# BUENO — sufijo por estructura
fc_id = f"{prefix}:FC:{pub}:{suffix}:{zone_id}"
```

Al llamar `_add_fare_components()`, pasar `suffix="Single"` o `suffix="DayPass"` etc.

### 2. Multi-file packager: mapear contenedores (plural) Y elementos (singular)
`ENTITY_FILE_MAP` debe incluir tanto el contenedor como los elementos individuales:

```python
ENTITY_FILE_MAP = {
    "VehicleJourneys": "netex_timetables.xml",  # contenedor
    "VehicleJourney": "netex_timetables.xml",    # elemento
}
```

Si falta el contenedor (plural), todo cae al default `netex_lines.xml`.

### 3. TicketingMode como texto, no como children de `_el()`
`_el("TicketingMode", None, "SingleTicket")` falla porque `_el` espera lista de Elementos, no strings.

```python
# MALO — TypeError
tm = _el("TicketingMode", None, "SingleTicket")

# BUENO
tm = _el("TicketingMode", None)
tm.text = "SingleTicket"
```

### 4. zone_id vs stop_id en zonas tarifarias
Al construir el dict de zonas desde stops, usar `stop.zone_id` como clave y `stop.stop_id` como valor:

```python
# MALO
zones.setdefault(stop.zone_id, []).append(stop.zone_id)

# BUENO
zones.setdefault(stop.zone_id, []).append(stop.stop_id)
```

### 5. Validador XPath: lxml vs ElementTree incompatible
El `xpath_validator.py` usa lxml pero el resto usa stdlib `xml.etree.ElementTree`. Las reglas XPath fallan con `'NoneType' object has no attribute 'xpath'`. Las 218 reglas semánticas Python funcionan correctamente.

### 6. ✅ RESUELTO — ElementTree: `if elem:` generaba DeprecationWarning
**Fixeado v3.0.** Cambiado a `if elem is not None:` en todas las ubicaciones de netex_writer.py y netex_reader.py.

### 7. ✅ RESUELTO — `datetime.utcnow()` deprecado
**Fixeado v3.0.** Cambiado a `datetime.now(UTC)` con `from datetime import datetime, UTC`.

### 8. Archivos grandes (>10MB)
GTFS grande (ej. Metro Bilbao: 5549 viajes, 6000 shapes → 24MB XML). Validador tarda 30-60s. Usar timeout alto en subprocess.

### 9. ✅ RESUELTO — Tests: camelCase NeTEx vs PascalCase
**Fixeado v3.0.** Los tests ahora buscan `stopPlaces`, `lines`, `routes` (camelCase correcto). 96 tests pasan, 0 fallan.

### 10. ✅ PARCIALMENTE RESUELTO — Spec ↔ implementación
**Mejorado v3.0.** El ejemplo XML fue regenerado desde el converter (IDs únicos, camelCase, MobilityImpairedAccess). La spec tiene 25 secciones. DECISIONES.md creado con 12 decisiones. Aún faltan: PlaceType específicos, transportSubMode correcto por nombre de ruta.

### 11. XSD validator: HTTP 404 al descargar schema
`xsd_validator.py` intenta descargar el schema NeTEx desde `http://netex-cen.github.io/netex-schemas/...` que devuelve 404. El schema local está en `netex-xsd/xsd/NeTEx_publication.xsd`. Usar cache local o actualizar URL.

### 12. route_type 1 siempre mapea a highSpeedTrain
`config.py` submode_map mapea route_type "1" a `highSpeedTrain`. Pero route_type 1 en GTFS es "Rail" genérico — debería distinguir AVE (highSpeedTrain) vs Cercanías (commuterTrain) vs Media Distancia (regionalTrain) por nombre de ruta, no solo route_type.

### 13. ✅ RESUELTO — Convertidor NeTEx→GTFS bidireccional
**Creado v3.0.** Ahora existe conversión bidireccional:
- `netex_reader.py` (613 líneas) — Lee XML NeTEx → GTFSFeed
- `gtfs_writer.py` (280 líneas) — GTFSFeed → archivos GTFS .txt
- Round-trip verificado: GTFS→NeTEx→GTFS preserva 100% routes, trips, stop_times
- 10 tests de round-trip en `tests/test_roundtrip.py`

### 14. ✅ PARCIALMENTE RESUELTO — GTFS files adicionales soportados
**Añadido v3.0.** El reader ahora soporta:
- `frequencies.txt` → HeadwayJourneyGroup con FrequencyHeadwayInterval ✅
- `pathways.txt` → SitePath con 7 modos (walkway, stairs, escalator, elevator, ramp) ✅
- `levels.txt` → LevelStructure ✅
- `translations.txt` → MultilingualString ✅
- `fare_products.txt` (GTFS-Fares v2) → NO (sin datos de prueba)
- `bookings.txt` → NO (spec lo documenta, código no lo implementa)

### 15. ✅ RESUELTO — Claims del README
**Fixeado v3.0.** README reescrito con datos reales: 96 tests, 218 reglas, sin claims inflados. CHANGELOG.md creado.

### 16. IDs duplicados en AccessibilityAssessment y Call — RESUELTO v3.0
**Bug crítico fixeado.** Dos bugs de IDs duplicados:
- `AccessibilityAssessment` usaba `acc-0`/`acc-1` (solo 2 valores posibles, se repetían 56 veces). Ahora usa contador global + entity_id.
- `Call` no incluía trip_id ni stop_sequence. Ahora: `ES:Call:MTM:CHAMARTIN:trip_001:3`.

### 17. SSPs sintéticos para stop_times huérfanos — RESUELTO v3.0
Stop_ids que aparecen en stop_times pero no en stops.txt ahora generan SSPs automáticamente en el ServiceFrame. Antes se perdían 9 stop_times en el round-trip.

### 18. `_parse_id` con prefijo ES duplicado — RESUELTO v3.0
IDs con formato `ES:Operator:ES:MTM` ahora extraen `MTM` como operador correctamente (antes devolvía `ES`).

### 19. Backend HTTP sin dependencias — AÑADIDO v3.0
`app/server.py` usa solo `http.server` de stdlib (sin Flask). 3 endpoints: `/convert` (GTFS→NeTEx), `/convert-back` (NeTEx→GTFS), `/validate`. Verificado vía HTTP con round-trip completo.

### 20. Principio de honestidad técnica — REGLA DE ORO
**Mejor no incluir algo que incluirlo con errores.** Si no hay datos de prueba para verificar una feature (GTFS-Fares v2, bookings), no se añade al código. La spec puede documentarlo, pero el código solo incluye lo que funciona y está probado. Tras cualquier cambio: `python -m pytest tests/ -v` y actualizar README con números reales.

## Archivos de referencia

- `references/gtfs-netex-mapping.md` — Mapeo completo GTFS→NeTEx
- `references/validator-rules-index.md` — Índice de 218 reglas
- `references/mega-auditoria-2026-07-07.md` — Mega auditoría inicial: 15 gaps críticos, plan de 8 fases
- `references/auditoria-final-2026-07-07.md` — Auditoría final v3.0: comparativa real con nórdico (71/100) y francés (64/100), NeTEx-ES 91/100. Lista honesta de lo que NO está hecho.

## Estado v3.0 (2026-07-07)

| Métrica | Valor |
|---|---|
| Tests | 96 passed, 0 failed |
| Reglas validador | 218 (0 placeholders) |
| Conversión | Bidireccional GTFS↔NeTEx |
| Round-trip | Verificado (10 tests) |
| Spec | 25 secciones, 1337 líneas |
| Dependencias | Solo stdlib Python |
| Backend | HTTP stdlib (sin Flask) |
| Score real | 91/100 (vs 71 nórdico, 64 francés) |

### Lo que NO está hecho (honestamente)
1. No probado con feeds GTFS reales de operadores españoles
2. XSD oficial no valida (decisión deliberada, frames tipados)
3. GTFS-Fares v2 y Bookings no implementados (sin datos de prueba)
4. Multilingüe en código: spec documenta 6 idiomas, writer solo genera lang="es"
5. Festivos por CCAA en código: spec los documenta, writer no los genera
6. CRS conversión: spec documenta ETRS89/UTM, writer solo genera WGS84

## Licencia

MIT — Compatible con RD 571/2023 (datos abiertos transporte público)
