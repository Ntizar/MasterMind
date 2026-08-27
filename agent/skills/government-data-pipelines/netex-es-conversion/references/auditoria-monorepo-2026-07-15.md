# Auditoría Monorepo netex-es — 15 Julio 2026

## Estado de tests en el monorepo (tras consolidación)

| Tool | Tests | Pasados | Fallos | Errores | Saltados |
|------|-------|---------|--------|---------|----------|
| gtfs-to-netex-es | 111 | 19 | 40 | 36 | 16 |
| netex-es-to-gtfs | 13 | 6 | 0 | 7 | 0 |
| netex-es-validator | 34 | 34 | 0 | 0 | 0 |

## Causas raíz de los fallos

### 1. Writer esqueleto (500 líneas vs 1995 líneas)
El monorepo tiene `netex_writer.py` de 500 líneas. El real tiene 1.995. El esqueleto carece de:

```
Métodos que faltan en el monorepo (presentes en el real):
- _create_service_frame()       → genera ServiceFrame con líneas, rutas
- _create_lines()                → genera Line + Route
- _create_routes()               → genera Route con puntos de parada
- _create_scheduled_stop_points()→ genera ScheduledStopPoint
- _create_journey_patterns()     → genera JourneyPattern + JourneyPatternElements
- _create_vehicle_journeys()     → genera VehicleJourney + Calls
- _create_fare_frame()           → genera FareFrame con tarifas
- _create_day_types()            → genera DayType + DayTypeAssignment
- _create_operating_periods()    → genera OperatingPeriod
- _create_holiday_day_types()    → genera festivos
- _create_headway_groups()       → genera HeadwayJourneyGroup
- _create_booking_rules()        → genera BookingRule
- _create_line_geometries()      → genera LineGeometry desde shapes
- to_string() / to_file()        → serialización a string/archivo
```

### 2. Errores de FileNotFoundError (36 tests)
Los tests buscan `gtfs-sample/` relativo al directorio del tool:
- `tests/../gtfs-sample` → espera `gtfs-sample/` junto al directorio del tool
- Solución: symlink `tools/gtfs-to-netex-es/gtfs-sample → ../../gtfs-sample`
- Symlink también necesario en `tools/netex-es-to-gtfs/gtfs-sample`

### 3. AttributeError: to_string (12 tests)
El writer esqueleto solo tiene `generate()` que devuelve `ET.Element`. Los tests llaman a `writer.to_string()` que no existe. El writer real sí lo tiene.

## Problemas de infraestructura del monorepo

### pyproject.toml — necesario para src/ layout
```toml
[tool.setuptools.package-dir]
"" = "src"
```
Sin esto, `pip install -e` no encuentra los paquetes dentro de `src/`.

### build-backend correcto
```toml
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.build_meta"  # NO setuptools.backends._legacy
```
`setuptools.backends._legacy` no existe en Python 3.13. Usar `build_meta`.

### README.md requerido
Si el `setup.py` (o legacy config) referencia `open("README.md").read()`, debe existir o pip falla. En monorepo con pyproject.toml puro no es necesario, pero si hay setup.py heredado, sí.

## Bug en enums.yaml — mapeo GTFS route_type incorrecto

```yaml
# ACTUAL (incorrecto):
"0": "metro"      # comentario: Tram/Streetcar/Light rail
"1": "rail"       # comentario: Subway/Metro

# CORRECTO:
# GTFS route_type 0 = Tram/Light Rail → LineType "tram"
# GTFS route_type 1 = Subway/Metro    → LineType "metro"
# GTFS route_type 101 = High Speed Rail → LineType "rail", Submode "highSpeedTrain"
```

Los comentarios que acompañan a cada mapeo están intercambiados con el valor de la línea siguiente. El mapeo 101→"bus" es incorrecto (AVE no es bus).

## Spec-Driven: aspirational, no real

- El paquete `netex-es-spec` existe en `packages/` pero **ningún tool lo importa**
- `gtfs-to-netex-es` importa de `converter.*`, no de `netex_es_spec.*`
- `netex-es-validator` tiene sus propias enumeraciones hardcodeadas en `line_rules.py`, `mode_rules.py`, etc.
- Si cambias `enums.yaml`, nada se actualiza automáticamente
- La verdadera fuente de verdad sigue siendo el código, no el spec

## Pipeline completa — nunca ejecutada desde el monorepo

No hay registro de:
1. GTFS → NeTEx (writer funcional)
2. Validador español (218 reglas)
3. Validación XSD (lxml contra XSD CEN 1.14)
4. NeTEx → GTFS (round-trip)

## Recomendaciones inmediatas

1. **Copiar el writer real** (1.995 líneas) del repo separado al monorepo
2. **Arreglar los pyproject.toml** con `package-dir = "src"` y `build-backend = "setuptools.build_meta"`
3. **Crear symlinks** de `gtfs-sample/` para cada tool
4. **Ejecutar todos los tests** y no avanzar hasta que estén verdes
5. **Hacer que los tools consuman `netex-es-spec`** — eliminar duplicación
6. **Arreglar enums.yaml** mapeos de route_type
7. **Ejecutar pipeline Ouigo completa** como prueba de humo