# Catálogo GBFS de España — 68 sistemas

**Fuente:** `raw.githubusercontent.com/MobilityData/gbfs/master/systems.csv`
**Fecha de extracción:** 2026-06-23
**Ubicación del dato completo:** `GBFSSpain/data/systems.json` en repo `github.com/Ntizar/GBFSSpain`

## Resumen

| Métrica | Valor |
|---|---|
| Total sistemas | 68 |
| Con GBFS v3.0 | 38 |
| Sin v3.0 (v2.3) | 30 |
| Ciudades | 58 |
| Plataformas | 9 |
| Autenticación | Ninguna (todos públicos) |

## Por plataforma

| Plataforma | Sistemas | v3.0 | Ejemplos |
|---|---|---|---|
| Getaround | 25 | 25 | Madrid, Barcelona, Valencia, Sevilla, Granada, Alicante... |
| Nextbike | 14 | 0 | AMBici, bizkaibizi, BiciPalma, moxsi, TUeBICI, BiciLOG... |
| Dott | 9 | 0 | Dott Murcia, Dott Tenerife, Dott Ibiza, Dott Tarragona... |
| Public Bike System (JCDecaux) | 8 | 8 | BiciMAD, Bicing BCN, Sevici, Valenbisi, Dbizi, Bizi Zaragoza... |
| Bird | 7 | 0 | Bird Madrid, Bird Barcelona, Bird Gijón, Bird Murcia... |
| Cyclocity | 2 | 2 | Sevici, Valenbisi |
| Cooltra | 1 | 1 | Cooltra Barcelona (scooters) |
| Donkey Republic | 1 | 1 | Donkey Barcelona |
| Ganxeta | 1 | 1 | Ganxeta Reus |

## Endpoints GBFS estándar

```
gbfs.json                  → discovery (lista de feeds)
station_information.json   → estaciones (lat, lon, nombre, capacidad)
station_status.json        → estado en tiempo real (bikes/spaces)
vehicle_types.json         → tipos de vehículo
geofencing_zones.json      → zonas de geocercado
system_information.json    → info del sistema
system_regions.json        → regiones
system_pricing_plans.json  → precios
gbfs_versions.json         → versiones
```

## Notas técnicas

- **URLs relativas:** Las URLs en gbfs.json pueden ser relativas. Resolver con `new URL(feed.url, discoveryUrl)`.
- **Rate limiting:** Los feeds se actualizan cada 30s. No hacer polling más frecuente.
- **CORS:** La mayoría permiten CORS. Bird y Dott pueden necesitar proxy.
- **Nextbike usa v2.3:** Estructura similar pero con diferencias menores.
- **Algunos feeds inactivos:** Los datos pueden estar vacíos aunque el endpoint exista.
