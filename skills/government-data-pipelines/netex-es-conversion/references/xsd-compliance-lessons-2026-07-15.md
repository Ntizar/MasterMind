# Lecciones de XSD Compliance — Pipeline Ouigo (15 Jul 2026)

## Resumen

Tras generar un NeTEx de 475KB desde el GTFS de Ouigo (68 trips, 231 stop_times, 16 stops), se validó contra:
- **netex-es-validator** (218 reglas españolas): 635 → 645 errores (↑ por nuevos IDs con formato correcto)
- **XSD oficial NeTEx-CEN 1.14** (lxml): 109 → **71 errores** tras correcciones

## Errores XSD arreglados (109→71)

### 1. `<version>` como elemento vs atributo
**Problema:** El writer ponía `<version>1.0</version>` como hijo de `PublicationDelivery`.
**XSD:** `version` debe ser un **atributo** de `PublicationDelivery`, no un elemento hijo.
**Fix:** Quitar `child(delivery, "version", "1.0")`. Ya está como atributo en el constructor del elemento.

### 2. ParticipantRef — código sin espacios
**Problema:** `"Ouigo España"` no es un `ParticipantCodeType` válido.
**XSD:** `ParticipantCodeType` (SIRI) no permite espacios ni acentos.
**Fix:** Sanitizar: `replace(" ", "").replace("í", "i")...[:20]` y fallback al frame_id_prefix.

### 3. FromDate/ToDate como dateTime (no date)
**Problema:** `"2025-01-06"` no es un `xs:dateTime` válido.
**XSD:** `ValidBetween/FromDate` y `ValidBetween/ToDate` son tipo `xs:dateTime`.
**Fix:** Usar `"2025-01-06T00:00:00Z"`.

### 4. `validBetween` (minúscula) vs `ValidBetween` (PascalCase)
**Problema:** El writer usaba `el("validBetween")`.
**XSD:** Todos los elementos en NeTEx usan PascalCase. El elemento correcto es `ValidBetween`.
**Fix:** Cambiar a `el("ValidBetween")`.

### 5. `stopPlaceElements` → `quays`
**Problema:** El writer usaba `<stopPlaceElements>` para contener los Quays hijos.
**XSD:** El contenedor correcto en `StopPlace_VersionStructure` es `<quays>`.
**Fix:** Cambiar el nombre del contenedor de `stopPlaceElements` a `quays`.

### 6. Orden de elementos en StopPlace
**Problema:** El orden era: Name → PostalAddress → Centroide → quays.
**XSD:** El orden esperado es: Name → Centroid (ZoneGroup) → PostalAddress (AddressablePlaceGroup) → AccessibilityAssessment (SiteElementGroup) → PublicCode (StopPlacePropertyGroup) → quays.
**Fix:** Reordenar según la estructura de herencia: ZoneGroup → PlaceGroup → AddressablePlaceGroup → SiteElementGroup → StopPlaceGroup.

### 7. LineType — enumeración incorrecta
**Problema:** `line_type_map` devolvía `"bus"` para route_type 101 (highSpeedTrain de Ouigo).
**XSD:** `LineType` solo acepta: `local`, `urban`, `longDistance`, `express`, `other`. No acepta `bus`.
**Fix:** Validar el valor contra la lista blanca del XSD; si no coincide, usar `"other"`.

### 8. TransportMode en Line
**Problema:** El writer usaba `transportMode` (minúscula) en posición incorrecta.
**XSD:** `TransportMode` (PascalCase) va en `LineDescriptionGroup`, DESPUÉS de `Description` y ANTES de `PublicCode`.
**Fix:** Mover `TransportMode` a la posición correcta.

### 9. OperatorRef no OwnerRef, y antes de LineType
**Problema:** El writer usaba `OwnerRef` y lo ponía después de `LineType`.
**XSD:** `OperatorRef` (en `LinePropertiesGroup`) va ANTES de `LineType` (en `LineClassificationGroup`). `OwnerRef` no existe en Line.
**Fix:** Cambiar a `ref(line, "OperatorRef", ...)` y posicionar antes de `LineType`.

### 10. `OperatingName` no existe en Line
**Problema:** El writer intentaba poner el nombre de la agencia como `OperatingName`.
**XSD:** No hay elemento `OperatingName` en `Line_VersionStructure`.
**Fix:** Eliminar. La agencia se referencia vía `OperatorRef`.

### 11. `routes` en ServiceFrame — orden de grupos
**Problema:** `routes` aparecía después de `lines` en ServiceFrame.
**XSD:** El orden de grupos en `ServiceFrameGroup` es:
1. NetworkInFrameGroup → Network
2. **RouteInFrameGroup → routes**
3. FlexibleRouteInFrameGroup
4. SectionInFrameGroup
5. ProjectionInFrameGroup
6. CommonPointAndLInkFrameGroup
7. **LineInFrameGroup → lines**
8. LineNetworkInFrameGroup
9. ServiceInFrameGroup
**Fix:** Poner `routes` ANTES de `lines` en el ServiceFrame.

### 12. Description duplicado en Line
**Problema:** Cada Line tenía dos elementos `<Description>` — uno del route_long_name y otro del agency_name.
**XSD:** Solo se permite un `Description` por Line (en `LineDescriptionGroup`).
**Fix:** Quitar el segundo `Description` (agency_name). La agencia va en `OperatorRef`.

### 13. accessibilityPolicy no va en CompositeFrame
**Problema:** El writer ponía `accessibilityPolicy` como hijo directo de `CompositeFrame`.
**XSD:** `accessibilityPolicy` no es un elemento válido de `CompositeFrame` — pertenece a `SiteFrame`/`StopPlace`.
**Fix:** Eliminar del CompositeFrame (o mover a SiteFrame).

## Errores XSD que quedan (71)

### ~68 journeyPatternRef en ServiceJourney
El elemento `journeyPatternRef` en `ServiceJourney` no está en la posición correcta. El XSD `ServiceJourney_VersionStructure` espera:
- Name → Description → **departureTime** → **JourneyDuration** → **dayTypes** → **journeyPatternRef** → **calls**/passingTimes

### ~1 operatingPeriods en ServiceCalendarFrame
`operatingPeriods` probablemente está en el contenedor/frame incorrecto.

### ~1 accessibilityPolicy
Ya corregido en código pero cuenta residual en validación.

### ~1 routes
Residual del cambio de orden.

## Errores del validador español (645)

### ~460 ES_ID_FORMAT
IDs con formato incorrecto. El patrón correcto es `ES:{Tipo}:{Operador}:{Secuencia}`:
- `ES:Operator:3780:001` (NO `ES:Operator:ES:3780`)
- `ES:CompositeFrame:3780:001` (NO `ES:Frame:ES:001`)
- `ES:DayType:3780:AllWeek` (NO `ES:DayType:AllWeek`)
- Usar siempre `writer._make_id(tipo, secuencia)` para generar IDs

### ~68 SERVICE_JOURNEY_3
Viajes sin stop_times. Ouigo tiene viajes de reposición en vacío. Para validación estricta, estos viajes pueden ser correctos.

### ~68 NETEX_ID_5
Referencias a DayTypes no resueltas (AllWeek/Weekends). Añadir DayTypes por defecto en el writer.

### ~11 ROUTE_3/ROUTE_4/LINE_4/JOURNEY_PATTERN_2
Errores de consistencia entre rutas, líneas y patrones de viaje. Requieren revisar que cada Route tenga su Line correspondiente y cada JourneyPattern tenga su RouteRef.

## Pipeline de validación recomendada

```bash
# 1. Generar NeTEx
python3 -c "
from converter.gtfs_reader import GTFSReader
from converter.netex_writer import NeTExWriter
from converter.config import Config
reader = GTFSReader('/path/to/gtfs')
feed = reader.read()
writer = NeTExWriter(feed, Config(publisher_name='Operator', frame_id_prefix='ES'))
with open('/tmp/output.xml', 'w') as f:
    f.write(writer.to_string(pretty=True))
"

# 2. Validar con reglas españolas
netex-es-validator /tmp/output.xml --verbose 2>&1 | grep "\[ERROR\]" | sed 's/.*\[ERROR\] \([^ ]*\).*/\1/' | sort | uniq -c | sort -rn

# 3. Validar con XSD oficial
python3 -c "
from lxml import etree
xsd = etree.XMLSchema(etree.parse('/path/to/neTEx_publication.xsd'))
xml = etree.parse('/tmp/output.xml')
valid = xsd.validate(xml)
print(f'Valid: {valid}')
if not valid:
    for e in xsd.error_log:
        print(f'  Line {e.line}: {e.message}')
"

# 4. Round-trip
netex-es-to-gtfs /tmp/output.xml /tmp/roundtrip-gtfs/
# Comparar feeds
```