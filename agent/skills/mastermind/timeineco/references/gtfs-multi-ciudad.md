# GTFS Multi-Ciudad — TimeIneco2

## Resumen

Añadido en 2026-06-21: 6 ciudades españolas con GTFS sintético realista en TimeIneco2.

## Ciudades disponibles

| Key | Ciudad | Operador | Paradas | Rutas |
|-----|--------|----------|---------|-------|
| sevilla | Sevilla | EMT Sevilla | 25 | 15 |
| valencia | Valencia | EMT Valencia | 25 | 15 |
| bilbao | Bilbao | EMT Bilbao | 25 | 14 |
| zaragoza | Zaragoza | EMT Zaragoza | 25 | 14 |
| malaga | Málaga | EMT Málaga | 25 | 14 |
| gran_canaria | Gran Canaria | TUS | 25 | 14 |

## Estructura del GTFS sintético

Cada `gtfs-cache-{ciudad}.json` contiene:

- `_meta`: versión, ciudad, operador, fecha
- `routes[]`: 14-15 rutas con IDs reales (EMT-S1, EMT-M1, etc.)
- `stops[]`: 25 paradas con coordenadas reales
- `trips[]`: 56-60 viajes (4 por ruta)
- `stop_times[]`: 968-1120 horarios
- `shapes[]`: 18 trazados con interpolación
- `route_stops[]`: 140 relaciones ruta-parada
- `calendar[]`: weekday/saturday/sunday

## Generación programática

Script `scripts/generate-gtfs-synthetic.py` permite añadir más ciudades:

1. Añadir ciudad en `CITIES` dict
2. Añadir rutas en `CITY_ROUTES_MAP`
3. Añadir paradas en `CITY_STOPS_MAP`
4. Ejecutar script

## Compatibilidad con GTFS Engine

El GTFS sintético es compatible con `gtfs-engine.v7.js` de TimeIneco:
- `findStopsNear()` funciona con `stops[]` + `route_stops{}`
- Motor GTFS-based de isocronas (BFS) necesita `trips[]` + `stop_times[]`
- Trazados en mapa necesitan `shapes[]`

## Pitfalls

- Prefijo alfabético en route_id: EMT-S1, EMT-V2, TUS-G1 → el parser quita cualquier prefijo alfabético
- `random.seed(42)` para reproducibilidad
- GTFS sintético con solo stops+route_stops funciona para búsqueda pero NO para isocronas BFS
