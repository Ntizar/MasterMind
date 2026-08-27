# GBFS v3.0 — Diferencias estructurales con v2.x

## Resumen

GBFS v3.0 (General Bikeshare Feed Specification) cambia la estructura JSON respecto a v2.x. Los campos están anidados bajo `data.*` en vez de estar en la raíz, y algunos campos cambian de nombre o tipo.

## Diferencias clave

### 1. Discovery (gbfs.json)

**v2.x:**
```json
{
  "feeds": [
    {"name": "station_status", "url": "..."},
    {"name": "station_information", "url": "..."}
  ]
}
```

**v3.0:**
```json
{
  "last_updated": "2026-06-25T15:13:05Z",
  "ttl": 30,
  "data": {
    "feeds": [
      {"name": "station_status", "url": "https://..."},
      {"name": "station_information", "url": "https://..."}
    ]
  },
  "version": "3.0"
}
```

**Parsing correcto:**
```javascript
const rawFeeds = (data.data && data.data.feeds) || data.feeds || [];
```

### 2. Station Status (station_status)

**v2.x:**
```json
{
  "stations": [
    {
      "station_id": "123",
      "num_bikes_available": 5,
      "num_docks_available": 10,
      "is_installed": 1,
      "is_renting": 1
    }
  ]
}
```

**v3.0:**
```json
{
  "data": {
    "stations": [
      {
        "station_id": "123",
        "num_vehicles_available": 5,
        "num_docks_available": 10,
        "is_installed": true,
        "is_renting": true,
        "vehicle_types_available": [
          {"vehicle_type_id": "FIT", "count": 3},
          {"vehicle_type_id": "BOOST", "count": 2}
        ]
      }
    ]
  }
}
```

**Cambios:**
- `num_bikes_available` → `num_vehicles_available`
- `is_installed`, `is_renting` son booleanos (no enteros 0/1)
- Nuevo campo: `vehicle_types_available`

**Parsing correcto:**
```javascript
const stations = (data.data && data.data.stations) || data.stations || [];

// Para bicis disponibles
const bicis = estacion.num_vehicles_available ?? estacion.num_bikes_available ?? null;

// Para estado
const isInstalled = estacion.is_installed === true || estacion.is_installed === 1;
const isRenting = estacion.is_renting === true || estacion.is_renting === 1;
```

### 3. Station Information (station_information)

**v2.x:**
```json
{
  "stations": [
    {
      "station_id": "123",
      "name": "Plaza Mayor",
      "lat": 40.4155,
      "lon": -3.7074,
      "capacity": 20
    }
  ]
}
```

**v3.0:**
```json
{
  "data": {
    "stations": [
      {
        "station_id": "123",
        "name": [
          {"text": "Plaza Mayor", "language": "es"},
          {"text": "Main Square", "language": "en"},
          {"text": "Plaça Major", "language": "ca"}
        ],
        "lat": 40.4155,
        "lon": -3.7074,
        "capacity": 20,
        "vehicle_types_capacity": [
          {"vehicle_type_ids": [], "count": 0}
        ]
      }
    ]
  }
}
```

**Cambios:**
- `name` es un array de objetos `[{text, language}]` (no string)
- Nuevo campo: `vehicle_types_capacity`

**Parsing correcto:**
```javascript
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
```

### 4. Platform patterns (por plataforma)

| Plataforma | Versiones | Feeds | Notas |
|---|---|---|---|
| Public Bike System (JCDecaux) | v3.0 | 8 | Madrid, Barcelona, Sevilla, Valencia, etc. |
| Getaround | v3.0 | 4 | Solo vehicle_types, system_information, station_information, station_status |
| Nextbike | v2.3 | 0 feeds (responde pero vacío) | API responde 200 pero sin datos |
| Bird | v2.3 | 0 feeds | Similar a Nextbike |
| Dott | v2.3 | 0 feeds | Algunos dan 403 |
| Cooltra | v3.0 | 5 | Sin station_information |
| Cyclocity | v3.0 | 5 | Similar a Cooltra |

### 5. API Health Check patterns

**URL de discovery:** Cada sistema tiene una URL de auto-discovery que retorna el JSON con la lista de feeds.

**Criterios de health check:**
- ✅ **OK**: HTTP 200 + JSON válido + feeds > 0 + estaciones > 0
- ⚠️ **Partial**: HTTP 200 + JSON válido + feeds = 0 (API responde pero sin datos)
- ❌ **Error**: HTTP 4xx/5xx o timeout
- 🐌 **Slow**: > 3000ms de respuesta

**Timeout recomendado:** 8-10 segundos (algunas APIs son lentas)

**User-Agent:** `GBFSSpain/2.0-Audit` o similar

## Code pattern completo

```javascript
class GBFSParser {
  async loadDiscovery(discoveryUrl) {
    const data = await this._peticion(discoveryUrl);
    if (!data) return { feeds: [], version: null };
    
    // v3.0: data.data.feeds | v2.x: data.feeds
    const rawFeeds = (data.data && data.data.feeds) || data.feeds || [];
    if (rawFeeds.length === 0) return { feeds: [], version: data.version || null };
    
    const feeds = rawFeeds.map(feed => ({
      nombre: feed.name,
      url: feed.url || this._construirUrl(discoveryUrl, feed.file || feed.name)
    }));
    
    return { feeds, version: data.version || null };
  }
  
  parseStationStatus(data) {
    const stations = (data?.data?.stations) || data?.stations || [];
    return stations.map(est => ({
      id: est.station_id,
      nombre: this._extraerNombre(est.name) || `Estación ${est.station_id}`,
      lat: est.lat || 0,
      lon: est.lon || 0,
      bicis: est.num_vehicles_available ?? est.num_bikes_available ?? null,
      docks: est.num_docks_available ?? null,
      estado: (est.is_installed === true || est.is_installed === 1)
        ? ((est.is_renting === true || est.is_renting === 1) ? 'activo' : 'no_alquila')
        : 'inactivo'
    }));
  }
  
  _extraerNombre(name) {
    if (!name) return null;
    if (typeof name === 'string') return name;
    if (Array.isArray(name)) {
      const es = name.find(n => n.language === 'es');
      return (es || name[0])?.text || null;
    }
    return null;
  }
}
```

## Datos de sesión (GBFSSpain, 2026-06-25)

- **68 sistemas** en catálogo
- **64/68 responden** (94%)
- **37 con datos de estaciones completos**
- **27 responden sin datos** (Bird, Dott, Nextbike, Getaround)
- **4 APIs muertas** (404/403)

## Referencias

- [GBFS Spec v3.0](https://github.com/MobilityData/gbfs/blob/master/gbfs.md)
- [GBFS Auto-discovery](https://github.com/MobilityData/gbfs/blob/master/gbfs-auto-discovery.md)
- Repo: `github.com/Ntizar/GBFSSpain`
