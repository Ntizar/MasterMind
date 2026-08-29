# NAP API — Patrón de Descarga GTFS

## Flujo de descarga
1. `GET https://nap.transportes.gob.es/api/v2/fichero/{fichero_id}/descarga` (Header: ApiKey)
2. Respuesta JSON: `{ data: { enlaceDescarga: "https://s3.../GTFS.zip?X-Amz-Expires=900&..." } }`
3. GET enlaceDescarga → ZIP (sin auth adicional). Caduca en ~15 min.

## ⚠️ `/api/v2/conjunto-dato/{id}` devuelve 404 — NO usar

## Fichero IDs conocidos
| Ciudad | Fichero ID | Operador | Paradas | Rutas |
|--------|-----------|----------|---------|-------|
| Sevilla | 1567 | TUSSAM | 1.038 | 59 |
| Valencia | 1166 | EMT Valencia | 1.155 | 49 |
| Zaragoza | 1176 | Tuzsa | 996 | 55 |
| Málaga | 1494 | EMT Málaga | 1.126 | 48 |
| Bilbao | 1460 | Bilbobus | 533 | 56 |

## GTFS estructura
agency.txt, stops.txt, routes.txt, trips.txt, stop_times.txt, calendar.txt, calendar_dates.txt, feed_info.txt

## Pitfalls
- Enlaces S3 caducan ~15 min — descargar inmediatamente
- Header `ApiKey` obligatorio solo para el primer endpoint
- `POST /nap-download-gtfs` en server.mjs sigue el redirect y devuelve ZIP
