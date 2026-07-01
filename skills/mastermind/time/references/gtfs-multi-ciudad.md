# GTFS Multi-Ciudad

## Ciudades con GTFS
| Key | Ciudad | Operador | Paradas | Rutas |
|-----|--------|----------|---------|-------|
| sevilla | Sevilla | EMT Sevilla | 25 | 15 |
| valencia | Valencia | EMT Valencia | 25 | 15 |
| bilbao | Bilbao | EMT Bilbao | 25 | 14 |
| zaragoza | Zaragoza | EMT Zaragoza | 25 | 14 |
| malaga | Málaga | EMT Málaga | 25 | 14 |
| madrid | Madrid | EMT Madrid | 250 | 46 |

## Estructura gtfs-cache-{ciudad}.json
_meta, routes[], stops[], trips[], stop_times[], shapes[], route_stops[], calendar[]

## Generación
Script `scripts/generate-gtfs-synthetic.py` — random.seed(42) para reproducibilidad.

## Pitfalls
- GTFS sintético con solo stops+route_stops funciona para búsqueda pero NO para isocronas BFS
- Prefijo alfabético en route_id: EMT-S1, TUS-G1 → parser quita prefijos
