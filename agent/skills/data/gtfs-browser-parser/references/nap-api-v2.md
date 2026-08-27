# API del NAP (Nacional Access Point) — Referencia Rápida

**Portal:** https://nap.transportes.gob.es
**API Base:** `https://nap.transportes.gob.es/api/v2/`
**Auth:** Header `x-api-key: ApiKey` (obligatorio en todos los endpoints)
**Swagger:** https://nap.transportes.gob.es/api/index.html?url=/swagger/v2/swagger.json

## Endpoints (31 total)

### Conjuntos de datos
| Endpoint | Método | Descripción |
|---|---|---|
| `/api/v2/conjunto-dato` | GET | Listar todos (paginado: page, items=1000) |
| `/api/v2/conjunto-dato/{id}` | GET | Detalle de un conjunto |
| `/api/v2/conjunto-dato/region/{id}` | GET | Por provincia |
| `/api/v2/conjunto-dato/tipo-transporte/{id}` | GET | Por modo de transporte |
| `/api/v2/conjunto-dato/tipo-fichero/{id}` | GET | Por tipo de fichero |
| `/api/v2/conjunto-dato/organizacion/{id}` | GET | Por organización |
| `/api/v2/conjunto-dato/{id}/historico` | GET | Versiones históricas |

### Ficheros
| Endpoint | Método | Descripción |
|---|---|---|
| `/api/v2/fichero/{id}/descarga` | GET | Enlace de descarga GTFS |
| `/api/v2/fichero/{id}/descarga/avisos` | GET | Avisos de validación |
| `/api/v2/fichero/{id}/descarga/historico` | GET | Historico de descargas |

### Lookups
| Endpoint | Método | Descripción |
|---|---|---|
| `/api/v2/tipo-transporte` | GET | Todos los tipos |
| `/api/v2/tipo-fichero` | GET | Todos los tipos de fichero |
| `/api/v2/region` | GET | Todas las regiones |
| `/api/v2/region/tipo` | GET | Tipos de región |
| `/api/v2/operador` | GET | Todos los operadores |
| `/api/v2/organizacion` | GET | Todas las organizaciones |

## Estructura de datos clave

### ConjuntoDatoV2Response
```
{ id, nombre, descripcion, tiposTransporte[], fechaCreacion,
  ficheros[], organizacion?, regiones[], operadores[], isObsolete }
```

### FicheroV2
```
{ id, nombreTipoFichero, numeroViajes, numeroRutas, numeroParadas,
  tamanio, esValido, fechaActualizacion, fechaDesde, fechaHasta,
  avisos[], metadatos[] }
```

### TipoTransporte (ejemplos)
IDs típicos: 1=Autobús urbano, 2=Autobús interurbano, 3=Tren, 4=Metro, 5=Tranvía, 6=Ferrocarril, 7=Ferry, 8=Funicular, 9=Teleférico, 10=Tren de alta velocidad...

### TipoFichero (ejemplos)
IDs típicos: 1=GTFS Static, 2=GTFS Realtime, 3=NeTEx...

## Limitaciones importantes

- **NO hay endpoints públicos** — todas las llamadas requieren API Key
- **No hay demo key** — hay que registrarse en el portal
- **GTFS Realtime** — la API del NAP distribuye principalmente GTFS estáticos. El GTFS-realtime existe pero es minoritario
- **Sin planificación de rutas** — la API no ofrece routing ni directions
- **Sin datos de posición GPS en vivo** — eso requiere APIs directas de operadores o SITDA

## Para mapa de transportes

Arquitectura mínima:
1. NAP → catálogo y descarga GTFS estáticos
2. Parser GTFS → extraer stops, routes, trips
3. Leaflet/Mapbox → visualización
4. APIs externas (SITDA, operadores) → tiempo real
5. OSRM/GraphHopper → planificación multimodal
