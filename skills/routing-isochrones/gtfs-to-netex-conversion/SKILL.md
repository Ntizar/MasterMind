---
name: gtfs-to-netex-conversion
version: "2.0.0"
description: Pipeline para convertir GTFS a NeTEx con adaptación española (NeTEx-ES), incluyendo jerarquía de paradas, tarifas zonales, modos de transporte y sistema de IDs.
---

# GTFS → NeTEx Conversion Pipeline

## Qué es

Pipeline para convertir datos de transporte público del formato **GTFS** (General Transit Feed Specification) al formato europeo **NeTEx** (Network Timetable Exchange, CEN/TS 16614), con adaptaciones específicas para España (NeTEx-ES).

## Cuándo usar

- El usuario necesita convertir feeds GTFS a NeTEx
- Se requiere migración de datos de transporte público a estándar europeo
- Se necesita interoperabilidad NAP (National Access Point)
- Se requiere soporte de tarifas zonales, jerarquía de paradas, accesibilidad completa

## Estructura del proyecto

```
netex/
├── spec/
│   └── NeTEx-ES.md          # Especificación completa NeTEx-ES (referencia)
├── converter/
│   ├── __init__.py
│   ├── __main__.py          # Entry point: python -m converter
│   ├── config.py            # Configuración + mapeo de transportes
│   ├── gtfs_reader.py       # Lector GTFS (.zip o directorio)
│   ├── netex_writer.py      # Generador XML NeTEx
│   └── cli.py               # CLI: python -m converter.cli input.zip -o output.xml
├── gtfs-sample/             # Datos de ejemplo Metro de Madrid
├── tests/
│   ├── test_gtfs_reader.py  # 19 tests
│   └── test_netex_writer.py # 20 tests
├── README.md
└── requirements.txt
```

## Pasos de conversión

1. **Leer GTFS** — zip o directorio con archivos .txt
2. **Extraer metadatos** — agency/feed_info → PublisherRef
3. **Crear jerarquía de paradas** — StopPlace (location_type=1) con Quays y StopPoints (location_type=0)
4. **Crear líneas y rutas** — Cada route GTFS → 1 Line + 2 Routes (ida/vuelta) con transportMode/submode correcto
5. **Crear journey patterns** — Agrupar trips por (route_id, direction_id)
6. **Crear vehicle journeys** — Cada trip → VehicleJourney con calls desde stop_times
7. **Crear calendarios** — calendar.txt → ServiceFrames + DayTypes
8. **Crear tarifas** — Si hay zone_id → FareZones + FareStructures
9. **Crear conexiones** — transfers.txt → Connection intermodal
10. **Validar y generar XML** — Con namespace NeTEx correcto y XSD location

## Mapeo de entidades GTFS → NeTEx

| GTFS | NeTEx-ES | Notas |
|---|---|---|
| `stops.txt` | `StopPlaces` + `Quays` + `StopPoints` | location_type=1→StopPlace, =0→StopPoint dentro de Quay |
| `routes.txt` | `Lines` + `Routes` | Separación línea/ruta + transportMode/submode |
| `trips.txt` | `VehicleJourneys` | Cada trip → VJ con JourneyPattern |
| `stop_times.txt` | `calls` | Dentro de VJ, orden por stop_sequence |
| `calendar.txt` | `ServiceFrames` + `DayTypes` | Calendario semanal |
| `calendar_dates.txt` | `DatePeriod` | Fechas especiales |
| `fare_attributes.txt` | `FareStructure` | Estructura tarifaria |
| `fare_rules.txt` | `FareElement` | Reglas por zona |
| `shapes.txt` | `LineGeometry` | Polilíneas de ruta |
| `transfers.txt` | `connections` | Transbordo intermodal |
| `agency.txt` | `PublisherRef` | Editor de datos |

## Mapeo de modos de transporte (GTFS route_type → NeTEx)

| GTFS type | NeTEx LineType | NeTEx SubMode | Español |
|---|---|---|---|
| 0 | `metro` | `metro` | Metro urbano |
| 1 | `rail` | `commuterTrain` / `highSpeedTrain` | Cercanías / AVE |
| 2 | `bus` | `bus` | Autobús urbano |
| 3 | `ferry` | `highSpeedVessel` | Transbordador |
| 4,5 | `cableCar` | `aerialLift` | Teleférico |
| 6 | `funicular` | `funicular` | Funicular |
| 7 | `tram` | `tram` | Tranvía |
| 12 | `bus` | `expressBus` | Bus expreso |
| 13 | `bus` | `nightBus` | Bus nocturno |

## Sistema de IDs NeTEx-ES

Formato: `ES:{TipoEntidad}:{Operador}:{Secuencia}`

- `ES:StopPlace:MTM:28079:001` — Parada de Metro de Madrid
- `ES:Quay:MTM:28079:001:Q01` — Andén 1
- `ES:StopPoint:MTM:28079:001:Q01` — Punto de parada
- `ES:Line:MTM:M1` — Línea M-1
- `ES:VJ:MTM:M1:N:001` — Viaje 001 sentido N

## Uso del convertidor

### Línea de comandos
```bash
# Conversión básica
python -m converter.cli gtfs_ejemplo.zip -o salida.xml

# Con options
python -m converter.cli gtfs_ejemplo.zip -o salida.xml --no-geography
python -m converter.cli gtfs_ejemplo.zip -o salida.xml --no-fares

# Con nombre de publisher
python -m converter.cli gtfs.zip -o salida.xml -n "CRTM"
```

### API Python
```python
from converter.config import Config
from converter.gtfs_reader import GTFSReader
from converter.netex_writer import NeTExWriter

config = Config(
    publisher_name="CRTM",
    include_geography=True,
    include_fares=True,
)

reader = GTFSReader("gtfs_madrid.zip")
feed = reader.read()

writer = NeTExWriter(feed, config)
writer.to_file("madrid_netex.xml")
```

## Reglas de validación NeTEx-ES

### Obligatorias
1. IDs formato `ES:{Tipo}:{CodigoFuente}:{Secuencia}`
2. Horarios `HH:MM:SS` (UTC+1/UTC+2 asumed)
3. Fechas ISO 8601 `YYYY-MM-DD`
4. Coordenadas EPSG:4326 (WGS84)
5. Idioma español (`lang="es"`)
6. UTF-8
7. Versión NeTEx ≥ 1.14

### Recomendadas
1. Distancia máx. entre paradas: 2 km (urbano), 50 km (interurbano)
2. Intervalo máx. entre servicios: 120 min
3. Servicio activo 04:00-02:00
4. Accesibilidad declarada siempre
5. Coherencia dirección (headsign ↔ directionName)

## Consideraciones específicas para España

1. **Códigos INE** — Usar código INE del municipio como parte del ID de StopPlace
2. **Zonas tarifarias** — Mapear `zone_id` GTFS a `FareZone` NeTEx (consorcios CRTM, TMBAR)
3. **Festivos** — Nacionales + autonómicos en DayTypes
4. **Horarios** — Hora local española (CET/CEST)
5. **Accesibilidad** — Obligatoria por ley europea
6. **Operadores múltiples** — Un feed puede contener MTM + RENFE + EMT

## Pitfalls

- **Config line_type_map**: Nunca usar el mapa antiguo donde TODO mapea a "bus" — siempre usar `config.py` actualizado
- **Namespace XML**: El writer usa `_post_process_xml()` para corregir namespaces; no confiar en el output directo de ET.tostring()
- **Jerarquía de paradas**: `location_type=1` = estación (StopPlace) con hijos, `location_type=0` = parada simple (StopPoint dentro de Quay)
- **Zonas tarifarias**: Solo se generan si el GTFS tiene `zone_id` en stops.txt
- **Schema location**: Usar `neTEx_publication.xsd` no `neTEx_local.xsd`
- **Test failures**: Los tests de netex_writer.py pueden dar warnings de Pyright por `pytest` no reconocido — es falso positivo, no afecta ejecución

## Referencias

- [CEN/TS 16614-1:2014] NeTEx Parte 1: Network Topology
- [EN 12896:2016] Transmodel: Modelo conceptual europeo
- [eu.data.public-transport.earth](https://eu.data.public-transport.earth/) — Portal comunitario de feeds
- [Spec completa](references/netex-es-spec.md) — Detalle de la especificación NeTEx-ES
