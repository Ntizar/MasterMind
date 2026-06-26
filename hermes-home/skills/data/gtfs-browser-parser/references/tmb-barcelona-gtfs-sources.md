# Fuentes GTFS TMB Barcelona — Session 2026-06-21

## Problema detectado

Desde la MicroVM de NaNBuilders (1vCPU/2GB/20GB), **todos los intentos de descargar GTFS de TMB fallan con `curl` status 000** (DNS resolution fail). No es que los feeds no existan, es que la VM no resuelve DNS para dominios externos.

## URLs probadas (todas con status 000 = DNS/connection fail)

| Fuente | URL | Estado |
|---|---|---|
| TMB oficial | `https://gtfs.tmb.cat/gtfs.zip` | 000 |
| MobilityData Barcelona | `https://barcelona.mobilitydata.org/gtfs.zip` | 000 |
| Barcelona Open Data | `https://opendata-ajuntament.barcelona.cat/datasets/tmb-metro-de-barcelona-gtfs/` | 404 |
| Datahub TMB | `https://obert.datahub.cat/tmb/metro-de-barcelona-gtfs` | 000 |
| datos.tmb.cat | `https://datos.tmb.cat/gtfs.zip` | 000 |
| TMB static | `https://www.tmb.cat/static/gtfs/gtfs.zip` | 404 |
| TransitLand API | `https://api.transit.land/api/v1/feeds?q=tmb+barcelona` | Sin respuesta |
| Interline API | `https://api.interline.io/v1/feed-sources?q=tmb+barcelona` | Sin respuesta |
| MobilityData API | `https://api.mobilitydata.com/v1/feeds?search=tmb+barcelona` | Sin respuesta |

## Fuentes alternativas para descargar desde máquina local

1. **GTFS Feed Registry (MobilityData)**: `https://gtfs.mobilitydata.org/feeds` — buscar "tmb" o "barcelona"
2. **TransitLand**: `https://transit.land/` — buscar feeds de Barcelona
3. **TMB Open Data**: `https://www.tmb.cat/obert-dades` — página oficial de datos abiertos
4. **Barcelona Open Data**: `https://opendata-ajuntament.barcelona.cat/` — portal de datos abiertos
5. **GTFS de Barcelona**: `https://www.barcelona.cat/obert-dades`

## Solución recomendada

1. Descargar el GTFS desde tu máquina local con acceso a internet
2. Colocar el archivo `gtfs-cache-barcelona.json` actualizado en `/root/workspace/TimeIneco2/data/`
3. Commit y push al repo `Ntizar/TimeIneco2`
