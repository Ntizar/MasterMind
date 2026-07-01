# NAP API — Patrón de Descarga GTFS

## Estado (2026-06-22)

El endpoint `/api/v2/conjunto-dato/{id}` devuelve **404** — NO usar.
El endpoint `/api/v2/fichero/{id}/descarga` devuelve **HTTP 200** con JSON que contiene un enlace temporal a S3.

## Flujo de descarga

```
1. GET https://nap.transportes.gob.es/api/v2/fichero/{fichero_id}/descarga
   Header: ApiKey: {NAP_API_KEY}
   Header: User-Agent: TimeIneco/2.0

2. Respuesta JSON:
   {
     "success": true,
     "message": "Enlace de descarga del fichero obtenido correctamente.",
     "data": {
       "enlaceDescarga": "https://mfomwpronapdata.s3.eu-west-1.amazonaws.com/GTFS/archive/20260430_100023_TUSSAM/TUSSAM.zip?X-Amz-Expires=900&X-Amz-Algorithm=AWS4-HMAC-SHA256&..."
     }
   }

3. GET {enlaceDescarga} → ZIP file (GTFS)
   No necesita headers de autenticación adicionales.
   Enlace temporal (~15 min caducidad).
```

## Fichero IDs conocidos

| Ciudad | Fichero ID | Operador | Paradas | Rutas | Viajes |
|--------|-----------|----------|---------|-------|--------|
| Sevilla | 1567 | TUSSAM | 1.038 | 59 | 28.295 |
| Valencia | 1166 | EMT Valencia | 1.155 | 49 | 23.116 |
| Zaragoza | 1176 | Tuzsa | 996 | 55 | 25.447 |
| Málaga | 1494 | EMT Málaga | 1.126 | 48 | 23.445 |
| Bilbao | 1460 | Bilbobus | 533 | 56 | 29.947 |

## Estructura GTFS descargada

```
data/gtfs/{ciudad}/
├── agency.txt      (1 archivo por operador)
├── stops.txt       (paradas con coordenadas)
├── routes.txt      (líneas/rutas)
├── trips.txt       (viajes por ruta)
├── stop_times.txt  (horarios por viaje)
├── calendar.txt    (días de servicio)
├── calendar_dates.txt (excepciones)
└── feed_info.txt   (metadatos del feed)
```

## Endpoint en server.mjs

`POST /nap-download-gtfs` — Recibe `{datasetId, operador}`, sigue el redirect a S3, devuelve el ZIP al frontend.

## Pitfalls

- La API NO devuelve el ZIP directamente, devuelve un JSON con URL de S3
- Los enlaces S3 caducan (~15 min) — descargar inmediatamente después de obtener la URL
- El header `ApiKey` es obligatorio para el primer endpoint, pero NO para la descarga de S3
- `conjunto-dato` endpoint devuelve 404 — no confundir con `fichero` que sí funciona
