# Arquitectura Modular del Writer (15 Jul 2026)

## Motivación

El writer original `netex_writer.py` tenía **1.995 líneas** en un solo archivo.
El usuario especificó: *"seguro que se puede hacer lo mismo en trozos más pequeños"*
→ Se partió en **7 módulos** de ~100-350 líneas cada uno.

## Estructura resultante

```
src/converter/
├── netex_writer.py          # Clase principal (268 líneas)
│   ├── __init__             # Config, feed, counters
│   ├── generate()           # Punto de entrada
│   ├── _create_composite_frame()  # Orquesta todos los frames
│   ├── _create_resource_frame()   # Operators, etc.
│   ├── _find_stop(), _find_route()  # Utilidades
│   ├── _get_publisher_code()
│   ├── _append_multilingual_names()
│   ├── to_string(), to_file()  # Serialización
│   └── _wgs84_to_utm(), _make_location()
│
├── writers/
│   ├── __init__.py          # Re-exporta todo
│   ├── helpers.py           # (96 líneas) Funciones XML helper
│   │   ├── el(), child(), ref(), ns()
│   │   ├── frame_base(), accessibility_elem()
│   │   └── NETEX_NS, XSI_NS, SCHEMA_LOCATION
│   │
│   ├── site_frame.py        # (130 líneas) StopPlaces, Quays, Pathways
│   │   ├── create_site_frame()
│   │   ├── build_stop_place()
│   │   ├── build_quay()
│   │   └── create_pathways()
│   │
│   ├── service_frame.py     # (350 líneas) Lines, Routes, SSP, JourneyPatterns
│   │   ├── create_service_frame()
│   │   ├── create_lines()
│   │   ├── create_routes()
│   │   ├── create_scheduled_stop_points()
│   │   ├── create_line_geometries()
│   │   ├── create_journey_patterns()
│   │   └── create_booking_rules()
│   │
│   ├── calendar_frame.py    # (240 líneas) DayTypes, OperatingPeriods, Holidays
│   │   ├── create_service_calendar_frame()
│   │   ├── create_day_types()
│   │   ├── classify_calendar()
│   │   ├── create_day_type_assignments()
│   │   ├── create_operating_periods()
│   │   ├── get_holiday_year()
│   │   └── create_holiday_day_types()
│   │
│   ├── timetable_frame.py   # (140 líneas) VehicleJourneys
│   │   ├── create_timetable_frame()
│   │   ├── create_headway_groups()
│   │   ├── create_vehicle_journeys()
│   │   └── build_single_vj()
│   │
│   └── fare_frame.py        # (130 líneas) FareFrame, Tariffs, FareProducts
│       ├── create_fare_frame()
│       ├── create_fare_products()
│       ├── create_sales_offer_packages()
│       ├── ticketing_mode_from_duration()
│       └── has_zones()
```

## Patrón de comunicación entre módulos

Cada función de frame toma `writer: "NeTExWriter"` como primer argumento
(forward reference con TYPE_CHECKING). Así acceden a `writer.feed`,
`writer.config`, `writer._counter` y los métodos helper.

```python
# writers/service_frame.py
if TYPE_CHECKING:
    from converter.netex_writer import NeTExWriter

def create_service_frame(writer: "NeTExWriter") -> ET.Element:
    frame = frame_base("ServiceFrame", ...)
    frame.append(create_lines(writer))
    frame.append(create_routes(writer))
    ...
    return frame
```

## Ventajas

- Cada archivo < 400 líneas (objetivo del usuario)
- Cada frame se puede testear independientemente
- Los cambios en un frame no afectan a otros (merge conflicts mínimos)
- Fácil añadir nuevos frames sin tocar el writer principal
- Las funciones helper están en un solo lugar (helpers.py)

## Lecciones aprendidas

### GTFS String Dates
`Calendar.start_date` y `Calendar.end_date` son strings ("20240101"),
NO objetos datetime. Siempre parsear con `datetime.strptime()` antes
de hacer operaciones aritméticas o `.strftime()`.

### Dataclass field names
Cada dataclass de GTFS tiene nombres de campo específicos que pueden
diferir de lo que esperas. Siempre verificar con `inspect.getsource()`:
```python
python3 -c "from converter.gtfs_reader import BookingRule; import inspect; print(inspect.getsource(BookingRule))"
```

### Backward-compat imports
Cuando mueves funciones de un módulo a otro, los tests antiguos que
importan `from converter.netex_writer import _ns, NETEX_NS` rompen.
Solución: actualizar los tests a los nuevos imports:
```python
# ANTES
from converter.netex_writer import NeTExWriter, _ns, NETEX_NS
# DESPUÉS
from converter.netex_writer import NeTExWriter
from converter.writers.helpers import ns as _ns, NETEX_NS
```

### `pretty` parameter en to_string
El writer original tenía `to_string(pretty=True)`. Añadirlo al nuevo
writer con `xml.dom.minidom` para compatibilidad de tests.

### `xml_declaration` config
El `Config` tiene `xml_declaration: bool = True`. El `to_string()` debe
usarlo: `ET.tostring(xml_root, xml_declaration=self.config.xml_declaration)`