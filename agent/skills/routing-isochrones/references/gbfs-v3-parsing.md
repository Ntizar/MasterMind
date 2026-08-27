# GBFS v3.0 — Guía de Parsing y Pitfalls

**Creado:** 2026-06-23 | **Actualizado:** 2026-06-25
**Contexto:** Debug de GBFSSpain — visor de bicicletas compartidas en España

## Estructura de anidamiento GBFS v3.0

### Discovery (gbfs.json)

```json
{
  "version": "3.0",
  "last_updated": "...",
  "ttl": 0,
  "data": {
    "feeds": [
      {
        "name": "station_status",
        "url": "https://.../station_status",
        "frequency": null,
        "since": "2026-06-23T12:00:00Z"
      }
    ]
  }
}
```

**Clave:** Los feeds están dentro de `data.feeds`, NO directamente en `feeds`.
**Clave:** Cada feed usa `url` (no `file` como en algunos parsers antiguos).

### Feed individual (station_status)

```json
{
  "last_updated": "...",
  "ttl": 0,
  "data": {
    "stations": [
      {
        "station_id": "3",
        "num_vehicles_available": 17,
        "num_vehicles_disabled": 0,
        "num_docks_available": 12,
        "num_docks_disabled": 0,
        "last_reported": "2026-06-25T15:13:08.727Z",
        "is_installed": true,
        "is_renting": true,
        "is_returning": true,
        "vehicle_docks_available": [...],
        "vehicle_types_available": [...]
      }
    ]
  }
}
```

**Clave:** Los datos están dentro de `data.stations`, NO directamente en `stations`.
**Clave:** Hay DOBLE anidamiento: `response.data.data.stations`

### Feed individual (station_information) — CAMPO name COMPLEJO

```json
{
  "data": {
    "stations": [
      {
        "station_id": "3",
        "name": [
          {"text": "Plaza De Pontevedra", "language": "en"},
          {"text": "Plaza De Pontevedra", "language": "es"},
          {"text": "Pl. de Pontevedra", "language": "gl"}
        ],
        "lat": 43.3680112,
        "lon": -8.4066505,
        "address": "R. San Andrés, 164",
        "capacity": 29,
        "is_charging_station": true,
        "vehicle_types_capacity": [...],
        "vehicle_docks_capacity": [...]
      }
    ]
  }
}
```

**Clave v3.0:** El campo `name` es un **array de objetos** `[{text, language}]`, NO un string.
**Clave v3.0:** `is_installed`/`is_renting` son **booleanos** `true/false`, NO enteros `0/1`.
**Clave v3.0:** `vehicle_types_capacity` reemplaza a `bike_type_ids`.

## Diferencias completas v2.x vs v3.0

| Campo / Estructura | v2.x (Nextbike, Bird, Dott) | v3.0 (Public Bike System, Getaround, etc.) |
|---|---|---|
| Discovery feeds | `response.data.feeds[].file` | `response.data.feeds[].url` |
| Feed stations | `response.data.stations` | `response.data.data.stations` |
| Bikes disponibles | `num_bikes_available` | `num_vehicles_available` |
| Docks disponibles | `num_docks_available` | `num_docks_available` (igual) |
| Station name | `string` | `[{text: "...", language: "es"}]` |
| is_installed | `0` / `1` (entero) | `true` / `false` (booleano) |
| is_renting | `0` / `1` (entero) | `true` / `false` (booleano) |
| Tipos bici | `bike_type_ids` | `vehicle_types_capacity` |
| Status field | `is_installed: 0` | `status: "IN_SERVICE"` |

## Patrón de parsing universal (v2.x + v3.0)

### Discovery

```javascript
// Soporta ambos formatos
const rawFeeds = (response.data && response.data.feeds) || response.feeds || [];
const feeds = rawFeeds.map(feed => ({
    nombre: feed.name,
    url: feed.url || new URL(feed.file, discoveryUrl).href
}));
```

### Stations (station_status + station_information)

```javascript
// Doble anidamiento v3.0 + fallback v2.x
const stations = (response.data && response.data.stations) ||
                 (response.data && response.data.data && response.data.data.stations) || [];

// Campo name: array v3.0 o string v2.x
function extraerNombre(name) {
    if (!name) return null;
    if (typeof name === 'string') return name;
    if (Array.isArray(name)) {
        const es = name.find(n => n.language === 'es');
        const en = name.find(n => n.language === 'en');
        return (es || en || name[0])?.text || null;
    }
    return null;
}

// Bicis: v3.0 num_vehicles_available, v2.x num_bikes_available
const bikes = station.num_vehicles_available ?? station.num_bikes_available ?? 0;

// Estado: booleanos v3.0, enteros v2.x
const isInstalled = station.is_installed === true || station.is_installed === 1;
const isRenting = station.is_renting === true || station.is_renting === 1;
```

## Pitfalls CRÍTICOS

### 1. DOBLE anidamiento `data.data.stations`

El discovery tiene `data.feeds[]`, y cada feed individual también tiene `data.stations[]`.
Esto significa que al parsear un feed individual, los datos están en `response.data.data.stations`.

```javascript
// ❌ MAL — solo un nivel de anidamiento
const stations = response.data.stations;

// ✅ BIEN — doble nivel con fallback
const stations = (response.data && response.data.stations) ||
                 (response.data && response.data.data && response.data.data.stations) || [];
```

### 2. Discovery: `data.feeds` no `feeds`

```javascript
// ❌ MAL
const feeds = response.feeds;

// ✅ BIEN
const feeds = (response.data && response.data.feeds) || response.feeds || [];
```

### 3. Feed URLs: `url` no `file`

```javascript
// ✅ BIEN
const feedUrl = feed.url || new URL(feed.file, discoveryUrl).href;
```

### 4. Campo name es array en v3.0

```javascript
// ❌ MAL — asume string
const name = station.name;

// ✅ BIEN — extraer de array multilingüe
const name = extraerNombre(station.name);
// → "Plaza De Pontevedra"
```

### 5. is_installed/is_renting son booleanos en v3.0

```javascript
// ❌ MAL — solo funciona con enteros
const active = station.is_installed === 1;

// ✅ BIEN — soporta ambos
const active = station.is_installed === true || station.is_installed === 1;
```

## Auditoría de APIs GBFS España (verificado 2026-06-25)

**68 sistemas catalogados**, probados con `User-Agent: GBFSSpain/2.0-Audit`, timeout 10s.

### Resultados

| Estado | Cantidad | % |
|---|---|---|
| ✅ Responden | 64 | 94% |
| ❌ Muertas (404/403) | 4 | 6% |
| 📐 Con datos de estaciones | 37 | 54% |
| ⚠️ Responden sin estaciones | 27 | 40% |

### APIs muertas

| Sistema | Error |
|---|---|
| BBK Klimabizi | HTTP 404 Not Found |
| Dott Ibiza | HTTP 403 Forbidden |
| Dott La-Manga | HTTP 403 Forbidden |
| Ontibici | HTTP 404 Not Found |

### APIs responden sin datos de estaciones (0 feeds o sin station_*)

**Getaround** (25 sistemas): Responden OK, 4 feeds cada uno, pero **NO tienen station_information ni station_status**. Solo system_information, system_pricing_plans, gbfs_versions, vehicle_types.

**Bird** (7 sistemas): Responden OK, 0 feeds.

**Dott** (7 sistemas, excluyendo 2 muertas): Responden OK, 0 feeds.

**Nextbike** (14 sistemas): Responden OK, 0 feeds.

**Cooltra Barcelona**: Responde OK, 5 feeds, pero sin station_status/station_information.

### Plataformas que funcionan completamente

| Plataforma | Sistemas | Feeds | Notas |
|---|---|---|---|
| Public Bike System (JCDecaux) | 11 | 8 cada uno | BiciMAD, Bicing, Bicicoruña, Bilbao Bizi, Bizi, Dbizi, Sevici, Valenbisi, Valladolid, BicinRivas |
| Donkey Republic | 1 | 8 | Donkey Barcelona |
| Ganxeta | 1 | 7 | Ganxeta Reus |

### Tiempos de respuesta típicos

- Public Bike System: 120-200ms
- Getaround: 170-650ms
- Nextbike: 120-160ms
- Bird/Dott: 60-200ms
- Cooltra: 400-650ms

## Ejemplo completo: Bicing Barcelona

```javascript
// 1. Discovery
const gbfs = await fetch('https://barcelona.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json')
    .then(r => r.json());
const rawFeeds = gbfs.data?.feeds || [];
// → 8 feeds

// 2. Cargar station_status
const statusFeed = rawFeeds.find(f => f.name === 'station_status');
const status = await fetch(statusFeed.url).then(r => r.json());
const stations = status.data?.data?.stations || status.data?.stations || [];
// → 537 estaciones

// 3. Cargar station_information
const infoFeed = rawFeeds.find(f => f.name === 'station_information');
const info = await fetch(infoFeed.url).then(r => r.json());
const infoStations = info.data?.data?.stations || info.data?.stations || [];
// → 537 estaciones con datos estáticos

// 4. Combinar
const combined = stations.map(s => {
    const base = infoStations.find(i => i.station_id === s.station_id) || {};
    return {
        id: s.station_id,
        name: extraerNombre(base.name) || s.station_id,
        lat: base.lat,
        lon: base.lon,
        bikes: s.num_vehicles_available ?? s.num_bikes_available ?? 0,
        docks: s.num_docks_available ?? 0,
        capacity: base.capacity || 0,
        active: (s.is_installed === true || s.is_installed === 1) &&
                (s.is_renting === true || s.is_renting === 1)
    };
});
```

## Versiones GBFS

| Versión | Estructura discovery | Feed stations | Campo bicis | Name field |
|---|---|---|---|---|
| v1.1 | `feeds[].file` | `stations` | `bikes_available` | string |
| v2.3 | `data.feeds[].file` | `data.stations` | `num_bikes_available` | string |
| v3.0 | `data.feeds[].url` | `data.data.stations` | `num_vehicles_available` | `[{text, language}]` |

**Nota:** Nextbike en España usa v2.3. El parser debe soportar ambos formatos.

## Referencias

- Bicing Barcelona: `https://barcelona.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- BiciMAD Madrid: `https://madrid.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- Bicicoruña: `https://acoruna.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- MobilityData GBFS spec: `github.com/MobilityData/gbfs/blob/master/specification.md`
- GBFSSpain repo: `github.com/Ntizar/GBFSSpain` (visor con Kaizen CSS + API checker)
