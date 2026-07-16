# Pipeline Ouigo: 0 errores + 0 warnings (15 Jul 2026)

## Logro
Validador español pasa con **0 errores y 0 warnings** usando datos reales de Ouigo (457KB XML, 68 viajes, 68 ServiceJourney, 8 rutas, 13 paradas).

## Arreglos clave en el generador (gtfs-to-netex-es)

### service_frame.py (writers/)
- **TransportSubmode añadido** a cada Line (`submode_map` basado en route_type: 101→highSpeedTrain, 102→interregionalTrain, etc.)
- **NetworkRef añadido** a cada Line (referencia a Network por defecto)
- **version="1"** añadido a PointOnRoute, direction, TimingPointInJourneyPattern
- **accessibility_elem** ahora recibe `writer._make_id` (callable), no un string

### helpers.py
- **accessibility_elem()** ya no retorna `None` cuando `wheelchair_boarding` es `None`. Siempre genera `AccessibilityAssessment` con `MobilityImpairedAccess` y valor "unknown" como fallback.
- **Firma:** `(wheelchair, make_id)` donde `make_id` es `writer._make_id`

### fare_frame.py (writers/)
- **Bug corregido:** `fm.sales_offer_package_id` → `fm.fare_media_id` (FareMedium no tiene `sales_offer_package_id`)
- **Bug corregido:** `fm.fare_media_type or "other"` → `str(fm.fare_media_type) if fm.fare_media_type is not None else "other"` (int→string explícito)

### netex_writer.py
- **availabilityCondition** añadido al CompositeFrame (COMPOSITE_FRAME_6)
- **validityConditions** añadido como wrapper de ValidBetween (COMPOSITE_FRAME_1/3)
- **CompanyNumber, LegalName, ContactDetails** añadidos al Operator (OPERATOR_1/3/4)

### site_frame.py (writers/)
- **accessibility_elem** recibe `writer._make_id` para IDs válidos (ES:ACCESSIBILITY_ASSESSMENT:3780:...)
- Eliminado el `if acc is not None:` (ahora siempre hay elemento)

### timetable_frame.py (writers/)
- **validityConditions** añadido al TimetableFrame (VALIDITY_CONDITIONS_IN_LINE_FILE_4)

## Arreglos clave en el validador (netex-es-validator)

### semantic_validator.py (validator/)
Todas las correcciones son bugs de **case-sensitivity** en la búsqueda de elementos con `find()`:

| Regla | Antes (roto) | Después (correcto) |
|-------|-------------|-------------------|
| LINE_4 | `transportMode` | `TransportMode` |
| ROUTE_4 | `routeElements` | `pointsInSequence` |
| SERVICE_JOURNEY_12 | `operatorRef` | `OperatorRef` |
| LINE_5 | `transportSubMode` | `TransportSubmode` |
| LINE_7 | `networkRef` | `NetworkRef` |
| OPERATOR_4 | `contactDetails` | `ContactDetails` |
| COMPOSITE_FRAME_3 | `validBetween` (directo) | busca en `validityConditions` → `ValidBetween` |
| SERVICE_JOURNEY_15 | `netex:ArrivalTime` | `n:ArrivalTime` (prefijo real del parser) |
| SERVICE_JOURNEY_13 | solo `dates`/`serviceCalendarRef` | también acepta `dayTypes` |
| VALID_SUBMODES["rail"] | faltaba `interregionalTrain` | añadido al set |

### validator_runner.py
| Regla | Antes | Después |
|-------|-------|---------|
| XPATH_1 | `./*[not(self::netex:PublicationDelivery)]` | `/*[not(self::netex:PublicationDelivery)]` |

## Lecciones aprendidas

1. **PascalCase es ley** — El validador español busca TODOS los elementos con nombres PascalCase (`TransportMode`, `OperatorRef`, `ValidBetween`, etc.). Cualquier variación (camelCase, minúscula inicial) genera falsos positivos. Esta es la fuente del 80% de los bugs.

2. **`validityConditions` es wrapper** — `ValidBetween` no va directamente bajo `CompositeFrame`, va dentro de `<validityConditions>`.

3. **Namespace `n:` vs `netex:`** — El parser lxml usa `n:` como prefijo cuando el namespace es default (`xmlns=...`). El validador busca con `self.NS = {'netex': '...'}`, pero el prefijo real en el XML parseado puede ser `n:`.

4. **Siempre generar elementos incluso sin datos** — `accessibility_elem()` siempre debe generar un elemento con valor "unknown" en lugar de retornar None. Evita 16 warnings.

5. **version attribute en todos los elementos con id** — Si un elemento tiene `id`, debe tener `version="1"`. Elimina cientos de warnings NETEX_ID_8.

6. **El patch tool pierde indentación** — Los parches multilínea eliminan la indentación de la primera línea. Verificar siempre con `read_file` después.

## Comando de validación final
```bash
# Generar XML
python3 -c "
from converter.gtfs_reader import GTFSReader
from converter.netex_writer import NeTExWriter
from converter.config import Config
reader = GTFSReader('/root/workspace/netex-es/gtfs-sample/ouigo')
feed = reader.read()
writer = NeTExWriter(feed, Config(publisher_name='OuigoEspana', frame_id_prefix='ES', version='1.0'))
with open('/tmp/ouigo_output.xml', 'w') as f:
    f.write(writer.to_string(pretty=True))
print('OK')
"

# Validar
pip3 install -e /root/workspace/netex-es/tools/netex-es-validator --quiet
netex-es-validator /tmp/ouigo_output.xml --verbose
```