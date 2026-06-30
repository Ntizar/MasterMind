# GTFS — Exploración completa de archivos y patrones avanzados

**Fecha:** 2026-06-23  
**Origen:** Auditoría del visor GTFSSpain — `GTFSSpain/visor/index.html`

## El problema

El visor original solo usaba 4 archivos GTFS: `stops.txt`, `routes.txt`, `trips.txt`, `stop_times.txt`.  
Un GTFS real tiene hasta 10 archivos estándar, y se perdía toda la información semántica:

- `route_short_name` → "822" (código interno) en vez de `trip_headsign` → "A Estrada E.A.-Troáns"
- `route_color` → todo azul genérico en vez de colores reales por línea
- `shapes.txt` → ninguna línea de ruta dibujada en el mapa
- `agency.txt` → nombre del ZIP en vez de "Autocares Rias Baixas S.L."

## Archivos GTFS y qué extraer

| Archivo | Obligatorio | Qué extraer | Uso |
|---------|-------------|-------------|-----|
| `stops.txt` | Sí | stop_id, stop_name, stop_code, stop_lat, stop_lon | Paradas en mapa |
| `routes.txt` | Sí | route_id, route_short_name, route_long_name, route_type, **route_color** | Colores reales |
| `trips.txt` | Sí | trip_id, route_id, **trip_headsign**, **shape_id** | Nombres reales, shapes |
| `stop_times.txt` | Sí | trip_id, arrival/departure_time, stop_id, stop_sequence | Horarios |
| `agency.txt` | No | agency_name, agency_url | Empresa real |
| `shapes.txt` | No | shape_id, shape_pt_lat, shape_pt_lon, **shape_pt_sequence** | Trazados en mapa |
| `calendar.txt` | No | service_id, días, fechas | Calendario |
| `calendar_dates.txt` | No | service_id, date, exception_type | Excepciones |
| `fare_attributes.txt` | No | fare_id, price, currency | Precios |
| `fare_rules.txt` | No | fare_id, route_id | Tarifas por ruta |

## Patrones clave

### trip_headsign como nombre de ruta
```javascript
// trips.txt → allTripHeadsigns[trip_id] = headsign
// showSchedulePanel → uniqueHeadsigns.slice(0,2).join(' / ')
```

### shapes.txt → dibujar en mapa
```javascript
// Leer → ordenar por shape_pt_sequence → quitar campo seq → L.polyline
```

### Frecuencia media real
```javascript
// timeToMin() → ordenar por hora → diff entre consecutivos → media
// NO usar totalViajes / 2
```

## Pitfalls descubiertos

1. **tripRouteMap hoisting** — declarar siempre al inicio del script con variables globales, no dentro de funciones.
2. **stop_times.txt doble lectura** — leer una sola vez, construir índices local+global en un bucle.
3. **shapes.txt desordenado** — siempre ordenar por shape_pt_sequence antes de dibujar.

## Ejemplo real (1843_GTFS-ZIP.zip)

```
agency.txt: 253 bytes → "Autocares Rias Baixas S.L."
stops.txt: 149,664 bytes → ~2,500 paradas
routes.txt: 19,878 bytes → ~120 rutas
trips.txt: 139,491 bytes → ~2,200 viajes
stop_times.txt: 1,889,439 bytes → ~30,000 paradas por viaje
calendar.txt: 3,455 bytes → ~25 servicios
calendar_dates.txt: 87,492 bytes → excepciones
shapes.txt: 323,336 bytes → ~5,000 puntos de forma
```

## Referencias

- Skill: `gtfs-browser-parser`
- Repo: `github.com/Ntizar/GTFSSpain`
- Visor: `visor/index.html` (147 KB, 1338 líneas)