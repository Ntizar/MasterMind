---
name: transit-data-pipelines
description: "Construir pipelines de datos de transporte público: conversión GTFS↔NeTEx, validación XSD, apps web generadoras, y mapeo de entidades. Soporte para EN 12896, RD 571/2023, NAP. Incluye generador web drag&drop para empresas sin conocimiento técnico."
version: "2.1.0"
tags: [transit, gtfs, netex, transport, esios, mobility, data-pipeline]
created: "2026-07-07"
---

# Transit Data Pipelines

Construir pipelines de datos de transporte público: conversión GTFS↔NeTEx, validación XSD, apps web generadoras, y mapeo de entidades.

## Cuándo usar

- El usuario habla de convertir GTFS a otro formato (NeTEx, SIRI, SIRI-SV)
- Necesita generar datos de transporte público para consorcios o empresas
- Quiere crear un generador/webapp para que no técnicos exporten datos de transporte
- Necesita validar schemas XML de transporte (NeTEx XSD, GTFS)
- Trabajando con datos de transporte público español (RD 571/2023, NAP)

## Componentes principales

### 1. GTFS Reader

```python
from converter.gtfs_reader import GTFSReader
reader = GTFSReader("ruta/a/feed.zip")  # .zip o directorio
feed = reader.read()
# feed.stops, feed.routes, feed.trips, feed.stop_times,
# feed.calendars, feed.shapes, feed.transfers_raw, feed.agencies
```

El reader acepta `.zip` o directorio con archivos `.txt`. Parsea todas las tablas GTFS estándar.

### 2. NeTEx Writer

```python
from converter.netex_writer import NeTExWriter
writer = NeTExWriter(feed, config)
xml_str = writer.to_string(pretty=True)
```

Genera XML NeTEx-ES conforme al XSD oficial NeTEx-CEN 1.14 con estructura de frames tipados:
- Función `_frame_base(frame_tag, frame_id, description)` crea la base XSD (grupos 1-3: EntityInVersionGroup → DataManagedObjectGroup → VersionFrameGroup) para todos los frames
- `PublicationDelivery` → `<dataObjects><CompositeFrame><frames>...</frames></CompositeFrame></dataObjects>`
- `ParticipantRef` → texto directo (no `_ref()`)
- `ResourceFrame`: `codespaces` → `Codespace` (solo `Xmlns`, `Description`), `organisations` → `Operator` con `PublicCode`
- `SiteFrame`: StopPlaces → StopPlaceElements → Quays
- `ServiceFrame`: Lines, Routes, ScheduledStopPoints (con QuayRef), JourneyPatterns
- `ServiceCalendarFrame`: DayTypes (con PropertyOfDay), DayTypeAssignments, OperatingPeriods
- `TimetableFrame`: VehicleJourneys con calls (Arrival/Departure)
- `FareFrame`: FareZones, FareProducts, Tariffs (con FareStructureElement + FareTable), SalesOfferPackages
- LineGeometries (shapes.txt), Connection (transfers.txt), AdministrativeAreas
- Sin `<dataObjects>` duplicado, sin `<Type>`, sin `FrameDefaults`, sin `PassengerStoppingArea`

Ver `references/netex-es-project.md` para estructura completa. La conformidad XSD se logra usando `_frame_base()` para todos los frames, `codespaces` (plural) para Codespace, `organisations` en vez de `operators`, y `PublicCode` en vez de `OperatorCode`. Ver sección "XSD Conformity" más abajo para reglas detalladas.

### 3. Configuración

```python
from converter.config import Config
config = Config(
    publisher_name="Mi Empresa",
    frame_id_prefix="ES",
    include_geography=True,
    include_fares=True,
    include_transfers=True,
    include_shapes=True,
    include_wheelchair=True,
    validate_output=True,
    pretty_print=True,
)
```

### 4. Validación XSD

```python
from converter.xsd_validator import validate_xml
is_valid, msg = validate_xml(xml_str)
```

3 niveles de validación:
1. XML bien formado
2. Namespace NeTEx correcto (`http://www.netex.org.uk/netex`)
3. Validación contra schema NeTEx 1.14 (cacheado en `spec/schema_cache/`)

### 5. Mapeo de modos de transporte

El config tiene 25+ mapeos de `route_type` (GTFS) a `LineType` (NeTEx):

| GTFS route_type | NeTEx LineType |
|---|---|
| 0 | metro |
| 1 | rail |
| 2 | bus |
| 3 | ferry |
| 4, 5 | cableCar |
| 6 | funicular |
| 7 | tram |
| 9-11 | passengerFerry |
| 12 | expressBus |
| 13 | nightBus |
| 14 | commuterTrain |
| 16 | monorail |
| Y más... | Y más... |

### 6. Aplicación Web para empresas

Generar una web profesional para que no técnicos exporten NeTEx:

**Estructura:**
```
app/
  index.html   # Frontend vanilla (HTML/CSS/JS)
server.py      # Backend Python (sin dependencias externas)
```

**Frontend pattern (4 pasos):**
1. **Datos del operador** — Formulario con nombre, código, sitio web
2. **Subir GTFS** — Drag & drop con preview de archivo
3. **Opciones** — Checkboxes para features (geografía, tarifas, transbordes...)
4. **Generar** — POST al backend con datos del zip → XML + stats

**Backend pattern:**
```python
from http.server import HTTPServer, SimpleHTTPRequestHandler

class NeTExHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/convert':
            data = json.loads(body)
            gtfs_bytes = bytes(data['gtfsData'])
            # Extract to temp zip → GTFSReader → NeTExWriter → response
```

**Deploy:**
```bash
python server.py              # localhost:8080
python server.py 9090         # custom port
```

## Entidades NeTEx mapeadas

| GTFS | NeTEx |
|---|---|
| stops.txt | StopPlaces → StopPoints → Quays |
| routes.txt | Lines → Routes |
| trips.txt | VehicleJourneys |
| stop_times.txt | calls (dentro de VJ) |
| calendar.txt | ServiceFrames + DayTypes |
| calendar_dates.txt | DatePeriods |
| fare_attributes.txt | FareStructure |
| fare_rules.txt | FareElement |
| shapes.txt | LineGeometry |
| transfers.txt | Connection |
| agency.txt | PublisherRef |
| — | AdministrativeAreas |
| — | GroupsOfLines |

## Reglas específicas de España

- **Horario:** Europe/Madrid (UTC+1/UTC+2, CET/CEST)
- **Nombres:** idioma español (`lang="es"`)
- **Referencias:** códigos INE, UN/LOCODE
- **Coordenadas:** EPSG:4326 (WGS84)
- **Codificación:** UTF-8
- **Normativa:** RD 571/2023, Reglamento (UE) 2017/1926 (NAP)
- **Formato IDs:** `ES:{Tipo}:{Operador}:{Secuencia}` (ej: `ES:StopPlace:MTM:28079:001`)
- **Codespace** declarado en ResourceFrame con `CodespaceId="ES"`

## XSD Conformity — Generar XML válido contra NeTEx-CEN XSD

**El XML generado SÍ puede pasar validación XSD oficial.** No hay que renunciar a la conformidad XSD.

### Patrón universal de frames (todos los frames)

Todos los frames del XSD NeTEx-CEN 1.14 siguen la misma estructura de 4 grupos secuenciales:

```
<FrameType id="..." version="1">
  <!-- Grupo 1: EntityInVersionGroup (minOccurs=0, opcional) -->
  <!-- Grupo 2: DataManagedObjectGroup (obligatorio por restricción XSD) -->
  <Extensions/>  <!-- placeholder: no requiere hijos, satisface la restricción -->
  <!-- Grupo 3: VersionFrameGroup -->
  <Description>...</Description>
  <!-- elementos específicos del grupo 3 -->
  <!-- Grupo 4: FrameGroup específico -->
  <!-- elementos específicos del frame -->
</FrameType>
```

**Función helper `_frame_base(frame_tag, frame_id, description)`** crea la base común (grupos 1-3) para todos los frames.

### Reglas XSD críticas descubiertas (2026-07-07)

- **PublicationDelivery**: debe contener `<dataObjects><CompositeFrame><frames>...</frames></CompositeFrame></dataObjects>` (no frame directo)
- **ParticipantRef**: texto directo `<ParticipantRef>publisher</ParticipantRef>`, NO `_ref()` con atributos `ref`/`version`. El tipo es `siri:ParticipantCodeType` (simpleType).
- **Codespace**: solo acepta `Xmlns`, `XmlnsUrl`, `Description` (extiende `EntityStructure` → solo `id` como atributo). **NO** acepta `version`, `validBetween`, `CodespaceId`, `preferredLanguage`.
- **Codespaces** (plural): elemento contenedor dentro de `VersionFrameGroup`, no `Codespace` directo.
- **ResourceFrame**: usa `<organisations>` (no `<operators>`). `OrganisationInFrameGroup` contiene `organisations`, `contacts`, `groupsOfOperators`, `operationalContexts`.
- **Operator**: dentro de `OrganisationGroup`, usa `OrganisationCodeGroup` → `PublicCode` (simpleContent con texto + atributo `type`), NO `OperatorCode` (no existe). Luego `OrganisationNameGroup` → `Name`.
- **Extension de frames**: `ResourceFrame extends ResourceFrame_VersionFrameStructure` que a su vez extiende `Common_VersionFrameStructure`. La restricción XSD usa `xsd:sequence` con 4 sub-secuencias (grupos). El orden es estricto.
- **DataManagedObjectGroup** es obligatorio en la restricción de ResourceFrame (sin `minOccurs=0`). Usar `<Extensions/>` vacío como placeholder seguro.
- **`<Type>` y `<FrameDefaults>`**: no existen en la estructura oficial. Eliminar de CompositeFrame.

### Verificación de XSD

```bash
# Clonar XSD oficial
git clone --depth 1 https://github.com/NeTEx-CEN/NeTEx.git netex-xsd
# Validar
pip install xmlschema
python -c "
import xmlschema
schema = xmlschema.XMLSchema('netex-xsd/xsd/NeTEx_publication_timetable.xsd')
schema.validate('output.xml')  # raises XMLSchemaValidationError si falla
"
```

### Pitfalls XSD

- **Elementos con nombres incorrectos**: `operators` → `organisations`, `OperatorCode` → `PublicCode`, `CodespaceId` → no existe, `validBetween` en Codespace → no existe.
- **Atributos incorrectos**: `Codespace` no acepta `version`, `PublicCode` es simpleContent (solo texto + `type`), `ParticipantRef` es texto directo.
- **Orden de grupos**: los 4 grupos XSD son secuenciales y estrictos. No se pueden mezclar.
- **Schema 404**: El XSD oficial de NeTEx-CEN puede dar 404 si se descarga por URL. Clonar el repo directamente.

### Pitfall: GTFSFeed `__post_init__` índice vacío (BUG CLÁSICO)

`GTFSFeed` es un `dataclass` con `__post_init__` que llama a `_build_indices()` — construye los hash `_stop_by_id`, `_route_by_id`, `_trip_by_id` a partir de listas vacías (el feed aún no se ha leído). Después de `reader.read()`, los datos se añenden a las listas PERO los índices hash no se reconstruyen. Resultado: `feed.get_stop(id)` retorna `None` SIEMPRE.

**Diagnóstico:** Si después de `reader.read()` los métodos `get_stop()`, `get_route()`, `get_trip()` retornan `None` para IDs que sí existen en `feed.stops`, es este bug.

**Fix:** Llamar `feed.rebuild_indices()` al final de `GTFSReader.read()`. El método `rebuild_indices()` existe y solo llama a `_build_indices()` para reconstruir todos los hash.

```python
# En GTFSReader.read(), al final del try:
self.feed = feed
feed.rebuild_indices()  # RECONSTRUIR DESPUÉS DE LEER
return feed
```

**Prevenir:** Cualquier dataclass con `__post_init__` que construya índices/estructuras a partir de campos que se populan después (ej: `_by_id` dicts a partir de listas) necesita un `rebuild_indices()` o equivalente que se llame explícitamente tras la lectura.