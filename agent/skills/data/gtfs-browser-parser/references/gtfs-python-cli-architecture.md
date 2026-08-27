# GTFStoCSV — Python CLI Architecture

Proyecto creado 2026-07-03 como extensión CLI del patrón de parseo GTFS. Complementa el enfoque browser-side con exportaciones a formatos GIS.

## Arquitectura

```
GTFS.zip ──► GTFSParser ──► dicts de datos ──► Exporters
  (zipfile+csv)                                 │
                                                ├──► CSV (csv.DictWriter)
                                                ├──► GeoJSON (json)
                                                ├──► SHP (pyshp, opcional)
                                                └──► Visor HTML (templater.py)
```

**Ruta:** `/root/workspace/GTFStoCSV/`

## GTFSParser (parser.py)

Clase que parsea un ZIP GTFS usando solo stdlib (`zipfile`, `csv`, `json`).

### Atributos de salida (todas listas de dicts)

| Atributo | Origen | Descripción |
|---|---|---|
| `parser.agency` | agency.txt | Operador(es) del feed |
| `parser.routes` | routes.txt | Líneas/rutas (43 en Cáceres) |
| `parser.trips` | trips.txt | Viajes (3,962) |
| `parser.stop_times` | stop_times.txt | Horarios parada por viaje (76,803) |
| `parser.stops` | stops.txt | Paradas (237) |
| `parser.shapes` | shapes.txt | Trazados geográficos (11,345 pts) |
| `parser.calendar` | calendar.txt | Servicios regulares (7 registros) |

### Índices pre-construidos

| Atributo | Tipo | Uso |
|---|---|---|
| `stops_by_id` | `{stop_id: dict}` | Lookup O(1) |
| `routes_by_id` | `{route_id: dict}` | Lookup O(1) |
| `trips_by_route` | `{route_id: [trips]}` | Trips por ruta |
| `shapes_coords` | `{shape_id: [(lat,lng)]}` | Coords para Leaflet |
| `stop_times_by_trip` | `{trip_id: [stop_times]}` | Horarios por viaje |

### Métodos útiles

- `parser.summary_text()` — Resumen formateado
- `parser.get_route_shape(route_id)` — [(lat, lng), ...]
- `parser.get_route_stops_ordered(route_id)` — Paradas en orden

### Manejo de archivos opcionales

El parser carga `stops.txt`, `routes.txt`, `trips.txt`, `stop_times.txt`, `shapes.txt`, `calendar.txt`, `agency.txt`. Si alguno falta, se omite sin error. No implementa calendar_dates, frequencies, transfers ni feed_info (contrario al skill browser-side).

## Exporter (exporter.py)

Funciones modulares que reciben el parser y escriben archivos en disco.

### export_csv(ruta, output_name, headers, rows)

Escribe un CSV individual con DictWriter. Se usa para cada tabla GTFS por separado.

### export_all_geojson(parser, output_dirs)

Genera un único FeatureCollection con todas las rutas. Cada Feature tiene:
- `geometry: LineString` — coordenadas del shape
- `properties` — route_id, route_short_name, route_long_name, route_type, agency_id, trip_count

Rutas sin shape (trazado circular) se incluyen sin geometry (coords=[]). El visor las maneja sin errores.

### export_shp_zip(parser, zip_path)

Dependencia: `pyshp`.

Crea ZIP con 4 archivos por formato shapefile:
- `rutas.shp` — geometrías LineString
- `rutas.shx` — índice espacial
- `rutas.dbf` — atributos (shape_id, route_id, etc.)
- `rutas.prj` — proyección WGS84 (EPSG:4326)

### export_table_summary(parser, output_dir)

Exporta todas las tablas GTFS parseadas como CSVs individuales en un directorio.

## Templater (templater.py)

Genera un visor HTML autocontenido (se abre con doble clic, sin servidor).

### Contenido del HTML

- **Kaizen Design System v4.0** (Ineco corporate) — CSS inline (~23KB)
- **Leaflet 1.9.4** — mapa interactivo (desde CDN)
- **IGN WMTS** — capas `IGNBaseTodo-gris` y `IGNBaseOrto`
- **JSZip 3.10.1** — inline para drag & drop adicional
- **Datos JSON** — `data.json` con todos los datos serializados
- **JavaScript del visor** — ~300 líneas inline

### Funcionalidad del visor

1. **Mapa IGN** — gris por defecto, toggle a ortofoto
2. **Rutas en mapa** — polylines coloreadas por ruta, clickeables
3. **Panel de ruta** — al click: nombre, tipo, agencia, paradas, trips
4. **Búsqueda** — filtro en tiempo real de rutas por nombre/código
5. **Todas las tablas** — acordeones con datos tabulares exportables
6. **Exportación individual** — GeoJSON descargable por ruta
7. **Drag & drop** — carga adicional de GTFS desde el navegador

### Pitfall: f-string escaping

**NUNCA usar** `f"${variable}"` en Python con template literals JS. Escapar como `f"${{variable}}"`.

## CLI Entry Point (run.py)

```bash
python run.py <GTFS.zip> [opciones]

Opciones:
  -o, --output DIR    Directorio de salida (default: output/)
  --no-shp            Saltar exportación SHP (si no hay pyshp)
  --format FORMAT     Exportar solo: csv, geojson, shp, html (default: todos)
  --skip-html         No generar visor HTML
```

## Dependencias

| Paquete | Tipo | Uso |
|---|---|---|
| `pyshp` | opcional | Exportación Shapefile (.shp) |
| stdlib | built-in | Todo lo demás (csv, json, zipfile) |

## Tamaños típicos (Cáceres, 43 rutas)

| Archivo | Tamaño |
|---|---|
| GTFS ZIP | 594 KB |
| visor.html | 783 KB (con Kaizen + JSZip inline) |
| data.json | 3.2 MB |
| todas_las_rutas.geojson | 559 KB |
| todas_las_rutas.shp.zip | 193 KB |
| output/csv/ (7 archivos) | 4.1 MB total |

## Git

No inicializado en `GTFStoCSV/`. Recomendación: `git init`, `git add .`, `git commit -m "feat: GTFStoCSV v1.0.0 — Python GTFS to CSV/GeoJSON/SHP/HTML"`.

## Ver también

- Skill principal: `gtfs-browser-parser` — sección "Python GTFS Parser & Exporter (CLI tool)"
- Proyecto browser-side: `GTFSSpain-v2` — visor web GTFS con todas las funcionalidades
- HTML escaping: `frontend-dashboard-patterns > references/python-fstring-html-escaping.md`