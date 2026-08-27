# Patrón: Visor GBFS — Bicicletas compartidas en el navegador

**Creado:** 2026-06-23 — Sesión GBFSSpain

## Contexto

El usuario quería un visor de sistemas de bicicletas compartidas en España, igual de guapo que GTFSSpain pero para bicis. Resultado: **GBFSSpain** — 68 sistemas de 58 ciudades, todo en el navegador sin servidor.

## Datos: catálogo MobilityData/gbfs

El catálogo oficial está en `https://raw.githubusercontent.com/MobilityData/gbfs/refs/heads/master/systems.csv`

### España: 68 sistemas, TODOS públicos

| Plataforma | Sistemas | Versiones | Ejemplos |
|---|---|---|---|
| Public Bike System (JCDecaux) | 8 | v3.0 | BiciMAD, Bicing BCN, Sevici, Valenbisi, Dbizi, Bizi Zaragoza, Bicicoruña, Bilbao Bizi |
| Nextbike | 14 | v2.3 | AMBici, bizkaibizi, moxsi, TUeBICI, BiciLOG, BiciPalma |
| Getaround | 22 | v3.0 | Madrid, Barcelona, Valencia, Sevilla, Granada... |
| Dott | 9 | v2.3 | Murcia, Tenerife, Ibiza, Tarragona, Lorca |
| Bird | 7 | v2.3 | Madrid, Barcelona, Gijón, Murcia, Adeje |
| Cyclocity | 2 | v3.0 | Sevici, Valenbisi |
| Donkey Republic | 1 | v3.0 | Barcelona |
| Cooltra | 1 | v3.0 | Barcelona (scooters) |
| Ganxeta | 1 | v3.0 | Reus |

### Estructura GBFS

Cada sistema tiene estos endpoints JSON (no CSV como GTFS):

```
gbfs.json (discovery)
├── system_information        → nombre, idioma, operador, licencia
├── station_information       → estaciones (lat, lon, nombre, capacidad)
├── station_status            → estado en tiempo real (bikes, docks)
├── vehicle_types             → tipos de vehículo
├── geofencing_zones          → zonas de geocercado
├── system_pricing_plans      → precios
└── gbfs_versions             → versiones soportadas
```

**Tamaño total:** ~200-500 KB por sistema (vs 50-200 MB de GTFS)

### URLs de feeds confirmadas

- Madrid: `https://madrid.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- Barcelona: `https://barcelona.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- Sevilla: `https://api.cyclocity.fr/contracts/seville/gbfs/v3/gbfs.json`
- Valencia: `https://api.cyclocity.fr/contracts/valence/gbfs/v3/gbfs.json`
- Zaragoza: `https://zaragoza.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- Bilbao: `https://bilbao.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- Donostia: `https://sansebastian.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- A Coruña: `https://acoruna.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- Valladolid: `https://valladolid.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`

## Comparativa GTFS vs GBFS

| | GTFS | GBFS |
|---|---|---|
| Formato | CSVs en ZIP | JSON directo |
| Parsing | CSV manual + JSZip | JSON.parse() |
| Tamaño | 50-200 MB | 200-500 KB |
| Servidor proxy | Necesario (CORS) | Generalmente no |
| Actualización | Semanal/diaria | Cada 30 segundos |

## Repo

`github.com/Ntizar/GBFSSpain` — visor completo, 68 sistemas, funciona con file://

## Bugs encontrados

1. **ID del mapa:** `new MapaGestor('mapa')` vs `<div id="map">` → mapa en blanco sin errores
2. **CORS con file://:** fetch falla, solución: embeber datos en `window.GBFS_SYSTEMS_DATA`
