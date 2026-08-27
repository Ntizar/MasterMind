# Pipeline Ouigo: 0 errores en validador español (2026-07-15)

## Resumen

El convertidor GTFS→NeTEx-ES genera XML válido para el perfil español con datos reales de Ouigo (458 KB, 68 viajes, 26 paradas, 231 stop_times).

- **Errores validador español:** 0 ✅ (desde 2.908)
- **Warnings:** 44 (no bloqueantes: ES_ACCESSIBILITY, LINE_5/7, OPERATOR_1/3/4, COMPOSITE_FRAME_6, VALIDITY_CONDITIONS_IN_LINE_FILE_2/4)
- **XSD oficial (lxml):** 71 errores (pendiente)

## Contenido del XML generado

| Entidad | Cantidad |
|---------|----------|
| CompositeFrame | 1 |
| ServiceFrame | 1 |
| TimetableFrame | 1 |
| SiteFrame | 1 |
| ResourceFrame | 1 |
| Operator | 1 |
| Line | 11 |
| Route | 11 |
| Direction | 11 |
| PointOnRoute | ~60 |
| ScheduledStopPoint | ~232 |
| StopPlace | 26 |
| Quay | 25 |
| JourneyPattern | 11 |
| VehicleJourney | 68 |
| TimetablePassingTime | ~231 |
| DayType | 2 |
| DayTypeAssignment | 14 |
| OperatingPeriod | 1 |

## Arreglos clave (generador)

1. **`_make_id()` centralizado** — genera `ES:COMPOSITE_FRAME:3780:001` con CamelCase→UPPER_SNAKE_CASE y sanitizado de `:` en secuencia
2. **`passingTimes`** wrapper en lugar de `calls`
3. **`TimetablePassingTime`** + `ArrivalTime`/`DepartureTime` como texto directo
4. **`journeyPatternElements`** en lugar de `pointsInSequence` en JourneyPattern
5. **`lineRef`** en cada Route (ROUTE_3)
6. **`TransportMode`** en cada Line (LINE_4)
7. **`validityConditions`** wrapper con `ValidBetween` en CompositeFrame
8. **Filtro** de viajes sin stop_times (68 viajes Ouigo sin paradas)
9. **`countryRef`** en PostalAddress (COMPOSITE_FRAME_1)

## Arreglos clave (validador)

1. **LINE_4**: `transportMode` → `TransportMode` (PascalCase)
2. **ROUTE_4**: `routeElements` → `pointsInSequence` (PascalCase)
3. **SERVICE_JOURNEY_12**: `operatorRef` → `OperatorRef` (PascalCase) — el generador ya emitía el elemento correcto pero el validador buscaba con minúscula
4. **SERVICE_JOURNEY_13**: aceptar `dayTypes` como alternativa a `dates`/`serviceCalendarRef`
5. **SERVICE_JOURNEY_15**: `arrival`/`departure` → `.//ArrivalTime`/`DepartureTime` (PascalCase + descendiente)
6. **XPATH_1**: `./*` → `/*` (contexto de raíz del documento, no hijos del root element)
7. **COMPOSITE_FRAME_3**: busca `ValidBetween` dentro de `validityConditions`

## Comandos

```bash
# Generar XML
cd /root/workspace/netex-es/tools/gtfs-to-netex-es
python3 -c "
from converter.gtfs_reader import GTFSReader
from converter.netex_writer import NeTExWriter
from converter.config import Config
reader = GTFSReader('/root/workspace/netex-es/gtfs-sample/ouigo')
feed = reader.read()
writer = NeTExWriter(feed, Config(publisher_name='OuigoEspana', frame_id_prefix='ES', version='1.0'))
with open('/tmp/ouigo_output.xml', 'w') as f:
    f.write(writer.to_string(pretty=True))
print('OK -', round(len(open('/tmp/ouigo_output.xml').read())/1024, 1), 'KB')
"

# Validar con validador español
netex-es-validator /tmp/ouigo_output.xml --verbose

# Validar con XSD oficial (lxml)
python3 -c "
from lxml import etree
xsd = etree.XMLSchema(etree.parse('/path/to/NeTEx_ES.xsd'))
xml = etree.parse('/tmp/ouigo_output.xml')
if xsd.validate(xml):
    print('XSD: OK')
else:
    for err in xsd.error_log:
        print(f'{err.type_name}: {err.message}')
"
```

## Próximos pasos

1. XSD oficial (71 errores de orden de elementos)
2. Round-trip NeTEx→GTFS
3. Tests monorepo (19 fail, 16 skip)
4. Warnings (517): version attributes, transportSubMode, AccessibilityAssessment
