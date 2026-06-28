# Time2 Master Plan — Auditoría + Arquitectura Completa

**Fecha:** 25 de junio de 2026
**Repo:** `Ntizar/TimeIneco2` (privado)

## Resumen Ejecutivo

Time2 es el sucesor de TimeIneco/Time. Mejora los datos ficticios por datos reales, añade costes/CO₂/teletrabajo, y reduce la interacción a UN solo click.

## Auditoría Time v1.0

### Fortalezas
- Arquitectura modular (12 módulos ES)
- Motor GTFS con BFS + convex hull
- Export DOCX/CSV/SHP/GeoJSON/KML
- Datos demográficos reales (28K CPs, INE)
- Kaizen Design System v4.0
- Servidor Node.js autocontenido

### Problemas críticos
- GTFS datos ficticios (rutas "1","2","3", 0 viajes)
- ORS key puede estar revocada (403)
- No hay parsing GTFS real end-to-end
- `suavizarPoligono()` es no-op
- Fórmula población `* 2.5` sin justificación
- `km2PerDeg2 = 12360` solo válida en Madrid

## Arquitectura Time2

### 10 capas de datos
1. Mapa IGN + geocodificación
2. GTFS real NAP (161 datasets)
3. Isócrónas ORS reales
4. Demografía INE
5. Vivienda Idealista
6. GBFS CityBikes
7. Costes por modo
8. Emisiones CO₂
9. Teletrabajo escenarios
10. Informes DOCX 15 secciones

### Stack
- Vanilla JS (ES modules, sin framework)
- Leaflet 1.9.4
- Kaizen Design System v4.0
- Node.js server (proxies + static)

### Scripts de datos
- `download-gtfs-nap.py` — NAP API GTFS
- `precalculate-isochrones.py` — OSMnx + NetworkX
- `generate-data-files.py` — INE/Idealista/AEAT

### APIs
| Fuente | Key | Coste |
|--------|-----|-------|
| ORS | `ORS_API_KEY` | 2,500/día gratis |
| IGN WMTS | Ninguna | Gratis CC BY 4.0 |
| NAP | `NAP_API_KEY` | Gratis |
| CityBikes | Ninguna | Gratis |
| INE | Ninguna | Gratis |
| Nominatim | User-Agent | 1 req/s |
| Idealista | Scraping | Gratis |
| AEAT | Ninguna | Gratis |

### Métricas: v1 vs v2
| Métrica | v1 | v2 |
|---------|----|----|
| Click → resultado | 5+ clics | 1 clic |
| Datos GTFS | Ficticios | Reales |
| Isócrónas | 70% simulación | 90% ORS real |
| Fuentes datos | 6 | 10+ |
| Secciones informe | 10 | 15 |
| Costes por modo | Estimados | Calculados |
| CO₂ | No | Sí |
| Teletrabajo | No | 4 escenarios |

### Estimación: ~3500 líneas, ~20h desarrollo
