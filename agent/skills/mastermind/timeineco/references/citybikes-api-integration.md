# CityBikes API — Integración TimeIneco v2.0

## API Overview
- **URL base:** `https://api.citybik.es/v2/`
- **Auth:** Ninguna (API abierta)
- **Rate limit:** No documentado (usar cache 60s)
- **Formato:** JSON

## Endpoints

### Listar redes
```
GET /networks
Response: { networks: [{ id, name, location: { city, country, latitude, longitude } }] }
```

### Red específica (con estaciones)
```
GET /networks/{id}
Response: { network: { name, stations: [{ id, name, latitude, longitude, free_bikes, empty_slots, timestamp }] } }
```

## Redes en España (74)

| Ciudad | ID | Nombre | Estaciones |
|--------|-----|--------|-----------|
| Madrid | `bicimad` | BiciMAD | 642 |
| Barcelona | `bicing` | Bicing | 543 |
| Barcelona | `ambici-amb` | Ambici | — |
| Valencia | `valenbisi` | Valenbisi | — |
| Valencia | `mibisivalencia` | MIBISI | — |
| Sevilla | `sevici` | Sevici | — |
| Bilbao | `bilbon-bizi` | Bilbaobizi | — |
| Bilbao | `bizkaibizi-bilbao` | Bizkaibizi | — |
| Zaragoza | `bizi` | Bizi | — |
| Palma | `bicipalma` | Bicipalma | — |
| Las Palmas | `sitycleta-las-palmas-...` | Sitycleta | — |
| San Sebastián | `dbizi` | Dbizi | — |
| Vitoria | `mugibike` | MugiBIKE | — |
| Pamplona | `nbici` | nbici | — |
| Santander | `tuebici` | TUeBICI | — |
| Gijón | `gijon` | Gijón Bici | — |
| Girona | `girocleta` | Girocleta | — |
| Valladolid | `biki` | BIKI | — |
| Burgos | `bicibur` | BiciBur | — |
| Logroño | `bicilog` | BiciLog | — |
| León | `alsa-nextbike-leon` | Alsa nextbike | — |
| Castellón | `bicicas` | Bicicas | — |
| Alicante/Elche | `bicielx` | Bicielx | — |
| + 52 redes más | ... | ... | ... |

## Mapeo ciudad → network IDs (en citybikes.js)

```javascript
const CITY_NETWORKS = {
  'madrid':      ['bicimad'],
  'barcelona':   ['bicing', 'ambici-amb'],
  'valencia':    ['valenbisi', 'mibisivalencia'],
  'sevilla':     ['sevici'],
  'bilbao':      ['bilbon-bizi', 'bizkaibizi-bilbao'],
  'zaragoza':    ['bizi'],
  'palma':       ['bicipalma'],
  // ... más ciudades
};
```

## Funciones del módulo (js/citybikes.js)

```javascript
// Obtener estaciones para una ciudad
const stations = await CityBikes.getStationsForCity('madrid');

// Filtrar por radio (metros)
const nearby = CityBikes.stationsWithinRadius(stations, lat, lng, 500);

// Resumen de estaciones cercanas
const summary = CityBikes.summarizeNearby(nearby);
// → { count, total_bikes, total_slots, min_distance_m, avg_bikes, networks, availability_pct }
```

## Server endpoints (server.mjs)

```
GET /citybikes/networks          → Lista de redes (cache 5min)
GET /citybikes/:networkId        → Estaciones de una red (cache 60s)
GET /citybikes/city/:cityName    → Buscar redes por ciudad
```

## Ejemplo real: Plaza Mayor Madrid

```
5 estaciones bici < 250m:
  32 - Plaza de la Provincia: 113m (4 bicis)
  31 - Mayor: 117m (1 bici)
  9 - Plaza de San Miguel: 179m (2 bicis)
  1 - Metro Sol: 200m (2 bicis)
  25B - Plaza de Celenque B: 244m (6 bicis)
```
