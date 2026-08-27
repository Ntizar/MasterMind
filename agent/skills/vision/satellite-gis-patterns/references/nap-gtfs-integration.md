# NAP API — Catálogo de GTFS (transportes.gob.es)

## Resumen

La API NAP de transportes.gob.es es un catálogo de datasets GTFS de España.
**No es un motor de routing** — es un repositorio de datos de transporte público
que se descargan y parsean localmente.

## Autenticación

- **Header:** `ApiKey: <tu_api_key>`
- **Sin auth:** devuelve `{"success": false, "message": "Api Key was not provided."}`
- **Obtener key:** registro en https://nap.transportes.gob.es

## Endpoints principales

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/v2/conjunto-dato` | GET | Listar datasets (paginado) |
| `/api/v2/conjunto-dato/{id}` | GET | Detalle de un dataset |
| `/api/v2/fichero/{id}/descarga` | GET | Descargar fichero GTFS |
| `/api/v2/region` | GET | Listar regiones (requiere auth) |
| `/api/v2/operador` | GET | Listar operadores |
| `/api/v2/tipo-transporte` | GET | Listar tipos de transporte |
| `/api/v2/tipo-fichero` | GET | Listar tipos de fichero |

## Parámetros de filtro (GET /conjunto-dato)

- `regionId` — Filtrar por región
- `tipoTransporteId` — Filtrar por tipo (Metro, Cercanías, Autobús, etc.)
- `tipoFicheroId` — Filtrar por tipo de fichero
- `organizacionId` — Filtrar por organización
- `page` — Página (default 1)
- `items` — Items por página (default 1000)

## Esquemas clave

### ConjuntoDatoV2Response
```json
{
  "id": 123,
  "nombre": "Metro de Madrid",
  "descripcion": "Datos GTFS del Metro de Madrid",
  "tiposTransporte": [{"id": 1, "nombre": "Metro", "nombreGrupo": "Férreo"}],
  "fechaCreacion": "2024-01-15T00:00:00Z",
  "ficheros": [{"id": 456, "numeroParadas": 200, "numeroRutas": 13, "tamanio": 50000}],
  "organizacion": {"id": 1, "nombre": "Metro de Madrid S.A."},
  "regiones": [{"id": 28, "nombre": "Madrid", "nombreTipo": "Provincia"}],
  "operadores": [{"id": 1, "nombre": "Metro de Madrid", "url": "..."}],
  "isObsolete": false
}
```

### FicheroV2
```json
{
  "id": 456,
  "nombreTipoFichero": "GTFS",
  "numeroViajes": 5000,
  "numeroRutas": 13,
  "numeroParadas": 200,
  "tamanio": 50000,
  "esValido": true,
  "fechaActualizacion": "2024-06-01T00:00:00Z",
  "fechaDesde": "2024-01-01T00:00:00Z",
  "fechaHasta": "2024-12-31T23:59:59Z"
}
```

## Tipos de transporte disponibles

Metro, Cercanías, Autobús urbano, Metro ligero, Tranvía, Funicular,
Teleférico, AVE, Media Distancia, Regional, Intercity, Autocar, Ferry,
Taxi, Aerolínea, Alquiler de bicicletas, Coche compartido

## Flujos típicos

### 1. Buscar datasets de una región
```bash
curl -H "ApiKey: $NAP_KEY" \
  'https://nap.transportes.gob.es/api/v2/conjunto-dato?regionId=28'
```

### 2. Filtrar por tipo de transporte
```bash
curl -H "ApiKey: $NAP_KEY" \
  'https://nap.transportes.gob.es/api/v2/conjunto-dato?tipoTransporteId=1'
```

### 3. Descargar GTFS
```bash
curl -H "ApiKey: $NAP_KEY" \
  -o gtfs.zip \
  'https://nap.transportes.gob.es/api/v2/fichero/456/descarga'
```

## Limitaciones

- **Solo España** — NAP solo cubre transporte público español
- **Requiere API key** — No hay endpoints públicos
- **No es routing** — Solo proporciona datos GTFS para parsear localmente
- **No tiene GTFS-RT** — Solo datos estáticos, no tiempo real

## Alternativas para TP mundial

- **Transitland API** — Agregador mundial de GTFS
- **OpenTripPlanner** — Motor de routing TP self-host
- **GTFS directo** — Descargar de cada operador de transporte

## Referencias

- API docs: https://nap.transportes.gob.es/api/index.html?url=/swagger/v2/swagger.json
- Swagger: https://nap.transportes.gob.es/api/swagger/v2/swagger.json
- Proyecto: TimeIneco (/root/workspace/TimeIneco)
