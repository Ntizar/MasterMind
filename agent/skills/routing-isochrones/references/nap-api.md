# NAP API — Catálogo de Datos de Transporte España

## Fuente
https://nap.transportes.gob.es/api/index.html?url=/swagger/v2/swagger.json

## Autenticación
- **Header:** `ApiKey: {tu_api_key}`
- **Registro:** https://nap.transportes.gob.es (solicitar a transportes.gob.es)

## Endpoints principales

### Conjuntos de datos
```
GET /api/v2/conjunto-dato                          # Listar todos
GET /api/v2/conjunto-dato/{id}                     # Detalle de un conjunto
GET /api/v2/conjunto-dato?regionId=X               # Filtrar por región
GET /api/v2/conjunto-dato?tipoTransporteId=X       # Filtrar por tipo
GET /api/v2/conjunto-dato/{id}/historico           # Versiones anteriores
```

### Ficheros GTFS
```
GET /api/v2/fichero/{id}/descarga                  # Descargar GTFS
GET /api/v2/fichero/{id}/descarga/avisos           # Avisos del fichero
GET /api/v2/fichero/{id}/descarga/historico        # Versiones anteriores
```

### Catálogos
```
GET /api/v2/region                          # Listar regiones
GET /api/v2/operador                        # Listar operadores
GET /api/v2/organizacion                    # Listar organizaciones
GET /api/v2/tipo-fichero                    # Listar tipos de fichero
GET /api/v2/tipo-transporte                 # Listar tipos de transporte
```

## Estructura de respuesta

### ConjuntoDatoV2Response
```json
{
    "id": 123,
    "nombre": "EMT Madrid - Autobuses urbanos",
    "descripcion": "Datos GTFS de autobuses urbanos de Madrid",
    "tiposTransporte": [
        {"id": 2, "nombre": "Autobús urbano", "idGrupo": 1, "nombreGrupo": "Terrestre"}
    ],
    "fechaCreacion": "2024-01-15T00:00:00Z",
    "ficheros": [
        {
            "id": 456,
            "nombreTipoFichero": "GTFS",
            "numeroViajes": 12500,
            "numeroRutas": 200,
            "numeroParadas": 3500,
            "tamanio": 2500000,
            "esValido": true,
            "fechaActualizacion": "2024-06-01T00:00:00Z"
        }
    ],
    "organizacion": {
        "id": 1,
        "nombre": "EMT Madrid"
    },
    "regiones": [
        {"id": 28, "nombre": "Madrid", "idTipo": 1, "nombreTipo": "Comunidad Autónoma"}
    ],
    "operadores": [
        {"id": 10, "nombre": "EMT Madrid", "url": "https://www.emtmadrid.es"}
    ],
    "isObsolete": false
}
```

### Tipos de transporte disponibles
- Metro (id: 1)
- Autobús urbano (id: 2)
- Cercanías (id: 3)
- Metro ligero (id: 4)
- Tranvía (id: 5)
- Funicular (id: 6)
- Teleférico (id: 7)
- AVE (id: 8)
- Media Distancia (id: 9)
- Regional (id: 10)
- Intercity (id: 11)
- Autocar (id: 12)
- Ferry (id: 13)
- Taxi (id: 14)
- Aerolínea (id: 15)
- Alquiler de bicicletas (id: 16)
- Coche compartido (id: 17)

### Tipos de fichero
- GTFS (estándar)
- GTFS-RT (tiempo real)
- GTFS-Fare (tarifas)

## Uso típico para isocronas

```
1. GET /api/v2/conjunto-dato?regionId=28&tipoTransporteId=2
   → Lista de datasets GTFS de autobuses en Madrid

2. GET /api/v2/conjunto-dato/{id}
   → Obtener fichero con id=456

3. GET /api/v2/fichero/456/descarga
   → Descargar archivo GTFS comprimido

4. Parsear GTFS localmente:
   - stops.txt → paradas (lat, lon, nombre)
   - routes.txt → rutas (id, nombre, tipo)
   - trips.txt → viajes (route_id, trip_id)
   - stop_times.txt → horarios (trip_id, arrival_time, departure_time)
   - calendar.txt → días de servicio

5. Calcular paradas cercanas a origen/destino (Haversine < 400m)

6. Filtrar rutas que conecten ambas zonas en horario laboral:
   - Ida: llegada 7:30-9:30
   - Vuelta: salida 16:30-18:30
```

## Limitaciones
- Solo datos de España
- Requiere API key (solicitar)
- No es un motor de routing (solo catálogo de datos)
- Para routing real con transbordos: usar OpenTripPlanner con los datos GTFS descargados
